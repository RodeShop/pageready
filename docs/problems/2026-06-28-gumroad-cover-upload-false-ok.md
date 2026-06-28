# Gumroad cover upload false positive

**Дата:** 2026-06-28  
**Статус:** fixed in playwright_gumroad.py  
**Slug:** notion-developer-career-os

## Симптом

Script printed `Cover image uploaded (direct input)` but Cover + Thumbnail empty on Product tab.

## Cause

Fallback `set_input_files` on hidden `input[type="file"]` did not bind to Gumroad Cover UI.

## Fix

- Product tab → Cover → **Computer files** tab → **Upload images or videos** (file chooser)
- Thumbnail section → **+ Upload** (file chooser)
- Verify preview before OK; removed silent direct-input success

## Content tab

`user-guide.md` on `/edit/content` — **keep**, correct file.
