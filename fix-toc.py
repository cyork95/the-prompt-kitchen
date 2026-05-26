# -*- coding: utf-8 -*-
import re

SRC = 'prompts/index.html'
with open(SRC, encoding='utf-8') as f:
    html = f.read()

# Replace entire TOC block from the opening div to its closing </div>
# The TOC starts with <div class="toc" and we know it ends before the what-is-a-prompt section
OLD = '''<div class="toc" style="max-width: 680px; margin-bottom: var(--s10);">
  <h4>Jump to a recipe</h4>
  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0 var(--s6);">
    <ol style="margin: 0; padding-left: var(--s5);">
      <li><a href="#research-plan">Research &#8594; Plan &#8594; Implement</a></li>
      <li><a href="#teach-me">Teach Me Like I\'m [level]</a></li>
      <li><a href="#devils-advocate">Devil\'s Advocate / Steelman</a></li>
      <li><a href="#step-by-step">Step-by-Step Breakdown</a></li>
      <li><a href="#summarize">Summarize for [Audience]</a></li>
      <li><a href="#draft-critique-revise">Draft &#8594; Critique &#8594; Revise Loop</a></li>
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
  <p style="font-size: var(--text-xs); color: var(--text-3); margin: var(--s4) 0 0;">New to AI? <a href="#beginner">Start here first &#8594;</a></p>
</div>'''

NEW = '''<div class="toc" style="max-width: 680px; margin-bottom: var(--s10);">
  <h4>Jump to a recipe</h4>
  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0 var(--s6);">
    <ol style="margin: 0; padding-left: var(--s5);">
      <li><a href="#research-plan">Research &#8594; Plan &#8594; Implement</a></li>
      <li><a href="#teach-me">Teach Me Like I\'m [level]</a></li>
      <li><a href="#devils-advocate">Devil\'s Advocate / Steelman</a></li>
      <li><a href="#step-by-step">Step-by-Step Breakdown</a></li>
      <li><a href="#summarize">Summarize for [Audience]</a></li>
      <li><a href="#draft-critique-revise">Draft &#8594; Critique &#8594; Revise Loop</a></li>
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
      <li><a href="#cold-email">Cold Email That Gets Replies &#10024;</a></li>
      <li><a href="#learn-skill">Learn Any Skill in 30 Days &#10024;</a></li>
      <li><a href="#content-repurpose">Content Repurposing Machine &#10024;</a></li>
      <li><a href="#meeting-followup">Post-Meeting Follow-Up Email &#10024;</a></li>
      <li><a href="#scene-starter">Scene Starter for Fiction &#10024;</a></li>
      <li><a href="#decision-1010">10-10-10 Decision Test &#10024;</a></li>
      <li><a href="#weekly-review">Weekly Review &amp; Reset &#10024;</a></li>
      <li><a href="#reverse-brainstorm">Reverse Brainstorm &#10024;</a></li>
    </ol>
  </div>
  <p style="font-size: var(--text-xs); color: var(--text-3); margin: var(--s4) 0 0;">New to AI? <a href="#beginner">Start here first &#8594;</a> &nbsp;&middot;&nbsp; &#10024; = new recipe</p>
</div>'''

# Use regex to find the actual TOC block (handles arrow encoding variants)
pattern = r'<div class="toc"[^>]*>.*?</div>\s*\n'
# Actually just do a direct find with the exact text from the file
if OLD in html:
    html = html.replace(OLD, NEW, 1)
    print('TOC replaced via direct match')
else:
    # Try to find using just the unique inner content
    # Find by the research-plan href which is unique to the TOC
    toc_start = html.find('<div class="toc"')
    toc_end = html.find('</div>', toc_start)
    # Find the closing </div> that closes the outer toc div
    # The toc has nested divs so find the right closing one
    depth = 0
    i = toc_start
    while i < len(html):
        if html[i:i+4] == '<div':
            depth += 1
        elif html[i:i+6] == '</div>':
            depth -= 1
            if depth == 0:
                toc_end = i + 6
                break
        i += 1

    old_toc = html[toc_start:toc_end]
    print('Found TOC block:')
    print(repr(old_toc[:200]))
    html = html[:toc_start] + NEW + html[toc_end:]
    print('TOC replaced via position search')

with open(SRC, 'w', encoding='utf-8') as f:
    f.write(html)
print('Done.')
