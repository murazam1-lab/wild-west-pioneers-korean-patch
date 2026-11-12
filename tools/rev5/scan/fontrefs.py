import os
import pathlib,sys,struct,collections
W=pathlib.Path(os.environ['WWP_WORK'])
sys.path.insert(0,str(W/'libs'))
import UnityPy
D=(pathlib.Path(os.environ['WWP_GAME'])/'WWP_Data')
FONTS={('resources.assets',113728):'Barlow-Regular-TK',('resources.assets',113729):'JingHua-TK',('resources.assets',113730):'NotoSans-TK(KO)',('sharedassets11.assets',24190):'Barlow-Medium-TK',('sharedassets11.assets',24191):'Barlow-SemiBold-TK(noKO)',('sharedassets11.assets',24192):'MaidenOrange-TK',('sharedassets0.assets',2543):'SHSerifLight-TK(noKO)'}
for f in ['sharedassets0.assets','sharedassets11.assets','resources.assets']:
    env=UnityPy.load(str(D/f));ext=['']+[e.path for e in env.file.externals]
    pats={}
    for (ff,pid),nm in FONTS.items():
        fid=0 if ff==f else (ext.index(ff) if ff in ext else None)
        if fid is not None:pats[struct.pack('<iq',fid,pid)]=nm
    for o in env.objects:
        if o.type.name!='MonoBehaviour':continue
        try:c=o.parse_monobehaviour_head().m_Script.deref_parse_as_object().m_ClassName
        except Exception:continue
        if c not in('StyleSheet','ThemeStyleSheet','VisualTreeAsset','PanelTextSettings','FontAsset'):continue
        raw=o.get_raw_data();hits=[nm for p,nm in pats.items() if p in raw]
        if hits:print(f,o.path_id,c,repr(o.peek_name()),hits)
