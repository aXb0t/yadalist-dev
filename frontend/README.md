# Yadalist UI Design System

A Tailwind CSS-based design system with Nord theme for the Schmango monorepo.

## Quick Start

### Local Development (without Docker)

```bash
cd frontend
npm install
npm run dev  # Runs CSS watch + Storybook in parallel
```

This will:
- Build and watch CSS changes (outputs to `dist/yadalist-ui.css`)
- Start Storybook on http://localhost:6006

### Docker Development

```bash
# From project root
docker-compose up
```

This starts:
- `db` - PostgreSQL database
- `frontend` - Builds CSS and watches for changes
- `web` - Django app on http://localhost:8000
- `storybook` - Storybook on http://localhost:6006

## Available Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Build CSS + run Storybook (parallel) |
| `npm run build` | Build production CSS (minified) |
| `npm run watch:css` | Watch CSS files and rebuild on changes |
| `npm run storybook` | Start Storybook dev server |
| `npm run build-storybook` | Build static Storybook for deployment |

## Design System Structure

```
frontend/
├── src/
│   ├── input.css           # Main Tailwind entry point
│   ├── components/         # (Future) Component-specific CSS
│   └── stories/            # (Future) Utility classes
├── stories/                # Storybook stories
│   ├── Button.stories.js
│   ├── Form.stories.js
│   ├── Alert.stories.js
│   ├── Navigation.stories.js
│   ├── Card.stories.js
│   └── Layout.stories.js
├── dist/                   # Built CSS (git-ignored)
│   └── yadalist-ui.css
└── tailwind.config.js      # Tailwind + Nord theme config
```

## Nord Theme Colors

### Usage in Templates

```html
<!-- Semantic colors -->
<button class="bg-primary text-white">Primary Button</button>
<div class="bg-success text-white">Success Message</div>
<div class="bg-error text-white">Error Message</div>

<!-- Nord palette (direct access) -->
<div class="bg-nord0 text-nord6">Dark section</div>
<div class="bg-nord6 text-nord0">Light section</div>
```

### Color Reference

**Semantic Colors:**
- `primary` - #5E81AC (nord10)
- `primary-hover` - #81A1C1 (nord9)
- `secondary` - #88C0D0 (nord8)
- `success` - #A3BE8C (nord14)
- `warning` - #EBCB8B (nord13)
- `error` - #BF616A (nord11)
- `info` - #8FBCBB (nord7)

**UI Colors:**
- `background` - #ECEFF4 (nord6)
- `surface` - #E5E9F0 (nord5)
- `card` - #FFFFFF
- `text` - #2E3440 (nord0)
- `text-muted` - #4C566A (nord3)
- `border` - #D8DEE9 (nord4)

## Component Classes

All components use Tailwind's `@layer components` for consistency:

### Buttons

```html
<button class="btn btn--primary">Primary</button>
<button class="btn btn--secondary">Secondary</button>
<button class="btn btn--success">Success</button>
<button class="btn btn--danger">Danger</button>
```

### Forms

```html
<div class="form-group">
  <label class="form-label">Username</label>
  <input type="text" class="form-input" placeholder="Enter username">
  <span class="form-helptext">Help text here</span>
</div>

<!-- With errors -->
<div class="form-group">
  <label class="form-label">Email</label>
  <input type="email" class="form-input" value="invalid">
  <ul class="errorlist">
    <li>Enter a valid email address</li>
  </ul>
</div>
```

### Alerts

```html
<div class="alert alert--success">Success message</div>
<div class="alert alert--error">Error message</div>
<div class="alert alert--info">Info message</div>
<div class="alert alert--warning">Warning message</div>

<!-- Multiple alerts -->
<ul class="alert-list">
  <li class="alert alert--success">First message</li>
  <li class="alert alert--info">Second message</li>
</ul>
```

### Navigation

```html
<nav class="nav nav--dark">
  <a href="#" class="nav__link">Home</a>
  <a href="#" class="nav__link">Profile</a>
  <a href="#" class="nav__link">Logout</a>
</nav>
```

### Cards

```html
<div class="card">
  <h2 class="heading-2">Card Title</h2>
  <p>Card content...</p>
</div>

<!-- Container with card -->
<div class="container-card">
  <div class="card">
    Content here
  </div>
</div>
```

## Using in Django Templates

### 1. Load static files

```django
{% load static %}
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="{% static 'yadalist-ui.css' %}">
</head>
```

### 2. Use component classes

Replace inline styles with component classes:

**Before:**
```html
<button style="background-color: #007bff; color: white; padding: 10px 20px;">
  Submit
</button>
```

**After:**
```html
<button class="btn btn--primary">Submit</button>
```

### 3. Example: Login Form

```django
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Login</title>
  <link rel="stylesheet" href="{% static 'yadalist-ui.css' %}">
</head>
<body>
  <nav class="nav nav--dark">
    <a href="{% url 'home' %}" class="nav__link">Home</a>
    <a href="{% url 'login' %}" class="nav__link">Login</a>
    <a href="{% url 'signup' %}" class="nav__link">Sign Up</a>
  </nav>

  <div class="container-card">
    <div class="card" style="max-width: 400px; margin: 0 auto;">
      {% if messages %}
      <ul class="alert-list">
        {% for message in messages %}
        <li class="alert alert--{{ message.tags }}">{{ message }}</li>
        {% endfor %}
      </ul>
      {% endif %}

      <h2 class="heading-2">Login</h2>

      <form method="post">
        {% csrf_token %}

        <div class="form-group">
          <label class="form-label">Username</label>
          {{ form.username }}
          {% if form.username.errors %}
          <ul class="errorlist">
            {% for error in form.username.errors %}
            <li>{{ error }}</li>
            {% endfor %}
          </ul>
          {% endif %}
        </div>

        <div class="form-group">
          <label class="form-label">Password</label>
          {{ form.password }}
        </div>

        <button type="submit" class="btn btn--primary">Login</button>
      </form>

      <p style="margin-top: 1rem;">
        Don't have an account? <a href="{% url 'signup' %}" class="link">Sign up</a>
      </p>
    </div>
  </div>
</body>
</html>
```

## Production Build

The Docker multi-stage build automatically:
1. Installs npm dependencies
2. Builds minified CSS
3. Copies to Django staticfiles
4. Builds final Python image

```bash
docker build -t schmango:latest .
```

## CI/CD Integration

Jenkins pipeline automatically:
1. Builds frontend assets
2. Builds Storybook static site
3. Deploys Storybook to `/opt/schmango/storybook/`
4. Builds and deploys Docker image

## Storybook Access

- **Development:** http://localhost:6006
- **Production:** Configure nginx to serve `/opt/schmango/storybook/` at a subdomain

### Example Nginx Config for Storybook

```nginx
server {
    listen 80;
    server_name storybook.schmango.com;

    root /opt/schmango/storybook;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

## Extending the Design System

### Adding New Components

1. Add component CSS to `src/input.css`:

```css
@layer components {
  .badge {
    @apply inline-block px-2 py-1 text-xs rounded-full;
  }

  .badge--primary {
    @apply bg-primary text-white;
  }
}
```

2. Create Storybook story `stories/Badge.stories.js`:

```javascript
export default {
  title: 'Components/Badge',
  tags: ['autodocs'],
}

export const Primary = () => `
  <span class="badge badge--primary">New</span>
`
```

3. Use in Django templates:

```django
<span class="badge badge--primary">New</span>
```

## Customizing Theme

Edit `tailwind.config.js` to customize:

```javascript
theme: {
  extend: {
    colors: {
      // Add custom colors
      'custom-blue': '#1E40AF',
    },
    fontFamily: {
      // Change fonts
      sans: ['Your Font', 'sans-serif'],
    },
  },
}
```

## Tips

1. **Use Tailwind utilities** for one-off styling: `<div class="mt-4 text-center">`
2. **Use component classes** for repeated patterns: `<button class="btn btn--primary">`
3. **Reference Storybook** when building templates - all components are documented there
4. **Keep `input.css` organized** - use `@layer components` for reusable classes
5. **Check Tailwind docs** for available utilities: https://tailwindcss.com/docs
