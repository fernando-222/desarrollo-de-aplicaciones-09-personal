
import json
from urllib.parse import parse_qs
from wsgiref.simple_server import make_server


# 1. Aplicacion principal WSGI
def aplicacion_inscripciones(environ, start_response):

    # Verificar el metodo HTTP
    if environ.get("REQUEST_METHOD") != "POST":
        respuesta = json.dumps({
            "error": "Metodo no permitido. Utilice POST."
        }).encode("utf-8")

        start_response("405 Method Not Allowed", [
            ("Content-Type", "application/json; charset=utf-8"),
            ("Content-Length", str(len(respuesta)))
        ])
        return [respuesta]

    # Verificar la ruta
    if environ.get("PATH_INFO") != "/api/inscripciones":
        respuesta = json.dumps({
            "error": "Endpoint no encontrado."
        }).encode("utf-8")

        start_response("404 Not Found", [
            ("Content-Type", "application/json; charset=utf-8"),
            ("Content-Length", str(len(respuesta)))
        ])
        return [respuesta]

    # 2. Leer el cuerpo de la peticion de forma controlada
    try:
        longitud = int(environ.get("CONTENT_LENGTH", "0") or "0")
    except ValueError:
        longitud = 0

    if longitud <= 0 or longitud > 10000:
        respuesta = json.dumps({
            "error": "Longitud del contenido no valida."
        }).encode("utf-8")

        start_response("400 Bad Request", [
            ("Content-Type", "application/json; charset=utf-8"),
            ("Content-Length", str(len(respuesta)))
        ])
        return [respuesta]

    cuerpo_bytes = environ["wsgi.input"].read(longitud)
    tipo_contenido = environ.get("CONTENT_TYPE", "")

    # 3. Deserializacion segun el formato recibido
    try:
        if "application/json" in tipo_contenido:
            datos = json.loads(cuerpo_bytes.decode("utf-8"))

        elif "application/x-www-form-urlencoded" in tipo_contenido:
            datos_listas = parse_qs(
                cuerpo_bytes.decode("utf-8")
            )
            datos = {
                clave: valores[0]
                for clave, valores in datos_listas.items()
            }

        else:
            respuesta = json.dumps({
                "error": "Formato no admitido. Envie JSON o formulario."
            }).encode("utf-8")

            start_response("415 Unsupported Media Type", [
                ("Content-Type", "application/json; charset=utf-8"),
                ("Content-Length", str(len(respuesta)))
            ])
            return [respuesta]

    except (json.JSONDecodeError, UnicodeDecodeError, ValueError):
        respuesta = json.dumps({
            "error": "Los datos enviados tienen un formato incorrecto."
        }).encode("utf-8")

        start_response("400 Bad Request", [
            ("Content-Type", "application/json; charset=utf-8"),
            ("Content-Length", str(len(respuesta)))
        ])
        return [respuesta]

    # Verificar que los datos formen un objeto
    if not isinstance(datos, dict):
        respuesta = json.dumps({
            "error": "Se esperaba un objeto de datos."
        }).encode("utf-8")

        start_response("400 Bad Request", [
            ("Content-Type", "application/json; charset=utf-8"),
            ("Content-Length", str(len(respuesta)))
        ])
        return [respuesta]

    # 4. Validar los campos obligatorios
    campos_obligatorios = {
        "dni",
        "correo_electronico",
        "programa_academico"
    }

    campos_faltantes = campos_obligatorios - datos.keys()

    if campos_faltantes:
        respuesta = json.dumps({
            "error": "Faltan campos obligatorios.",
            "campos_faltantes": sorted(campos_faltantes)
        }).encode("utf-8")

        start_response("400 Bad Request", [
            ("Content-Type", "application/json; charset=utf-8"),
            ("Content-Length", str(len(respuesta)))
        ])
        return [respuesta]

    # 5. Confirmar la inscripcion
    respuesta = json.dumps({
        "estado": "Inscripcion recibida correctamente",
        "datos": datos
    }, ensure_ascii=False).encode("utf-8")

    start_response("201 Created", [
        ("Content-Type", "application/json; charset=utf-8"),
        ("Content-Length", str(len(respuesta)))
    ])

    return [respuesta]


# 6. Middleware de seguridad por token
class MiddlewareTokenSeguridad:

    def __init__(self, aplicacion_interna):
        self.aplicacion_interna = aplicacion_interna
        self.token_esperado = "Bearer TOKEN_SECRETO_2026"

    def __call__(self, environ, start_response):

        autorizacion = environ.get("HTTP_AUTHORIZATION", "")

        # Rechazar las peticiones sin el token correcto
        if autorizacion != self.token_esperado:
            respuesta = json.dumps({
                "error": "No autorizado. Token invalido o ausente."
            }).encode("utf-8")

            start_response("401 Unauthorized", [
                ("Content-Type", "application/json; charset=utf-8"),
                ("Content-Length", str(len(respuesta)))
            ])

            return [respuesta]

        # Si el token es correcto, continuar hacia la aplicacion
        return self.aplicacion_interna(environ, start_response)


# 7. Envolver la aplicacion con el middleware
aplicacion_segura = MiddlewareTokenSeguridad(
    aplicacion_inscripciones
)


# 8. Iniciar el servidor WSGI
if __name__ == "__main__":
    servidor = make_server(
        "127.0.0.1",
        8084,
        aplicacion_segura
    )

    print("Servicio de inscripciones activo.")
    print("Endpoint: http://127.0.0.1:8084/api/inscripciones")
    print("Presiona Ctrl + C para detener el servidor.")

    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")
    finally:
        servidor.server_close()
