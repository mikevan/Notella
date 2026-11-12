"""Prepare portable, hash-verified domain profiles through the public core API."""
import hashlib,json
from pathlib import Path
from .core import check

def prepare_profile(api,profile_file):
    """Read a local profile pack. Returns artifact IDs; never starts training."""
    path=Path(profile_file).resolve();root=path.parent
    profile=json.loads(path.read_text(encoding='utf-8-sig'))
    check(isinstance(profile,dict) and profile.get('formatVersion')=='notella.profile.v1','Unsupported profile format')
    hashes={}
    def read_component(key):
        item=profile.get(key);check(isinstance(item,dict) and set(item)=={'file','sha256'},'Profile component requires file and sha256')
        check(isinstance(item['file'],str) and item['file'] and not Path(item['file']).is_absolute(),'Component path must be relative')
        target=(root/item['file']).resolve()
        check(target.is_relative_to(root),'Component path escapes profile folder')
        raw=target.read_bytes();digest=hashlib.sha256(raw).hexdigest()
        check(digest==item['sha256'],'Profile component hash mismatch: '+key)
        hashes[key]=digest
        return json.loads(raw.decode('utf-8-sig'))
    ontology=read_component('ontology');examples=read_component('examples')
    training=profile.get('training');check(isinstance(training,dict) and set(training)=={'baseModel','steps','rank','learningRate'},'Profile requires explicit supported training settings')
    registered=api.register_ontology(ontology);curriculum=api.compile(registered['id'],examples,profile.get('excludedPromptHashes'))
    plan=api.plan(curriculum['id'],training['baseModel'],training['steps'],training['rank'],training['learningRate'])
    return dict(ontologyId=registered['id'],curriculumId=curriculum['id'],planId=plan['id'],splits=curriculum['artifact']['splits'],
        profileSha256=hashlib.sha256(path.read_bytes()).hexdigest(),componentSha256=hashes,trainingStarted=False)
