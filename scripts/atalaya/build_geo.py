#!/usr/bin/env python3
"""Atalaya: descarga y simplifica límites (Opendatasoft georef-spain, IGN).
Salida: atalaya/data/provincias.geojson, atalaya/data/prov/NN.geojson, atalaya/data/indice.json
Uso (raíz del repo): python3 scripts/atalaya/build_geo.py
"""
import json, urllib.request, urllib.parse, time
from pathlib import Path
RAIZ = Path(__file__).resolve().parents[2]; OUT = RAIZ / "atalaya/data"
API = "https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/%s/exports/geojson?"

def fetch(ds, where, select):
    q = urllib.parse.urlencode({"where": where, "select": select, "limit": -1})
    for i in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(API % ds + q, headers={"User-Agent": "EmirodgarBot/1.0"}), timeout=180) as r:
                return json.load(r)["features"]
        except Exception as e: print("reintento", e); time.sleep(3)
    raise SystemExit("fallo " + ds)

def dp(pts, eps):
    if len(pts) < 3: return pts
    a, b = pts[0], pts[-1]; dx, dy = b[0]-a[0], b[1]-a[1]; n = (dx*dx+dy*dy)**.5
    m = i = 0
    for k in range(1, len(pts)-1):
        d = abs(dy*pts[k][0]-dx*pts[k][1]+b[0]*a[1]-b[1]*a[0])/n if n > 1e-11 else ((pts[k][0]-a[0])**2+(pts[k][1]-a[1])**2)**.5
        if d > m: m, i = d, k
    return dp(pts[:i+1], eps)[:-1] + dp(pts[i:], eps) if m > eps else [a, b]

def simp(g, eps, dec):
    polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
    out = []
    for poly in polys:
        rs = []
        for r in poly:
            s = [[round(x, dec), round(y, dec)] for x, y in dp(r, eps)]
            if len(s) >= 4: rs.append(s)
        if rs and len(poly[0]) >= 4 and rs[0] is not None and len(dp(poly[0], eps)) >= 4: out.append(rs)
    return {"type": "MultiPolygon", "coordinates": out} if out else None

def s1(v): return v[0] if isinstance(v, list) else v

def main():
    (OUT/"prov").mkdir(parents=True, exist_ok=True)
    provs = []
    for f in fetch("georef-spain-provincia", "prov_code is not null", "prov_code,prov_name,geo_shape"):
        g = simp(f["geometry"], 0.006, 3)
        if g: provs.append({"type": "Feature", "properties": {"c": str(s1(f["properties"]["prov_code"])), "n": s1(f["properties"]["prov_name"])}, "geometry": g})
    provs.sort(key=lambda f: f["properties"]["c"])
    (OUT/"provincias.geojson").write_text(json.dumps({"type": "FeatureCollection", "features": provs}, separators=(",", ":"), ensure_ascii=False), encoding="utf8")
    print(len(provs), "provincias")
    indice = {"prov": {f["properties"]["c"]: f["properties"]["n"] for f in provs}, "mun": []}
    for f in provs:
        pc = f["properties"]["c"]
        feats = []
        for m in fetch("georef-spain-municipio", 'prov_code="%s"' % pc, "mun_code,mun_name,geo_shape"):
            g = simp(m["geometry"], 0.0009, 4)
            if not g: continue
            c = str(s1(m["properties"]["mun_code"])); n = s1(m["properties"]["mun_name"])
            feats.append({"type": "Feature", "properties": {"c": c, "n": n}, "geometry": g})
            indice["mun"].append([c, n])
        (OUT/"prov"/(pc+".geojson")).write_text(json.dumps({"type": "FeatureCollection", "features": feats}, separators=(",", ":"), ensure_ascii=False), encoding="utf8")
        print(pc, f["properties"]["n"], len(feats), flush=True)
    (OUT/"indice.json").write_text(json.dumps(indice, separators=(",", ":"), ensure_ascii=False), encoding="utf8")
main()
