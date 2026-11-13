"""Same prospective controls and decoding for the two student adapters."""
import argparse,hashlib,json,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from notella import Notella
from notella.core import canonical
from notella.scoring import score_output
from profiles.layertime.decision_contract import inspect_warning_output

def main():
 p=argparse.ArgumentParser();p.add_argument('--condition',choices=['direct','augmented'],required=True);p.add_argument('--adapter',type=Path,required=True);a=p.parse_args()
 out=ROOT/'runtime/student-v1-teacher-augmentation';dest=out/(a.condition+'-historical-controls.json')
 if dest.exists():raise ValueError('Preserve prior evaluation')
 prepared=json.loads((out/'prepared.json').read_text());api=Notella(out/'store');historical=json.loads((ROOT/'runtime/warning-v6-typed-training/prepared.json').read_text());corpus=Notella(ROOT/'runtime/warning-v6-typed-training/store').get('curricula',historical['curriculumId']);ontology=api.get('ontologies',prepared['ontologyId']);contract=json.loads((ROOT/'experiments/warning-v5-contracts/contract.json').read_text())
 import torch
 from transformers import AutoTokenizer,AutoModelForCausalLM,BitsAndBytesConfig
 from transformers.integrations import sdpa_attention
 from peft import PeftModel
 torch.backends.cuda.enable_flash_sdp(False);torch.backends.cuda.enable_math_sdp(False);torch.backends.cuda.enable_mem_efficient_sdp(True);sdpa_attention.use_gqa_in_sdpa=lambda attention_mask,key:False
 model_path=Path('C:/workspace/TUltra-Project/LayerTime/tools/ai-training/models/qwen3-0.6b-base')
 tokenizer=AutoTokenizer.from_pretrained(model_path,local_files_only=True)
 model=AutoModelForCausalLM.from_pretrained(model_path,local_files_only=True,quantization_config=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type='nf4',bnb_4bit_use_double_quant=True,bnb_4bit_compute_dtype=torch.float16),device_map={'':0},dtype=torch.float16,attn_implementation='sdpa').eval()
 model=PeftModel.from_pretrained(model,a.adapter,local_files_only=True,is_trainable=False).eval();results=[]
 for e in corpus['examples']:
  if e['split']!='validation':continue
  messages=e['messages'][:-1];prompt=tokenizer.apply_chat_template(messages,tokenize=False,add_generation_prompt=True,enable_thinking=False)
  assert all(m['content'] in prompt for m in messages)
  inputs=tokenizer(prompt,return_tensors='pt',add_special_tokens=False).to('cuda');start=time.monotonic()
  with torch.inference_mode():generated=model.generate(**inputs,max_new_tokens=96,do_sample=False,pad_token_id=tokenizer.eos_token_id)
  text=tokenizer.decode(generated[0,inputs.input_ids.shape[1]:],skip_special_tokens=True);target=json.loads(e['messages'][-1]['content'])
  score=score_output(text,target,ontology['outputSchema'],['posture','combinedTrigger','evidenceClass']);frame=json.loads(e['messages'][-2]['content'])['observation'];guard=inspect_warning_output(text,dict(eligibleForModel=True,modelInput=frame),ontology['outputSchema'],contract['allowedStates'])
  results.append(dict(id=e['id'],promptSha256=hashlib.sha256(prompt.encode()).hexdigest(),output=text,seconds=time.monotonic()-start,score=score,guard=guard,outputTokens=int(generated.shape[1]-inputs.input_ids.shape[1])))
 report=dict(suite='previously-inspected-v6-development-controls',evaluatorSha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),condition=a.condition,adapterSha256=hashlib.sha256((a.adapter/'adapter_model.safetensors').read_bytes()).hexdigest(),total=len(results),decisionMatches=sum(r['score']['decisionFieldsMatch'] for r in results),schemaPasses=sum(r['score']['schemaValid'] for r in results),guardPasses=sum(r['guard']['checksPassed'] for r in results),maxNewTokens=96,results=results,fieldQualified=False)
 dest.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='results'}),flush=True)
if __name__=='__main__':main()
