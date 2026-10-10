
import os
import mimetypes
from http.server import BaseHTTPRequestHandler, HTTPServer


class ServidorEstaticoFortificado(BaseHTTPRequestHandler):

    def do_GET(self):
        # 1. Definir el directorio permitido
        directorio_base = os.path.realpath(os.getcwd())

        # 2. Obtener la ruta solicitada
        ruta_cruda = self.path.split("?")[0].lstrip("/")

        if not ruta_cruda:
            ruta_cruda = "index.html"

        # 3. Construir y normalizar la ruta
        ruta_resuelta = os.path.realpath(
            os.path.join(directorio_base, ruta_cruda)
        )

        # 4. Verificar que el archivo permanezca dentro
        # del directorio permitido
        if (
            os.path.commonpath([directorio_base, ruta_resuelta])
            != directorio_base
            or not os.path.isfile(ruta_resuelta)
        ):
            self.send_error(
                404,
                "Recurso no encontrado o acceso denegado."
            )
            return

        # 5. Identificar el tipo de archivo
        tipo_mime, _ = mimetypes.guess_type(ruta_resuelta)

        try:
            # 6. Leer el archivo en modo binario
            with open(ruta_resuelta, "rb") as archivo:
                contenido = archivo.read()

            # 7. Enviar la respuesta HTTP
            self.send_response(200)
            self.send_header(
                "Content-Type",
                tipo_mime or "application/octet-stream"
            )
            self.send_header(
                "Content-Length",
                str(len(contenido))
            )
            self.end_headers()

            self.wfile.write(contenido)

        except OSError:
            self.send_error(500, "Error al leer el archivo.")


# 8. Iniciar el servidor
if __name__ == "__main__":
    servidor = HTTPServer(
        ("127.0.0.1", 8000),
        ServidorEstaticoFortificado
    )

    print("Servidor activo en http://127.0.0.1:8000")
    print("Presiona Ctrl + C para detenerlo.")

    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")
    finally:
        servidor.server_close()
