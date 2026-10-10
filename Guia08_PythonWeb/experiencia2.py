
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

# Colección de usuarios almacenada en memoria
coleccion_usuarios = [
    {"id": 100, "nombre": "Linus Torvalds", "perfil": "SysAdmin"}
]


class EnrutadorAPI(BaseHTTPRequestHandler):

    # Función para enviar respuestas en formato JSON
    def emitir_json(self, codigo_http, datos_diccionario):
        payload = json.dumps(
            datos_diccionario,
            ensure_ascii=False
        ).encode("utf-8")

        self.send_response(codigo_http)
        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8"
        )
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    # GET: consultar usuarios
    def do_GET(self):
        if self.path == "/api/usuarios":
            self.emitir_json(200, {
                "estado": "ok",
                "total": len(coleccion_usuarios),
                "datos": coleccion_usuarios
            })
        else:
            self.emitir_json(404, {
                "error": "Endpoint no mapeado en la API"
            })

    # POST: registrar un usuario
    def do_POST(self):
        if self.path != "/api/usuarios":
            self.emitir_json(404, {
                "error": "Endpoint no mapeado en la API"
            })
            return

        longitud = int(self.headers.get("Content-Length", 0))

        if longitud <= 0 or longitud > 10000:
            self.emitir_json(400, {
                "error": "Longitud del contenido no válida"
            })
            return

        bytes_recibidos = self.rfile.read(longitud)

        try:
            nuevo_registro = json.loads(
                bytes_recibidos.decode("utf-8")
            )

            if not isinstance(nuevo_registro, dict):
                raise ValueError("Se esperaba un objeto JSON")

            if not all(
                isinstance(nuevo_registro.get(campo), str)
                and nuevo_registro[campo].strip()
                for campo in ("nombre", "perfil")
            ):
                self.emitir_json(400, {
                    "error": "Se requieren nombre y perfil"
                })
                return

            nuevo_registro["id"] = (
                coleccion_usuarios[-1]["id"] + 1
                if coleccion_usuarios else 1
            )

            coleccion_usuarios.append(nuevo_registro)

            self.emitir_json(201, {
                "estado": "creado",
                "datos": nuevo_registro
            })

        except (json.JSONDecodeError, UnicodeDecodeError, ValueError):
            self.emitir_json(400, {
                "error": "El cuerpo debe contener JSON válido"
            })


if __name__ == "__main__":
    servidor = HTTPServer(
        ("127.0.0.1", 8001),
        EnrutadorAPI
    )

    print("API activa en http://127.0.0.1:8001")
    print("Presiona Ctrl + C para detener el servidor.")

    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")
    finally:
        servidor.server_close()
