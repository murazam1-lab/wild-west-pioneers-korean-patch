import os
import pathlib,sys,json,re,struct
W=pathlib.Path(os.environ['WWP_WORK'])
sys.path.insert(0,str(W/'libs'))
import UnityPy
D=(pathlib.Path(os.environ['WWP_GAME'])/'WWP_Data');AA=D/'StreamingAssets/aa/StandaloneWindows64'
def strings(raw):
    out=[];i=0;n=len(raw)
    while i+4<=n:
        ln=struct.unpack_from('<i',raw,i)[0]
        if 1<=ln<=4000 and i+4+ln<=n:
            s=raw[i+4:i+4+ln]
            try:
                t=s.decode('utf8')
                if t.isprintable() or '\n' in t:
                    out.append((i,t));i+=4+((ln+3)&~3);continue
            except UnicodeDecodeError:pass
        i+=4
    return out
for f in sys.argv[1:]:
    p=D/f if (D/f).exists() else AA/f
    env=UnityPy.load(str(p))
    for o in env.objects:
        if o.type.name!='MonoBehaviour':continue
        try:
            h=o.parse_monobehaviour_head();s=h.m_Script.deref_parse_as_object()
        except Exception:continue
        if s.m_ClassName not in('VisualTreeAsset','UIDocument','PanelSettings','PanelTextSettings','StyleSheet'):continue
        raw=o.get_raw_data()
        st=[t for _,t in strings(raw)]
        print('==',f,o.path_id,s.m_ClassName,repr(h.m_Name),len(raw))
        print('   ',json.dumps(st,ensure_ascii=False))
