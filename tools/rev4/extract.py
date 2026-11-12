import os
import pathlib,sys,json,collections
W=pathlib.Path(os.environ['WWP_WORK'])
sys.path.insert(0,str(W/'libs'));sys.path.insert(0,str(W))
import UnityPy
from i2_data import parse
game=pathlib.Path(os.environ['WWP_GAME'])
env=UnityPy.load(str(game/'WWP_Data/resources.assets'))
objs={o.path_id:o for o in env.objects}
raw=objs[113714].get_raw_data();pathlib.Path('113714.bin').write_bytes(raw)
print(repr(raw[:120]))
terms,end=parse(raw)
print('TERMS',len(terms),'END',end,'LEN',len(raw))
pathlib.Path('terms_new.json').write_text(json.dumps(terms,ensure_ascii=False,indent=1),encoding='utf8')
print(collections.Counter(t['key'].split('/')[0] for t in terms))
print('NLANGS',collections.Counter(len(t['langs']) for t in terms))
