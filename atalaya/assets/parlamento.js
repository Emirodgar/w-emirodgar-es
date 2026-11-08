/* Congreso y Senado de Atalaya: mapa de puntos, ficha de persona, histórico y altas/bajas entre legislaturas.
   Datos: /atalaya/data/parlamento/{congreso,senado}.json (los genera scripts/atalaya/build_parlamento.py; nunca se borra nada). */
(function () {
  'use strict';
  var CAM = document.currentScript.getAttribute('data-camara'), SEN = CAM === 'senado';
  var $ = function (id) { return document.getElementById(id); };
  var esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  var norm = function (s) { return String(s || '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase(); };
  var ROM = ['Constituyente', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI'];

  /* partido o grupo -> [clave, nombre, color] */
  var PAL = { PP: ['PP', '#3b9cff'], PSOE: ['PSOE', '#ef4444'], VOX: ['Vox', '#7ac943'], SUMAR: ['Sumar / IU', '#d6246e'], PODEMOS: ['Podemos', '#9b59d0'], ERC: ['ERC', '#f95838'], JUNTS: ['Junts / CiU', '#00c3b2'],
    BILDU: ['EH Bildu', '#03cfb5'], PNV: ['PNV', '#046e44'], BNG: ['BNG', '#76b2e1'], CC: ['CC', '#ffd74f'], UPN: ['UPN', '#1d4ed8'], CS: ['Cs', '#fb923c'], UCD: ['UCD', '#16a34a'], AP: ['AP / PP', '#60a5fa'], MIXTO: ['Mixto / otros', '#94a3b8'] };
  var GSEN = { GPP: 'PP', GPS: 'PSOE', GPERB: 'ERC', GPV: 'PNV', GPPLU: 'JUNTS', GPIC: 'SUMAR', GPMX: 'MIXTO', GPUCD: 'UCD', GPCP: 'AP', GP: 'PP', GPCIU: 'JUNTS', GPSNV: 'PNV', GPV2: 'PNV', GPPOD: 'PODEMOS', GPECP: 'PODEMOS', GPSS: 'PSOE', GPCS: 'CS', GPPLU2: 'JUNTS' };
  function pk(txt) {
    var t = norm(txt);
    if (!t) return 'MIXTO';
    if (/popular|^pp\b|\bpp$|alianza popular|\bpp-|-pp\b/.test(t)) return 'PP';
    if (/socialista|psoe|psc|psib|psn|pse-|\bpsoe/.test(t)) return 'PSOE';
    if (/\bvox\b/.test(t)) return 'VOX';
    if (/sumar|izquierda unida|comuns|compromis|\bmas madrid|mas pais|ezker|\bcatalunya en comu/.test(t)) return 'SUMAR';
    if (/podemos/.test(t)) return 'PODEMOS';
    if (/erc|esquerra/.test(t)) return 'ERC';
    if (/junts|jxcat|ciu|convergencia|democratica/.test(t)) return 'JUNTS';
    if (/bildu|eusko alkartasuna|\bea\b/.test(t)) return 'BILDU';
    if (/pnv|eaj|nacionalista vasco/.test(t)) return 'PNV';
    if (/bng|bloque nacionalista/.test(t)) return 'BNG';
    if (/coalicion canaria|^cc\b|\bcc-/.test(t)) return 'CC';
    if (/\bupn\b|union del pueblo/.test(t)) return 'UPN';
    if (/ciudadanos|^cs\b|\bcs\b/.test(t)) return 'CS';
    if (/\bucd\b|centro democratico/.test(t)) return 'UCD';
    return 'MIXTO';
  }
  function keyOf(m) { return SEN ? (GSEN[m.g] || pk(m.gn || m.g || m.pt)) : pk(m.pt || m.g); }
  var col = function (k) { return (PAL[k] || PAL.MIXTO)[1]; }, nm = function (k) { return (PAL[k] || PAL.MIXTO)[0]; };
  var fdate = function (d) { return d ? d.split('-').reverse().join('/') : '—'; };
  var initials = function (n) { return (n || '?').split(' ').filter(function (w) { return /^[A-ZÁÉÍÓÚÑ]/.test(w); }).slice(0, 2).map(function (w) { return w[0]; }).join(''); };

  var D, GJ, ES, map, markers = [], PR = {}, byP = {}, cur, vig = [], fG = '', fT = '', fQ = '', showOff = false, PN = {}, CEN = {}, chart;

  Promise.all([
    fetch('../data/parlamento/' + CAM + '.json').then(function (r) { return r.json(); }),
    fetch('../data/provincias.geojson').then(function (r) { return r.json(); }),
    fetch('../data/escanos.json').then(function (r) { return r.json(); }).catch(function () { return null; })
  ]).then(function (a) { D = a[0]; GJ = a[1]; ES = a[2]; init(); }).catch(function (e) { $('main').innerHTML = '<p class="empty">No se pudieron cargar los datos (' + esc(e && e.message) + ').</p>'; });

  function legName(n) { var l = D.legislaturas[n]; return l ? (n === 0 ? 'Constituyente' : ROM[n] + ' Legislatura') : n; }
  function init() {
    cur = D.legislatura_actual;
    D.mandatos.forEach(function (m) { (byP[m.p] = byP[m.p] || []).push(m); m.k = keyOf(m); });
    GJ.features.forEach(function (f) { PN[f.properties.c] = f.properties.n; CEN[f.properties.c] = L.geoJSON(f).getBounds().getCenter(); });
    vig = D.mandatos.filter(function (m) { return m.l === cur && m.vig !== undefined && m.vig !== null; });
    $('capt').textContent = 'Datos oficiales capturados el ' + fdate(D.capturado) + (D.disolucion ? ' · Cortes disueltas el ' + fdate(D.disolucion) : '');
    tabs(); initMap(); fillHist(); renderAll();
  }
  function tabs() {
    var bs = document.querySelectorAll('.tabs button');
    bs.forEach(function (b) { b.onclick = function () { bs.forEach(function (x) { x.setAttribute('aria-selected', x === b); }); $('tAct').hidden = b.dataset.t !== 'act'; $('tHis').hidden = b.dataset.t !== 'his'; if (b.dataset.t === 'act') { map.invalidateSize(); layout(); } else drawHist(); }; });
  }
  function pool() { return vig.filter(function (m) { return showOff ? true : m.vig; }); }
  function pass(m) {
    if (fG && m.k !== fG) return false; if (fT && m.c !== fT) return false;
    if (fQ && norm(D.personas[m.p].n).indexOf(norm(fQ)) < 0) return false; return true;
  }
  function initMap() {
    map = L.map('map', { zoomControl: true, attributionControl: false, scrollWheelZoom: false, zoomSnap: .25 }).setView([40.1, -3.6], 5.5);
    L.geoJSON(GJ, { style: { color: '#1f2937', weight: 1, fillColor: '#101722', fillOpacity: 1 }, onEachFeature: function (f, l) { l.bindTooltip(esc(f.properties.n), { sticky: true }); } }).addTo(map);
    map.on('zoomend', layout);
    $('can').onclick = function () { map.setView([28.3, -15.9], 6.5); }; $('pen').onclick = function () { map.setView([40.1, -3.6], 5.5); };
  }
  function layout() { /* un punto por persona, en espiral alrededor del centro de su provincia (separación en píxeles) */
    markers.forEach(function (x) { map.removeLayer(x); }); markers = [];
    var by = {}; pool().filter(pass).forEach(function (m) { if (m.c) (by[m.c] = by[m.c] || []).push(m); });
    Object.keys(by).forEach(function (c) {
      var base = map.latLngToLayerPoint(CEN[c]); by[c].sort(function (a, b) { return a.k < b.k ? -1 : a.k > b.k ? 1 : D.personas[a.p].n.localeCompare(D.personas[b.p].n, 'es'); });
      by[c].forEach(function (m, i) {
        var r = 8 * Math.sqrt(i + .4), an = i * 2.39996, ll = map.layerPointToLatLng(L.point(base.x + r * Math.cos(an), base.y + r * Math.sin(an)));
        var off = !m.vig, d = SEN && m.t !== 'E';
        var mk = L.circleMarker(ll, { radius: 5.2, fillColor: col(m.k), fillOpacity: off ? .25 : .95, color: d ? '#fff' : '#05070a', weight: d ? 1.6 : 1 }).addTo(map);
        mk.bindTooltip(esc(D.personas[m.p].n) + ' · ' + esc(nm(m.k)), { direction: 'top' }); mk.on('click', function () { openP(m.p); }); markers.push(mk);
      });
    });
  }
  function renderAll() {
    var P = pool(), cnt = {}; P.forEach(function (m) { cnt[m.k] = (cnt[m.k] || 0) + 1; });
    var ks = Object.keys(cnt).sort(function (a, b) { return cnt[b] - cnt[a]; });
    $('kpis').innerHTML = '<button class="m" data-k="" aria-pressed="' + (fG === '') + '"><span>Total</span><b>' + P.length + '</b></button>' + ks.map(function (k) { return '<button class="m" style="--c:' + col(k) + '" data-k="' + k + '" aria-pressed="' + (fG === k) + '"><span>' + esc(nm(k)) + '</span><b>' + cnt[k] + '</b></button>'; }).join('');
    $('kpis').querySelectorAll('button').forEach(function (b) { b.onclick = function () { fG = fG === b.dataset.k ? '' : b.dataset.k; renderAll(); }; });
    var ts = {}; P.forEach(function (m) { if (m.c) ts[m.c] = 1; }); var cs = Object.keys(ts).sort(function (a, b) { return PN[a].localeCompare(PN[b], 'es'); });
    $('ft').innerHTML = '<option value="">Todas las provincias</option>' + cs.map(function (c) { return '<option value="' + c + '"' + (fT === c ? ' selected' : '') + '>' + esc(PN[c]) + '</option>'; }).join('');
    var L2 = P.filter(pass).sort(function (a, b) { return D.personas[a.p].n.localeCompare(D.personas[b.p].n, 'es'); });
    $('cnt').textContent = L2.length + ' de ' + P.length;
    $('list').innerHTML = L2.length ? L2.map(function (m) { return '<button class="pr' + (m.vig ? '' : ' off') + '" data-p="' + esc(m.p) + '" style="--c:' + col(m.k) + '"><i></i><span><b>' + esc(D.personas[m.p].n) + '</b><small>' + esc(nm(m.k)) + ' · ' + esc(terr(m)) + (m.vig ? '' : ' · baja ' + fdate(m.baja || '')) + '</small></span></button>'; }).join('') : '<p class="empty">Nadie coincide con el filtro.</p>';
    $('list').querySelectorAll('button').forEach(function (b) { b.onclick = function () { openP(b.dataset.p); }; });
    $('lg').innerHTML = ks.map(function (k) { return '<span data-k="' + k + '"><i style="background:' + col(k) + '"></i>' + esc(nm(k)) + '</span>'; }).join('') + (SEN ? '<span><i style="background:none;border:2px solid #fff"></i>Designado/a por parlamento autonómico</span>' : '');
    layout();
  }
  function terr(m) { return (SEN && m.t !== 'E' ? 'designado por ' : '') + (m.cn || (m.c && PN[m.c]) || '—'); }

  /* ───── ficha de persona ───── */
  var wikiCache = {};
  function wiki(name) {
    if (wikiCache[name]) return wikiCache[name];
    return wikiCache[name] = fetch('https://es.wikipedia.org/w/rest.php/v1/search/title?limit=3&q=' + encodeURIComponent(name)).then(function (r) { return r.json(); }).then(function (j) {
      var toks = norm(name).split(' ').filter(function (w) { return w.length > 2; });
      var hit = (j.pages || []).filter(function (p) { var t = norm(p.title); return toks.slice(0, 3).every(function (w) { return t.indexOf(w) >= 0; }); })[0];
      if (!hit) return null;
      return fetch('https://es.wikipedia.org/api/rest_v1/page/summary/' + encodeURIComponent(hit.key)).then(function (r) { return r.json(); }).then(function (s) {
        var ex = norm((s.extract || '') + ' ' + (s.description || '')); /* guardia: solo si el resumen habla de política, para no mostrar un homónimo */
        return /diputad|senador|polític|politic|parlament|alcalde|ministr|president/.test(ex) ? { t: s.title, u: s.content_urls && s.content_urls.desktop.page, img: s.thumbnail && s.thumbnail.source, ex: s.extract } : null;
      });
    }).catch(function () { return null; });
  }
  function openP(id) {
    var P = D.personas[id], ms = (byP[id] || []).slice().sort(function (a, b) { return a.l - b.l; }), last = ms[ms.length - 1], k = last.k, c = col(k);
    $('dFace').style.cssText = '--c:' + c; $('dFace').textContent = initials(P.n);
    $('dName').textContent = P.n; $('dSub').textContent = nm(k) + (last.l === cur ? '' : ' · última legislatura: ' + legName(last.l));
    var dl = '<dl><dt>' + (SEN ? 'Procedencia' : 'Circunscripción') + '</dt><dd>' + esc(terr(last)) + '</dd>' + (last.pt ? '<dt>Partido</dt><dd>' + esc(last.pt) + '</dd>' : '') + (last.g || last.gn ? '<dt>Grupo</dt><dd>' + esc(last.gn || last.g) + '</dd>' : '') +
      (last.alta ? '<dt>Alta</dt><dd>' + fdate(last.alta) + '</dd>' : '') + (last.baja ? '<dt>Baja</dt><dd>' + fdate(last.baja) + '</dd>' : last.baja_txt ? '<dt>Baja</dt><dd>' + esc(last.baja_txt) + '</dd>' : '') + (last.sust ? '<dt>Relevo</dt><dd>' + esc(last.sust) + '</dd>' : '') + (last.pos ? '<dt>Escaño</dt><dd>' + esc(last.pos) + '</dd>' : '') +
      (last.l === cur ? '<dt>Estado</dt><dd>' + (last.vig ? 'En el cargo' + (D.disolucion && !SEN && last.e !== 'activo' ? ' al disolverse las Cortes' : '') : 'Baja') + '</dd>' : '') + '</dl>';
    var chips = '<h3>Legislaturas (' + ms.length + ')</h3><div class="chips">' + ms.map(function (m) { return '<span class="' + (m.l === cur ? 'cur' : '') + '" title="' + esc(nm(m.k) + ' · ' + terr(m)) + '">' + (m.l === 0 ? 'Const.' : ROM[m.l]) + ' · ' + esc(nm(m.k)) + '</span>'; }).join('') + '</div>';
    var bio = last.bio ? '<h3>Biografía oficial</h3><p class="bio">' + esc(last.bio.length > 1400 ? last.bio.slice(0, 1400) + '…' : last.bio) + '</p>' : '';
    $('dBody').innerHTML = dl + chips + bio + '<div id="dWiki"></div>';
    $('dFoot').innerHTML = 'Fuente: <a href="' + esc(D.fuente) + '" target="_blank" rel="noopener">' + (SEN ? 'senado.es' : 'congreso.es') + '</a>. La coincidencia con Wikipedia es automática: verifícala.';
    var dr = $('dr'); dr.hidden = false; requestAnimationFrame(function () { dr.classList.add('on'); }); $('dName').focus();
    wiki(P.n).then(function (w) { if ($('dName').textContent !== P.n) return; if (w) { if (w.img) $('dFace').style.backgroundImage = 'url(' + w.img + ')', $('dFace').textContent = ''; $('dWiki').innerHTML = '<h3>Wikipedia</h3><p>' + esc((w.ex || '').slice(0, 320)) + '… <a href="' + esc(w.u) + '" target="_blank" rel="noopener">Leer más</a></p>'; } });
  }
  function closeP() { var dr = $('dr'); dr.classList.remove('on'); setTimeout(function () { dr.hidden = true; }, 200); }

  /* ───── histórico ───── */
  function fillHist() {
    var ls = Object.keys(D.legislaturas).map(Number).sort(function (a, b) { return a - b; });
    var opt = function (sel) { return ls.map(function (n) { return '<option value="' + n + '"' + (n === sel ? ' selected' : '') + '>' + legName(n) + (D.legislaturas[n].inicio ? ' (' + D.legislaturas[n].inicio.slice(0, 4) + ')' : '') + '</option>'; }).join(''); };
    $('hA').innerHTML = opt(cur - 1); $('hB').innerHTML = opt(cur); $('hA').onchange = $('hB').onchange = drawHist;
  }
  function members(l) { var s = {}; D.mandatos.forEach(function (m) { if (m.l === l && (l !== cur || m.vig !== false)) s[m.p] = m; }); return s; }
  function listP(ids, ref, tag) {
    return ids.length ? '<div class="list" style="max-height:340px">' + ids.sort(function (a, b) { return D.personas[a].n.localeCompare(D.personas[b].n, 'es'); }).map(function (id) { var m = ref[id]; return '<button class="pr" data-p="' + esc(id) + '" style="--c:' + col(m.k) + '"><i></i><span><b>' + esc(D.personas[id].n) + '</b><small>' + esc(nm(m.k)) + ' · ' + esc(terr(m)) + '</small></span></button>'; }).join('') + '</div>' : '<p class="empty">Nadie.</p>';
  }
  function drawHist() {
    var a = +$('hA').value, b = +$('hB').value, A = members(a), B = members(b);
    var stay = Object.keys(B).filter(function (id) { return A[id]; }), inn = Object.keys(B).filter(function (id) { return !A[id]; }), out = Object.keys(A).filter(function (id) { return !B[id]; });
    $('hCmp').innerHTML = '<div><h3>Entran <span>' + inn.length + ' en ' + legName(b) + '</span></h3>' + listP(inn, B) + '</div><div><h3>Salen <span>' + out.length + ' de ' + legName(a) + '</span></h3>' + listP(out, A) + '</div><div><h3>Continúan <span>' + stay.length + '</span></h3>' + listP(stay, B) + '</div>';
    $('hCmp').querySelectorAll('button').forEach(function (x) { x.onclick = function () { openP(x.dataset.p); }; });
    var pct = Math.round(inn.length / Math.max(1, Object.keys(B).length) * 100);
    if (SEN && !D.historico_completo) { $('hSum').textContent = 'Histórico del Senado en construcción: el listado oficial solo indica la última legislatura de cada persona. Se completa con la ficha individual de cada senador, y hasta entonces las entradas y salidas de legislaturas anteriores no son fiables.'; $('hCmp').innerHTML = ''; drawComp(); return; }
    $('hSum').textContent = 'Renovación entre ' + legName(a) + ' y ' + legName(b) + ': ' + pct + ' % de caras nuevas.' + (a === cur || b === cur ? ' La legislatura actual incluye solo a quienes ocupaban el cargo al disolverse.' : '');
    drawComp();
  }
  function composition() { /* {leg: {clave: n}} */
    var c = {};
    if (!SEN && ES) {
      var K = { PP: 'PP', PSOE: 'PSOE', Vox: 'VOX', Cs: 'CS', UCD: 'UCD', 'AP/PP': 'AP', Podemos: 'PODEMOS', Sumar: 'SUMAR', IU: 'SUMAR' };
      var el = ES['01'].elecciones; el.forEach(function (_, i) { c[i] = {}; });
      Object.keys(ES).forEach(function (p) { var e = ES[p]; el.forEach(function (_, i) { var tot = e.total[i] || 0, used = 0; Object.keys(e.partidos).forEach(function (k) { var v = e.partidos[k][i] || 0; used += v; var kk = K[k] || 'MIXTO'; c[i][kk] = (c[i][kk] || 0) + v; }); c[i].MIXTO = (c[i].MIXTO || 0) + Math.max(0, tot - used); }); });
    } else if (SEN) {
      D.mandatos.forEach(function (m) { if (m.l === cur && m.vig === false) return; (c[m.l] = c[m.l] || {})[m.k] = ((c[m.l] || {})[m.k] || 0) + 1; });
    }
    return c;
  }
  function drawComp() {
    if (chart) { chart.destroy(); chart = null; } if (typeof Chart === 'undefined') return;
    var c = composition(), ls = Object.keys(c).map(Number).sort(function (x, y) { return x - y; }), ks = {};
    ls.forEach(function (l) { Object.keys(c[l]).forEach(function (k) { ks[k] = (ks[k] || 0) + c[l][k]; }); });
    var keys = Object.keys(ks).sort(function (x, y) { return ks[y] - ks[x]; });
    chart = new Chart($('ch'), { type: 'bar', data: { labels: ls.map(function (l) { return (D.legislaturas[l] && D.legislaturas[l].inicio ? D.legislaturas[l].inicio.slice(0, 4) + ' · ' : '') + (l === 0 ? 'Const.' : ROM[l]); }),
      datasets: keys.map(function (k) { return { label: nm(k), backgroundColor: col(k), data: ls.map(function (l) { return c[l][k] || 0; }) }; }) },
      options: { responsive: true, maintainAspectRatio: false, animation: false, plugins: { legend: { labels: { color: '#8b97a8', boxWidth: 10 } } }, scales: { x: { stacked: true, ticks: { color: '#8b97a8' }, grid: { color: '#1f2937' } }, y: { stacked: true, ticks: { color: '#8b97a8' }, grid: { color: '#1f2937' } } } } });
  }

  $('dx').onclick = closeP; document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeP(); });
  $('q').oninput = function () { fQ = this.value; renderAll(); }; $('ft').onchange = function () { fT = this.value; renderAll(); };
  $('off').onchange = function () { showOff = this.checked; renderAll(); };
})();
