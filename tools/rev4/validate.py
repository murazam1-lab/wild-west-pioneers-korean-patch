"""Usage: py -I -X utf8 validate.py NN [--warn]  (checks chunks/chunk_NN.json + out/rev_NN*.tsv)"""
import json,pathlib,re,sys,collections
R=pathlib.Path(__file__).parent
FIX={'UI_Icon_Pioneer_64':'UI_Icon_Person_64','UI_Icon_Stone_chips_64':'UI_Icon_Stone_Chips_64'}
SPRITES=set(json.loads((R/'sprite_names.json').read_text(encoding='utf8')))
TAGS=('b','i','u','s','color','size','link','mark','align','cspace','style','font','sup','sub','lowercase','uppercase','smallcaps','indent','line-height','nobr','voffset','margin','pos','alpha','noparse')
ALLOW={'UI','OK','II','III','IV','VI','VII','VIII','IX','XP','FPS','HUD','DLSS','FSR','FX','AMD','NVIDIA','Steam','Discord','DX','PC','Esc','Shift','Ctrl','Alt','Tab','Enter','Space','WASD','LMB','RMB','FAQ','HDR','VSync','Wild','West','Pioneers','Toplitz','SFX','BETA','Beta','TAA','SMAA','FXAA','MSAA','RAM','GPU','CPU','QWERTY','AZERTY'}
def sprites(s):
    return collections.Counter(FIX.get(n,n) for n in re.findall(r'<sprite[^>]*name="([^"]+)"',s))
def params(s):return collections.Counter(re.findall(r'\{\[[^\]]+\]\}|\{[A-Za-z_][A-Za-z0-9_]*\}',s))
def tagc(s):
    c=collections.Counter()
    for m in re.finditer(r'<(/?)([a-zA-Z-]+)(?:[= ][^>]*)?>',s):
        if m[2].lower() in TAGS:c[(m[2].lower(),bool(m[1]))]+=1
    return c
def balanced(c):return all(c[(t,False)]==c[(t,True)] for t in TAGS if t not in('align','indent','line-height','margin','pos','voffset','cspace','alpha','size','font'))
def check(item,ko):
    en=re.sub(r'<sprite name=([A-Za-z0-9_]+)">',r'<sprite name="\1">',item['en']);E=[];Wn=[]
    if not ko.strip():E.append('empty translation')
    if sprites(en)!=sprites(ko):E.append(f'sprite mismatch en={dict(sprites(en))} ko={dict(sprites(ko))}')
    for n in re.findall(r'<sprite[^>]*name="([^"]+)"',ko):
        if n not in SPRITES:E.append(f'unknown sprite name {n}')
    if params(en)!=params(ko):E.append(f'variable mismatch en={dict(params(en))} ko={dict(params(ko))}')
    if en.count('<br>')!=ko.count('<br>'):E.append(f'<br> count en={en.count("<br>")} ko={ko.count("<br>")}')
    if en.count('\n')!=ko.count('\n'):Wn.append(f'newline count en={en.count(chr(10))} ko={ko.count(chr(10))}')
    ce,ck=tagc(en),tagc(ko)
    if ce!=ck:
        if balanced(ce) or not balanced(ck):E.append(f'tag mismatch en={dict(ce)} ko={dict(ck)}')
    if re.search(r'<b>\s*<b>|</b>\s*</b>',ko):E.append('nested <b>')
    if re.search(r'<b>\s*</b>',ko):E.append('empty <b></b>')
    if en.lstrip().startswith('<align') and not ko.lstrip().startswith('<align'):E.append('align tag must stay at start')
    plain=re.sub(r'<[^>]+>|\{[^}]+\}','',ko)
    words=[w for w in re.findall(r'[A-Za-z]{3,}',plain) if w not in ALLOW]
    if words and re.search('[가-힣]',plain):Wn.append('latin words left: '+','.join(words[:6]))
    if not re.search('[가-힣]',plain) and re.search('[A-Za-z]{3,}',re.sub(r'<[^>]+>|\{[^}]+\}','',en)):Wn.append('no Hangul in translation')
    if re.search(r' [.,!?](?!\.)',plain):Wn.append('space before punctuation')
    if '당신' in plain:Wn.append('uses 당신 (avoid unless needed)')
    return E,Wn
if __name__=='__main__':
    n=sys.argv[1].zfill(2)
    items=json.loads((R/'chunks'/f'chunk_{n}.json').read_text(encoding='utf8'))
    sys.path.insert(0,str(R));from revload import load_rev
    rev,problems=load_rev(n)
    for pr in problems:print('ERROR',pr)
    keys={x['key'] for x in items}
    unknown=[k for k in rev if k not in keys]
    errs=warns=len(problems)*0
    errs=len(problems)
    for k in unknown:print('ERROR',k,'key not in this chunk');errs+=1
    for it in items:
        ko=rev.get(it['key'],it['ko']);E,Wn=check(it,ko)
        for e in E:print('ERROR',it['key'],'|',e);errs+=1
        if '--warn' in sys.argv:
            for w in Wn:print('WARN',it['key'],'|',w);warns+=1
    print(f'chunk {n}: items={len(items)} revised={len(rev)} errors={errs} warnings={warns}')
