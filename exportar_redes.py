import csv
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def generar_copy(evento):
    prompt = (
        "Crea un copy breve y divertido para Instagram o TikTok anunciando este "
        f"evento tech en Madrid:\nTitulo: {evento['titulo']}\nFecha: {evento['fecha']}\n" 
        "Copy:"
    )
    try:
        res = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=40,
            temperature=0.7,
        )
        return res.choices[0].text.strip()
    except openai.error.OpenAIError as e:
        return f"No se pudo generar copy para {evento['titulo']}: {e}"


def generar_contenido(csv_file="eventos.csv", cantidad=3):
    with open(csv_file, newline="", encoding="utf-8") as f:
        eventos = list(csv.DictReader(f))[:cantidad]
    contenido = [generar_copy(e) for e in eventos]
    mensaje = "\n".join(f"{i+1}. {c}" for i, c in enumerate(contenido))
    return mensaje


if __name__ == "__main__":
    texto = generar_contenido()
    with open("redes.txt", "w", encoding="utf-8") as f:
        f.write(texto)
    print("Contenido generado en redes.txt")
    print(texto)

