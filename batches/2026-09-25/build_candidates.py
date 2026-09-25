"""Build 00_candidates.csv: the 95 unvetted DR 40+ rows from backlink-2026-09-23-b plus new candidates.
Line format: companyName|webDomain|country|serviceType|segment|competitor reason (blank = not a competitor)."""
import csv

NEW = """
Croud|croud.com|UK|Digital marketing agency|A|
Journey Further|journeyfurther.com|UK|Performance marketing agency|A|
Search Laboratory|searchlaboratory.com|UK|Search marketing agency|A|
Stickyeyes|stickyeyes.com|UK|Search and content agency|A|
Jaywing|jaywing.com|UK|Data and search marketing agency|A|
Blueclaw|blueclaw.co.uk|UK|SEO and digital PR agency|A|
Liberty Marketing|libertymarketing.co.uk|UK|SEO and PPC agency|A|
Glass Digital|glass.digital|UK|SEO agency|A|
Found|found.co.uk|UK|Search marketing agency|A|
Coast Digital|coast-digital.co.uk|UK|Digital marketing agency|A|
Reflect Digital|reflectdigital.co.uk|UK|Digital marketing agency|A|
Loud Mouth Media|loudmouthmedia.co.uk|UK|PPC and paid social agency|A|
Embryo|embryo.com|UK|Digital marketing agency|A|
Mediaworks|mediaworks.co.uk|UK|Digital marketing agency|A|
Ricemedia|ricemedia.co.uk|UK|SEO and PPC agency|A|
Six & Flow|sixandflow.com|UK|B2B growth agency|A|
Gripped|gripped.io|UK|B2B tech marketing agency|A|
Ledger Bennett|ledgerbennett.com|UK|B2B demand gen agency|A|
Fifty Five and Five|fiftyfiveandfive.com|UK|B2B tech marketing agency|A|
The Marketing Practice|themarketingpractice.com|UK|B2B marketing agency|A|
Gravity Global|gravityglobal.com|UK|B2B marketing agency|A|
Twogether|twogether-group.com|UK|B2B marketing agency|A|
Man Bites Dog|manbitesdog.com|UK|B2B thought leadership agency|A|
Hard Numbers|hardnumbers.co.uk|UK|B2B PR agency|A|
Aspectus|aspectusgroup.com|UK|B2B PR and marketing agency|A|
Cognito|wearecognito.com|UK|Fintech PR and marketing agency|A|
Tyto PR|tyto.co.uk|UK|Tech PR agency|A|
Babel PR|babelpr.com|UK|Tech PR agency|A|
AxiCom|axicom.com|UK|Tech PR agency|A|
Onclusive|onclusive.com|UK|PR measurement software|A|
BrightLocal|brightlocal.com|UK|Local SEO software|A|
Turtl|turtl.co|UK|Content format platform|A|
Sendible|sendible.com|UK|Social media management software|A|
Orlo|orlo.tech|UK|Social media management software|A|
Echobox|echobox.com|UK|Social publishing software|A|
Adzooma|adzooma.com|UK|Ad management software|A|
Adthena|adthena.com|UK|Search ad intelligence software|A|
Pure360|pure360.com|UK|Email marketing software|A|
Feefo|feefo.com|UK|Reviews platform|A|
REVIEWS.io|reviews.io|UK|Reviews platform|A|
Quill Podcasting|quillpodcasting.com|UK|Podcast production agency|A|
Rephonic|rephonic.com|UK|Podcast data platform|A|
Audioboom|audioboom.com|UK|Podcast platform|A|
Lead Forensics|leadforensics.com|UK|B2B website visitor tracking software|A|
Kota|kota.co.uk|UK|Web design agency|A|
Code Computerlove|codecomputerlove.com|UK|Digital product agency|A|
Distinctly|distinctly.co.uk|UK|Digital PR and SEO agency|A|
Stratton Craig|strattoncraig.co.uk|UK|Copywriting agency|A|
Smart Insights|smartinsights.com|UK|Digital marketing training platform|A|
Vidsy|vidsy.co|UK|Creator video ad production|A|Makes short-form video ads for brands
Dubb|dubb.com|US|Video sales platform|A|
Vidalytics|vidalytics.com|US|Video hosting for marketers|A|
SproutVideo|sproutvideo.com|US|Video hosting platform|A|
Dacast|dacast.com|US|Video streaming platform|A|
Panopto|panopto.com|US|Video platform|A|
Kaltura|kaltura.com|US|Video platform|A|
Vbrick|vbrick.com|US|Enterprise video platform|A|
ON24|on24.com|US|Webinar platform|A|
BigMarker|bigmarker.com|US|Webinar platform|A|
Demio|demio.com|US|Webinar platform|A|
Bizzabo|bizzabo.com|US|Event platform|A|
Ziflow|ziflow.com|US|Creative proofing software|A|
Brandfolder|brandfolder.com|US|Digital asset management|A|
Air|air.inc|US|Creative operations platform|A|
Loomly|loomly.com|US|Social media management software|A|
Conductor|conductor.com|US|SEO platform|A|
BrightEdge|brightedge.com|US|SEO platform|A|
seoClarity|seoclarity.net|US|SEO platform|A|
Botify|botify.com|US|SEO platform|A|
Optimizely|optimizely.com|US|Digital experience platform|A|
Mutiny|mutinyhq.com|US|Website personalisation software|A|
Litmus|litmus.com|US|Email marketing software|A|
Customer.io|customer.io|US|Messaging automation software|A|
Iterable|iterable.com|US|Customer engagement platform|A|
Braze|braze.com|US|Customer engagement platform|A|
Terminus|terminus.com|US|ABM platform|A|
RollWorks|rollworks.com|US|ABM platform|A|
Metadata.io|metadata.io|US|B2B ad automation|A|
Bombora|bombora.com|US|B2B intent data|A|
Navattic|navattic.com|US|Interactive demo software|A|
Storylane|storylane.io|US|Interactive demo software|A|
Walnut|walnut.io|US|Interactive demo software|A|
Arcade|arcade.software|US|Interactive demo software|A|
Consensus|goconsensus.com|US|Video demo automation|A|
Typeface|typeface.ai|US|AI content platform|A|
Anyword|anyword.com|US|AI copywriting software|A|
Duda|duda.co|US|Website builder for agencies|A|
Zencastr|zencastr.com|US|Podcast recording platform|A|
Libsyn|libsyn.com|US|Podcast hosting|A|
Castos|castos.com|US|Podcast hosting|A|
Highwire PR|highwirepr.com|US|Tech PR agency|A|
Bospar|bospar.com|US|Tech PR agency|A|
SHIFT Communications|shiftcomm.com|US|PR agency|A|
Matter Communications|matternow.com|US|Tech PR and marketing agency|A|
Inkhouse|inkhouse.com|US|PR agency|A|
PAN Communications|pancommunications.com|US|B2B tech PR agency|A|
BLASTmedia|blastmedia.com|US|B2B SaaS PR agency|A|
Barrel|barrelny.com|US|Digital agency|A|
Digital Silk|digitalsilk.com|US|Web design agency|A|
Huemor|huemor.rocks|US|Web design agency|A|
Big Human|bighuman.com|US|Brand and digital studio|A|
Heinz Marketing|heinzmarketing.com|US|B2B marketing consultancy|A|
Revenue River|revenueriver.co|US|B2B marketing agency|A|
Hawke Media|hawkemedia.com|US|Marketing agency|A|
Disruptive Advertising|disruptiveadvertising.com|US|Paid media agency|A|
Stratabeat|stratabeat.com|US|B2B branding and web agency|A|
Hinge Marketing|hingemarketing.com|US|Professional services marketing agency|A|
Express Writers|expresswriters.com|US|Content writing agency|A|
Compose.ly|compose.ly|US|Content writing service|A|
WriterAccess|writeraccess.com|US|Content writing platform|A|
Ceros|ceros.com|US|Interactive content platform|A|
Wave.video|wave.video|US|Online video maker|A|
Vyond|vyond.com|US|Animated video software|A|Sells software for making animated explainer videos
Column Five|columnfivemedia.com|US|Content and design agency|A|Creative agency that makes infographics, motion graphics and video
Red Berries|redberries.ae|UAE|B2B tech PR agency|A|
Sherpa Communications|sherpacomms.com|UAE|B2B PR agency|A|
ZECOMMS|zecomms.com|UAE|Tech PR agency|A|
OBA PR|obapr.com|UAE|PR agency|A|
Pella Dynamics|pelladynamics.com|UAE|Tech PR agency|A|
PRHub|prhub.ae|UAE|PR agency|A|
TishTash|tishtash.ae|UAE|PR and communications agency|A|
Seven Media|sevenmedia.ae|UAE|PR agency|A|
Volga Tigris|volgatigris.com|UAE|Digital marketing agency|A|
DiMarketo|dimarketo.com|UAE|Digital marketing agency|A|
C2C Media|c2cmedia.ae|UAE|Digital marketing agency|A|
RedSpider|redspider.ae|UAE|Web design agency|A|
Peniel Tech|penieltech.com|UAE|Web design agency|A|
GO-Gulf|go-gulf.ae|UAE|Web design and digital agency|A|
Emirates Graphic|emiratesgraphic.com|UAE|Web design agency|A|
Flow Digital|flow-digital.com|UAE|Digital agency|A|
Hug Digital|hugdigital.com|UAE|Digital marketing agency|A|
Create Media Group|createmediagroup.com|UAE|Digital agency|A|
MAGNiTT|magnitt.com|UAE|Startup data platform|B|
BitOasis|bitoasis.net|UAE|Crypto exchange|B|
Cashew|cashewpayments.com|UAE|Buy now pay later|B|
Postpay|postpay.io|UAE|Buy now pay later|B|
Beehive|beehive.ae|UAE|SME lending platform|B|
NOW Money|nowmoney.me|UAE|Payroll banking fintech|B|
SmartCrowd|smartcrowd.ae|UAE|Property investment platform|B|
PRYPCO|prypco.com|UAE|Proptech platform|B|
Holo|holo.ae|UAE|Mortgage platform|B|
Tenderd|tenderd.com|UAE|Construction fleet software|B|
TruKKer|trukker.com|UAE|Freight logistics platform|B|
Quiqup|quiqup.com|UAE|Ecommerce logistics|B|
Magnati|magnati.com|UAE|Payments provider|B|
Nomod|nomod.com|UAE|Mobile payments app|B|
Grubtech|grubtech.com|UAE|Restaurant operations SaaS|B|
Sapaad|sapaad.com|UAE|Restaurant POS software|B|
Supy|supy.io|UAE|Restaurant inventory software|B|
Virtuzone|vzone.ae|UAE|Company formation services|B|
Creative Zone|creativezone.ae|UAE|Company formation services|B|
Shuraa|shuraa.com|UAE|Company formation services|B|
Alef Education|alefeducation.com|UAE|Edtech platform|B|
Aramex|aramex.com|UAE|Logistics|B|
Lean Technologies|leantech.me|UAE|Open banking API|B|
Qlub|qlub.io|UAE|Restaurant payments|B|
Uqudo|uqudo.com|UAE|Identity verification|B|
Pluto|getpluto.com|UAE|Spend management|B|
Fuze|fuze.finance|UAE|Digital asset infrastructure|B|
Fasset|fasset.com|UAE|Digital asset platform|B|
Willo|willo.video|UK|Video interviewing software|B|
Kayako|kayako.com|UK|Customer support software|B|
CybSafe|cybsafe.com|UK|Security awareness software|B|
Egress|egress.com|UK|Email security software|B|
Immersive Labs|immersivelabs.com|UK|Cyber skills platform|B|
Intruder|intruder.io|UK|Vulnerability scanning software|B|
ComplyAdvantage|complyadvantage.com|UK|AML compliance software|B|
Sumsub|sumsub.com|UK|Identity verification|B|
Featurespace|featurespace.com|UK|Fraud prevention software|B|
Allica Bank|allica.bank|UK|SME bank|B|
OakNorth|oaknorth.co.uk|UK|SME lender|B|
ClearBank|clear.bank|UK|Clearing bank infrastructure|B|
Railsr|railsr.com|UK|Embedded finance platform|B|
Banked|banked.com|UK|Account-to-account payments|B|
Token.io|token.io|UK|Open banking payments|B|
Volt|volt.io|UK|Real-time payments|B|
Ecommpay|ecommpay.com|UK|Payment provider|B|
Equals Money|equalsmoney.com|UK|Business payments|B|
Capital on Tap|capitalontap.com|UK|Business credit cards|B|
Codat|codat.io|UK|Business data API|B|
Superscript|gosuperscript.com|UK|Business insurance|B|
Hokodo|hokodo.co|UK|B2B buy now pay later|B|
Kriya|kriya.co|UK|B2B payments and finance|B|
Duco|du.co|UK|Data reconciliation software|B|
Sonovate|sonovate.com|UK|Recruitment finance|B|
Tillo|tillo.io|UK|Gift card platform|B|
Dojo|dojo.tech|UK|Card payments for business|B|
Quantexa|quantexa.com|UK|Decision intelligence software|B|
Behavox|behavox.com|UK|Compliance AI software|B|
Ably|ably.com|UK|Realtime messaging API|B|
Tray.ai|tray.ai|UK|Integration platform|B|
Unily|unily.com|UK|Employee experience platform|B|
Blink|joinblink.com|UK|Frontline employee app|B|
Juro|juro.com|UK|Contract management software|B|
Legl|legl.com|UK|Law firm software|B|
Cledara|cledara.com|UK|SaaS management software|B|
Capsule CRM|capsulecrm.com|UK|CRM software|B|
Kallidus|kallidus.com|UK|Learning and talent software|B|
Learning Pool|learningpool.com|UK|Learning software|B|
Filtered|filtered.com|UK|Learning software|B|
Hive HR|hive.hr|UK|Employee voice software|B|
Zinc|zincwork.com|UK|Background check software|B|
Tribepad|tribepad.com|UK|Recruitment software|B|
Ciphr|ciphr.com|UK|HR software|B|
RotaCloud|rotacloud.com|UK|Staff scheduling software|B|
Fourth|fourth.com|UK|Hospitality workforce software|B|
Moneypenny|moneypenny.com|UK|Outsourced call answering|B|
Coda|coda.io|US|Docs and workflow software|B|
Lucid|lucid.co|US|Visual collaboration software|B|
Miro|miro.com|US|Visual collaboration software|B|
Betterworks|betterworks.com|US|Performance management software|B|
Bonusly|bonus.ly|US|Employee recognition software|B|
SmartRecruiters|smartrecruiters.com|US|Recruiting software|B|
HireVue|hirevue.com|US|Video interviewing software|B|
Spark Hire|sparkhire.com|US|Video interviewing software|B|
Pipedrive|pipedrive.com|US|CRM software|B|
Allego|allego.com|US|Sales enablement software|B|
Gainsight|gainsight.com|US|Customer success software|B|
ChurnZero|churnzero.com|US|Customer success software|B|
Vitally|vitally.io|US|Customer success software|B|
Crossbeam|crossbeam.com|US|Partner ecosystem software|B|
Kustomer|kustomer.com|US|Customer service CRM|B|
Gladly|gladly.com|US|Customer service software|B|
LogRocket|logrocket.com|US|Product analytics software|B|
Productboard|productboard.com|US|Product management software|B|
Aha!|aha.io|US|Product roadmap software|B|
Canny|canny.io|US|Feedback management software|B|
UserTesting|usertesting.com|US|User research platform|B|
Whatfix|whatfix.com|US|Digital adoption platform|B|
Scribe|scribehow.com|US|Process documentation software|B|
GitLab|gitlab.com|US|DevOps platform|B|
PagerDuty|pagerduty.com|US|Incident management software|B|
Grafana Labs|grafana.com|US|Observability software|B|
Supabase|supabase.com|US|Database platform|B|
Airbyte|airbyte.com|US|Data integration platform|B|
Hex|hex.tech|US|Data analytics platform|B|
Metabase|metabase.com|US|Business intelligence software|B|
Secureframe|secureframe.com|US|Compliance automation|B|
Huntress|huntress.com|US|Managed security platform|B|
Persona|withpersona.com|US|Identity verification|B|
Alloy|alloy.com|US|Identity and fraud platform|B|
Rho|rho.co|US|Business banking|B|
Emburse|emburse.com|US|Expense management software|B|
Zip|ziphq.com|US|Procurement software|B|
Routable|routable.com|US|Accounts payable automation|B|
Stampli|stampli.com|US|Accounts payable automation|B|
FloQast|floqast.com|US|Accounting close software|B|
Mosaic|mosaic.tech|US|Strategic finance software|B|
Cube|cubesoftware.com|US|FP&A software|B|
Modern Treasury|moderntreasury.com|US|Payment operations software|B|
Unit|unit.co|US|Embedded banking platform|B|
Dwolla|dwolla.com|US|Payments API|B|
Zuora|zuora.com|US|Subscription billing software|B|
Baremetrics|baremetrics.com|US|Subscription analytics|B|
Oyster|oysterhr.com|US|Global employment platform|B|
Papaya Global|papayaglobal.com|US|Global payroll platform|B|
Vendr|vendr.com|US|SaaS buying platform|B|
Ironclad|ironcladapp.com|US|Contract management software|B|
Simpplr|simpplr.com|US|Employee intranet software|B|
"""

rows = []
for line in NEW.strip().splitlines():
    name, dom, country, svc, seg, comp = line.split("|")
    rows.append(dict(companyName=name, webDomain=dom, country=country, serviceType=svc, segment=seg,
                     competitor="yes" if comp else "no", competitorReason=comp, source="new"))
for r in csv.DictReader(open("../2026-09-23-b/01_needs_check.csv")):
    rows.append(dict(companyName=r["companyName"], webDomain=r["webDomain"], country=r["country"],
                     serviceType=r["serviceType"], segment=r["segment"], competitor=r["competitor"] or "no",
                     competitorReason="", source="2026-09-23-b needs_check"))
cols = ["companyName", "webDomain", "country", "serviceType", "segment", "competitor", "competitorReason", "source"]
with open("00_candidates.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)
from collections import Counter
print(len(rows), Counter((r["segment"], r["country"]) for r in rows))
