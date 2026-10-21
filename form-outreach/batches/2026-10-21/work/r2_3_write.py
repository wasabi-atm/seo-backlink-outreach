import csv
S="A"
rows=[
("Nonprofit Hub","nonprofithub.org","US","nonprofit communications education"),
("Pursuant","pursuant.com","US","fundraising agency"),
("Lautman Maska Neill","lautmanmaskaneill.com","US","nonprofit fundraising direct marketing agency"),
("DNL OmniMedia","dnlomnimedia.com","US","nonprofit digital and HubSpot agency"),
("Grizzard","grizzard.com","US","fundraising marketing agency"),
("RKD Group","rkdgroup.com","US","nonprofit fundraising marketing agency"),
("Campbell & Company","campbellcompany.com","US","fundraising consultancy"),
("CCS Fundraising","ccsfundraising.com","US","fundraising consultancy"),
("Marts&Lundy","martsandlundy.com","US","fundraising consultancy"),
("Bentz Whaley Flessner","bwf.com","US","fundraising consultancy"),
("GG+A","grenzebachglier.com","US","philanthropy consultancy"),
("Hager Sharp","hagersharp.com","US","social impact communications firm"),
("Burness","burness.com","US","nonprofit communications firm"),
("Mission Minded","missionminded.com","US","nonprofit brand strategy firm"),
("Aly Sterling Philanthropy","alysterling.com","US","nonprofit fundraising consultancy"),
("Dunham+Company","dunhamandcompany.com","US","nonprofit fundraising marketing agency"),
("Graham-Pelton","grahampelton.com","US","fundraising consultancy"),
("TWB Fundraising","twbfundraising.com","US","fundraising agency"),
("Vanguard Communications","vancomm.com","US","social impact communications firm"),
("Resource Media","resource-media.org","US","nonprofit communications consultancy"),
("Precision Marketing Group","precisionmarketinggroup.com","US","HubSpot inbound marketing agency"),
("InboxArmy","inboxarmy.com","US","email marketing agency"),
("Ignyte Branding","ignytebrands.com","US","brand strategy firm"),
("Monigle","monigle.com","US","brand strategy consultancy"),
("BrandingBusiness","brandingbusiness.com","US","B2B brand strategy firm"),
("Tronvig","tronviggroup.com","US","brand strategy agency"),
("ContentBacon","contentbacon.com","US","content marketing agency"),
("Simple Strat","simplestrat.com","US","HubSpot partner agency"),
("Bluefrog","bluefroglondon.com","UK","charity fundraising agency"),
("Open Fundraising","openfundraising.co.uk","UK","charity fundraising agency"),
("Good Agency","goodagency.co.uk","UK","charity brand and fundraising agency"),
("Revolutionise","revolutionise.com","UK","fundraising consultancy"),
("Cause4","cause4.co.uk","UK","charity fundraising consultancy"),
("Platypus Digital","platypusdigital.co.uk","UK","charity digital marketing agency"),
("WPNC","wpnc.co.uk","UK","charity fundraising agency"),
("More Partnership","morepartnership.com","UK","fundraising consultancy"),
("Lyntons","lyntons.com","UK","HubSpot inbound marketing agency"),
("Holistic Email Marketing","holisticemail.com","UK","email marketing consultancy"),
("Jarrang","jarrang.com","UK","email marketing agency"),
("Think Consulting Solutions","thinkcs.org","UK","charity fundraising consultancy"),
]
assert len(set(r[1] for r in rows))==len(rows)
with open('cand_r2_3.csv','w',newline='') as f:
    w=csv.writer(f);w.writerow(["companyName","webDomain","country","serviceType","segment","articleHint"])
    for r in rows:
        hint="https://simplestrat.com/blog/simple-strat-soars-to-top-1-of-hubspot-agencies-nationwide" if False else ""
        w.writerow([*r,S,hint])
print(len(rows))
