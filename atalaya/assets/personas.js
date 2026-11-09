/* Utilidades compartidas sobre personas políticas (Panel y página Políticos). Expone window.PE. */
(function () {
  var norm = function (s) { return s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase(); };
  var PCOL = { PP: '#3b9cff', PSOE: '#ef4444', VOX: '#7ac943', FA: '#d6246e', 'FA/PODEMOS': '#d6246e', SUMAR: '#d6246e', PODEMOS: '#9b59d0', ERC: '#f95838', JUNTS: '#00c3b2', EHB: '#03cfb5', BILDU: '#03cfb5', PNV: '#046e44', BNG: '#76b2e1', CC: '#ffd74f' };
  var PNAME = { PP: 'PP', PSOE: 'PSOE', VOX: 'Vox', FA: 'Frente Amplio', 'FA/PODEMOS': 'Frente Amplio / Podemos', SUMAR: 'Sumar', PODEMOS: 'Podemos', ERC: 'ERC', JUNTS: 'Junts', EHB: 'EH Bildu', BILDU: 'EH Bildu', PNV: 'PNV', BNG: 'BNG', CC: 'CC' };
  var PORDER = ['PP', 'PSOE', 'VOX', 'FA', 'FA/PODEMOS', 'SUMAR', 'PODEMOS', 'ERC', 'JUNTS', 'EHB', 'BILDU', 'PNV', 'BNG', 'CC'];

  function partyKey(txt) {
    if (!txt) return '';
    var t = norm(txt);
    if (t.indexOf('popular') >= 0) return 'PP';
    if (t.indexOf('socialista') >= 0 || t.indexOf('psoe') >= 0 || t.indexOf('psc') >= 0) return 'PSOE';
    if (t.indexOf('vox') >= 0) return 'VOX';
    if (t.indexOf('podemos') >= 0) return 'PODEMOS';
    if (t.indexOf('nacionalista vasco') >= 0) return 'PNV';
    if (t.indexOf('esquerra') >= 0) return 'ERC';
    return txt.slice(0, 14);
  }
  function initials(n) { return n ? n.split(' ').filter(function (w) { return /^[A-ZÁÉÍÓÚÑ]/.test(w); }).slice(0, 2).map(function (w) { return w[0]; }).join('') : '?'; }

  /* formas con las que se busca a la persona en un titular (siempre dos palabras o más: evita apellidos sueltos ambiguos) */
  function aliasesOf(p) {
    var out = {}; if (p.nombre) out[p.nombre] = 1;
    if (p.wiki) { var w = decodeURIComponent(p.wiki).replace(/_/g, ' ').replace(/\s*\(.*\)$/, ''); if (w.split(' ').length >= 2) out[w] = 1; }
    var t = (p.nombre || '').split(' '); if (t.length >= 3) out[t.slice(-2).join(' ')] = 1;
    return Object.keys(out).filter(function (a) { return a.split(' ').length >= 2; });
  }

  /* estado y puntuación a partir de los titulares: usa la clasificación de Gemini (n.s) si existe y, si no, las palabras clave (n.r).
   El tono (n.s.tono) valora la NOTICIA, no a la persona (en «X acusa a Y» no se sabe a quién afecta), así que se muestra como dato
   orientativo y NO entra en la puntuación. */
  function isRisk(n) { return n.s ? n.s.riesgo >= 2 : n.r; }
  function riskOf(p, news) {
    var al = aliasesOf(p); if (!al.length) return { k: 'none', label: 'Neutro', score: 0, n: 0, r: 0 };
    var rx = al.map(function (a) { return new RegExp('(?<!\\w)' + norm(a).replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '(?!\\w)'); });
    var hits = news.filter(function (n) { var t = norm(n.t); return rx.some(function (r) { return r.test(t); }); });
    var rk = hits.filter(isRisk), tn = hits.filter(function (n) { return n.s; }).map(function (n) { return n.s.tono; });
    var k = rk.length >= 6 ? 'crisis' : rk.length >= 2 ? 'press' : hits.length ? 'focus' : 'none';
    return { k: k, label: { crisis: 'Alta cobertura de riesgo', press: 'Cobertura de riesgo', focus: 'Con cobertura', none: 'Neutro' }[k],
             score: hits.length ? Math.min(100, rk.length * 18 + hits.length * 4) : 0, n: hits.length, r: rk.length, nt: tn.length,
             tono: tn.length ? tn.reduce(function (s, x) { return s + x; }, 0) / tn.length : null, last: rk[0] || hits[0] };
  }

  /* foto de Wikipedia: promesa con la URL de la miniatura ('' si no hay), con caché en memoria y en sessionStorage */
  var cache = {};
  function photoUrl(wiki) {
    if (!wiki) return Promise.resolve('');
    if (cache[wiki] !== undefined) return Promise.resolve(cache[wiki]);
    var v = null; try { v = sessionStorage.getItem('atl-ph-' + wiki); } catch (e) {}
    if (v !== null) { cache[wiki] = v; return Promise.resolve(v); }
    return fetch('https://es.wikipedia.org/api/rest_v1/page/summary/' + encodeURIComponent(wiki)).then(function (r) { return r.json(); }).then(function (j) {
      var u = (j.type === 'standard' && j.thumbnail) ? j.thumbnail.source : ''; cache[wiki] = u;
      try { sessionStorage.setItem('atl-ph-' + wiki, u); } catch (e) {} return u;
    }).catch(function () { cache[wiki] = ''; return ''; });
  }

  window.PE = { PCOL: PCOL, PNAME: PNAME, PORDER: PORDER, partyKey: partyKey, initials: initials, aliasesOf: aliasesOf, isRisk: isRisk, riskOf: riskOf, photoUrl: photoUrl };
})();
