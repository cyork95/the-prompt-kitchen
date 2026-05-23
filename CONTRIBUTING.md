# Contributing to The Prompt Kitchen

Thanks for wanting to help. This site is a community effort — the more prompts, examples, and corrections people contribute, the more useful it becomes for everyone.

No coding experience is required to contribute content changes. If you can edit a text file, you can contribute.

---

## Ways to contribute

| Type | What it involves | Coding needed? |
|------|-----------------|----------------|
| Fix a typo or error | Edit an HTML file | No |
| Add a prompt recipe | Add a section to `prompts/index.html` | No |
| Add a daily playbook entry | Add a section to `daily/index.html` | No |
| Add a tasting menu example | Add a card to `examples/index.html` | No |
| Add a gallery image | Add a file + one entry in `gallery-data.js` | Minimal |
| Report a bug or broken link | Open a GitHub Issue | No |
| Improve the design or JS | Edit `css/style.css` or `js/main.js` | Yes |

---

## How to submit a change

### Option A — GitHub Pull Request (preferred for content changes)

1. **Fork the repository** — click "Fork" in the top right on GitHub
2. **Make your changes** to the relevant file(s) — you can edit directly in GitHub's web editor
3. **Commit your changes** with a clear message: `Add prompt pattern: Socratic questioning` or `Fix typo in context page`
4. **Open a Pull Request** — describe what you changed and why
5. We'll review and merge it (usually within a few days)

### Option B — GitHub Issue (for reporting problems)

If you spotted something wrong but don't want to fix it yourself:
1. Go to the repository's **Issues** tab
2. Click **New Issue**
3. Describe what's wrong and where (include the page URL)

---

## Content guidelines

### Prompt recipes (for `prompts/index.html`)

A good recipe submission includes:

- **Title** — clear and descriptive (`Socratic questioning`, not `my cool prompt`)
- **Tag** — one of: `Learning`, `Writing`, `Planning`, `Research`, `Communication`, `Problem Solving`, `Role-Play`, `How-To`, `Critical Thinking`
- **When to use / Best for** — one line each
- **Brief intro** — 2–3 sentences explaining the pattern and why it works
- **The Recipe** — the actual prompt template in a `<div class="prompt-block"><pre>` block, using `[brackets]` for user-fillable parts
- **An Example** — a filled-in, specific version of the recipe
- **Beginner callout** — the `<div class="callout callout-beginner">` block telling a first-time user exactly what to do

**Voice:** Warm, practical, no jargon without explanation. Write as if explaining to a smart friend who has never used AI before.

**Don't submit:**
- Prompts that require a paid model to work
- Jailbreaks, prompt injections, or anything designed to circumvent safety measures
- Prompts that could be used to deceive or harm others
- Vague prompts without a clear use case

### Gallery images (for `/gallery/` + `js/gallery-data.js`)

Gallery submissions should:

- Be genuinely interesting and educational — show something that teaches a lesson about prompting
- Include the **full, exact prompt** — no paraphrasing
- Include the **model and version** used
- Include a **note** explaining what specifically made it work (1–2 sentences)
- Be reasonably high quality — blurry or broken outputs belong in a "what went wrong" section, not the gallery
- Not include human faces unless clearly labeled as AI-generated and the subject has no identifiable private information
- Be appropriate for a general audience

**Image format:** JPG or PNG, under 2MB. Aim for 1200–2400px on the long edge.

**File naming:** `img-XXX.jpg` where XXX is the next sequential number in the data file.

**The data entry schema:**
```js
{
  id: "img-009",           // next available ID
  type: "image",           // or "video"
  title: "Short title",    // shown in lightbox
  src: "gallery/img-009.jpg",
  thumbnail: "gallery/img-009.jpg",
  model: "Midjourney v6.1",
  prompt: "Full prompt text exactly as used...",
  negativePrompt: "comma, separated, exclusions",  // or "" if none
  params: "--ar 16:9 --style raw",                 // or "" if none
  tags: ["photography", "nature"],                 // see available tags below
  note: "What specifically made this work."
}
```

**Available tags:** `photography`, `illustration`, `concept-art`, `product`, `architecture`, `nature`

---

## Code contributions

If you're changing `css/style.css` or `js/main.js`:

- Keep the existing code style (2-space indentation, single quotes in JS, comments only where non-obvious)
- Test in both light and dark mode
- Test on mobile (use browser dev tools at 375px width minimum)
- Make sure copy buttons still work on any new `.prompt-block` elements you add
- Don't add npm packages or build steps — the site must remain zero-dependency deployable

---

## Corrections and fact-checks

AI models change fast. If you notice:
- A model comparison that's out of date
- A price or tier description that has changed
- A feature listed as available that no longer exists (or vice versa)
- Any factual inaccuracy

Please open an Issue or submit a PR with a correction. Include a source link if possible.

---

## Code of conduct

This is a friendly, helpful space. Contributors are expected to:

- Be respectful in PR comments and issues
- Assume good intent
- Give constructive feedback, not just criticism
- Not submit content designed to harm, deceive, or exclude

---

## Questions?

Open a GitHub Issue with the label `question`. We'll do our best to respond promptly.

Thank you for contributing to The Prompt Kitchen. 🍳
