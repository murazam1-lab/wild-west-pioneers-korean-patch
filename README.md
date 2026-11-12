# Wild West Pioneers — Unofficial Korean Localization

[한국어 설명은 README.ko.md](README.ko.md)

This is a full Korean localization of the Steam game *Wild West Pioneers* (Unity 6, IL2CPP), made as an unofficial fan project. The repository documents the process and publishes the tools I wrote. It does not contain game files, extracted game text, or the finished translation (see [What is not included](#what-is-not-included)).

## At a glance

| | |
|---|---|
| Engine | Unity 6000.1.17f1, IL2CPP build |
| Text systems | I2 Localization, TextMeshPro, UI Toolkit |
| Localization table | 7,820 I2 entries, 7,262 translatable lines fully revised |
| Hard-coded UI text | 179 labels (78 distinct strings) outside I2 found and translated |
| Files patched | `resources.assets`, `level0/6/8/9/11`, `sharedassets0/6/11.assets` |
| Game build | Steam build 26485589 (2026-11-07) |
| Revisions | 5 (2026-11-01 → 2026-11-08) |

## What the work involved

### 1. Translation
- **Style guide and glossary** ([docs/style-guide.ko.md](docs/style-guide.ko.md)). It sets the register for each text type: short noun phrases for UI labels, polite `합니다`-style for tooltips and help, noun endings for quest objectives, and in-character speech for dialogue (residents call the player "대장", bandits speak rough). It also fixes about 300 terms: buildings, resources, places, characters, and quest titles.
- **Korean-specific rules.** Korean particles change with the previous word's final consonant (을/를, 이/가). Sentences are restructured so that no such particle follows an icon tag or a variable, since the game can't pick the right form at runtime.
- **Revision history.** Revisions 1–3 were a machine-translation draft made with a local EN→KO model ([quickmt](https://huggingface.co/quickmt/quickmt-en-ko)), plus partial manual fixes. Revision 4 was a full LLM-assisted pass over every line against the style guide, which changed 3,965 entries. [Before/after examples](docs/examples.md).
- **Automated checks on every line** ([tools/rev4/validate.py](tools/rev4/validate.py)):
  - icon sprites, variables, `<br>`, line breaks, and rich-text tags must match the source, with tags correctly nested
  - glossary terms must be used consistently
  - no leftover English except an allowlist of key names and abbreviations
  - every Korean character used must be present in the bundled font

### 2. Engineering
- **I2 Localization binary.** I wrote a parser and rebuilder for the serialized `LanguageSourceAsset` ([tools/work/i2_data.py](tools/work/i2_data.py)). It swaps the language column, preserves keys, flags, and other languages, and disables the live Google Sheets sync that would otherwise overwrite the patch.
- **Fonts.**
  - The game's bundled Source Han Serif is added as the global TextMeshPro fallback, with multi-atlas and modern Hangul line breaking turned on.
  - The UI Toolkit dynamic font is pointed at the same TTF.
  - In revision 5, a cross-file fallback reference fixed a quest-panel font that rendered Hangul as boxes.
- **Hard-coded labels outside I2.** I scanned every scene and asset file for TextMeshPro text that the localization system doesn't own ([tools/rev5/scan/](tools/rev5/scan/)). A label was changed only when nothing but display scripts references its component ([tools/rev5/gen_targets.py](tools/rev5/gen_targets.py)). Text that code overwrites at runtime and developer-only UI (console, terrain tools, debug panels) were left alone.
- **Serialization fidelity.** UnityPy writes objects on 8-byte boundaries, while the original files use 16, so the writer is patched to match. After saving, every patched file is reloaded and each object's hash is compared with the original. Only the intended objects may differ. Header, type table, externals, and object order are checked as well ([tools/rev5/structcheck.py](tools/rev5/structcheck.py)).
- **Safe install and restore** ([tools/rev5/install5.py](tools/rev5/install5.py)). Originals are backed up and every copy is verified with SHA-256. The generated Apply/Restore PowerShell scripts refuse to run if the game is open or the files no longer match a known version, for example after a Steam update.

## Repository layout

```
docs/
  style-guide.ko.md    translation style guide and glossary (Korean)
  examples.md          before/after samples from revision 4
tools/
  work/                I2 binary parser/rebuilder, machine-translation draft script
  rev4/                extract → prepare chunks → validate → merge → build resources.assets
  rev5/                scene/asset text scan, target selection, build, structure check, install
requirements.txt
```

The scripts need two environment variables: `WWP_GAME`, the game's install folder, and `WWP_WORK`, a working folder that holds `i2_data.py`, the Python libraries, and the extracted type-tree files. They are published as a reference. They can't run end to end from this repository alone, because the game data they read is not included.

## What is not included

All game content belongs to its developer and publisher, so this repository leaves out:
- game files and patched game files
- extracted text, type trees, and fonts
- the full translation table

Short before/after excerpts appear in `docs/examples.md` to illustrate the work.

## Known limitations

- The patch is tied to one game build. A Steam update replaces the patched files, and the patch has to be rebuilt for the new version. The install scripts detect this and stop.
- English strings compiled into `GameAssembly.dll` (mostly logs and errors) were not changed.
- Revision 5 was verified at the file and object level. The in-game screens for those labels have not all been checked visually yet.

## Disclaimer

This is an unofficial fan translation. It is not affiliated with or endorsed by the developer or publisher of *Wild West Pioneers*.
