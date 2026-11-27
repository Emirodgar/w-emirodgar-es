#!/usr/bin/env python3
"""BOCYL -> bocyl-salamanca/data.json

Descarga el sumario de cada boletin del BOCYL, baja el texto de cada disposicion,
filtra lo que afecta a Salamanca, lo clasifica y lo fusiona con data.json
(idempotente: volver a ejecutarlo sobre un dia ya procesado no duplica nada).
Los resumenes en lenguaje llano viven en resumenes.json (id -> texto).

Uso:
  python scripts/bocyl/build.py                      # ultimos 3 dias
  python scripts/bocyl/build.py --desde 28/10/2026 --hasta 27/11/2026
  python scripts/bocyl/build.py --cache ruta/r30.json   # reutiliza textos ya bajados
"""
import argparse, datetime, html, json, os, re, time, urllib.request
from concurrent.futures import ThreadPoolExecutor

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA = os.path.join(RAIZ, 'bocyl-salamanca', 'data.json')
RESUM = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resumenes.json')
H = {'User-Agent': 'Mozilla/5.0'}
PROVS = ['Ávila', 'Burgos', 'León', 'Palencia', 'Segovia', 'Soria', 'Valladolid', 'Zamora']

CATEGORIAS = [  # (clave, etiqueta, regex sobre el titulo) - el orden importa
    ('subastas', 'Subastas', r'subasta'),
    ('impuestos', 'Impuestos y tasas', r'impuesto|\btasas?\b(?! de reposici)|tributo|precio público|ordenanza fiscal'),
    ('sanciones', 'Sanciones', r'sanci|denuncia|infracci'),
    ('laboral', 'Laboral', r'servicios mínimos|huelga|convenio colectivo|organización sindical'),
    ('empleo', 'Empleo y oposiciones', r'oposici|convocatoria|bolsa|proceso selectivo|libre designaci|admitidos|nombra|\bcese|concurso|plazas|tribunal|catedr'),
    ('ambiente', 'Medio ambiente', r'ambiental|impacto|explotaci|monte|forestal|vía pecuaria|\bcoto|caza|pesca|residuos'),
    ('urbanismo', 'Urbanismo', r'urban|plan general|plan parcial|suelo|estudio de detalle|junta de compensaci|licencia'),
    ('ayudas', 'Ayudas y subvenciones', r'subvenci|ayuda|beneficiarios|becas|premio'),
]


def get(u):
    for _ in range(3):
        try:
            r = urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=40).read()
            try:
                return r.decode('utf-8')
            except UnicodeDecodeError:
                return r.decode('latin-1')
        except Exception:
            time.sleep(1)
    return None


def limpio(t):
    t = re.sub(r'<script.*?</script>|<style.*?</style>', '', t, flags=re.S)
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', t))).strip()


def parsear_sumario(t):
    t = re.sub(r'<!--.*?-->', '', t, flags=re.S)
    items = []
    for m in re.finditer(r'<p[^>]*>((?:(?!<p[\s>]).)*?)</p>\s*<ul class="descargaBoletin">(.*?)</ul>', t, flags=re.S):
        idm = re.search(r'(BOCYL-[A-Z]-\d+-\d+-\d+)\.do', m.group(2))
        titulo = re.sub(r'\s+', ' ', limpio(m.group(1)))
        if idm and not re.match(r'(Sumario|Anterior)', titulo):
            items.append({'id': idm.group(1), 'titulo': titulo})
    return items


def num_boletin(t):
    m = re.search(r'<title>[^<]*?(\d+)/(\d{4})', t)
    return f'{m.group(1)}/{m.group(2)}' if m else None


def categoria(titulo):
    for k, _, rx in CATEGORIAS:
        if re.search(rx, titulo, re.I):
            return k
    return 'otros'


def alcance(titulo, cuerpo):
    """provincia | comunidad | mencion | None (ruido: no afecta a Salamanca)"""
    if re.search(r'\bSalamanca\b', titulo):
        return 'provincia'
    if re.match(r'(LEY|DECRETO-LEY|DECRETO)\s+\d+/\d{4}', titulo):
        return 'comunidad'
    n_sal = len(re.findall(r'\bSalamanca\b', cuerpo))
    if not n_sal:
        return None
    if sum(1 for p in PROVS if re.search(r'\b' + p + r'\b', cuerpo)) >= 4:
        return 'comunidad'
    callejero = len(re.findall(r'(?:Avenida|Avda\.?|Camino|Calle|Carretera|oleoducto|gasoducto|Bilbao-)\s*(?:de\s+)?[^.,;]{0,12}Salamanca', cuerpo))
    return None if callejero >= n_sal else 'mencion'


def dia(fecha):
    d, m, y = fecha.split('/')
    # el servidor a veces devuelve el sumario cortado: se reintenta hasta que el
    # numero de disposiciones parseadas coincida con el de bloques de descarga
    for _ in range(4):
        t = get(f'https://bocyl.jcyl.es/boletin.do?fechaBoletin={fecha}')
        if not t or 'NO ENCONTRADO' in t:
            return None
        parsed = parsear_sumario(t)
        if '</html>' in t and len(parsed) == len(re.findall(r'class="descargaBoletin"', re.sub(r'<!--.*?-->', '', t, flags=re.S))):
            break
        time.sleep(2)
    its = []
    for x in parsed:
        x['fecha'] = fecha
        x['boletin'] = num_boletin(t)
        x['url'] = f'https://bocyl.jcyl.es/html/{y}/{m}/{d}/html/{x["id"]}.do'
        its.append(x)
    with ThreadPoolExecutor(4) as ex:
        for x, b in zip(its, ex.map(lambda x: get(x['url']) or '', its)):
            x['cuerpo'] = limpio(b)
    return its


def procesar(items):
    out = []
    for x in items:
        a = alcance(x['titulo'], x.get('cuerpo', ''))
        if not a:
            continue
        out.append({'id': x['id'], 'fecha': x['fecha'], 'boletin': x.get('boletin'), 'titulo': x['titulo'],
                    'url': x['url'], 'categoria': categoria(x['titulo']), 'alcance': a, 'resumen': None})
    return out


def clave_fecha(f):
    return f.split('/')[::-1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--desde')
    ap.add_argument('--hasta')
    ap.add_argument('--cache')
    a = ap.parse_args()
    fin = datetime.datetime.strptime(a.hasta, '%d/%m/%Y').date() if a.hasta else datetime.date.today()
    ini = datetime.datetime.strptime(a.desde, '%d/%m/%Y').date() if a.desde else fin - datetime.timedelta(days=2)
    fechas = [(ini + datetime.timedelta(days=i)).strftime('%d/%m/%Y') for i in range((fin - ini).days + 1)]

    datos = json.load(open(DATA, encoding='utf-8')) if os.path.exists(DATA) else {'dias': {}, 'items': []}
    resum = json.load(open(RESUM, encoding='utf-8')) if os.path.exists(RESUM) else {}
    cache = {}
    if a.cache:
        for x in json.load(open(a.cache, encoding='utf-8')):
            cache.setdefault(x['fecha'], []).append(x)

    for f in fechas:
        if f in cache:
            its = [x for x in cache[f] if not re.match(r'(Sumario|Anterior)', x['titulo'])]
        else:
            its = dia(f)
        if not its:
            datos['dias'].pop(f, None)
            print(f, 'sin boletin')
            continue
        rel = procesar(its)
        datos['items'] = [i for i in datos['items'] if i['fecha'] != f] + rel
        datos['dias'][f] = {'total': len(its), 'salamanca': sum(1 for r in rel if r['alcance'] == 'provincia'),
                            'boletin': its[0].get('boletin') if its else None}
        print(f, len(its), 'disposiciones,', len(rel), 'relevantes')

    for i in datos['items']:
        i['resumen'] = resum.get(i['id'])
    datos['items'].sort(key=lambda i: (clave_fecha(i['fecha']), i['id']), reverse=True)
    datos['dias'] = dict(sorted(datos['dias'].items(), key=lambda kv: clave_fecha(kv[0])))
    datos['actualizado'] = max(datos['dias'], key=clave_fecha) if datos['dias'] else None
    datos['categorias'] = {**{k: e for k, e, _ in CATEGORIAS}, 'otros': 'Otros'}
    os.makedirs(os.path.dirname(DATA), exist_ok=True)
    json.dump(datos, open(DATA, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('guardado', DATA, len(datos['items']), 'items')


if __name__ == '__main__':
    main()
