# TASK-023 — Video Pipeline · Phase 0 (prep)

**Статус:** ready · параллельно TASK-022 (covers)  
**Не трогать:** `pillow_pin.py` · `generate_cover_variants.py` · `playwright_*` · `setup_product.py` · `.mimocode/MIMO_FACTORY.md`

---

## Разделение с параллельным чатом

| Зона | Параллельный чат | Этот трек (видео) |
|------|------------------|-------------------|
| Covers | TASK-022 D/E/F/G | — |
| Scripts | pillow_pin, cover variants | `generate_video.py` (Phase 1) |
| Products | notion-cover upload | `video-script.md` только |
| Owner | выбор cover | clips + music + ElevenLabs + bio |

**Phase 1** (код в pipeline) — только когда Owner закрыл cover + parallel hotfix.

---

## Phase 0 — можно сейчас

## Phase 0 — пошагово (Owner)

Lead → один шаг → Owner «готово» → Lead принимает → дальше.

| # | Шаг | Статус |
|---|-----|--------|
| **1** | ElevenLabs → `.env` | ✅ |
| **2** | клипы → `assets/notion-clips/` | 🔄 СЕЙЧАС |
| 3 | music → `assets/music/` | ⏳ |
| 4 | bio TikTok/Reels | ⏳ |
| 5 | caption TikTok | ⏳ |

---

### Owner (сводка)

| # | Действие | Куда |
|---|----------|------|
| 1 | ElevenLabs API key | `.env` |
| 2 | 4–5 скринкастов 15–20 сек | `assets/notion-clips/clip1.mp4` … |
| 3 | 2–3 lo-fi MP3 | `assets/music/track1.mp3` … |
| 4 | Bio | TikTok + Reels |
| 5 | Статический caption | TikTok черновик |

**Клипы:** скролл · смена баз · карточка · kanban · formula.

### Mechanic — отдельный чат

**Маршрут:** `@mechanic` + копипаст ниже.

```
Тикет: docs/problems/2026-06-28-install-tiktok-script-writer-skill.md

Скачай SKILL.md в C:\Users\hramo\all skill\tiktok-script-writer\

ЗАПРЕЩЕНО: setup_product.py, pillow_pin.py, playwright_*, MIMO_FACTORY.md
```

### Coder — пилот скрипт (после skill установлен)

**Маршрут:** `@coder` + копипаст ниже.

```
TASK-023 pilot · slug notion-developer-career-os

Прочитай:
- skills/VIDEO_SCRIPT_SKILL.md
- products/draft/notion-developer-career-os/spec.json
- docs/team/common/VIDEO_PIPELINE.md

ОБЯЗАТЕЛЬНО вызови скиллы через /:
/copywriting
/marketing-psychology
/social-media
/tiktok-script-writer

Создай ТОЛЬКО:
products/draft/notion-developer-career-os/video-script.md

Builder tone. Hook = JTBD developers. ## Caption по шаблону (архив).

ЗАПРЕЩЕНО: mp4, scripts/, spec.json, listing, pillow_pin, covers
```

Lead verify → Owner слушает 2 голоса (Phase 0.5, после Mechanic Phase 1).

---

## Phase 1 — ждём (не стартовать пока cover не выбран)

| # | Кто | Что |
|---|-----|-----|
| 1 | Mechanic | `generate_video.py` + `pip install moviepy elevenlabs` |
| 2 | Mechanic | шаг 2.5 в `setup_product.py` |
| 3 | Lead→MiMo | `video-script.md` в MIMO_FACTORY Coder Mode |
| 4 | Mechanic | 2 voice варианта на Career OS |
| 5 | Owner | выбор `ELEVENLABS_VOICE_ID` |
| 6 | MiMo | backfill video-script × 7 |

Тикет: `docs/problems/2026-06-28-video-pipeline.md`

---

## Готово когда (Phase 0)

- [ ] `assets/notion-clips/` ≥ 4 mp4
- [ ] `assets/music/` ≥ 2 mp3
- [x] `ELEVENLABS_API_KEY` в `.env`
- [ ] Bio + caption TikTok настроены
- [ ] `all skill/tiktok-script-writer/SKILL.md` есть
- [ ] `video-script.md` пилот Career OS — Lead verify ✅

→ тогда Phase 1 Mechanic
