# -*- coding: utf-8 -*-
"""
update-recipes.py
1. Adds Leftover Remixes section to each of the 18 existing recipe cards
2. Inserts 8 new recipe cards before the bottom CTA block
3. Updates the Table of Contents
"""

import re, sys

SRC = 'prompts/index.html'

with open(SRC, encoding='utf-8') as f:
    html = f.read()

# ─────────────────────────────────────────────
# Helper
# ─────────────────────────────────────────────

def remix_block(spicy, mild, budget):
    return (
        '\n    <div style="margin-top:var(--s5);padding:var(--s4) var(--s5);'
        'background:var(--bg-alt);border:1px solid var(--border);border-radius:var(--r3);">\n'
        '      <div class="recipe-section-label" style="margin-bottom:var(--s3);">🔁 Leftover Remixes</div>\n'
        '      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:var(--s4);">\n'
        '        <div>\n'
        '          <p style="font-weight:700;font-size:var(--text-sm);color:var(--accent);margin-bottom:var(--s1);">🌶️ Spicy</p>\n'
        f'          <p style="font-size:0.8rem;color:var(--text-2);margin:0;line-height:1.5;">{spicy}</p>\n'
        '        </div>\n'
        '        <div>\n'
        '          <p style="font-weight:700;font-size:var(--text-sm);color:var(--accent);margin-bottom:var(--s1);">🧊 Mild</p>\n'
        f'          <p style="font-size:0.8rem;color:var(--text-2);margin:0;line-height:1.5;">{mild}</p>\n'
        '        </div>\n'
        '        <div>\n'
        '          <p style="font-weight:700;font-size:var(--text-sm);color:var(--accent);margin-bottom:var(--s1);">💰 Budget</p>\n'
        f'          <p style="font-size:0.8rem;color:var(--text-2);margin:0;line-height:1.5;">{budget}</p>\n'
        '        </div>\n'
        '      </div>\n'
        '    </div>'
    )

def add_remix(content, recipe_id, spicy, mild, budget):
    """Append a Leftover Remixes block inside the named recipe card."""
    rb = remix_block(spicy, mild, budget)
    # The outer recipe card closes with exactly:  \n  </div>\n</details>
    pattern = (
        r'(<details id="' + re.escape(recipe_id) + r'"'
        r'.*?)(  </div>\n</details>)'
    )
    def repl(m):
        return m.group(1) + rb + '\n  </div>\n</details>'
    new, n = re.subn(pattern, repl, content, count=1, flags=re.DOTALL)
    if n == 0:
        print(f'  WARNING: no match for recipe id="{recipe_id}"', file=sys.stderr)
    return new

# ─────────────────────────────────────────────
# 1. Add Leftover Remixes to all 18 existing recipes
# ─────────────────────────────────────────────

REMIXES = [
    ('research-plan',
     'After the 3-step plan, add: "Now identify the two assumptions in this plan most likely to be wrong — and tell me the cheapest way to test each one before I commit."',
     'Skip the research phase. Just ask: "What is the single most important first step I should take this week to make progress on [goal]?"',
     '"What free resources — communities, YouTube channels, or books — would you use to learn this without spending money?"'),

    ('teach-me',
     'After the explanation, ask: "Now quiz me with 3 questions to check whether I actually understood this. Grade my answers and fill in any gaps."',
     'Strip it back: "Give me just the one key insight about [topic] that most people miss. One sentence."',
     '"What\'s the single best free resource — one book, video, or website — to actually learn this properly?"'),

    ('devils-advocate',
     'Run both at once: "Steelman my idea AND devil\'s advocate it simultaneously. Show me the strongest case for and against, then tell me where the real crux of the disagreement lies."',
     'Just the headlines: "Give me the top 3 objections, each in one sentence. No explanation needed."',
     '"What\'s the cheapest, lowest-risk experiment I could run this week to test whether the main objection is actually true?"'),

    ('step-by-step',
     'After the steps: "Now identify which two steps are the most likely failure points for most people, and give me a contingency for each one."',
     'Bite-sized: "Give me just the first 3 steps. I\'ll ask for more once I\'ve done those."',
     '"Do the full plan but with zero budget — what\'s the free or DIY version of each step?"'),

    ('summarize',
     'Summarize and fact-check in one pass: "Flag any claims in the original that look weakly supported or that you\'d want someone to verify before acting on."',
     'One-liner: "What\'s the single most important sentence I should take away from this?"',
     '"Give me 3 bullet points short enough to paste into a text message."'),

    ('draft-critique-revise',
     'Add a fourth round: after the revision, ask "If this was the last thing I ever sent on this topic, what\'s the one thing you\'d still change?"',
     'Skip the loop: "Just write me a solid first draft. I\'ll edit it myself from there."',
     '"Give me a reusable template with [FILL IN] placeholders so I can write this type of message faster every time."'),

    ('act-as',
     'Before any advice, add: "As this expert, ask me the 5 hardest questions you\'d want answered before giving a recommendation. I\'ll answer them, then you advise."',
     'No roleplay needed: "Without playing a role — what would a knowledgeable generalist flag as the most important thing to think about here?"',
     '"What would a smart, experienced person with no specialist credentials recommend for free, and what would they tell me to google?"'),

    ('rubber-duck',
     'After the questions: "Now give me your honest assessment — based on what I\'ve told you, what do you think I\'m actually doing wrong? Don\'t soften it."',
     'One question only: "Ask me the single most important question that would help reveal what\'s really going on."',
     '"Give me a 5-question checklist I can run through on my own next time I get stuck like this."'),

    ('chain-prompts',
     'At each reasoning step, add a confidence level: "Rate your confidence at each step 1–10 and note what new information would change your conclusion."',
     'Skip the reasoning: "Just give me your best answer. I\'ll ask for the reasoning if I need it."',
     '"What\'s the fastest version of this analysis I could do myself in 5 minutes with a pen and paper?"'),

    ('constraints',
     'Add a creative constraint: "The output must feel surprising — something I wouldn\'t have written myself if left to my defaults."',
     'Start open: "Ignore all constraints for now and give me a rough draft. I\'ll add guardrails after I see what I\'m working with."',
     '"Give me a fill-in-the-blanks template I can reuse for this type of content without running the prompt again."'),

    ('compare-options',
     'After the recommendation: "Tell me what would have to be true for the runner-up option to actually be the better choice. What\'s the scenario where you\'d change your mind?"',
     'Cut to the chase: "Just tell me which one to pick and the single most important reason why. One sentence."',
     '"Is there a free or significantly cheaper option I haven\'t listed? What would I be giving up by choosing it?"'),

    ('iterative-refine',
     'One more pass: after the revision, ask "Rewrite it as the best possible version of this piece — as if it were written by the world\'s best writer of this format. Show me a brief note on the biggest things you changed."',
     'Minimum viable edit: "Change only the single most impactful thing. Leave everything else exactly as it is."',
     '"Give me 3 editing rules — specific to this style of writing — that I can apply myself to anything I write in this format."'),

    ('meeting-notes',
     'After the summary, add: "Flag any decisions in these notes that look risky, any action items that seem likely to get dropped, and any open questions that could derail next steps."',
     'Action items only: "Pull out only the action items — who has to do what, by when. Nothing else."',
     '"Write me a 2-line Slack message I can paste to the team right now that captures the key outcome and next step."'),

    ('code-review',
     'After the review: "Now rewrite the function with all the fixes applied. Show me a brief summary of every change you made and why."',
     'Bugs only: "Just look for logic errors and bugs. Skip style, readability, and security for this pass."',
     '"What\'s the single most important test I should write for this code before shipping it? Write the test for me."'),

    ('interview-prep',
     'Score mode: "After each answer, rate it 1–10 and tell me exactly what a hiring manager at a top-tier company would think — including whether it would move me to the next round."',
     'Question list only: "Give me the 5 most likely questions for this role and a one-sentence tip for approaching each. I\'ll prep the answers myself."',
     '"What\'s the one thing most candidates at this level fail to communicate clearly — and what\'s the simplest way to make sure I nail it?"'),

    ('reframe',
     'After the 5 reframes, add: "Now give me the contrarian take — the version where my original problem isn\'t actually a problem at all. What if I\'m solving for the wrong thing entirely?"',
     'Two reframes only: "Give me the reframe most different from how I\'m currently thinking, and the most immediately practical one."',
     '"What\'s the smallest experiment I could run this week — for free or nearly free — to test whether I\'m even solving the right problem?"'),

    ('tone-shift',
     'Three versions at once: "Rewrite it in 3 completely different tones back-to-back. I\'ll pick the one to develop further."',
     'One change only: "Make it shorter and more direct. That\'s it. Don\'t change anything else."',
     '"List 5 specific words or phrases in my original that are hurting the tone, and tell me what to replace each one with."'),

    ('gap-finder',
     'Hardest critic mode: "Pretend you\'re the most skeptical, most informed person in the room. What would you say right now to torpedo this completely?"',
     'Top gap only: "Tell me the single most important thing that\'s missing. One bullet. Then stop."',
     '"What\'s one thing I could add in 10 minutes that would meaningfully strengthen this before I share it?"'),
]

print(f'Adding remixes to {len(REMIXES)} recipes...')
for rid, spicy, mild, budget in REMIXES:
    before = html
    html = add_remix(html, rid, spicy, mild, budget)
    if html == before:
        print(f'  SKIPPED (no change): {rid}')
    else:
        print(f'  OK {rid}')

# ─────────────────────────────────────────────
# 2. Eight new recipe cards
# ─────────────────────────────────────────────

NEW_RECIPES = '''
<!-- ==============================
     RECIPE: COLD EMAIL THAT GETS REPLIES
     ============================== -->
<details id="cold-email" class="recipe-card" style="margin-bottom: var(--s10);">
  <summary class="recipe-card-header">
    <div>
      <span class="recipe-tag">Outreach</span>
      <h3 style="margin-top: var(--s2);">The Cold Email That Gets Replies</h3>
    </div>
    <span class="recipe-chevron" aria-hidden="true">▾</span>
  </summary>
  <div class="recipe-card-body">
    <div class="recipe-meta">
      <span>🎯 Goal: A personalized cold email the recipient actually wants to read</span>
      <span>📊 Difficulty: Beginner</span>
      <span>🤖 Best for: Claude, ChatGPT</span>
    </div>
    <p>Most cold emails fail for one reason: they lead with what the sender wants, not what the recipient cares about. This recipe flips that. The prompt forces AI to write from the recipient's perspective first — which is the only way cold outreach actually works.</p>

    <div class="recipe-section-label">Ingredients</div>
    <ul style="font-size: var(--text-sm); color: var(--text-2);">
      <li><strong>[YOUR NAME &amp; ROLE]</strong> — who you are in one line</li>
      <li><strong>[RECIPIENT NAME &amp; ROLE]</strong> — who you're writing to</li>
      <li><strong>[ONE SPECIFIC THING YOU KNOW ABOUT THEM]</strong> — a post, project, company news, or achievement</li>
      <li><strong>[WHAT YOU'RE ASKING FOR]</strong> — one small, specific ask (a call, feedback, intro)</li>
      <li><strong>[WHAT'S IN IT FOR THEM]</strong> — the actual value you're offering</li>
    </ul>

    <div class="recipe-section-label">The Recipe</div>
    <div class="prompt-block"><pre>Write a cold email from [YOUR NAME &amp; ROLE] to [RECIPIENT NAME &amp; ROLE].

What I know about them specifically: [ONE SPECIFIC THING — a recent post, project, or achievement of theirs]

What I'm asking for: [SMALL, SPECIFIC ASK — e.g., "a 20-minute call to get your perspective on X"]

What's in it for them: [VALUE YOU BRING — e.g., "I'm working on X which directly relates to their work on Y"]

Rules for the email:
- Subject line that references the specific thing I mentioned (not generic)
- Under 150 words total
- Lead with THEM, not me — reference what I know about their work in the first sentence
- One clear ask only — no list of things I want
- No "I hope this email finds you well" or similar filler
- Sign off with my name and one-line context (not a full signature block)</pre></div>

    <div class="recipe-section-label">Example — Reaching out to a podcast host</div>
    <div class="prompt-block"><pre>Write a cold email from Sarah Chen (UX researcher, 8 years in fintech) to Marcus Webb (host of the "Product Failures" podcast).

What I know about them specifically: His recent episode on the Robinhood IPO app crash was the most detailed post-mortem I've heard — specifically the point about loading state UX causing panic selling.

What I'm asking for: A 15-minute conversation about whether a research-focused episode on fintech UX failure patterns would resonate with his audience.

What's in it for them: I have access to 3 unpublished case studies from my work that would be exclusive content for his show.

Rules for the email:
- Subject line that references the specific thing I mentioned (not generic)
- Under 150 words total
- Lead with THEM — reference his episode in the first sentence
- One clear ask only
- No "I hope this email finds you well" or filler
- Sign off with my name and one-line context</pre></div>

    <div class="callout callout-tip">
      <span class="callout-icon">💡</span>
      <div class="callout-body">
        <h4>The one rule of cold email</h4>
        <p>The specific thing you know about them is 80% of the work. "I read your article" is generic. "Your point about loading states in the Robinhood episode changed how I think about failure UX" is specific. Specificity is proof you actually paid attention — and it's nearly impossible to fake.</p>
      </div>
    </div>

    <div style="margin-top:var(--s5);padding:var(--s4) var(--s5);background:var(--bg-alt);border:1px solid var(--border);border-radius:var(--r3);">
      <div class="recipe-section-label" style="margin-bottom:var(--s3);">🔁 Leftover Remixes</div>
      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:var(--s4);">
        <div>
          <p style="font-weight:700;font-size:var(--text-sm);color:var(--accent);margin-bottom:var(--s1);">🌶️ Spicy</p>
          <p style="font-size:0.8rem;color:var(--text-2);margin:0;line-height:1.5;">After the draft: "Now write 3 different subject lines — one curiosity-driven, one direct, one that references their specific work. Tell me which you'd send and why."</p>
        </div>
        <div>
          <p style="font-weight:700;font-size:var(--text-sm);color:var(--accent);margin-bottom:var(--s1);">🧊 Mild</p>
          <p style="font-size:0.8rem;color:var(--text-2);margin:0;line-height:1.5;">LinkedIn version: "Rewrite this as a LinkedIn connection request message — max 300 characters, same personalization rules."</p>
        </div>
        <div>
          <p style="font-weight:700;font-size:var(--text-sm);color:var(--accent);margin-bottom:var(--s1);">💰 Budget</p>
          <p style="font-size:0.8rem;color:var(--text-2);margin:0;line-height:1.5;">"Give me a follow-up email template to send if I don't hear back in 5 days — short, non-pushy, one sentence of new value."</p>
        </div>
      </div>
    </div>
  </div>
</details>

<!-- ==============================
     RECIPE: LEARN ANY SKILL IN 30 DAYS
     ============================== -->
<details id="learn-skill" class="recipe-card" style="margin-bottom: var(--s10);">
  <summary class="recipe-card-header">
    <div>
      <span class="recipe-tag">Learning</span>
      <h3 style="margin-top: var(--s2);">Learn Any Skill in 30 Days</h3>
    </div>
    <span class="recipe-chevron" aria-hidden="true">▾</span>
  </summary>
  <div class="recipe-card-body">
    <div class="recipe-meta">
      <span>🎯 Goal: A realistic, personalized accelerated learning plan</span>
      <span>📊 Difficulty: Home Cook</span>
      <span>🤖 Best for: Claude, Perplexity</span>
    </div>
    <p>Generic learning advice fails because it ignores your specific situation — how much time you have, what you already know, and what "good enough" looks like for your goal. This recipe produces a learning plan that actually fits your life.</p>

    <div class="recipe-section-label">Ingredients</div>
    <ul style="font-size: var(--text-sm); color: var(--text-2);">
      <li><strong>[SKILL]</strong> — what you want to learn</li>
      <li><strong>[YOUR STARTING POINT]</strong> — what you already know</li>
      <li><strong>[GOAL OUTCOME]</strong> — what does "done" look like for you?</li>
      <li><strong>[TIME AVAILABLE]</strong> — realistic hours per week</li>
      <li><strong>[DEADLINE OR DRIVER]</strong> — why 30 days? what's pushing this?</li>
    </ul>

    <div class="recipe-section-label">The Recipe</div>
    <div class="prompt-block"><pre>I want to learn [SKILL] in 30 days. Design me a realistic learning plan.

My starting point: [WHAT YOU ALREADY KNOW — even "absolutely nothing" is fine]
My goal: [WHAT DOES SUCCESS LOOK LIKE — e.g., "build a working app", "hold a basic conversation", "pass a certification exam"]
Time I can commit: [HOURS PER WEEK — be honest, not aspirational]
Why I'm doing this: [CONTEXT — job change, curiosity, a specific project]

Give me:
1. A week-by-week breakdown (Weeks 1–4) with a clear focus for each week
2. The 3 most important concepts or skills to nail in the first 7 days
3. The biggest mistake beginners make that wastes their time — and how to avoid it
4. One free resource and one paid resource (with a cost estimate) for each phase
5. A simple way to measure whether I'm actually making progress each week</pre></div>

    <div class="recipe-section-label">Example — Learning SQL for data analysis</div>
    <div class="prompt-block"><pre>I want to learn SQL in 30 days. Design me a realistic learning plan.

My starting point: I understand spreadsheets well (pivot tables, VLOOKUP) but have never written a SQL query.
My goal: Be able to write queries to pull, filter, and aggregate data from our company's PostgreSQL database independently — no hand-holding from the engineering team.
Time I can commit: 45 minutes per day on weekdays, 2 hours on Saturday.
Why I'm doing this: My new role requires me to pull my own data instead of requesting it from a data analyst.

Give me:
1. A week-by-week breakdown (Weeks 1–4) with a clear focus for each week
2. The 3 most important concepts to nail in the first 7 days
3. The biggest mistake beginners make that wastes their time
4. One free resource and one paid resource for each phase
5. A simple weekly progress check I can do in 10 minutes</pre></div>

    <div class="callout callout-tip">
      <span class="callout-icon">💡</span>
      <div class="callout-body">
        <h4>The secret to 30-day learning</h4>
        <p>The goal isn't mastery — it's "good enough for my specific use case." Being honest about your actual outcome (not the aspirational one) produces a much more useful plan. "Hold a basic conversation in Spanish" and "achieve B2 fluency" need completely different 30-day plans.</p>
      </div>
    </div>

    <div style="margin-top:var(--s5);padding:var(--s4) var(--s5);background:var(--bg-alt);border:1px solid var(--border);border-radius:var(--r3);">
      <div class="recipe-section-label" style="margin-bottom:var(--s3);">🔁 Leftover Remixes</div>
      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:var(--s4);">
        <div>
          <p style="font-weight:700;font-size:var(--text-sm);color:var(--accent);margin-bottom:var(--s1);">🌶️ Spicy</p>
          <p style="font-size:0.8rem;color:var(--text-2);margin:0;line-height:1.5;">After the plan: "Now design Week 1 Day 1 in full detail — exactly what I should do in my first 45-minute session, step by step."</p>
        </div>
        <div>
          <p style="font-weight:700;font-size:var(--text-sm);color:var(--accent);margin-bottom:var(--s1);">🧊 Mild</p>
          <p style="font-size:0.8rem;color:var(--text-2);margin:0;line-height:1.5;">"I only have 7 days, not 30. What's the minimum I need to learn to be useful immediately?"</p>
        </div>
        <div>
          <p style="font-weight:700;font-size:var(--text-sm);color:var(--accent);margin-bottom:var(--s1);">💰 Budget</p>
          <p style="font-size:0.8rem;color:var(--text-2);margin:0;line-height:1.5;">"Build the same plan using only free resources — YouTube, official docs, free tiers of tools. No paid courses."</p>
        </div>
      </div>
    </div>
  </div>
</details>

<!-- ==============================
     RECIPE: CONTENT REPURPOSING MACHINE
     ============================== -->
<details id="content-repurpose" class="recipe-card" style="margin-bottom: var(--s10);">
  <summary class="recipe-card-header">
    <div>
      <span class="recipe-tag">Content</span>
      <h3 style="margin-top: var(--s2);">The Content Repurposing Machine</h3>
    </div>
    <span class="recipe-chevron" aria-hidden="true">▾</span>
  </summary>
  <div class="recipe-card-body">
    <div class="recipe-meta">
      <span>🎯 Goal: Turn one piece of content into five ready-to-post formats</span>
      <span>📊 Difficulty: Home Cook</span>
      <span>🤖 Best for: ChatGPT, Claude</span>
    </div>
    <p>Creating content from scratch every day is exhausting. But most creators have a library of solid long-form content that's only ever been seen once. This recipe extracts the maximum value from something you've already made.</p>

    <div class="recipe-section-label">Ingredients</div>
    <ul style="font-size: var(--text-sm); color: var(--text-2);">
      <li><strong>[ORIGINAL CONTENT]</strong> — a blog post, newsletter, video transcript, podcast episode, or long LinkedIn post</li>
      <li><strong>[YOUR AUDIENCE]</strong> — who follows you and what they care about</li>
      <li><strong>[YOUR TONE]</strong> — how you normally sound (e.g., "direct and a bit dry", "warm and encouraging")</li>
    </ul>

    <div class="recipe-section-label">The Recipe</div>
    <div class="prompt-block"><pre>Here's a piece of content I've created:

[PASTE YOUR ORIGINAL CONTENT]

My audience: [WHO THEY ARE AND WHAT THEY CARE ABOUT]
My usual tone: [HOW YOU NORMALLY SOUND]

Repurpose this into 5 formats:
1. **Twitter/X thread** — 5–7 tweets, hook tweet first, each tweet one clear idea
2. **LinkedIn post** — 150–200 words, professional but personal, ends with a question to drive comments
3. **Email newsletter intro** — 100 words, conversational, makes the reader want to read the full piece
4. **Instagram caption** — 80 words max, starts with a strong hook line, includes a call to action
5. **TL;DR summary** — 3 bullet points, could be used as a content preview or story slide

Keep my tone consistent across all formats. Don't add ideas that weren't in the original.</pre></div>

    <div class="callout callout-tip">
      <span class="callout-icon">💡</span>
      <div class="callout-body">
        <h4>One piece of content, a week of posts</h4>
        <p>A solid 1,000-word article contains enough material for a week of daily posts across platforms — if you extract the right things. The key constraint is "don't add ideas that weren't in the original" — this keeps each repurposed piece authentic and prevents the AI from drifting into generic territory.</p>
      </div>
    </div>

    <div style="margin-top:var(--s5);padding:var(--s4) var(--s5);background:var(--bg-alt);border:1px solid var(--border);border-radius:var(--r3);">
      <div class="recipe-section-label" style="margin-bottom:var(--s3);">🔁 Leftover Remixes</div>
      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:var(--s4);">
        <div>
          <p style="font-weight:700;font-size:var(--text-sm);color:var(--accent);margin-bottom:var(--s1);">🌶️ Spicy</p>
          <p style="font-size:0.8rem;color:var(--text-2);margin:0;line-height:1.5;">Add: "Also pull out the 3 most quotable sentences from the original and format them as standalone quote graphics (just the text, no context needed)."</p>
        </div>
        <div>
          <p style="font-weight:700;font-size:var(--text-sm);color:var(--accent);margin-bottom:var(--s1);">🧊 Mild</p>
          <p style="font-size:0.8rem;color:var(--text-2);margin:0;line-height:1.5;">"Just give me the Twitter thread and the LinkedIn post. That's all I need right now."</p>
        </div>
        <div>
          <p style="font-weight:700;font-size:var(--text-sm);color:var(--accent);margin-bottom:var(--s1);">💰 Budget</p>
          <p style="font-size:0.8rem;color:var(--text-2);margin:0;line-height:1.5;">"Give me a content calendar — suggest which platform to post each format on, and in what order across 5 days, to maximize reach."</p>
        </div>
      </div>
    </div>
  </div>
</details>

<!-- ==============================
     RECIPE: POST-MEETING FOLLOW-UP EMAIL
     ============================== -->
<details id="meeting-followup" class="recipe-card" style="margin-bottom: var(--s10);">
  <summary class="recipe-card-header">
    <div>
      <span class="recipe-tag">Productivity</span>
      <h3 style="margin-top: var(--s2);">Post-Meeting Follow-Up Email</h3>
    </div>
    <span class="recipe-chevron" aria-hidden="true">▾</span>
  </summary>
  <div class="recipe-card-body">
    <div class="recipe-meta">
      <span>🎯 Goal: A professional follow-up email from raw notes in 60 seconds</span>
      <span>📊 Difficulty: Beginner</span>
      <span>🤖 Best for: Claude, Gemini</span>
    </div>
    <p>A good follow-up email does three things: confirms what was agreed, assigns clear ownership, and keeps the momentum going. Most people either don't send one or send something so vague it's useless. This recipe fixes that in under a minute.</p>

    <div class="recipe-section-label">Ingredients</div>
    <ul style="font-size: var(--text-sm); color: var(--text-2);">
      <li><strong>[MEETING TYPE]</strong> — sales call, team standup, client review, job interview, etc.</li>
      <li><strong>[WHO ATTENDED]</strong> — names and roles (optional but improves output)</li>
      <li><strong>[RAW NOTES]</strong> — bullet points, half-sentences, whatever you captured</li>
      <li><strong>[RELATIONSHIP]</strong> — how formal should this be?</li>
    </ul>

    <div class="recipe-section-label">The Recipe</div>
    <div class="prompt-block"><pre>I just had a [MEETING TYPE] with [WHO ATTENDED]. Here are my raw notes:

[PASTE YOUR NOTES]

Write a follow-up email that:
- Opens by thanking them and naming the specific topic we discussed (not "our meeting today")
- Summarizes the 2–3 key points we agreed on
- Lists action items clearly: what, who, by when (use what's in the notes; flag [OWNER?] if unclear)
- Ends with a clear next step — either a date for the next touchpoint or what I'll deliver first
- Tone: [FORMAL / PROFESSIONAL BUT WARM / CASUAL]
- Length: Short — under 200 words. This is a follow-up, not a report.</pre></div>

    <div class="recipe-section-label">Example — Client discovery call</div>
    <div class="prompt-block"><pre>I just had a discovery call with Sarah (Head of Marketing) and James (CMO) at Elevate Health. Here are my raw notes:

- They want to rebrand before Q4 product launch
- Pain point: current brand feels "clinical" not "human"
- Budget: $25–40k for full brand identity
- Timeline: needs to be done by Sept 15
- They liked our healthcare portfolio but want to see B2C examples too
- James: final decision maker, Sarah runs day-to-day
- Next step: send proposal + 3 B2C case studies by Friday
- They're also talking to 2 other agencies

Write a follow-up email that:
- Opens by thanking them and naming the specific thing we discussed
- Summarizes the 2–3 key things we agreed on
- Lists action items clearly: what, who, by when
- Ends with a clear next step
- Tone: Professional but warm — we want to stand out from the other agencies
- Length: Under 200 words</pre></div>

    <div class="callout callout-beginner">
      <span class="callout-icon">🟢</span>
      <div class="callout-body">
        <h4>Send it within 2 hours</h4>
        <p>The best follow-up email is the one that arrives while the meeting is still fresh in everyone's mind. Paste your notes as soon as the call ends, generate the email, do a quick read-through, and send. The whole process takes under 5 minutes.</p>
      </div>
    </div>

    <div style="margin-top:var(--s5);padding:var(--s4) var(--s5);background:var(--bg-alt);border:1px solid var(--border);border-radius:var(--r3);">
      <div class="recipe-section-label" style="margin-bottom:var(--s3);">🔁 Leftover Remixes</div>
      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:var(--s4);">
        <div>
          <p style="font-weight:700;font-size:var(--text-sm);color:var(--accent);margin-bottom:var(--s1);">🌶️ Spicy</p>
          <p style="font-size:0.8rem;color:var(--text-2);margin:0;line-height:1.5;">Add: "Also flag any commitments I've made in these notes that look risky or that I might struggle to deliver on time."</p>
        </div>
        <div>
          <p style="font-weight:700;font-size:var(--text-sm);color:var(--accent);margin-bottom:var(--s1);">🧊 Mild</p>
          <p style="font-size:0.8rem;color:var(--text-2);margin:0;line-height:1.5;">"Just give me the action items in a bullet list. I'll write the email myself."</p>
        </div>
        <div>
          <p style="font-weight:700;font-size:var(--text-sm);color:var(--accent);margin-bottom:var(--s1);">💰 Budget</p>
          <p style="font-size:0.8rem;color:var(--text-2);margin:0;line-height:1.5;">"Give me a reusable follow-up template with [FILL IN] placeholders I can use for every meeting of this type."</p>
        </div>
      </div>
    </div>
  </div>
</details>

<!-- ==============================
     RECIPE: SCENE STARTER FOR FICTION
     ============================== -->
<details id="scene-starter" class="recipe-card" style="margin-bottom: var(--s10);">
  <summary class="recipe-card-header">
    <div>
      <span class="recipe-tag">Creative</span>
      <h3 style="margin-top: var(--s2);">Scene Starter for Fiction</h3>
    </div>
    <span class="recipe-chevron" aria-hidden="true">▾</span>
  </summary>
  <div class="recipe-card-body">
    <div class="recipe-meta">
      <span>🎯 Goal: A compelling opening scene in the exact mood and style you want</span>
      <span>📊 Difficulty: Beginner</span>
      <span>🤖 Best for: Claude, ChatGPT</span>
    </div>
    <p>The blank page problem in fiction is almost always a starting problem, not a story problem. Once you have a scene with real texture — specific details, a voice, a mood — the story usually flows. This recipe gives you that first handhold.</p>

    <div class="recipe-section-label">Ingredients</div>
    <ul style="font-size: var(--text-sm); color: var(--text-2);">
      <li><strong>[GENRE / MOOD]</strong> — the feeling you want the reader to have</li>
      <li><strong>[CHARACTER]</strong> — who is in this scene and what do we know about them?</li>
      <li><strong>[SETTING]</strong> — where and when is this happening?</li>
      <li><strong>[DRAMATIC TENSION]</strong> — what's wrong, uncertain, or at stake?</li>
      <li><strong>[STYLISTIC NOTES]</strong> — any authors or works you want to sound like</li>
    </ul>

    <div class="recipe-section-label">The Recipe</div>
    <div class="prompt-block"><pre>Write the opening scene of a story with these parameters:

Genre / mood: [GENRE AND THE FEELING YOU WANT — e.g., "quiet dread, literary thriller", "warm and nostalgic, like a memory"]
Character: [WHO — name, age, one key thing we need to know immediately]
Setting: [WHERE AND WHEN — be specific: city, season, time of day, decade]
What's at stake: [THE TENSION — what's wrong, uncertain, or about to change]
Style: [ANY REFERENCE POINTS — e.g., "Kazuo Ishiguro's restraint", "short sentences like Hemingway", "lush and sensory like Donna Tartt"]

Write approximately 300–400 words. End at a moment of tension or curiosity, not resolution. Show, don't tell — use specific sensory details rather than telling me how the character feels.</pre></div>

    <div class="recipe-section-label">Example — Quiet horror, small town</div>
    <div class="prompt-block"><pre>Write the opening scene of a story with these parameters:

Genre / mood: Quiet horror — the kind where something is wrong but nobody says it out loud
Character: Miriam, 52, who has just returned to her childhood home to care for her aging mother and immediately notices something has changed
Setting: A small town in rural Ohio, late October, overcast mid-afternoon
What's at stake: Miriam knows something happened in this house. Her mother refuses to talk about it. The town behaves strangely around her.
Style: Short sentences, restrained — more Patricia Highsmith than Stephen King. The horror is in what's not said.

Write approximately 350 words. End at a moment of unease, not explanation.</pre></div>

    <div class="callout callout-tip">
      <span class="callout-icon">💡</span>
      <div class="callout-body">
        <h4>Use it as a first draft, not a final product</h4>
        <p>The best use of this recipe is to generate three or four different opening scenes from the same ingredients and see which one has the energy you want to follow. Ask for "a completely different take on the same scene" after each one — you'll usually find your voice by seeing it from different angles.</p>
      </div>
    </div>

    <div style="margin-top:var(--s5);padding:var(--s4) var(--s5);background:var(--bg-alt);border:1px solid var(--border);border-radius:var(--r3);">
      <div class="recipe-section-label" style="margin-bottom:var(--s3);">🔁 Leftover Remixes</div>
      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:var(--s4);">
        <div>
          <p style="font-weight:700;font-size:var(--text-sm);color:var(--accent);margin-bottom:var(--s1);">🌶️ Spicy</p>
          <p style="font-size:0.8rem;color:var(--text-2);margin:0;line-height:1.5;">After the scene: "Now write the same scene from a completely different character's point of view — someone who was watching Miriam arrive."</p>
        </div>
        <div>
          <p style="font-weight:700;font-size:var(--text-sm);color:var(--accent);margin-bottom:var(--s1);">🧊 Mild</p>
          <p style="font-size:0.8rem;color:var(--text-2);margin:0;line-height:1.5;">"I have a scene I've already written. Edit it to increase the tension without adding new plot — just sharpen what's already there."</p>
        </div>
        <div>
          <p style="font-weight:700;font-size:var(--text-sm);color:var(--accent);margin-bottom:var(--s1);">💰 Budget</p>
          <p style="font-size:0.8rem;color:var(--text-2);margin:0;line-height:1.5;">"Give me 5 opening lines only — each a completely different angle on this story. I'll pick the one to develop."</p>
        </div>
      </div>
    </div>
  </div>
</details>

<!-- ==============================
     RECIPE: 10-10-10 DECISION TEST
     ============================== -->
<details id="decision-1010" class="recipe-card" style="margin-bottom: var(--s10);">
  <summary class="recipe-card-header">
    <div>
      <span class="recipe-tag">Decisions</span>
      <h3 style="margin-top: var(--s2);">The 10-10-10 Decision Test</h3>
    </div>
    <span class="recipe-chevron" aria-hidden="true">▾</span>
  </summary>
  <div class="recipe-card-body">
    <div class="recipe-meta">
      <span>🎯 Goal: Get unstuck on a hard decision by stress-testing it across three time horizons</span>
      <span>📊 Difficulty: Beginner</span>
      <span>🤖 Best for: Claude</span>
    </div>
    <p>The 10-10-10 framework (from Suzy Welch) asks: how will you feel about this decision in 10 minutes, 10 months, and 10 years? Most people are stuck because they're optimizing for the wrong time horizon. AI applies this framework rigorously — then tells you what it actually sees.</p>

    <div class="recipe-section-label">Ingredients</div>
    <ul style="font-size: var(--text-sm); color: var(--text-2);">
      <li><strong>[YOUR DECISION]</strong> — stated as clearly as possible</li>
      <li><strong>[THE OPTIONS]</strong> — what are you choosing between?</li>
      <li><strong>[WHAT'S MAKING IT HARD]</strong> — why haven't you decided yet?</li>
    </ul>

    <div class="recipe-section-label">The Recipe</div>
    <div class="prompt-block"><pre>I'm trying to make this decision: [YOUR DECISION]

My options are: [OPTION A] vs [OPTION B] (and [OPTION C if applicable])

What's making it hard: [WHY YOU'RE STUCK]

Apply the 10-10-10 framework to each option:
- In 10 minutes: How will I feel right after making this choice?
- In 10 months: How will this look in the context of where I am then?
- In 10 years: Will this even matter? What would I wish I had done?

After working through all three horizons for each option:
1. Tell me which time horizon I'm probably overweighting right now (and why)
2. Give me your honest read on what this framework suggests I should do
3. Name the one thing I haven't mentioned that might change the answer</pre></div>

    <div class="recipe-section-label">Example — Taking a lower-paying job for better work-life balance</div>
    <div class="prompt-block"><pre>I'm trying to make this decision: Whether to take a new job offer that pays $15k less per year but has much better hours and culture.

My options are: Stay at my current company (higher pay, longer hours, toxic management) vs. take the new offer (lower pay, better everything else).

What's making it hard: I have a mortgage and I've always told myself I'd never take a pay cut. But I've been miserable for two years.

Apply the 10-10-10 framework:
- In 10 minutes: How will I feel right after saying yes or no?
- In 10 months: How will each choice look once I've lived with it for nearly a year?
- In 10 years: Which version of this decision will I be glad I made?

After working through the three horizons:
1. Tell me which time horizon I'm probably overweighting
2. Give me your honest read on what this framework suggests
3. Name the one thing I haven't mentioned that could change the answer</pre></div>

    <div class="callout callout-tip">
      <span class="callout-icon">💡</span>
      <div class="callout-body">
        <h4>Why this works when nothing else does</h4>
        <p>Most stuck decisions are stuck because you're weighing short-term discomfort against long-term gain without making that trade-off explicit. The 10-10-10 framework forces you to look at all three at once — which almost always reveals that you've been optimizing for the wrong one.</p>
      </div>
    </div>

    <div style="margin-top:var(--s5);padding:var(--s4) var(--s5);background:var(--bg-alt);border:1px solid var(--border);border-radius:var(--r3);">
      <div class="recipe-section-label" style="margin-bottom:var(--s3);">🔁 Leftover Remixes</div>
      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:var(--s4);">
        <div>
          <p style="font-weight:700;font-size:var(--text-sm);color:var(--accent);margin-bottom:var(--s1);">🌶️ Spicy</p>
          <p style="font-size:0.8rem;color:var(--text-2);margin:0;line-height:1.5;">Add: "Also apply the regret minimization framework — which option would 80-year-old me be more likely to regret not taking?"</p>
        </div>
        <div>
          <p style="font-weight:700;font-size:var(--text-sm);color:var(--accent);margin-bottom:var(--s1);">🧊 Mild</p>
          <p style="font-size:0.8rem;color:var(--text-2);margin:0;line-height:1.5;">"Skip the framework. Just tell me what you'd do in my position, and why. One paragraph."</p>
        </div>
        <div>
          <p style="font-weight:700;font-size:var(--text-sm);color:var(--accent);margin-bottom:var(--s1);">💰 Budget</p>
          <p style="font-size:0.8rem;color:var(--text-2);margin:0;line-height:1.5;">"What information could I gather this week — for free, with a few phone calls or conversations — that would make this decision obvious?"</p>
        </div>
      </div>
    </div>
  </div>
</details>

<!-- ==============================
     RECIPE: WEEKLY REVIEW & RESET
     ============================== -->
<details id="weekly-review" class="recipe-card" style="margin-bottom: var(--s10);">
  <summary class="recipe-card-header">
    <div>
      <span class="recipe-tag">Productivity</span>
      <h3 style="margin-top: var(--s2);">Weekly Review &amp; Reset</h3>
    </div>
    <span class="recipe-chevron" aria-hidden="true">▾</span>
  </summary>
  <div class="recipe-card-body">
    <div class="recipe-meta">
      <span>🎯 Goal: Clear your head, extract the lessons, and plan next week in one session</span>
      <span>📊 Difficulty: Beginner</span>
      <span>🤖 Best for: Claude, Gemini</span>
    </div>
    <p>Most people end the week by stopping, not by reflecting. A 15-minute weekly review — where you actually process what happened and make deliberate choices about next week — is one of the highest-ROI habits in personal productivity. This recipe turns that into a structured conversation with AI.</p>

    <div class="recipe-section-label">Ingredients</div>
    <ul style="font-size: var(--text-sm); color: var(--text-2);">
      <li><strong>[BRAIN DUMP]</strong> — everything on your mind, messy and unfiltered</li>
      <li><strong>[WHAT HAPPENED]</strong> — wins, frustrations, surprises from the week</li>
      <li><strong>[NEXT WEEK'S BIG PRIORITIES]</strong> — what matters most</li>
    </ul>

    <div class="recipe-section-label">The Recipe</div>
    <div class="prompt-block"><pre>I'm doing my weekly review. Help me process and plan.

Here's my brain dump — everything on my mind right now, unfiltered:
[PASTE YOUR BRAIN DUMP — tasks, worries, ideas, unfinished things]

Here's what happened this week:
- Wins: [WHAT WENT WELL]
- Frustrations: [WHAT DIDN'T GO WELL OR FELT DRAINING]
- Surprises: [ANYTHING UNEXPECTED]

Next week's known priorities: [WHAT YOU ALREADY KNOW IS COMING]

Based on this, help me:
1. Identify the 3 most important things I should focus on next week (not just urgent — actually important)
2. Flag anything in my brain dump that I should either schedule, delegate, or drop entirely
3. Name one pattern you notice from my wins and frustrations that I should pay attention to
4. Give me a clean "top 3 priorities" card I could put on my desk for the week</pre></div>

    <div class="callout callout-tip">
      <span class="callout-icon">💡</span>
      <div class="callout-body">
        <h4>The brain dump is the secret ingredient</h4>
        <p>The value of this recipe comes from the unfiltered brain dump — writing everything down without editing. Don't tidy it up before pasting. The messiness is the point. AI is excellent at organizing chaos; it doesn't need you to organize it first.</p>
      </div>
    </div>

    <div style="margin-top:var(--s5);padding:var(--s4) var(--s5);background:var(--bg-alt);border:1px solid var(--border);border-radius:var(--r3);">
      <div class="recipe-section-label" style="margin-bottom:var(--s3);">🔁 Leftover Remixes</div>
      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:var(--s4);">
        <div>
          <p style="font-weight:700;font-size:var(--text-sm);color:var(--accent);margin-bottom:var(--s1);">🌶️ Spicy</p>
          <p style="font-size:0.8rem;color:var(--text-2);margin:0;line-height:1.5;">Add: "After planning next week, ask me 3 hard questions about how I'm spending my time — the kind I probably don't want to answer."</p>
        </div>
        <div>
          <p style="font-weight:700;font-size:var(--text-sm);color:var(--accent);margin-bottom:var(--s1);">🧊 Mild</p>
          <p style="font-size:0.8rem;color:var(--text-2);margin:0;line-height:1.5;">"I only have 5 minutes. Just take my brain dump and tell me: what's the ONE thing I must do first thing Monday morning?"</p>
        </div>
        <div>
          <p style="font-weight:700;font-size:var(--text-sm);color:var(--accent);margin-bottom:var(--s1);">💰 Budget</p>
          <p style="font-size:0.8rem;color:var(--text-2);margin:0;line-height:1.5;">"Give me a simple weekly review template — 5 questions I can answer in writing every Friday in under 10 minutes."</p>
        </div>
      </div>
    </div>
  </div>
</details>

<!-- ==============================
     RECIPE: REVERSE BRAINSTORM (KILL YOUR IDEA)
     ============================== -->
<details id="reverse-brainstorm" class="recipe-card" style="margin-bottom: var(--s10);">
  <summary class="recipe-card-header">
    <div>
      <span class="recipe-tag">Ideation</span>
      <h3 style="margin-top: var(--s2);">Reverse Brainstorm — Kill Your Idea First</h3>
    </div>
    <span class="recipe-chevron" aria-hidden="true">▾</span>
  </summary>
  <div class="recipe-card-body">
    <div class="recipe-meta">
      <span>🎯 Goal: Find the real weaknesses in an idea by actively trying to destroy it</span>
      <span>📊 Difficulty: Sous Chef</span>
      <span>🤖 Best for: Claude, ChatGPT</span>
    </div>
    <p>Classic brainstorming asks "how could this work?" Reverse brainstorming asks "how could this spectacularly fail?" It's a lateral thinking technique used by product teams and strategists to surface hidden risks. The ideas that survive this process are genuinely stronger.</p>

    <div class="recipe-section-label">Ingredients</div>
    <ul style="font-size: var(--text-sm); color: var(--text-2);">
      <li><strong>[YOUR IDEA OR PLAN]</strong> — the thing you want to stress-test</li>
      <li><strong>[CONTEXT]</strong> — who's involved, what stage it's at, what's at stake</li>
    </ul>

    <div class="recipe-section-label">The Recipe</div>
    <div class="prompt-block"><pre>I have an idea I want to stress-test using reverse brainstorming.

The idea: [DESCRIBE YOUR IDEA OR PLAN]
Context: [STAGE, WHO'S INVOLVED, WHAT'S AT STAKE]

Phase 1 — Kill it.
Give me 10 specific ways this idea could fail. Not generic risks — specific, realistic failure modes for this exact idea. Include failures from: execution, market/audience, timing, the team, assumptions that might be wrong, and things outside my control.

Phase 2 — Flip it.
For the 3 most likely or most damaging failure modes, tell me: what would I need to do to prevent or mitigate each one? What's the signal that each one is happening, and how early would I see it?

Phase 3 — Verdict.
Given everything above, does this idea look stronger or weaker than before? What's the single most important thing I should validate before committing resources to this?</pre></div>

    <div class="recipe-section-label">Example — New SaaS product idea</div>
    <div class="prompt-block"><pre>I have an idea I want to stress-test using reverse brainstorming.

The idea: A subscription tool ($29/month) that helps solo freelancers track their income, send invoices, and automatically set aside the right amount for taxes each month — connected to their bank account.
Context: I'm a solo developer who's been freelancing for 3 years. I'd build this myself on weekends. I already use something like this manually in spreadsheets and find it painful.

Phase 1 — Kill it. Give me 10 specific ways this idea could fail. Include failures from execution, market, timing, assumptions, and competition.

Phase 2 — Flip it. For the 3 most dangerous failure modes, what would prevent or mitigate each one? What's the early signal?

Phase 3 — Verdict. Does this look stronger or weaker after the analysis? What's the single most important thing to validate before writing a line of code?</pre></div>

    <div class="callout callout-tip">
      <span class="callout-icon">💡</span>
      <div class="callout-body">
        <h4>Why killing your idea makes it stronger</h4>
        <p>The goal isn't to talk yourself out of it — it's to find the failure modes early, when they're cheap to fix. An idea that survives a rigorous reverse brainstorm is one you can commit to with confidence. An idea that falls apart under questions was going to fail anyway — better to find out now.</p>
      </div>
    </div>

    <div style="margin-top:var(--s5);padding:var(--s4) var(--s5);background:var(--bg-alt);border:1px solid var(--border);border-radius:var(--r3);">
      <div class="recipe-section-label" style="margin-bottom:var(--s3);">🔁 Leftover Remixes</div>
      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:var(--s4);">
        <div>
          <p style="font-weight:700;font-size:var(--text-sm);color:var(--accent);margin-bottom:var(--s1);">🌶️ Spicy</p>
          <p style="font-size:0.8rem;color:var(--text-2);margin:0;line-height:1.5;">After Phase 3: "Now give me the version of this idea that survives all these failure modes — the modified, battle-hardened version I should actually build."</p>
        </div>
        <div>
          <p style="font-weight:700;font-size:var(--text-sm);color:var(--accent);margin-bottom:var(--s1);">🧊 Mild</p>
          <p style="font-size:0.8rem;color:var(--text-2);margin:0;line-height:1.5;">Just Phase 1: "Give me 5 realistic failure modes for this idea. That's all I need right now."</p>
        </div>
        <div>
          <p style="font-weight:700;font-size:var(--text-sm);color:var(--accent);margin-bottom:var(--s1);">💰 Budget</p>
          <p style="font-size:0.8rem;color:var(--text-2);margin:0;line-height:1.5;">"What's the smallest, cheapest experiment I could run in the next 2 weeks to validate or kill the riskiest assumption in this idea?"</p>
        </div>
      </div>
    </div>
  </div>
</details>

'''

# Insert new recipes before the bottom CTA div
CTA_ANCHOR = '<div style="background: var(--accent-light); border: 1px solid var(--accent-border)'
if CTA_ANCHOR in html:
    html = html.replace(CTA_ANCHOR, NEW_RECIPES + CTA_ANCHOR, 1)
    print('\nOK Inserted 8 new recipe cards')
else:
    print('\nWARNING: Could not find CTA anchor — new recipes not inserted', file=sys.stderr)

# ─────────────────────────────────────────────
# 3. Update Table of Contents
# ─────────────────────────────────────────────

OLD_TOC = '''  <div class="toc" style="max-width: 680px; margin-bottom: var(--s10);">
  <h4>Jump to a recipe</h4>
  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0 var(--s6);">
    <ol style="margin: 0; padding-left: var(--s5);">
      <li><a href="#research-plan">Research → Plan → Implement</a></li>
      <li><a href="#teach-me">Teach Me Like I'm [level]</a></li>
      <li><a href="#devils-advocate">Devil's Advocate / Steelman</a></li>
      <li><a href="#step-by-step">Step-by-Step Breakdown</a></li>
      <li><a href="#summarize">Summarize for [Audience]</a></li>
      <li><a href="#draft-critique-revise">Draft → Critique → Revise Loop</a></li>
      <li><a href="#act-as">Act as [Expert]</a></li>
      <li><a href="#rubber-duck">Rubber Duck Debugging</a></li>
      <li><a href="#chain-prompts">Chain of Thought</a></li>
    </ol>
    <ol start="10" style="margin: 0; padding-left: var(--s5);">
      <li><a href="#constraints">Constraints &amp; Guardrails</a></li>
      <li><a href="#compare-options">Compare My Options</a></li>
      <li><a href="#iterative-refine">Iterative Refinement</a></li>
      <li><a href="#meeting-notes">Meeting Notes Cleaner</a></li>
      <li><a href="#code-review">Code Review Partner</a></li>
      <li><a href="#interview-prep">Interview Prep Coach</a></li>
      <li><a href="#reframe">Reframe the Problem</a></li>
      <li><a href="#tone-shift">Tone Shift</a></li>
      <li><a href="#gap-finder">Gap Finder</a></li>
    </ol>
  </div>
  <p style="font-size: var(--text-xs); color: var(--text-3); margin: var(--s4) 0 0;">New to AI? <a href="#beginner">Start here first →</a></p>
</div>'''

NEW_TOC = '''  <div class="toc" style="max-width: 680px; margin-bottom: var(--s10);">
  <h4>Jump to a recipe</h4>
  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0 var(--s6);">
    <ol style="margin: 0; padding-left: var(--s5);">
      <li><a href="#research-plan">Research → Plan → Implement</a></li>
      <li><a href="#teach-me">Teach Me Like I'm [level]</a></li>
      <li><a href="#devils-advocate">Devil's Advocate / Steelman</a></li>
      <li><a href="#step-by-step">Step-by-Step Breakdown</a></li>
      <li><a href="#summarize">Summarize for [Audience]</a></li>
      <li><a href="#draft-critique-revise">Draft → Critique → Revise Loop</a></li>
      <li><a href="#act-as">Act as [Expert]</a></li>
      <li><a href="#rubber-duck">Rubber Duck Debugging</a></li>
      <li><a href="#chain-prompts">Chain of Thought</a></li>
      <li><a href="#constraints">Constraints &amp; Guardrails</a></li>
      <li><a href="#compare-options">Compare My Options</a></li>
      <li><a href="#iterative-refine">Iterative Refinement</a></li>
      <li><a href="#meeting-notes">Meeting Notes Cleaner</a></li>
    </ol>
    <ol start="14" style="margin: 0; padding-left: var(--s5);">
      <li><a href="#code-review">Code Review Partner</a></li>
      <li><a href="#interview-prep">Interview Prep Coach</a></li>
      <li><a href="#reframe">Reframe the Problem</a></li>
      <li><a href="#tone-shift">Tone Shift</a></li>
      <li><a href="#gap-finder">Gap Finder</a></li>
      <li><a href="#cold-email">Cold Email That Gets Replies ✨</a></li>
      <li><a href="#learn-skill">Learn Any Skill in 30 Days ✨</a></li>
      <li><a href="#content-repurpose">Content Repurposing Machine ✨</a></li>
      <li><a href="#meeting-followup">Post-Meeting Follow-Up Email ✨</a></li>
      <li><a href="#scene-starter">Scene Starter for Fiction ✨</a></li>
      <li><a href="#decision-1010">The 10-10-10 Decision Test ✨</a></li>
      <li><a href="#weekly-review">Weekly Review &amp; Reset ✨</a></li>
      <li><a href="#reverse-brainstorm">Reverse Brainstorm ✨</a></li>
    </ol>
  </div>
  <p style="font-size: var(--text-xs); color: var(--text-3); margin: var(--s4) 0 0;">New to AI? <a href="#beginner">Start here first →</a> &nbsp;·&nbsp; ✨ = new recipe</p>
</div>'''

if OLD_TOC in html:
    html = html.replace(OLD_TOC, NEW_TOC, 1)
    print('OK Updated Table of Contents')
else:
    print('WARNING: TOC anchor not found — TOC not updated', file=sys.stderr)

# ─────────────────────────────────────────────
# Write output
# ─────────────────────────────────────────────

with open(SRC, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'\nDone — wrote {SRC}')
