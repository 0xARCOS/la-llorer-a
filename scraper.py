# scraper.py
import csv
import logging
import openai
import os
from dotenv import load_dotenv
import getpass
from fuentes import todas

# Carga variables de entorno desde .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")  # Usa la clave desde .env
ADMIN_KEY = os.getenv("ADMIN_KEY")            # Usa la clave desde .env

logging.basicConfig(
    filename="errores.log",
    filemode="a",
    level=logging.ERROR,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

def verificar_admin():
    """Solicita la clave de administrador solo si no se proporcionó por
    variable de entorno.

    Cuando el script se ejecuta de forma automática (por ejemplo en
    GitHub Actions) se espera que `ADMIN_KEY` ya esté definida, por lo que
    se omite la petición interactiva.
    """
    if os.getenv("GITHUB_ACTIONS") == "true":
        # En entornos no interactivos confiamos en la clave del entorno
        if not ADMIN_KEY:
            print("❌ ADMIN_KEY no configurada. Acceso denegado.")
            exit()
        return

    clave = getpass.getpass("🔐 Ingresa la clave de administrador: ")
    if clave != ADMIN_KEY:
        print("❌ Clave incorrecta. Acceso denegado.")
        exit()

# Paso 1: Obtener eventos de múltiples fuentes

# Paso 2: Clasificación temática
def clasificar_evento(titulo):
    prompt = f"Clasifica este evento tech: '{titulo}' en una de estas categorías: IA, Ciberseguridad, Web, Absurdos, Otro.\nCategoría:"
    try:
        res = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=10,
            temperature=0.2,
        )
        return res.choices[0].text.strip()
    except openai.error.OpenAIError as e:
        logging.error("Error de OpenAI clasificando '%s': %s", titulo, e)
        return "Otro"

# Paso 3: Descripción estilo ‘La Llorería’
def generar_resumen_humor(evento):
    prompt = f"""
Convierte este evento en una descripción sarcástica y absurda, como si Black Mirror conociera a Chiquito de la Calzada.

Título: {evento['titulo']}
Fecha: {evento['fecha']}
Enlace: {evento['enlace']}

Ejemplo de tono: “Un taller donde los asistentes creen que están revolucionando la IA mientras apenas saben abrir el navegador.”

Resumen:"""
    try:
        res = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=100,
            temperature=0.8,
        )
        return res.choices[0].text.strip()
    except openai.error.OpenAIError as e:
        logging.error("Error de OpenAI generando resumen para '%s': %s", evento.get('titulo'), e)
        return "No se pudo generar resumen"

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
    eventos = []
    for fuente in todas:
        try:
            eventos.extend(fuente.obtener_eventos())
        except Exception as e:
            msg = f"Error al obtener eventos de {fuente.__class__.__name__}: {e}"
            print(f"⚠️ {msg}")
            logging.error(msg)
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
