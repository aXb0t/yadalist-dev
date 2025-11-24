# Yadalist Design System Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     STORYBOOK (Workshop)                     │
│                   http://localhost:6006                      │
│  ┌────────────┬────────────┬────────────┬────────────┐     │
│  │  Buttons   │   Forms    │   Alerts   │    Nav     │     │
│  │  Stories   │  Stories   │  Stories   │  Stories   │     │
│  └────────────┴────────────┴────────────┴────────────┘     │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │ Document & Preview
                              │
┌─────────────────────────────┴───────────────────────────────┐
│              DESIGN SYSTEM (Source of Truth)                 │
│                    frontend/src/                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  input.css                                            │  │
│  │  ├─ @tailwind base                                    │  │
│  │  ├─ @tailwind components                             │  │
│  │  │   └─ Custom component classes (btn, form, etc)    │  │
│  │  └─ @tailwind utilities                              │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  tailwind.config.js                                   │  │
│  │  └─ Nord Theme (colors, fonts, spacing, shadows)     │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
                              │
                              │ Build Process
                              │ (PostCSS + Tailwind)
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   COMPILED CSS OUTPUT                        │
│                 frontend/dist/yadalist-ui.css                │
│  - All Tailwind utilities                                    │
│  - Custom component classes                                  │
│  - Nord theme variables                                      │
│  - Minified for production                                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ Django STATICFILES_DIRS
                              │ or Docker COPY
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    DJANGO TEMPLATES                          │
│              accounts/templates/accounts/*.html              │
│                                                              │
│  {% load static %}                                           │
│  <link rel="stylesheet" href="{% static 'yadalist-ui.css' %}">│
│                                                              │
│  <button class="btn btn--primary">Login</button>            │
│  <div class="alert alert--success">Success!</div>           │
│  <input class="form-input" type="text">                     │
└─────────────────────────────────────────────────────────────┘
```

## Development Workflow

```
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│   Designer   │      │  Developer   │      │    Django    │
│              │      │              │      │   Runtime    │
└──────┬───────┘      └──────┬───────┘      └──────┬───────┘
       │                     │                     │
       │ 1. Design in        │                     │
       │    Storybook        │                     │
       │ ───────────►        │                     │
       │                     │                     │
       │                     │ 2. Update           │
       │                     │    input.css        │
       │                     │ ───────────►        │
       │                     │                     │
       │                     │    (Auto rebuild    │
       │                     │     via watch)      │
       │                     │                     │
       │ 3. Preview in       │                     │
       │    Storybook        │                     │
       │ ◄───────────────────┤                     │
       │                     │                     │
       │                     │ 4. Use classes      │
       │                     │    in Django        │
       │                     │    templates        │
       │                     │ ─────────────────►  │
       │                     │                     │
       │                     │                     │ 5. CSS loaded
       │                     │                     │    from static
       │                     │                     │    files
       │                     │ ◄───────────────────│
```

## Docker Architecture

### Development (docker-compose.yml)

```
┌─────────────────────────────────────────────────────────────┐
│                      Docker Compose                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   frontend   │  │  storybook   │  │     web      │     │
│  │  (node:20)   │  │  (node:20)   │  │  (python)    │     │
│  │              │  │              │  │              │     │
│  │ - npm        │  │ - npm        │  │ - Django     │     │
│  │   install    │  │   install    │  │ - Loads CSS  │     │
│  │ - npm run    │  │ - npm run    │  │   from       │     │
│  │   build      │  │   storybook  │  │   frontend/  │     │
│  │ - npm run    │  │              │  │   dist/      │     │
│  │   watch:css  │  │ Port: 6006   │  │              │     │
│  │              │  │              │  │ Port: 8000   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│         │                  │                  │            │
│         │                  │                  │            │
│         ▼                  ▼                  ▼            │
│  ┌──────────────────────────────────────────────────┐     │
│  │          Shared Volumes                           │     │
│  │  - ./frontend:/app/frontend                       │     │
│  │  - ./staticfiles:/app/staticfiles                 │     │
│  └──────────────────────────────────────────────────┘     │
│                                                              │
│  ┌──────────────┐                                          │
│  │      db      │                                          │
│  │ (postgres)   │                                          │
│  └──────────────┘                                          │
└─────────────────────────────────────────────────────────────┘
```

### Production (Dockerfile Multi-stage)

```
┌─────────────────────────────────────────────────────────────┐
│                  Stage 1: Frontend Build                     │
│                    FROM node:20                              │
├─────────────────────────────────────────────────────────────┤
│  1. COPY frontend/package*.json                             │
│  2. RUN npm ci --only=production                            │
│  3. COPY frontend/                                          │
│  4. RUN npm run build                                       │
│  5. OUTPUT: /frontend/dist/yadalist-ui.css                  │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ COPY --from=frontend
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                 Stage 2: Python Runtime                      │
│                 FROM python:3.11-slim                        │
├─────────────────────────────────────────────────────────────┤
│  1. COPY --from=frontend /frontend/dist → staticfiles/css/  │
│  2. COPY requirements.txt                                    │
│  3. RUN pip install                                          │
│  4. COPY application code                                    │
│  5. CMD django runserver                                     │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ Final image contains:
                              │ - Python app
                              │ - Built CSS
                              │ - No Node/npm
                              ▼
                    Optimized Production Image
```

## CI/CD Pipeline (Jenkinsfile)

```
┌─────────────┐
│  Checkout   │ git clone from Gitea
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│ Build Frontend  │ cd frontend && npm ci && npm run build
└──────┬──────────┘
       │
       ├─► npm run build-storybook → storybook-static/
       │
       ▼
┌───────────────────┐
│ Build Docker      │ docker build (uses multi-stage)
│ Image             │
└──────┬────────────┘
       │
       ▼
┌───────────────────┐
│ Test              │ docker run pytest
└──────┬────────────┘
       │
       ▼
┌───────────────────┐
│ Deploy            │
├───────────────────┤
│ 1. scp storybook  │ → /opt/schmango/storybook/
│ 2. docker save    │
│ 3. ssh deploy     │
│ 4. collectstatic  │
│ 5. docker up -d   │
└───────────────────┘
```

## File Flow

```
INPUT FILES                BUILD                 OUTPUT
────────────              ──────                ────────

tailwind.config.js ──┐
                     │
input.css ───────────┼──► PostCSS + Tailwind ──► dist/yadalist-ui.css
                     │
*.stories.js ────────┘                            │
                                                  │
                                                  ├──► Django staticfiles/
                                                  │
                                                  └──► Docker image
```

## Component Layer Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     UTILITY CLASSES                          │
│  Tailwind utilities: m-4, p-2, text-center, flex, etc.      │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │ Built on top of
                              │
┌─────────────────────────────┴───────────────────────────────┐
│                   COMPONENT CLASSES                          │
│  @layer components:                                          │
│    .btn, .form-input, .alert, .nav, .card                   │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │ Built on top of
                              │
┌─────────────────────────────┴───────────────────────────────┐
│                    DESIGN TOKENS                             │
│  CSS Variables & Tailwind config:                           │
│    --color-primary, nord0-15, spacing, shadows              │
└─────────────────────────────────────────────────────────────┘
```

## Monorepo Integration

```
schmango/                         ← Django project root
├── frontend/                     ← Design system (new)
│   ├── src/
│   │   └── input.css            ← Component styles
│   ├── stories/                 ← Storybook stories
│   ├── dist/                    ← Built CSS
│   ├── package.json             ← npm config
│   └── tailwind.config.js       ← Theme config
│
├── accounts/                     ← Django app
│   ├── templates/
│   │   └── accounts/
│   │       ├── base.html        ← Uses design system
│   │       ├── login.html       ← Uses design system
│   │       └── signup.html      ← Uses design system
│   └── static/                  ← App-specific assets
│
├── hello/                        ← Django app
│   └── templates/               ← Will use design system
│
├── [future apps]/               ← Will use design system
│
├── staticfiles/                 ← Collected static files
│   └── yadalist-ui.css         ← Copied from frontend/dist/
│
├── schmango/                    ← Django settings
│   └── settings.py
│       └── STATICFILES_DIRS = ["frontend/dist"]
│
├── docker-compose.yml           ← Dev environment
├── Dockerfile                   ← Production build
└── Jenkinsfile                  ← CI/CD pipeline
```

## Design System Benefits

### Single Source of Truth
```
Design Decision
      │
      ▼
tailwind.config.js (colors, spacing)
      │
      ▼
All components automatically consistent
      │
      ├──► Storybook stories
      ├──► accounts/ templates
      ├──► hello/ templates
      └──► [all future apps]
```

### Component Reuse
```
Define once:               Use everywhere:
───────────               ────────────────

@layer components {        accounts/login.html:
  .btn--primary {           <button class="btn btn--primary">
    @apply bg-primary       
    text-white;            hello/dashboard.html:
  }                         <button class="btn btn--primary">
}                          
                           [any future app]:
                            <button class="btn btn--primary">
```

## Scaling Strategy

As your monorepo grows:

```
Current:                    Future:
────────                   ─────────

frontend/                  frontend/
├── src/                   ├── src/
│   └── input.css          │   ├── base/        ← Base styles
└── stories/               │   │   └── tokens.css
                           │   ├── components/  ← Per-component CSS
                           │   │   ├── button.css
                           │   │   ├── form.css
                           │   │   └── card.css
                           │   └── utilities/   ← Custom utilities
                           │       └── spacing.css
                           ├── stories/
                           │   └── *.stories.js
                           └── components/      ← Web Components (later)
                               └── *.js

accounts/                  accounts/            ← Uses design system
hello/                     hello/               ← Uses design system
                           billing/             ← Uses design system
                           dashboard/           ← Uses design system
                           api/                 ← Uses design system
                           [new apps]/          ← Uses design system
```

This architecture ensures:
- ✅ All apps share the same design language
- ✅ Changes propagate automatically
- ✅ Components are documented in Storybook
- ✅ Fast development iteration
- ✅ Easy onboarding for new developers
