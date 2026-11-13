"""Archive runtime records without model/optimizer weights; preserve exact bytes."""
import argparse,hashlib,json,re,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];DEST=ROOT/'archive/morphology-v1'
TEXT={'.py','.ps1','.json','.jsonl','.md','.txt','.jinja','.log'}
STATE={'training_args.bin','scheduler.pt','scaler.pt','rng_state.pth'}
SECRET=re.compile(rb'\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{30,}|AKIA[A-Z0-9]{16}|sk-[A-Za-z0-9]{24,})\b')

def main():
 paths=subprocess.run(['rg','--files','--hidden','--no-ignore','-g','!**/__pycache__/**','-g','!**/*.pyc','runtime'],cwd=ROOT,capture_output=True,text=True,check=True).stdout.splitlines()
 entries=[];excluded=[];blobs={};checked=set();kinds={}
 for name in sorted(paths):
  source=ROOT/name;relative=source.relative_to(ROOT).as_posix();data=source.read_bytes();sha=hashlib.sha256(data).hexdigest()
  allowed=source.suffix.lower() in TEXT or source.name in STATE
  record=dict(path=relative,sha256=sha,bytes=len(data),modifiedUtcNs=source.stat().st_mtime_ns)
  if not allowed:
   record['reason']='Model or optimizer binary; retained locally' if source.suffix=='.safetensors' or source.name=='optimizer.pt' else 'Non-document/cache/runtime file; retained locally'
   excluded.append(record);continue
  if sha not in checked and source.suffix.lower() in TEXT:
   text=data.decode('utf-8-sig')
   if SECRET.search(data):raise ValueError('Credential-shaped text requires review: '+relative)
   values=[]
   if source.suffix=='.json':
    try:values=[json.loads(text)]
    except ValueError:pass
   elif source.suffix=='.jsonl':
    for line in text.splitlines():
     try:values.append(json.loads(line))
     except ValueError:pass
   def inspect(value):
    if isinstance(value,dict):
     s=value.get('source')
     if isinstance(s,dict) and 'kind' in s:
      kind=str(s['kind']);kinds[kind]=kinds.get(kind,0)+1
      if kind!='synthetic':raise ValueError('Source permission requires review: '+relative)
     for key,item in value.items():
      if isinstance(item,str) and ((re.fullmatch(r'(?:api[_-]?key|access[_-]?token|auth[_-]?token|bearer[_-]?token|password|secret)',key,re.I) and len(item)>12) or (key.lower()=='token' and re.fullmatch(r'[a-fA-F0-9]{32,}',item))):raise ValueError('Potential credential requires review: '+relative)
      inspect(item)
    elif isinstance(value,list):
     for item in value:inspect(item)
   for value in values:inspect(value)
   checked.add(sha)
  blob='blobs/'+sha+'.artifact';target=DEST/blob
  if sha not in blobs:
   target.parent.mkdir(parents=True,exist_ok=True)
   if target.exists():
    if target.read_bytes()!=data:raise ValueError('Existing archived bytes differ')
   else:target.write_bytes(data)
   blobs[sha]=len(data)
  record['blob']=blob;entries.append(record)
 DEST.mkdir(parents=True,exist_ok=True)
 (DEST/'index.json').write_text(json.dumps(dict(formatVersion='notella.runtime-document-archive.v1',entries=entries),indent=2)+'\n',encoding='utf-8')
 (DEST/'excluded-binaries.json').write_text(json.dumps(dict(files=excluded),indent=2)+'\n',encoding='utf-8')
 summary=dict(includedFiles=len(entries),uniqueBlobs=len(blobs),originalBytes=sum(r['bytes'] for r in entries),archivedBytes=sum(blobs.values()),excludedFiles=len(excluded),excludedBytes=sum(r['bytes'] for r in excluded),sourceKindsInUniqueParsedRecords=kinds,credentialScan='No matches in the configured high-confidence checks; not a formal guarantee',preserved='Exact bytes, hashes and original paths; no redaction of included artifacts')
 (DEST/'summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
