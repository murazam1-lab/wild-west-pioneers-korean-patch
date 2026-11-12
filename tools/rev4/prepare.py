import os
import json,pathlib,collections
W=pathlib.Path(os.environ['WWP_WORK'])
R=pathlib.Path(__file__).parent
old={t['key']:t for t in json.loads((W/'terms.json').read_text(encoding='utf8'))}
new=json.loads((R/'terms_new.json').read_text(encoding='utf8'))
ko=json.loads((W/'korean.json').read_text(encoding='utf8'))
SKIP=('AUDIO_FILES','Assets','Keybind_Keys')
CHUNKS=[
 ['ConditionQuests_EA','ConditionQuests'],
 ['Gameplay_Effects','Character_Progression','Technology','Achievement'],
 ['Technology_EA','Tooltips','UI_BottomBar','MiniGame_UI','UI_InGameConsole'],
 ['Quests_EA','Quests_New','ConditionQuests_New','StartAndEndOfDay'],
 ['Dialogue','CutScenes'],
 ['Dioramas_EA','StrategicMap_Locations'],
 ['FAQ','Tutorial_Quests_New'],
 ['BUILDINGS_UI','DECORATIONS_UI','UI','MAINMENU_UI','UI_Buildings','Resources','Buildings','Characters','Town_Hall_Officials','TownHall_Milestones','StrategicMap_UI'],
 ['Brothel_UIandQuests','SpecialistsCamp','Journey','UI_Satisfaction','StrategicMap_Events'],
]
cat2chunk={c:i+1 for i,cs in enumerate(CHUNKS) for c in cs}
base={};chunks=collections.defaultdict(list);stat=collections.Counter()
for t in new:
    k=t['key'];en=t['langs'][0];cat=k.split('/')[0]
    if k in old and old[k]['langs'][0]==en: cur=ko[k];status='ok'
    elif k in old: cur=ko[k];status='changed'
    else: cur='';status='new'
    if cat in SKIP or not en.strip():
        base[k]=en if status!='ok' else cur;stat['skip']+=1;continue
    base[k]=cur
    item={'key':k,'en':en,'ko':cur,'status':status}
    if status=='changed':item['old_en']=old[k]['langs'][0]
    chunks[cat2chunk[cat]].append(item);stat[status]+=1
assert all(c in cat2chunk or c in SKIP for c in {t['key'].split('/')[0] for t in new}),'unassigned category'
(R/'chunks').mkdir(exist_ok=True)
for i,items in sorted(chunks.items()):
    (R/'chunks'/f'chunk_{i:02d}.json').write_text(json.dumps(items,ensure_ascii=False,indent=1),encoding='utf8')
    print(i,len(items),sum(len(x['en']) for x in items),collections.Counter(x['status'] for x in items))
(R/'base_korean.json').write_text(json.dumps(base,ensure_ascii=False,indent=1),encoding='utf8')
print(stat,len(base))
