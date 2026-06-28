# [TICKET] Video Pipeline — generate_video.py + интеграция

**Продукт:** factory-wide
**Приоритет:** high
**Статус:** open

## Задача

Реализовать автогенерацию TikTok/Reels видео по плану `docs/team/common/VIDEO_PIPELINE.md`.

## Что сделать

1. `pip install moviepy elevenlabs` (документировать в README или комментарий в скрипте)
2. Создать `scripts/generate_video.py`:
   - Вход: `<slug>`
   - Читает `products/draft/<slug>/video-script.md` (hook, voiceover, CTA, caption)
   - ElevenLabs → `voiceover.mp3` (ключ `ELEVENLABS_API_KEY` из `.env`)
   - moviepy: фон из случайного `assets/notion-clips/clip*.mp4`, hook-текст, voiceover, CTA, 1080×1920
   - Fallback если нет clips: `gumroad-thumb.png` + Ken Burns zoom
   - Музыка из `assets/music/*.mp3` (тихий фон, fade out на CTA)
   - Выход: `tiktok-video.mp4` + `tiktok-caption.txt` (из ## Caption, архив)
3. `setup_product.py` — шаг 2.5 после Designer Mode:
   ```python
   if (draft / 'video-script.md').exists():
       run([py, 'scripts/generate_video.py', slug], '2.5/3  Video')
   ```
4. `.mimocode/MIMO_FACTORY.md` — Coder Mode:
   - `video-script.md` в списке файлов
   - **Перед video-script.md** — обязательный блок:
   ```markdown
   /copywriting
   /marketing-psychology
   /social-media
   /tiktok-script-writer
   ```
   Канон: `skills/VIDEO_SCRIPT_SKILL.md` §4.1
5. `skills/MIMO_SKILL.md` — §4.1 (Lead ✅)
6. `skills/VIDEO_SCRIPT_SKILL.md` — канон 4 скиллов (Lead ✅)
7. Тикет `install-tiktok-script-writer-skill.md` — клон SKILL.md в `all skill/`
6. Создать пустые папки `assets/music/` и `assets/notion-clips/` с `.gitkeep`

## Не делать

- Автозаливку в TikTok
- Запись notion-clips (это Owner)

## Проверка

```bash
python scripts/generate_video.py notion-developer-career-os
```
(нужен тестовый `video-script.md` в draft — Mechanic может создать минимальный для теста)

## Решено

_(Mechanic заполняет после закрытия)_
