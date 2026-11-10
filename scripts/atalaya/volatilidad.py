"""Atalaya: cálculo de volatilidad territorial (provincias y ciudades) para las fichas «¿qué provincias pueden cambiar de partido?».

Tres señales, todas con datos reales del repositorio:
  1. HISTÓRICO: escaños por provincia en las 16 elecciones generales desde 1977 (atalaya/data/escanos.json):
     alternancias del partido con más escaños, empates en cabeza y partidos distintos que han liderado.
  2. 2023: votos oficiales por provincia y por municipio (Interior): margen entre el primero y el segundo.
  3. SONDEOS: proyección de cambio proporcional uniforme (la misma de ficha_nacional.py) con la media de los sondeos de los últimos
     30 días y con cada sondeo por separado, para ver cuántos escenarios hacen cambiar al partido más votado.

«Cambiar de partido» = que el partido más votado (por votos) sea distinto al de julio de 2023. Es una proyección orientativa:
supone que el cambio nacional es igual en todas partes. No hay encuestas provinciales.
"""
import glob, re
from datetime import datetime

import ficha_nacional as fn

NOM = {"VOX": "Vox", "SUMAR": "Sumar", "JxCAT - JUNTS": "Junts", "EAJ-PNV": "PNV", "EH Bildu": "EH Bildu", "B.N.G.": "BNG", "CCa": "CC", "U.P.N.": "UPN",
       "ERC": "ERC", "CUP-PR": "CUP", "CpM": "Coalición por Melilla", "NC-bc": "NC", "EXISTE": "Teruel Existe", "SY": "Soria ¡YA!", "U.P.L.": "UPL"}
nom = lambda k: NOM.get(k, k)
UMBRAL_AIRE, UMBRAL_CORTA = 3.0, 6.0   # puntos de margen proyectado


def _ratios(sondeo, base):
    return {k: sondeo[k] / base[k] for k in fn.CUATRO}


def _lider(votos, blanco, r):
    nv = {n: v * r.get(n, 1.0) for n, v in votos.items()}
    o = sorted(nv.items(), key=lambda kv: -kv[1]); tt = sum(nv.values()) + blanco
    return o[0][0], o[1][0], 100 * (o[0][1] - o[1][1]) / tt


def escanos_prov(p, r):
    """D'Hondt con barrera del 3 % en una provincia, tras aplicar el cambio proporcional r. Devuelve {lista: escaños}."""
    nv = {n: v[0] * r.get(n, 1.0) for n, v in p["v"].items()}
    tv = sum(nv.values()) + p["blanco"]
    n = sum(s for _, s in p["v"].values())
    el = {k: v for k, v in nv.items() if v >= 0.03 * tv and v > 0}
    return fn.dhondt(el, n), el, n


def ultimo_escano(p, r):
    """Margen del último escaño: qué lista lo gana, cuál es la siguiente y cuántos votos le faltaron a la siguiente para quitárselo."""
    sc, el, n = escanos_prov(p, r)
    q = sorted(((v / d, k, d) for k, v in el.items() for d in range(1, n + 2)), reverse=True)
    ganador = q[n - 1]; perdedor = q[n]
    # votos que necesitaba la lista que se queda fuera para igualar el cociente de la que se llevó el último escaño
    falta = ganador[0] * perdedor[2] - el[perdedor[1]]
    return dict(gana=ganador[1], pierde=perdedor[1], falta=max(falta, 0), pct=100 * max(falta, 0) / (sum(el.values()) + p["blanco"]))


def historico(esc, ind):
    """Por provincia: alternancias, empates en cabeza, partidos líderes y la secuencia de líderes por elección."""
    out = {}
    for pc, v in esc.items():
        P = v["partidos"]; N = len(v["elecciones"]); lead = []
        for i in range(N):
            s = sorted(((P[p][i], p) for p in P), reverse=True)
            lead.append(None if (len(s) > 1 and s[0][0] == s[1][0]) or s[0][0] == 0 else s[0][1])
        det = [(i, l) for i, l in enumerate(lead) if l]
        alt = sum(1 for a, b in zip(det, det[1:]) if a[1] != b[1])
        alt8 = sum(1 for a, b in zip(det, det[1:]) if a[1] != b[1] and a[0] >= N - 8)
        out[pc] = dict(alt=alt, alt8=alt8, empates=sum(1 for l in lead if l is None), partidos=sorted({l for l in lead if l}), seq=lead, elecciones=v["elecciones"],
                       ultimo=lead[-1], total=N)
    return out


def calcular(c):
    J, D, RAIZ = c["J"], c["D"], c["RAIZ"]
    prov = J(D / "resultados/congreso-2023-07/circunscripciones.json")["prov"]
    esc = J(D / "escanos.json"); ind = J(D / "indice.json")["prov"]
    enc = J(RAIZ / "elecciones-espana/data/2026-11-29/encuestas.json")
    sond = [x for x in enc["sondeos"] if not re.search("cis", x["empresa"], re.I)]
    ref = datetime.fromisoformat(sond[0]["fecha"])
    rec = [x for x in sond if (ref - datetime.fromisoformat(x["fecha"])).days <= 30]
    comp = [x for x in rec if all(k in x["voto"] for k in fn.CUATRO)]
    med = fn.media(sond, ref)
    tot = sum(p["validos"] for p in prov.values())
    base = {k: sum(p["v"].get(k, [0])[0] for p in prov.values()) / tot * 100 for k in fn.CUATRO}
    r_med = _ratios(med, base); r_pol = [_ratios(x["voto"], base) for x in comp]
    hist = historico(esc, ind)

    P = {}
    for pc, p in prov.items():
        votos = {n: v[0] for n, v in p["v"].items()}
        l23, s23, m23 = _lider(votos, p["blanco"], {})
        lm, sm, mm = _lider(votos, p["blanco"], r_med)
        polls = [_lider(votos, p["blanco"], r) for r in r_pol]
        flips = sum(1 for l, _, _ in polls if l != l23)
        margenes = [(m if l == l23 else -m) for l, _, m in polls]   # margen respecto al líder de 2023 (negativo = vuelco)
        seats23 = {n: v[1] for n, v in p["v"].items() if v[1]}
        sc_m = escanos_prov(p, r_med)[0]
        sc_pol = [escanos_prov(p, r)[0] for r in r_pol]
        listas = set(seats23) | set(sc_m) | {k for s in sc_pol for k in s}
        esc_rango = {k: (min(s.get(k, 0) for s in sc_pol), max(s.get(k, 0) for s in sc_pol)) for k in listas}
        hp = hist[pc]
        if lm != l23: cat = "cambio"
        elif mm < UMBRAL_AIRE or flips: cat = "aire"
        elif mm < UMBRAL_CORTA: cat = "corta"
        else: cat = "estable"
        P[pc] = dict(pc=pc, n=p["n"], escanos=sum(seats23.values()), censo=p["censo"], l23=l23, s23=s23, m23=m23, lm=lm, sm=sm, mm=mm, flips=flips, npol=len(polls),
                     marg_min=min(margenes) if margenes else mm, marg_max=max(margenes) if margenes else mm, seats23=seats23, seats_med={k: v for k, v in sc_m.items() if v},
                     seats_rango={k: v for k, v in esc_rango.items() if v[1]}, hist=hp, cat=cat, ult23=ultimo_escano(p, {}), ult_med=ultimo_escano(p, r_med))

    # ciudades (≥ 50.000 habitantes) con resultados de las generales de 2023 por municipio
    C = []
    for f in sorted(glob.glob(str(D / "resultados/congreso-2023-07/[0-9][0-9].json"))):
        d = J(__import__("pathlib").Path(f))
        pc = f[-7:-5]
        for code, m in d["mun"].items():
            if m["pob"] < 50000: continue
            l23, s23, m23 = _lider(m["v"], m["blanco"], {})
            lm, sm, mm = _lider(m["v"], m["blanco"], r_med)
            polls = [_lider(m["v"], m["blanco"], r)[0] for r in r_pol]
            flips = sum(1 for l in polls if l != l23)
            cat = "cambio" if lm != l23 else ("aire" if mm < UMBRAL_AIRE or flips else ("corta" if mm < UMBRAL_CORTA else "estable"))
            C.append(dict(code=code, pc=pc, n=m["n"], pob=m["pob"], l23=l23, s23=s23, m23=m23, lm=lm, mm=mm, flips=flips, npol=len(polls), cat=cat))
    t23 = {}
    for p in prov.values():
        for n, v in p["v"].items(): t23[n] = t23.get(n, 0) + v[1]
    t_med = fn.proyectar(prov, med); t_pol = [fn.proyectar(prov, x["voto"]) for x in comp]
    tot_rango = {k: (min(t.get(k, 0) for t in t_pol), max(t.get(k, 0) for t in t_pol)) for k in fn.CUATRO}
    return dict(P=P, C=C, med=med, base=base, nsond=len(rec), ncomp=len(comp), fsond=sond[0]["fecha"], r_med=r_med, t23=t23, t_med=t_med, t_rango=tot_rango)
