
import json
from urllib.parse import parse_qs
from wsgiref.simple_server import make_server


# 1. Simulación de una base de datos con 100 artículos
base_de_datos = [
    {"id": i, "articulo": f"Item {i}", "valor": i * 10}
    for i in range(1, 101)
]


# 2. Endpoint de inventario con paginación
def endpoint_inventario_paginado(environ, start_response):

    # Obtener los parámetros de la URL
    cadena_consulta = environ.get("QUERY_STRING", "")
    parametros_url = parse_qs(cadena_consulta)

    try:
        limite_elementos = int(
            parametros_url.get("limite", ["10"])[0]
        )
        pagina_actual = int(
            parametros_url.get("pagina", ["1"])[0]
        )

        # Validar los valores recibidos
        if limite_elementos < 1 or pagina_actual < 1:
            raise ValueError

    except ValueError:
        estado = "400 Bad Request"
        cuerpo = {
            "error": "La pagina y el limite deben ser enteros positivos"
        }

    else:
        # 3. Establecer el límite máximo de 50 registros
        limite_elementos = min(limite_elementos, 50)

        # 4. Calcular el desplazamiento
        indice_desplazamiento = (
            pagina_actual - 1
        ) * limite_elementos

        indice_corte = (
            indice_desplazamiento + limite_elementos
        )

        # 5. Seleccionar los registros de la página
        datos_cortados = base_de_datos[
            indice_desplazamiento:indice_corte
        ]

        estado = "200 OK"
        cuerpo = {
            "meta": {
                "pagina": pagina_actual,
                "limite_real": limite_elementos,
                "total_items": len(base_de_datos)
            },
            "registros": datos_cortados
        }

    # 6. Convertir la respuesta a JSON y enviarla
    payload = json.dumps(
        cuerpo,
        ensure_ascii=False,
        indent=4
    ).encode("utf-8")

    start_response(estado, [
        ("Content-Type", "application/json; charset=utf-8"),
        ("Content-Length", str(len(payload)))
    ])

    return [payload]


# 7. Iniciar el servidor WSGI
if __name__ == "__main__":
    servidor = make_server(
        "127.0.0.1",
        8082,
        endpoint_inventario_paginado
    )

    print("Servidor de inventario activo.")
    print("Prueba: http://127.0.0.1:8082/?limite=10&pagina=1")
    print("Presiona Ctrl + C para detenerlo.")

    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")
    finally:
        servidor.server_close()
