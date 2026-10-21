(async (RE) => {
  const re = new RegExp(RE || 'video|market|content|brand|social|advert|ads|visual|design|email|promot|engag|campaign|story', 'i');
  const P = new DOMParser();
  const fx = async (u) => { try { const r = await fetch(u); if (r.status >= 400) return null; const t = await r.text(); if (!/<(urlset|sitemapindex)/.test(t)) return null; return P.parseFromString(t, 'text/xml'); } catch (e) { return null; } };
  let idx = null, src = '';
  for (const p of ['/sitemap_index.xml', '/sitemap.xml', '/post-sitemap.xml', '/wp-sitemap.xml']) { idx = await fx(location.origin + p); if (idx) { src = p; break; } }
  if (!idx) return { err: 'no sitemap' };
  let maps = [...idx.querySelectorAll('sitemap > loc')].map(x => x.textContent.trim());
  let docs = [];
  if (maps.length) {
    const pm = maps.filter(m => /post|blog|article|resource|news|insight/i.test(m)).slice(0, 6);
    docs = (await Promise.all((pm.length ? pm : maps.slice(0, 4)).map(fx))).filter(Boolean);
  } else docs = [idx];
  const urls = [];
  docs.forEach(d => d.querySelectorAll('url').forEach(u => { const loc = (u.querySelector('loc') || {}).textContent || ''; const lm = (u.querySelector('lastmod') || {}).textContent || ''; urls.push([loc.trim(), lm.slice(0, 10)]); }));
  const hits = urls.filter(x => re.test(x[0]) && x[1] >= '2024-10-21').sort((a, b) => b[1].localeCompare(a[1]));
  return { src, maps: maps.slice(0, 12), total: urls.length, hits: hits.slice(0, 30) };
})
