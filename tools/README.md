# tools/

Executable patches that mirror the narrative in `OPENSPEC.md`. Run these against a fresh Claude Design extract to apply the Syfo customizations on top.

| Script                          | What it does                                                                                                            |
|---------------------------------|--------------------------------------------------------------------------------------------------------------------------|
| `patch-zh-typography.py`        | Produces the ZH variant from an EN copy: rewrites font stacks, bumps line-heights, applies the EN→ZH string translation map. |
| `patch-lang-toggle.py`          | Injects the `[中文 \| EN]` language toggle into both EN and ZH prototype HTMLs with runtime JS positioning.              |

Both scripts hardcode paths (`/tmp/syfo-zh`, `/tmp/syfo-v2/syfo-mock/project`) that mirror the working directories used when iterating with Tony on 2026-05-20. Adapt the path constants at the top of each file when applying to fresh extracts.

These scripts are NOT part of the runtime; they are reproducible patch records.
