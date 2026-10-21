(async (KW) => {
  const P = new DOMParser(); const seen = new Set(); const urls = [];
  const fx = async (u) => { try { const r = await fetch(u); if (!r.ok) return null; const t = await r.text(); if (!/<(urlset|sitemapindex)/i.test(t)) return null; return P.parseFromString(t, 'text/xml'); } catch (e) { return null; } };
  let roots = ['/sitemap_index.xml', '/sitemap.xml', '/post-sitemap.xml', '/blog/sitemap.xml'];
  try { const rb = await (await fetch('/robots.txt')).text(); (rb.match(/sitemap:\s*(\S+)/gi) || []).forEach(x => roots.unshift(x.split(/:\s*/).slice(1).join(':'))); } catch (e) {}
  const queue = [...new Set(roots)]; let n = 0;
  while (queue.length && n < 8) {
    const u = queue.shift(); if (seen.has(u)) continue; seen.add(u); n++;
    const d = await fx(u); if (!d) continue;
    const sms = [...d.querySelectorAll('sitemap')].map(s => ({ l: s.querySelector('loc')?.textContent.trim(), m: s.querySelector('lastmod')?.textContent || '' }));
    sms.filter(s => /post|blog|article|resource|news|insight|guide/i.test(s.l)).sort((a, b) => b.m.localeCompare(a.m)).slice(0, 4).forEach(s => queue.unshift(s.l));
    if (!sms.length) [...d.querySelectorAll('url')].forEach(x => urls.push({ l: x.querySelector('loc')?.textContent.trim(), m: (x.querySelector('lastmod')?.textContent || '').slice(0, 10) }));
  }
  const re = new RegExp(KW, 'i');
  const rec = urls.filter(x => x.m >= '2024-10-21' || !x.m);
  return { checked: [...seen], total: urls.length, recent: rec.length, hits: rec.filter(x => re.test(x.l)).sort((a, b) => b.m.localeCompare(a.m)).slice(0, 40).map(x => x.m + ' ' + x.l.replace(location.origin, '')) };
})
