const SM = async () => { const o={src:[],hits:[]}; const P=new DOMParser(); const g=async u=>{try{const r=await fetch(u,{credentials:'omit'}); if(r.status>=400) return null; return P.parseFromString(await r.text(),'text/xml');}catch(e){return null}}; let d=null; for (const p of ['/sitemap_index.xml','/sitemap.xml','/post-sitemap.xml','/wp-sitemap.xml']){ d=await g(location.origin+p); if(d&&d.querySelector('loc')){o.src.push(p);break;} } if(!d) return o; let urls=[]; const idx=[...d.querySelectorAll('sitemap > loc')].map(x=>x.textContent.trim()); if(idx.length){ o.idx=idx.slice(0,30); const pick=idx.filter(u=>/post|blog|article|resource|news|insight|guide/i.test(u)&&!/tag|categor|author/i.test(u)).slice(0,6); for(const u of pick){const dd=await g(u); if(dd) urls.push(...[...dd.querySelectorAll('url')].map(x=>({l:x.querySelector('loc')?.textContent.trim(),m:(x.querySelector('lastmod')?.textContent||'').slice(0,10)})));} } else urls=[...d.querySelectorAll('url')].map(x=>({l:x.querySelector('loc')?.textContent.trim(),m:(x.querySelector('lastmod')?.textContent||'').slice(0,10)})); o.total=urls.length; const re=/video|market|brand|content|social|advert|\bads?\b|campaign|email|seo|visual|design|promot|engag|launch|story|referral|growth|youtube|tiktok|instagram|graphic|creative|website|landing|funnel|fundrais|donor|communicat|newsletter|sms/i; o.hits=urls.filter(u=>u.l&&re.test(u.l.split('/').slice(3).join('/'))&&(!u.m||u.m>='2024-10-21')).sort((a,b)=>b.m.localeCompare(a.m)).slice(0,40).map(u=>u.m+' '+u.l.replace(location.origin,'')); return o; };
const SCAN = (async (ARTICLE) => {
  const out = { origin: location.origin, home: location.href, pages: [], article: null, errors: [] };
  const P = new DOMParser();
  const get = async (u) => {
    try {
      const r = await fetch(u, { credentials: 'omit', redirect: 'follow' });
      const t = await r.text();
      return { status: r.status, url: r.url, doc: P.parseFromString(t, 'text/html'), html: t };
    } catch (e) { out.errors.push(u + ': ' + e.message); return null; }
  };
  const labelOf = (doc, el) => {
    let l = '';
    if (el.id) { const lb = doc.querySelector('label[for="' + CSS.escape(el.id) + '"]'); if (lb) l = lb.textContent; }
    if (!l) { const p = el.closest('label'); if (p) l = p.textContent; }
    if (!l) l = el.getAttribute('aria-label') || el.getAttribute('placeholder') || el.name || '';
    return l.replace(/\s+/g, ' ').trim().slice(0, 60);
  };
  const scanDoc = (doc, html) => {
    const forms = [];
    doc.querySelectorAll('form').forEach(f => {
      const fields = [];
      f.querySelectorAll('input,textarea,select').forEach(el => {
        const ty = (el.type || el.tagName).toLowerCase();
        if (['hidden', 'submit', 'button', 'image', 'reset'].includes(ty)) return;
        const o = { l: labelOf(doc, el), t: ty === 'textarea' ? 'TEXTAREA' : ty };
        if (el.required || el.getAttribute('aria-required') === 'true') o.req = 1;
        if (el.maxLength > 0 && el.maxLength < 100000) o.max = el.maxLength;
        if (el.tagName === 'SELECT') o.opts = [...el.options].map(x => x.text.trim()).filter(Boolean).slice(0, 15);
        fields.push(o);
      });
      const txt = fields.map(x => x.l).join(' ').toLowerCase();
      if (fields.length < 2 || /search|newsletter|subscribe/.test(txt) && fields.length < 3) return;
      forms.push({ action: (f.getAttribute('action') || '').slice(0, 80), fields });
    });
    const h = html.toLowerCase();
    const embeds = [];
    [['hubspot', /hbspt\.forms|hsforms\.(net|com)|js\.hsforms|hs-form/], ['marketo', /mktoform|marketo/], ['pardot', /pardot|go\.pardot/], ['typeform', /typeform/], ['jotform', /jotform/], ['gravity', /gform_wrapper/], ['cf7', /wpcf7/], ['webflow', /w-form/], ['formstack', /formstack/], ['chilipiper', /chilipiper/], ['calendly', /calendly/], ['iframeForm', /<iframe[^>]+(form|contact)/]].forEach(([n, re]) => { if (re.test(h)) embeds.push(n); });
    const captcha = [];
    [['recaptcha', /recaptcha|g-recaptcha/], ['hcaptcha', /hcaptcha/], ['turnstile', /turnstile|cf-turnstile/], ['cloudflareChallenge', /just a moment|cf-chl|challenge-platform/]].forEach(([n, re]) => { if (re.test(h)) captcha.push(n); });
    const emails = [...new Set((html.match(/mailto:([^"'?>\s]+)/gi) || []).map(x => x.slice(7).toLowerCase()))].slice(0, 8);
    return { forms, embeds, captcha, emails };
  };
  // homepage links
  const homeLinks = [...document.querySelectorAll('a[href]')].map(a => ({ h: a.href, t: a.textContent.replace(/\s+/g, ' ').trim().toLowerCase() }));
  const want = /contact|get-in-touch|lets-talk|let-s-talk|talk-to|partner|write-for|contribut|press|media|newsroom|about|reach-us|enquir|inquir/;
  const urls = new Set();
  homeLinks.forEach(l => { try { const u = new URL(l.h); if (u.origin === location.origin && (want.test(u.pathname.toLowerCase()) || want.test(l.t))) urls.add(u.origin + u.pathname); } catch (e) {} });
  ['/contact', '/contact-us', '/get-in-touch', '/partners', '/write-for-us', '/press'].forEach(p => urls.add(location.origin + p));
  const list = [...urls].filter(u => !/careers|jobs|login|signin|sign-in|privacy|legal|terms|cookie/.test(u)).slice(0, 14);
  const home = scanDoc(document, document.documentElement.outerHTML);
  out.homeForms = home.forms.length; out.homeEmbeds = home.embeds; out.homeEmails = home.emails;
  const res = await Promise.all(list.map(async u => { const r = await get(u); if (!r || r.status >= 400) return { u, status: r ? r.status : 0 }; const s = scanDoc(r.doc, r.html); return { u, final: r.url, status: r.status, title: (r.doc.title || '').slice(0, 70), ...s }; }));
  out.pages = res.filter(x => x.status && x.status < 400);
  out.missing = res.filter(x => !x.status || x.status >= 400).map(x => x.u.replace(location.origin, '') + ':' + x.status);
  if (ARTICLE) {
    let r = null;
    try { if (new URL(ARTICLE).origin === location.origin) r = await get(ARTICLE); else out.article = { crossOrigin: true }; } catch (e) {}
    if (r) {
      const d = r.doc; const m = (s) => (d.querySelector(s) || {}).content || '';
      const ld = [...d.querySelectorAll('script[type="application/ld+json"]')].map(s => s.textContent).join(' ');
      const pick = (re) => { const x = ld.match(re); return x ? x[1] : ''; };
      const main = d.querySelector('article') || d.querySelector('main') || d.body;
      const text = (main ? main.textContent : '').replace(/\s+/g, ' ');
      out.article = {
        status: r.status, final: r.url, title: (d.querySelector('h1') || {}).textContent?.replace(/\s+/g, ' ').trim().slice(0, 140) || d.title,
        published: m('meta[property="article:published_time"]') || pick(/"datePublished"\s*:\s*"([^"]+)"/),
        modified: m('meta[property="article:modified_time"]') || pick(/"dateModified"\s*:\s*"([^"]+)"/),
        timeTags: [...d.querySelectorAll('time')].map(t => t.getAttribute('datetime') || t.textContent.trim()).slice(0, 4),
        dateText: (text.match(/(Updated|Published|Last updated)[^.]{0,40}?(20\d\d)/i) || [''])[0],
        words: text.split(' ').length,
        videos: (main ? main.querySelectorAll('video,iframe[src*="youtube"],iframe[src*="vimeo"],iframe[src*="wistia"],iframe[src*="loom"],.wistia_embed') : []).length,
        imgs: (main ? main.querySelectorAll('img') : []).length,
        imgsNoAlt: (main ? [...main.querySelectorAll('img')].filter(i => !(i.getAttribute('alt') || '').trim()).length : 0),
        h2: [...(main || d).querySelectorAll('h2,h3')].map(h => h.textContent.replace(/\s+/g, ' ').trim()).slice(0, 25),
        mentions: ['video', 'animation', 'explainer', 'infographic', 'visual', 'diagram', 'demo'].map(k => k + ':' + (text.toLowerCase().split(k).length - 1)).join(' '),
        sample: text.slice(0, 50)
      };
    }
  }
  return out;
});
const r = await SCAN(''); r.sm = await SM(); JSON.stringify(r);