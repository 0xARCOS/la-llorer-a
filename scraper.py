# scraper.py
import csv
import requests
from bs4 import BeautifulSoup
import openai
import os
from dotenv import load_dotenv
import getpass

# Carga variables de entorno desde .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")  # Usa la clave desde .env
ADMIN_KEY = os.getenv("ADMIN_KEY")            # Usa la clave desde .env

def verificar_admin():
    clave = getpass.getpass("🔐 Ingresa la clave de administrador: ")
    if clave != ADMIN_KEY:
        print("❌ Clave incorrecta. Acceso denegado.")
        exit()

# Paso 1: Scraping simple de Eventbrite
def obtener_eventos_eventbrite():
    url = 'https://www.eventbrite.es/d/spain--madrid/tecnologia/'
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    eventos = []

    for card in soup.select('div.eds-event-card-content__content'):
        try:
            titulo = card.select_one('div.eds-event-card-content__title').text.strip()
            fecha = card.select_one('div.eds-event-card-content__sub-title').text.strip()
            enlace = card.find_parent('a')['href']
            eventos.append({'titulo': titulo, 'fecha': fecha, 'enlace': enlace})
        except Exception:
            continue

    return eventos

# Paso 2: Clasificación temática
def clasificar_evento(titulo):
    prompt = f"Clasifica este evento tech: '{titulo}' en una de estas categorías: IA, Ciberseguridad, Web, Absurdos, Otro.\nCategoría:"
    res = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=10,
        temperature=0.2
    )
    return res.choices[0].text.strip()

# Paso 3: Descripción estilo ‘La Llorería’
def generar_resumen_humor(evento):
    prompt = f"""
Convierte este evento en una descripción sarcástica y absurda, como si Black Mirror conociera a Chiquito de la Calzada.

Título: {evento['titulo']}
Fecha: {evento['fecha']}
Enlace: {evento['enlace']}

Ejemplo de tono: “Un taller donde los asistentes creen que están revolucionando la IA mientras apenas saben abrir el navegador.”

Resumen:"""
    res = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        temperature=0.8
    )
    return res.choices[0].text.strip()

# Paso 4: Guardar resultados en CSV
def guardar_eventos_csv(eventos, nombre_archivo="eventos.csv"):
    campos = ["titulo", "fecha", "enlace", "categoria", "humor"]
    with open(nombre_archivo, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(eventos)

# Ejecutar todo
def main():
    verificar_admin()
    eventos = obtener_eventos_eventbrite()
    for e in eventos:
        e['categoria'] = clasificar_evento(e['titulo'])
        e['humor'] = generar_resumen_humor(e)
        print("\n---")
        print(f"🗓️ {e['titulo']} ({e['fecha']})")
        print(f"📂 Categoría: {e['categoria']}")
        print(f"🎭 Descripción: {e['humor']}")
        print(f"🔗 {e['enlace']}")
    guardar_eventos_csv(eventos)

if __name__ == "__main__":
    main()
