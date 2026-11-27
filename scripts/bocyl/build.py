#!/usr/bin/env python3
"""BOCYL -> bocyl-salamanca/data.json

Descarga el sumario de cada boletin del BOCYL, baja el texto de cada disposicion,
filtra lo que afecta a Salamanca, lo clasifica y lo fusiona con data.json
(idempotente: volver a ejecutarlo sobre un dia ya procesado no duplica nada).
Los resumenes en lenguaje llano viven en resumenes.json (id -> texto).

Si hay GEMINI_API_KEY, redacta con Gemini el resumen en lenguaje llano de las
disposiciones nuevas que aun no lo tienen (sin clave, o si falla, quedan sin
resumen y se reintenta en la siguiente ejecucion). GEMINI_MODEL es opcional.

Uso:
  python scripts/bocyl/build.py                      # ultimos 7 dias
  python scripts/bocyl/build.py --desde 28/10/2026 --hasta 27/11/2026
  python scripts/bocyl/build.py --cache ruta/r30.json   # reutiliza textos ya bajados
"""
import argparse, datetime, html, json, os, re, sys, time, urllib.error, urllib.request
from concurrent.futures import ThreadPoolExecutor

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA = os.path.join(RAIZ, 'bocyl-salamanca', 'data.json')
RESUM = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resumenes.json')
H = {'User-Agent': 'Mozilla/5.0'}
MODELO = os.environ.get('GEMINI_MODEL') or 'gemini-2.5-flash'
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


SISTEMA = (
    "Eres el redactor de un panel ciudadano que explica el Boletin Oficial de Castilla y Leon en lenguaje llano. "
    "Para cada disposicion escribes un resumen de 2 o 3 frases en espanol de Espana, claro para alguien sin "
    "conocimientos juridicos: que se decide, a quien afecta, el resultado (favorable, desfavorable, aprobado, "
    "convocado...) y, si existe, el plazo o el importe. Solo cuentas lo que esta en el texto: no inventas datos, "
    "cifras ni fechas. No incluyas nombres de personas fisicas, DNI ni datos personales: di 'una persona', "
    "'un nuevo propietario', etc. Si la norma afecta a toda Castilla y Leon y no solo a Salamanca, dilo. "
    "Devuelves unicamente JSON valido."
)
ESQUEMA = {'type': 'OBJECT', 'required': ['resumenes'], 'properties': {'resumenes': {'type': 'ARRAY', 'items': {
    'type': 'OBJECT', 'required': ['id', 'resumen'],
    'properties': {'id': {'type': 'STRING'}, 'resumen': {'type': 'STRING'}}}}}}


def gemini(prompt):
    clave = os.environ.get('GEMINI_API_KEY')
    url = f'https://generativelanguage.googleapis.com/v1beta/models/{MODELO}:generateContent'
    config = {'responseMimeType': 'application/json', 'responseSchema': ESQUEMA, 'temperature': 0.2}
    if '2.5' in MODELO:
        config['thinkingConfig'] = {'thinkingBudget': 0}
    cuerpo = json.dumps({'systemInstruction': {'parts': [{'text': SISTEMA}]},
                         'contents': [{'role': 'user', 'parts': [{'text': prompt}]}],
                         'generationConfig': config}).encode('utf-8')
    for intento in range(4):
        req = urllib.request.Request(url, data=cuerpo, method='POST',
                                     headers={'Content-Type': 'application/json', 'x-goog-api-key': clave})
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                datos = json.loads(r.read().decode('utf-8'))
            cand = (datos.get('candidates') or [{}])[0]
            texto = ''.join(p.get('text', '') for p in (cand.get('content') or {}).get('parts') or [])
            return json.loads(texto)['resumenes']
        except urllib.error.HTTPError as e:
            print('[gemini] HTTP', e.code, e.read().decode('utf-8', errors='replace')[:200])
            if e.code not in (429, 500, 502, 503, 504):
                break
        except (urllib.error.URLError, TimeoutError, ValueError, KeyError) as e:
            print('[gemini] fallo:', e)
        time.sleep(5 * 2 ** intento)
    return []


def extracto(titulo, cuerpo):
    i = cuerpo.find(titulo[:60])
    t = cuerpo[i + len(titulo):] if i >= 0 else cuerpo
    return t if len(t) <= 6000 else t[:3500] + ' [...] ' + t[-2500:]


def resumir(items, cuerpos, resum):
    """Anade a `resum` el resumen de las disposiciones relevantes que aun no lo tienen. Devuelve cuantas."""
    if not os.environ.get('GEMINI_API_KEY'):
        return 0
    pend = [i for i in items if i['alcance'] in ('provincia', 'comunidad') and i['id'] not in resum and i['id'] in cuerpos]
    hechos = 0
    for k in range(0, len(pend), 6):
        lote = pend[k:k + 6]
        bloques = [f"ID: {i['id']}\nTITULO: {i['titulo']}\nTEXTO: {extracto(i['titulo'], cuerpos[i['id']])}" for i in lote]
        prompt = 'Resume cada disposicion. Devuelve un objeto por id.\n\n' + '\n\n'.join(bloques)
        validos = {i['id'] for i in lote}
        for r in gemini(prompt):
            txt = (r.get('resumen') or '').strip()
            if r.get('id') in validos and 40 <= len(txt) <= 700:
                resum[r['id']] = txt
                hechos += 1
    return hechos


def salida(valores):
    ruta = os.environ.get('GITHUB_OUTPUT')
    if ruta:
        with open(ruta, 'a', encoding='utf-8') as fh:
            for k, v in valores.items():
                fh.write(f'{k}={v}\n')


def clave_fecha(f):
    return f.split('/')[::-1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--desde')
    ap.add_argument('--hasta')
    ap.add_argument('--cache')
    a = ap.parse_args()
    fin = datetime.datetime.strptime(a.hasta, '%d/%m/%Y').date() if a.hasta else datetime.date.today()
    ini = datetime.datetime.strptime(a.desde, '%d/%m/%Y').date() if a.desde else fin - datetime.timedelta(days=6)
    fechas = [(ini + datetime.timedelta(days=i)).strftime('%d/%m/%Y') for i in range((fin - ini).days + 1)]

    datos = json.load(open(DATA, encoding='utf-8')) if os.path.exists(DATA) else {'dias': {}, 'items': []}
    resum = json.load(open(RESUM, encoding='utf-8')) if os.path.exists(RESUM) else {}
    cache = {}
    if a.cache:
        for x in json.load(open(a.cache, encoding='utf-8')):
            cache.setdefault(x['fecha'], []).append(x)

    cuerpos = {}
    for f in fechas:
        if f in cache:
            its = [x for x in cache[f] if not re.match(r'(Sumario|Anterior)', x['titulo'])]
        else:
            its = dia(f)
        if not its:
            print(f, 'sin boletin (o no disponible)')
            continue
        cuerpos.update({x['id']: x['cuerpo'] for x in its})
        rel = procesar(its)
        datos['items'] = [i for i in datos['items'] if i['fecha'] != f] + rel
        datos['dias'][f] = {'total': len(its), 'salamanca': sum(1 for r in rel if r['alcance'] == 'provincia'),
                            'boletin': its[0].get('boletin') if its else None}
        print(f, len(its), 'disposiciones,', len(rel), 'relevantes')

    nuevos = resumir(datos['items'], cuerpos, resum)
    if nuevos:
        json.dump(dict(sorted(resum.items())), open(RESUM, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
        print(nuevos, 'resumenes nuevos')
    for i in datos['items']:
        i['resumen'] = resum.get(i['id'])
    datos['items'].sort(key=lambda i: (clave_fecha(i['fecha']), i['id']), reverse=True)
    datos['dias'] = dict(sorted(datos['dias'].items(), key=lambda kv: clave_fecha(kv[0])))
    datos['actualizado'] = max(datos['dias'], key=clave_fecha) if datos['dias'] else None
    datos['categorias'] = {**{k: e for k, e, _ in CATEGORIAS}, 'otros': 'Otros'}
    os.makedirs(os.path.dirname(DATA), exist_ok=True)
    json.dump(datos, open(DATA, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('guardado', DATA, len(datos['items']), 'items')
    salida({'periodo': datos['actualizado'] or ''})


if __name__ == '__main__':
    main()
