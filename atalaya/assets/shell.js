/* Menú lateral de Atalaya: una sola fuente de verdad para todas las páginas. */
(function () {
  var KEY = 'atalaya-menu', root = document.documentElement;
  var I = function (d) { return '<svg viewBox="0 0 24 24" aria-hidden="true">' + d + '</svg>'; };
  var ITEMS = [
    ['Panel', '/atalaya/', I('<rect x="3" y="3" width="7" height="9" rx="1.5"/><rect x="14" y="3" width="7" height="5" rx="1.5"/><rect x="14" y="12" width="7" height="9" rx="1.5"/><rect x="3" y="16" width="7" height="5" rx="1.5"/>')],
    ['Escenarios', '/atalaya/escenarios/', I('<path d="M4 6h10M18 6h2M4 12h2M10 12h10M4 18h12M20 18h0"/><circle cx="16" cy="6" r="2"/><circle cx="8" cy="12" r="2"/><circle cx="18" cy="18" r="2"/>')],
    ['Políticos', '/atalaya/politicos/', I('<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c0-3.6 2.9-6 6.5-6s6.5 2.4 6.5 6"/><path d="M16 4.6a3.5 3.5 0 0 1 0 6.8M18 14.5c2 .7 3.5 2.4 3.5 5.5"/>')],
    ['Programas', '/atalaya/programas/', I('<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 14l2 2 4-4"/>')],
    ['Fuentes', '/atalaya/fuentes/', I('<ellipse cx="12" cy="5.5" rx="8" ry="3"/><path d="M4 5.5v13c0 1.7 3.6 3 8 3s8-1.3 8-3v-13M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/>')],
    ['Fichas', '/atalaya/fichas/', I('<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h6"/>')]
  ];
  var small = window.matchMedia && matchMedia('(max-width:700px)').matches, saved = null;
  try { saved = localStorage.getItem(KEY); } catch (e) {}
  if (saved === 'c' || (saved === null && small)) root.classList.add('sb-c');

  var path = location.pathname.replace(/index\.html$/, '');
  var nav = document.createElement('nav');
  nav.className = 'sb'; nav.setAttribute('aria-label', 'Principal');
  nav.innerHTML = '<a class="sb-brand" href="/atalaya/" aria-label="Atalaya, inicio"><i></i><span>ATALAYA</span></a><ul class="sb-list"></ul>' +
    '<div class="sb-foot"><button class="sb-tog" type="button" aria-expanded="true">' + I('<path d="M15 6l-6 6 6 6"/>') + '<span class="lb">Contraer menú</span></button></div>';
  var ul = nav.querySelector('ul');
  ITEMS.forEach(function (it) {
    var cur = it[1] === '/atalaya/' ? path === '/atalaya/' : path.indexOf(it[1]) === 0;
    var li = document.createElement('li');
    li.innerHTML = '<a href="' + it[1] + '" title="' + it[0] + '"' + (cur ? ' aria-current="page"' : '') + '>' + it[2] + '<span class="lb">' + it[0] + '</span></a>';
    ul.appendChild(li);
  });
  var tog = nav.querySelector('.sb-tog');
  function sync() {
    var c = root.classList.contains('sb-c');
    tog.setAttribute('aria-expanded', String(!c));
    tog.title = c ? 'Expandir menú' : 'Contraer menú';
    tog.setAttribute('aria-label', c ? 'Expandir menú' : 'Contraer menú');
  }
  tog.addEventListener('click', function () {
    root.classList.toggle('sb-c');
    try { localStorage.setItem(KEY, root.classList.contains('sb-c') ? 'c' : 'o'); } catch (e) {}
    sync();
    window.dispatchEvent(new Event('resize')); // para que Leaflet y Chart.js recalculen su tamaño
    setTimeout(function () { window.dispatchEvent(new Event('resize')); }, 250);
  });
  document.body.insertBefore(nav, document.body.firstChild);
  sync();
})();
