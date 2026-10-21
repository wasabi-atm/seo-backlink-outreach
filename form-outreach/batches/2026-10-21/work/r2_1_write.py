import csv
rows = """Formidable Forms|formidableforms.com|US|WordPress form builder plugin
ConvertBox|convertbox.com|US|On-site popup and form software
Picreel|picreel.com|US|Exit intent popup software
Teamgate|teamgate.com|UK|Sales CRM for small business
Endorsal|endorsal.io|UK|Testimonial and review software
Perkville|perkville.com|US|Loyalty and referral software
Loopy Loyalty|loopyloyalty.com|UK|Digital loyalty card software
GrowSurf|growsurf.com|US|Referral program software
Referral Factory|referral-factory.com|UK|Referral program software
KickoffLabs|kickofflabs.com|US|Viral referral and giveaway software
Dub|dub.co|US|Link management platform
Pretty Links|prettylinks.com|US|WordPress link management plugin
Kissmetrics|kissmetrics.io|US|Product and marketing analytics
PPC Protect|ppcprotect.com|UK|Click fraud protection software
CANDDi|canddi.com|UK|Website visitor tracking and analytics
Malomo|malomo.com|US|Ecommerce shipment tracking marketing app
Elegant Themes|elegantthemes.com|US|WordPress themes and Divi builder
Beaver Builder|wpbeaverbuilder.com|US|WordPress page builder plugin
UpdraftPlus|updraftplus.com|UK|WordPress backup plugin
SearchWP|searchwp.com|US|WordPress search plugin
WP Fusion|wpfusion.com|US|WordPress CRM and marketing automation plugin
GrowthBar|growthbar.com|US|SEO and AI content tool
Delivra|delivra.com|US|Email marketing software
SocketLabs|socketlabs.com|US|Email delivery platform
Call-Loop|callloop.com|US|SMS marketing software
TextAnywhere|textanywhere.com|UK|Business SMS platform
Text Marketer|textmarketer.co.uk|UK|SMS marketing platform
dlvr.it|dlvr.it|US|Social media auto posting tool
Annex Cloud|annexcloud.com|US|Loyalty and referral platform
Zinrelo|zinrelo.com|US|Loyalty rewards platform
WordFly|wordfly.com|US|Email marketing for arts organisations
Digioh|digioh.com|US|Popups forms and quizzes software
KnoCommerce|knocommerce.com|US|Post purchase survey app for ecommerce
OptimizePress|optimizepress.com|UK|WordPress landing page and funnel builder
Paid Memberships Pro|paidmembershipspro.com|US|WordPress membership plugin
Popup Maker|wppopupmaker.com|US|WordPress popup plugin
Ultimate Member|ultimatemember.com|UK|WordPress membership and community plugin
Warfare Plugins|warfareplugins.com|US|WordPress social sharing plugin
ShareThis|sharethis.com|US|Social sharing tools
tinyEmail|tinyemail.com|US|Email marketing software"""
out = []
for l in rows.splitlines():
    n,d,c,s = l.split('|')
    out.append([n,d,c,s,'A',''])
assert len(set(r[1] for r in out)) == len(out)
w = csv.writer(open('cand_r2_1.csv','w',newline=''))
w.writerow(['companyName','webDomain','country','serviceType','segment','articleHint'])
w.writerows(out)
open('r2_1_domains.txt','w').write('\n'.join(r[1] for r in out))
print(len(out))
