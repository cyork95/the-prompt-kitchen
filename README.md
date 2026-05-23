# The Prompt Kitchen

**Simple recipes for getting the most out of AI.**

A free, friendly, jargon-free guide to using AI tools in everyday life — for everyone from complete beginners to experienced practitioners. No ads, no tracking, no paywalls.

→ **Live site:** https://thepromkitchen.dev

---

## What's in here

| Page | Path | Description |
|------|------|-------------|
| Home | `/index.html` | Hero, quick-start cards, featured recipes |
| Recipe Book | `/prompts/` | Prompt pattern library with copy buttons |
| Kitchen Prep | `/context/` | Context engineering explained simply |
| Appliance Guide | `/models/` | Plain-English model comparison + decision tree |
| Daily Specials | `/daily/` | Ready-to-use playbooks for everyday tasks |
| Tasting Menu | `/examples/` | Real prompt → output examples |
| Image & Video | `/image-video/` | Complete guide to visual AI tools |
| Gallery | `/gallery/` | AI-generated images with full prompt transparency |
| Support | `/support.html` | Donation options (PayPal + crypto) |

---

## Deploying to GitHub Pages

No build step. No npm. No dependencies to install. Just:

**1. Create a GitHub repository**
```
Go to github.com → New repository
Name it anything (e.g. "the-prompt-kitchen" or "username.github.io")
Set it to Public
Don't initialize with README (you already have one)
```

**2. Push this folder to the repo**
```bash
# From inside this folder:
git init
git add .
git commit -m "Initial deploy"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

**3. Enable GitHub Pages**
```
Go to your repo on GitHub
Settings → Pages
Source: Deploy from a branch
Branch: main / (root)
Save
```

Your site will be live at `https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/` within a minute or two.

**4. (Optional) Custom domain**

Add a `CNAME` file to the repo root containing your domain name:
```
thepromkitchen.dev
```
Then point your domain's DNS to GitHub Pages. See [GitHub's docs](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site) for the exact DNS records needed.

---

## Before you launch — checklist

- [x] ~~Replace crypto addresses in `support.html`~~ — BTC, SOL, XRP + destination tag, PayPal all set
- [ ] Update `https://thepromkitchen.dev` throughout with your actual domain (or GitHub Pages URL)
- [ ] Update the GitHub link in the footer of each page to your actual repo URL
- [ ] Add real images to `/gallery/` and update `js/gallery-data.js` with actual file paths
- [ ] Update `sitemap.xml` dates if you've made changes since initial build

---

## File structure

```
/
├── index.html              ← Home page
├── support.html            ← Donation page
├── sitemap.xml
├── robots.txt
├── README.md
├── CONTRIBUTING.md
│
├── css/
│   └── style.css           ← Complete design system (edit here for visual changes)
│
├── js/
│   ├── main.js             ← All interactivity (dark mode, copy, nav, gallery, lightbox, QR)
│   └── gallery-data.js     ← Gallery content — add entries here to update the gallery
│
├── gallery/                ← Drop image/video files here
│   ├── img-001.jpg
│   └── ...
│
├── prompts/
│   └── index.html
├── context/
│   └── index.html
├── models/
│   └── index.html
├── daily/
│   └── index.html
├── examples/
│   └── index.html
├── image-video/
│   └── index.html
└── gallery/
    └── index.html
```

---

## Adding content

### Adding a new prompt recipe
Edit `prompts/index.html`. Copy an existing `<section class="recipe-card">` block and fill in:
- Title and tag
- When to use / best for
- The prompt (inside `<div class="prompt-block"><pre>`)
- Example (same structure)
- Beginner callout box

Copy buttons are added automatically by `js/main.js` for any `.prompt-block` element.

### Adding a gallery image
1. Drop the image file into `/gallery/` (e.g., `gallery/img-009.jpg`)
2. Open `js/gallery-data.js`
3. Add a new object to the `GALLERY_DATA` array following the existing schema:

```js
{
  id: "img-009",
  type: "image",
  title: "Your Image Title",
  src: "gallery/img-009.jpg",
  thumbnail: "gallery/img-009.jpg",
  model: "Midjourney v6.1",
  prompt: "Your full prompt here...",
  negativePrompt: "things, to, exclude",
  params: "--ar 16:9 --style raw",
  tags: ["photography", "nature"],  // used for filtering
  note: "One or two sentences about what made this work."
}
```

Available tags: `photography`, `illustration`, `concept-art`, `product`, `architecture`, `nature`

### Adding a daily playbook entry
Edit `daily/index.html`. Copy an existing `<div class="playbook-card">` block, give it a new `id`, and fill in the situation, recipes, and tips.

---

## Design system

All visual decisions live in `css/style.css` as CSS custom properties at the top of the file:

```css
:root {
  --accent: #B85C20;        /* change this to update the accent color everywhere */
  --font-display: 'DM Serif Display', ...;
  --font-body: 'Source Serif 4', ...;
  /* ... */
}
```

Dark mode is handled by `[data-theme="dark"]` overrides in the same file. Toggle state is persisted in `localStorage` via `js/main.js`.

---

## Tech stack

- Pure HTML5, CSS3 (custom properties), vanilla JavaScript (ES6+)
- Zero npm, zero build tools, zero frameworks
- One CDN dependency: [highlight.js](https://highlightjs.org/) for code syntax highlighting
- Google Fonts loaded via `@import` in `style.css`
- Fully static — works on any host, not just GitHub Pages

---

## License

Content: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — you're free to share and adapt with attribution.

Code: MIT — do whatever you like with it.
