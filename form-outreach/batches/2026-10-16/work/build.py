import json,csv,re
B='/home/claude/seo-backlink-outreach/form-outreach/batches/2026-10-16/'
P=json.load(open(B+'work/passes.json'))
PH='+44 2039847787'
APIFY={'excitemedia.com.au':76,'swiftdigital.com.au':44,'smsglobal.com':65,'cemoh.com':52,'aroflo.com':57,'vivi.io':53,'hatch.team':40,'lyrebirdhealth.com':57,'boylen.com.au':71,'livingonline.com.au':53,'eber.co':68,'moodle.com':91,'hellopixels.com':50,'hospitable.com':76,'talentlms.com':85,'lifterlms.com':80,'fairing.co':63,'virtuous.org':73,'mediashower.com':63,'munro.agency':47,'thedatacity.com':62,'opace.agency':49,'getadministrate.com':59,'panintelligence.com':50,'ebi.ai':45,'flexa.careers':61,'atendesigngroup.com':54,'appointedd.com':74,'gregoryagency.com':43,'reddoor.biz':59,'hennessey.com':72,'fourkitchens.com':62,'clockwork.com':57,'palantir.net':63,'phase2.io':62,'currentagency.com':53,'kalamuna.com':45,'thirdandgrove.com':55,'odd.dog':50,'brandextract.com':57,'padillaco.com':52,'dbswebsite.com':68,'brodeur.com':40,'userinterviews.com':76}
FREE={'tovutilms.com':54,'momogood.com':61,'cornershopcreative.com':71,'r3.agency':47,'atomicdust.com':43,'arrows.to':56,'spekit.com':70,'sendbird.com':76,'pipelinecrm.com':72,'gptzero.me':81}
# section phrase for quote swaps: completes "one from me for ____"
SWAP={'Excite Media':'your "Video content" section','Living Online':'a video marketing entry in the V section of your glossary','Boylen':'this piece','Aten Design Group':'your "When (and When Not) to Use Surveys" section'}
# offer phrase for B rows: completes "Happy to ____, free."
OFFER={'Hatch':'add a short founder\'s quote on how video and motion shape an employer brand for the "How does the Marketing Team contribute to the employer brand at Tracksuit?" section',
'User Interviews':'add a short founder\'s quote for your "A few caveats on comics" section',
'Spekit':'make a short animated explainer of the forgetting curve stats for your "The Power of Visual Learning: How Video is Redefining Training" section',
'GPTZero':'give a founder\'s quote on how a video studio uses AI for short videos, for your "Content types and formats" section',
'Panintelligence':'design a one page "which chart should I use" infographic covering the five chart types in the post',
'Administrate':'design the example board slide from "The slide itself" section as a graphic for the post',
'Sendbird':'make a short animated explainer of the awareness, acquisition and retention loop for your "2. Acquisition stage" section'}
SUBJ={'Aten Design Group':'noticed something in your survey mistakes post','Phase2':'a quote for your AI digital experience post','Brodeur Partners':'your piece on great brand stories'}
BS={
'Cemoh':f'Phone is required: {PH}. Tick the required terms and privacy box. Leave Budget unselected.',
'Excite Media':f'Phone is required: {PH}. Company name: Motion The Agency. Website: motiontheagency.com. Leave the Facebook field blank (it is a spam trap).',
'SMSGlobal':f'Use the "Get in touch" form. Company name: Motion The Agency. Mobile number is required: {PH}. Leave Estimated Monthly Messaging Volume blank.',
'Swift Digital':f'Use the main contact form at the top of the page. Last name: Jupp. Company: Motion The Agency. Phone is required: {PH}.',
'AroFlo':'Click the Enquiries tab, then "Send a General Enquiry" (opens a Typeform). Nothing else required beyond email.',
'Vivi':f'"How can we help you": Media & partnerships. Role: Other. Current customer: No. Last name: Jupp. Phone is required: {PH}. Organisation: Motion The Agency. Country: United Kingdom.',
'Moodle':'"How can we help you today?": I have a different enquiry. "Nature of your enquiry": PR & media enquiry. Job function: CEO. Last name: Jupp. Country: United Kingdom.',
'Lyrebird Health':f'Use the partner form. Company: Motion The Agency. Phone is required: {PH}. Country: Other. Website: https://motiontheagency.com',
'Hatch':'Contact preference: tick "Send me an email". Nothing else required.',
'Living Online':f'Company: Motion The Agency. Phone is required: {PH}. Job title: Founder. The message box is optional, so make sure it is filled.',
'Boylen':f'Phone is required: {PH}. Timeframe is required: write "No project, partnership idea". Leave Budget blank.',
'Eber':f'Industry dropdown: Partnerships / For Customers. Role: Owner / CEO / Founder. Phone is required: {PH}. Company: Motion The Agency. Website: motiontheagency.com.',
'Hello Pixels':f'"What do you need?" dropdown: Others. Phone is required: {PH}. Company: Motion The Agency.',
'Hospitable':f'Click "Contact marketing" (opens a Typeform). Topic: Contributing to the blog. Phone is required: {PH}. Company: Motion The Agency.',
'TalentLMS':'"What do you need help with?": I have a general question. Company: Motion The Agency. Country: United Kingdom. Existing customer: No. If goal or team size dropdowns appear, pick Other and Don\'t know yet.',
'LifterLMS':'"What are you contacting us about?": Request for marketing collaboration (i.e. interview, affiliate, partnership). Leave the X/Twitter field blank.',
'Fairing':'"What can we help with?": Something else. Fill name and email.',
'Virtuous':f'Phone is required: {PH}. Organisation name: Motion The Agency.',
'Media Shower':'"What Brings You Here Today?": I want to be featured on the Media Shower blog. Company website: motiontheagency.com.',
'The Munro Agency':'Tick the reCAPTCHA box at the bottom of the form.',
'Opace':f'Phone is required: {PH}. Service dropdown: Other / Not Sure Yet. Leave the Website field blank (it is a spam trap).',
'The Data City':f'Click "Contact us" under "Get in touch" to open the General Enquiry popup. "I work in": Other. Company: Motion The Agency. Phone is required: {PH}.',
'Administrate':'Use the "General inquiries" form on the right. Country/Region: United Kingdom. Tick the required box to receive Administrate news (the form will not send without it).',
'Appointedd':'Tick the required privacy policy box.',
'Panintelligence':f'Phone is required: {PH}. Company: Motion The Agency.',
'EBI.AI':'The form can take a few seconds to load (accept only necessary cookies if asked). Nothing else required.',
'Flexa':'Pick "I\'m an employer" in the radio choice.',
'Aten Design Group':'Paste the subject below into the required Subject field. A Cloudflare check box may appear: tick it yourself.',
'Gregory':'Scroll to "Let\'s Connect." The form loads after a moment. Leave the marketing box unticked.',
'Red Door Interactive':'Click the "EVERYTHING ELSE / Get in touch" card to open the form. Company: Motion The Agency. Leave the marketing box unticked.',
'Hennessey Digital':f'Industry: Other. Phone is required: {PH}. Company: Motion The Agency. Company URL: https://motiontheagency.com',
'Four Kitchens':'Organisation: Motion The Agency. Country: United Kingdom. Tick the required privacy agreement box.',
'Clockwork':'Company: Motion The Agency. Leave the marketing box unticked.',
'Palantir.net':'"I work for": Motion The Agency. Leave the marketing box unticked.',
'Current Agency':'Leave Budget blank. A Cloudflare check box may appear: tick it yourself.',
'Phase2':'Paste the subject below into the required Subject field (max 100 characters).',
'Kalamuna':'Leave "I need help with a project" unticked and use the Message box. Leave the marketing box unticked.',
'Third and Grove':'There is no name field, so the message already ends with Sam\'s name. "How did you hear about us": Your blog.',
'Padilla':'Company: Motion The Agency. Leave the radio and dropdown choices empty. A Cloudflare check box may appear: tick it yourself.',
'BrandExtract':'Nothing extra',
'Odd Dog Media':'Use the enquiry form near the bottom of the About page (the Contact page only has a booking widget). Leave the marketing box unticked.',
'DBS Interactive':f'Repeat the email in Confirm Email. Fill Phone ({PH}) and Company (Motion The Agency) to be safe, as required fields are not marked.',
'Brodeur Partners':'Company name: Motion The Agency. Paste the subject below into the Subject field.',
'Atomicdust':'Optional interest box: tick Other. A Cloudflare check box may appear: tick it yourself.',
'Arrows':'Nothing extra',
'User Interviews':'Use the form on the Partners page. Type of partnership: Reports & Content. Company: Motion The Agency.',
'Spekit':'Reason: General Inquiry. Company name: Motion The Agency.',
'Sendbird':'Use the "Have a question?" form, not Contact sales. Company name: Motion The Agency. Leave the marketing box unticked.',
'Pipeline CRM':'Tick the required terms box. Leave the Company Website field blank (it is a spam trap).',
'Cornershop Creative':'"What can we help you with?": Anything Else. Organisation: Motion The Agency. Job title: Founder. "How did you hear about Cornershop?": From another website or article. Leave the project dates and budget blank.',
'R3':'Company: Motion The Agency. Leave Project Budget Range blank. Tick the required privacy box.',
'momoGood':'"What can we help with?": Partnership opportunities. Organisation: Motion The Agency. Country: United Kingdom.',
'Tovuti LMS':'Business phone is required: +44 2039847787. The message box is optional, so make sure it is filled.',
'GPTZero':'Subject dropdown: Press and media. Organisation: Motion The Agency. Role: Founder.',
}
def clean(s):
    s=s.replace('—',', ').replace('–',' to ').replace('’',"'").replace('‘',"'").replace('“','"').replace('”','"')
    s=re.sub(r'\s*\U0001F3A5','',s)
    return s.strip()
rows=[];sub=[]
for r in P:
    n=r['companyName']; d=r['webDomain']
    title=clean(r['articleTitle']); url=r['articleUrl']; hook=clean(r['articleHook'])
    g=f"Hey {n} team,"
    if r['segment']=='A' or r['offerSuggestion']=="Founder's quote swap":
        sec=SWAP.get(n, f'your "{clean(r["linkPlacement"])}" section')
        p3=f"I run a motion studio. Happy to swap founder quotes: one from me for {sec}, and one from you for ours."
        p4="In return, a credit link back to motiontheagency.com with my quote, and one to yours with your quote on ours, or we'll pay for placement instead."
        offer="Founder's quote swap"
    else:
        ol=clean(OFFER.get(n,r['offerLine']))
        ol=ol.replace(' for the "',' for your "')
        p3=f"I run a motion studio. Happy to {ol}, free."
        p4="In return, just a credit link back to motiontheagency.com, or we'll pay for placement instead."
        offer=r['offerSuggestion']
    msg=f'{g}\n\nJust read your piece "{title}" ({url}). {hook}\n\n{p3}\n\n{p4}\n\nWould you be open to exploring this?\n\nCheers,\nSam\nFounder @ Motion The Agency'
    if n=='Third and Grove': msg=msg.replace('Cheers,\nSam\n','Cheers,\nSam Jupp\n')
    dom=d.replace('www.','')
    dr=APIFY.get(dom) or FREE.get(dom); src='Apify ahrefs-scraper' if dom in APIFY else 'Ahrefs public-domain-rating-free'
    assert dr and dr>=40, n
    rows.append(dict(companyName=n,webDomain=dom,domainRating=dr,drSource=src,drDate='2026-10-16',country=r['country'],segment=r['segment'],offer=offer,formUrl=r['formUrl'],formSteps=clean(r['formSteps']),articleTitle=title,articleUrl=url,articleDate=r['articleDate'],articleTopic=clean(r['articleTopic']),linkPlacement=clean(r['linkPlacement']),articleHook=hook,captcha=r['captcha'],consentBox=r['consentBox'],liveDomain=(r.get('liveDomain') or '').replace('www.','')))
    sub.append(dict(companyName=n,formUrl=r['formUrl'],beforeSubmit=BS[n],subjectText=SUBJ.get(n,''),messageText=msg))
    mx=r.get('messageMaxChars')
    bad=[c for c in msg if c in '—–']
    print(f"{n[:22]:22} words={len(msg.split()):3} chars={len(msg):4} max={mx} dash={bool(bad)}" + ('  OVER!' if mx and len(msg)>int(mx) else ''))
json.dump(sub,open(B+'work/messages_draft.json','w'),indent=1)
json.dump(rows,open(B+'work/targets_draft.json','w'),indent=1)
