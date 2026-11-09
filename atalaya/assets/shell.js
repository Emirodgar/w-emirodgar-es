/* Menú lateral de Atalaya: una sola fuente de verdad para todas las páginas. */
(function () {
  var KEY = 'atalaya-menu', root = document.documentElement;
  var I = function (d) { return '<svg viewBox="0 0 24 24" aria-hidden="true">' + d + '</svg>'; };
  var ITEMS = [
    ['Panel', '/atalaya/', I('<rect x="3" y="3" width="7" height="9" rx="1.5"/><rect x="14" y="3" width="7" height="5" rx="1.5"/><rect x="14" y="12" width="7" height="9" rx="1.5"/><rect x="3" y="16" width="7" height="5" rx="1.5"/>')],
    ['Escenarios', '/atalaya/escenarios/', I('<path d="M4 6h10M18 6h2M4 12h2M10 12h10M4 18h12M20 18h0"/><circle cx="16" cy="6" r="2"/><circle cx="8" cy="12" r="2"/><circle cx="18" cy="18" r="2"/>')],
    ['Políticos', '/atalaya/politicos/', I('<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c0-3.6 2.9-6 6.5-6s6.5 2.4 6.5 6"/><path d="M16 4.6a3.5 3.5 0 0 1 0 6.8M18 14.5c2 .7 3.5 2.4 3.5 5.5"/>')],
    ['Programas', '/atalaya/programas/', I('<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 14l2 2 4-4"/>')],
    ['Medios', '/atalaya/medios/', I('<path d="M4 5h13a1 1 0 0 1 1 1v13H6a2 2 0 0 1-2-2zM18 9h2a1 1 0 0 1 1 1v7a2 2 0 0 1-2 2M8 9h6M8 13h6M8 16h4"/>')],
    ['Encuestas', '/atalaya/encuestas/', I('<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>')],
    ['Congreso', '/atalaya/congreso/', I('<path d="M3 20h18M5 20V10M9.5 20V10M14.5 20V10M19 20V10M3 10l9-6 9 6z"/>')],
    ['Senado', '/atalaya/senado/', I('<path d="M4 20h16M6 20v-8a6 6 0 0 1 12 0v8M12 6V3M9 20v-6M15 20v-6"/>')]
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
  // Pie común: Fichas y Privacidad. /atalaya/fuentes/ existe pero no se enlaza (uso privado).
  // Este script se carga al principio del <body>: el pie se añade cuando el documento está completo, para que quede al final.
  function pie() {
    var pf = document.createElement('footer');
    pf.className = 'pf';
    pf.innerHTML = '<a href="/atalaya/fichas/">Fichas</a><a href="/atalaya/privacidad/">Privacidad</a>';
    document.body.appendChild(pf);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', pie); else pie();
  sync();
})();
