/* Atalaya: los mapas Leaflet arrancan "bloqueados" (la rueda y, en táctil, el arrastre con un dedo siguen desplazando la página).
   Se activan al hacer clic o tocar el mapa y se vuelven a bloquear al pulsar fuera de él. Cargar justo después de leaflet.js. */
(function () {
  if (!window.L || !L.Map) return;
  var tactil = !!(window.matchMedia && matchMedia('(pointer: coarse)').matches);
  L.Map.addInitHook(function () {
    var map = this, el = map.getContainer(), activo = null;
    function poner(on) {
      if (on === activo) return; activo = on;
      var f = on ? 'enable' : 'disable';
      if (map.scrollWheelZoom) map.scrollWheelZoom[f]();
      if (tactil && map.dragging) map.dragging[f]();
    }
    poner(false);
    el.addEventListener('pointerdown', function () { poner(true); }, true);
    document.addEventListener('pointerdown', function (e) { if (!el.contains(e.target)) poner(false); }, true);
  });
})();
