async function pageFunction(context) {
    const { $, request } = context;
    const url = request.loadedUrl || request.url;
    const base = new URL(url);
    const root = base.hostname.replace(/^www\./, '').split('.').slice(-2).join('.');
    $('nav,[role=navigation],[role=banner],[role=contentinfo],body > header,body > footer,body > div > header,body > div > footer,[class*=site-header],[class*=site-footer],[class*=navbar],[class*=mega-menu],#header,#footer').remove();
    const seen = new Set();
    const posts = [];
    $('a[href]').each((i, el) => {
        let href = $(el).attr('href') || '';
        let u;
        try { u = new URL(href, url); } catch (e) { return; }
        if (!u.hostname.replace(/^www\./, '').endsWith(root)) return;
        u.hash = ''; u.search = '';
        const path = u.pathname.replace(/\/$/, '');
        if (path.split('/').filter(Boolean).length < 1) return;
        if (/\/(tag|tags|category|categories|author|authors|page|search|login|signup|pricing|contact|about|careers|privacy|terms|demo)(\/|$)/i.test(path)) return;
        if (/\.(pdf|png|jpg|jpeg|gif|svg|zip)$/i.test(path)) return;
        const text = $(el).text().replace(/\s+/g, ' ').trim();
        const key = u.toString();
        if (seen.has(key)) { const p = posts.find(x => x.url === key); if (p && text.length > p.title.length) p.title = text.slice(0, 160); return; }
        seen.add(key);
        if (key.replace(/\/$/, '') === url.replace(/\/$/, '')) return;
        const card = $(el).closest('article,li,div');
        const dt = card.find('time').attr('datetime') || card.find('time').text() || '';
        posts.push({ url: key, title: text.slice(0, 160), date: (dt || '').trim().slice(0, 40) });
    });
    const keep = posts.filter(p => p.title.length >= 15).slice(0, 40);
    return {
        webDomain: request.userData.domain,
        indexUrl: url,
        contributorLink: /write for us|contribute|guest post|become a contributor/i.test($('body').text()),
        posts: keep
    };
}
