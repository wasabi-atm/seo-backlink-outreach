H={
'Cemoh':'Under "Picking Your Marketing Channels" the Content Marketing and SEO path lists videos as helpful content, though the post only uses images.',
'Excite Media':'The "Video content" section says sometimes showing really is better than telling, but there\'s no video in the post, only images.',
'AroFlo':'Section 4, "Use Social Media for Online Marketing", says tutorial videos can do amazing things for an electrician\'s advertising, and the 3,200 word guide doesn\'t have one.',
'Vivi':'The post recaps a webinar where Adam from Woodleigh talks about playing rich video on campus screens, but the recap is just text and photos, with no clip from the session.',
'Moodle':'Under "Practical applications of microlearning" the post suggests sending a three-minute explainer before a meeting, and "Designing effective microlearning" covers video scripts, but there\'s no video on the page.',
'Lyrebird Health':'The section "Choose the format before choosing the file" says a video can teach technique, and the seven-point check covers any handout, PDF or video. The guide has no video of its own.',
'Hatch':'The interview asks why the Tracksuit brand has gone so viral on the ANZ tech scene and mentions creating social content, but the post doesn\'t show any of that brand work.',
'Boylen':'The post quotes BrightEdge research listing Videos among the SERP features that push organic results down, and the article itself has three images and no video.',
'Hospitable':'The social media section tells hosts to "update your photos and videos", but the 3,400 word guide has no video in it.',
'LifterLMS':'Tip 7, "Create Video Testimonials", tells course creators to use video, but there\'s none in the post, and the byline still says Posted on July 27, 2021.',
'Media Shower':'All five use cases, including "Teach a practical skill" and "Explain original data", follow the same How to use it, Why it works and How to do it breakdown, each with an embedded example.',
'EBI.AI':'Idea 16 says personalised content like blog posts, videos and infographics reaches the right audience, and idea 20 backs live product demos, but the post has no video.',
'Red Door Interactive':'The "Interactive Email Experiences" trend mentions product carousels, forms and polls in the inbox, but video and animated GIFs never come up.',
'Four Kitchens':'The "Refresh vs. redesign" section puts refresh timelines at six to 12 weeks rather than six to 12 months.',
'Clockwork':'The closing section leans on the McKinsey Design Index link between design and business performance, but the post has just one image to show what good experience design looks like.',
'Current Agency':'The "Motion as a Brand Asset" part says static guidelines don\'t cover motion and that pace, easing and personality matter, but the post has no images or motion examples.',
'Third and Grove':'The post opens by saying "8 in 10 shoppers say high-quality images and video directly influence whether they buy", and the piece has four images and no video.',
'BrandExtract':'Under "The Test: Performance or Resonance" you call referral and unpaid mentions "close to a gold standard", and the post is all text apart from one image, with no chart of those proxies.',
'Odd Dog Media':'The first point, "Video shows rather than tells", makes the case for a short video, but the post has one image and no video, and still shows its April 6, 2020 date.',
'Arrows':'Section 3 lists six content blocks your best customers use, including "A curated product/demo library (videos, guides, etc.)", but only as a plain bullet list.',
'Sendbird':'The Acquisition stage says adding "a short video with text captions" will help grab attention, but the 4,000 word guide has 39 images and no video.',
'GPTZero':'Under "Content types and formats" the post says 31% of businesses now make short videos with AI. There\'s no video in it, and it was last updated in March 2025.',
}
import json
M=json.load(open('messages_draft.json')); T=json.load(open('targets_draft.json'))
for m,t in zip(M,T):
    n=m['companyName']
    if n in H:
        old=t['articleHook']; assert old in m['messageText'],n
        m['messageText']=m['messageText'].replace(old,H[n]); t['articleHook']=H[n]
json.dump(M,open('messages_final.json','w'),indent=1); json.dump(T,open('targets_final.json','w'),indent=1)
bad=[m['companyName'] for m in M if any(c in m['messageText'] for c in '—–“”')]
print('dash/curly:',bad)
for m in M: print(len(m['messageText']), m['companyName'])
print(M[0]['messageText']); print('----'); print(M[46]['messageText']); print('----'); print(M[8]['messageText'])
