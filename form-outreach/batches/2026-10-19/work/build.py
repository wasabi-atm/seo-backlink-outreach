import json,csv,re
B='/home/claude/seo-backlink-outreach/form-outreach/batches/2026-10-19/'
P=json.load(open(B+'work/passes.json'))
PH='+44 2039847787'
DR={"agentfire.com":69,"fullmedia.com":70,"planningpod.com":71,"swoogo.events":76,"petdesk.com":82,"referralrock.com":82,"bugherd.com":73,"clariantcreative.com":43,"netline.com":62,"truenorthagency.com":47,"1digitalagency.com":59,"anedot.com":89,"thanx.com":75,"tapcart.com":72,"intuitivedigital.com":47,"beehivepr.biz":40,"cirrusinsight.com":77,"antavo.com":74,"nucleuscommercialfinance.com":42,"octaneai.com":71,"locomotive.agency":56,"slicktext.com":76,"textline.com":70,"sendtrumpet.com":65,"document360.com":80,"marcom.com":67,"coefficient.io":72,"swagup.com":67,"marketman.com":70,"joinblvd.com":80,"seranking.com":86,"littlegreenlight.com":68,"visible.vc":69,"hunchads.com":63,"tune.com":77,"contentsnare.com":73,"channelscaler.com":66,"sweetprocess.com":72,"thnks.com":50,"whimsical.com":79,"getsubly.com":58,"withmoxie.com":64,"playroll.com":60,"mo.work":49,"daasity.com":70}
NAME={'True North Custom':'True North','Beehive Strategic Communication':'Beehive','Allbound':'Channelscaler','Locomotive Agency':'Locomotive','Nucleus Commercial Finance':'Nucleus'}
OFFER={'Whimsical':'make a one page spotter\'s guide graphic of the four comparison page species for your closing section',
'Textline':'make a short animated product explainer for the "Make it visual" tip in your "Best practices for RCS marketing" section',
'Mo':'make a simple graphic of the best practices list for your "What Are the Best Practices for Internal Communication?" section',
'Moxie':'make a simple infographic of your "6 kinds of content you should be making" list',
'Little Green Light':'make a simple planning timeline graphic for your "Here are some tips to help you plan ahead" section',
'Octane AI':'turn the numbers in your "The Data: Quiz Pages vs Product Pages" section into a simple comparison graphic',
'Allbound':'turn the 70X, 40X and 60X telecoms results in your "The True ROI of Intelligent Content Systems" section into a simple infographic',
'SlickText':'turn your "Sample Black Friday SMS marketing timeline" section into a simple visual timeline graphic',
'Tapcart':'turn the high-signal push notification table into a clean infographic for your "High-Signal vs. Low-Signal Push Notifications" section',
'Referral Rock':'make an infographic of the seven steps in your "How to start a social media ambassador program" section',
'Thanx':'make a simple diagram of the guest journey through the six automations in your "Build a Lifecycle Marketing Engine" section',
'Planning Pod':'make a short animated explainer for your "golden hour" follow-up section',
'Visible':'make a short animated example of a moving chart slide for your "8. Motion Graphics" section',
'BugHerd':'add a founder\'s quote on presenting motion and animation work for your "Showcase the Kind of Work You Like To Do" section',
'Coefficient':'make a short animated example video for your "Engagement by Post Type" section',
}
BS={
'Swoogo':f'Use the partner form at the bottom of the Partners page ("Howdy, partner"). Business type: Agency. Country: United Kingdom. Region: EMEA. Phone is required: {PH}. Company: Motion The Agency. Leave customer and employee counts blank.',
'Planning Pod':'Pick "General Inquiry" at the top of the form. Paste the subject below into the required Subject field.',
'Full Media':'The form appears after you scroll or move the mouse on the page. Company name: Motion The Agency. Leave the newsletter box unticked.',
'NetLine':'Pick "Leave a Comment" at the top (not Contact Sales). Reason for Comment: Other Comment. NetLine Department: Marketing. Title: Founder. Company: Motion The Agency. Job area: Creative/Design. Industry: Advertising/Marketing. Country: United Kingdom. Fill any other field the form flags on submit (phone: '+PH+').',
'AgentFire':'Use the main contact form, not the quiz. "Are you a current customer?": No. Tick the required "I agree" box.',
'Referral Rock':f'"Main goal for reaching out": Contribute Content. Phone is required: {PH}. Company: Motion The Agency.',
'PetDesk':f'Use the "Ready to grow together?" form at the bottom of the Partnerships page. Phone is required: {PH}. Company: Motion The Agency. Website: motiontheagency.com.',
'Clariant Creative':'Company Name: Motion The Agency. Email list question: No thank you.',
'BugHerd':'The form is a Typeform. On the first question pick "I\'d like to talk about something else" (not the demo option), then paste the message and add name and email when asked.',
'True North Custom':'Company: Motion The Agency.',
'Thanx':f'"What can we help you with?": Partnership inquiry. Phone is required: {PH}. Company: Motion The Agency.',
'1Digital Agency':'The form sits in a box on the contact page. Company: Motion The Agency. Leave the SMS opt-in unticked.',
'Anedot':'Use the Content Partner Program form under "Join the partner program today!". Company: Motion The Agency. Website: https://motiontheagency.com. Company size: Motion\'s real headcount. Product or services offered: Motion design, animated explainer videos and blog graphics for B2B companies. Paste the message into "What type of content would you like to partner on?".',
'Tapcart':f'Partner type: Agency. Website: https://motiontheagency.com. Country: United Kingdom. Business phone: {PH}.',
'Antavo':'Scroll down so the form loads. Role: Other. "What can we help you with?": Marketing Inquiries (guest post, press, events, etc.). Last name: Jupp. Tick the required data processing box.',
'Octane AI':'Type of inquiry: Partnership. Company: Motion The Agency.',
'Intuitive Digital':'Leave all service boxes and the free audit box unticked.',
'Beehive Strategic Communication':f'"I\'d like to chat about": Partnering with Beehive. Phone is required: {PH}. Company: Motion The Agency.',
'Cirrus Insight':'Company name: Motion The Agency.',
'Nucleus Commercial Finance':f'Contact reason: Marketing & PR. Company: Motion The Agency. Phone is required: {PH}. Answer the simple sum (5+2) at the bottom.',
'Locomotive Agency':f'Phone is required: {PH}. Company URL: motiontheagency.com. Leave the newsletter box unticked.',
'SlickText':f'Click "Send a Message" to open the form. Reason: Other. Mobile phone is required: {PH}. Company: Motion The Agency.',
'Textline':f'Company: Motion The Agency. Phone is required: {PH} (max 14 characters, so type it without spaces). The required box agrees to automated texts from Textline to that number.',
'Document360':f'Company: Motion The Agency. Country: United Kingdom. Phone is required: {PH}.',
'Trumpet':'On the Partners page click the "Co-marketing: Pitch a collaboration" card. Company: Motion The Agency. Website: motiontheagency.com. "Who\'s your audience?": B2B SaaS marketing and sales teams. Tick "Blog or report".',
'Coefficient':'Under "How can we help you?" tick Partnerships only.',
'MarcomCentral':f'The form loads after a moment. Company: Motion The Agency. Phone is required: {PH}.',
'Boulevard':'Use the Become a Contributor form (it loads after a moment). Business name: Motion The Agency.',
'Visible':f'Phone is required: {PH}.',
'SwagUp':'"I am a": Other. "What can we help you with": General Inquiry. Company: Motion The Agency. Leave the "keep me in the loop" box unticked.',
'MarketMan':f'Use the Become a Partner form. Cell phone is required: {PH}. Company: Motion The Agency. Job title: Founder. Country: United Kingdom.',
'SE Ranking':'Type of issue: "Advetrising & Partnership" (spelt that way on the site). Paste the subject below into the required Subject field.',
'Little Green Light':'Organisation name: Motion The Agency. Leave the donor system question blank.',
'Hunch':'Use a business email if the form rejects the reply email. Tick the required terms box.',
'TUNE':'Company: Motion The Agency. Job title: Founder. Country: United Kingdom. Business type: Agency. The "receive more information" box is required, so tick it.',
'Content Snare':'Pick "Something else". Type the word Snare in the anti-spam box.',
'Allbound':f'The site is now Channelscaler. Company: Motion The Agency. Phone is required: {PH} (pick the UK country code). Paste the message into "Nature of Enquiry".',
'Thnks':'"Interested In": Other. The form may only appear after you answer the cookie banner (accept only necessary cookies).',
'SweetProcess':'Paste the subject below into the required Subject field.',
'Whimsical':'Nothing extra',
'Playroll':'Nothing extra',
'Subly':'Use the General form (not Sales or Support).',
'Moxie':'Nothing extra',
'Mo':'"How did you hear about Mo?": Your blog. Leave company size blank.',
'Daasity':f'Contact Type: Other. Phone is required: {PH}. Website URL: https://motiontheagency.com. Leave Platform and Size of Company blank.',
}
SUBJ={'Planning Pod':'the recap video idea in your ticketed events post','SE Ranking':'a quote for your videos and SEO post','SweetProcess':'a video for your training materials post'}
def clean(s):
    s=(s or '').replace('—',', ').replace('–',' to ').replace('’',"'").replace('‘',"'").replace('“','"').replace('”','"')
    return s.strip()
rows=[];sub=[]
for r in P:
    n=r['companyName']; d=r['webDomain'].replace('www.',''); live=(r.get('liveDomain') or '').replace('www.','')
    title=clean(r['articleTitle']); url=r['articleUrl']; hook=clean(r['articleHook'])
    g=f"Hey {NAME.get(n,n)} team,"
    if r['offerSuggestion']=="Founder's quote swap":
        sec=clean(r['offerLine']); sec=re.sub(r'^the ','your ',sec)
        p3=f"I run a motion studio. Happy to swap founder quotes: one from me for {sec}, and one from you for ours."
        p4="In return, a credit link back to motiontheagency.com with my quote, and one to yours with your quote on ours, or we'll pay for placement instead."
        offer="Founder's quote swap"
    else:
        ol=clean(OFFER.get(n,r['offerLine'])).replace(' for the "',' for your "')
        p3=f"I run a motion studio. Happy to {ol}, free."
        p4="In return, just a credit link back to motiontheagency.com, or we'll pay for placement instead."
        offer=r['offerSuggestion']
    msg=f'{g}\n\nJust read your piece "{title}" ({url}). {hook}\n\nThe {p3}\n\n{p4}\n\nWould you be open to exploring this?\n\nCheers,\nSam\nFounder @ Motion The Agency'.replace('\n\nThe I run','\n\nI run')
    dr=DR.get(live or d) or DR.get(d)
    assert dr and dr>=40, n
    rows.append(dict(companyName=n,webDomain=d,domainRating=dr,drSource='Apify ahrefs-scraper',drDate='2026-10-19',country=r['country'],segment=r['segment'],offer=offer,formUrl=r['formUrl'],formSteps=clean(r.get('formSteps')),articleTitle=title,articleUrl=url,articleDate=clean(r.get('articleDate')),articleTopic=clean(r.get('articleTopic')),linkPlacement=clean(r.get('linkPlacement')),articleHook=hook,captcha=r.get('captcha',''),consentBox=r.get('consentBox',''),liveDomain=live))
    sub.append(dict(companyName=n,formUrl=r['formUrl'],beforeSubmit=BS[n],subjectText=SUBJ.get(n,''),messageText=msg))
    mx=r.get('messageMaxChars'); bad=[c for c in msg+BS[n]+SUBJ.get(n,'') if c in '—–']
    flag=(' OVER!' if mx and len(msg)>int(mx) else '')+(' DASH!' if bad else '')+(' NEEDSUBJ' if r.get('hasSubjectField')=='yes' and not SUBJ.get(n) else '')
    print(f"{n[:24]:24} w={len(msg.split()):3} c={len(msg):4} max={mx}{flag}")
json.dump(sub,open(B+'work/messages_draft.json','w'),indent=1)
json.dump(rows,open(B+'work/targets_draft.json','w'),indent=1)
