# DESIGNER_SKILL — MiMo Designer Mode

Этот скилл активируется когда Architect переключает MiMo в режим дизайнера.

Источник: ConardLi/garden-skills · gpt-image-2 (MIT) — адаптировано под фабрику.

---

## Твоя задача в Designer Mode

Для каждого продукта сгенерировать:
1. **Pinterest pin** — изображение 1000×1500px
2. **Gumroad thumbnail** — изображение 1600×900px
3. **Промпты** для генерации если нет OpenAI ключа

---

## Определение режима (сделай это первым)

```python
import os
has_openai = bool(os.environ.get('OPENAI_API_KEY'))
has_garden = os.environ.get('ENABLE_GARDEN_IMAGEGEN') in ('1','true','yes')
```

| Условие | Режим | Действие |
|---------|-------|----------|
| `OPENAI_API_KEY` + `ENABLE_GARDEN_IMAGEGEN=1` | **A** | Генерируй через `scripts/generate_image.py` |
| Нет ключа или флага | **B** | Генерируй через `scripts/pillow_pin.py` (Pillow, бесплатно) |

**Режим B — основной.** Pillow всегда доступен, бесплатно, стабильно.

---

## Режим B: Pillow-генерация (основной)

Запускай: `python scripts/pillow_pin.py <slug>`

Скрипт создаёт:
```
products/ready/<slug>/
├── pinterest-pin.png     ← 1000×1500px
└── gumroad-thumb.png     ← 1600×900px
```

### Что должно быть на Pinterest pin (1000×1500)

```
Фон: градиент под нишу (см. цвета ниже)
Верхний блок (40%):
  - Большой эмодзи продукта (центр)
  - Лейбл "NOTION TEMPLATE" мелким шрифтом
Средний блок (40%):
  - Заголовок шаблона (2-3 строки, крупно)
  - Подзаголовок: "for [аудитория]"
Нижний блок (20%):
  - "RodeShop" логотип
  - Цена: "From $19"
  - URL: rodeshop.github.io/RodeShop
```

### Цвета по нишам

| Ниша | Фон (от) | Фон (до) | Акцент |
|------|----------|----------|--------|
| Freelance | #f0fdf4 | #dcfce7 | #059669 |
| Content/Creator | #fef9c3 | #fef08a | #ca8a04 |
| Students/Study | #ede9fe | #ddd6fe | #7c3aed |
| Startup/Business | #eff6ff | #dbeafe | #2563eb |
| Finance | #fff7ed | #ffedd5 | #ea580c |
| Job Search | #fdf2f8 | #fce7f3 | #db2777 |

### Что должно быть на Gumroad thumbnail (1600×900)

```
Фон: тот же градиент ниши
Левая половина:
  - Большой эмодзи (150px)
  - Название шаблона (крупно)
  - Аудитория (средне, серый)
Правая половина:
  - 3-4 иконки с ключевыми фичами:
    📊 Clients Database
    📁 Projects Tracker  
    💰 Revenue Dashboard
  - Цена внизу: "$29"
```

---

## Режим A: OpenAI GPT Image 2 (если есть ключ)

Запускай: `python scripts/generate_image.py <slug> pinterest`

Промпт-формула для Pinterest pin:
```
Clean minimal digital product mockup. Notion template for [АУДИТОРИЯ].
Background: soft [ЦВЕТ] gradient. Large [ЭМОДЗИ] emoji centered.
Text overlay: "[НАЗВАНИЕ]" in bold Inter font.
Subtitle: "for [АУДИТОРИЯ]". Brand tag "RodeShop" at bottom.
Professional, modern, conversion-optimized. No people. Flat design.
Size: 1000x1500 portrait. Style: Gumroad/Etsy digital product listing.
```

---

## Файлы которые Designer создаёт

```
products/ready/<slug>/
├── pinterest-pin.png       ← изображение для пина
├── gumroad-thumb.png       ← обложка листинга
└── image-prompts.md        ← промпты (для повторной генерации)
```

---

## Чеклист Designer перед сдачей

- [ ] pinterest-pin.png существует и не пустой
- [ ] gumroad-thumb.png существует и не пустой
- [ ] Цвета соответствуют нише продукта
- [ ] Название шаблона читается на thumbnail
- [ ] Обновить board.html: subtask Designer → done
