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
    src: "/gallery/img-001.jpg",
    thumbnail: "/gallery/img-001.jpg",
    model: "Grok Aurora",
    prompt: "Ancient redwood forest at dawn, golden light rays breaking through morning mist, moss-covered bark, fern undergrowth, photorealistic, shot on Sony A7R V with 24-70mm f/2.8 lens, 8K detail",
    negativePrompt: "",
    params: "Default settings — Aurora generates one image per prompt, no parameters needed",
    tags: ["photography", "nature"],
    note: "Grok's Aurora image model is free at grok.com with a free X account — no credits, no waitlist. Naming a specific camera body and lens gives it a precise reference for optics and depth of field. The 'golden light rays through mist' detail reliably produces strong atmospheric lighting."
  },
  {
    id: "img-002",
    type: "image",
    title: "Brutalist Reading Room",
    src: "/gallery/img-002.jpg",
    thumbnail: "/gallery/img-002.jpg",
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
    src: "/gallery/img-003.jpg",
    thumbnail: "/gallery/img-003.jpg",
    model: "Google Gemini Imagen",
    prompt: "Crowded night market in a rain-soaked cyberpunk city, neon reflections on wet cobblestones, vendors selling glowing food, paper lanterns mixed with holographic signs, warm vs cool color contrast, cinematic, no logos or text, high detail",
    negativePrompt: "",
    params: "Generated in Gemini chat — type the prompt directly, Gemini produces images inline",
    tags: ["concept-art", "illustration"],
    note: "Google Gemini's free tier includes Imagen-powered image generation — just type an image prompt in the chat at gemini.google.com. No separate tool needed. The warm/cool color contrast instruction (warm vendor stalls, cool neon) is one of the most effective cinematic prompts across all models."
  },
  {
    id: "img-004",
    type: "image",
    title: "Minimalist Product Shot — Ceramic Mug",
    src: "/gallery/img-004.jpg",
    thumbnail: "/gallery/img-004.jpg",
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
    src: "/gallery/img-005.jpg",
    thumbnail: "/gallery/img-005.jpg",
    model: "Leonardo AI",
    prompt: "Botanical illustration style, hand-drawn ink and watercolor, sourdough bread loaf surrounded by wheat stalks, rosemary sprigs, sea salt crystals, soft cream paper texture, warm earth tones, editorial cookbook illustration, vintage feel",
    negativePrompt: "photography, 3D render, digital look, modern, harsh shadows, people",
    params: "Model: Leonardo Diffusion XL · Preset: Illustration · Dimensions: 3:4",
    tags: ["illustration"],
    note: "Leonardo AI's free tier gives ~150 tokens/day — enough for several images. The Illustration preset at leonardo.ai naturally leans toward painterly results; combining it with 'hand-drawn ink and watercolor' and 'cream paper texture' grounds the style precisely. Without those medium descriptors, 'botanical illustration' alone gives inconsistent results."
  },
  {
    id: "img-006",
    type: "image",
    title: "Cozy Home Office Concept",
    src: "/gallery/img-006.jpg",
    thumbnail: "/gallery/img-006.jpg",
    model: "Adobe Firefly (free tier — firefly.adobe.com)",
    prompt: "Cozy home office in a converted attic, exposed wooden beams, large dormer window with afternoon light, built-in bookshelves filled with books and plants, a vintage wooden desk with a modern monitor, warm reading lamp, plaid blanket on chair, hygge aesthetic",
    negativePrompt: "people, anime, cartoon, watermark, messy, cluttered, unrealistic proportions",
    params: "Content Credentials: on · Aspect ratio: 4:3 · Style: Photo",
    tags: ["architecture", "photography"],
    note: "Adobe Firefly's free tier (firefly.adobe.com) includes lifestyle and interior scenes alongside product shots. The 'hygge aesthetic' reference is surprisingly precise — it communicates warmth, texture, soft lighting, and comfort as a single concept. Firefly's commercially-safe training makes it a solid choice for interior design mockups and lifestyle branding."
  },
  {
    id: "img-007",
    type: "image",
    title: "Abstract Data Visualization Art",
    src: "/gallery/img-007.jpg",
    thumbnail: "/gallery/img-007.jpg",
    model: "Canva AI Image Generator",
    prompt: "Abstract art inspired by data flow, flowing streams of light particles in deep navy and amber, connections branching like neural networks, glowing nodes, dark background, generative art aesthetic, painterly, digital fine art",
    negativePrompt: "",
    params: "Style: None (let the model interpret freely) · Aspect ratio: 16:9",
    tags: ["concept-art", "illustration"],
    note: "Canva's free plan includes AI image generation — no credits needed for the basic generator. For abstract work, leaving the Style selector on 'None' and letting the prompt drive the visual gives more interesting results than using a preset. Deep navy + amber is a high-contrast palette that reads well at small sizes and as a background."
  },
  {
    id: "img-008",
    type: "image",
    title: "Mountain Lodge at Twilight",
    src: "/gallery/img-008.jpg",
    thumbnail: "/gallery/img-008.jpg",
    model: "Ideogram v2",
    prompt: "Rustic mountain lodge exterior at twilight, warm amber light glowing through windows, snow on the pine trees, clear sky beginning to show stars, smoke from chimney, wide establishing shot, cinematic, national geographic style photography",
    negativePrompt: "people, text signs, cars, power lines",
    params: "Style: Realistic, Aspect ratio: 16:9",
    tags: ["photography", "nature"],
    note: "Ideogram v2 handles architectural exteriors with surrounding environment very well, especially for establishing shots. The 'twilight' time specification reliably produces the blue-hour color palette with interior warm light — one of the most effective lighting prompts across all models."
  }
];
