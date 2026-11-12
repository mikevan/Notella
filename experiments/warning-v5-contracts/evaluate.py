"""Matched inference-only contract diagnostic. No generated answer is repaired."""
import argparse,hashlib,json,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from notella.core import canonical
from notella.scoring import score_output
from profiles.layertime.decision_contract import project_observation,inspect_warning_output

def main():
 p=argparse.ArgumentParser();p.add_argument('--model',type=Path,required=True);p.add_argument('--adapter',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 if a.output.exists():raise ValueError('Preserve existing output')
 folder=Path(__file__).resolve().parent;manifest=json.loads((folder/'frozen-inputs.json').read_text())
 for name,key in [('contract.json','contractSha256'),('cases.json','casesSha256')]:
  if hashlib.sha256((folder/name).read_bytes()).hexdigest()!=manifest[key]:raise ValueError('Frozen contract/input hash changed')
 config=json.loads((folder/'contract.json').read_text());cases=json.loads((folder/'cases.json').read_text())
 prepared=[]
 for e in cases:
  raw=json.loads(e['messages'][1]['content']);o=next(f['value'] for f in raw['facts'] if f['factId']=='capture_summary')
  projection=project_observation(o,config['registry'],config['ongoingThreat'])
  prepared.append((e,projection))
 import torch
 from transformers import AutoTokenizer,AutoModelForCausalLM,BitsAndBytesConfig
 from transformers.integrations import sdpa_attention
 torch.backends.cuda.enable_flash_sdp(False);torch.backends.cuda.enable_math_sdp(False);torch.backends.cuda.enable_mem_efficient_sdp(True)
 sdpa_attention.use_gqa_in_sdpa=lambda attention_mask,key:False
 tokenizer=AutoTokenizer.from_pretrained(a.model,local_files_only=True)
 quantization=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type='nf4',bnb_4bit_use_double_quant=True,bnb_4bit_compute_dtype=torch.float16)
 model=AutoModelForCausalLM.from_pretrained(a.model,local_files_only=True,quantization_config=quantization,device_map={'':0},dtype=torch.float16,attn_implementation='sdpa').eval()
 if a.adapter:
  from peft import PeftModel
  model=PeftModel.from_pretrained(model,a.adapter,local_files_only=True,is_trainable=False).eval()
 rows=[]
 for e,projection in prepared:
  row=dict(id=e['id'],group=e['caseGroup'],projection=projection,inputDeferred=not projection['eligibleForModel'])
  if row['inputDeferred']:
   row.update(modelInvoked=False,disposition='needs_review',notCountedAsModelPass=True);rows.append(row);continue
  messages=[dict(role='system',content=config['systemInstruction']),dict(role='user',content=canonical(dict(observation=projection['modelInput'])))]
  prompt=tokenizer.apply_chat_template(messages,tokenize=False,add_generation_prompt=True,enable_thinking=False)
  for m in messages:
   if m['content'] not in prompt:raise ValueError('Native template dropped message content')
  inputs=tokenizer(prompt,return_tensors='pt',add_special_tokens=False).to('cuda')
  if inputs.input_ids.shape[1]+384>4096:raise ValueError('Context budget exceeded')
  start=time.monotonic()
  with torch.inference_mode():generated=model.generate(**inputs,max_new_tokens=384,do_sample=False,pad_token_id=tokenizer.eos_token_id)
  output=tokenizer.decode(generated[0,inputs.input_ids.shape[1]:],skip_special_tokens=True)
  target=json.loads(e['messages'][-1]['content']);score=score_output(output,target,config['outputSchema'],['posture','combinedTrigger','evidenceClass'])
  guard=inspect_warning_output(output,projection,config['outputSchema'],config['allowedStates'])
  row.update(modelInvoked=True,promptSha256=hashlib.sha256(prompt.encode()).hexdigest(),output=output,outputSha256=hashlib.sha256(output.encode()).hexdigest(),
    inputTokens=int(inputs.input_ids.shape[1]),outputTokens=int(generated.shape[1]-inputs.input_ids.shape[1]),seconds=time.monotonic()-start,score=score,guard=guard)
  rows.append(row);print(json.dumps(dict(id=e['id'],matched=score['decisionFieldsMatch'],contractPassed=guard['checksPassed'])),flush=True)
 evaluated=[e for e in rows if e['modelInvoked']]
 groups={group:dict(total=sum(e['group']==group for e in evaluated),
  rawDecisionMatches=sum(e['group']==group and e['score']['decisionFieldsMatch'] for e in evaluated),
  contractPasses=sum(e['group']==group and e['guard']['checksPassed'] for e in evaluated),
  acceptedWrong=sum(e['group']==group and e['guard']['checksPassed'] and not e['score']['decisionFieldsMatch'] for e in evaluated),
  rejectedCorrect=sum(e['group']==group and not e['guard']['checksPassed'] and e['score']['decisionFieldsMatch'] for e in evaluated)) for group in ('primary','robustness','prospective')}
 report=dict(condition='adapted' if a.adapter else 'base',noWeightUpdates=True,groups=groups,inputDeferred=sum(e['inputDeferred'] for e in rows),
   outputRepaired=False,semanticAccuracyMeasured=False,fieldQualification=False,
   evaluatorSha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),frozenInputs=manifest,
   baseIntakeManifestSha256=hashlib.sha256((a.model/'intake-manifest.json').read_bytes()).hexdigest(),
   adapterSha256=hashlib.sha256((a.adapter/'adapter_model.safetensors').read_bytes()).hexdigest() if a.adapter else None,
   sourceSha256={str(file.relative_to(ROOT)):hashlib.sha256(file.read_bytes()).hexdigest() for file in [ROOT/'notella/lineage.py',ROOT/'notella/output_contracts.py',ROOT/'profiles/layertime/decision_contract.py',ROOT/'profiles/layertime/temporal_features.py']},
   limitations=['The typed representation, trusted system instruction and output-state contract change together; this is not an isolated intervention.',
    'The registry contains authored synthetic provenance assertions, not verified field lineage.','Input deferrals and output rejections are not correct model decisions.'],results=rows)
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(condition=report['condition'],groups=groups,inputDeferred=report['inputDeferred'])),flush=True)

if __name__=='__main__':main()
