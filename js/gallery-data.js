/* ============================================================
   THE PROMPT KITCHEN — Gallery Data
   Add new entries here. Drop images/videos in /gallery/
   Each entry: id, type, title, src, thumbnail, model,
               prompt, negativePrompt, params, tags, note
   ============================================================ */

const GALLERY_DATA = [
  {
    id: "img-001",
    type: "image",
    title: "Misty Forest at Dawn",
    src: "gallery/img-001.jpg",
    thumbnail: "gallery/img-001.jpg",
    model: "Midjourney v6.1",
    prompt: "Ancient redwood forest at dawn, golden god rays breaking through morning mist, moss-covered bark, fern undergrowth, photorealistic, 8K, shot on Sony A7R V with 24-70mm f/2.8 lens",
    negativePrompt: "people, animals, buildings, text, watermark, oversaturated",
    params: "--ar 16:9 --style raw --v 6.1 --chaos 10",
    tags: ["photography", "nature"],
    note: "The --style raw flag removes Midjourney's default painterly treatment, making the lighting feel genuinely photographic. Adding the specific camera body and lens gives the model a concrete reference point for realistic optics."
  },
  {
    id: "img-002",
    type: "image",
    title: "Brutalist Reading Room",
    src: "gallery/img-002.jpg",
    thumbnail: "gallery/img-002.jpg",
    model: "DALL-E 3",
    prompt: "Interior of a brutalist library reading room, poured concrete walls, dramatic skylights casting geometric shadows, rows of wooden study desks, warm tungsten lamp pools, empty, late afternoon, architectural photography style, editorial lighting",
    negativePrompt: "",
    params: "1024x1024, vivid style",
    tags: ["architecture", "photography"],
    note: "DALL-E 3 is excellent at architectural interiors when you name a specific style movement (brutalist) and describe lighting precisely. 'Geometric shadows' from skylights was the detail that made this composition work."
  },
  {
    id: "img-003",
    type: "image",
    title: "Cyberpunk Street Market",
    src: "gallery/img-003.jpg",
    thumbnail: "gallery/img-003.jpg",
    model: "Midjourney v6.1",
    prompt: "Crowded night market in a rain-soaked cyberpunk city, neon reflections on wet cobblestones, vendors selling glowing food, paper lanterns mixed with holographic signs, warm vs cool color contrast, cinematic, Blade Runner aesthetic without logos, high detail",
    negativePrompt: "text, logos, blurry, deformed people",
    params: "--ar 2:3 --v 6.1 --chaos 20 --style raw",
    tags: ["concept-art", "illustration"],
    note: "Specifying 'without logos' and including it in the negative prompt keeps the image clean for commercial use. The warm/cool contrast instruction (warm stalls, cool neon) gave the image far more visual interest than a generic cyberpunk prompt."
  },
  {
    id: "img-004",
    type: "image",
    title: "Minimalist Product Shot — Ceramic Mug",
    src: "gallery/img-004.jpg",
    thumbnail: "gallery/img-004.jpg",
    model: "Adobe Firefly 3",
    prompt: "Handmade ceramic coffee mug, matte speckled glaze in warm terracotta and cream, sitting on a pale linen cloth, soft diffused window light from the left, shallow depth of field, product photography, white background, studio, commercial quality",
    negativePrompt: "shadows on background, text, logos, fake ceramics, shiny glaze",
    params: "Content Credentials: on, Structure Reference: none",
    tags: ["product"],
    note: "Adobe Firefly is the right tool for product shots you might want to use commercially — it's trained on licensed content. Specifying 'matte' in the glaze description was critical; without it the default was a shiny, generic mug."
  },
  {
    id: "img-005",
    type: "image",
    title: "Illustrated Recipe Card Style",
    src: "gallery/img-005.jpg",
    thumbnail: "gallery/img-005.jpg",
    model: "Midjourney v6.1",
    prompt: "Botanical illustration style recipe card, hand-drawn ink and watercolor, sourdough bread loaf surrounded by wheat stalks, rosemary sprigs, sea salt crystals, soft cream paper texture, warm earth tones, editorial cookbook illustration, vintage feel",
    negativePrompt: "photography, 3D, digital look, modern, harsh shadows",
    params: "--ar 3:4 --v 6.1 --chaos 5",
    tags: ["illustration"],
    note: "Low chaos (--chaos 5) keeps the illustration consistent for editorial use. Specifying both the medium ('ink and watercolor') and the paper texture grounds the style — 'botanical illustration' alone gives wildly varying results."
  },
  {
    id: "img-006",
    type: "image",
    title: "Cozy Home Office Concept",
    src: "gallery/img-006.jpg",
    thumbnail: "gallery/img-006.jpg",
    model: "Stable Diffusion XL + ComfyUI",
    prompt: "Cozy home office in a converted attic, exposed wooden beams, large dormer window with afternoon light, built-in bookshelves filled with books and plants, a vintage wooden desk with a modern monitor, warm reading lamp, plaid blanket on chair, hygge aesthetic",
    negativePrompt: "people, anime, cartoon, watermark, messy, cluttered, unrealistic proportions",
    params: "Steps: 35, CFG: 7, Sampler: DPM++ 2M Karras, Size: 1024x768, Seed: 42819",
    tags: ["architecture", "photography"],
    note: "The seed is noted here so this exact composition is reproducible. 'Hygge aesthetic' is a surprisingly precise style reference — the model understands the concept and applies it coherently across warmth, texture, and light quality."
  },
  {
    id: "img-007",
    type: "image",
    title: "Abstract Data Visualization Art",
    src: "gallery/img-007.jpg",
    thumbnail: "gallery/img-007.jpg",
    model: "Midjourney v6.1",
    prompt: "Abstract art inspired by data flow, flowing streams of light particles in deep navy and amber, connections branching like neural networks, glowing nodes, dark background, generative art aesthetic, 8K, painterly, digital fine art",
    negativePrompt: "text, labels, UI elements, people, faces",
    params: "--ar 16:9 --v 6.1 --chaos 35 --stylize 750",
    tags: ["concept-art", "illustration"],
    note: "Higher chaos (35) and higher stylize (750) push Midjourney toward more abstract, creative interpretations. This combination is ideal for art pieces where you want visual interest over strict prompt adherence — good for backgrounds and hero images."
  },
  {
    id: "img-008",
    type: "image",
    title: "Mountain Lodge at Twilight",
    src: "gallery/img-008.jpg",
    thumbnail: "gallery/img-008.jpg",
    model: "Ideogram v2",
    prompt: "Rustic mountain lodge exterior at twilight, warm amber light glowing through windows, snow on the pine trees, clear sky beginning to show stars, smoke from chimney, wide establishing shot, cinematic, national geographic style photography",
    negativePrompt: "people, text signs, cars, power lines",
    params: "Style: Realistic, Aspect ratio: 16:9",
    tags: ["photography", "nature"],
    note: "Ideogram v2 handles architectural exteriors with surrounding environment very well, especially for establishing shots. The 'twilight' time specification reliably produces the blue-hour color palette with interior warm light — one of the most effective lighting prompts across all models."
  }
];
