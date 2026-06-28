# SCRIPTS MAP — Gumroad Factory

**Ведёт:** Lead — обновляет при появлении **нового скрипта/модуля**  
**Читают:** все исполнители перед стартом задачи

> Цель: агент сразу понимает что уже существует и куда идти.  
> Не дублировать логику — сначала проверь здесь.

---

## Как читать

Перед созданием нового скрипта / функции — найди здесь, нет ли похожего.  
Если нашёл — **расширяй существующее**, не создавай новое.  
Не нашёл — создай и скажи Lead добавить строку в эту карту.

---

## Pipeline скрипты

| Скрипт | Путь | Что делает |
|--------|------|-----------|
| setup_product | `scripts/setup_product.py` | Полный цикл: Notion + Gumroad для одного slug |
| playwright_notion | `scripts/playwright_notion.py` | Создание базы в Notion по spec.json |
| playwright_gumroad | `scripts/playwright_gumroad.py` | Публикация продукта на Gumroad |
| generate_listing | `scripts/generate_listing.py` | Генерация листинга (описание + теги) |
| generate_video | `scripts/generate_video.py` | Генерация TikTok-видео (moviepy + ElevenLabs) |
| promote | `scripts/promote.py` | Автопостинг Pinterest |

## Bat-скрипты (запуск)

| Файл | Что делает |
|------|-----------|
| `mimo_loop.bat` | Запуск MiMo factory loop (бесконечный цикл) |
| `rebuild_loop.bat` | Rebuild pipeline loop |
| `run_setup.bat` | Разовый запуск setup |

## Ключевые конфиги / данные

| Файл | Путь | Что хранит |
|------|------|-----------|
| spec.json | `products/draft/<slug>/spec.json` | Спецификация продукта для MiMo |
| TRENDS | `research/TRENDS.md` | Очередь ниш |
| MIMO_FACTORY | `.mimocode/MIMO_FACTORY.md` | Инструкции MiMo factory |
| MIMO_SKILL | `skills/MIMO_SKILL.md` | Стандарты качества продукта |

---

## Правила Lead при обновлении

1. **Новый скрипт** → добавить строку в таблицу
2. **Удалён скрипт** → удалить строку + проверить что ничего не вызывает его
3. **Переименован** → обновить таблицу
4. Не перечислять каждую функцию — только модули

---

_Gumroad Factory · SCRIPTS_MAP · Lead обновляет при структурных изменениях_
