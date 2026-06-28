# NOTION_BLOCKS — Формат блоков для Welcome-страницы

МиМо генерирует `welcome_blocks` в spec.json по этому шаблону.
`notion_create.py` читает их и создаёт красивую страницу через API.

---

## Поддерживаемые типы блоков

```json
{"type": "heading_1",   "text": "...", "color": "default"}
{"type": "heading_2",   "text": "...", "color": "default"}
{"type": "callout",     "text": "...", "emoji": "👋", "color": "green_background"}
{"type": "paragraph",   "text": "..."}
{"type": "bullet",      "text": "..."}
{"type": "numbered",    "text": "..."}
{"type": "divider"}
{"type": "quote",       "text": "..."}
{"type": "toggle",      "text": "...", "children": [...]}
```

**Цвета callout:** `green_background` | `blue_background` | `yellow_background` | `purple_background` | `red_background`

---

## Эталонный шаблон Welcome-страницы (копируй в spec.json)

```json
"welcome_blocks": [
  {
    "type": "callout",
    "emoji": "👋",
    "text": "Welcome! This template helps you [ЧТО ДЕЛАЕТ]. Start with the Quick Start below.",
    "color": "green_background"
  },
  {
    "type": "divider"
  },
  {
    "type": "heading_2",
    "text": "⚡ Quick Start (3 steps)"
  },
  {
    "type": "numbered",
    "text": "Duplicate this page to your Notion workspace (button top-right)"
  },
  {
    "type": "numbered",
    "text": "Delete the sample data or keep it as a reference"
  },
  {
    "type": "numbered",
    "text": "Open [ГЛАВНАЯ БАЗА] and add your first entry"
  },
  {
    "type": "divider"
  },
  {
    "type": "heading_2",
    "text": "🗂 Database Overview"
  },
  {
    "type": "bullet",
    "text": "📋 [База 1] — [для чего, 1 строка]"
  },
  {
    "type": "bullet",
    "text": "📁 [База 2] — [для чего, 1 строка]"
  },
  {
    "type": "bullet",
    "text": "💰 [База 3, если есть] — [для чего, 1 строка]"
  },
  {
    "type": "divider"
  },
  {
    "type": "heading_2",
    "text": "🎯 Pro Tips"
  },
  {
    "type": "bullet",
    "text": "[Полезный совет по использованию 1]"
  },
  {
    "type": "bullet",
    "text": "[Полезный совет по использованию 2]"
  },
  {
    "type": "bullet",
    "text": "[Полезный совет по использованию 3]"
  },
  {
    "type": "divider"
  },
  {
    "type": "heading_2",
    "text": "➕ Adding Views (Board, Calendar, Gallery)"
  },
  {
    "type": "callout",
    "emoji": "ℹ️",
    "text": "Notion API doesn't support creating views automatically. Add them manually — it takes 30 seconds.",
    "color": "blue_background"
  },
  {
    "type": "numbered",
    "text": "Open any database in this template"
  },
  {
    "type": "numbered",
    "text": "Click the + icon next to the existing view tabs"
  },
  {
    "type": "numbered",
    "text": "Choose Board view → Group by Status for a Kanban layout"
  },
  {
    "type": "divider"
  },
  {
    "type": "callout",
    "emoji": "💬",
    "text": "Questions? Found a bug? Reply to your Gumroad receipt — I respond within 24 hours.",
    "color": "yellow_background"
  }
]
```

---

## Полный пример spec.json

```json
{
  "title": "Freelance Client Tracker",
  "slug": "notion-freelance-client-tracker",
  "emoji": "💼",
  "target_audience": "Freelancers & Independent Contractors",
  "price": 29,
  "tagline": "Never lose track of a client again",
  "cover_color": "green",

  "databases": [
    {
      "name": "Clients",
      "emoji": "👤",
      "properties": [
        {"name": "Name",            "type": "title"},
        {"name": "Status",          "type": "select",
         "options": [
           {"name": "Active",    "color": "green"},
           {"name": "Prospect",  "color": "yellow"},
           {"name": "On Hold",   "color": "orange"},
           {"name": "Inactive",  "color": "gray"}
         ]},
        {"name": "Email",           "type": "email"},
        {"name": "Monthly Revenue", "type": "number", "format": "dollar"},
        {"name": "Start Date",      "type": "date"},
        {"name": "Projects",        "type": "relation", "related_db": "Projects"}
      ],
      "sample_rows": [
        {
          "Name": "Acme Design Studio",
          "Status": "Active",
          "Email": "sarah@acmedesign.com",
          "Monthly Revenue": 3500,
          "Start Date": "2026-01-15"
        },
        {
          "Name": "TechFlow Inc.",
          "Status": "Active",
          "Email": "mark@techflow.io",
          "Monthly Revenue": 2200,
          "Start Date": "2026-03-01"
        },
        {
          "Name": "Bloom Agency",
          "Status": "Prospect",
          "Email": "hello@bloomagency.com",
          "Monthly Revenue": 0,
          "Start Date": null
        }
      ]
    },
    {
      "name": "Projects",
      "emoji": "📁",
      "properties": [
        {"name": "Name",       "type": "title"},
        {"name": "Status",     "type": "select",
         "options": [
           {"name": "In Progress", "color": "blue"},
           {"name": "Review",      "color": "yellow"},
           {"name": "Done",        "color": "green"},
           {"name": "Backlog",     "color": "gray"}
         ]},
        {"name": "Deadline",   "type": "date"},
        {"name": "Budget",     "type": "number", "format": "dollar"},
        {"name": "Client",     "type": "relation", "related_db": "Clients"}
      ],
      "sample_rows": [
        {
          "Name": "Brand Identity Redesign",
          "Status": "In Progress",
          "Deadline": "2026-07-15",
          "Budget": 5000
        },
        {
          "Name": "Website Revamp",
          "Status": "Review",
          "Deadline": "2026-07-01",
          "Budget": 3500
        }
      ]
    }
  ],

  "welcome_blocks": [
    {
      "type": "callout",
      "emoji": "👋",
      "text": "Welcome! This template helps freelancers manage clients, projects, and revenue — all in one connected workspace.",
      "color": "green_background"
    },
    {"type": "divider"},
    {"type": "heading_2", "text": "⚡ Quick Start (3 steps)"},
    {"type": "numbered", "text": "Duplicate this page to your Notion workspace"},
    {"type": "numbered", "text": "Delete the sample data or keep it as a reference"},
    {"type": "numbered", "text": "Open the Clients database and add your first client"},
    {"type": "divider"},
    {"type": "heading_2", "text": "🗂 Database Overview"},
    {"type": "bullet", "text": "👤 Clients — track every client with status, revenue, and contact info"},
    {"type": "bullet", "text": "📁 Projects — manage deliverables linked to each client"},
    {"type": "divider"},
    {"type": "heading_2", "text": "🎯 Pro Tips"},
    {"type": "bullet", "text": "Use the Status filter in Clients to focus on Active accounts only"},
    {"type": "bullet", "text": "Link every Project to a Client to see the full relationship"},
    {"type": "bullet", "text": "Add a Board view to Projects and group by Status for a Kanban board"},
    {"type": "divider"},
    {
      "type": "callout",
      "emoji": "💬",
      "text": "Questions? Reply to your Gumroad receipt — I respond within 24 hours.",
      "color": "yellow_background"
    }
  ]
}
```

---

## Relations в sample_rows — ОБЯЗАТЕЛЬНО

Rollup **не работает**, если relations пустые в `sample_rows`.

| Правило | Почему |
|---|---|
| Title-поле = `"Name"` | `notion_create.py` линкует по ключу `Name` |
| Каждый relation → ключ в sample_rows | Иначе Skill Count / Task Count = 0 |
| Двусторонние связи — обе стороны | Projects.Skills + Skills.Projects |
| Имена строк — **точное совпадение** | "React" ≠ "react" |

```json
{"Name": "My Project", "Skills": ["React", "TypeScript"]}
{"Name": "React", "Projects": ["My Project"]}
```

Verify: в логе `notion_create.py` → `Linked N rows via relations`, N ≥ 3.
