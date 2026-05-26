/* ============================================================
   THE PROMPT KITCHEN — Main JavaScript
   Handles: dark mode, copy buttons, mobile nav, smooth scroll,
            gallery filtering, lightbox, QR code generation
   ============================================================ */

'use strict';

// ============================================================
// 1. DARK MODE
// ============================================================
(function initTheme() {
  const saved = localStorage.getItem('pk-theme');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const theme = saved || (prefersDark ? 'dark' : 'light');
  document.documentElement.setAttribute('data-theme', theme);
})();

function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme');
  const next = current === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', next);
  localStorage.setItem('pk-theme', next);
}

// ============================================================
// 2. DOM READY
// ============================================================
document.addEventListener('DOMContentLoaded', function () {
  initThemeButton();
  initMobileNav();
  initNavMore();
  initCopyButtons();
  initBackToTop();
  initSmoothScroll();
  initGallery();
  initLightbox();
  setActiveNavLink();
});

// ============================================================
// 3. THEME BUTTON
// ============================================================
function initThemeButton() {
  const btn = document.getElementById('btn-theme');
  if (!btn) return;
  btn.addEventListener('click', toggleTheme);
}

// ============================================================
// 4. MOBILE NAV
// ============================================================
function initMobileNav() {
  const btn  = document.getElementById('btn-hamburger');
  const menu = document.getElementById('nav-mobile');
  if (!btn || !menu) return;

  btn.addEventListener('click', function () {
    const open = menu.classList.toggle('open');
    btn.setAttribute('aria-expanded', String(open));
  });

  // Close on outside click
  document.addEventListener('click', function (e) {
    if (!menu.contains(e.target) && !btn.contains(e.target)) {
      menu.classList.remove('open');
      btn.setAttribute('aria-expanded', 'false');
    }
  });

  // Close on nav link click
  menu.querySelectorAll('a').forEach(function (a) {
    a.addEventListener('click', function () {
      menu.classList.remove('open');
      btn.setAttribute('aria-expanded', 'false');
    });
  });
}

// ============================================================
// 5. "MORE" DROPDOWN NAV
// ============================================================
function initNavMore() {
  const navMore = document.querySelector('.nav-more');
  if (!navMore) return;
  const btn      = navMore.querySelector('.nav-more-btn');
  const dropdown = navMore.querySelector('.nav-dropdown');
  if (!btn || !dropdown) return;

  function open()  { navMore.classList.add('open');    btn.setAttribute('aria-expanded', 'true');  }
  function close() { navMore.classList.remove('open'); btn.setAttribute('aria-expanded', 'false'); }
  function toggle(){ navMore.classList.contains('open') ? close() : open(); }

  btn.addEventListener('click', function (e) { e.stopPropagation(); toggle(); });

  // Close when clicking outside
  document.addEventListener('click', function (e) {
    if (!navMore.contains(e.target)) close();
  });

  // Close on Escape
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') close();
  });

  // Close when a dropdown link is clicked
  dropdown.querySelectorAll('a').forEach(function (a) {
    a.addEventListener('click', close);
  });
}

// ============================================================
// 6. COPY BUTTONS
// ============================================================
function initCopyButtons() {
  // Auto-create copy buttons for .prompt-block elements
  document.querySelectorAll('.prompt-block').forEach(function (block) {
    if (block.querySelector('.copy-btn')) return; // already has one
    const pre = block.querySelector('pre');
    if (!pre) return;

    const btn = makeCopyBtn(function () {
      return pre.textContent;
    });
    block.appendChild(btn);
  });

  // Handle manually-placed copy buttons (data-copy-target or data-copy)
  document.querySelectorAll('[data-copy]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      const text = btn.getAttribute('data-copy');
      copyText(text, btn);
    });
  });

  document.querySelectorAll('[data-copy-target]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      const target = document.getElementById(btn.getAttribute('data-copy-target'));
      if (!target) return;
      copyText(target.textContent, btn);
    });
  });
}

function makeCopyBtn(getTextFn) {
  const btn = document.createElement('button');
  btn.className = 'copy-btn';
  btn.setAttribute('aria-label', 'Copy to clipboard');
  btn.innerHTML = '<span class="copy-icon">⎘</span> Copy';
  btn.addEventListener('click', function () {
    copyText(getTextFn(), btn);
  });
  return btn;
}

function copyText(text, btn) {
  if (!text) return;
  navigator.clipboard.writeText(text.trim()).then(function () {
    const original = btn.innerHTML;
    btn.innerHTML = '✓ Copied!';
    btn.classList.add('copied');
    setTimeout(function () {
      btn.innerHTML = original;
      btn.classList.remove('copied');
    }, 2000);
  }).catch(function () {
    // Fallback for older browsers
    const ta = document.createElement('textarea');
    ta.value = text.trim();
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    document.execCommand('copy');
    document.body.removeChild(ta);
    const original = btn.innerHTML;
    btn.innerHTML = '✓ Copied!';
    btn.classList.add('copied');
    setTimeout(function () {
      btn.innerHTML = original;
      btn.classList.remove('copied');
    }, 2000);
  });
}

// ============================================================
// 6. BACK TO TOP
// ============================================================
function initBackToTop() {
  const btn = document.getElementById('back-to-top');
  if (!btn) return;

  window.addEventListener('scroll', function () {
    btn.classList.toggle('visible', window.scrollY > 400);
  }, { passive: true });

  btn.addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
}

// ============================================================
// 7. SMOOTH SCROLL for anchor links
// ============================================================
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      const id = a.getAttribute('href').slice(1);
      const target = document.getElementById(id);
      if (!target) return;
      e.preventDefault();
      const offset = parseInt(getComputedStyle(document.documentElement).getPropertyValue('--nav-h') || '64', 10) + 16;
      const top = target.getBoundingClientRect().top + window.scrollY - offset;
      window.scrollTo({ top, behavior: 'smooth' });
      history.pushState(null, '', '#' + id);
    });
  });
}

// ============================================================
// 8. ACTIVE NAV LINK
// ============================================================
function setActiveNavLink() {
  const path = window.location.pathname.replace(/\/$/, '') || '/';
  document.querySelectorAll('.nav-links a, .nav-dropdown a, .nav-mobile-links a').forEach(function (a) {
    const href = a.getAttribute('href');
    if (!href) return;
    try {
      const url = new URL(href, window.location.href);
      const linkPath = url.pathname.replace(/\/$/, '') || '/';
      const isActive = (linkPath !== '/' && path.startsWith(linkPath)) || linkPath === path;
      if (isActive) {
        a.classList.add('active');
        // If this link is inside the More dropdown, also highlight the More button
        if (a.closest('.nav-dropdown')) {
          const navMore = a.closest('.nav-more');
          if (navMore) navMore.querySelector('.nav-more-btn').classList.add('active');
        }
      }
    } catch (_) {}
  });
}

// ============================================================
// 9. GALLERY FILTERING
// ============================================================

// Model URL map — links model names to their tools in cards and lightbox
const GALLERY_MODEL_URLS = {
  'Grok Aurora': 'https://grok.com',
  'DALL-E 3': 'https://chat.openai.com',
  'Google Gemini Imagen': 'https://gemini.google.com',
  'Adobe Firefly 3': 'https://firefly.adobe.com',
  'Adobe Firefly': 'https://firefly.adobe.com',
  'Leonardo AI': 'https://leonardo.ai',
  'Canva AI Image Generator': 'https://canva.com',
  'Ideogram v2': 'https://ideogram.ai',
  'Ideogram': 'https://ideogram.ai',
  'Midjourney': 'https://midjourney.com',
  'Stable Diffusion': 'https://stability.ai',
  'Stable Diffusion XL': 'https://stability.ai',
  'Kling AI': 'https://klingai.com',
  'Runway': 'https://runwayml.com',
  'Pika Labs': 'https://pika.art',
  'Luma Dream Machine': 'https://lumalabs.ai',
  'Hailuo AI': 'https://hailuoai.video',
  'Sora': 'https://sora.com',
};

function galleryModelLink(name) {
  if (!name) return '';
  const url = GALLERY_MODEL_URLS[name];
  if (url) return `<a href="${url}" target="_blank" rel="noopener" class="gallery-model-link">${escHtml(name)}</a>`;
  return escHtml(name);
}

function initGallery() {
  const container = document.getElementById('gallery-grid');
  if (!container) return;

  // Load gallery data
  if (typeof GALLERY_DATA === 'undefined') return;
  renderGallery(GALLERY_DATA);

  // Filter buttons
  document.querySelectorAll('.filter-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const filter = btn.getAttribute('data-filter');
      filterGallery(filter);
    });
  });
}

function renderGallery(items) {
  const container = document.getElementById('gallery-grid');
  if (!container) return;
  container.innerHTML = '';

  items.forEach(function (item, index) {
    const el = createGalleryCard(item, index);
    container.appendChild(el);
  });
}

function createGalleryCard(item, index) {
  const div = document.createElement('div');
  div.className = 'gallery-item';
  div.setAttribute('data-id', item.id);
  div.setAttribute('data-tags', (item.tags || []).join(' '));
  div.setAttribute('data-type', item.type || 'image');
  div.style.animationDelay = (index * 0.05) + 's';

  if (item.type === 'video') {
    const video = document.createElement('video');
    video.src = item.thumbnail || item.src;
    video.muted = true;
    video.loop = true;
    video.playsInline = true;
    video.addEventListener('mouseenter', () => video.play());
    video.addEventListener('mouseleave', () => { video.pause(); video.currentTime = 0; });
    div.appendChild(video);

    const play = document.createElement('div');
    play.className = 'play-icon';
    play.textContent = '▶';
    div.appendChild(play);
  } else {
    const img = document.createElement('img');
    img.src = item.thumbnail || item.src;
    img.alt = item.title || 'Gallery image';
    img.loading = 'lazy';
    div.appendChild(img);
  }

  const overlay = document.createElement('div');
  overlay.className = 'gallery-item-overlay';

  const meta = document.createElement('div');
  meta.className = 'gallery-item-meta';
  meta.innerHTML = `<div class="gallery-item-model">${galleryModelLink(item.model)}</div><div>${escHtml(item.title || '')}</div>`;
  overlay.appendChild(meta);
  div.appendChild(overlay);

  div.addEventListener('click', function () {
    openLightbox(item);
  });

  return div;
}

function filterGallery(filter) {
  document.querySelectorAll('.gallery-item').forEach(function (item) {
    if (filter === 'all') {
      item.classList.remove('hidden');
      return;
    }
    const tags = item.getAttribute('data-tags') || '';
    const type = item.getAttribute('data-type') || '';
    const match = tags.includes(filter) || type === filter;
    item.classList.toggle('hidden', !match);
  });
}

// ============================================================
// 10. LIGHTBOX
// ============================================================
let _lightboxItem = null;

function initLightbox() {
  const lb = document.getElementById('lightbox');
  if (!lb) return;

  // Close on background click
  lb.addEventListener('click', function (e) {
    if (e.target === lb) closeLightbox();
  });

  // Close button
  const closeBtn = lb.querySelector('.lightbox-close');
  if (closeBtn) closeBtn.addEventListener('click', closeLightbox);

  // Keyboard
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeLightbox();
  });
}

function openLightbox(item) {
  const lb = document.getElementById('lightbox');
  if (!lb) return;
  _lightboxItem = item;

  const mediaEl = lb.querySelector('.lightbox-media');
  const infoEl  = lb.querySelector('.lightbox-info');

  // Clear previous
  mediaEl.innerHTML = '';
  infoEl.innerHTML  = '';

  // Media
  if (item.type === 'video' && item.video) {
    const video = document.createElement('video');
    video.src = item.video;
    video.controls = true;
    video.autoplay = true;
    mediaEl.appendChild(video);
  } else {
    const img = document.createElement('img');
    img.src = item.src;
    img.alt = item.title || '';
    mediaEl.appendChild(img);
  }

  // Info
  infoEl.innerHTML = `
    <h3>${escHtml(item.title || 'Untitled')}</h3>
    <span class="lightbox-model-badge">${galleryModelLink(item.model)}</span>
    <div class="lightbox-prompt-label">Prompt</div>
    <div class="prompt-block" style="margin:0 0 var(--s4)">
      <pre id="lb-prompt">${escHtml(item.prompt || '')}</pre>
    </div>
    ${item.negativePrompt ? `
    <div class="lightbox-prompt-label">Negative Prompt</div>
    <div class="lightbox-params" id="lb-neg">${escHtml(item.negativePrompt)}</div>
    ` : ''}
    ${item.params ? `
    <div class="lightbox-prompt-label">Parameters</div>
    <div class="lightbox-params" id="lb-params">${escHtml(item.params)}</div>
    ` : ''}
    ${item.note ? `<div class="lightbox-note">${escHtml(item.note)}</div>` : ''}
  `;

  // Re-init copy buttons for newly injected prompt block
  infoEl.querySelectorAll('.prompt-block').forEach(function (block) {
    const pre = block.querySelector('pre');
    if (!pre) return;
    const btn = makeCopyBtn(() => pre.textContent);
    block.appendChild(btn);
  });

  lb.classList.add('open');
  document.body.style.overflow = 'hidden';
}

function closeLightbox() {
  const lb = document.getElementById('lightbox');
  if (!lb) return;
  lb.classList.remove('open');
  document.body.style.overflow = '';
  // Stop any playing video
  const video = lb.querySelector('video');
  if (video) { video.pause(); video.src = ''; }
  _lightboxItem = null;
}

// ============================================================
// 11. QR CODE GENERATOR (Pure Canvas — No External Libraries)
// ============================================================
// Supports: byte mode, error correction level L, versions 1-10
// Based on ISO/IEC 18004:2015 QR Code standard

const QR = (function () {

  // --- GF(256) Arithmetic ---
  const EXP = new Uint8Array(512);
  const LOG  = new Uint8Array(256);

  (function buildGF() {
    let x = 1;
    for (let i = 0; i < 255; i++) {
      EXP[i] = x;
      LOG[x]  = i;
      x <<= 1;
      if (x & 0x100) x ^= 0x11D; // primitive polynomial
    }
    for (let i = 255; i < 512; i++) EXP[i] = EXP[i - 255];
  })();

  function gfMul(a, b) {
    return (a && b) ? EXP[(LOG[a] + LOG[b]) % 255] : 0;
  }

  function gfPolyMul(p, q) {
    const r = new Uint8Array(p.length + q.length - 1);
    for (let i = 0; i < p.length; i++)
      for (let j = 0; j < q.length; j++)
        r[i + j] ^= gfMul(p[i], q[j]);
    return r;
  }

  function rsGeneratorPoly(degree) {
    let poly = new Uint8Array([1]);
    for (let i = 0; i < degree; i++)
      poly = gfPolyMul(poly, new Uint8Array([1, EXP[i]]));
    return poly;
  }

  function rsEncode(data, ecLen) {
    const gen = rsGeneratorPoly(ecLen);
    const msg = new Uint8Array(data.length + ecLen);
    msg.set(data);
    for (let i = 0; i < data.length; i++) {
      const coef = msg[i];
      if (coef) for (let j = 1; j < gen.length; j++)
        msg[i + j] ^= gfMul(gen[j], coef);
    }
    return msg.slice(data.length);
  }

  // --- Version/capacity tables (Byte mode, EC Level L) ---
  // [dataCapacity, ecPerBlock, totalBlocks]
  const VER = [
    null,
    [19,  7, 1],  // v1  — 21x21
    [34, 10, 1],  // v2  — 25x25
    [55, 15, 1],  // v3  — 29x29
    [80, 20, 1],  // v4  — 33x33
    [108,26, 1],  // v5  — 37x37
    [136,18, 2],  // v6  — 41x41
    [156,20, 2],  // v7  — 45x45
    [194,24, 2],  // v8  — 49x49
    [232,30, 2],  // v9  — 53x53
    [274,18, 4],  // v10 — 57x57
  ];

  // Alignment pattern centers (version 2-10)
  const ALIGN = [
    null, null,
    [18],       // v2
    [22],       // v3
    [26],       // v4
    [30],       // v5
    [34],       // v6
    [6,22,38],  // v7
    [6,24,42],  // v8
    [6,26,46],  // v9
    [6,28,50],  // v10
  ];

  function getVersion(dataLen) {
    // overhead = mode indicator (4 bits) + char count (8 bits for byte mode v1-9) + terminator
    // ≈ 4 bytes overhead (conservative)
    for (let v = 1; v <= 10; v++) {
      if (VER[v][0] >= dataLen + 3) return v;
    }
    return -1;
  }

  function encodeData(str, version) {
    const bytes = [];
    for (let i = 0; i < str.length; i++) {
      bytes.push(str.charCodeAt(i) & 0xFF);
    }

    // Build bit stream
    const bits = [];
    function pushBits(val, len) {
      for (let i = len - 1; i >= 0; i--)
        bits.push((val >> i) & 1);
    }

    pushBits(0b0100, 4);               // mode: byte
    pushBits(bytes.length, 8);          // char count (8 bits for v1-9)
    bytes.forEach(b => pushBits(b, 8)); // data

    // Terminator
    for (let i = 0; i < 4 && bits.length < VER[version][0] * 8; i++)
      bits.push(0);

    // Pad to byte boundary
    while (bits.length % 8) bits.push(0);

    // Padding codewords
    const padBytes = [0xEC, 0x11];
    let pi = 0;
    while (bits.length < VER[version][0] * 8)
      pushBits(padBytes[pi++ % 2], 8);

    // Convert bits to bytes
    const codewords = [];
    for (let i = 0; i < bits.length; i += 8) {
      let b = 0;
      for (let j = 0; j < 8; j++) b = (b << 1) | (bits[i + j] || 0);
      codewords.push(b);
    }
    return codewords;
  }

  function buildCodewords(dataBytes, version) {
    const [, ecPerBlock, totalBlocks] = VER[version];
    const totalData = VER[version][0];
    const blockSize = Math.floor(totalData / totalBlocks);
    const extraBlocks = totalData % totalBlocks;

    const dataBlocks = [];
    const ecBlocks   = [];
    let pos = 0;

    for (let b = 0; b < totalBlocks; b++) {
      const size = blockSize + (b < extraBlocks ? 1 : 0);
      const slice = dataBytes.slice(pos, pos + size);
      pos += size;
      dataBlocks.push(slice);
      ecBlocks.push(Array.from(rsEncode(new Uint8Array(slice), ecPerBlock)));
    }

    const result = [];
    // Interleave data
    const maxD = Math.max(...dataBlocks.map(b => b.length));
    for (let i = 0; i < maxD; i++)
      dataBlocks.forEach(b => { if (i < b.length) result.push(b[i]); });
    // Interleave EC
    for (let i = 0; i < ecPerBlock; i++)
      ecBlocks.forEach(b => { if (i < b.length) result.push(b[i]); });

    return result;
  }

  // Convert codewords to bit array
  function codewordsToBits(cw) {
    const bits = [];
    cw.forEach(b => {
      for (let i = 7; i >= 0; i--) bits.push((b >> i) & 1);
    });
    return bits;
  }

  // --- Matrix Building ---
  function makeMatrix(size) {
    return Array.from({ length: size }, () => new Int8Array(size).fill(-1));
    // -1 = empty, 0 = light, 1 = dark, +128 flag = function module
  }

  const FUNC = 128;

  function setModule(m, r, c, dark) {
    if (r >= 0 && r < m.length && c >= 0 && c < m.length)
      m[r][c] = dark | FUNC;
  }

  function isFunc(m, r, c) {
    return (m[r][c] & FUNC) !== 0;
  }

  function placeFinderPattern(m, row, col) {
    for (let r = -1; r <= 7; r++) {
      for (let c = -1; c <= 7; c++) {
        const dark = r === -1 || r === 7 || c === -1 || c === 7 ||
                     (r >= 2 && r <= 4 && c >= 2 && c <= 4);
        setModule(m, row + r, col + c, dark ? 1 : 0);
      }
    }
  }

  function placeFinders(m, N) {
    placeFinderPattern(m, 0, 0);         // top-left
    placeFinderPattern(m, 0, N - 7);     // top-right
    placeFinderPattern(m, N - 7, 0);     // bottom-left
  }

  function placeTiming(m, N) {
    for (let i = 8; i < N - 8; i++) {
      setModule(m, 6, i, i % 2 === 0 ? 1 : 0);
      setModule(m, i, 6, i % 2 === 0 ? 1 : 0);
    }
  }

  function placeAlignment(m, version) {
    const centers = ALIGN[version];
    if (!centers) return;

    const positions = [];
    for (let r of centers)
      for (let c of centers)
        positions.push([r, c]);

    positions.forEach(([r, c]) => {
      // Skip if overlaps finder
      if (m[r][c] !== -1 && isFunc(m, r, c)) return;
      for (let dr = -2; dr <= 2; dr++) {
        for (let dc = -2; dc <= 2; dc++) {
          const dark = dr === -2 || dr === 2 || dc === -2 || dc === 2 || (dr === 0 && dc === 0);
          setModule(m, r + dr, c + dc, dark ? 1 : 0);
        }
      }
    });
  }

  function placeDarkModule(m, version) {
    setModule(m, 4 * version + 9, 8, 1);
  }

  // Format information string (EC Level L = 01, mask pattern)
  // Format info: 5 data bits + 10 BCH bits, XOR with 101010000010010
  const FORMAT_MASK = 0b101010000010010;

  function formatBits(maskPattern) {
    // EC Level L = bits 01, then 3 mask bits
    const data = (0b01 << 3) | maskPattern;
    // BCH error correction
    let rem = data << 10;
    const gen = 0b10100110111;
    for (let i = 14; i >= 10; i--) {
      if ((rem >> i) & 1) rem ^= gen << (i - 10);
    }
    return ((data << 10) | rem) ^ FORMAT_MASK;
  }

  function placeFormat(m, N, maskPattern) {
    const bits = formatBits(maskPattern);
    const seq = [0,1,2,3,4,5,7,8,8,7,6,5,4,3,2,1,0];

    // Around top-left finder
    for (let i = 0; i <= 5; i++) setModule(m, 8, i, (bits >> (14 - i)) & 1);
    setModule(m, 8, 7, (bits >> 8) & 1);
    setModule(m, 8, 8, (bits >> 7) & 1);
    setModule(m, 7, 8, (bits >> 6) & 1);
    for (let i = 5; i >= 0; i--) setModule(m, 5 - i, 8, (bits >> i) & 1);

    // Around top-right and bottom-left finders
    for (let i = 0; i <= 7; i++) setModule(m, 8, N - 1 - i, (bits >> i) & 1);
    for (let i = 0; i <= 6; i++) setModule(m, N - 7 + i, 8, (bits >> (14 - i)) & 1);
  }

  function placeData(m, bits) {
    const N = m.length;
    let bitIdx = 0;
    let goUp = true;

    for (let right = N - 1; right >= 1; right -= 2) {
      if (right === 6) right--; // skip timing column
      const cols = [right, right - 1];
      const rowRange = goUp
        ? Array.from({ length: N }, (_, i) => N - 1 - i)
        : Array.from({ length: N }, (_, i) => i);

      for (const row of rowRange) {
        for (const col of cols) {
          if (m[row][col] === -1) { // not a function module
            const bit = bitIdx < bits.length ? bits[bitIdx++] : 0;
            m[row][col] = bit;
          }
        }
      }
      goUp = !goUp;
    }
  }

  // Mask patterns (0-7)
  const MASK_FNS = [
    (r, c) => (r + c) % 2 === 0,
    (r, c) => r % 2 === 0,
    (r, c) => c % 3 === 0,
    (r, c) => (r + c) % 3 === 0,
    (r, c) => (Math.floor(r / 2) + Math.floor(c / 3)) % 2 === 0,
    (r, c) => (r * c) % 2 + (r * c) % 3 === 0,
    (r, c) => ((r * c) % 2 + (r * c) % 3) % 2 === 0,
    (r, c) => ((r + c) % 2 + (r * c) % 3) % 2 === 0,
  ];

  function applyMask(m, maskPattern) {
    const fn = MASK_FNS[maskPattern];
    const N = m.length;
    for (let r = 0; r < N; r++) {
      for (let c = 0; c < N; c++) {
        if (!isFunc(m, r, c)) {
          m[r][c] ^= fn(r, c) ? 1 : 0;
        }
      }
    }
  }

  // Simplified penalty (just count dark modules ratio — pick mask 0 for simplicity)
  function evaluatePenalty(m) {
    const N = m.length;
    let penalty = 0;

    // Rule 1: consecutive same-color runs
    for (let r = 0; r < N; r++) {
      let run = 1;
      for (let c = 1; c < N; c++) {
        if ((m[r][c] & 1) === (m[r][c-1] & 1)) { run++; }
        else { if (run >= 5) penalty += run - 2; run = 1; }
      }
      if (run >= 5) penalty += run - 2;
    }

    // Rule 3: dark/light ratio
    let dark = 0, total = N * N;
    for (let r = 0; r < N; r++)
      for (let c = 0; c < N; c++)
        if ((m[r][c] & 1) === 1) dark++;
    const pct = dark / total;
    penalty += Math.abs(Math.ceil(pct * 20) - 10) * 10;

    return penalty;
  }

  function bestMask(m, version) {
    // Try all 8 masks, pick best penalty
    let best = Infinity, bestIdx = 0;
    for (let mp = 0; mp < 8; mp++) {
      const copy = m.map(row => new Int8Array(row));
      applyMask(copy, mp);
      placeFormat(copy, copy.length, mp);
      const p = evaluatePenalty(copy);
      if (p < best) { best = p; bestIdx = mp; }
    }
    return bestIdx;
  }

  // --- Rendering ---
  function render(m, canvas, scale) {
    const N   = m.length;
    const quiet = 4; // quiet zone modules
    const size  = (N + quiet * 2) * scale;
    canvas.width  = size;
    canvas.height = size;

    const ctx = canvas.getContext('2d');
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';

    ctx.fillStyle = '#FFFFFF';
    ctx.fillRect(0, 0, size, size);

    ctx.fillStyle = '#000000';
    for (let r = 0; r < N; r++) {
      for (let c = 0; c < N; c++) {
        if ((m[r][c] & 1) === 1) {
          ctx.fillRect((c + quiet) * scale, (r + quiet) * scale, scale, scale);
        }
      }
    }
  }

  // --- Public API ---
  function generate(text, canvas, scale) {
    scale = scale || 6;
    const version = getVersion(text.length);
    if (version < 0) { console.error('QR: data too long'); return; }

    const N = version * 4 + 17;
    const m = makeMatrix(N);

    // Place function modules
    placeFinders(m, N);
    placeTiming(m, N);
    placeAlignment(m, version);
    placeDarkModule(m, version);

    // Temporary format (will be overwritten)
    placeFormat(m, N, 0);

    // Encode data
    const dataBytes   = encodeData(text, version);
    const allCodewords = buildCodewords(dataBytes, version);
    const dataBits    = codewordsToBits(allCodewords);

    // Place data modules
    placeData(m, dataBits);

    // Find best mask
    const maskPattern = bestMask(m, version);
    applyMask(m, maskPattern);
    placeFormat(m, N, maskPattern);

    render(m, canvas, scale);
  }

  return { generate };

})();

// ============================================================
// 12. SUPPORT PAGE — QR CODES
// ============================================================
function initQRCodes() {
  document.querySelectorAll('[data-qr]').forEach(function (canvas) {
    const text = canvas.getAttribute('data-qr');
    if (!text || text.startsWith('[')) return; // placeholder
    const scale = parseInt(canvas.getAttribute('data-qr-scale') || '6', 10);
    QR.generate(text, canvas, scale);
  });
}

// Initialize QR codes after DOM ready
document.addEventListener('DOMContentLoaded', initQRCodes);

// Re-render QR codes when theme changes (background color)
document.addEventListener('click', function (e) {
  if (e.target.closest && e.target.closest('#btn-theme')) {
    setTimeout(initQRCodes, 100);
  }
});

// ============================================================
// 13. EXAMPLE GALLERY FILTERING (examples page)
// ============================================================
function initExamplesFilter() {
  const buttons = document.querySelectorAll('.filter-btn[data-filter]');
  if (!buttons.length) return;

  buttons.forEach(function (btn) {
    btn.addEventListener('click', function () {
      buttons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const filter = btn.getAttribute('data-filter');

      document.querySelectorAll('.example-card[data-tags]').forEach(function (card) {
        if (filter === 'all') {
          card.style.display = '';
          return;
        }
        const tags = card.getAttribute('data-tags') || '';
        card.style.display = tags.includes(filter) ? '' : 'none';
      });
    });
  });
}

document.addEventListener('DOMContentLoaded', initExamplesFilter);

// ============================================================
// 14. UTILITY
// ============================================================
function escHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}
