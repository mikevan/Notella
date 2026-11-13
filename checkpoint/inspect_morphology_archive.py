"""Verify the checkpoint archive or extract one original file without overwriting."""
import argparse,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];ARCHIVE=ROOT/'archive/morphology-v1'
def main():
 p=argparse.ArgumentParser();p.add_argument('--verify',action='store_true');p.add_argument('--source');p.add_argument('--output',type=Path);args=p.parse_args()
 entries=json.loads((ARCHIVE/'index.json').read_text(encoding='utf-8'))['entries']
 if args.verify:
  seen=set()
  for record in entries:
   blob=(ARCHIVE/record['blob']).resolve();assert blob.is_relative_to(ARCHIVE.resolve())
   if blob not in seen:
    data=blob.read_bytes();assert hashlib.sha256(data).hexdigest()==record['sha256'] and len(data)==record['bytes'];seen.add(blob)
  print(f'Verified {len(entries)} source records and {len(seen)} unique blobs.')
 if args.source:
  if not args.output:raise ValueError('--output required')
  record=next(r for r in entries if r['path']==args.source.replace('\\','/'));data=(ARCHIVE/record['blob']).read_bytes()
  assert hashlib.sha256(data).hexdigest()==record['sha256']
  if args.output.exists():raise ValueError('Refusing to overwrite existing output')
  args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_bytes(data);print('Extracted '+record['path'])
 if not args.verify and not args.source:p.error('Use --verify or --source/--output')
if __name__=='__main__':main()
