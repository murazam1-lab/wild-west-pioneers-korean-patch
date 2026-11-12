"""Merge base translation + out/rev_NN*.tsv -> final_korean.json; run validators and glossary consistency checks."""
import os
import json,pathlib,sys,re,collections,io
R=pathlib.Path(__file__).parent
W=pathlib.Path(os.environ['WWP_WORK'])
sys.path.insert(0,str(R));from revload import load_rev;from validate import check
base=json.loads((R/'base_korean.json').read_text(encoding='utf8'))
final=dict(base);errs=0;revised=0;report=[]
for n in range(1,10):
    nn=f'{n:02d}';items=json.loads((R/'chunks'/f'chunk_{nn}.json').read_text(encoding='utf8'))
    rev,problems=load_rev(nn);keys={x['key'] for x in items}
    for p in problems:print('ERROR',p);errs+=1
    for k in rev:
        if k not in keys:print('ERROR stray key',nn,k);errs+=1
    for it in items:
        ko=rev.get(it['key'],it['ko'])
        E,_=check(it,ko)
        for e in E:print('ERROR',it['key'],e);errs+=1
        if ko!=it['ko']:revised+=1;report.append({'key':it['key'],'en':it['en'],'before':it['ko'],'after':ko})
        final[it['key']]=ko
    print(nn,'items',len(items),'revised',sum(1 for it in items if rev.get(it['key'],it['ko'])!=it['ko']))
terms=json.loads((R/'terms_new.json').read_text(encoding='utf8'))
en={t['key']:t['langs'][0] for t in terms}
assert set(final)==set(en)
# glossary consistency
RULES=[(r'Dust Creek','더스트크리크',['더스트 크리크']),(r'Sand Storm','샌드스톰',['모래 폭풍 정착지']),(r'\bBandits?\b','도적',['밴디트']),(r'[Ss]ettlements?','',['정착촌']),
       (r'Town Hall','시청',['타운홀','타운 홀']),(r'Warehouse','창고',[]),(r'\bBoss\b','',['보스']),(r'Food Shop','식료품점',['푸드샵','음식 가게']),(r'Loggers.? Cabin','벌목꾼 오두막',[]),(r'Scouts.? Cabin','정찰대 오두막',[]),(r'Talent Points','재능 점수',[]),(r'Westwood Bar','웨스트우드 주점',[]),(r'Deaf Canyon','고요한 협곡',[])]
warn=collections.Counter();samples=collections.defaultdict(list)
for k,v in final.items():
    if k.split('/')[0] in('AUDIO_FILES','Assets','Keybind_Keys'):continue
    e=en[k]
    for pat,need,bad in RULES:
        if re.search(pat,e):
            if need and need not in v:warn[pat+' missing '+need]+=1;samples[pat+' missing '+need].append(k)
            for b in bad:
                if b in v:warn[pat+' has '+b]+=1;samples[pat+' has '+b].append(k)
for k,c in warn.most_common():print('GLOSS',c,k,samples[k][:6])
# font coverage
sys.path.insert(0,str(W/'libs'))
from fontTools.ttLib import TTFont
cmap=TTFont(str(W/'4630.ttf'),fontNumber=0).getBestCmap()
missing=sorted({c for v in final.values() for c in v if ord(c)>0x2000 and ord(c) not in cmap})
print('FONT missing chars:',missing[:50])
(R/'final_korean.json').write_text(json.dumps(final,ensure_ascii=False,indent=1),encoding='utf8')
(R/'revision4_changes.json').write_text(json.dumps(report,ensure_ascii=False,indent=1),encoding='utf8')
print('TOTAL revised',revised,'errors',errs)
