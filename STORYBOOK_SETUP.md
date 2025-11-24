# Storybook Setup Complete! 🎨

Your Tailwind + Nord theme design system with Storybook is ready to go.

## What's Been Set Up

### ✅ Frontend Workspace
- **Location:** `/frontend/`
- **Framework:** Tailwind CSS with Nord theme
- **Build tool:** PostCSS + Tailwind CLI
- **Component workshop:** Storybook 8

### ✅ Design System
- **Theme:** Nord color palette with semantic color aliases
- **Components:** Button, Form, Alert, Navigation, Card, Layout
- **Stories:** 6 complete story files showcasing all UI patterns
- **Responsive:** Mobile-first design with Nord colors

### ✅ Docker Integration
- **Development:** Separate `frontend` and `storybook` services
- **Production:** Multi-stage Dockerfile builds CSS in image
- **Hot reload:** CSS watch mode in development

### ✅ CI/CD Pipeline
- **Jenkins:** Builds frontend, compiles CSS, generates Storybook
- **Deployment:** Copies Storybook static files to `/opt/schmango/storybook/`

### ✅ Django Integration
- **Settings:** `STATICFILES_DIRS` points to `frontend/dist/`
- **Template:** New `base_new.html` using design system classes
- **Static files:** Served from `/static/yadalist-ui.css`

## Next Steps to Get Running

### 1. Install Dependencies

```bash
cd /Users/alex/Dev/Schmango/schmango/frontend
npm install
```

### 2. Build CSS (First Time)

```bash
npm run build
```

This creates `frontend/dist/yadalist-ui.css` with all your styles.

### 3. Start Development Environment

**Option A: Everything with Docker**
```bash
cd /Users/alex/Dev/Schmango/schmango
docker-compose up
```

Access:
- Django: http://localhost:8000
- Storybook: http://localhost:6006

**Option B: Frontend only (faster iteration)**
```bash
cd frontend
npm run dev
```

This runs both:
- Tailwind CSS watch mode (rebuilds on changes)
- Storybook dev server on port 6006

### 4. Update Your Templates

Replace `base.html` with `base_new.html` when ready:

```bash
cd /Users/alex/Dev/Schmango/schmango/accounts/templates/accounts
mv base.html base_old.html
mv base_new.html base.html
```

Or gradually migrate by updating templates one by one to use the new classes.

## Quick Reference

### Development Workflow

1. **Design in Storybook:** Create/modify components in `frontend/stories/*.stories.js`
2. **Update CSS:** Edit `frontend/src/input.css` for component styles
3. **Use in Django:** Apply classes in templates like `<button class="btn btn--primary">`

### Key Files

| File | Purpose |
|------|---------|
| `frontend/package.json` | Dependencies and scripts |
| `frontend/tailwind.config.js` | Nord theme + Tailwind config |
| `frontend/src/input.css` | Component CSS classes |
| `frontend/stories/*.stories.js` | Storybook component stories |
| `frontend/.storybook/main.js` | Storybook configuration |
| `docker-compose.yml` | Development environment |
| `Dockerfile` | Production multi-stage build |
| `Jenkinsfile` | CI/CD pipeline |

## Component Usage Examples

### Buttons
```html
<button class="btn btn--primary">Save</button>
<button class="btn btn--secondary">Cancel</button>
<button class="btn btn--success">Confirm</button>
<button class="btn btn--danger">Delete</button>
```

### Forms
```html
<div class="form-group">
  <label class="form-label">Email</label>
  <input type="email" class="form-input" placeholder="you@example.com">
  <span class="form-helptext">We'll never share your email</span>
</div>
```

### Alerts (Django Messages)
```html
<ul class="alert-list">
  {% for message in messages %}
  <li class="alert alert--{{ message.tags }}">{{ message }}</li>
  {% endfor %}
</ul>
```

### Navigation
```html
<nav class="nav nav--dark">
  <a href="#" class="nav__link">Home</a>
  <a href="#" class="nav__link">Profile</a>
</nav>
```

## Nord Theme Colors

**Semantic (use these in templates):**
- `bg-primary` / `text-primary` - Blue accent (#5E81AC)
- `bg-success` / `text-success` - Green (#A3BE8C)
- `bg-error` / `text-error` - Red (#BF616A)
- `bg-warning` / `text-warning` - Yellow (#EBCB8B)
- `bg-info` / `text-info` - Cyan (#8FBCBB)

**UI Colors:**
- `bg-background` - Light gray (#ECEFF4)
- `bg-card` - White
- `text-text` - Dark gray (#2E3440)
- `border-border` - Light border (#D8DEE9)

**Direct Nord palette:**
- `nord0` through `nord15` - Full Nord color range

## Customizing

### Add New Component
1. Add CSS to `frontend/src/input.css` in `@layer components`
2. Create story in `frontend/stories/YourComponent.stories.js`
3. Rebuild: `npm run build`
4. Use in templates

### Change Colors
Edit `frontend/tailwind.config.js` > `theme.extend.colors`

### Add Fonts
1. Add Google Fonts link to templates
2. Update `tailwind.config.js` > `theme.extend.fontFamily`

## Storybook in Production

After Jenkins builds, Storybook will be available at `/opt/schmango/storybook/`.

**Add to nginx config:**
```nginx
location /storybook {
    alias /opt/schmango/storybook;
    index index.html;
    try_files $uri $uri/ /storybook/index.html;
}
```

Then access at: `https://your-domain.com/storybook`

## Troubleshooting

### CSS not updating?
```bash
# Clear and rebuild
rm -rf frontend/dist
cd frontend && npm run build
```

### Storybook not starting?
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run storybook
```

### Docker build fails?
```bash
# Build CSS locally first
cd frontend && npm run build
# Then build Docker
cd .. && docker-compose build
```

### Django can't find CSS?
```bash
# Check static files config
python manage.py findstatic yadalist-ui.css
# Collect static files
python manage.py collectstatic
```

## Resources

- **Tailwind CSS:** https://tailwindcss.com/docs
- **Nord Theme:** https://www.nordtheme.com/
- **Storybook:** https://storybook.js.org/docs
- **BEM Methodology:** http://getbem.com/

## Migration Checklist

- [ ] Install npm dependencies (`cd frontend && npm install`)
- [ ] Build CSS (`npm run build`)
- [ ] Start Storybook (`npm run storybook`)
- [ ] Review components at http://localhost:6006
- [ ] Test Docker setup (`docker-compose up`)
- [ ] Update one template to use new classes
- [ ] Verify styles work correctly
- [ ] Gradually migrate remaining templates
- [ ] Update nginx config for Storybook (production)
- [ ] Test CI/CD build in Jenkins

---

**You're all set!** The design system is ready for development. Start with `cd frontend && npm install && npm run dev` to see Storybook in action.
