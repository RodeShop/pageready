# VIDEO_PIPELINE — TikTok/Reels (согласовано 28.06.2026)

_Статус: Phase 0 prep · Phase 1 после cover (TASK-022)_

---

## Решения Owner (28.06)

| Вопрос | Решение |
|--------|---------|
| Визуал | **Гибрид C** — hook на живом скринкасте, середина Ken Burns обложки, CTA на тёмном фоне |
| Язык | **English only** (голос + текст на экране) |
| Голос | **2 тестовых варианта** на пилоте → выбираем один voice ID для конвейера |
| Музыка | **Lo-fi / chill** — study-with-me вайб, тихо под голосом |
| Старт кода | **После rebuild wave** — не мешаем TASK-016 |
| Очередь | **Конвейер:** продукт → video-script → mp4 в папку → Owner заливает когда удобно |
| Backfill | **Все 7 live** — тоже получат видео (MiMo допишет script, скрипт сгенерит mp4) |
| Позиционирование | **Notion-разработчик** — решает боли людей; ниша = конкретное видео |
| Bio TikTok/Reels | `I build Notion systems that solve real problems → Link to shop` |

---

## Позиционирование

### Аккаунт (один раз — не зависит от ниши)

**Кто ты:** Notion-разработчик, который проектирует системы под **реальные боли людей**.

Фабрика берёт ниши из TRENDS — сегодня freelancers, завтра podcasters, потом wedding planners. **Аккаунт не перечисляет ниши** — он про роль builder'а. **Чью боль решаешь** — видно из конкретного видео (hook + voiceover под `target_audience` продукта).

**Метафора:** столяр делает мебель для разных домов — не притворяется, что живёт в каждом.

| Уровень | Что говорит | Пример |
|---------|-------------|--------|
| **Аккаунт** (bio + статический caption) | Я builder, решаю проблемы через Notion | см. ниже |
| **Видео** (hook + voice) | Боль **этой** аудитории + система для них | «For freelancers who lose track of clients…» |
| **Продукт** | Конкретная OS под нишу из TRENDS | Freelance Client OS, Study OS, etc. |

**Bio (TikTok + Instagram) — настроить один раз:**
```
I build Notion systems that solve real problems → [shop link]
```

**Статический caption при заливке — один на все посты:**
```
Notion systems built for real problems. Link in bio.
#notion #notiontemplate #notionos
```

Нишевой хэштег (`#freelancelife`, `#studytok`…) — **не в caption Owner'а**. MiMo кладёт в `tiktok-caption.txt` (архив); боль и аудитория уже **внутри видео**.

### Тон в видео (каждый продукт — свой)

| ❌ Не так | ✅ Так |
|----------|--------|
| "I struggled with tracking my clients" | "Here's the system I built for freelancers who lose track of clients" |
| "I needed this for myself" | "This OS is designed for developers managing skills and job applications" |
| "My template" | "A complete Notion system for [audience]" |

**Почему:** воспринимаемая ценность выше — ты **builder**, который проектирует системы, не «чувак со своим шаблоном». Оправдывает $19 и сильнее для портфолио.

**Голос в скрипте:**
- Hook — боль **аудитории** (вопрос или факт про них)
- Voiceover — «I built…» / «This system gives [audience]…» / «Designed for…»
- Запрещено: «I was struggling», «When I started freelancing», «I made this for myself»

---

## Caption (конвейер — Owner не трогает)

**Owner не пишет caption.** При заливке — только статический текст из секции «Аккаунт» выше.

**Внутри конвейера:**
- MiMo пишет `## Caption` в `video-script.md` — per-product, для verify и архива
- `generate_video.py` → `tiktok-caption.txt` рядом с mp4
- Lead verify: caption по шаблону, builder tone, JTBD

**Шаблон MiMo (per-product, внутренний):**
```
[Hook — дословно из ## Hook]

Built for [аудитория] who [боль одной фразой].
[N] databases. $[цена]. Link in bio.

#notion #notiontemplate #[нишевой хэштег]
```

---

## Скиллы — обязательно перед video-script.md

**4 скилла через `/`** — канон: `skills/VIDEO_SCRIPT_SKILL.md`

| # | Скилл | Путь |
|---|-------|------|
| 1 | `/copywriting` | `C:/Users/hramo/all skill/copywriting/SKILL.md` |
| 2 | `/marketing-psychology` | `C:/Users/hramo/all skill/marketing-psychology/SKILL.md` |
| 3 | `/social-media` | `C:/Users/hramo/all skill/social-media/SKILL.md` |
| 4 | `/tiktok-script-writer` | `C:/Users/hramo/all skill/tiktok-script-writer/SKILL.md` |

**tiktok-script-writer** — GitHub [Affitor/affiliate-skills](https://github.com/Affitor/affiliate-skills) (MIT). Beat-структура hook→pain→demo→CTA, ≤10 слов в spoken, overlay каждые 3–5 сек. Mechanic клонирует SKILL.md в `all skill/`.

**social-media** — уже локально. TikTok algo: watch time, hook 0–3 сек, vertical, silent viewers.

Без всех 4 → Grade B → mp4 не генерим.

Mechanic: `MIMO_FACTORY.md` Coder Mode — блок скиллов перед `video-script.md`.

---

## Цель

К каждому продукту автоматически генерировать короткое видео (20–30 сек) для TikTok и Instagram Reels.

**Формат:** faceless — гибридный визуал + AI-голос + текст-оверлей + lo-fi музыка.

**Owner заливает вручную** — автопостинг не делаем (риск бана).  
**Owner делает только одно:** загрузить mp4 в отложку TikTok + Reels. Caption — статический, один раз.

---

## Визуальный стиль (гибрид)

```
┌─────────────────────────────────────┐
│  0:00–0:03  HOOK                    │
│  Живой Notion screencast (assets/)  │
│  Крупный белый текст = боль (≤8 слов)│
│  Движение в первые 0.5 сек — обязательно │
├─────────────────────────────────────┤
│  0:03–0:22  DEMO + VOICE            │
│  gumroad-thumb.png Ken Burns zoom   │
│  AI голос 40–60 слов                │
│  3–4 feature-подписи по таймингу  │
├─────────────────────────────────────┤
│  0:22–0:30  CTA                     │
│  Тёмный фон (#1a1a2e)               │
│  «Get [Product Name] on Gumroad»    │
│  $19 — one-time · rodeshop.gumroad… │
│  Lo-fi fade out                     │
└─────────────────────────────────────┘
```

**Брендинг:** шрифт sans-serif bold (как на обложках Direction D), белый текст + тень для читаемости.

**Формат:** 1080×1920 (9:16), H.264, 30fps.

---

## Стек

| Компонент | Инструмент | Кто |
|-----------|------------|-----|
| Сборка | `moviepy` | Mechanic |
| Голос | ElevenLabs API | Mechanic + Owner (ключ) |
| Hook-фон | `assets/notion-clips/*.mp4` | Owner (разово) |
| Demo-фон | `gumroad-thumb.png` из draft | авто (Designer) |
| Музыка | `assets/music/*.mp3` lo-fi | Owner (разово) |
| Скрипт | `video-script.md` | MiMo (Coder Mode) |

```
pip install moviepy elevenlabs
ELEVENLABS_API_KEY=...   # в .env
```

---

## Конвейер (полная цепочка)

```
MiMo Coder Mode
  → video-script.md (hook + voiceover + CTA + caption)
       ↓
Designer Mode
  → gumroad-thumb.png
       ↓
setup_product.py шаг 2.5
  → generate_video.py <slug>
  → tiktok-video.mp4 + tiktok-caption.txt (архив)
       ↓
Lead verify
  → ready/
       ↓
Owner
  → только заливка mp4 в отложку (статический caption)
```

**Важно:** видео генерится с каждым продуктом. Owner раз в неделю (или когда накопилось) — **одна сессия**: загрузить пачку mp4 в Schedule. Caption не трогает.

---

## Файл `video-script.md`

MiMo создаёт в Coder Mode:

```markdown
# Video Script — [Product Name]

## Hook (3 sec, on-screen text)
[Audience pain — max 8 words, about THEM not you]
Example: "Freelancers losing clients between projects?"

## Voiceover (20 sec, ElevenLabs reads this)
[40-60 words. Builder voice: "I built…" / "Designed for…". 3-4 features.]
Example: "I built this Notion OS for freelancers who juggle clients,
projects, and invoices in separate places. Five linked databases —
open any client and see every project and what they owe.
Ten realistic examples included so they can start today."

## CTA (5 sec, on-screen text)
Get the [Product Name] on Gumroad
$19 — one-time payment
rodeshop.gumroad.com/l/<slug>

## Caption (internal — MiMo, Owner не использует)
[Hook — дословно из ## Hook]

Built for [audience] who [pain phrase].
[N] databases. $[price]. Link in bio.

#notion #notiontemplate #[niche hashtag]
```

Verify: hook ≤8 слов · voiceover 40–60 слов · CTA · caption по шаблону · builder tone.

**Выход конвейера на slug:**
```
products/ready/<slug>/
  tiktok-video.mp4      ← Owner заливает
  tiktok-caption.txt    ← архив, Owner не открывает
  video-script.md       ← внутренний, Owner не открывает
```

---

## `scripts/generate_video.py`

```
generate_video.py <slug>
  1. Читает products/draft/<slug>/video-script.md
  2. ElevenLabs → voiceover.mp3 (voice_id из .env после пилота)
  3. moviepy:
     a. [0-3s]  random clip из assets/notion-clips/ + hook text overlay
     b. [3-22s] gumroad-thumb.png Ken Burns + voiceover + feature captions
     c. [22-30s] dark CTA slide + lo-fi music fade
     d. Export 1080x1920 tiktok-video.mp4
  4. Пишет tiktok-caption.txt из секции ## Caption (архив)
  5. Удаляет temp voiceover.mp3
```

Интеграция в `setup_product.py` — после pillow_pin, до publish:

```python
if (draft / 'video-script.md').exists():
    run([py, 'scripts/generate_video.py', slug], '2.5/3  Video')
```

---

## Что Owner делает

**Зона Owner = только заливка.** Никаких скриптов, caption, video-script.

### Разово (до старта)

| # | Действие |
|---|----------|
| 1 | ElevenLabs API key → `.env` |
| 2 | 4–5 клипов Notion → `assets/notion-clips/` |
| 3 | 2–3 lo-fi трека → `assets/music/` |
| 4 | Bio TikTok + Reels (builder) + ссылка на shop |
| 5 | **Статический caption** в TikTok — сохранить как черновик / «последний caption» (см. выше) |
| 6 | Пилот голоса — выбрать из 2 вариантов (один раз) |

### Заливка — отложка, несколько в день

Фабрика растёт быстрее чем постинг → **3 видео в день** в Schedule.

**Слоты (EST, прайм US):**

| Слот | Время EST | Зачем |
|------|-----------|-------|
| 1 | **12:00** | US East обед / EU вечер |
| 2 | **18:00** | US after work — главный |
| 3 | **21:00** | US вечер |

**Сессия Owner (~20 мин раз в неделю или когда ≥9 mp4 в очереди):**
1. Открыть TikTok → Upload → Schedule
2. Загрузить пачку mp4 из `products/ready/*/tiktok-video.mp4`
3. На каждое: тот же статический caption (TikTok подставит последний)
4. Расставить по слотам 12:00 / 18:00 / 21:00 EST
5. Reels — то же

**Не смотреть каждое видео** — Lead verify уже прошёл. Spot-check 1 из 10 опционально.

### Расписание backfill (7 live) — 3 дня

| День | 12:00 EST | 18:00 EST | 21:00 EST |
|------|-----------|-----------|-----------|
| **Д1** | study-knowledge-management | job-search-command-center | developer-career-os |
| **Д2** | freelance-client-tracker | social-media-content-calendar | personal-finance-tracker |
| **Д3** | startup-metrics-okr-tracker | — | — |

Новые продукты → следующие свободные слоты в очереди (FIFO, 3/день).

**Рост очереди:** при 1 новом продукте/день от фабрики — 3 слота/день успевают. При ускорении фабрики → увеличить до **4–5/день** (добавить слоты 09:00, 15:00 EST).

### Пилот голоса (один раз)

1. Mechanic генерит **2 варианта** ElevenLabs на `notion-developer-career-os`
2. Owner слушает **на телефоне** с наушниками — оба до конца

**Критерии выбора (все 3 должны пройти):**

| # | Критерий | Как проверить |
|---|----------|---------------|
| 1 | **Досмотрел до конца без «морщинки»** | Не хочется выключить на 5-й секунде |
| 2 | **Звучит как человек, не робот** | Нет металлического/монотонного AI-вайба |
| 3 | **Темп комфортный для 25 сек** | Успеваешь усвоить фичи, не торопится и не тянет |

Победитель → `ELEVENLABS_VOICE_ID=...` в `.env` → все следующие видео этим голосом.

---

## Backfill 7 live продуктов

После пайплайна готов:

1. Lead → TASK: MiMo пишет `video-script.md` (+ caption) для каждого slug
2. `python scripts/generate_video.py <slug>` × 7
3. mp4 в `products/ready/<slug>/`
4. Owner — одна сессия: 7 mp4 в отложку за 3 дня (3+3+1)

---

## Метрики успеха

**Отсчёт:** с даты **первого запланированного поста** (Пн 18:00 EST).

**Через 30 дней:**

| Результат | Критерий | Действие |
|-----------|----------|----------|
| ✅ **Успех** | ≥1 продажа Gumroad с UTM/referrer TikTok или Reels | Продолжаем: тот же hook-формат, тот же голос |
| ⚠️ **Пересмотр** | 0 продаж | Меняем **hook формулу** (не голос, не визуал) — Lead обновляет шаблон в MIMO_SKILL |
| 📊 **Доп.** | Views < 500 на 3+ видео | Проверить движение в первые 0.5 сек + нишевой хэштег |

**UTM для отслеживания:** `?utm_source=tiktok&utm_medium=video&utm_campaign=<slug>`  
(Lead/Mechanic в linktree — Owner не настраивает)

**Не считаем провалом:** мало views при 0 продаж в первые 2 недели — алгоритм прогревается.

---

## План работ (пошагово)

| Шаг | Кто | Когда | Результат |
|-----|-----|-------|-----------|
| 0 | MiMo | сейчас | Rebuild wave завершён (TASK-016) |
| 1 | Owner | параллельно rebuild | `assets/notion-clips/` + `assets/music/` + ElevenLabs key |
| 2 | Lead | после rebuild | TASK-017 → Mechanic: `generate_video.py` |
| 3 | Mechanic | TASK-017 | скрипт + интеграция setup_product.py |
| 4 | Lead | после 3 | video-script в MIMO_FACTORY + MIMO_SKILL verify |
| 5 | Mechanic + Owner | пилот | 2 voice варианта на Developer Career OS |
| 6 | Owner | выбор голоса | `ELEVENLABS_VOICE_ID` в .env |
| 7 | MiMo | backfill TASK | video-script + mp4 × 7 |
| 8 | Owner | одна сессия | отложка: **3 видео/день**, статический caption |
| 9 | Owner | +30 дней | метрики: ≥1 продажа = успех |

---

## Verify чеклист (Lead)

- [ ] `video-script.md` — hook, voiceover, CTA, ## Caption, builder tone
- [ ] `tiktok-caption.txt` сгенерирован (архив)
- [ ] `tiktok-video.mp4` — 20–30 сек, 1080×1920
- [ ] Первые 0.5 сек — видимое движение
- [ ] Голос читаем, музыка не перебивает
- [ ] CTA показывает правильный slug/цену

---

## Не делаем

- Автозаливку TikTok/Reels
- Лицо на камеру
- Русский язык (пока)
- Видео без продукта (каждый mp4 привязан к slug)

---

## Тикет Mechanic

`docs/problems/2026-06-28-video-pipeline.md` — открыть после rebuild.
