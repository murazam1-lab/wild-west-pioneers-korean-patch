"""scan/scan_texts.json + scan/scan_refs.json -> scene_targets.json (파일, path_id, 원문, 번역)"""
import json,pathlib,re,collections,sys
R=pathlib.Path(__file__).parent;sys.path.insert(0,str(R))
from scene_text_ko import KO
r=json.loads((R/'scan/scan_texts.json').read_text(encoding='utf8'))
refs=json.loads((R/'scan/scan_refs.json').read_text(encoding='utf8'))
loc={(x['cab'],x['go']) for x in r if x.get('cls')=='I2.Loc.Localize'}
GEN={'AztecButton','ScrollingTMPText','ES3ReferenceMgr','TMP_InputField','RebuildLayoutOnLabel','ReactToPointer','Letterbox'}
FILES={'level0','level6','level8','level9','level11','sharedassets0.assets','sharedassets6.assets','sharedassets11.assets'}
SKIP=('Quantum Console','Debug','Canvas/Runtime Terrain')
T=[];used=collections.Counter()
for x in r:
    if 'text' not in x or x['file'] not in FILES or (x['cab'],x['go']) in loc:continue
    if x['text'] not in KO or x['goname'].startswith(SKIP):continue
    rc=set(refs.get(x['file'],{}).get(str(x['pid']),[]))
    if rc-GEN:continue
    T.append({'file':x['file'],'pid':x['pid'],'cls':x['cls'],'path':x['goname'],'en':x['text'],'ko':KO[x['text']]});used[x['text']]+=1
unused=[k for k in KO if k not in used]
(R/'scene_targets.json').write_text(json.dumps(T,ensure_ascii=False,indent=1),encoding='utf8')
print('targets',len(T),'distinct',len(used),'files',dict(collections.Counter(t['file'] for t in T)))
print('unused keys',unused)
