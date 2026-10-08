async function pageFunction(context) {
    const { $, request, response, body } = context;
    const url = request.loadedUrl || request.url;
    const finalHost = new URL(url).hostname.replace(/^www\./, '');
    const html = typeof body === 'string' ? body : body.toString();
    const adPats = ['doubleclick', 'googlesyndication', 'adsbygoogle', 'taboola', 'outbrain', 'mgid', 'revcontent', 'adnxs', 'criteo', 'media.net', 'amazon-adsystem'];
    const srcs = [];
    $('script[src],iframe[src],link[href]').each((i, el) => {
        srcs.push((($(el).attr('src') || $(el).attr('href') || '') + '').toLowerCase());
    });
    const inline = $('script:not([src])').map((i, el) => $(el).html() || '').get().join(' ').toLowerCase();
    const ads = adPats.filter(p => srcs.some(s => s.includes(p)) || (p === 'adsbygoogle' && inline.includes('adsbygoogle')) || (p === 'googlesyndication' && inline.includes('googlesyndication')));
    const ext = new Set();
    $('a[href]').each((i, el) => {
        try {
            const h = new URL($(el).attr('href'), url).hostname.replace(/^www\./, '');
            if (h && h !== finalHost && !h.endsWith('.' + finalHost) && !finalHost.endsWith('.' + h)) ext.add(h);
        } catch (e) {}
    });
    const blogLinks = [];
    $('a[href]').each((i, el) => {
        const href = $(el).attr('href') || '';
        if (/\/(blog|insights|resources|articles|news|journal|learn|library)(\/|$|\?)/i.test(href) || /^https?:\/\/(blog|insights|resources)\./i.test(href)) blogLinks.push(href);
    });
    const title = $('title').first().text().replace(/\s+/g, ' ').trim();
    const metaDesc = ($('meta[name="description"]').attr('content') || '').replace(/\s+/g, ' ').trim().slice(0, 200);
    const h1 = $('h1').first().text().replace(/\s+/g, ' ').trim().slice(0, 160);
    $('script,style,noscript,svg,template').remove();
    const text = $('body').text().replace(/\s+/g, ' ').trim();
    const lower = text.toLowerCase();
    const farm = ['casino', 'betting', 'sportsbook', 'cbd', 'payday', 'loans', 'viagra', 'escort'].filter(w => new RegExp('\\b' + w + '\\b').test(lower));
    const wfu = /write for us|guest post|contribute to our blog|become a contributor|submit a guest/i.test(text) || $('a[href*="write-for-us"],a[href*="guest-post"]').length > 0;
    const parked = /domain (is )?for sale|buy this domain|this domain may be for sale|parked free/i.test(text);
    return {
        webDomain: request.userData.domain,
        loaded: true,
        httpStatus: response ? response.statusCode : null,
        finalUrl: url,
        adNetworks: ads.join(';'),
        farmWords: farm.join(';'),
        writeForUs: wfu,
        parked,
        outboundLinks: ext.size,
        wordCount: text ? text.split(' ').length : 0,
        title,
        h1,
        metaDesc,
        blogLink: blogLinks[0] || '',
        htmlBytes: html.length
    };
}
