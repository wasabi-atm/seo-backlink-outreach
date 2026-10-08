import json, csv, re, os
B = '/home/claude/seo-backlink-outreach/form-outreach/batches/2026-10-08'
res = json.load(open(B + '/work/merged.json'))
keep = json.load(open(B + '/work/keep.json'))
OUT = json.load(open(B + '/work/review_out.json'))
DR = {"forumone.com":63,"act-on.com":75,"matchstic.com":51,"projectmanager.com":78,"getcanopy.com":71,"kustomer.com":79,"nivoda.com":55,"iamproperty.com":51,"honchosearch.com":43,"modo25.com":54,"instanda.com":48,"tealium.com":81,"aprimo.com":72,"deposco.com":67,"litera.com":74,"filtered.com":66,"ecommpay.com":62,"pragencyone.co.uk":42,"hive.hr":52,"trainual.com":73,"simpplr.com":71,"foundershield.com":59,"bol-agency.com":53,"poqcommerce.com":58,"hookagency.com":74,"fahrenheitmarketing.com":48,"thisisgain.com":74,"turtl.co":80}

# (kind, hook, offer/section, subject)  kind: Q = quote swap, F = free offer
M = {
 'forumone.com': ('Q', 'There are no charts in the body, and under "1. Is this the best use of our budget?" you argue a static visualisation "can be just as impactful" as an interactive tool.', 'the "1. Is this the best use of our budget?" section'),
 'matchstic.com': ('Q', 'Under "Skills equip your marketers" the skill file examples cover presentations, social posts and illustration. Motion and video guidelines never come up in the piece.', 'the "Skills equip your marketers" section'),
 'getcanopy.com': ('Q', 'Small thing, but the opening paragraph appears twice in a row. The drop "from ~50K to ~15K monthly visits" is also told in text only, with no chart.', 'the "5. Weave in Your Personal Expertise and Experience" section'),
 'act-on.com': ('Q', 'Under "Production demonstrations" you suggest showing how the product works "using video or another interactive method", and the post itself only has the one buyer\'s journey graphic.', 'the "Production demonstrations" section'),
 'projectmanager.com': ('Q', 'Under "Content Marketing Action Plan" the task list runs through research, writing, design and distribution, and the post has Gantt and template screenshots but no video.', 'the "Content Marketing Action Plan" section'),
 'foundershield.com': ('Q', 'The TikTok example under "How Copyright Missteps Turn Into High-Cost Brand Exposure" turns on one unlicensed audio track, with damages of up to $150,000 per infringement.', 'the "Operational Tips for Minimizing Risk While Maximizing Engagement" section'),
 'kustomer.com': ('Q', 'Small thing, but the mascot is "Kusty" in the first paragraph under "A new modern, flexible, and fun Kustomer logo" and "Kusti" in the next one.', 'the "The Design Fundamentals" section'),
 'iamproperty.com': ('F', 'Section 4, "Promoting property developments", suggests a development page with "a gallery of images", and none of the five ways mentions video.', 'make a short animated development teaser for that section'),
 'nivoda.com': ('Q', '"Build Visibility and Trust Through Social Media" calls Instagram, Facebook and Pinterest "highly visual and discovery-driven", but video and Reels don\'t come up.', 'the "Build Visibility and Trust Through Social Media" section'),
 'honchosearch.com': ('Q', 'The thought leadership section quotes the Edelman LinkedIn report, but it doesn\'t say which formats carry that thought leadership, video included.', 'the "Thought leadership is doing more commercial work than it used to" section'),
 'instanda.com': ('F', 'The date on the page reads "01 07, 2026", and "AI at Two Levels Simultaneously" explains the Foundational and Catalyst levels in text only.', 'design a simple two level diagram for that section'),
 'modo25.com': ('Q', 'The page still shows "Updated 31st Mar, 2022", and under "Keep your videos short and sweet" the 8 second attention span line has no source.', 'the "Keep your videos short and sweet" section'),
 'aprimo.com': ('Q', '"Implement Role-Based Onboarding" says to demonstrate the workflow each role uses most, step by step, and the guide has no walkthrough video of its own.', 'the "Implement Role-Based Onboarding" section'),
 'tealium.com': ('Q', 'The first heading still reads "Drinking our own [insert favorite sweetened drink here].", which looks like a placeholder that was left in.', 'the "This is not just a Tealium.com solution" section'),
 'deposco.com': ('F', 'It invites readers to "Watch Loose Threads unravel day by day", but on this page the story has one image and no video.', 'make a short animated recap of the Loose Threads story for the "Why we told it as a story" section', 'loose threads in your viral brand story'),
 'litera.com': ('F', 'Under "Optimize Your Website Marketing" you praise BD&P for its "various videos", but the guide has none of its own, and the title still says 2025.', 'make a short animated explainer for that section'),
 'filtered.com': ('F', 'The byline says "by Paul" while the first heading credits Toby Harris and Chris Littlewood. The £870k saving is also explained in text only, under "How did we work this out?"', 'make a simple graphic of the two steps in that section'),
 'ecommpay.com': ('F', 'Under "The rise of social commerce" a sentence ends with "please consider the scheme below:", and the post still forecasts the market "By 2025".', 'redraw that scheme as a clean graphic'),
 'hive.hr': ('F', 'It tells readers to share updates "via video, or include images and infographics", but the page has no video and still shows 9th November 2021.', 'make a short animated explainer for the "Videos and podcasts" section'),
 'pragencyone.co.uk': ('Q', 'Emily McGowan-Phoenix uses the new Strictly Come Dancing line-up as the case study, and the piece runs to about 1,300 words with no images in the body.', 'the "How to communicate continuity and change honestly" section', 'a quote for your heritage brands piece?'),
 'trainual.com': ('Q', 'The stat that people are "75% more likely to watch training videos" links to the Forrester homepage rather than the study, and the page still shows July 8, 2021.', 'the "The devil is in the details" section'),
 'simpplr.com': ('F', '"10. Onboarding center" recommends videos for new hires, but the 34 minute read embeds none. "Top 13 types of internal communication software" also lists products rather than types.', 'make a short animated explainer for the "10. Onboarding center" section'),
 'poqcommerce.com': ('F', 'The heading "The four asymmetries between TikTok and your app" goes straight into "The retention maths", so the four asymmetries don\'t show on the page.', 'design a graphic of the four asymmetries for that section'),
 'bol-agency.com': ('Q', 'Ingredient 2 says "motion can demonstrate them in seconds" and suggests a short animation of a complex process, but the post has no animation of its own.', 'the "Ingredient 2: Motion That Guides Attention and Explains Complexity" section'),
 'fahrenheitmarketing.com': ('Q', 'Under "How to Optimize E-E-A-T for LLMs" you say every piece needs a verified author bio, and the byline on this one just reads "FAHRENHEIT".', 'the "How to Optimize E-E-A-T for LLMs" section'),
 'hookagency.com': ('Q', 'It is about 2,500 words on real photos versus stock, and video doesn\'t come up once, even under "Photos That Show Who You Are".', 'the "Photos That Show Who You Are" section'),
 'vertical-leap.uk': ('Q', 'Under "How to Fix a Fatigued Ad" you suggest turning a static image into a motion graphic, but the post has no motion example to show it.', 'the "How to Fix a Fatigued Ad" section'),
 'turtl.co': ('Q', 'The modular content section suggests cutting one video interview into short clips, but the post has no video. The takeaway also mentions three avenues while the title says four.', 'the "What is modular content and why does it distribute better?" section'),
}
TITLE_FIX = {'hookagency.com': 'Why Stock Photos Are Costing Contractors Jobs (And What To Use Instead)'}
NAME_FIX = {'vertical-leap.uk': ('GAIN', 'thisisgain.com'), 'bol-agency.com': ('BOL Agency', 'bol-agency.com'), 'hive.hr': ('Hive', 'hive.hr'), 'poqcommerce.com': ('Poq', 'poqcommerce.com')}

def msg(d, r):
    kind, hook, off = M[d][:3]
    name = NAME_FIX.get(d, (r['companyName'], d))[0]
    title = TITLE_FIX.get(d, r['articleTitle']).replace('’', "'")
    p = [f'Hey {name} team,', f'Just read your piece "{title}" ({r["articleUrl"]}). {hook}']
    if kind == 'Q':
        p.append(f'I run a motion studio. Happy to swap founder quotes: one from me for {off}, and one from you for ours.')
        p.append('In return, a credit link back to motiontheagency.com with my quote, and one to yours with your quote on ours, or we\'ll pay for placement instead.')
    else:
        p.append(f'I run a motion studio. Happy to {off}, free.')
        p.append('In return, just a credit link back to motiontheagency.com, or we\'ll pay for placement instead.')
    p.append('Would you be open to exploring this?')
    p.append('Cheers,\nSam\nFounder @ Motion The Agency')
    return '\n\n'.join(p)

def before(r):
    parts = []
    if r.get('formSteps'): parts.append(r['formSteps'].rstrip('.'))
    ex = r.get('requiredExtras', '')
    fs = r.get('formSteps', '').lower()
    for e in [x.strip() for x in ex.rstrip('.').split(';') if x.strip()]:
        v = e.split(':', 1)[-1].strip().lower()
        if ':' in e and v and v in fs: continue
        if 'consent box' in e.lower() and r.get('consentBox') == 'requiredTerms': continue
        parts.append(e)
    cap = r.get('captcha', 'none')
    if cap == 'recaptchaCheckbox': parts.append('Tick the reCAPTCHA box')
    elif cap == 'hcaptcha': parts.append('Complete the hCaptcha check')
    elif cap == 'turnstile': parts.append('Wait for the Cloudflare check to pass')
    if r.get('consentBox') == 'requiredTerms': parts.append('Tick the required consent box')
    parts = [x + ': pick Indonesia' if x.strip() == 'Country dropdown' else x for x in parts]
    s = '; '.join(parts) or 'Nothing extra'
    s = s.replace("pick sender's country", 'pick Indonesia').replace('pick our country', 'pick Indonesia').replace('Phone required', 'Phone is required: +44 2039847787').replace('Subject required', 'Subject is required: use the subject below').replace('Terms of use box required; Tick the required consent box', 'Tick the required terms box')
    return s

rows6, rows3, master = [], [], []
for d in keep:
    r = res[d]
    name, dom = NAME_FIX.get(d, (r['companyName'], d))
    m = msg(d, r)
    subj = M[d][3] if len(M[d]) > 3 and r.get('hasSubjectField') == 'yes' else ''
    kind = M[d][0]
    seg = r['segment']
    offer = "Founder's quote swap" if kind == 'Q' else r.get('offerSuggestion', '')
    rows6.append(dict(companyName=name, formUrl=r['formUrl'], beforeSubmit=before(r), subjectText=subj, messageText=m))
    rows3.append(dict(companyName=name, webDomain=dom, domainRating=DR[dom], drSource='Apify ahrefs-scraper', drDate='2026-10-08', country=r['country'], segment=seg, offer=offer,
                      formUrl=r['formUrl'], formSteps=r.get('formSteps', ''), articleTitle=TITLE_FIX.get(d, r['articleTitle']), articleUrl=r['articleUrl'], articleTopic=r.get('articleTopic', ''),
                      linkPlacement=r.get('linkPlacement', ''), articleHook=M[d][1], captcha=r.get('captcha', ''), consentBox=r.get('consentBox', '')))
    lim = r.get('messageMaxChars')
    n = len(m); bad = [c for c in m if c in '—–']
    flag = ''
    try:
        if lim and n > int(lim): flag = f'OVER LIMIT {lim}'
    except: pass
    print(f'{name:28} words={len(m.split()):3} chars={n:4} dashes={len(bad)} {flag}')

def w(fn, rows, fields=None):
    fields = fields or list(rows[0].keys())
    with open(os.path.join(B, fn), 'w', newline='', encoding='utf-8') as f:
        x = csv.DictWriter(f, fieldnames=fields); x.writeheader(); x.writerows(rows)
w('06_form_outreach.csv', rows6)
w('03_form_targets.csv', rows3)

# 02_forms.csv: every researched site
cand = {}
for fn in ('00_candidates_clean.csv', '00_candidates_round2_clean.csv'):
    for c in csv.DictReader(open(os.path.join(B, fn))): cand[c['webDomain']] = c
f2 = []
for d, r in res.items():
    fit = 'skip' if r['verdict'] != 'pass' else ('good' if d in keep else 'skip')
    reason = r.get('skipReason', '') if r['verdict'] != 'pass' else (OUT.get(d, 'Passed form and article checks'))
    f2.append(dict(companyName=r['companyName'], webDomain=d, country=r.get('country', ''), segment=r.get('segment', ''), source=cand.get(d, {}).get('source', ''), formUrl=r.get('formUrl', ''),
                   formPurpose=r.get('formPurpose', ''), formFields=r.get('formFields', ''), hasSubjectField=r.get('hasSubjectField', ''), captcha=r.get('captcha', ''), consentBox=r.get('consentBox', ''),
                   altEmail=r.get('altEmail', ''), fit=fit, fitReason=reason))
w('02_forms.csv', f2)
# 07_left_out.csv
lo = []
for d, r in res.items():
    if d in keep: continue
    reason = OUT.get(d) or r.get('skipReason', '')
    if r.get('competitor') == 'yes': reason = 'Competitor (makes video or motion for clients). ' + reason
    reason = re.sub(r'\s+', ' ', reason.replace('—', ',').replace('–', ',')).strip()
    if len(reason) > 170: reason = reason[:167].rsplit(' ', 1)[0] + '...'
    lo.append(dict(companyName=r['companyName'], webDomain=d, reason=reason))
w('07_left_out.csv', lo)
with open(os.path.join(B, '02_low_dr.csv'), 'w') as f: f.write('companyName,webDomain,domainRating,drSource,drDate\n')
print(len(rows6), 'forms;', len(lo), 'left out;', len(res), 'researched')
