-- Atalaya · modelo de datos (SQLite hoy, PostgreSQL + PostGIS + pgvector en producción).
-- Principios: 1) el territorio (código INE) es la clave de todo; 2) cada dato lleva fuente, fecha de captura
-- y fecha del hecho; 3) nunca se sobrescribe: se añade (histórico completo); 4) separar hecho observado
-- de inferencia (sentimiento, etiquetas) guardando modelo y versión; 5) solo agregados por territorio, sin perfiles personales.

PRAGMA foreign_keys = ON;

-- ───────── Territorio ─────────
CREATE TABLE territorio (
  codigo      TEXT PRIMARY KEY,                 -- INE: 'ES', '37' (provincia), '37274' (municipio)
  nivel       TEXT NOT NULL CHECK (nivel IN ('pais','provincia','municipio','seccion')),
  nombre      TEXT NOT NULL,
  padre       TEXT REFERENCES territorio(codigo),
  poblacion   INTEGER,                          -- se rellena desde INE (Fase 2)
  geom        TEXT                              -- GeoJSON hoy; geometry(MultiPolygon,4326) en PostGIS
);

-- ───────── Fuentes y trazabilidad ─────────
CREATE TABLE fuente (
  id          INTEGER PRIMARY KEY,
  nombre      TEXT NOT NULL,                    -- 'El País', 'Interior', 'CIS', 'Reddit r/spain'
  tipo        TEXT NOT NULL CHECK (tipo IN ('prensa','opinion','oficial','encuesta','red_social','foro','video','documento')),
  url         TEXT,
  fiabilidad  REAL                              -- 0-1, ponderación editable
);

-- ───────── Política ─────────
CREATE TABLE partido (
  id TEXT PRIMARY KEY, nombre TEXT NOT NULL, siglas TEXT, color TEXT, ambito TEXT, ideologia TEXT
);
CREATE TABLE politico (
  id TEXT PRIMARY KEY, nombre TEXT, partido_id TEXT REFERENCES partido(id), cargo TEXT,
  ambito TEXT, territorio TEXT REFERENCES territorio(codigo), estado TEXT,  -- candidato / seguimiento / por_definir
  wikipedia TEXT, alias TEXT                    -- alias en JSON: formas con las que se detecta en texto
);

-- ───────── Elecciones, resultados y encuestas (histórico para volatilidad) ─────────
CREATE TABLE eleccion (
  id TEXT PRIMARY KEY, tipo TEXT, fecha TEXT NOT NULL, ambito TEXT
);
CREATE TABLE resultado (
  eleccion_id TEXT REFERENCES eleccion(id), territorio TEXT REFERENCES territorio(codigo),
  partido_id TEXT REFERENCES partido(id), votos INTEGER, porcentaje REAL, escanos INTEGER,
  censo INTEGER, votantes INTEGER, fuente_id INTEGER REFERENCES fuente(id),
  PRIMARY KEY (eleccion_id, territorio, partido_id)
);
CREATE TABLE encuesta (
  id INTEGER PRIMARY KEY, fecha TEXT NOT NULL, empresa TEXT, medio TEXT, muestra INTEGER,
  tipo TEXT, territorio TEXT REFERENCES territorio(codigo) DEFAULT 'ES', fuente_id INTEGER REFERENCES fuente(id)
);
CREATE TABLE encuesta_voto (
  encuesta_id INTEGER REFERENCES encuesta(id), partido_id TEXT, porcentaje REAL,
  PRIMARY KEY (encuesta_id, partido_id)
);

-- ───────── Contenido: prensa, opinión, redes, foros, vídeos ─────────
CREATE TABLE articulo (
  id INTEGER PRIMARY KEY, url TEXT UNIQUE NOT NULL, titulo TEXT NOT NULL, medio TEXT, fuente_id INTEGER REFERENCES fuente(id),
  ambito TEXT CHECK (ambito IN ('nacional','local','internacional')), tipo TEXT DEFAULT 'noticia',  -- noticia | opinion | tuit | foro | video
  publicado TEXT NOT NULL, capturado TEXT NOT NULL, texto TEXT                          -- 'texto' completo se guarda en Fase 2
);
CREATE TABLE articulo_territorio (articulo_id INTEGER REFERENCES articulo(id), territorio TEXT REFERENCES territorio(codigo),
  metodo TEXT, confianza REAL, PRIMARY KEY (articulo_id, territorio));
CREATE TABLE articulo_politico (articulo_id INTEGER REFERENCES articulo(id), politico_id TEXT REFERENCES politico(id),
  PRIMARY KEY (articulo_id, politico_id));
CREATE TABLE articulo_partido (articulo_id INTEGER REFERENCES articulo(id), partido_id TEXT, PRIMARY KEY (articulo_id, partido_id));

-- Inferencias del NLP: separadas del dato, con modelo y versión para poder recalcular
CREATE TABLE analisis (
  articulo_id INTEGER REFERENCES articulo(id), modelo TEXT NOT NULL, version TEXT NOT NULL, creado TEXT NOT NULL,
  sentimiento REAL,            -- -1..1 hacia la entidad principal
  tema TEXT, es_evento_riesgo INTEGER, severidad INTEGER,
  PRIMARY KEY (articulo_id, modelo, version)
);

-- ───────── Eventos / peligros ─────────
CREATE TABLE evento (
  id INTEGER PRIMARY KEY, fecha TEXT NOT NULL, tipo TEXT,   -- detencion, imputacion, accidente, dimision, escandalo…
  titulo TEXT, territorio TEXT REFERENCES territorio(codigo), politico_id TEXT REFERENCES politico(id),
  partido_id TEXT, severidad INTEGER, estado TEXT DEFAULT 'abierto'
);
CREATE TABLE evento_articulo (evento_id INTEGER REFERENCES evento(id), articulo_id INTEGER REFERENCES articulo(id), PRIMARY KEY (evento_id, articulo_id));

-- ───────── Segundo cerebro: programas, propuestas, declaraciones ─────────
CREATE TABLE documento (
  id INTEGER PRIMARY KEY, tipo TEXT,                         -- programa, nota_prensa, entrevista, discurso, votacion
  partido_id TEXT REFERENCES partido(id), politico_id TEXT REFERENCES politico(id), fecha TEXT NOT NULL,
  url TEXT, titulo TEXT, texto TEXT
);
CREATE TABLE propuesta (
  id INTEGER PRIMARY KEY, documento_id INTEGER REFERENCES documento(id), partido_id TEXT REFERENCES partido(id),
  tema TEXT, area TEXT CHECK (area IN ('economica','politica','social','otra')), enunciado TEXT NOT NULL,
  cita TEXT, fecha TEXT NOT NULL, pagina INTEGER           -- «quién dijo qué y cuándo»
);
-- En PostgreSQL: CREATE TABLE fragmento (documento_id, texto, embedding vector(1024)) para búsqueda semántica (RAG).

-- ───────── Escenarios (reproducibles y comparables) ─────────
CREATE TABLE escenario (
  id INTEGER PRIMARY KEY, creado TEXT NOT NULL, autor TEXT, nombre TEXT, tipo TEXT, partido_id TEXT,
  efecto INTEGER, gravedad REAL, alcance REAL, fidelidad REAL, recuperacion REAL, indecisos REAL,
  modelo_version TEXT NOT NULL, ambito TEXT REFERENCES territorio(codigo)
);
CREATE TABLE escenario_resultado (
  escenario_id INTEGER REFERENCES escenario(id), territorio TEXT REFERENCES territorio(codigo),
  partido_id TEXT, cuota_antes REAL, cuota_despues REAL, indecisos_antes REAL, indecisos_despues REAL, cambia_ganador INTEGER,
  PRIMARY KEY (escenario_id, territorio, partido_id)
);

-- ───────── Índices de lectura frecuente ─────────
CREATE INDEX ix_art_fecha ON articulo(publicado);
CREATE INDEX ix_art_terr ON articulo_territorio(territorio);
CREATE INDEX ix_res_terr ON resultado(territorio, eleccion_id);
CREATE INDEX ix_evento_terr ON evento(territorio, fecha);
