"""Fixed narrative repetition diagnostic, not a semantic correctness judge."""
import json,re
from collections import Counter

def measure(text):
    try:
        value=json.loads(text)
        narratives=[value.get('assessment',{}).get('rationale',''),value.get('change',{}).get('summary','')]
    except (ValueError,TypeError,AttributeError):
        narratives=re.findall(r'"(?:rationale|summary)"\s*:\s*"((?:\\.|[^"\\])*)',text)
    measurements=[]
    for narrative in narratives:
        if not isinstance(narrative,str):continue
        tokens=re.findall(r'\b\w+\b',narrative.lower());grams=Counter(tuple(tokens[i:i+12]) for i in range(max(0,len(tokens)-11)))
        total=sum(grams.values());duplicates=sum(n-1 for n in grams.values());maximum=max(grams.values(),default=0)
        fraction=duplicates/total if total else 0
        measurements.append(dict(words=len(tokens),max12gramOccurrences=maximum,duplicate12gramFraction=fraction,repetitive=len(tokens)>=36 and maximum>=3 and fraction>=0.25))
    return dict(repetitive=any(m['repetitive'] for m in measurements),narratives=measurements)

if __name__=='__main__':
    sentence='This is a deliberately repeated narrative sentence with more than twelve separate words describing evidence. '
    assert measure(json.dumps(dict(assessment=dict(rationale=sentence*5))))['repetitive']
    assert measure('{"assessment":{"rationale":"'+sentence*5)['repetitive']
    assert not measure(json.dumps(dict(nodes=[dict(status='observed',counts=dict(reportCount=1))]*20)))['repetitive']
    print('Narrative repetition diagnostic checks passed.')
