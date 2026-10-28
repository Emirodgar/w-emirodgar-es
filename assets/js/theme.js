/* Modo claro/oscuro, menú móvil, desplegable y enlace activo. Sin dependencias. */
(function () {
  var root = document.documentElement;

  function setTheme(dark) {
    if (dark) {
      root.setAttribute('dark', '');
      root.classList.add('dark-mode');
    } else {
      root.removeAttribute('dark');
      root.classList.remove('dark-mode');
    }
    try { localStorage.setItem('theme', dark ? 'dark' : 'light'); } catch (e) {}
    var btn = document.querySelector('.sg-theme');
    if (btn) btn.setAttribute('aria-label', dark ? 'Activar modo claro' : 'Activar modo oscuro');
  }

  document.addEventListener('DOMContentLoaded', function () {
    var theme = document.querySelector('.sg-theme');
    if (theme) {
      theme.setAttribute('aria-label', root.hasAttribute('dark') ? 'Activar modo claro' : 'Activar modo oscuro');
      theme.addEventListener('click', function () { setTheme(!root.hasAttribute('dark')); });
    }

    var burger = document.querySelector('.sg-hamburger');
    var nav = document.getElementById('sg-nav');
    if (burger && nav) {
      burger.addEventListener('click', function () {
        var open = nav.classList.toggle('is-visible');
        burger.classList.toggle('is-open', open);
        burger.setAttribute('aria-expanded', open);
      });
    }

    var drop = document.querySelector('.sg-dropdown');
    if (drop) {
      var toggle = drop.querySelector('.sg-dropdown__toggle');
      toggle.addEventListener('click', function () {
        var open = drop.classList.toggle('is-open');
        toggle.setAttribute('aria-expanded', open);
      });
      document.addEventListener('click', function (e) {
        if (!drop.contains(e.target)) { drop.classList.remove('is-open'); toggle.setAttribute('aria-expanded', 'false'); }
      });
    }

    // Enlace activo: el más específico que coincida con la ruta actual
    var path = location.pathname.replace(/\/index\.html$/, '/');
    var norm = function (p) { return p.replace(/\/$/, '') || '/'; };
    var best = null, bestLen = 0;
    document.querySelectorAll('.sg-header a[href]').forEach(function (a) {
      var u; try { u = new URL(a.getAttribute('href'), location.origin); } catch (e) { return; }
      if (u.origin !== location.origin || u.protocol.indexOf('http') !== 0) return;
      var p = norm(u.pathname), c = norm(path);
      if (p === '/' ) return;
      if (c === p || c.indexOf(p + '/') === 0) { if (p.length > bestLen) { best = a; bestLen = p.length; } }
    });
    if (best) {
      best.classList.add('active-link');
      best.setAttribute('aria-current', 'page');
      var menu = best.closest('.sg-dropdown');
      if (menu) menu.querySelector('.sg-dropdown__toggle').classList.add('active-link');
    }
  });
})();
