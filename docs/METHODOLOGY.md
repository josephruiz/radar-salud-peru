# Política de fuentes, territorio y calidad
## Finalidad
Archivo público de seguimiento sanitario informativo del Perú a cinco años; NO sustituye la vigilancia epidemiológica oficial ni representa a las autoridades.
## Estados
- `unreviewed`: metadatos descubiertos automáticamente, sin validación del contenido.
- `verified`: una persona revisó fuente, fecha y contenido relevante.
- `rejected`: duplicado, incorrecto o irrelevante.
- `failed`: el recolector no terminó; **no** significa que hubo cero eventos.
- `partial`: una o más fuentes fallaron; cobertura incompleta.
## Territorio
25 ámbitos (24 departamentos + Callao). Una mención en el título no confirma lugar del evento. Para el futuro integrar catálogo UBIGEO INEI, provincia y distrito; distinguir Lima Metropolitana y Lima Provincias al contar con datos fiables.
## Fenómeno El Niño
Incorporar fuentes primarias SENAMHI, ENFEN, INDECI, CDC Perú, MINSA y autoridades regionales. Nunca afirmar impactos epidemiológicos causales usando solamente titulares; separar escenarios, pronósticos, alertas y observaciones.
## Normativa
El Peruano ofrece búsqueda dinámica. El prototipo actual únicamente explora metadatos HTML visibles. No afirmar exhaustividad, vigencia, derogación ni efectos jurídicos sin texto oficial y revisión. No se realiza descarga masiva de PDFs.
## Estadísticas
Los recuentos de noticias son recuentos documentales, no tasas de enfermedad. Indicadores de salud requieren una fuente oficial, unidad, población/denominador, periodo y metodología. Registrar versiones, licencias y citas.
## Retención
GitHub retiene exportaciones JSON por fecha; Supabase es el futuro motor de consulta. Configurar respaldos externos y supervisar límites antes de cinco años. Nunca incluir secretos en git, frontend o archivos JSON.
