"""Matched generation on frozen scenario prefixes; no repair or optimizer work."""
import argparse,copy,hashlib,json,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from notella import Notella
from notella.core import canonical
from notella.scenarios import validate_scenario
from notella.scenario_scoring import score_scenario_output

def main():
 p=argparse.ArgumentParser();p.add_argument('--condition',choices=['base','adapted'],required=True);p.add_argument('--adapter',type=Path);p.add_argument('--run',choices=['scenario-model-v5'],default='scenario-model-v5');a=p.parse_args()
 folder=Path(__file__).resolve().parent;out=ROOT/'runtime'/a.run;dest=out/(a.condition+'-generation.json');journal=out/(a.condition+'-generation.jsonl')
 if dest.exists() or journal.exists():raise ValueError('Preserve earlier outputs; no silent restart')
 if (a.condition=='adapted')!=(a.adapter is not None):raise ValueError('Adapter required only for adapted condition')
 prepared=json.loads((out/'prepared.json').read_text(encoding='utf-8'));api=Notella(out/'store');corpus=api.get('curricula',prepared['curriculumId']);ontology=api.get('ontologies',prepared['ontologyId'])
 assert hashlib.sha256((folder/'development-scenarios.json').read_bytes()).hexdigest()==prepared['evaluationSha256'],'Frozen evaluation changed'
 scenarios=json.loads((folder/'development-scenarios.json').read_text(encoding='utf-8'));records={s['id']:s for s in scenarios}
 import torch
 from transformers import AutoTokenizer,AutoModelForCausalLM,BitsAndBytesConfig
 from transformers.integrations import sdpa_attention
 torch.backends.cuda.enable_flash_sdp(False);torch.backends.cuda.enable_math_sdp(False);torch.backends.cuda.enable_mem_efficient_sdp(True);sdpa_attention.use_gqa_in_sdpa=lambda attention_mask,key:False
 model_path=Path(prepared['model']);tokenizer=AutoTokenizer.from_pretrained(model_path,local_files_only=True)
 model=AutoModelForCausalLM.from_pretrained(model_path,local_files_only=True,quantization_config=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type='nf4',bnb_4bit_use_double_quant=True,bnb_4bit_compute_dtype=torch.float16),device_map={'':0},dtype=torch.float16,attn_implementation='sdpa').eval()
 if a.adapter:
  from peft import PeftModel
  model=PeftModel.from_pretrained(model,a.adapter,local_files_only=True,is_trainable=False).eval()
 cached={}
 if a.condition=='base':
  previous=json.loads((ROOT/'experiments/scenario-model-v4/evidence/base-generation.json').read_text(encoding='utf-8'))
  for row in previous['results']:cached[row['id']]=row
 results=[];generated_states={s['id']:[] for s in scenarios}
 with journal.open('x',encoding='utf-8') as stream:
  for e in corpus['examples']:
   if e['split']!='validation':continue
   scenario=next(s for s in scenarios if e['id'].startswith(s['id']+'-step-'));frame=json.loads(e['messages'][-2]['content']);cutoff=frame['asOfMs']
   messages=e['messages'][:-1];prompt=tokenizer.apply_chat_template(messages,tokenize=False,add_generation_prompt=True,enable_thinking=False)
   if e['id'] in cached:
    row=copy.deepcopy(cached[e['id']])
    assert row['promptSha256']==hashlib.sha256(prompt.encode()).hexdigest(),'Cached prompt changed'
    rescored=score_scenario_output(ontology,scenario,cutoff,row['output'],token_limit_reached=row['score']['tokenLimitReached'])
    assert rescored==row['score'],'Cached score changed'
    row['reusedFrom']='scenario-model-v4/base-generation.json'
    results.append(row);stream.write(json.dumps(row,ensure_ascii=False)+'\n');stream.flush()
    if row['score']['schemaValid']:generated_states[scenario['id']].append(dict(asOfMs=cutoff,target=json.loads(row['output'])))
    print(json.dumps(dict(condition=a.condition,id=e['id'],reused=True)),flush=True)
    continue

   assert all(m['content'] in prompt for m in messages)
   inputs=tokenizer(prompt,return_tensors='pt',add_special_tokens=False).to('cuda')
   if inputs.input_ids.shape[1]+1536>4096:raise ValueError('Input exceeds bounded generation context; no truncation')
   start=time.monotonic()
   with torch.inference_mode():tokens=model.generate(**inputs,max_new_tokens=1536,do_sample=False,pad_token_id=tokenizer.eos_token_id)
   output_tokens=int(tokens.shape[1]-inputs.input_ids.shape[1]);text=tokenizer.decode(tokens[0,inputs.input_ids.shape[1]:],skip_special_tokens=True)
   limit=output_tokens>=1536 and int(tokens[0,-1])!=tokenizer.eos_token_id
   score=score_scenario_output(ontology,scenario,cutoff,text,token_limit_reached=limit)
   row=dict(id=e['id'],scenarioId=scenario['id'],asOfMs=cutoff,promptSha256=hashlib.sha256(prompt.encode()).hexdigest(),output=text,outputSha256=hashlib.sha256(text.encode()).hexdigest(),seconds=time.monotonic()-start,inputTokens=int(inputs.input_ids.shape[1]),outputTokens=output_tokens,score=score)
   results.append(row);stream.write(json.dumps(row,ensure_ascii=False)+'\n');stream.flush()
   if score['schemaValid']:generated_states[scenario['id']].append(dict(asOfMs=cutoff,target=json.loads(text)))
   print(json.dumps(dict(condition=a.condition,id=e['id'],seconds=round(row['seconds'],2),outputTokens=output_tokens,contractValid=score['contractValid'],criticalityMatch=score['criticalityMatch'],fullStateMatch=score['fullStateMatch'])),flush=True)
 trajectory=[]
 for scenario in scenarios:
  row=dict(scenarioId=scenario['id'],complete=len(generated_states[scenario['id']])==len(scenario['steps']),contractValid=False)
  if row['complete']:
   try:
    candidate=copy.deepcopy(scenario);candidate['steps']=generated_states[scenario['id']];validate_scenario(ontology,candidate);row['contractValid']=True
   except (ValueError,TypeError,KeyError) as error:row['error']=str(error)
  trajectory.append(row)
 metrics=['jsonValid','schemaValid','contractValid','criticalityMatch','assessmentStatusMatch','assessmentEvidenceMatch','nodesMatch','edgesMatch','contractAndDecisionMatch','fullStateMatch']
 report=dict(condition=a.condition,curriculumId=prepared['curriculumId'],evaluationSha256=prepared['evaluationSha256'],evaluatorSha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),scorerSha256=hashlib.sha256((ROOT/'notella/scenario_scoring.py').read_bytes()).hexdigest(),adapterSha256=hashlib.sha256((a.adapter/'adapter_model.safetensors').read_bytes()).hexdigest() if a.adapter else None,total=len(results),counts={k:sum(r['score'][k] for r in results) for k in metrics},trajectories=trajectory,results=results,releaseEligible=False,semanticAccuracyMeasured=False,
  limits=['All eighteen v4 prefixes are now known diagnostics; fresh F-1120/F-1230 frozen before v5 training; same author, not independent field evidence.','Full visible-prefix reconstruction, not rollout from previous generated states.','Topology agreement follows reference conventions and excludes exact prose matching.','Contract-valid decision agreement is not complete semantic correctness.'])
 dest.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in report.items() if k not in ('results','limits')},indent=2),flush=True)
if __name__=='__main__':main()
