import pathlib,glob
R=pathlib.Path(__file__).parent
def load_rev(n):
    """Merge out/rev_NN*.tsv (sorted by name; later files override). Line: key<TAB>korean, newline written as \n"""
    rev={};problems=[]
    for p in sorted((R/'out').glob(f'rev_{n}*.tsv')):
        for i,line in enumerate(p.read_text(encoding='utf-8-sig').splitlines(),1):
            if not line.strip():continue
            if '\t' not in line:problems.append(f'{p.name}:{i} no TAB');continue
            k,v=line.split('\t',1)
            rev[k.strip()]=v.replace('\\n','\n')
    return rev,problems
