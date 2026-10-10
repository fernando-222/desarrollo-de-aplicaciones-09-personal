
from wsgiref.simple_server import make_server


# 1. Núcleo del micro-framework
class NucleoWSGI:

    def __init__(self):
        self.mapa_enrutamiento = {}

    # Registrar rutas mediante un decorador
    def registrar_endpoint(self, ruta_esperada):
        def envoltura_compilacion(funcion_controlador):
            self.mapa_enrutamiento[ruta_esperada] = funcion_controlador
            return funcion_controlador

        return envoltura_compilacion

    # Despachador de peticiones WSGI
    def __call__(self, environ, start_response):
        ruta_solicitada = environ.get("PATH_INFO", "/")

        if ruta_solicitada in self.mapa_enrutamiento:
            respuesta_texto = self.mapa_enrutamiento[ruta_solicitada](environ)
            estado = "200 OK"
        else:
            respuesta_texto = "Error 404: Ruta no encontrada."
            estado = "404 Not Found"

        payload = respuesta_texto.encode("utf-8")

        start_response(estado, [
            ("Content-Type", "text/plain; charset=utf-8"),
            ("Content-Length", str(len(payload)))
        ])

        return [payload]


# 2. Middleware de auditoría
class MiddlewareAuditoria:

    def __init__(self, aplicacion_interior):
        self.aplicacion_interior = aplicacion_interior

    def __call__(self, environ, start_response):
        verbo = environ.get("REQUEST_METHOD")
        uri = environ.get("PATH_INFO")

        print(
            f"[Auditoria] Peticion recibida: {verbo} {uri}"
        )

        # Delegar la petición al framework
        return self.aplicacion_interior(environ, start_response)


# 3. Crear la aplicación
app = NucleoWSGI()


# 4. Registrar una ruta con un decorador
@app.registrar_endpoint("/saludo")
def vista_saludo(environ):
    return "Micro-Framework funcionando correctamente."


# 5. Envolver la aplicación con el middleware
aplicacion_fortificada = MiddlewareAuditoria(app)


# 6. Iniciar el servidor
if __name__ == "__main__":
    servidor = make_server(
        "127.0.0.1",
        8081,
        aplicacion_fortificada
    )

    print("Micro-Framework activo en http://127.0.0.1:8081")
    print("Ruta de prueba: http://127.0.0.1:8081/saludo")
    print("Presiona Ctrl + C para detener el servidor.")

    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")
    finally:
        servidor.server_close()
