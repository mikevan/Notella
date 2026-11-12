"""Allowlisted local training backend. No shell commands accepted from API callers."""
import hashlib,json,os,subprocess,sys,threading,uuid,shutil
from datetime import datetime,timezone
from pathlib import Path
from .core import check,canonical,ValidationError

def now():return datetime.now(timezone.utc).isoformat()

class Jobs:
    def __init__(self,service,engine=None,python=None,models=None):
        self.service=service;self.engine=Path(engine).resolve() if engine else None
        self.python=Path(python).resolve() if python else Path(sys.executable)
        self.models={k:Path(v).resolve() for k,v in (models or {}).items()}
        self.root=service.root/'jobs';self.root.mkdir(exist_ok=True);self.lock=self.root/'gpu.lock'
        self.state_lock=threading.RLock()

    def get(self,identity):
        check(isinstance(identity,str) and len(identity)==32 and all(c in '0123456789abcdef' for c in identity),'Invalid job ID')
        p=self.root/identity/'job.json'
        if not p.exists():raise FileNotFoundError(identity)
        with self.state_lock:return json.loads(p.read_text(encoding='utf-8'))

    def start(self,plan_id):
        check(self.engine is not None and (self.engine/'train_lora.py').is_file(),'Training backend is not configured')
        plan=self.service.get('plans',plan_id)
        check(plan['baseModel'] in self.models,'Model is not configured on this server')
        model=self.models[plan['baseModel']];check(model.is_dir(),'Configured model directory is missing')
        check(self.python.is_file(),'Configured Python executable is missing')
        c=self.service.get('curricula',plan['curriculumId']);o=self.service.get('ontologies',c['ontologyId'])
        check(c['splits']['validation']>0,'Training requires a separate validation split')
        identity=uuid.uuid4().hex
        try:fd=os.open(self.lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY)
        except FileExistsError:raise ValidationError('A training job holds the GPU lock; inspect it before starting another')
        os.write(fd,canonical(dict(jobId=identity,createdAt=now())).encode());os.close(fd)
        folder=self.root/identity;folder.mkdir();data=folder/'dataset';data.mkdir()
        state=dict(id=identity,planId=plan_id,status='starting',createdAt=now(),releaseEligible=False)
        def save():
            with self.state_lock:
                tmp=folder/'job.tmp';tmp.write_text(canonical(state)+'\n',encoding='utf-8');os.replace(tmp,folder/'job.json')
        try:
            manifest=dict(profile='notella-lora-v1',releaseEligible=False,ontology=o,ontologyId=c['ontologyId'],excludedPromptHashes=c['excludedPromptHashes'],splits={})
            for split in ('train','validation','test'):
                rows=[e for e in c['examples'] if e['split']==split];p=data/(split+'.jsonl')
                p.write_text(''.join(canonical(r)+'\n' for r in rows),encoding='utf-8')
                manifest['splits'][split]=dict(file=p.name,examples=len(rows),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
            (data/'manifest.json').write_text(canonical(manifest),encoding='utf-8')
            from .training_profile import verify
            verify(data)
            engine_snapshot=folder/'engine';engine_snapshot.mkdir()
            for source in self.engine.glob('*.py'):shutil.copy2(source,engine_snapshot/source.name)
            api_snapshot=folder/'api-source'/'notella';api_snapshot.mkdir(parents=True)
            for source in Path(__file__).resolve().parent.glob('*.py'):shutil.copy2(source,api_snapshot/source.name)
            command=[str(self.python),str(engine_snapshot/'train_lora.py'),'--dataset',str(data),'--base-model',str(model),'--output',str(folder/'adapter'),
                '--domain','--qlora','--cpu-frozen-layers','--max-steps',str(plan['steps']),'--checkpoint-steps',str(min(plan['steps'],100)),
                '--lora-rank',str(plan['rank']),'--lora-alpha',str(plan['rank']*2),'--learning-rate',str(plan['learningRate']),'--initial-loss-scale','256']
            # Original engine alpha is bounded at 256; the public plan bounds rank to 128.
            state['command']=command;state['engineSha256']=hashlib.sha256((self.engine/'train_lora.py').read_bytes()).hexdigest()
            state['sourceSha256']={str(p.relative_to(folder)):hashlib.sha256(p.read_bytes()).hexdigest() for base in (engine_snapshot,api_snapshot) for p in base.glob('*.py')}
            env=os.environ.copy();env.update(HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=str(api_snapshot.parent))
            with (folder/'stdout.log').open('wb') as stdout,(folder/'stderr.log').open('wb') as stderr:
                process=subprocess.Popen(command,cwd=folder,env=env,stdout=stdout,stderr=stderr,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
            state.update(status='running',pid=process.pid);save()
        except Exception:
            state.update(status='failed',finishedAt=now());save();self.lock.unlink(missing_ok=True);raise
        def monitor():
            code=process.wait();state.update(status='completed' if code==0 else 'failed',exitCode=code,finishedAt=now())
            try:save()
            finally:self.lock.unlink(missing_ok=True)
        threading.Thread(target=monitor,daemon=True).start()
        return state.copy()
