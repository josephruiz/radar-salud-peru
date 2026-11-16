# Radar Salud Perú · Observatorio sanitario 2026–2031

Plataforma pública para consultar información sanitaria por día, palabra clave, tema y territorio. Repositorio **independiente** de Radar IA Salud y de otros proyectos.

## Ver la web
Abra `index.html` con un servidor estático o active **GitHub Pages** desde Settings → Pages → Deploy from a branch → `main` → `/(root)`. La web podrá consultarse en `https://josephruiz.github.io/radar-salud-peru/` una vez que Pages esté habilitado y publicado.

## Estructura
- `index.html`, `styles.css`, `app.js`: frontend responsive, calendario, buscador por fecha y por índice histórico (hasta 8 000 registros recientes), filtros y archivos.
- `data/YYYY/MM/DD/edition.json`: edición de cada día (no se consolida en una única página).
- `data/index.json`: índice para navegar días archivados.
- `collector/daily.py`: primera captura RSS de noticias con 25 búsquedas regionales.
- `collector/el_peruano.py`: prototipo conservador de metadatos de normas, **no exhaustivo**.
- `sql/001_initial.sql`: esquema PostgreSQL para un proyecto **nuevo** de Supabase, todavía no conectado.
- `.github/workflows/daily.yml`: tarea diaria a las 07:15, hora de Perú.
- `docs/METHODOLOGY.md`: criterios para fuentes, El Niño, relevancia y calidad.

## Ejecutar localmente
```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python collector/daily.py
python -m http.server 8000
```
Abra `http://localhost:8000`.

## Limitaciones actuales
La búsqueda entre fechas se realiza con un índice JSON **acotado a 8 000 registros**; para búsquedas integrales durante cinco años habrá que conectar PostgreSQL/Supabase. Las noticias encontradas mediante RSS requieren validación editorial. El recolector de normas de El Peruano no garantiza resultados completos debido a la carga dinámica del portal. Sin configuración GitHub Pages la web no estará públicamente desplegada. La ejecución programada de Actions puede sufrir retrasos o fallos: revisar pestaña Actions. No hay una conexión activa a Supabase ni un modelo de deep learning entrenado.

## Fuentes prioritarias siguientes
MINSA, CDC Perú, INS, DIGEMID, EsSalud, SENAMHI, ENFEN, INDECI, INEI y El Peruano. Usar UBIGEO oficial para indicadores territoriales y distinguir eventos clínicos de noticias.
