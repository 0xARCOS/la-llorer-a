# La LlorerA

Este proyecto extrae eventos tecnológicos de varias fuentes (Eventbrite, Meetup, GDG Madrid, OpenExpo, Codemotion y Hackathon.com), los clasifica con OpenAI y genera descripciones humorísticas. Al ejecutarlo se guardan los resultados en `eventos.csv`.

```
python scraper.py
```

## Automatización semanal

Puedes programar la ejecución automática del scraper cada semana de varias maneras.

### Cron
Si ejecutas el proyecto en un servidor Linux puedes añadir la siguiente entrada de cron para lanzarlo los lunes a las 10:00:

```
0 10 * * MON /home/usuario/lloreria_env/bin/python /ruta/scraper.py
```

### GitHub Actions
Otra opción es usar GitHub Actions. Configura los secretos `OPENAI_API_KEY` y `ADMIN_KEY` y utiliza el flujo de trabajo incluido en `.github/workflows/weekly.yml`. Ejecutará el scraper todos los lunes a las 10:00.
