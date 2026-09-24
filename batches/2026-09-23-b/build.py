import csv
A = """Vimeo|vimeo.com|US|Video hosting platform
Loom|loom.com|US|Async video messaging tool
Animoto|animoto.com|US|Online video maker
Kapwing|kapwing.com|US|Online video editor
Riverside|riverside.fm|US|Podcast and video recording platform
StreamYard|streamyard.com|US|Live streaming studio
Restream|restream.io|US|Multistreaming platform
Brightcove|brightcove.com|US|Enterprise video platform
JW Player|jwplayer.com|US|Video player and hosting
Mux|mux.com|US|Video API platform
Cloudinary|cloudinary.com|US|Media management platform
Hippo Video|hippovideo.io|US|Video sales platform
BombBomb|bombbomb.com|US|Video email platform
Sendspark|sendspark.com|US|Personalised video platform
TechSmith|techsmith.com|US|Screen recording software
Screencastify|screencastify.com|US|Screen recording tool
Pictory|pictory.ai|US|AI video tool
HeyGen|heygen.com|US|AI video generation
Elai|elai.io|US|AI video generation
Siege Media|siegemedia.com|US|Content marketing agency
Fractl|frac.tl|US|Content marketing agency
Directive|directiveconsulting.com|US|B2B SaaS marketing agency
Single Grain|singlegrain.com|US|Digital marketing agency
WebFX|webfx.com|US|Digital marketing agency
Ignite Visibility|ignitevisibility.com|US|Digital marketing agency
Orbit Media|orbitmedia.com|US|Web design and content agency
Content Harmony|contentharmony.com|US|Content brief software
ClearVoice|clearvoice.com|US|Content creation platform
Contently|contently.com|US|Content marketing platform
Skyword|skyword.com|US|Content marketing platform
Scripted|scripted.com|US|Freelance writing platform
Verblio|verblio.com|US|Content writing service
Brafton|brafton.com|US|Content marketing agency
Walker Sands|walkersands.com|US|B2B marketing and PR agency
97th Floor|97thfloor.com|US|Digital marketing agency
Seer Interactive|seerinteractive.com|US|Digital marketing agency
Victorious|victorious.com|US|SEO agency
NoGood|nogood.io|US|Growth marketing agency
Refine Labs|refinelabs.com|US|B2B demand gen agency
Ironpaper|ironpaper.com|US|B2B growth agency
Kuno Creative|kunocreative.com|US|Inbound marketing agency
New Breed|newbreedrevenue.com|US|B2B revenue agency
IMPACT|impactplus.com|US|Marketing training and agency
Square 2|square2marketing.com|US|Inbound marketing agency
Weidert Group|weidert.com|US|B2B inbound agency
Bluleadz|bluleadz.com|US|Inbound marketing agency
SmartBug Media|smartbugmedia.com|US|Inbound marketing agency
Lean Labs|leanlabs.com|US|SaaS growth agency
SimpleTiger|simpletiger.com|US|SaaS SEO agency
Uplift Content|upliftcontent.com|US|B2B content agency
Codeless|codeless.io|US|Content marketing agency
Draft.dev|draft.dev|US|Technical content agency
Semrush|semrush.com|US|SEO software
Moz|moz.com|US|SEO software
Sprout Social|sproutsocial.com|US|Social media software
Buffer|buffer.com|US|Social media software
CoSchedule|coschedule.com|US|Marketing calendar software
MarketMuse|marketmuse.com|US|Content planning software
Clearscope|clearscope.io|US|Content optimisation software
Frase|frase.io|US|SEO content tool
Jasper|jasper.ai|US|AI marketing copy platform
Copy.ai|copy.ai|US|AI GTM platform
Writer|writer.com|US|Enterprise AI writing platform
Visme|visme.co|US|Visual content platform
Beautiful.ai|beautiful.ai|US|Presentation software
Prezi|prezi.com|US|Presentation software
Instapage|instapage.com|US|Landing page platform
Leadpages|leadpages.com|US|Landing page builder
Klaviyo|klaviyo.com|US|Email marketing platform
Kit|kit.com|US|Creator email marketing
beehiiv|beehiiv.com|US|Newsletter platform
Qualified|qualified.com|US|Pipeline generation platform
Demandbase|demandbase.com|US|ABM platform
6sense|6sense.com|US|ABM platform
G2|g2.com|US|Software review marketplace
TrustRadius|trustradius.com|US|Software review platform
Wynter|wynter.com|US|B2B message testing
Crazy Egg|crazyegg.com|US|Website heatmap tool
Muck Rack|muckrack.com|US|PR software
Cision|cision.com|US|PR software
Meltwater|meltwater.com|US|Media intelligence
5W Public Relations|5wpr.com|US|PR agency
Sweet Fish Media|sweetfishmedia.com|US|B2B podcast agency
Content Allies|contentallies.com|US|B2B podcast agency
Casted|casted.us|US|Podcast marketing platform
Headliner|headliner.app|US|Podcast promo video tool
Buzzsprout|buzzsprout.com|US|Podcast hosting
Transistor|transistor.fm|US|Podcast hosting
Red Antler|redantler.com|US|Brand agency
Focus Lab|focuslab.agency|US|Brand agency
Ramotion|ramotion.com|US|Brand and web design agency
Clay|clay.global|US|UI UX design agency
Veza Digital|vezadigital.com|US|Webflow agency for B2B
Webflow|webflow.com|US|Website builder
Framer|framer.com|US|Website builder
Hotjar|hotjar.com|US|Website analytics tool
Unbounce|unbounce.com|US|Landing page builder
Vidyard|vidyard.com|US|Video platform for sales
Synthesia|synthesia.io|UK|AI video generation
VEED|veed.io|UK|Online video editor
Colossyan|colossyan.com|UK|AI video for training
BuzzSumo|buzzsumo.com|UK|Content research tool
Brandwatch|brandwatch.com|UK|Social listening
Pulsar|pulsarplatform.com|UK|Audience intelligence
Captivate|captivate.fm|UK|Podcast hosting
Lower Street|lowerstreet.co|UK|Podcast production agency
JAR Audio|jaraudio.com|UK|Branded podcast agency
Impression|impression.co.uk|UK|Digital marketing agency
Rise at Seven|riseatseven.com|UK|Search and content agency
Builtvisible|builtvisible.com|UK|SEO and content agency
Brainlabs|brainlabsdigital.com|UK|Performance marketing agency
Reboot Online|rebootonline.com|UK|SEO agency
Verve Search|vervesearch.com|UK|SEO and digital PR agency
The SEO Works|seoworks.co.uk|UK|SEO agency
Exposure Ninja|exposureninja.com|UK|Digital marketing agency
Click Consult|clickconsult.com|UK|Search marketing agency
Bird Marketing|birdmarketing.co.uk|UK|Digital marketing agency
Blue Array|bluearray.co.uk|UK|SEO consultancy
Re:signal|resignal.com|UK|SEO agency
Kaizen|kaizen.co.uk|UK|Digital PR agency
Digitaloft|digitaloft.co.uk|UK|Digital PR agency
Semetrical|semetrical.com|UK|SEO and data agency
Fox Agency|thisisfox.com|UK|B2B tech marketing agency
Transmission|transmissionagency.com|UK|B2B marketing agency
Napier|napierb2b.com|UK|B2B tech PR agency
Stein IAS|steinias.com|UK|B2B marketing agency
Omobono|omobono.com|UK|B2B brand agency
Hotwire|hotwireglobal.com|UK|Tech PR agency
Brands2Life|brands2life.com|UK|Tech PR agency
Wildfire|wildfirepr.com|UK|Tech PR agency
Koto|koto.studio|UK|Brand studio
Ragged Edge|raggededge.com|UK|Brand agency
DixonBaxi|dixonbaxi.com|UK|Brand agency
Pearlfisher|pearlfisher.com|UK|Brand design agency
JKR|jkrglobal.com|UK|Brand design agency
Sitebulb|sitebulb.com|UK|SEO audit software
Lumar|lumar.io|UK|Website intelligence software
Audiense|audiense.com|UK|Audience intelligence
Copify|copify.com|UK|Content writing service
Propellernet|propellernet.co.uk|UK|Search marketing agency
Digital Marketing Institute|digitalmarketinginstitute.com|UK|Marketing training
Growth Marketing Pro UK|growthmarketinghq.co.uk|UK|Growth marketing agency
Tenet|tenet.ae|UAE|B2B growth marketing agency
Chain Reaction|chainreaction.ae|UAE|B2B digital marketing agency
Vadecom|vadecom.net|UAE|B2B digital agency
PUSH|pushgroup.ae|UAE|B2B marketing agency
Kleosa|kleosa.com|UAE|SEO and paid ads agency
WebQuest|webquest.ae|UAE|SEO agency
Dot IT|dotit.ae|UAE|Digital marketing agency
SEO Sherpa|seosherpa.com|UAE|SEO agency
Traffic Digital|traffic-digital.com|UAE|Digital agency
Prism Digital|prism-me.com|UAE|Digital marketing agency
Socialize|socializeagency.com|UAE|Social media agency
Digital Boutique|digitalboutique.ae|UAE|Digital marketing agency
The Bold Group|theboldgroup.ae|UAE|Creative and digital agency
Hyperlink InfoSystem UAE|hyperlinkinfosystem.ae|UAE|Web and app agency
Brand Lounge|brandlounge.ae|UAE|Brand agency
Blue Beetle|bluebeetle.ae|UAE|Digital marketing agency
Webpuzzlemaster|webpuzzlemaster.com|UAE|Digital marketing agency
Crowd|wearecrowd.com|UAE|Digital agency
Brandformance|brandformance.com|UAE|Performance marketing agency
Digital Marketing Community UAE|digitalmarketingcommunity.ae|UAE|Marketing media
Communicate Online|communicateonline.me|UAE|Marketing news
Campaign Middle East|campaignme.com|UAE|Marketing news
ArabAd|arabadonline.com|UAE|Marketing news
Wamda|wamda.com|UAE|Startup media platform
"""
B = """Gusto|gusto.com|US|Payroll SaaS
Rippling|rippling.com|US|HR and IT SaaS
Deel|deel.com|US|Global payroll SaaS
Remote|remote.com|US|Global HR SaaS
Justworks|justworks.com|US|PEO and HR SaaS
BambooHR|bamboohr.com|US|HR SaaS
Lever|lever.co|US|Recruiting software
Greenhouse|greenhouse.com|US|Recruiting software
Ashby|ashbyhq.com|US|Recruiting software
Gem|gem.com|US|Recruiting CRM
Zapier|zapier.com|US|Automation SaaS
Airtable|airtable.com|US|Work platform
Notion|notion.com|US|Workspace software
ClickUp|clickup.com|US|Project management SaaS
Asana|asana.com|US|Work management SaaS
Smartsheet|smartsheet.com|US|Work management SaaS
Wrike|wrike.com|US|Work management SaaS
Calendly|calendly.com|US|Scheduling SaaS
PandaDoc|pandadoc.com|US|Document automation SaaS
Gong|gong.io|US|Revenue intelligence
Outreach|outreach.io|US|Sales engagement
Salesloft|salesloft.com|US|Sales engagement
ZoomInfo|zoominfo.com|US|B2B data platform
Apollo.io|apollo.io|US|Sales intelligence
Clari|clari.com|US|Revenue platform
Chili Piper|chilipiper.com|US|Meeting scheduling for revenue teams
Highspot|highspot.com|US|Sales enablement
Seismic|seismic.com|US|Sales enablement
Mindtickle|mindtickle.com|US|Sales readiness
Copper|copper.com|US|CRM
Intercom|intercom.com|US|Customer service AI
Zendesk|zendesk.com|US|Customer service software
Front|front.com|US|Customer operations platform
Gorgias|gorgias.com|US|Ecommerce helpdesk
Vercel|vercel.com|US|Frontend cloud
Netlify|netlify.com|US|Web platform
Postman|postman.com|US|API platform
LaunchDarkly|launchdarkly.com|US|Feature management
Sentry|sentry.io|US|Error monitoring
Datadog|datadoghq.com|US|Observability
CircleCI|circleci.com|US|CI CD platform
Retool|retool.com|US|Internal tools builder
Render|render.com|US|Cloud hosting
Twilio|twilio.com|US|Communications API
Algolia|algolia.com|US|Search API
Glean|glean.com|US|Enterprise AI search
Otter.ai|otter.ai|US|AI meeting notes
Fathom|fathom.video|US|AI meeting notes
Ramp|ramp.com|US|Spend management
Brex|brex.com|US|Corporate cards and spend
Mercury|mercury.com|US|Business banking
BILL|bill.com|US|AP and AR automation
Plaid|plaid.com|US|Open banking API
Chargebee|chargebee.com|US|Subscription billing
Recurly|recurly.com|US|Subscription billing
Maxio|maxio.com|US|SaaS billing
Tipalti|tipalti.com|US|Payables automation
Navan|navan.com|US|Travel and expense
Expensify|expensify.com|US|Expense management
Melio|meliopayments.com|US|B2B payments
Novo|novo.co|US|Small business banking
Relay|relayfi.com|US|Business banking
Pilot|pilot.com|US|Startup bookkeeping
Carta|carta.com|US|Equity management
15Five|15five.com|US|Performance management
Workable|workable.com|US|Recruiting software
Amplitude|amplitude.com|US|Product analytics
Mixpanel|mixpanel.com|US|Product analytics
Heap|heap.io|US|Digital insights
FullStory|fullstory.com|US|Digital experience analytics
Pendo|pendo.io|US|Product experience platform
PostHog|posthog.com|US|Product analytics
Vanta|vanta.com|US|Compliance automation
Drata|drata.com|US|Compliance automation
Jotform|jotform.com|US|Form builder
SurveyMonkey|surveymonkey.com|US|Survey software
Qualtrics|qualtrics.com|US|Experience management
Userpilot|userpilot.com|US|Product growth platform
Loopio|loopio.com|US|RFP software
Docebo|docebo.com|US|Learning platform
Paddle|paddle.com|UK|Merchant of record for SaaS
Monzo|monzo.com|UK|Digital bank
Wise|wise.com|UK|International payments
Checkout.com|checkout.com|UK|Payments platform
Modulr|modulrfinance.com|UK|Payments infrastructure
Tide|tide.co|UK|Business banking
Soldo|soldo.com|UK|Spend management
Payhawk|payhawk.com|UK|Spend management
Primer|primer.io|UK|Payments orchestration
Ebury|ebury.com|UK|FX and payments
iwoca|iwoca.co.uk|UK|Business lending
Funding Circle|fundingcircle.com|UK|Business lending
Sage|sage.com|UK|Accounting software
Dext|dext.com|UK|Bookkeeping automation
Charlie HR|charliehr.com|UK|HR software
HiBob|hibob.com|UK|HR platform
Cezanne HR|cezannehr.com|UK|HR software
Beamery|beamery.com|UK|Talent management
Applied|beapplied.com|UK|Hiring software
Perkbox|perkbox.com|UK|Employee benefits
Unmind|unmind.com|UK|Workplace mental health
Spill|spill.chat|UK|Workplace mental health
Attio|attio.com|UK|CRM
Onfido|onfido.com|UK|Identity verification
Multiverse|multiverse.io|UK|Workforce upskilling
Deskpro|deskpro.com|UK|Helpdesk software
Mention Me|mention-me.com|UK|Referral marketing software
Ometria|ometria.com|UK|Customer marketing platform
Dotdigital|dotdigital.com|UK|Customer engagement platform
Snyk|snyk.io|UK|Developer security
Cloudsmith|cloudsmith.com|UK|Package management
Darktrace|darktrace.com|UK|AI cybersecurity
Faculty|faculty.ai|UK|Applied AI company
Peak|peak.ai|UK|AI for business
Luminance|luminance.com|UK|Legal AI
Tractable|tractable.ai|UK|AI for insurance
Ravelin|ravelin.com|UK|Fraud detection
Signal AI|signal-ai.com|UK|Risk and reputation AI
Cytora|cytora.com|UK|Insurance risk platform
Pento|pento.io|UK|Payroll software
Crezco|crezco.com|UK|Account to account payments
Float|floatapp.com|UK|Cash flow forecasting
Satago|satago.com|UK|Cash flow tools
Brightpearl|brightpearl.com|UK|Retail operations software
Planday|planday.com|UK|Workforce scheduling
Rotageek|rotageek.com|UK|Workforce scheduling
Culture Amp UK|cultureamp.com|UK|Employee experience platform
Thought Machine|thoughtmachine.net|UK|Core banking software
Cleo|meetcleo.com|UK|AI money assistant
Zego|zego.com|UK|Commercial insurance
Bud|thisisbud.com|UK|Financial data AI
Yoti|yoti.com|UK|Digital identity
Hopin|hopin.com|UK|Events software
Tabby|tabby.ai|UAE|Buy now pay later
Pemo|pemo.io|UAE|Spend management
Baraka|getbaraka.com|UAE|Investing app
Huspy|huspy.com|UAE|Mortgage platform
Property Finder|propertyfinder.ae|UAE|Property portal
Bayut|bayut.com|UAE|Property portal
Careem|careem.com|UAE|Everyday super app
Kitopi|kitopi.com|UAE|Cloud kitchen platform
Wio|wio.io|UAE|Digital bank
NymCard|nymcard.com|UAE|Card issuing platform
Network International|network.ae|UAE|Payments provider
Telr|telr.com|UAE|Payment gateway
Stake|getstake.com|UAE|Property investing
Mal|mal.ae|UAE|Islamic digital bank
Comfi|comfi.app|UAE|B2B BNPL
CredibleX|crediblex.io|UAE|SME lending
Astra Tech|astratech.ae|UAE|Consumer tech
AXON|axon.ae|UAE|Fintech
Zywa|zywa.co|UAE|Gen Z neobank
Fils|fils.ae|UAE|Sustainable payments
Qashio|qashio.com|UAE|Spend management
Taptap Send|taptapsend.com|UAE|Remittances
Rain|rain.com|UAE|Crypto exchange
Sarwa Trade|sarwatrade.com|UAE|Investing app
Zoho Middle East|zoho.com|UAE|Business software
Emirates Draw|emiratesdraw.com|UAE|Consumer
Deriv|deriv.com|UAE|Trading platform
Anghami|anghami.com|UAE|Music streaming
Talabat|talabat.com|UAE|Delivery platform
Swvl|swvl.com|UAE|Mass transit tech
Nuvei MENA|nuvei.com|UAE|Payments
Pure Harvest|pureharvest.ae|UAE|Agritech
Aspire Zone|aspire.ae|UAE|Business services
Genie|genie.ae|UAE|AI assistant
Hala|hala.com|UAE|Payments
YAP|yap.com|UAE|Digital banking app
Zbooni|zbooni.com|UAE|Social commerce payments
Eden|eden.ae|UAE|Home services platform
Justlife|justlife.com|UAE|Home services platform
Zenda|zenda.com|UAE|School payments
Salt|salt.ae|UAE|B2B SaaS HR and payroll
Hubstaff|hubstaff.com|US|Time tracking software
Toggl|toggl.com|US|Time tracking software
Harvest|getharvest.com|US|Time tracking software
Freshbooks|freshbooks.com|US|Accounting software
Gorilla|gorilla.co|US|Accounting software
Xero US|xero.com|US|Accounting software
Bench|bench.co|US|Bookkeeping
Stripe|stripe.com|US|Payments
Paystand|paystand.com|US|B2B payments
Airbase|airbase.com|US|Spend management
Spendesk|spendesk.com|UK|Spend management
Pleo|pleo.io|UK|Spend management
Personio|personio.com|UK|HR software
Leapsome|leapsome.com|US|People enablement
Lattice Talent|lattice.co|US|Performance management
"""
rows=[]
for seg,txt in (("A",A),("B",B)):
    for line in txt.strip().splitlines():
        n,d,c,s=line.split("|")
        comp="no"; reason=""
        if d in ("vidyard.com","hippovideo.io","sendspark.com","bombbomb.com"): pass
        rows.append(dict(companyName=n,webDomain=d,country=c,serviceType=s,segment=seg,competitor=comp,competitorReason=reason))
w=csv.DictWriter(open("00_candidates.csv","w",newline=""),fieldnames=list(rows[0]))
w.writeheader(); w.writerows(rows)
from collections import Counter
print(len(rows), Counter((r["segment"],r["country"]) for r in rows))
