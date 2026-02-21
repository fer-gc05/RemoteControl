import threading
import time

# Importamos el módulo de conexión al carro (car_socket.py)
import car_socket

# Comandos del firmware actual del carro (WeMos): F B L R X + U J O C + 0-9

CMD_STOP = "X"           # Detener motores
CMD_FORWARD_15CM = "F"   # Avanzar ~15 cm y parar
CMD_BACKWARD_15CM = "B"  # Retroceder ~15 cm y parar
CMD_TURN_90_LEFT = "L"   # Girar 90° izquierda y parar
CMD_TURN_90_RIGHT = "R"  # Girar 90° derecha y parar
CMD_ARM_UP = "U"         # Brazo arriba
CMD_ARM_DOWN = "J"       # Brazo abajo
CMD_GRIPPER_OPEN = "O"   # Pinza abrir
CMD_GRIPPER_CLOSE = "C"  # Pinza cerrar


# Clase para controlar el carro.
class CarController:

    def __init__(self):
        self._connection = None
        self._receiver_thread = None
        self._shutdown = False

    # Funcion para conectar al WebSocket del carro.
    def connect(self):
        self._connection = car_socket.connect_socket()
        if self._connection is None:
            return False
        self._shutdown = False
        self._receiver_thread = threading.Thread(
            target=self._receive_loop, daemon=True)
        self._receiver_thread.start()
        return True

    # Funcion para recibir datos del WebSocket del carro en segundo plano.
    def _receive_loop(self):
        while not self._shutdown and self._connection is not None:
            try:
                msg = car_socket.receive_data(self._connection)
                if msg:
                    print(f"Carro: {msg}")
            except Exception:
                break

    # Funcion para enviar un comando al WebSocket del carro.
    def _send(self, char):
        return car_socket.send_command(self._connection, char)

    # Funcion para enviar un comando al WebSocket del carro.
    def send_char(self, char):
        return self._send(char)

    # Funcion para cerrar la conexion con el WebSocket del carro.
    def disconnect(self):
        self._shutdown = True
        if self._connection is not None:
            car_socket.close_socket(self._connection)
            self._connection = None

    # --- Movimiento (el firmware solo tiene F/B/L/R con parada automática + X) ---
    def stop(self):
        return self._send(CMD_STOP)

    def forward(self):
        """Avanzar ~15 cm y parar (comando F)."""
        return self._send(CMD_FORWARD_15CM)

    def forward_15cm(self):
        return self._send(CMD_FORWARD_15CM)

    def backward(self):
        """Retroceder ~15 cm y parar (comando B)."""
        return self._send(CMD_BACKWARD_15CM)

    def backward_15cm(self):
        return self._send(CMD_BACKWARD_15CM)

    def turn_left(self):
        """Girar 90° izquierda y parar (comando L)."""
        return self._send(CMD_TURN_90_LEFT)

    def turn_90_left(self):
        return self._send(CMD_TURN_90_LEFT)

    def turn_right(self):
        """Girar 90° derecha y parar (comando R)."""
        return self._send(CMD_TURN_90_RIGHT)

    def turn_90_right(self):
        return self._send(CMD_TURN_90_RIGHT)

    # --- Brazo y pinza ---
    # Funcion para subir el brazo el carro.
    def arm_up(self):
        return self._send(CMD_ARM_UP)

    # Funcion para bajar el brazo el carro.
    def arm_down(self):
        return self._send(CMD_ARM_DOWN)

    # Funcion para abrir la pinza el carro.
    def gripper_open(self):
        return self._send(CMD_GRIPPER_OPEN)

    # Funcion para cerrar la pinza el carro.
    def gripper_close(self):
        return self._send(CMD_GRIPPER_CLOSE)

    # --- Velocidad (0–9, en el carro se mapea a 100–255) ---
    # Funcion para establecer la velocidad el carro.
    def set_speed(self, level):
        if 0 <= level <= 9:
            return self._send(str(level))
        return False


# Funcion principal para el controlador del carro.
def main():
    print("Controlador del carro — WebSocket (módulo car_socket)")
    print()

    ctrl = CarController()  # instancia del controlador del carro
    if not ctrl.connect():  # conecta al carro
        return

    print("Conectado. Comandos: F B L R X | U J O C | 0-9 | Q salir")
    print("  F=avanzar 15cm  B=retroceder 15cm  L=90° izq  R=90° der  X=stop")
    print("  U=brazo arriba  J=brazo abajo  O=pinza abrir  C=pinza cerrar")
    print("  0-9 = velocidad")
    print()

    try:
        while True:
            line = input("Comando > ").strip().upper()
            if not line:
                ctrl.stop()
                continue
            if line == "Q":
                break
            for char in line:
                if char in "FBRLXUJOC0123456789":  # comandos que entiende el carro
                    ctrl.send_char(char)
                    time.sleep(0.05)
    except KeyboardInterrupt:
        pass
    finally:
        ctrl.stop()
        ctrl.disconnect()
        print("Desconectado.")


if __name__ == "__main__":
    main()
