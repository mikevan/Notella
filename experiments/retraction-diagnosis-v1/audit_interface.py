"""Read-only audit of saved training/evaluation interfaces; no model generation."""
import importlib.util,json,sys,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def main():
 from transformers import AutoTokenizer
 model=Path('C:/workspace/TUltra-Project/LayerTime/tools/ai-training/models/qwen3-4b-instruct-2507')
 tokenizer=AutoTokenizer.from_pretrained(model,local_files_only=True)
 config=json.loads((model/'generation_config.json').read_text(encoding='utf-8'));eos=config.get('eos_token_id');eos=eos if isinstance(eos,list) else [eos]
 assert tokenizer.eos_token_id in eos,'Tokenizer/model EOS mismatch'
 result=dict(tokenizerEos=tokenizer.eos_token_id,generationEos=eos,runs=[],limits=['Checks saved code, rendered prefixes, logged lengths and EOS configuration; not a dump of live label tensors or gradients.','Matching interfaces and numerical stability do not prove adequate training or correct semantics.'])
 for run in ['scenario-model-v3','scenario-model-v4','scenario-model-v5']:
  r=json.loads((ROOT/'runtime'/run/'training-result.json').read_text(encoding='utf-8'));job=Path(r['adapter']).parent
  helper=job/'engine/evaluate_local_model.py';spec=importlib.util.spec_from_file_location('saved_helper_'+run.replace('-','_'),helper);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
  logged=next(json.loads(line) for line in (job/'stdout.log').read_text(encoding='utf-8').splitlines() if line.startswith('{"trainingTokenLengths":'))
  checks={}
  for split,key in [('train','trainingTokenLengths'),('validation','validationTokenLengths')]:
   lengths=[];count=0
   for line in (job/'dataset'/(split+'.jsonl')).read_text(encoding='utf-8').splitlines():
    row=json.loads(line);training=module.render_evaluation_prompt(tokenizer,row,merge_system_messages=False)
    evaluation=tokenizer.apply_chat_template(row['messages'][:-1],tokenize=False,add_generation_prompt=True,enable_thinking=False)
    assert training==evaluation,'Rendered prefix mismatch: '+row['id']
    ids=tokenizer(training,add_special_tokens=False)['input_ids'];answer=tokenizer(row['messages'][-1]['content'],add_special_tokens=False)['input_ids']+[tokenizer.eos_token_id]
    assert len(ids)+len(answer)<=4096
    lengths.append(len(ids)+len(answer));count+=1
   assert lengths==logged[key],'Lengths do not match actual training log'
   checks[split]=dict(prefixesMatched=count,lengthsMatchTrainingLog=True,maxLength=max(lengths))
  result['runs'].append(dict(run=run,checks=checks,helperSha256=hashlib.sha256(helper.read_bytes()).hexdigest()))
 out=Path(__file__).resolve().parent/'interface-audit.json';out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
