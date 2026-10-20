import json, csv, re
B = '/home/claude/seo-backlink-outreach/form-outreach/batches/2026-10-20/'
S = json.load(open(B + 'work/selected.json'))
DR = {}
for p in open(B + 'work/dr_apify.txt').read().split():
    d, v = p.split('='); DR[d] = int(v)
PH = '+44 2039847787'
DATE = '2026-10-20'

GREET = {'Podcast Page': 'Beamly', 'Stranger & Stranger': 'Stranger & Stranger', 'Stevens and Tate': 'Stevens & Tate',
         'Spark Business Works': 'SPARK', 'Carnegie Higher Ed': 'Carnegie', 'Pivotal Agency': 'Pivotal',
         'Upbeat Agency': 'Upbeat', 'Rosemont Media': 'Rosemont', 'Mindgruve': 'Mindgruve', 'Outloud Group': 'Outloud',
         'Idea Marketing': 'Idea Marketing', 'Elite Strategies': 'Elite Strategies'}

# Hooks: one or two specific, checkable things seen on the live page.
HOOK = {
 'Certain': 'It lists 20 formats in four groups, Product Demonstrations among them, but the page has a single image and no video of its own.',
 'Fast Simon': 'It opens with a 65% revenue surge and 20% higher conversion rates as plain text headings, with no chart or video to show those numbers.',
 'Visions Design': 'Small thing, but the byline says 12 June 2025 while the page data says 17 June, and the five numbered steps have no diagram or video.',
 'Prowess': 'The "Long-form explainers and tutorials" section recommends explainer video, but the guide itself has no video embedded.',
 'Klatch': 'The Background section says form abandonment is typically 80% to 85% in hospitality and up to 95% for travel, but there are no visuals showing the form change.',
 'Moncur': 'The intro says buyers spend 70% of their journey researching in stealth mode, and the awareness and consideration sections explain it all in text.',
 'Autymate': 'Section 5 is "Content Marketing and Education", but the post has no video of its own across its ten strategies.',
 'GWS Media': 'The "Bring that story to life" section is all about storytelling across channels, but the post has no video and only two images.',
 'Outloud Group': 'Small thing, but the browser tab says "How Brands Kill Their Own Influencer Campaigns" while the headline reads "Your Influencer Campaign May Have a Brand Problem".',
 '29 Design': 'It says "Social platforms are built for visuals" and has a "Higher Engagement Rates" section, but there is no video or animation among its examples.',
 'Bright Vessel': 'Small thing, but the page data has it modified a month before it was published.',
 'Enjoy Digital': 'The four red flags, like "The feedback silence" and "Journey hesitation", are all in text, and the maturity model has no video or walkthrough.',
 'TicToc Digital': 'Section 3 is "Show testimonials from service users", but the post has no video testimonial of its own, only still images.',
 'Fused': 'It has a section on "The AI-Generated Imagery Question" next to "Build an Image Library", yet the seven minute read has just one image in the body.',
 'AIP Media': 'The "From broad labels to better questions" section asks which platforms really capture attention, but the post has no visuals or examples of any platform.',
 'Pink Pine Media': 'The "Put real people forward" foundation says showing your team does more for trust than polished copy, but the post has no images or video of any people.',
 'Podcast Page': 'Step 3 suggests sharing video clips on Instagram, but the post has no clip embedded, even with the August 2026 update.',
 'Mailmunch': 'It is a full guide to video ads with a "Types of Video Ads" section, yet it has no video embedded and only three images.',
 'LeadDyno': 'Small thing, but the title promises 7 secrets while the section heading calls them 7 tips.',
 'Sites by Sara': 'It flags "Overuse of Stock Images" and "Slow-Loading Visuals" as mistakes, but the page has no video or animation of its own.',
 'Intrepy': 'Small thing, but the URL says 3 content marketing strategies while the page lists six, starting with "Invest in Video Content to Connect with Patients".',
 'Clearstream': 'The intro says you can record video without an expensive camera or team, and the "Tips for recording videos" section points to a $100 DIY lighting kit.',
 '829 Studios': 'The "YouTube SEO: 3 Pillars for Driving More Video Views" section says video optimisation is no longer optional, but the post has no video embedded.',
 '321 Web Marketing': 'Factor 3 in "Seven Factors That Affect AI Search Visibility" is "Add Information Competitors Can\'t Easily Repeat", yet the post has only static images and no video.',
 'Reach Marketing': 'The "Marketing to the Buying Committee Builds Broader Account Awareness" section describes a multichannel flow, but there is no visual showing how it fits together.',
 'Wired Impact': 'The "Film a Forward-Looking Interview" section recommends video, but the post has no video embedded, only five images.',
 'Pivotal Agency': 'The "Connecting Digital Efforts to Business Objectives" section ties ads, email and blog posts into one plan, but the post has no video or visuals of its own.',
 'Ironistic': 'The "Numbers to Know" box lists four stats, like 82% of consumers wanting a human agent, as plain text, with no chart or video.',
 'Rosemont Media': 'It mentions video 17 times and has an "Ideas for Captivating Content" section, but no video embedded and only one image.',
 'Upbeat Agency': 'It mentions video nine times, including in the "Organic content still matters" section, but the 3,800 word post has 23 images and no video.',
 'Idea Marketing': 'The "Testimonials & Case Studies That Show Real Outcomes" section is all text, and the post covers UGC and testimonials without a single video.',
 'My Dental Agency': 'The "Show, Don\'t Tell" section urges practices to show their work, but the post has no video embedded.',
 'Big Duck': 'Small thing, but the seven ways sit as bold lines inside the paragraphs rather than headings, so "Move from deficit- to asset-based storytelling" is easy to miss when skimming.',
 'Stevens and Tate': 'The "6 Elements of Effective Digital Storytelling" section walks through six steps, but the post has no video and only three images.',
 'nDash': 'The "Signs AI Is Blurring a Writer\'s Original Voice" section uses a sign and solution table, but the whole post has one image and no video or diagram.',
 'Influ2': 'The heading promises "13 ABM campaign ideas (with ad examples)", but the examples are described in text under each idea and the page has no video.',
 'Hannon Hill': 'Small thing, but the intro promises 3 short stories, and the page has a Prequel before Story #1 to Story #3, so it reads as four.',
 'Elite Strategies': 'Small thing, but the browser tab says "Content Pruning Case Study: The 2026 Agentic Version" while the headline reads "Content Cruft Cleanup Case Study".',
 'Ad Results Media': 'It argues podcast clips on TikTok, Reels and Shorts now drive discovery, but the page itself has no clip, image or video.',
 'Mindgruve': 'The whole post is about online video and has a section called "The case for rich media display", but the body has no video or embed, only images.',
 'Etumos': 'The "How an AI Module Is Built" section explains the process in words only, and the post has no diagram or video.',
 'Arcalea': 'It makes the case for publishing a citable benchmark, yet the post has no charts or visuals at all.',
 'BKA Content': 'The checklist says "Make one focused video per post" and "Embed the video near the top of the post", which is a neat brief for a short explainer.',
 'Stranger & Stranger': 'The intro says shoppers meet a product through advertising, social feeds and recommendations before the shelf, but the post has a single image and no video.',
 'Local SEO Guide': 'The $605.20 test runs as one long section across 13 images, with no subheadings.',
 'CaliberMind': 'Small thing, but "Should You Ungate Your Content?" and "Pros and Cons of Gating Content on Your Website" sit back to back and cover the same ground.',
 'Extole': 'It rounds up 58 statistics across sections like "Loyalty and Reward Program Statistics", but there is no infographic or video that sums them up.',
 'InEvent': 'Tip 2 says to post countdown teasers and behind the scenes clips, but the post has no video embedded, only 13 images.',
 'Carnegie Higher Ed': 'The "Post Video Content Consistently" section says phone-filmed clips often beat professional shoots, but the page itself has no video embedded.',
 'Spark Business Works': 'Section 3, "Connect with Compelling Stories", tells readers to tell their brand story, but the post never mentions video and has none embedded.',
}

# B offers (video for the post); everything else is the founder's quote swap.
BOFFER = {
 'Prowess': 'make a short animated explainer for your "Long-form explainers and tutorials" section',
 'Autymate': 'make a short animated explainer for your "Content Marketing and Education" section',
 'Clearstream': 'make a short animated explainer for your "Ways churches use video" section',
 'InEvent': 'make a short animated countdown teaser for your "Post Countdown Teasers and Behind-the-Scenes Clips" section',
 'Spark Business Works': 'make a short animated brand story video for your "Connect with Compelling Stories" section',
}
SECTION = {  # quote swap section, cleaned
 'Certain': 'Experiential & Immersive Formats', 'Fast Simon': 'The Take Away', 'Visions Design': '3. Update Metadata and Content Strategically',
 'Klatch': 'The Solution', 'Moncur': 'The Awareness Stage: Where Problems Get Named', 'GWS Media': 'Bring that story to life',
 'Outloud Group': 'You Cannot Approve Authenticity Into Existence', '29 Design': 'Higher Engagement Rates', 'Bright Vessel': 'They Weight Expertise and Credibility Signals',
 'Enjoy Digital': 'Common trust red flags', 'TicToc Digital': 'Show testimonials from service users', 'Fused': 'Build an Image Library',
 'AIP Media': 'From broad labels to better questions', 'Pink Pine Media': 'Put real people forward', 'Podcast Page': 'Step 3: Cross-Promote Your Content',
 'Mailmunch': 'How to Create Video Ads That Convert', 'LeadDyno': '4. Use Strong, High-Quality Images', 'Sites by Sara': 'Overuse of Stock Images',
 'Intrepy': 'Invest in Video Content to Connect with Patients', '829 Studios': 'YouTube SEO: 3 Pillars for Driving More Video Views',
 '321 Web Marketing': "Add Information Competitors Can't Easily Repeat", 'Reach Marketing': 'Marketing to the Buying Committee Builds Broader Account Awareness',
 'Wired Impact': 'Film a Forward-Looking Interview', 'Pivotal Agency': 'Connecting Digital Efforts to Business Objectives',
 'Ironistic': 'Where AI Actually Earns Its Keep in Content Marketing', 'Rosemont Media': 'Ideas for Captivating Content', 'Upbeat Agency': 'Organic content still matters',
 'Idea Marketing': 'Testimonials & Case Studies That Show Real Outcomes', 'My Dental Agency': "Show, Don't Tell", 'Big Duck': 'Move from deficit- to asset-based storytelling',
 'Stevens and Tate': '6 Elements of Effective Digital Storytelling', 'nDash': "Signs AI Is Blurring a Writer's Original Voice", 'Influ2': '8. Thought leadership campaigns',
 'Hannon Hill': 'Story #3: The Frankenstein Website', 'Elite Strategies': 'The Numbers (So Far)', 'Ad Results Media': 'Podcast Clipping: The New Discovery Engine for Audio & Video',
 'Mindgruve': 'The case for rich media display', 'Etumos': 'What the New Roles Actually Do', 'Arcalea': 'What a Citable Benchmark Actually Requires',
 'BKA Content': 'Make one focused video per post', 'Stranger & Stranger': None, 'Local SEO Guide': None,
 'CaliberMind': 'Pros and Cons of Gating Content on Your Website', 'Extole': 'Referral Program Design Benchmarks', 'Carnegie Higher Ed': 'Post Video Content Consistently',
}

BS = {
 'Certain': 'Company: Motion The Agency.',
 'Fast Simon': '"What can we help with?": Partnerships.',
 'Visions Design': 'Subject: General Enquiry. "How did you find us?": Other. Tick the required consent box.',
 'Prowess': 'Nothing extra',
 'Klatch': 'Nothing extra',
 'Moncur': 'Inquiry Type: General.',
 'Autymate': f'Company: Motion The Agency. Phone is required: {PH}. Leave the Subject dropdown (product list) blank and the newsletter box unticked.',
 'GWS Media': '"How can we help?": Something else. Company: Motion The Agency. Tick the required privacy policy box, leave the newsletter box unticked.',
 'Outloud Group': '"Who Are You?": Agency. Company: Motion The Agency. "Why are you reaching out?": General Inquiry.',
 '29 Design': 'Nothing extra',
 'Bright Vessel': 'Last name: Jupp. The message box takes 600 characters, so paste the short message below as is. Tick the reCAPTCHA box if it shows one.',
 'Enjoy Digital': 'Reason for enquiry: I have a general enquiry. Company: Motion The Agency. Tick the consent box and the reCAPTCHA box if shown.',
 'TicToc Digital': 'Tick the consent box and the reCAPTCHA box if shown.',
 'Fused': 'Company name: Motion The Agency. Paste the message into "Tell us about the challenges you\'re facing".',
 'AIP Media': f'Company: Motion The Agency. Mobile phone is required: {PH}. "How can we help?": Creative (optional).',
 'Pink Pine Media': 'Company: Motion The Agency. "How did you find us?": Their blog.',
 'Podcast Page': 'The site is now Beamly (podcastpage.io redirects to beamly.com). Paste the subject below into the required Subject field.',
 'Mailmunch': 'Website: https://motiontheagency.com (optional).',
 'LeadDyno': 'Use the General Requests form. Last name: Jupp. Website URL: https://motiontheagency.com.',
 'Sites by Sara': 'This is the Become a Partner form. Company: Motion The Agency. "Services You Are Interested in Providing": Motion design and video. "How did you hear about SBS?": pick Other, or the closest honest option. Paste the message into "Tell Us About Your Partnership Proposal".',
 'Intrepy': f'Phone is required: {PH}. "How Did You Hear About Us?": Other.',
 'Clearstream': 'Organization: Motion The Agency.',
 '829 Studios': 'Company: Motion The Agency. Leave Industry and Service of Interest on Please Select.',
 '321 Web Marketing': f'Last name: Jupp. Phone is required: {PH}.',
 'Reach Marketing': f'Company: Motion The Agency. Job title: Founder. Phone is required: {PH}. Leave the solution dropdown blank.',
 'Wired Impact': 'Organization: Motion The Agency. Website: https://motiontheagency.com.',
 'Pivotal Agency': 'Company: Motion The Agency. Leave the service boxes and sliders alone. Timeframe: "I\'m not in a hurry". "How did you hear about us?": Other. Paste the message into Project Details.',
 'Ironistic': f'Last name: Jupp. Phone is required: {PH}. Tick the required terms box, leave the newsletter box unticked.',
 'Rosemont Media': f'Phone is required: {PH}. Zip code is required: try the UK postcode, and if the form only takes a US zip code, skip this one and note it in Slack. Specialty: Other. Leave the text and news boxes unticked.',
 'Upbeat Agency': f'Phone is required: {PH}. Business website: https://motiontheagency.com.',
 'Idea Marketing': f'Company: Motion The Agency. Website: https://motiontheagency.com. Last name: Jupp. Phone is required: {PH}. Leave the service boxes unticked. Paste the message into Project Notes and tick the consent box if asked.',
 'My Dental Agency': f'Last name: Jupp. Phone is required: {PH}.',
 'Big Duck': 'Country: United Kingdom. Title: Founder. Organization: Motion The Agency. Leave the opt-in box unticked.',
 'Stevens and Tate': 'The form loads after a few seconds. Company: Motion The Agency. Role: Agency. "Purpose for Contacting Us": Other.',
 'nDash': 'Tick the reCAPTCHA box.',
 'Influ2': '"I\'m interested in": Partnership. Company: Motion The Agency. Tick the required Privacy Policy box, leave the marketing box unticked.',
 'Hannon Hill': 'Organization: Motion The Agency. Industry: Agency. Topic: General Inquiry. Tick the reCAPTCHA box.',
 'Elite Strategies': f'Use the form on the Press page, not the main contact page. Phone is required: {PH}. Paste the subject below into "What is your Inquiry about?".',
 'Ad Results Media': 'Company: Motion The Agency. "How did you hear about us?": Other. Interest: Business Partnerships. Paste the message into Comments.',
 'Mindgruve': 'Use the first (general) form, not the careers form. Company: Motion The Agency. "How Did You Hear About Us?": Other. Paste the message into Notes.',
 'Etumos': 'Company: Motion The Agency. Request Type: Partnerships.',
 'Arcalea': 'Company: Motion The Agency. Title: Founder. Leave "What best describes what you need?" on Please Select. Paste the message into "What\'s the situation?".',
 'BKA Content': '"I am a...": Curious about something else. Leave the service boxes unticked.',
 'Stranger & Stranger': 'Country: United Kingdom. Company: Motion The Agency. Job title: Founder.',
 'Local SEO Guide': 'The message box takes 600 characters, so paste the short message below as is. "Interested in": Other (optional).',
 'CaliberMind': 'Job title: Founder. Company: Motion The Agency.',
 'Extole': 'Company: Motion The Agency. The message box takes 1,000 characters; the message below fits.',
 'InEvent': 'This is the partner programme form. Company: Motion The Agency. Paste the message into Notes.',
 'Carnegie Higher Ed': 'Institution/Organization: Motion The Agency. Job title: Founder. Tick the "Other" solution box only, leave budget and file upload empty, leave the newsletter box unticked.',
 'Spark Business Works': 'Company: Motion The Agency. Phone if asked: ' + PH + '.',
}
SUBJ = {'Podcast Page': 'a quote for your youtube promotion post',
        'Elite Strategies': 'a quote swap for your content cruft case study'}

def clean(s):
    s = (s or '').replace('—', ', ').replace('–', ' to ').replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')
    return re.sub(r'\s+', ' ', s).strip()

QS3 = 'In return, a credit link back to motiontheagency.com with my quote, and one to yours with your quote on ours, or we\'ll pay for placement instead.'
B3 = "In return, just a credit link back to motiontheagency.com, or we'll pay for placement instead."
rows = []; sub = []
for r in S:
    n = r['companyName']
    d = r['webDomain'].replace('www.', ''); live = (r.get('liveDomain') or '').replace('www.', '').replace('https://', '').strip('/')
    if live == d: live = ''
    title = clean(r['articleTitle']).rstrip('.') 
    url = r['articleUrl']
    if n == 'Industrial': pass
    hook = clean(HOOK[n])
    g = f"Hey {GREET.get(n, n)} team,"
    if n in BOFFER:
        p3 = f"I run a motion studio. Happy to {BOFFER[n]}, free."; p4 = B3; offer = 'Video for the post'
    else:
        sec = SECTION[n]
        where = f'your "{sec}" section' if sec else {'Local SEO Guide':'your Yelp ads test','Stranger & Stranger':'your packaging piece'}[n]
        p3 = f"I run a motion studio. Happy to swap founder quotes: one from me for {where}, and one from you for ours."
        p4 = QS3; offer = "Founder's quote swap"
    msg = f'{g}\n\nJust read your piece "{title}" ({url}). {hook}\n\n{p3}\n\n{p4}\n\nWould you be open to exploring this?\n\nCheers,\nSam\nFounder @ Motion The Agency'
    mx = r.get('messageMaxChars')
    if mx and len(msg) > int(mx):
        msg = msg.replace(", or we'll pay for placement instead.", '.')
    if mx and len(msg) > int(mx):
        msg = msg.replace(' with my quote, and one to yours with your quote on ours', ', and one to yours on ours')
    dr = DR[live or d] if (live or d) in DR else DR[d]
    assert dr >= 40, n
    rows.append(dict(companyName=n, webDomain=live or d, domainRating=dr, drSource='Apify ahrefs-scraper', drDate=DATE,
        country=r['country'], segment=r['segment'], offer=offer, formUrl=r['formUrl'], formSteps=clean(r.get('formSteps')),
        articleTitle=title, articleUrl=url, articleDate=clean(r.get('articleDate')), articleTopic=clean(r.get('articleTopic')),
        linkPlacement=clean(r.get('linkPlacement')), articleHook=hook, captcha=r.get('captcha', ''), consentBox=r.get('consentBox', ''),
        liveDomain=live, originalDomain=d if live else ''))
    sub.append(dict(companyName=n if n != 'Podcast Page' else 'Beamly (Podcast Page)', formUrl=r['formUrl'], beforeSubmit=BS[n], subjectText=SUBJ.get(n, ''), messageText=msg))
    bad = [c for c in msg + BS[n] + SUBJ.get(n, '') if c in '—–']
    flag = (' OVER!' if mx and len(msg) > int(mx) else '') + (' DASH!' if bad else '')
    print(f"{n[:24]:24} w={len(msg.split()):3} c={len(msg):4} max={mx}{flag}")
json.dump(sub, open(B + 'work/messages_draft.json', 'w'), indent=1)
json.dump(rows, open(B + 'work/targets_draft.json', 'w'), indent=1)
