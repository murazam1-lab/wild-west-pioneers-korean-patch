"""5차 설치: 원본 백업(KoreanPatch_Backup_20261108) -> 패치 파일 복사 -> 해시 검증 -> outputs/ 생성.
Usage: py -I -X utf8 install5.py"""
import os
import pathlib,json,hashlib,shutil,subprocess,sys,re
R=pathlib.Path(__file__).parent;R4=R.parent/'rev4';O=R/'outputs';O.mkdir(exist_ok=True)
GAME=pathlib.Path(os.environ['WWP_GAME']);D=GAME/'WWP_Data'
B=GAME/'KoreanPatch_Backup_20261108';B4=GAME/'KoreanPatch_Backup_20261107'
sha=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
if 'WWP.exe' in subprocess.run(['tasklist','/FI','IMAGENAME eq WWP.exe'],capture_output=True,text=True,encoding='cp949',errors='replace').stdout:
    sys.exit('게임이 실행 중입니다. 종료 후 다시 실행하세요.')
m5=json.loads((R/'patch_manifest5.json').read_text(encoding='utf8'));m4=json.loads((R4/'patch_manifest.json').read_text(encoding='utf8'))
files=dict(m5['files'])
files['resources.assets']={'original_sha256':m4['original_sha256'],'patched_sha256':sha(R/'patched'/'resources.assets'),'rev4_patched_sha256':m4['patched_sha256'],
    'note':'4차 내용 그대로, 객체 정렬만 원본과 같은 16바이트로 다시 저장','backup':str(B4/'resources.assets.original')}
B.mkdir(exist_ok=True)
for f,info in files.items():
    cur=D/f;curh=sha(cur);pat=R/'patched'/f
    assert sha(pat)==info['patched_sha256'],('patched file corrupt',f)
    if f=='resources.assets':
        assert sha(B4/'resources.assets.original')==info['original_sha256']
        assert curh in(info['rev4_patched_sha256'],info['patched_sha256'],info['original_sha256']),('unexpected current',f)
    else:
        bk=B/(f+'.original');info['backup']=str(bk)
        if bk.exists():assert sha(bk)==info['original_sha256'],('backup mismatch',f)
        else:
            assert curh==info['original_sha256'],('current is not the original; refusing to back up',f)
            shutil.copy2(cur,bk);assert sha(bk)==info['original_sha256']
    if curh!=info['patched_sha256']:
        shutil.copy2(pat,cur)
    assert sha(cur)==info['patched_sha256'],('install verify failed',f)
    print('installed',f)
# outputs
sys.path.insert(0,str(R));from scene_text_ko import KO
targets=json.loads((R/'scene_targets.json').read_text(encoding='utf8'))
final=json.loads((R4/'final_korean.json').read_text(encoding='utf8'))
manifest={'revision':5,'date':'2026-11-08','game_build_guid':m5['game_build_guid'],'steam_buildid':'26485589',
 'update_wiped_patch':False,'note':'2026-11-07 업데이트(빌드 26485589) 이후 새 업데이트 없음. 4차 패치(I2 7,820항목) 유지. 5차는 I2 밖 고정 문구와 글꼴 보완.',
 'i2_entries_total':len(final),'i2_new_or_changed_since_rev4':0,
 'scene_texts_translated':len(targets),'scene_text_strings':len({t['en'] for t in targets}),
 'font_fix':'sharedassets11.assets #24191 BarlowCondensed-SemiBold-Toolkit (UI Toolkit 퀘스트 패널) 대체 글꼴에 resources.assets #113730(한글 Source Han Serif 동적) 추가',
 'files':files,'backup_dir':str(B),'runtime_ui_checked':False}
(O/'patch_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
shutil.copy(O/'patch_manifest.json',B/'patch_manifest.json')
(O/'한글패치_5차_고정문구.json').write_text(json.dumps([{k:t[k] for k in('file','path','en','ko')} for t in targets],ensure_ascii=False,indent=1),encoding='utf8')
(O/'WildWestPioneers_Korean.json').write_text(json.dumps(final,ensure_ascii=False,indent=1),encoding='utf8')
shutil.copy(R4/'glossary.md',O/'번역_용어집.md')
rows=[]
for f,i in files.items():
    bk=i['backup']
    rows.append(f"  @{{ Name='{f}'; Orig='{i['original_sha256'].upper()}'; Patched='{i['patched_sha256'].upper()}'; Old=@('{i.get('rev4_patched_sha256','').upper()}'); Backup='{bk}' }}")
common=f"""$ErrorActionPreference = 'Stop'
$data = '{D}'
$files = @(
{chr(10).join(rows)}
)
if (Get-Process -Name WWP -ErrorAction SilentlyContinue) {{ Write-Host '게임을 먼저 종료하세요.'; exit 1 }}
function Get-Sha($p) {{ (Get-FileHash $p -Algorithm SHA256).Hash }}
"""
apply=common+"""$todo = @()
foreach ($f in $files) {
  $cur = Get-Sha (Join-Path $data $f.Name)
  if ($cur -eq $f.Patched) { continue }
  if ($cur -ne $f.Orig -and -not ($f.Old -contains $cur)) { Write-Host "$($f.Name): 게임이 업데이트되어 이 패치와 맞지 않습니다. 새 버전에 맞춰 다시 제작해야 합니다."; exit 1 }
  $src = Join-Path $PSScriptRoot ('../patched/' + $f.Name)
  if ((Get-Sha $src) -ne $f.Patched) { Write-Host "$($f.Name): 패치 파일이 손상되었습니다."; exit 1 }
  $todo += ,@($f, $src)
}
foreach ($t in $todo) { Copy-Item $t[1] (Join-Path $data $t[0].Name) -Force; if ((Get-Sha (Join-Path $data $t[0].Name)) -ne $t[0].Patched) { Write-Host "$($t[0].Name): 적용 후 해시가 다릅니다!"; exit 1 } }
Write-Host ('한글 패치 적용 완료 (변경 파일 ' + $todo.Count + '개)')
"""
restore=common+"""foreach ($f in $files) {
  $cur = Get-Sha (Join-Path $data $f.Name)
  if ($cur -eq $f.Orig) { continue }
  if ($cur -ne $f.Patched -and -not ($f.Old -contains $cur)) { Write-Host "$($f.Name): 게임 파일이 업데이트되어 패치/원본과 다릅니다. 복구를 중단합니다. (Steam 무결성 검사로 원본을 받을 수 있습니다)"; exit 1 }
  if ((Get-Sha $f.Backup) -ne $f.Orig) { Write-Host "$($f.Name): 백업 파일이 손상되었습니다."; exit 1 }
}
foreach ($f in $files) { $t = Join-Path $data $f.Name; if ((Get-Sha $t) -ne $f.Orig) { Copy-Item $f.Backup $t -Force; if ((Get-Sha $t) -ne $f.Orig) { Write-Host "$($f.Name): 복구 후 해시가 다릅니다!"; exit 1 } } }
Write-Host '원본(영어)으로 복구했습니다.'
"""
for name,body in [('Apply-KoreanPatch.ps1',apply),('Restore-KoreanPatch.ps1',restore)]:
    (O/name).write_text(body.replace('\r\n','\n').replace('\n','\r\n'),encoding='utf-8-sig')
print(json.dumps({k:v for k,v in manifest.items() if k!='files'},ensure_ascii=False,indent=1))
