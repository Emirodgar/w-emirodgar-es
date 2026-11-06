/* Núcleo de simulación de Atalaya (datos de ejemplo + motor de escenarios). Expone window.AT. */
(function () {
  var PARTIES = [['PP', '#3b9cff'], ['PSOE', '#ef4444'], ['Vox', '#7ac943'], ['Cs', '#fb923c'], ['Sumar', '#d6246e'], ['Podemos', '#9b59d0'], ['Otros', '#94a3b8']];
  var COL = {}; PARTIES.forEach(function (p) { COL[p[0]] = p[1]; });
  var POS = { Vox: 9, PP: 7, Cs: 5.5, Otros: 5, PSOE: 3.5, Sumar: 2, Podemos: 1.5 };   // eje ideológico 0-10 (supuesto del modelo)
  var ID2P = { PP: 'PP', PSOE: 'PSOE', VOX: 'Vox', SUMAR: 'Sumar', PODEMOS: 'Podemos' };
  var YEARS = [2011, 2015, 2019, 2023], CAPITAL = '37274';

  function rng(seed) { var a = seed >>> 0; return function () { a |= 0; a = a + 0x6D2B79F5 | 0; var t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }

  function simulate(code, scale) {
    var r = rng(parseInt(code, 10) * 2654435761), lean = r(), trait = (0.6 + r() * 2.4) * (scale || 1), hist = [];
    var base = { PP: 28 + lean * 30, PSOE: 22 + (1 - lean) * 22 };
    var target = [[1, 1, 0, 0], [.85, .95, 0, 1], [.8, .9, .45, .55], [.95, .85, 1, .1]], noise = 7 * (scale || 1);
    YEARS.forEach(function (y, i) {
      var s = {}, tot = 0;
      s.PP = base.PP * target[i][0] * (.55 + .45 * target[i][0]) + (r() - .5) * noise * trait;
      s.PSOE = base.PSOE * target[i][1] + (r() - .5) * noise * trait;
      s.Vox = (4 + r() * 9) * target[i][2]; s.Cs = (5 + r() * 9) * target[i][3];
      ['PP', 'PSOE', 'Vox', 'Cs'].forEach(function (k) { s[k] = Math.max(0, s[k]); tot += s[k]; });
      s.Otros = Math.max(2, 6 + r() * 12); tot += s.Otros;
      for (var k in s) s[k] = +(s[k] / tot * 100).toFixed(1);
      hist.push(s);
    });
    var sent = Math.round((r() - .5) * 24 * (scale ? 1.6 : 1));
    if (code === CAPITAL) {
      [[44.8, 29.1, 6.2, 12.1], [41.2, 28.4, 7.5, 17.0], [43.3, 31.0, 8.8, 10.2], [45.9, 27.5, 10.4, 2.5]].forEach(function (v, i) {
        var s = { PP: v[0], PSOE: v[1], Vox: v[2], Cs: v[3] }; s.Otros = +(100 - v[0] - v[1] - v[2] - v[3]).toFixed(1); hist[i] = s;
      });
      sent = -38;
    }
    return { hist: hist, sent: sent };
  }

  function analyse(sim) {
    var h = sim.hist, K = ['PP', 'PSOE', 'Vox', 'Cs'];
    var win = h.map(function (s) { return K.slice().sort(function (a, b) { return s[b] - s[a]; })[0]; });
    var last = h[h.length - 1], ord = K.slice().sort(function (a, b) { return last[b] - last[a]; });
    var margin = +(last[ord[0]] - last[ord[1]]).toFixed(1), ped = 0;
    for (var i = 1; i < h.length; i++) { var d = 0; for (var k in h[i]) d += Math.abs(h[i][k] - h[i - 1][k]); ped += d / 2; }
    ped /= h.length - 1;
    var switches = win.reduce(function (n, w, i) { return n + (i && w !== win[i - 1] ? 1 : 0); }, 0);
    var vol = Math.min(100, Math.round(ped * 4.2 + switches * 14)), distinct = new Set(win).size;
    var risk = 0.34 * vol + 0.30 * Math.max(0, 30 - margin) / 30 * 100 + 0.36 * Math.min(100, Math.max(0, -sim.sent) * 2.2);
    if (distinct === 1 && sim.sent < -20) risk += 14;
    risk = Math.max(0, Math.min(100, Math.round(risk)));
    return { winner: win[win.length - 1], margin: margin, vol: vol, risk: risk, sent: sim.sent, last: last, hist: h, distinct: distinct, switches: switches,
             type: distinct === 1 ? 'Bastión' : (distinct >= 3 || vol >= 85) ? 'Volátil' : 'Cambiante' };
  }

  /* Modelo transparente (puntos sobre el electorado). Evento negativo: el partido pierde L=cuota*0,30*I;
     40 % de L pasa a indecisos, 20 % a abstención y 40 % a otros según cercanía ideológica.
     Evento positivo: gana G=cuota*0,12*I; 50 % de G viene de indecisos y 50 % de otros según cercanía.
     Recuperación: el partido recupera rec % × 0,7 de lo que se fue a indecisos. */
  function proxW(from, keys) { var w = {}, t = 0; keys.forEach(function (k) { if (k === from) return; w[k] = Math.exp(-Math.abs((POS[k] == null ? 5 : POS[k]) - (POS[from] == null ? 5 : POS[from])) / 2.2); t += w[k]; }); for (var k in w) w[k] /= t; return w; }
  function engine(shares, und, p, sens) {
    var keys = Object.keys(shares), dec = 100 - und, pts = {}; keys.forEach(function (k) { pts[k] = shares[k] * dec / 100; });
    var u = und, abst = 0, I = Math.min(1, (p.grav / 100) * (p.alc / 100) * (1 - 0.6 * p.fid / 100) * sens), X = p.party;
    if (pts[X] === undefined) return null;
    var w = proxW(X, keys);
    if (p.dir < 0) {
      var L = pts[X] * 0.30 * I; pts[X] -= L; u += 0.4 * L; abst += 0.2 * L;
      keys.forEach(function (k) { if (k !== X) pts[k] += 0.4 * L * w[k]; });
      var back = (p.rec / 100) * 0.7 * 0.4 * L; pts[X] += back; u -= back;
    } else {
      var G = pts[X] * 0.12 * I, fromU = Math.min(u, 0.5 * G); u -= fromU; pts[X] += G;
      var rest = G - fromU; keys.forEach(function (k) { if (k !== X) pts[k] -= rest * w[k]; });
    }
    var sum = keys.reduce(function (s, k) { return s + pts[k]; }, 0), sh = {}; keys.forEach(function (k) { sh[k] = pts[k] / sum * 100; });
    var top = function (o) { return keys.filter(function (k) { return k !== 'Otros'; }).sort(function (a, b) { return o[b] - o[a]; })[0]; };
    return { before: shares, after: sh, und0: und, und1: u, abst: abst, I: I, winB: top(shares), winA: top(sh) };
  }
  function terrShares(a) { var s = a.last, o = s.Otros; return { PP: s.PP, PSOE: s.PSOE, Vox: s.Vox, Cs: s.Cs, Sumar: o * .45, Podemos: o * .15, Otros: o * .40 }; }

  /* media de encuestas real (como /elecciones-espana: sondeos de los últimos 30 días, sin CIS) */
  function nationalFromPolls(enc) {
    if (!enc || !enc.sondeos) return null;
    var s = enc.sondeos.filter(function (x) { return !/cis/i.test(x.empresa); }), last = new Date(s[0].fecha);
    var rec = s.filter(function (x) { return (last - new Date(x.fecha)) / 864e5 <= 30; }), sm = {}, ct = {};
    rec.forEach(function (x) { var w = Math.sqrt(x.muestra || 1000); for (var k in x.voto) { var p = ID2P[k]; if (!p) continue; sm[p] = (sm[p] || 0) + x.voto[k] * w; ct[p] = (ct[p] || 0) + w; } });
    var shares = {}, tot = 0; for (var p in sm) { shares[p] = sm[p] / ct[p]; tot += shares[p]; }
    shares.Cs = 0; shares.Otros = Math.max(0, 100 - tot);
    return { shares: shares, n: rec.length, fecha: s[0].fecha };
  }

  window.AT = { PARTIES: PARTIES, COL: COL, POS: POS, YEARS: YEARS, rng: rng, simulate: simulate, analyse: analyse, engine: engine, terrShares: terrShares, nationalFromPolls: nationalFromPolls };
})();
