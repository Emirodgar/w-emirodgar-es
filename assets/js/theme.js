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

  // Preguntas frecuentes: los párrafos «**¿Pregunta?** respuesta» bajo un h2 "Preguntas frecuentes" pasan a acordeón
  function buildFaq() {
    document.querySelectorAll('.sg-post h2, .sg-content h2').forEach(function (h) {
      if (!/^preguntas frecuentes/i.test(h.textContent.trim())) return;
      var box = null, node = h.nextElementSibling;
      while (node && node.tagName !== 'H2') {
        var next = node.nextElementSibling;
        var q = node.tagName === 'P' && node.firstElementChild && node.firstElementChild.tagName === 'STRONG' ? node.firstElementChild : null;
        if (q && /\?\s*$/.test(q.textContent) && node.firstChild === q) {
          if (!box) { box = document.createElement('div'); box.className = 'sg-faq'; node.parentNode.insertBefore(box, node); }
          var d = document.createElement('details'), sm = document.createElement('summary'), body = document.createElement('div');
          d.className = 'sg-faq__item'; body.className = 'sg-faq__body';
          sm.textContent = q.textContent.trim();
          q.remove();
          while (node.firstChild && (node.firstChild.nodeName === 'BR' || (node.firstChild.nodeType === 3 && !node.firstChild.textContent.trim()))) node.removeChild(node.firstChild);
          body.appendChild(node);
          d.appendChild(sm); d.appendChild(body); box.appendChild(d);
        } else if (box && node.tagName === 'HR') {
          node.remove();
        } else if (box) {
          box = null;
        }
        node = next;
      }
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    buildFaq();
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
