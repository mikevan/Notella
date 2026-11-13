"""Domain-neutral source-lineage summaries from caller-reviewed registry assertions."""
import hashlib
from .core import canonical,check

def summarize_lineage(labels,registry):
    check(isinstance(labels,list) and labels and all(type(s) is str and s for s in labels),'Source labels must be a nonempty string list')
    check(isinstance(registry,dict),'Source registry must be an object')
    origins={};groups=[];reviewed=True;receipts=[]
    for label in labels:
        item=registry.get(label)
        if item is None:
            groups.append(None);reviewed=False
        else:
            check(isinstance(item,dict) and set(item)=={'originRef','reviewed'},'Registry entries require originRef and reviewed')
            check(type(item['originRef']) is str and item['originRef'] and type(item['reviewed']) is bool,'Invalid registry entry')
            if item['reviewed']:
                origins.setdefault(item['originRef'],len(origins));groups.append(origins[item['originRef']])
            else:groups.append(None);reviewed=False
        receipts.append(dict(labelSha256=hashlib.sha256(label.encode()).hexdigest(),registryEntry=item))
    relationship='unknown' if not reviewed else 'distinct_reviewed_origins' if len(origins)>1 else 'shared_origin' if len(labels)>1 else 'single_origin'
    summary=dict(reportCount=len(labels),originGroups=groups,reviewedDistinctOrigins=len(origins),relationship=relationship)
    return dict(summary=summary,receipt=dict(registrySha256=hashlib.sha256(canonical(registry).encode()).hexdigest(),sources=receipts,
        assertionScope='Caller-supplied provenance assertions; not external verification or statistical independence.'))
