# Configuración: IP del ESP32/carro o simulador. Puerto y ruta /ws.
# Misma PC que el simulador → usa 127.0.0.1. Carro/simulador en otra PC → usa su IP (ej. 192.168.2.16).
HOST = "127.0.0.1"
PORT = 8080
WS_PATH = "/ws"


# Funcion para obtener la URL del WebSocket del carro.
def _get_ws_url():
    """URL completa del WebSocket del carro."""
    return f"ws://{HOST}:{PORT}{WS_PATH}"


# Funcion para conectar al WebSocket del carro.
def connect_socket():
    try:
        import websocket
        ws = websocket.create_connection(_get_ws_url(), timeout=5)
        return ws
    except Exception as e:
        print(f"Error al conectar al socket: {e}")
        return None


# Funcion para enviar un comando al WebSocket del carro.
def send_command(sock, command):
    if sock is None:
        print("No hay conexión. Usa connect_socket() antes.")
        return False
    try:
        s = command if isinstance(command, str) else str(command)
        sock.send(s)
        return True
    except Exception as e:
        print(f"Error al enviar comando: {e}")
        return False


# Funcion para recibir datos del WebSocket del carro.
# Si no hay respuesta (timeout, etc.) devuelve None sin imprimir nada.
# Solo se muestra algo en consola cuando el controlador recibe un mensaje (CONNECTED, ACK:x).
def receive_data(sock):
    if sock is None:
        return None
    try:
        data = sock.recv()
        return data if isinstance(data, str) else data.decode("utf-8")
    except Exception:
        return None


# Funcion para cerrar la conexion con el WebSocket del carro.
def close_socket(sock):
    if sock is None:
        return True
    try:
        sock.close()
        return True
    except Exception as e:
        print(f"Error al cerrar la conexión: {e}")
        return False
