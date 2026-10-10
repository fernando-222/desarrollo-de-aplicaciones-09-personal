
import json
from urllib.parse import parse_qs
from wsgiref.simple_server import make_server


def endpoint_recepcion_estricta(environ, start_response):

    # 1. Aceptar únicamente POST y PUT
    if environ.get("REQUEST_METHOD") not in ["POST", "PUT"]:
        start_response("405 Method Not Allowed", [
            ("Content-Type", "application/json")
        ])
        return [b'{"error": "Metodo transaccional bloqueado"}']

    # 2. Leer la longitud del contenido
    try:
        tamano_buffer = int(
            environ.get("CONTENT_LENGTH", "0") or "0"
        )
    except ValueError:
        tamano_buffer = 0

    if tamano_buffer <= 0 or tamano_buffer > 10000:
        start_response("400 Bad Request", [
            ("Content-Type", "application/json")
        ])
        return [b'{"error": "Tamano del contenido no valido"}']

    cuerpo_bytes = environ["wsgi.input"].read(tamano_buffer)
    metadato_formato = environ.get("CONTENT_TYPE", "")

    # 3. Deserializacion segun el formato recibido
    try:
        if "application/json" in metadato_formato:
            dto_diccionario = json.loads(
                cuerpo_bytes.decode("utf-8")
            )

        elif "application/x-www-form-urlencoded" in metadato_formato:
            diccionario_listas = parse_qs(
                cuerpo_bytes.decode("utf-8")
            )
            dto_diccionario = {
                clave: valores[0]
                for clave, valores in diccionario_listas.items()
            }

        else:
            start_response("415 Unsupported Media Type", [
                ("Content-Type", "application/json")
            ])
            return [
                b'{"error": "Formato JSON o URL-Encoded requerido"}'
            ]

    except (json.JSONDecodeError, UnicodeDecodeError, ValueError):
        start_response("400 Bad Request", [
            ("Content-Type", "application/json")
        ])
        return [b'{"error": "Formato de transferencia incorrecto"}']

    # 4. Verificar que el JSON sea un objeto
    if not isinstance(dto_diccionario, dict):
        start_response("400 Bad Request", [
            ("Content-Type", "application/json")
        ])
        return [b'{"error": "Se esperaba un objeto de datos"}']

    # 5. Validar las propiedades obligatorias de la guia
    llaves_obligatorias = {
        "identificador",
        "token_operacion",
        "comando"
    }

    llaves_faltantes = (
        llaves_obligatorias - dto_diccionario.keys()
    )

    if llaves_faltantes:
        mensaje = json.dumps({
            "error": "Violacion del esquema",
            "propiedades_faltantes": sorted(llaves_faltantes)
        }).encode("utf-8")

        start_response("400 Bad Request", [
            ("Content-Type", "application/json"),
            ("Content-Length", str(len(mensaje)))
        ])
        return [mensaje]

    # 6. Confirmar que los datos cumplen el esquema
    respuesta_ok = json.dumps({
        "estado": "Payload estandarizado y auditado exitosamente",
        "datos": dto_diccionario
    }, ensure_ascii=False).encode("utf-8")

    start_response("200 OK", [
        ("Content-Type", "application/json; charset=utf-8"),
        ("Content-Length", str(len(respuesta_ok)))
    ])

    return [respuesta_ok]


# 7. Iniciar el servidor
if __name__ == "__main__":
    servidor = make_server(
        "127.0.0.1",
        8083,
        endpoint_recepcion_estricta
    )

    print("Servidor de recepcion activo en http://127.0.0.1:8083")
    print("Presiona Ctrl + C para detenerlo.")

    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")
    finally:
        servidor.server_close()
