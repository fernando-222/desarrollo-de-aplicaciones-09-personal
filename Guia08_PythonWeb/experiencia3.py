
import json
from wsgiref.simple_server import make_server


def inspector_entorno_wsgi(environ, start_response):

    # 1. Filtrar las variables que contienen texto
    entorno_legible = {}

    for clave, valor in environ.items():
        if isinstance(valor, str):
            entorno_legible[clave] = valor

    # 2. Convertir el diccionario a JSON
    texto_diagnostico = json.dumps(
        entorno_legible,
        indent=4,
        ensure_ascii=False
    )

    cuerpo_bytes = texto_diagnostico.encode("utf-8")

    # 3. Preparar la respuesta HTTP
    start_response("200 OK", [
        ("Content-Type", "application/json; charset=utf-8"),
        ("Content-Length", str(len(cuerpo_bytes)))
    ])

    # 4. Devolver la respuesta en bytes
    return [cuerpo_bytes]


# Iniciar el servidor WSGI
if __name__ == "__main__":
    servidor_diagnostico = make_server(
        "127.0.0.1",
        8080,
        inspector_entorno_wsgi
    )

    print("Servidor WSGI activo en http://127.0.0.1:8080")
    print("Presiona Ctrl + C para detenerlo.")

    try:
        servidor_diagnostico.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")
    finally:
        servidor_diagnostico.server_close()
