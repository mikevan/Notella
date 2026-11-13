"""Notella curriculum adapter for the retained, numerically audited LoRA engine."""
import hashlib,json
from pathlib import Path
from notella.core import check,canonical,validate_schema,fingerprint

def verify(folder):
    folder=Path(folder);m=json.loads((folder/'manifest.json').read_text(encoding='utf-8'))
    check(m.get('profile')=='notella-lora-v1' and m.get('releaseEligible') is False,'Wrong training profile')
    check(fingerprint(m['ontology'])==m['ontologyId'],'Ontology changed')
    seen=set();families={};prompts={};blocked=set(m['excludedPromptHashes'])
    for split,info in m['splits'].items():
        check(split in ('train','validation','test'),'Unknown split')
        check(info['file']==split+'.jsonl','Unexpected split filename')
        p=folder/info['file'];check(hashlib.sha256(p.read_bytes()).hexdigest()==info['sha256'],'Split changed')
        rows=[json.loads(l) for l in p.read_text(encoding='utf-8').splitlines() if l]
        check(len(rows)==info['examples'],'Split count changed')
        for r in rows:
            check(r['id'] not in seen and r['split']==split,'Duplicate ID or wrong split');seen.add(r['id'])
            check(r['family'] not in families or families[r['family']]==split,'Family crosses splits');families[r['family']]=split
            check(fingerprint(r['messages'][:-1])==r['promptSha256'],'Prompt changed')
            ph=r['promptSha256'];ih=fingerprint(r['messages'][1]['content'])
            check(ph not in blocked and ih not in blocked,'Evaluation leakage')
            check(ih not in prompts or prompts[ih]==split,'Input crosses splits');prompts[ih]=split
            if split=='train':check(r['source']['trainingAllowed'] is True,'Unadmitted source')
            validate_schema(json.loads(r['messages'][-1]['content']),m['ontology']['outputSchema'])
    return m
