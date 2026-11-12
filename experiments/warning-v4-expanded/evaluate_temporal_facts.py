"""Matched development generation. Same prompts and decoding for base and adapter."""
import argparse,hashlib,json,sys,time
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from notella import Notella
from notella.core import canonical,validate_schema
from notella.scoring import score_output
from profiles.layertime.temporal_features import derive_temporal_fact

def main():
 p=argparse.ArgumentParser();p.add_argument('--model',type=Path,required=True);p.add_argument('--adapter',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 if a.output.exists():raise ValueError('Preserve existing evaluation; use a new output path')
 source_ids=[];examples=[];case_groups={}
 for group,location in [('primary','warning-v4-expanded'),('robustness','warning-v4-robustness')]:
  prepared=json.loads((ROOT/'runtime'/location/'prepared.json').read_text())
  service=Notella(ROOT/'runtime'/location/'store');part=service.get('curricula',prepared['curriculumId']);source_ids.append(prepared['curriculumId'])
  ontology=service.get('ontologies',part['ontologyId'])
  for e in part['examples']:
   if e['split']=='validation':examples.append(e);case_groups[e['id']]=group
 corpus=dict(examples=examples);prepared=dict(curriculumId=source_ids[0])
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
 results=[]
 for example in corpus['examples']:
  if example['split']!='validation':continue
  messages=[dict(m) for m in example['messages'][:-1]]
  raw=json.loads(messages[1]['content']);observation=next(f['value'] for f in raw['facts'] if f['factId']=='capture_summary')
  receipt=derive_temporal_fact(observation)
  model_fact=dict(factId='computed_temporal_link',value=dict(receipt['value']['measurement'],configuredWindowMs=receipt['value']['configuredWindowMs']))
  raw['facts'].append(model_fact);messages[1]['content']=json.dumps(raw,sort_keys=True)
  prompt=tokenizer.apply_chat_template(messages,tokenize=False,add_generation_prompt=True,enable_thinking=False)
  for message in messages:
   if message['content'] not in prompt:raise ValueError('Native template dropped message content')
  inputs=tokenizer(prompt,return_tensors='pt',add_special_tokens=False).to('cuda')
  if inputs.input_ids.shape[1]+384>4096:raise ValueError('Development input exceeds bounded context')
  start=time.monotonic()
  with torch.inference_mode():output=model.generate(**inputs,max_new_tokens=384,do_sample=False,pad_token_id=tokenizer.eos_token_id)
  text=tokenizer.decode(output[0,inputs.input_ids.shape[1]:],skip_special_tokens=True)
  row=dict(id=example['id'],promptSha256=hashlib.sha256(prompt.encode()).hexdigest(),output=text,outputSha256=hashlib.sha256(text.encode()).hexdigest(),seconds=time.monotonic()-start,inputTokens=int(inputs.input_ids.shape[1]),outputTokens=int(output.shape[1]-inputs.input_ids.shape[1]),schemaValid=False)
  target=json.loads(example['messages'][-1]['content'])
  assessment=score_output(text,target,ontology['outputSchema'],['posture','combinedTrigger','evidenceClass'])
  row.update(assessment);row['caseGroup']=case_groups[example['id']];row['derivedTemporalReceipt']=receipt;row['modelVisibleTemporalFact']=model_fact
  results.append(row);print(json.dumps({k:v for k,v in row.items() if k!='output'}),flush=True)
 report=dict(condition='adapted' if a.adapter else 'base',curriculumId=prepared['curriculumId'],split='development-validation',
  evaluatorSha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
  baseIntakeManifestSha256=hashlib.sha256((a.model/'intake-manifest.json').read_bytes()).hexdigest(),
  adapterSha256=hashlib.sha256((a.adapter/'adapter_model.safetensors').read_bytes()).hexdigest() if a.adapter else None,
  promptVariant='derived-temporal-facts-v1',sourceCurriculumIds=source_ids,noWeightUpdates=True,
  featureSourceSha256=hashlib.sha256((ROOT/'profiles/layertime/temporal_features.py').read_bytes()).hexdigest(),
  arithmeticSourceSha256=hashlib.sha256((ROOT/'notella/correlation.py').read_bytes()).hexdigest(),
  model=str(a.model),adapter=str(a.adapter) if a.adapter else None,decoding=dict(doSample=False,maxNewTokens=384),
  schemaPasses=sum(r['schemaValid'] for r in results),decisionFieldMatches=sum(r['decisionFieldsMatch'] for r in results),total=len(results),
  semanticAccuracyMeasured=False,limitations=['Post-hoc feature-representation diagnostic on ten development cases and six related robustness probes; not independent qualification.','Decision-field agreement does not validate the explanation.'],results=results)
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='results'}),flush=True)

if __name__=='__main__':main()
