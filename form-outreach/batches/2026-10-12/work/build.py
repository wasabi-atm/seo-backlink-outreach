import json, csv, re
B = '/home/claude/seo-backlink-outreach/form-outreach/batches/2026-10-12'
rows = json.load(open(B + '/work/merged.json'))
sel = json.load(open(B + '/work/selected.json'))
DRF = json.load(open(B + '/work/dr_final.json'))
DR, ALIAS = DRF['dr'], DRF['alias']

# domain: (name for greeting/company, kind Q=quote swap / F=free offer, hook, section-or-offer, subject or None)
M = {
 'constructor.io': ('Constructor', 'F', 'Your "No-code visual merchandising" section explains pinning, boosting and burying items in words only, and further down you say video helps "boosting customer confidence in their purchase".', 'make a short animated walkthrough for the "No-code visual merchandising" section'),
 'monsterinsights.com': ('MonsterInsights', 'Q', 'Section 8 says a video "can also explain a step that\'s hard to follow in writing", but that section has no example of its own. The only video is the tutorial at the very end.', 'the "8. Add Videos to Your Pages" section'),
 'ebiquity.com': ('Ebiquity', 'Q', 'The whole case rests on one number, online at just 10% of UK food sales, and the four measurement techniques that follow are all text with no chart.', 'the "Four Techniques That Actually Work" section'),
 'prosek.com': ('Prosek', 'Q', 'Small thing, but the tips list has "Groc" for Grok, and the last line reads "If Malcom Gladwell were writing Blinkin 2025".', 'the "Offense is the best defense" tip'),
 'onlineoptimism.com': ('Online Optimism', 'Q', 'Section 2 sums up TikTok as "short, entertaining videos with an immediate hook" and YouTube as longer storytelling, but the post doesn\'t show a video of either.', 'the "Understand the Essence and Rules of Each Platform" section'),
 'jwplayer.com': ('JWX', 'Q', 'You make the point that a Reel, a Short and a Threads post "are not interchangeable executions of the same idea", and the post itself only has a header image.', 'the "What Effective Distribution Actually Requires" section'),
 'browsermedia.agency': ('Browser Media', 'Q', 'Under "Sweat the assets across your other marketing channels" you say a strong statistic "might make a great LinkedIn post", but the post never shows what one of those repurposed assets looks like.', 'the "Sweat the assets across your other marketing channels" section'),
 'whitespace.agency': ('White Space', 'Q', '"Align visuals with copy" wants images that back up the message, and step 3 warns against heavy background video. Light motion sits right between the two and the post skips it.', 'the "Align visuals with copy" section'),
 'triplewhale.com': ('Triple Whale', 'Q', 'Small thing, but the contents list jumps from 4 to "6. Improve abandonment campaigns with Sonar Send", because step 5 on loyalty rewards isn\'t set as a heading.', 'the "4. Build win-back campaigns around purchase timing" section'),
 'mcgaw.io': ('McGaw', 'Q', 'The five layers and the four week rollout plan run to about 3,300 words with a single image, so the stack itself is never drawn out.', 'the "The 5-Layer Marketing Attribution Stack Marketing Ops Can Own" section'),
 'system1group.com': ('System1', 'Q', 'The Jaffa Cakes poster scoring 88% on Fast Fluency is a neat proof that the 60/30/10 rule carries over from web design to billboards.', 'the "Enter The 60/30/10 Rule." section'),
 'oneupweb.com': ('Oneupweb', 'Q', 'The examples under "3. Define Deliverables (and Intangibles)" cover social media and a new website but never video, and the page has no images at all.', 'the "3. Define Deliverables (and Intangibles)" section'),
 'terakeet.com': ('Terakeet', 'Q', 'Section 5 on video and webinars still quotes what B2B marketers planned to spend on video in 2022, even though the guide was updated this July.', 'the "5. Use video and webinars for B2B content marketing" section'),
 'listrak.com': ('Listrak', 'Q', 'The intro follows a shopper who opens an email on Monday, gets a back in stock text on Wednesday and buys on Friday, but that path is only told in text.', 'the "Building the Cross-Channel View" section'),
 'bruceclay.com': ('Bruce Clay', 'Q', 'The "3. Video Content" section leans on Wyzowl\'s 2024 video stats, while the post was updated in August 2026.', 'the "3. Video Content" section'),
 'lform.com': ('Lform', 'Q', 'The Capabilities and Case Studies sections tell manufacturers to show their work, but the post has no video or process graphic, and 6 of its 7 images have no alt text.', 'the "Case Studies" section'),
 'digitalauthority.me': ('Digital Authority Partners', 'Q', 'You list "Videos: Walk patients through procedures or conditions" as a content type that earns trust, and the page itself has no video.', 'the "Types of Healthcare Content That Earn Patient Trust" section'),
 'emulent.com': ('Emulent', 'Q', 'The title promises a diagram, but the five numbered steps are all text with no images. Step 04 has the best line in it too: roughly 85 percent of retrieved pages are never cited.', 'the "Cut most of them: retrieval is not citation" section'),
 'rainfocus.com': ('RainFocus', 'Q', 'The opening line puts average registration abandonment at around 33% with no source, and the post has no images or video.', 'the "What to Do When Attendees Abandon Their Cart" section'),
 'artversion.com': ('ArtVersion', 'Q', '"Interface Behavior as Brand Behavior" says even the speed of a transition is a brand decision, and the 1,300 words don\'t show a single motion example.', 'the "Interface Behavior as Brand Behavior" section'),
 'anvilmediainc.com': ('Anvil Media', 'Q', 'You say buyers judge visuals "before a headline, before a price", and the quick audit asks four good questions about photos, but video and motion never come up.', 'the "What Does a Year of Intentional Photography Look Like?" section'),
 'lullabot.com': ('Lullabot', 'Q', 'The four 2025 shifts and five predictions, design systems included, are all in text with no visuals beyond the author photo.', 'the "The acceleration of design systems" section'),
 'steerpoint.com': ('SteerPoint', 'Q', 'The social proof section lists reviews, photos, awards and logos, but not video testimonials.', 'that section'),
 'gumgum.com': ('GumGum', 'Q', 'Rob Auger\'s point that years of optimisation have flattened brands creatively is a good one, and the post on memorable CTV has no ad example on the page.', 'the "Create CTV Experiences People Will Never Forget" section'),
 'improvado.io': ('Improvado', 'Q', '"Reasons to Run Facebook Video Ads" still lists Periscope, which closed in 2021, and a post about video ads has no video on the page.', 'the "Reasons to Run Facebook Video Ads" section', ),
 'vistasocial.com': ('Vista Social', 'Q', '"Match the format to the job" says video earns its place when motion or demonstration helps the explanation, and the post has no video example of its own.', 'the "Match the format to the job" section', 'video in your linkedin algorithm post'),
 'highwirepr.com': ('Highwire', 'Q', 'Step 3 says "Videos are the most popular form of social media right now", but the guide has one image, and the steps heading reads "Brand Strategy" rather than brand launch.', 'the "3. Develop A Comms Plan" section'),
 'pimberly.com': ('Pimberly', 'F', 'The "Include immersive digital assets" section recommends explainer videos to show use cases, but the post itself has two images and no video.', 'make a short animated explainer for the "Include immersive digital assets" section'),
 'socialpilot.co': ('SocialPilot', 'Q', 'Section 3 still points readers to creators for "YouTube and Vine", and Vine closed years before the July 2026 update.', 'the "3. Who will develop your video content?" section'),
 'dsmn8.com': ('DSMN8', 'Q', 'The intro asks "Is video really essential on LinkedIn?", and none of the ten experts actually makes video for a living.', 'the "Start With the Outcome, Not the Format" section'),
 'blastmedia.com': ('PANBlast', 'Q', 'The Edutainment section says short form video is eating search traffic and long form YouTube is coming back, and the post has no video or images at all.', 'the "Edutainment" section'),
 'rocketagency.com.au': ('Rocket Agency', 'Q', 'The checklist runs from "Hook fast or lose them" to "Blend short with long", and a post about short form video has no video in it.', 'the "How to do short-form really well" checklist'),
 'zibdigital.com.au': ('Zib Digital', 'Q', '"Video is vertical first" tells businesses to make video for TikTok, Shorts and Reels, and the page carries one image and no video.', 'the "Video is vertical first" section'),
 'marketingeye.com.au': ('Marketing Eye', 'Q', 'The repurposing tips suggest turning client stories into short video testimonials, but the post has no video. Small thing too: the H1 reads "the most power brand story".', 'the "Turning case studies into adaptable sales collateral" section'),
 'linqia.com': ('Linqia', 'Q', '"AEO Loves YouTube" says AI engines pick YouTube 200x more than any other video platform, and the post has no video of its own.', 'the "AEO Loves YouTube" section'),
 'plannthat.com': ('Plann', 'Q', 'The title promises an ultimate guide but covers four trends, and Trend 2 still frames the year around the TikTok ban.', 'the "Diversified Content Strategies" section'),
 'clickmatix.com.au': ('Clickmatix', 'Q', 'Step 12, "Creating the Video Ad Creative", covers pasting the video link and character limits, but nothing on making the ad itself.', 'the "Step 12: Creating the Video Ad Creative" section'),
 'hashmeta.com': ('Hashmeta', 'Q', 'Month 1 asks for explainer videos and a short form video in week 2, and the post doesn\'t show what either looks like.', 'the Month 1 "Attract" section'),
 'impossible.sg': ('Impossible', 'Q', 'The GEO section makes a good point that AI made video still needs clear on-screen text and accurate captions. Small thing: the Minis line reads "such mini dramas", missing an "as".', 'the "Connecting this to GEO for social search" section'),
 'ematicsolutions.com': ('Ematic', 'Q', '"Step 3: Show, Don\'t Tell" makes the case for showing, and the guide to short video ads has no example video of its own.', 'the "The Anatomy of an Ad That Clicks" section'),
 'rivaliq.com': ('Rival IQ', 'Q', 'The post on AI video is filed under "Uncategorized", and it compares the two with eight static images rather than any video.', 'the "Comparing AI-Generated Videos vs. Non-AI Content" section'),
 'playwire.com': ('Playwire', 'Q', 'The FAQ asks how to make video ads without a big budget for studio shoots, and the 2,500 word guide has no video of its own.', 'that FAQ'),
 'lickd.co': ('Lickd', 'Q', 'The byline still says August 4, 2021 though the page was updated in June 2026, and "6. Shapes" covers branded shape overlays in one short paragraph.', 'the "6. Shapes" section', 'the shapes section in your transitions post'),
 'localdigital.com.au': ('Local Digital', 'Q', 'You note 89% of marketers rate video as their best performing content, and the page has no video or images.', 'the "Content Marketing in Australia: Key Statistics for 2025" section'),
 'tribegroup.co': ('TRIBE', 'Q', 'It compares how one vertical video does on TikTok, Reels and Shorts, but there\'s no video on the page, only two stills. There\'s also an empty heading just before "The Next Creator Opportunity".', 'the "The Next Creator Opportunity" section'),
 'streem.com.au': ('Streem', 'Q', 'The post is dated May 2026, but its newest figures come from the Digital News Report: Australia 2024 and social stats from February 2024.', 'the "How Companies Should Adjust Their PR Strategies" section'),
 'digital8.com.au': ('Digital8', 'Q', 'The intro lists watching short form videos and finding a reel on Instagram as steps in the buyer journey, and the post has ten images but no video.', 'the "Social Media Builds Brand Awareness" section'),
 'moosend.com': ('Moosend', 'Q', 'The page was updated in August 2026, but the byline still says August 19, 2022, so the video advice can look four years old.', 'the "7. Share your story" section'),
 'clickclickmedia.com.au': ('Click Click Media', 'Q', '"Keeping Creative Ahead of Decay" says a UGC style video reads differently to a static ad, and the post only shows static images.', 'the "Keeping Creative Ahead of Decay" section'),
 'ionline.com.au': ('iOnline', 'Q', 'The title still says 2024 though the page was updated in August 2025, and "Highlight Your Video on the Page" has no video on the page.', 'the "Highlight Your Video on the Page" section'),
 'getvero.com': ('Vero', 'Q', 'Step 4 says to map the flow visually first because gaps are easier to spot in a diagram, and the post never shows one for its own six email sequence.', 'the "Step 4: Build the automation in your platform" section'),
 'verzdesign.com': ('Verz Design', 'Q', 'Section 2 says 75% of marketers now use AI for video and images, but it only covers images, scripts and captions, not what makes the video itself work.', 'the "2. AI Image and Video Creation" section'),
}

# extra steps for beforeSubmit (plain words). Default comes from formSteps + requiredExtras.
BEFORE = {
 'constructor.io': 'Scroll down to the partner form. Immediate client need: No. Nature of interest: Other. Job title: Founder. Company: Motion The Agency. Country: United Kingdom. Tick the terms box.',
 'monsterinsights.com': 'Use the "I have a basic question" form, not the support link. Website: motiontheagency.com',
 'ebiquity.com': 'Company: Motion The Agency. Country: United Kingdom. Organisation Type: Agency. Tick the reCAPTCHA if it shows.',
 'prosek.com': 'Nothing extra',
 'onlineoptimism.com': 'The message box is a single line, so paste the message as it is (line breaks may be lost). Leave the marketing box unticked.',
 'jwplayer.com': 'Click the "Other" tab above the form first. Company Name: Motion The Agency. Headquarters Region: Asia Pacific.',
 'browsermedia.agency': 'The form is in the footer panel at the bottom of the page.',
 'whitespace.agency': 'Tick the required consent box.',
 'triplewhale.com': '"I\'m Reaching Out About...": General Question (the message box appears after that). Agency or Brand: Agency.',
 'mcgaw.io': 'How did you hear about us: Your blog',
 'system1group.com': 'I\'m Interested In: Something Else. Company Type: Creative Agency. Industry: Professional Services. Company: Motion The Agency. Country: United Kingdom. How Did You Find Us: Article/News story. Tick the privacy box.',
 'oneupweb.com': 'Tick "Other" under "I\'d like to..." to show the "Drop us a note" box.',
 'terakeet.com': 'How did you hear about us: Your blog. Use /contact, not the /get-started sales form.',
 'listrak.com': 'This is the Become a Partner form (the contact page has no form). Phone: +44 2039847787. Company: Motion The Agency. Mutual clients: No. Leave retailer size blank.',
 'bruceclay.com': 'Phone: +44 2039847787. Company URL: https://motiontheagency.com. hCaptcha may ask you to tick a box. Do not use the /quoteform/ page.',
 'lform.com': 'Phone: +44 2039847787. Leave the service boxes unticked.',
 'digitalauthority.me': 'Phone: +44 2039847787.',
 'emulent.com': 'Website we will be discussing: motiontheagency.com',
 'rainfocus.com': 'Reason for request: Partnership. Company: Motion The Agency.',
 'artversion.com': 'Pick "General Inquiry" (not "Looking for a Quote"). Company: Motion The Agency. Phone: +44 2039847787. Tick the required email/SMS consent box.',
 'anvilmediainc.com': 'Nothing extra',
 'lullabot.com': 'Your organization: Motion The Agency. How you heard about us: Your articles.',
 'steerpoint.com': 'Phone: +44 2039847787. Company: Motion The Agency. Website: motiontheagency.com. Today\'s date field: type the date you submit. Message box is limited to 455 characters; the message below fits.',
 'gumgum.com': 'Who are you?: Other. Job title: Founder. Company: Motion The Agency. Country: pick from the full list. Leave the marketing box unticked.',
 'improvado.io': 'Scroll down to the partner form. Company: Motion The Agency. Leave Partnership type blank.',
 'vistasocial.com': 'Typeform, one question per screen. Team: Partnerships. Paste the subject below into the subject question.',
 'highwirepr.com': 'I Am: something else. Industry: Other. Company: Motion The Agency. Company Website: motiontheagency.com.',
 'pimberly.com': 'The form is under "Get in touch" on the contact page. Fill in name fields if they show.',
 'socialpilot.co': 'Nothing extra',
 'dsmn8.com': 'Job title: Founder. Leave the marketing box unticked.',
 'blastmedia.com': 'I\'m interested in: Other. Company: Motion The Agency. How did you hear about us: Google/Search Engine. Leave the marketing box unticked.',
 'rocketagency.com.au': 'Phone: +44 2039847787. How did you hear about us: Your blog.',
 'zibdigital.com.au': 'Last name: Jupp. Company: Motion The Agency. Phone: +44 2039847787.',
 'marketingeye.com.au': 'Company: Motion The Agency. Phone: +44 2039847787. Tick the reCAPTCHA box.',
 'linqia.com': 'Use this Partner Program form, not /contact-sales/ (that one asks for a budget). Last name: Jupp. Company: Motion The Agency.',
 'plannthat.com': 'Enquiry type: Guest Blogging (or Media Opportunities).',
 'clickmatix.com.au': 'Phone: +44 2039847787. Website: https://motiontheagency.com',
 'hashmeta.com': 'This is the Write For Us form at the bottom of the page. The required "links to 3 of your best articles" box: paste links to three posts from motiontheagency.com/blog.',
 'impossible.sg': 'Phone number: 442039847787 (numbers only).',
 'ematicsolutions.com': 'Click the "I want to explore potential partnership" tab first.',
 'rivaliq.com': 'Phone: +44 2039847787.',
 'playwire.com': 'Tick the communications consent box (marked required).',
 'lickd.co': 'Paste the subject below into the Subject field.',
 'localdigital.com.au': 'What do you need help with?: Partnerships.',
 'tribegroup.co': 'How can we help?: Other (or Press Enquiries). Region: Other. Company: Motion The Agency.',
 'streem.com.au': 'Last name: Jupp. Phone: +44 2039847787. Company Name: Motion The Agency. Leave the marketing box unticked.',
 'digital8.com.au': 'What digital services are you looking for?: Something else. Phone: +44 2039847787 if asked.',
 'moosend.com': 'This is the Write For Us form. Collaboration: General Marketing. Last name: Jupp. Company: Motion The Agency. Website: https://motiontheagency.com. Leave the marketing box unticked.',
 'clickclickmedia.com.au': 'Phone: +44 2039847787. Leave Urgency as it is.',
 'ionline.com.au': 'Type of Enquiry: General Enquiry. Phone: +44 2039847787. How did you hear about us: Your blog. Leave the marketing box unticked.',
 'getvero.com': 'This is the Partners form (the "Talk to us" form is for sales). Company: Motion The Agency.',
 'verzdesign.com': 'Phone: +44 2039847787. Leave the two dropdowns blank.',
}

CAPTCHA_NOTE = {'recaptchaCheckbox': 'Tick the reCAPTCHA box.', 'hcaptcha': 'hCaptcha may ask you to tick a box.'}

def message(d, r):
    name, kind, hook, off = M[d][:4]
    title = r['articleTitle'].replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')
    url = r['articleUrl']
    p = [f'Hey {name} team,', f'Just read your piece "{title}" ({url}). {hook}']
    if kind == 'Q':
        p.append(f'I run a motion studio. Happy to swap founder quotes: one from me for {off}, and one from you for ours.')
        p.append("In return, a credit link back to motiontheagency.com with my quote, and one to yours with your quote on ours, or we'll pay for placement instead.")
    else:
        p.append(f'I run a motion studio. Happy to {off}, free.')
        p.append("In return, just a credit link back to motiontheagency.com, or we'll pay for placement instead.")
    p.append('Would you be open to exploring this?')
    p.append('Cheers,\nSam\nFounder @ Motion The Agency')
    return '\n\n'.join(p)

def short_message(d, r):
    # for tight character limits: same template, title only (URL kept), shortest hook
    return message(d, r)

out6, out3, problems = [], [], []
for d in sel:
    r = rows[d]
    if d not in M: problems.append('no copy for ' + d); continue
    msg = message(d, r)
    lim = r.get('messageMaxChars')
    lim = int(lim) if str(lim).strip().isdigit() else None
    if lim and len(msg) > lim:
        problems.append(f'{d}: {len(msg)} chars > limit {lim}')
    if re.search('[–—]', msg + BEFORE.get(d, '')):
        problems.append(d + ': dash found')
    subj = M[d][4] if len(M[d]) > 4 else ''
    if r.get('hasSubjectField') == 'yes' and not subj: problems.append(d + ': needs subject')
    bs = BEFORE.get(d, 'Nothing extra')
    cn = CAPTCHA_NOTE.get(r.get('captcha', ''))
    if cn and cn not in bs: bs = (bs + ' ' + cn) if bs != 'Nothing extra' else cn
    out6.append({'companyName': M[d][0], 'formUrl': r['formUrl'], 'beforeSubmit': bs, 'subjectText': subj, 'messageText': msg})
    live = ALIAS.get(d, d)
    seg = r.get('segment') or 'A'
    offer = "Founder's quote swap" if M[d][1] == 'Q' else 'Video for the post'
    out3.append({'companyName': M[d][0], 'webDomain': d, 'domainRating': DR[live], 'drSource': 'Apify ahrefs-scraper', 'drDate': '2026-10-12',
                 'country': r.get('country', ''), 'segment': seg, 'offer': offer, 'formUrl': r['formUrl'], 'formSteps': r.get('formSteps', ''),
                 'articleTitle': r['articleTitle'], 'articleUrl': r['articleUrl'], 'articleTopic': r.get('articleTopic', ''),
                 'linkPlacement': r.get('linkPlacement', ''), 'articleHook': M[d][2], 'captcha': r.get('captcha', ''), 'consentBox': r.get('consentBox', ''),
                 'source': r.get('_src', ''), 'liveDomain': live if live != d else ''})
    print(f'{d:26} {len(msg):5} chars {len(msg.split()):4} words' + (f'  limit {lim}' if lim else ''))

for row in out3 + out6:
    for k, v in row.items():
        if isinstance(v, str) and re.search('[–—]', v):
            row[k] = re.sub(r'\s*[–—]\s*', ' - ' if k in ('articleTitle',) else ', ', v)
            problems.append(f'dash replaced in {k} of {row["companyName"]}')

print('ROWS', len(out6)); print('\n'.join(problems))
f6 = ['companyName', 'formUrl', 'beforeSubmit', 'subjectText', 'messageText']
w = csv.DictWriter(open(B + '/06_form_outreach.csv', 'w', newline=''), fieldnames=f6); w.writeheader(); w.writerows(out6)
f3 = list(out3[0].keys())
w = csv.DictWriter(open(B + '/03_form_targets.csv', 'w', newline=''), fieldnames=f3); w.writeheader(); w.writerows(out3)
