# [TICKET] Установить tiktok-script-writer skill

**Продукт:** factory-wide (video pipeline)  
**Приоритет:** medium  
**Статус:** open  
**Блокер:** после rebuild, вместе с video-pipeline.md

## Задача

Склонировать SKILL.md из GitHub в `all skill/` для вызова MiMo через `/tiktok-script-writer`.

## Команда

```powershell
mkdir "C:\Users\hramo\all skill\tiktok-script-writer" -Force
curl -o "C:\Users\hramo\all skill\tiktok-script-writer\SKILL.md" ^
  "https://raw.githubusercontent.com/Affitor/affiliate-skills/main/skills/content/tiktok-script-writer/SKILL.md"
```

Источник: https://github.com/Affitor/affiliate-skills (MIT)

## RodeShop-адаптация (MiMo читает VIDEO_SCRIPT_SKILL.md)

- Без FTC `#ad` — свой продукт
- 20–30 сек, не 45–60
- Builder tone, не affiliate persona
- Hook style default: `demo_first` (Notion визуален)

## Проверка

Файл существует: `C:/Users/hramo/all skill/tiktok-script-writer/SKILL.md`  
MiMo в Coder Mode видит `/tiktok-script-writer` в MIMO_FACTORY.md

## Связано

- `docs/problems/2026-06-28-video-pipeline.md`
- `skills/VIDEO_SCRIPT_SKILL.md`
