import csv, json, re
REPLY = "sam.jupp@globalmotiontheagency.com"
PHONE = "+44 2039847787"
ME = "I'm Sam, founder of Motion, a motion design studio (motiontheagency.com)."
CREDIT = "In return, just a credit link back to motiontheagency.com, or we'll pay for placement instead."
SWAPCREDIT = "In return, a credit link back to motiontheagency.com with my quote, and one to yours with your quote on ours, or we'll pay for placement instead."
ASK = f"Would you be open to exploring this? Best place to reach me is {REPLY}."
END = "Cheers,\nSam"
def msg(*paras): return "\n\n".join(paras + (ASK, END))

rows = []
def add(company, domain, dr, country, segment, source, offer, formUrl, title, url, subject, message, fields, captcha, consent, manual=""):
    rows.append(dict(companyName=company, webDomain=domain, domainRating=dr, country=country, segment=segment, source=source, offer=offer,
        formUrl=formUrl, articleTitle=title, articleUrl=url, subjectText=subject, messageText=message,
        fieldMap=json.dumps(fields, ensure_ascii=False), captcha=captcha, consentBox=consent, manualCheck=manual))

t,u="High fuel costs? Try Auto Routing","https://blog.servicem8.com/2026/04/high-fuel-costs-try-auto-routing/"
m=msg("Hi ServiceM8 team,",
 f'Could you pass this to whoever runs the blog? I just read "{t}" ({u}). Two small typos in it: "to attend jobs their jobs for the day" and "choose to re-scheduled fixed bookings".',
 ME+' Happy to design a before-and-after route graphic for the "Review before Applying" section, free.', CREDIT)
add("ServiceM8","servicem8.com",84,"Australia","B","new","Blog graphic","https://www.servicem8.com/contact-us",t,u,"your auto routing post",m,
 {"Your email address":REPLY,"Subject":"your auto routing post","Message":m},"check","none")

t,u="How to Audit Your Inventory Infrastructure Before Q4 Hits","https://www.cin7.com/blog/audit-your-inventory-infrastructure/"
m=msg("Hi Cin7 team,",
 f'Could you pass this to whoever looks after the blog? I just read "{t}" ({u}). One line in Audit Area 2 has got scrambled: "Especially for the between 37% and 60% e-commerce businesses". The red flag latency thresholds just below it are plain bullets too.',
 ME+" Happy to design a graphic of those thresholds, free.", CREDIT)
add("Cin7","cin7.com",78,"Australia","B","new","Blog graphic","https://www.cin7.com/contact-us/",t,u,"",m,
 {"First name":"Sam","Last name":"Jupp","Email":REPLY,"Phone":PHONE,"Company name":"Motion The Agency","Reason for reaching out":"Partnership Opportunities","How can we help you?":m},"check","none")

t,u="B2B Marketing Playbook: 7 Steps To Plan A Perfect Project","https://www.imab2b.com/b2b-marketing/"
m=("Hi IMA team,\n\n"
 f'Read your B2B Marketing Playbook ({u}). The buyer\'s journey section opens with the same paragraph as the sales funnel section above it.\n\n'
 "I'm Sam, founder of Motion (motiontheagency.com). Happy to swap founder quotes: mine for that section, yours for one of ours, each with a credit link.\n\n"
 f"Open to it? Reach me at {REPLY}\n\nCheers,\nSam")
add("IMA B2B","imab2b.com",45,"Australia","A","new","Founder's quote swap","https://www.imab2b.com/contact/",t,u,"",m,
 {"Name":"Sam Jupp","Phone":PHONE,"Email":REPLY,"What do you need help with?":m},"check","optionalTerms","500 character limit, so no paid placement line")

t,u="Why Original Human-Led Content Matters in the Age of AI","https://www.melottimedia.com.au/blog/why-original-human-led-content-matters-in-the-age-of-ai/"
m=msg("Hi Melotti team,",
 f'A quick heads-up: your newest post, "{t}" ({u}), loads with no heading or article text. Only the orange banner and the contact block show.',
 ME+" Once the post is back up, happy to swap founder quotes: one from me for that piece, and one from you for ours.", SWAPCREDIT)
add("Melotti Media","melottimedia.com.au",45,"Australia","A","new","Founder's quote swap","https://www.melottimedia.com.au/contact/",t,u,"",m,
 {"First Name":"Sam","Last Name":"Jupp","Phone/Mobile":PHONE,"Email":REPLY,"Your Message":m},"check","none")

t,u="The core disciplines that make up Experience Design","https://inviqa.com/blog/the-core-disciplines-that-make-up-experience-design"
m=msg("Hi Inviqa team,",
 f'Could you pass this to whoever runs the blog? I just read "{t}" ({u}). There\'s a small typo under "UI, interaction and visual design": "Where visual design in a broader design discipline" (should be "is a broader").',
 ME+' Happy to swap founder quotes: one from me on motion design for that section, and one from you for ours.', SWAPCREDIT)
add("Inviqa","inviqa.com",72,"UK","A","leftover","Founder's quote swap","https://inviqa.com/contact",t,u,"",m,
 {"First Name":"Sam","Last Name":"Jupp","Job Title":"Founder","Company Name":"Motion The Agency","Email":REPLY,"Message":m},"check","requiredTerms","required consent box for the human")

t,u="Benchmark Report: Autonomous unit test generation at enterprise scale","https://www.diffblue.com/resources/benchmark-report-autonomous-unit-test-generation-at-enterprise-scale/"
m=msg("Hi Diffblue team,",
 f'Could you pass this to whoever runs content? I just read your benchmark report ({u}). Two numbers seem to clash: the summary says "average line coverage of only 36% with Claude", while the results give 32.3% for Developer + Claude Code.',
 ME+' Happy to make a short animated explainer of the key findings, free.', CREDIT)
add("Diffblue","diffblue.com",62,"UK","B","leftover","Video for the blog post","https://www.diffblue.com/contact/",t,u,"",m,
 {"First Name":"Sam","Last Name":"Jupp","Job Title":"Founder","Company":"Motion The Agency","Work Email":REPLY,"Message":m},"recaptchaEnterprise","none","open General tab, then Ask us anything")

t,u="Off-the-Shelf vs Bespoke Software: How to Choose","https://www.rocketmakers.com/blog/off-the-shelf-software-vs-bespoke-software"
m=msg("Hi Rocketmakers team,",
 f'I just read "{t}" ({u}). The intro promises "a simple framework for making the call", but the cost comparison is arrow bullets with no chart, so the framework is hard to see at a glance.',
 ME+' Happy to swap founder quotes: one from me for "How Does the Cost Compare Over Time?", and one from you for ours.', SWAPCREDIT)
add("Rocketmakers","rocketmakers.com",48,"UK","A","leftover","Founder's quote swap","https://www.rocketmakers.com/contact",t,u,"",m,
 {"Name":"Sam Jupp","Company":"Motion The Agency","Email":REPLY,"Reason":"Find out more about something else","Message":m},"check","none","field labels to confirm at prefill")

t,u="B2B Case Studies That Win Deals","https://elevationb2b.com/blog/b2b-case-studies-sales-decisions/"
m=msg("Hi Elevation team,",
 f'I just read "{t}" ({u}). It argues that a memorable visual can anchor a message better than two extra paragraphs, but the page itself has no image, chart or video.',
 ME+' Happy to swap founder quotes: one from me for the section on case study format, and one from you for ours.', SWAPCREDIT)
add("Elevation Marketing","elevationb2b.com",65,"US","A","leftover","Founder's quote swap","https://elevationb2b.com/contact-us/",t,u,"",m,
 {"First Name":"Sam","Last Name":"Jupp","Email Address":REPLY,"Phone Number":PHONE,"What can we do for you?":m},"recaptchaCheckbox","optionalMarketing","reCAPTCHA for the human; leave newsletter box unticked")

t,u="Top 8 Customer Success Dashboard Examples and Best Practices","https://www.velaris.io/articles/customer-success-dashboard-examples"
m=msg("Hi Velaris team,",
 f'Could you pass this to whoever runs the blog? I just read "{t}" ({u}). The byline is dated 3 December 2026, two months from now, and 85 of the 89 images have empty alt text.',
 ME+' Happy to make a short walkthrough video for "4. Onboarding progress dashboard", free.', CREDIT)
add("Velaris","velaris.io",48,"UK","B","leftover","Video for the blog post","https://www.velaris.io/contact",t,u,"your customer success dashboards piece",m,
 {"First name":"Sam","Last name":"Jupp","Email":REPLY,"Company":"Motion The Agency","Phone number":PHONE,"Subject":"your customer success dashboards piece","Message":m},"check","none")

for r in rows:
    w=len(r['messageText'].split()); c=len(r['messageText'])
    bad=re.search('[—–]',r['messageText'])
    print(f"{r['companyName']:20} words={w} chars={c} dash={'YES' if bad else 'no'}")
with open('04_form_messages.csv','w',newline='') as f:
    wr=csv.DictWriter(f,list(rows[0].keys())); wr.writeheader(); wr.writerows(rows)
with open('03_form_targets.csv','w',newline='') as f:
    k=['companyName','webDomain','domainRating','country','segment','source','offer','formUrl','articleTitle','articleUrl']
    wr=csv.DictWriter(f,k,extrasaction='ignore'); wr.writeheader(); wr.writerows(rows)
