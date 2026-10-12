#!/usr/bin/env python3
"""Genera las páginas SEO del proyecto Elecciones en España a partir de los JSON de la convocatoria vigente.

    python scripts/elecciones/generar_paginas.py

Escribe:
  a-quien-votar/index.html          (test de afinidad ampliado + contenido explicativo)
  programas-electorales/index.html  (comparador de posiciones por tema)

El contenido (tablas, FAQ, JSON-LD) se escribe en el HTML para que los buscadores lo lean sin ejecutar
JavaScript; el JS solo añade la interactividad. Hay que volver a ejecutarlo cada vez que cambien los
JSON de proyectos/elecciones-espana/data/. La carpeta scripts/ no se publica (_config.yml: exclude).
"""
import html
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "proyectos" / "elecciones-espana" / "data"
SITE = "https://emirodgar.es"
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

POS_LABEL = {"favor": "A favor", "contra": "En contra", "matizada": "Matizada", "sin_posicion": "Sin posición clara"}
POS_ICON = {"favor": "✔", "contra": "✘", "matizada": "≈", "sin_posicion": "–"}
POS_CLASS = {
    "favor": "bg-emerald-50 text-emerald-800 border-emerald-200",
    "contra": "bg-rose-50 text-rose-800 border-rose-200",
    "matizada": "bg-amber-50 text-amber-800 border-amber-200",
    "sin_posicion": "bg-slate-50 text-slate-500 border-slate-200",
}

e = html.escape


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def slug(text):
    t = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")


def fecha_larga(iso):
    y, m, d = map(int, iso.split("-"))
    return f"{d} de {MESES[m - 1]} de {y}"


# ---------------------------------------------------------------- datos
idx = load(DATA / "elecciones.json")
actual = next(x for x in idx["elecciones"] if x["estado"] != "historica")
base = DATA / actual["id"]
conv = load(base / "convocatoria.json")
partidos_all = load(base / "partidos.json")["partidos"]
cand = {c["partidoId"]: c for c in load(base / "candidatos.json")["candidatos"]}
afi = load(base / "afinidad.json")
modified_iso = idx.get("lastUpdatedISO", actual["fecha"])
modified_txt = idx["lastUpdated"]
partidos = [p for p in partidos_all if p.get("enTest")]
pid = {p["id"]: p for p in partidos_all}
stm = afi["afirmaciones"]
temas = []
for a in stm:
    if a["tema"] not in temas:
        temas.append(a["tema"])
n_stm, n_temas = len(stm), len(temas)
fecha_elec = fecha_larga(actual["fecha"])
camp = next((h for h in conv["hitos"] if "Campaña" in h["titulo"]), None)
siglas_lista = ", ".join(p["siglas"] for p in partidos[:-1]) + " y " + partidos[-1]["siglas"]

# ---------------------------------------------------------------- bloques comunes
GROUP_NAV = [
    ("Panel y encuestas", "/proyectos/elecciones-espana/", "chart"),
    ("A quién votar", "/a-quien-votar/", "test"),
    ("Programas electorales", "/programas-electorales/", "prog"),
    ("Cómo votar", "/proyectos/elecciones-espana/#sec-votar", "votar"),
]


def head(title, desc, path, jsonld, extra_css=""):
    ld = "\n".join(f'    <script type="application/ld+json">{json.dumps(j, ensure_ascii=False)}</script>' for j in jsonld)
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{e(title)}</title>
    <meta name="description" content="{e(desc)}">
    <link rel="canonical" href="{SITE}{path}">
    <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
    <meta property="og:type" content="website">
    <meta property="og:locale" content="es_ES">
    <meta property="og:title" content="{e(title)}">
    <meta property="og:description" content="{e(desc)}">
    <meta property="og:url" content="{SITE}{path}">
    <meta property="og:image" content="https://emirodgar.com/cdn/images/og/estrategia-seo.png">
    <meta name="twitter:card" content="summary_large_image">
    <link rel="icon" href="https://emirodgar.com/cdn/images/hash.png" />
{ld}
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <script>
        tailwind.config = {{ theme: {{ extend: {{ fontFamily: {{ sans: ['Inter', 'sans-serif'] }}, colors: {{ brand: {{ 50: '#f0f7ff', 100: '#e0effe', 500: '#0284c7', 600: '#0369a1', 700: '#075985', 900: '#0c4a6e' }} }} }} }} }}
    </script>
    <style>
        body {{ font-family: 'Inter', sans-serif; }}
        html {{ scroll-behavior: smooth; scroll-padding-top: 5rem; }}
        details > summary {{ list-style: none; }}
        details > summary::-webkit-details-marker {{ display: none; }}
        details[open] .chev {{ transform: rotate(180deg); }}
        .bar-fill {{ transition: width .6s ease; }}
        .prose-x p {{ margin: .6rem 0; line-height: 1.7; }}
        .prose-x h2 {{ margin-top: 2rem; }}
{extra_css}
    </style>
</head>"""


def topbar(crumbs, active):
    bc = ' <span>/</span> '.join(
        f'<a href="{u}" class="hover:text-white transition">{e(t)}</a>' for t, u in crumbs
    )
    tabs = "".join(
        f'<a href="{u}" class="whitespace-nowrap px-3 py-2.5 border-b-2 {"border-brand-600 text-brand-600" if k == active else "border-transparent text-slate-500 hover:text-brand-600"}">{e(t)}</a>'
        for t, u, k in GROUP_NAV
    )
    return f"""<body class="bg-slate-50 text-slate-800 min-h-screen flex flex-col antialiased">
    <div class="bg-slate-950 text-slate-400 text-xs">
        <div class="max-w-5xl mx-auto px-4 sm:px-6 py-2 flex items-center gap-2 flex-wrap">{bc}</div>
    </div>
    <header class="bg-slate-900 text-white border-b border-slate-800">
        <div class="max-w-5xl mx-auto px-4 sm:px-6 py-3 flex items-center gap-3">
            <div class="p-2.5 bg-brand-600 rounded-xl shadow-lg"><i class="fa-solid fa-check-to-slot text-lg text-white"></i></div>
            <div><p class="font-bold leading-tight">Elecciones generales 2026</p><p class="text-xs text-slate-400">{e(fecha_elec)} · guía de voto y seguimiento</p></div>
        </div>
        <nav class="bg-white text-xs font-semibold overflow-x-auto" aria-label="Secciones de la guía electoral"><div class="max-w-5xl mx-auto px-4 sm:px-6 flex gap-2">{tabs}</div></nav>
    </header>"""


def related(active):
    cards = {
        "chart": ("Panel y encuestas", "Cuenta atrás, calendario, media de encuestas, candidatos y Congreso.", "/proyectos/elecciones-espana/", "fa-chart-line"),
        "test": ("A quién votar: test de afinidad", f"{n_stm} preguntas para saber con qué partido coincides más, con sus fuentes.", "/a-quien-votar/", "fa-wand-magic-sparkles"),
        "prog": ("Programas electorales por temas", "Qué propone cada partido en vivienda, sanidad, pensiones, impuestos…", "/programas-electorales/", "fa-scale-balanced"),
        "votar": ("Cómo votar el 29N", "Voto por correo, papeletas, plazos y el simulador de la ley D'Hondt.", "/proyectos/elecciones-espana/#sec-votar", "fa-envelope-open-text"),
    }
    items = "".join(
        f'<a href="{u}" class="block bg-white rounded-xl border border-slate-200 p-4 hover:border-brand-500 transition"><i class="fa-solid {ic} text-brand-600 mb-2"></i><h3 class="font-semibold text-sm text-slate-900">{e(t)}</h3><p class="text-xs text-slate-500 mt-1 leading-snug">{e(d)}</p></a>'
        for k, (t, d, u, ic) in cards.items() if k != active
    )
    return f"""<section aria-labelledby="rel" class="space-y-3"><h2 id="rel" class="text-lg font-bold">Sigue explorando las elecciones generales</h2><div class="grid sm:grid-cols-3 gap-3">{items}</div></section>"""


def footer():
    return f"""<footer class="bg-slate-900 text-slate-400 text-xs mt-10">
        <div class="max-w-5xl mx-auto px-4 sm:px-6 py-6 space-y-2">
            <p>Proyecto educativo y experimental de <a class="text-slate-200 underline" href="https://emirodgar.es/">Emilio Rodríguez (Emirodgar)</a>, sin vinculación con ningún partido ni administración. Actualizado el {e(modified_txt)}.</p>
            <p>Datos oficiales: <a class="underline" href="https://www.juntaelectoralcentral.es" target="_blank" rel="noopener">Junta Electoral Central</a> · <a class="underline" href="https://www.infoelectoral.interior.gob.es" target="_blank" rel="noopener">Ministerio del Interior</a>. <a class="underline" href="https://emirodgar.es/elecciones-espana">Documentación del proyecto</a>.</p>
        </div></footer>"""


def byline():
    return f'<p class="text-xs text-slate-500">Por <a class="underline" href="https://emirodgar.es/sobre-mi.html">Emilio Rodríguez</a> · Actualizado el <time datetime="{modified_iso}">{e(modified_txt)}</time> · Todas las posiciones llevan su fuente enlazada</p>'


def faq_block(faq):
    items = "".join(
        f'<details class="bg-white rounded-xl border border-slate-200"><summary class="cursor-pointer p-4 flex items-center justify-between gap-3 text-sm font-semibold text-slate-900"><h3 class="text-sm font-semibold">{e(q)}</h3><i class="fa-solid fa-chevron-down chev text-xs text-slate-400 transition-transform"></i></summary><p class="px-4 pb-4 text-sm text-slate-600 leading-relaxed">{e(a)}</p></details>'
        for q, a in faq
    )
    return f'<section aria-labelledby="faq" class="space-y-3"><h2 id="faq" class="text-lg font-bold">Preguntas frecuentes</h2>{items}</section>'


def faq_ld(faq):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}


def breadcrumb_ld(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(items)]}


def webpage_ld(name, desc, path):
    return {"@context": "https://schema.org", "@type": "WebPage", "name": name, "description": desc, "url": SITE + path,
            "inLanguage": "es-ES", "dateModified": modified_iso,
            "author": {"@type": "Person", "name": "Emilio Rodríguez", "url": SITE + "/sobre-mi.html"},
            "isPartOf": {"@type": "WebSite", "name": "Emirodgar", "url": SITE + "/"}}


def pos_chip(pos):
    return f'<span class="inline-flex items-center gap-1 text-[11px] font-semibold px-2 py-0.5 rounded border {POS_CLASS[pos]}"><span aria-hidden="true">{POS_ICON[pos]}</span>{POS_LABEL[pos]}</span>'


def source_link(p):
    if not p.get("fuente"):
        return ""
    f = f' ({e(p["fecha"])})' if p.get("fecha") else ""
    return f'<a class="text-brand-600 underline" href="{e(p["fuente"])}" target="_blank" rel="noopener nofollow">Fuente{f}</a>'


def compact_matrix():
    head_cells = "".join(f'<th scope="col" class="px-2 py-2 text-center font-semibold" style="color:{p["color"]}">{e(p["siglas"])}</th>' for p in partidos)
    rows = ""
    for t in temas:
        rows += f'<tr class="bg-slate-50"><th colspan="{len(partidos) + 1}" scope="colgroup" class="px-3 py-1.5 text-left text-[11px] uppercase tracking-wide text-slate-500">{e(t)}</th></tr>'
        for a in stm:
            if a["tema"] != t:
                continue
            cells = "".join(f'<td class="px-2 py-2 text-center">{pos_chip(a["posiciones"].get(p["id"], {}).get("posicion", "sin_posicion"))}</td>' for p in partidos)
            rows += f'<tr class="border-t border-slate-100"><th scope="row" class="px-3 py-2 text-left font-medium text-slate-800 min-w-[16rem]">{e(a["texto"])}</th>{cells}</tr>'
    return f'<div class="overflow-x-auto bg-white rounded-xl border border-slate-200"><table class="w-full text-sm"><caption class="sr-only">Posición de cada partido sobre {n_stm} propuestas</caption><thead class="text-xs"><tr><th scope="col" class="px-3 py-2 text-left font-semibold text-slate-500">Propuesta</th>{head_cells}</tr></thead><tbody>{rows}</tbody></table></div>'


def candidates_list():
    rows = ""
    for p in partidos_all:
        c = cand.get(p["id"])
        if p["ambito"] != "estatal" or not c:
            continue
        nom = e(c["nombre"]) if c.get("nombre") else "por definir"
        rows += f'<li class="flex items-center gap-3"><span class="w-14 text-center text-xs font-extrabold text-white rounded py-1" style="background:{p["color"]}">{e(p["siglas"])}</span><span class="text-sm"><strong>{nom}</strong> <span class="text-slate-500">· {e(p["nombre"])}</span></span></li>'
    return f'<ul class="space-y-2">{rows}</ul>'


# ---------------------------------------------------------------- A QUIÉN VOTAR
TEST_JS = r"""
(function () {
    'use strict';
    const D = JSON.parse(document.getElementById('test-data').textContent);
    const $ = id => document.getElementById(id);
    const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
    const LABEL = { favor: 'A favor', contra: 'En contra', matizada: 'Matizada', sin_posicion: 'Sin posición clara' };
    const S = { prior: new Set(), ans: {}, step: -1 };   // step -1 = temas prioritarios; 0..n-1 = preguntas; n = resultados
    const N = D.statements.length;

    function score() {
        return D.parties.map(p => {
            let num = 0, den = 0, used = 0, answered = 0; const byTema = {}, agree = [], disagree = [];
            D.statements.forEach(s => {
                const a = S.ans[s.id]; if (!a) return;
                answered++;
                const pos = s.pos[p.id]; const w = S.prior.has(s.tema) ? 2 : 1;
                if (!pos || pos.p === 'sin_posicion') return;
                const m = pos.p === 'matizada' ? 0.5 : ((pos.p === 'favor' ? 1 : -1) === a ? 1 : 0);
                num += w * m; den += w; used++;
                const t = byTema[s.tema] || (byTema[s.tema] = { n: 0, d: 0 }); t.n += m; t.d += 1;
                (m === 1 ? agree : m === 0 ? disagree : []).push({ s, pos, a });
            });
            return { p, score: den ? num / den * 100 : null, used, answered, byTema, agree, disagree };
        }).sort((x, y) => (y.score ?? -1) - (x.score ?? -1));
    }

    function encode() {
        const pr = D.temas.map((t, i) => S.prior.has(t) ? i : -1).filter(i => i >= 0).join(',');
        const an = D.statements.map(s => S.ans[s.id] === 1 ? 'a' : S.ans[s.id] === -1 ? 'd' : 'n').join('');
        return pr + '.' + an;
    }
    function decode(h) {
        const [pr, an] = h.split('.'); if (!an || an.length !== N) return false;
        S.prior = new Set(pr ? pr.split(',').map(i => D.temas[+i]).filter(Boolean) : []);
        S.ans = {}; D.statements.forEach((s, i) => { if (an[i] === 'a') S.ans[s.id] = 1; else if (an[i] === 'd') S.ans[s.id] = -1; });
        return true;
    }

    function render() {
        const box = $('test-box');
        if (S.step === -1) {
            box.innerHTML = `<div class="p-6 sm:p-8 space-y-5">
              <div><p class="text-xs font-semibold uppercase tracking-wide text-brand-600">Paso 1 · Tus prioridades</p>
              <h2 class="text-xl sm:text-2xl font-bold mt-1">¿Qué temas te importan más a la hora de votar?</h2>
              <p class="text-sm text-slate-500 mt-1">Elige hasta 3. Las preguntas de esos temas pesarán el doble en tu resultado. Puedes saltarte este paso.</p></div>
              <div class="flex flex-wrap gap-2" id="prior-chips">${D.temas.map(t => `<button type="button" data-t="${esc(t)}" aria-pressed="${S.prior.has(t)}" class="chip px-3 py-1.5 rounded-full border text-sm font-medium ${S.prior.has(t) ? 'bg-brand-600 text-white border-brand-600' : 'bg-white text-slate-700 border-slate-300 hover:border-brand-500'}">${esc(t)}</button>`).join('')}</div>
              <button id="start" class="px-5 py-2.5 bg-brand-600 hover:bg-brand-700 text-white rounded-lg text-sm font-semibold">Empezar el test (${N} preguntas)</button>
              <p class="text-xs text-slate-400">Tus respuestas no se guardan ni se envían: todo se calcula en tu navegador.</p></div>`;
            box.querySelectorAll('.chip').forEach(b => b.onclick = () => { const t = b.dataset.t; if (S.prior.has(t)) S.prior.delete(t); else if (S.prior.size < 3) S.prior.add(t); render(); });
            $('start').onclick = () => { S.step = 0; render(); };
            return;
        }
        if (S.step >= N) return results();
        const s = D.statements[S.step], cur = S.ans[s.id];
        box.innerHTML = `<div class="h-1.5 bg-slate-100"><div class="bar-fill h-full bg-brand-600" style="width:${Math.round(S.step / N * 100)}%"></div></div>
          <div class="p-6 sm:p-8 space-y-6">
            <div><p class="text-xs font-semibold uppercase tracking-wide text-brand-600">${esc(s.tema)} · Pregunta ${S.step + 1} de ${N}${S.prior.has(s.tema) ? ' · <span class="text-amber-600">prioritaria</span>' : ''}</p>
            <h2 class="text-xl sm:text-2xl font-bold text-slate-900 mt-1">${esc(s.texto)}</h2></div>
            <div class="grid sm:grid-cols-3 gap-3">
              <button data-v="1" class="ans py-3 rounded-xl border-2 font-semibold text-sm border-emerald-200 hover:border-emerald-500 hover:bg-emerald-50 ${cur === 1 ? 'border-emerald-500 bg-emerald-50' : ''}"><i class="fa-solid fa-thumbs-up mr-1"></i> De acuerdo</button>
              <button data-v="0" class="ans py-3 rounded-xl border-2 font-semibold text-sm border-slate-200 hover:border-slate-400 hover:bg-slate-50"><i class="fa-solid fa-forward mr-1"></i> Paso / no lo sé</button>
              <button data-v="-1" class="ans py-3 rounded-xl border-2 font-semibold text-sm border-rose-200 hover:border-rose-500 hover:bg-rose-50 ${cur === -1 ? 'border-rose-500 bg-rose-50' : ''}"><i class="fa-solid fa-thumbs-down mr-1"></i> En desacuerdo</button>
            </div>
            <div class="flex justify-between text-xs"><button id="back" class="text-slate-500 hover:text-slate-800"><i class="fa-solid fa-arrow-left"></i> Anterior</button><button id="finish" class="text-brand-600 font-semibold hover:underline">Ver resultados ahora</button></div>
          </div>`;
        box.querySelectorAll('.ans').forEach(b => b.onclick = () => { const v = +b.dataset.v; if (v === 0) delete S.ans[s.id]; else S.ans[s.id] = v; S.step++; render(); });
        $('back').onclick = () => { S.step--; render(); };
        $('finish').onclick = () => { S.step = N; render(); };
        box.scrollIntoView({ block: 'nearest' });
    }

    function results() {
        const box = $('test-box'), res = score(), answered = res[0].answered;
        if (!answered) { box.innerHTML = `<div class="p-8 text-center space-y-4"><p class="text-slate-600">No has respondido a ninguna pregunta todavía.</p><button id="again" class="px-4 py-2 bg-brand-600 text-white rounded-lg text-sm font-semibold">Empezar el test</button></div>`; $('again').onclick = () => { S.step = -1; render(); }; return; }
        history.replaceState(null, '', '#r=' + encode());
        const top = res[0], second = res[1];
        const close = second && second.score != null && top.score != null && top.score - second.score < 5;
        const cols = D.parties.map(p => p.id);
        const temasUsados = D.temas.filter(t => res.some(r => r.byTema[t]));
        const cell = (r, t) => { const x = r.byTema[t]; if (!x) return '<td class="px-2 py-2 text-center text-slate-300">–</td>'; const v = Math.round(x.n / x.d * 100); return `<td class="px-2 py-2 text-center"><span class="inline-block min-w-[3rem] rounded px-1.5 py-0.5 text-xs font-bold ${v >= 70 ? 'bg-emerald-100 text-emerald-800' : v >= 40 ? 'bg-amber-100 text-amber-800' : 'bg-rose-100 text-rose-800'}">${v} %</span></td>`; };
        const list = (arr, empty) => arr.length ? arr.map(x => `<li class="py-2"><p class="text-sm font-medium text-slate-800">${esc(x.s.texto)}</p><p class="text-xs text-slate-500 mt-0.5">${esc(top.p.siglas)}: <strong>${LABEL[x.pos.p]}</strong>${x.pos.c ? ' · «' + esc(x.pos.c) + '»' : ''} ${x.pos.f ? `<a class="text-brand-600 underline" target="_blank" rel="noopener nofollow" href="${esc(x.pos.f)}">fuente${x.pos.d ? ' (' + esc(x.pos.d) + ')' : ''}</a>` : ''}</p></li>`).join('') : `<li class="py-2 text-sm text-slate-400">${empty}</li>`;
        box.innerHTML = `<div class="p-6 sm:p-8 space-y-7">
          <div class="rounded-xl p-5 text-white" style="background:${top.p.color}">
            <p class="text-xs uppercase tracking-wide opacity-90">Tu mayor afinidad según tus respuestas</p>
            <p class="text-3xl font-extrabold mt-1">${esc(top.p.nombre)} · ${Math.round(top.score)} %</p>
            <p class="text-sm mt-1 opacity-95">${close ? `Casi empatado con ${esc(second.p.nombre)} (${Math.round(second.score)} %): la diferencia es pequeña y no es concluyente.` : 'Es el partido cuyas posiciones documentadas más se parecen a las tuyas en las preguntas que has respondido.'}</p>
          </div>
          <div class="space-y-3"><h2 class="text-lg font-bold">Afinidad con cada partido</h2>
            ${res.map(r => `<div class="flex items-center gap-3"><div class="w-16 text-center text-xs font-extrabold text-white rounded py-1.5" style="background:${r.p.color}">${esc(r.p.siglas)}</div><div class="flex-1"><div class="h-3 bg-slate-100 rounded-full overflow-hidden"><div class="bar-fill h-full rounded-full" style="width:${r.score ?? 0}%;background:${r.p.color}"></div></div><p class="text-[11px] text-slate-400 mt-0.5">Sobre ${r.used} de ${r.answered} respuestas con posición documentada</p></div><span class="text-lg font-extrabold tabular-nums w-14 text-right">${r.score == null ? '–' : Math.round(r.score) + ' %'}</span></div>`).join('')}</div>
          <div class="space-y-2"><h2 class="text-lg font-bold">Por qué: afinidad por temas</h2><p class="text-xs text-slate-500">Porcentaje de coincidencia en cada tema, solo con las preguntas que has respondido.</p>
            <div class="overflow-x-auto"><table class="w-full text-sm"><thead class="text-xs text-slate-500"><tr><th class="text-left px-2 py-2">Tema</th>${res.map(r => `<th class="px-2 py-2" style="color:${r.p.color}">${esc(r.p.siglas)}</th>`).join('')}</tr></thead><tbody>${temasUsados.map(t => `<tr class="border-t border-slate-100"><th scope="row" class="text-left px-2 py-2 font-medium">${esc(t)}${S.prior.has(t) ? ' <span class="text-[10px] text-amber-600 font-semibold">prioritario</span>' : ''}</th>${res.map(r => cell(r, t)).join('')}</tr>`).join('')}</tbody></table></div></div>
          <div class="grid md:grid-cols-2 gap-6"><div><h2 class="text-lg font-bold text-emerald-700">En qué coincides con ${esc(top.p.siglas)}</h2><ul class="divide-y divide-slate-100">${list(top.agree, 'No hay coincidencias claras.')}</ul></div>
          <div><h2 class="text-lg font-bold text-rose-700">En qué discrepas con ${esc(top.p.siglas)}</h2><ul class="divide-y divide-slate-100">${list(top.disagree, 'No hay discrepancias claras.')}</ul></div></div>
          <div class="flex flex-wrap gap-3 text-sm"><button id="copy" class="px-4 py-2 bg-slate-900 text-white rounded-lg font-semibold"><i class="fa-solid fa-link"></i> Copiar enlace a mis resultados</button><button id="again" class="px-4 py-2 border border-slate-300 rounded-lg font-semibold"><i class="fa-solid fa-rotate-left"></i> Repetir el test</button><a href="/programas-electorales/" class="px-4 py-2 border border-slate-300 rounded-lg font-semibold">Comparar programas por temas →</a></div>
          <p class="text-xs text-slate-500 leading-relaxed bg-slate-50 rounded-lg p-3">${esc(D.aviso)}</p></div>`;
        $('again').onclick = () => { S.ans = {}; S.prior = new Set(); S.step = -1; history.replaceState(null, '', location.pathname); render(); };
        $('copy').onclick = () => { navigator.clipboard && navigator.clipboard.writeText(location.href).then(() => { $('copy').innerHTML = '<i class="fa-solid fa-check"></i> Enlace copiado'; }); };
        box.scrollIntoView({ block: 'start' });
    }

    const m = location.hash.match(/^#r=(.+)$/);
    if (m && decode(m[1])) S.step = N;
    render();
})();
"""


def build_a_quien_votar():
    path = "/a-quien-votar/"
    title = "¿A quién votar? Test de afinidad con los partidos 2026"
    desc = (f"Test gratuito para saber a qué partido votar en las elecciones generales del {fecha_elec}: {n_stm} preguntas, "
            f"compara tus ideas con {siglas_lista} y explica el porqué con fuentes.")
    faq = [
        ("¿A quién votar en las elecciones generales de 2026?",
         f"No hay una respuesta única: depende de los temas que más te importen. Este test compara tus opiniones en {n_stm} cuestiones concretas con las posiciones documentadas de {siglas_lista} y te muestra con cuál coincides más y en qué temas. Las elecciones se celebran el {fecha_elec}."),
        ("¿Cómo puedo saber qué partido me representa?",
         f"Responde a las {n_stm} preguntas del test, indica opcionalmente hasta tres temas prioritarios y consulta tu resultado: verás el porcentaje de afinidad con cada partido, el desglose por temas y las propuestas en las que coincides o discrepas, cada una con su fuente."),
        ("¿Cómo se calcula el porcentaje de afinidad?",
         "Cada respuesta se compara con la posición documentada del partido: coincidencia plena suma 1, posición matizada suma 0,5 y desacuerdo suma 0. Las preguntas de tus temas prioritarios pesan el doble. Las afirmaciones en las que un partido no tiene una posición clara y verificable no cuentan para ese partido."),
        ("¿Qué partido es el mejor o el más fiable?",
         "Ninguna web puede decirte objetivamente cuál es el mejor partido: depende de tus prioridades. Lo que sí se puede hacer es comparar sus propuestas con fuentes, que es lo que hace este test y el comparador de programas electorales. Para valorar la fiabilidad conviene contrastar lo prometido con lo votado en el Congreso y publicado en el BOE."),
        ("¿Es un test neutral?",
         "Todos los partidos se tratan con el mismo formato y criterio, cada posición cita una fuente y, cuando no hay evidencia clara, se marca «sin posición» en lugar de suponerla. Aun así es una herramienta orientativa, no una recomendación de voto."),
        ("¿Se guardan mis respuestas?",
         "No. El cálculo se hace en tu navegador y no se envía nada a ningún servidor. Si copias el enlace a tus resultados, tus respuestas viajan codificadas en la propia URL."),
        ("¿Qué partidos incluye el test?",
         f"Los partidos de ámbito estatal con presencia en el Congreso: {siglas_lista}. Los partidos autonómicos (ERC, Junts, EH Bildu, PNV, BNG, CC, UPN, Compromís…) solo se presentan en su territorio y aparecen en la guía de candidatos del panel de elecciones."),
        ("¿Ya se han publicado los programas electorales de 2026?",
         "Todavía no. Las posiciones del test se basan en programas anteriores, votaciones y declaraciones públicas recientes, con la fuente enlazada. Se revisarán cuando cada partido publique su programa oficial, previsiblemente al inicio de la campaña" + (f" ({fecha_larga(camp['fecha'])})." if camp else ".")),
    ]
    jsonld = [
        webpage_ld(title, desc, path),
        {"@context": "https://schema.org", "@type": "WebApplication", "name": "Test «¿A quién votar?» de las elecciones generales 2026",
         "url": SITE + path, "applicationCategory": "EducationalApplication", "operatingSystem": "Web", "inLanguage": "es-ES",
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"}, "description": desc},
        breadcrumb_ld([("Inicio", "/"), ("Elecciones generales 2026", "/proyectos/elecciones-espana/"), ("A quién votar", path)]),
        faq_ld(faq),
    ]
    test_data = {
        "aviso": afi["aviso"],
        "temas": temas,
        "parties": [{"id": p["id"], "siglas": p["siglas"], "nombre": p["nombre"], "color": p["color"]} for p in partidos],
        "statements": [{"id": a["id"], "tema": a["tema"], "texto": a["texto"],
                        "pos": {k: {"p": v["posicion"], "c": v.get("cita", ""), "f": v.get("fuente", ""), "d": v.get("fecha", "")} for k, v in a["posiciones"].items()}} for a in stm],
    }
    td = json.dumps(test_data, ensure_ascii=False).replace("</", "<\\/")
    h = head(title, desc, path, jsonld)
    body = f"""{topbar([("Emirodgar.es", "/"), ("Proyectos", "/proyectos"), ("Elecciones generales 2026", "/proyectos/elecciones-espana/"), ("A quién votar", path)], "test")}
    <main class="flex-grow max-w-5xl w-full mx-auto px-4 sm:px-6 py-8 space-y-10">
        <section class="space-y-3">
            <h1 class="text-3xl sm:text-4xl font-extrabold tracking-tight text-slate-900">¿A quién votar en las elecciones generales de 2026?</h1>
            <p class="text-lg text-slate-600">Contesta {n_stm} preguntas sobre {n_temas} temas ({e(', '.join(t.lower() for t in temas[:5]))}…) y descubre con qué partido coincides más, <strong>por qué</strong> y con qué fuentes.</p>
            {byline()}
        </section>

        <section id="test" aria-label="Test de afinidad" class="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden"><div id="test-box"><noscript><p class="p-6 text-sm text-slate-600">El test necesita JavaScript. Mientras tanto, puedes consultar la tabla de posiciones de más abajo.</p></noscript></div></section>

        <section class="prose-x space-y-2 text-slate-700">
            <h2 class="text-xl font-bold text-slate-900">Cómo funciona este test para decidir tu voto</h2>
            <p>Las elecciones generales del <strong>{e(fecha_elec)}</strong> renuevan el Congreso (350 diputados) y el Senado. Para decidir tu voto no basta con la intención de voto: importa qué piensa cada partido sobre las cuestiones concretas que te afectan. Este test te presenta {n_stm} afirmaciones y compara tu respuesta con la <strong>posición documentada</strong> de {e(siglas_lista)}.</p>
            <ol class="list-decimal pl-6 space-y-1">
                <li><strong>Elige tus prioridades.</strong> Los temas que marques pesan el doble.</li>
                <li><strong>Responde</strong> «de acuerdo», «en desacuerdo» o «paso» a cada afirmación.</li>
                <li><strong>Consulta el resultado:</strong> porcentaje de afinidad por partido, desglose por temas y las propuestas en las que coincides o discrepas, con su fuente.</li>
            </ol>
            <h2 class="text-xl font-bold text-slate-900">¿Qué partido es el mejor o el más fiable?</h2>
            <p>Es una de las búsquedas más habituales y la respuesta honesta es que <strong>no existe un mejor partido en abstracto</strong>: depende de qué te importe. Quien prioriza la vivienda, la fiscalidad o la inmigración puede coincidir con partidos muy distintos. Por eso este test no emite un veredicto: calcula la afinidad con tus propias respuestas.</p>
            <p>Para valorar la <strong>fiabilidad</strong> de un partido, lo más sólido es contrastar lo que promete con lo que ha votado y aprobado: las votaciones del Congreso, el BOE y los programas anteriores. Cada posición de esta página enlaza a su fuente para que puedas comprobarla. Tienes todas las propuestas ordenadas por temas en el <a class="text-brand-600 underline" href="/programas-electorales/">comparador de programas electorales</a>.</p>
            <h2 class="text-xl font-bold text-slate-900">Metodología y límites</h2>
            <p>Cada respuesta se compara con la posición del partido: coincidencia plena suma 1, posición matizada 0,5 y desacuerdo 0; las preguntas de tus temas prioritarios pesan el doble. Si un partido no tiene una posición clara y verificable en una afirmación, esa pregunta no cuenta para él, y el resultado indica sobre cuántas respuestas se ha calculado.</p>
            <p>{e(afi["aviso"])}</p>
        </section>

        <section aria-labelledby="matriz" class="space-y-3">
            <h2 id="matriz" class="text-xl font-bold">Posiciones de los partidos sobre {n_stm} propuestas</h2>
            <p class="text-sm text-slate-600">Resumen de las posiciones documentadas que usa el test. La cita y la fuente de cada una están en el <a class="text-brand-600 underline" href="/programas-electorales/">comparador de programas electorales</a>.</p>
            {compact_matrix()}
        </section>

        <section aria-labelledby="quien" class="space-y-3">
            <h2 id="quien" class="text-xl font-bold">¿Quién encabeza las listas?</h2>
            <p class="text-sm text-slate-600">Cabezas de lista anunciadas por los partidos de ámbito estatal. Las listas definitivas se proclaman el 2 de noviembre. Más datos en el <a class="text-brand-600 underline" href="/proyectos/elecciones-espana/#sec-partidos">panel de elecciones</a>.</p>
            {candidates_list()}
        </section>

        {faq_block(faq)}
        {related("test")}
    </main>
    {footer()}
    <script type="application/json" id="test-data">{td}</script>
    <script>{TEST_JS}</script>
</body>
</html>
"""
    out = ROOT / "a-quien-votar" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(h + "\n" + body, encoding="utf-8")


# ---------------------------------------------------------------- PROGRAMAS ELECTORALES
COMP_JS = r"""
(function () {
    const tabs = document.querySelectorAll('[data-tema-btn]');
    const secs = document.querySelectorAll('[data-tema]');
    function show(t) {
        tabs.forEach(b => { const on = b.dataset.temaBtn === t; b.className = b.className.replace(/ ?(bg-brand-600 text-white border-brand-600|bg-white text-slate-700 border-slate-300)/g, '') + (on ? ' bg-brand-600 text-white border-brand-600' : ' bg-white text-slate-700 border-slate-300'); b.setAttribute('aria-pressed', on); });
        secs.forEach(s => s.classList.toggle('hidden', t !== 'todos' && s.dataset.tema !== t));
        if (t !== 'todos') history.replaceState(null, '', '#' + t); else history.replaceState(null, '', location.pathname);
    }
    tabs.forEach(b => b.onclick = () => show(b.dataset.temaBtn));
    const h = location.hash.slice(1);
    if (h && [...secs].some(s => s.dataset.tema === h)) show(h);
})();
"""


def build_programas():
    path = "/programas-electorales/"
    title = "Programas electorales 2026: comparador de propuestas"
    desc = (f"Qué propone cada partido en las elecciones generales del {fecha_elec}: compara {siglas_lista} por temas "
            f"(vivienda, sanidad, impuestos, pensiones…) con la cita y la fuente de cada posición.")
    pend = [p for p in partidos if not p.get("programaUrl")]
    estado_prog = (f"Ninguno de los {len(partidos)} partidos de ámbito estatal ha publicado todavía su programa electoral oficial para 2026"
                   if len(pend) == len(partidos) else f"{len(partidos) - len(pend)} de {len(partidos)} partidos han publicado ya su programa")
    faq = [
        ("¿Dónde puedo leer los programas electorales de 2026?",
         f"{estado_prog}. Los partidos suelen presentarlos al inicio de la campaña" + (f" ({fecha_larga(camp['fecha'])})" if camp else "") + ". Esta página enlaza a la web oficial de cada partido y se actualizará con cada programa en cuanto se publique."),
        ("¿Qué propone cada partido en las elecciones generales?",
         f"Hasta que se publiquen los programas, esta página recoge sus posiciones conocidas sobre {n_stm} propuestas en {n_temas} temas ({', '.join(t.lower() for t in temas)}), cada una con una cita y la fuente en la que se basa."),
        ("¿De dónde salen las posiciones de cada partido?",
         "De programas electorales anteriores, votaciones en el Congreso, notas oficiales y declaraciones públicas recientes publicadas en medios, siempre con el enlace a la fuente. Si no hay evidencia clara, se marca «sin posición clara» en lugar de suponerla."),
        ("¿Puedo saber con qué partido coincido más?",
         "Sí. El test «¿A quién votar?» compara tus respuestas con estas mismas posiciones y calcula tu afinidad con cada partido, con el desglose por temas."),
        ("¿Qué partidos se comparan?",
         f"Los de ámbito estatal con presencia en el Congreso: {siglas_lista}. Los partidos autonómicos se presentan solo en su territorio."),
    ]
    jsonld = [webpage_ld(title, desc, path),
              breadcrumb_ld([("Inicio", "/"), ("Elecciones generales 2026", "/proyectos/elecciones-espana/"), ("Programas electorales", path)]),
              faq_ld(faq)]
    tab_btns = '<button type="button" data-tema-btn="todos" aria-pressed="true" class="px-3 py-1.5 rounded-full border text-sm font-medium bg-brand-600 text-white border-brand-600">Todos los temas</button>' + "".join(
        f'<button type="button" data-tema-btn="{slug(t)}" aria-pressed="false" class="px-3 py-1.5 rounded-full border text-sm font-medium bg-white text-slate-700 border-slate-300">{e(t)}</button>' for t in temas)
    secciones = ""
    for t in temas:
        bloques = ""
        for a in [x for x in stm if x["tema"] == t]:
            filas = ""
            for p in partidos:
                x = a["posiciones"].get(p["id"], {"posicion": "sin_posicion", "cita": "Sin evidencia clara de su posición."})
                filas += (f'<tr class="border-t border-slate-100 align-top"><th scope="row" class="px-3 py-2.5 text-left whitespace-nowrap"><span class="inline-block w-2.5 h-2.5 rounded-full mr-1.5" style="background:{p["color"]}"></span>{e(p["siglas"])}</th>'
                          f'<td class="px-3 py-2.5">{pos_chip(x["posicion"])}</td>'
                          f'<td class="px-3 py-2.5 text-slate-600">{e(x.get("cita", ""))}</td><td class="px-3 py-2.5 whitespace-nowrap text-xs">{source_link(x)}</td></tr>')
            bloques += (f'<div class="bg-white rounded-xl border border-slate-200 overflow-hidden"><h3 class="px-4 py-3 bg-slate-50 font-semibold text-slate-900 text-sm">«{e(a["texto"])}»</h3>'
                        f'<div class="overflow-x-auto"><table class="w-full text-sm"><thead class="text-xs text-slate-500"><tr><th scope="col" class="px-3 py-2 text-left">Partido</th><th scope="col" class="px-3 py-2 text-left">Posición</th><th scope="col" class="px-3 py-2 text-left">Qué dice</th><th scope="col" class="px-3 py-2 text-left">Fuente</th></tr></thead><tbody>{filas}</tbody></table></div></div>')
        secciones += f'<section id="{slug(t)}" data-tema="{slug(t)}" class="space-y-3"><h2 class="text-xl font-bold">{e(t)}: qué propone cada partido</h2>{bloques}</section>'
    def _lnk(url, text):
        return f'<a class="text-brand-600 underline" href="{e(url)}" target="_blank" rel="noopener">{text}</a>'

    prog_rows = ""
    for p in partidos:
        prog = _lnk(p["programaUrl"], "Programa electoral oficial") if p.get("programaUrl") else '<span class="text-slate-400">Pendiente de publicación</span>'
        web = _lnk(p["web"], "Web oficial") if p.get("web") else "–"
        prog_rows += (f'<tr class="border-t border-slate-100"><th scope="row" class="px-3 py-2 text-left"><span class="inline-block w-2.5 h-2.5 rounded-full mr-1.5" style="background:{p["color"]}"></span>{e(p["nombre"])}</th>'
                      f'<td class="px-3 py-2 text-sm">{prog}</td><td class="px-3 py-2 text-sm">{web}</td></tr>')
    h = head(title, desc, path, jsonld)
    body = f"""{topbar([("Emirodgar.es", "/"), ("Proyectos", "/proyectos"), ("Elecciones generales 2026", "/proyectos/elecciones-espana/"), ("Programas electorales", path)], "prog")}
    <main class="flex-grow max-w-5xl w-full mx-auto px-4 sm:px-6 py-8 space-y-10">
        <section class="space-y-3">
            <h1 class="text-3xl sm:text-4xl font-extrabold tracking-tight text-slate-900">Programas electorales 2026: qué propone cada partido</h1>
            <p class="text-lg text-slate-600">Compara a {e(siglas_lista)} en {n_temas} temas, con la cita y la fuente de cada posición. Elecciones generales del {e(fecha_elec)}.</p>
            {byline()}
            <p class="text-sm bg-amber-50 border border-amber-200 text-amber-900 rounded-lg p-3"><strong>Estado de los programas:</strong> {e(estado_prog)}. Mientras tanto se muestran sus posiciones conocidas (programas anteriores, votaciones y declaraciones recientes), que se sustituirán por las del programa oficial cuando se publique.</p>
        </section>

        <section aria-label="Filtrar por tema" class="space-y-3"><div class="flex flex-wrap gap-2" role="group">{tab_btns}</div>
            <p class="text-sm text-slate-600">¿Prefieres que te digamos con cuál coincides más? Haz el <a class="text-brand-600 underline font-semibold" href="/a-quien-votar/">test «¿A quién votar?»</a>.</p></section>

        {secciones}

        <section aria-labelledby="oficial" class="space-y-3"><h2 id="oficial" class="text-xl font-bold">Programas oficiales y webs de los partidos</h2>
            <div class="overflow-x-auto bg-white rounded-xl border border-slate-200"><table class="w-full text-sm"><thead class="text-xs text-slate-500"><tr><th scope="col" class="px-3 py-2 text-left">Partido</th><th scope="col" class="px-3 py-2 text-left">Programa 2026</th><th scope="col" class="px-3 py-2 text-left">Web</th></tr></thead><tbody>{prog_rows}</tbody></table></div></section>

        <section class="prose-x text-slate-700"><h2 class="text-xl font-bold text-slate-900">Cómo se han recopilado estas posiciones</h2>
            <p>Cada posición procede de una fuente enlazada: programas electorales anteriores, votaciones del Congreso, notas oficiales de los partidos o declaraciones recogidas por medios. Cuando no hay evidencia clara y reciente, se indica «sin posición clara». Todos los partidos se tratan con el mismo formato y en el mismo orden (escaños del Congreso disuelto). {e(afi["aviso"])}</p></section>

        {faq_block(faq)}
        {related("prog")}
    </main>
    {footer()}
    <script>{COMP_JS}</script>
</body>
</html>
"""
    out = ROOT / "programas-electorales" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(h + "\n" + body, encoding="utf-8")


if __name__ == "__main__":
    build_a_quien_votar()
    build_programas()
    print(f"OK · {n_stm} afirmaciones · {n_temas} temas · {len(partidos)} partidos · {modified_txt}")
