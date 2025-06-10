# La LlorerA

Este proyecto extrae eventos tecnológicos de varias fuentes (Eventbrite, Meetup, GDG Madrid, OpenExpo, Codemotion y Hackathon.com), los clasifica con OpenAI y genera descripciones humorísticas.

Al ejecutarlo se guardan los resultados en `eventos.csv`.

## Puesta en marcha

1. Crea un entorno virtual y activa:
   ```bash
   python3 -m venv lloreria_env
   source lloreria_env/bin/activate
   ```
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Copia el archivo `.env.example` a `.env` e indica tus claves `OPENAI_API_KEY` y `ADMIN_KEY`.

Con todo listo ejecuta:
```bash
python scraper.py
```
Se pedirá la clave de administrador y tras completarse obtendrás `eventos.csv`.

## Automatización semanal

Puedes programar la ejecución automática del scraper cada semana de varias maneras.

### Cron
Si ejecutas el proyecto en un servidor Linux puedes añadir la siguiente entrada de cron para lanzarlo los lunes a las 10:00:
```bash
0 10 * * MON /home/usuario/lloreria_env/bin/python /ruta/scraper.py
```

### GitHub Actions
Otra opción es usar GitHub Actions. Configura los secretos `OPENAI_API_KEY` y `ADMIN_KEY` y utiliza el flujo de trabajo incluido en `.github/workflows/weekly.yml`. Ejecutará el scraper todos los lunes a las 10:00.

## Exportación para redes

Tras ejecutar el scraper y generar `eventos.csv` puedes crear un resumen corto para TikTok o Instagram:
```bash
python exportar_redes.py
```
Se generará un archivo `redes.txt` con tres eventos y su *copy* listo para compartir en tus redes.

## Pendiente por implementar

- Añadir más fuentes de eventos.
- Guardar los resultados en una base de datos en lugar de CSV.
- Incluir pruebas automáticas para garantizar el correcto funcionamiento.
- Mejorar la exportación de contenido para redes sociales.
