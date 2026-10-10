
import os
import json
import mimetypes
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlsplit, parse_qs


# 1. Preparar el directorio publico permitido
DIRECTORIO_BASE = os.path.abspath(os.getcwd())
DIRECTORIO_PUBLICO = os.path.abspath(
    os.path.join(DIRECTORIO_BASE, "public")
)

# 2. Simular una coleccion de 100 articulos
base_de_datos = [
    {"id": i, "articulo": f"Item {i}", "valor": i * 10}
    for i in range(1, 101)
]


class ServidorHibrido(BaseHTTPRequestHandler):

    # Enviar respuestas JSON
    def emitir_json(self, codigo, datos):
        contenido = json.dumps(
            datos,
            ensure_ascii=False,
            indent=4
        ).encode("utf-8")

        self.send_response(codigo)
        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8"
        )
        self.send_header(
            "Content-Length",
            str(len(contenido))
        )
        self.end_headers()
        self.wfile.write(contenido)

    # Procesar peticiones GET
    def do_GET(self):

        ruta = urlsplit(self.path).path

        # 3. API de inventario
        if ruta == "/api/inventario":
            parametros = parse_qs(
                urlsplit(self.path).query
            )

            try:
                limite = int(
                    parametros.get("limite", ["10"])[0]
                )
                pagina = int(
                    parametros.get("pagina", ["1"])[0]
                )
            except ValueError:
                self.emitir_json(400, {
                    "error": "limite y pagina deben ser numericos"
                })
                return

            if limite < 1 or pagina < 1:
                self.emitir_json(400, {
                    "error": "limite y pagina deben ser positivos"
                })
                return

            # 4. Limite maximo de 100 registros
            limite = min(limite, 100)

            # 5. Filtrar por coincidencia parcial
            filtro = parametros.get("filtro", [""])[0].strip()

            datos_filtrados = [
                articulo for articulo in base_de_datos
                if filtro.lower() in articulo["articulo"].lower()
            ]

            # 6. Calcular paginacion
            total = len(datos_filtrados)
            desplazamiento = (pagina - 1) * limite

            datos_pagina = datos_filtrados[
                desplazamiento:desplazamiento + limite
            ]

            self.emitir_json(200, {
                "meta": {
                    "pagina": pagina,
                    "limite": limite,
                    "total_items": total,
                    "total_paginas": (
                        (total + limite - 1) // limite
                    )
                },
                "registros": datos_pagina
            })
            return

        # 7. Servir archivos estaticos desde /public
        if ruta == "/":
            ruta_relativa = "index.html"
        elif ruta.startswith("/public/"):
            ruta_relativa = ruta[len("/public/"):]
        else:
            self.send_error(404, "Ruta no encontrada")
            return

        ruta_archivo = os.path.abspath(
            os.path.join(DIRECTORIO_PUBLICO, ruta_relativa)
        )

        # 8. Comprobar que la ruta permanezca dentro de public
        try:
            dentro_del_directorio = (
                os.path.commonpath([
                    DIRECTORIO_PUBLICO,
                    ruta_archivo
                ]) == DIRECTORIO_PUBLICO
            )
        except ValueError:
            dentro_del_directorio = False

        if not dentro_del_directorio:
            self.send_error(403, "Acceso denegado")
            return

        if not os.path.isfile(ruta_archivo):
            self.send_error(404, "Archivo no encontrado")
            return

        # 9. Identificar MIME y enviar el archivo
        tipo_mime, _ = mimetypes.guess_type(ruta_archivo)

        try:
            with open(ruta_archivo, "rb") as archivo:
                contenido = archivo.read()

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
            self.send_error(500, "Error al leer el archivo")


# 10. Iniciar el servidor
if __name__ == "__main__":

    os.makedirs(DIRECTORIO_PUBLICO, exist_ok=True)

    servidor = HTTPServer(
        ("127.0.0.1", 8085),
        ServidorHibrido
    )

    print("Servidor hibrido activo en http://127.0.0.1:8085")
    print("Inventario: http://127.0.0.1:8085/api/inventario")
    print("Presiona Ctrl + C para detenerlo.")

    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")
    finally:
        servidor.server_close()
