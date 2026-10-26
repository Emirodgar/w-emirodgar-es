(function () {
  var input = document.getElementById('search-input');
  var out = document.getElementById('search-results');
  var count = document.getElementById('search-count');
  if (!input || !out) return;
  var data = null;

  function norm(s) {
    return (s || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
  }

  function score(item, tokens) {
    var total = 0;
    for (var i = 0; i < tokens.length; i++) {
      var k = tokens[i], s = 0;
      var pos = item._t.indexOf(k);
      if (pos !== -1) s += (pos === 0 || item._t.indexOf(' ' + k) !== -1) ? 6 : 4;
      if (item._d.indexOf(k) !== -1) s += 2;
      if (item._c.indexOf(k) !== -1) s += 1;
      if (item._x.indexOf(k) !== -1) s += 1;
      if (!s) return 0;
      total += s;
    }
    return total;
  }

  function render(q) {
    out.textContent = '';
    var tokens = norm(q).split(/\s+/).filter(function (w) { return w.length > 1; });
    if (!tokens.length) { count.textContent = ''; return; }
    var res = data
      .map(function (it) { return { it: it, s: score(it, tokens) }; })
      .filter(function (r) { return r.s > 0; })
      .sort(function (a, b) { return b.s - a.s; })
      .slice(0, 40);
    count.textContent = res.length
      ? res.length + (res.length === 1 ? ' resultado' : ' resultados')
      : 'Sin resultados para «' + q + '». Prueba con otras palabras o consulta el mapa web.';
    res.forEach(function (r) {
      var li = document.createElement('li');
      var a = document.createElement('a');
      a.href = r.it.u;
      a.textContent = r.it.t;
      li.appendChild(a);
      if (r.it.c) {
        var b = document.createElement('small');
        b.textContent = ' · ' + r.it.c;
        li.appendChild(b);
      }
      var desc = r.it.d || r.it.x;
      if (desc) {
        var p = document.createElement('p');
        p.textContent = desc.length > 200 ? desc.slice(0, 197) + '…' : desc;
        li.appendChild(p);
      }
      out.appendChild(li);
    });
  }

  function run() {
    var q = input.value.trim();
    try { history.replaceState(null, '', q ? '?q=' + encodeURIComponent(q) : location.pathname); } catch (e) {}
    if (data) render(q);
  }

  var m = location.search.match(/[?&]q=([^&]*)/);
  if (m) { try { input.value = decodeURIComponent(m[1].replace(/\+/g, ' ')); } catch (e) {} }

  fetch('/search.json')
    .then(function (r) { return r.json(); })
    .then(function (j) {
      data = j.map(function (it) {
        it._t = norm(it.t); it._d = norm(it.d); it._c = norm(it.c); it._x = norm(it.x);
        return it;
      });
      run();
    })
    .catch(function () { count.textContent = 'No se ha podido cargar el buscador. Prueba el mapa web.'; });

  input.addEventListener('input', run);
  input.focus();
})();
