# VIDEO_SCRIPT_SKILL — TikTok/Reels скрипты (RodeShop)

_Канон для MiMo при создании `video-script.md`. Verify: Lead._

---

## Обязательные скиллы — вызов через `/` перед video-script.md

Порядок важен. **Не читать пассивно — вызывать.**

| # | Скилл | Путь |
|---|-------|------|
| 1 | `/copywriting` | `C:/Users/hramo/all skill/copywriting/SKILL.md` |
| 2 | `/marketing-psychology` | `C:/Users/hramo/all skill/marketing-psychology/SKILL.md` |
| 3 | `/social-media` | `C:/Users/hramo/all skill/social-media/SKILL.md` |
| 4 | `/tiktok-script-writer` | `C:/Users/hramo/all skill/tiktok-script-writer/SKILL.md` |

Без всех четырёх → video-script = **Grade B** → mp4 не генерим.

**Источник tiktok-script-writer:** [Affitor/affiliate-skills](https://github.com/Affitor/affiliate-skills/tree/main/skills/content/tiktok-script-writer) (MIT). Mechanic клонирует в `all skill/tiktok-script-writer/`.

---

## Что брать из каждого скилла

| Скилл | Применить к |
|-------|-------------|
| **copywriting** | Clarity, benefits > features, specificity, ≤10 слов в spoken-фразах |
| **marketing-psychology** | JTBD, loss aversion в hook, present bias, contrast |
| **social-media** | TikTok: watch time, hook 0–3 сек, vertical 9:16, captions для silent viewers |
| **tiktok-script-writer** | Beat-структура, text overlay каждые 3–5 сек, hook style |

---

## RodeShop-адаптация tiktok-script-writer

| В affiliate-skills | У нас |
|--------------------|-------|
| Affiliate product | **Свой** Gumroad OS ($19) |
| FTC `#ad` overlay | **Не нужен** — свой продукт |
| Личная история | **Builder tone** — «I built for [audience]» |
| 45–60 сек | **20–30 сек** |
| Demo on camera | **Гибрид:** screencast hook → thumb zoom → CTA slide |

**Hook style по умолчанию:** `demo_first` или `relatable` — Notion визуален.

---

## Beat-структура (25 сек → video-script.md)

| Time | Сегмент | Visual (generate_video.py) | video-script.md |
|------|---------|---------------------------|-----------------|
| 0–3s | **Hook** | notion-clips + text overlay | `## Hook` |
| 3–8s | **Pain** | thumb zoom starts | начало `## Voiceover` |
| 8–22s | **Demo** | thumb + feature captions | `## Voiceover` (3–4 фичи) |
| 22–30s | **CTA** | dark slide | `## CTA` |

**Правила из tiktok-script-writer:**
1. Spoken ≤10 слов на фразу
2. Новый text overlay / смена визуала каждые 3–5 сек
3. Hook **заканчивается setup'ом**, не голым вопросом
4. Text overlay = история без звука (40% смотрят без audio)
5. Demo = конкретная фича, не «amazing system»

---

## Позиционирование (аккаунт vs видео)

- **Аккаунт:** Notion-разработчик, решает реальные проблемы — bio/caption статические
- **Видео:** боль **target_audience этого slug** — из TRENDS

Запрещено: «I struggled», «for myself», «my template».

---

## Формат video-script.md

```markdown
# Video Script — [Product Name]

## Hook (3 sec, on-screen text)
[Audience pain — max 8 words]

## Voiceover (20 sec)
[40-60 words. Builder. Short sentences. 3-4 features.]

## CTA (5 sec, on-screen text)
Get the [Product Name] on Gumroad
$[price] — one-time payment
rodeshop.gumroad.com/l/<slug>

## Caption (internal — archive)
[Hook дословно]

Built for [audience] who [pain].
[N] databases. $[price]. Link in bio.

#notion #notiontemplate #[niche hashtag]
```

Owner **не использует** Caption — только mp4 + статический caption аккаунта.

---

## Verify чеклист

- [ ] 4 скилла вызваны (`/copywriting` … `/tiktok-script-writer`)
- [ ] Hook ≤8 слов, JTBD, loss aversion
- [ ] Voiceover: builder tone, spoken phrases ≤10 слов
- [ ] CTA: slug + цена верны
- [ ] Caption по шаблону (архив)
- [ ] Нет buzzwords: streamline, leverage, game-changer, all-in-one

---

## GitHub — что смотрели, что не берём

| Репо | Вердикт |
|------|---------|
| [Affitor/tiktok-script-writer](https://github.com/Affitor/affiliate-skills) | ✅ **Подключаем** — beat-структура |
| [tanishaio/creator-studio-skill](https://github.com/tanishaio/creator-studio-skill) | 📎 Идеи hook_library — не клонируем (нужен voice-setup) |
| [45ck/content-machine](https://github.com/45ck/content-machine) | ❌ Другой пайплайн — у нас moviepy |
| [aituberapp/ai-video-skill](https://github.com/aituberapp/ai-video-skill) | ❌ SaaS API, не наш стек |
| [hiteshK03/video-production-skill](https://github.com/hiteshK03/video-production-skill) | ❌ DaVinci Resolve — overkill |
