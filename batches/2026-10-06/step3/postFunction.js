async function pageFunction(context) {
    const { $, request } = context;
    const url = request.loadedUrl || request.url;
    const host = new URL(url).hostname.replace(/^www\./, '');
    const root = host.split('.').slice(-2).join('.');
    let published = $('meta[property="article:published_time"]').attr('content') || '';
    let modified = $('meta[property="article:modified_time"]').attr('content') || '';
    let author = $('meta[name="author"]').attr('content') || '';
    $('script[type="application/ld+json"]').each((i, el) => {
        const t = $(el).html() || '';
        const p = t.match(/"datePublished"\s*:\s*"([^"]+)"/); if (p && !published) published = p[1];
        const m = t.match(/"dateModified"\s*:\s*"([^"]+)"/); if (m && !modified) modified = m[1];
        const a = t.match(/"author"\s*:\s*\{[^}]*"name"\s*:\s*"([^"]+)"/); if (a && !author) author = a[1];
    });
    if (!published) published = $('time[datetime]').first().attr('datetime') || '';
    const h1 = $('h1').first().text().replace(/\s+/g, ' ').trim().slice(0, 160);
    const title = $('title').first().text().replace(/\s+/g, ' ').trim().slice(0, 160);
    $('script,style,noscript,svg,template,header,nav,footer,aside,form,[role=navigation],[class*=related],[class*=share],[class*=social],[class*=newsletter],[class*=sidebar],[class*=footer],[class*=header],[class*=menu],[class*=cta],[class*=comment],#comments,[class*=author-bio],[class*=breadcrumb]').remove();
    let body = null, best = 0;
    $('[class*=post-content], [class*=entry-content], [class*=article-body], [class*=article-content], [class*=blog-content], [class*=rich-text], [class*=post-body], [class*=prose], article, main').each((i, el) => {
        const n = $(el).text().replace(/\s+/g, ' ').trim().length;
        if (n > best) { best = n; body = $(el); }
    });
    if (!body || best < 400) body = $('body');
    const skip = /(^|\.)(twitter|x|linkedin|facebook|instagram|youtube|youtu|tiktok|pinterest|google|goo|apple|apps\.apple|play\.google|wikipedia|wikimedia|bit|t|lnkd|vimeo|wistia|gravatar|wp|wordpress|cloudflare|amazonaws|hubspot|hs-sites|calendly|typeform|medium|reddit|github|gstatic|doubleclick)\.[a-z.]+$/i;
    const domains = {};
    body.find('a[href]').each((i, el) => {
        let u;
        try { u = new URL($(el).attr('href'), url); } catch (e) { return; }
        if (!/^https?:$/.test(u.protocol)) return;
        const h = u.hostname.replace(/^www\./, '');
        if (!h || h.endsWith(root) || skip.test(h)) return;
        domains[h] = (domains[h] || 0) + 1;
    });
    const text = body.text().replace(/\s+/g, ' ').trim();
    const quoteHits = (text.match(/\b(founder|co-founder|ceo|cmo|cto|head of|director|vp|vice president|managing director|partner) (of|at) [A-Z][\w&.-]+/gi) || []).slice(0, 5);
    return {
        webDomain: request.userData.domain,
        url,
        title,
        h1,
        published: published.slice(0, 25),
        modified: modified.slice(0, 25),
        author: author.slice(0, 80),
        words: text ? text.split(' ').length : 0,
        outsideDomains: Object.keys(domains),
        h2: body.find('h2').map((i, el) => $(el).text().replace(/\s+/g, ' ').trim().slice(0, 90)).get().slice(0, 15),
        images: body.find('img').length,
        videoEmbeds: body.find('iframe[src*=youtube],iframe[src*=vimeo],iframe[src*=wistia],iframe[src*=loom],video,[class*=wistia],[class*=vidyard]').length,
        quoteHits
    };
}
