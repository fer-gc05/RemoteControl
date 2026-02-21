import threading
import time

# Importamos el módulo de conexión al carro (car_socket.py)
import car_socket

# En base a la informavion del codigo aplicado al carro tenemos los siguientes comandos:

CMD_FORWARD = "W"  # Avanzar
CMD_BACKWARD = "S"  # Retroceder
CMD_LEFT = "A"  # Girar izquierda
CMD_RIGHT = "D"  # Girar derecha
CMD_STOP = "X"  # Detener motores
CMD_FORWARD_15CM = "F"  # Avanzar 15cm
CMD_TURN_90_LEFT = "L"  # Girar 90° izquierda
CMD_TURN_90_RIGHT = "R"  # Girar 90° derecha
CMD_ARM_UP = "U"  # Brazo arriba
CMD_ARM_DOWN = "J"  # Brazo abajo
CMD_GRIPPER_OPEN = "O"  # Pinza abrir
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
        self._receiver_thread = threading.Thread(target=self._receive_loop, daemon=True)
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

    # --- Movimiento ---
    # Funcion para avanzar el carro.
    def forward(self):
        return self._send(CMD_FORWARD)

    # Funcion para retroceder el carro.
    def backward(self):
        return self._send(CMD_BACKWARD)

    # Funcion para girar a la izquierda el carro.
    def turn_left(self):
        return self._send(CMD_LEFT)

    # Funcion para girar a la derecha el carro.
    def turn_right(self):
        return self._send(CMD_RIGHT)

    # Funcion para detener el carro.
    def stop(self):
        return self._send(CMD_STOP)

    # Funcion para avanzar 15cm el carro.
    def forward_15cm(self):
        return self._send(CMD_FORWARD_15CM)

    # Funcion para girar 90° a la izquierda el carro.
    def turn_90_left(self):
        return self._send(CMD_TURN_90_LEFT)

    # Funcion para girar 90° a la derecha el carro.
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

    print("Conectado. Comandos: W S A D X | F L R | U J O C | 0-9 | Q salir")
    print("  W=avanzar S=atrás A=izq D=der X=stop")
    print("  F=avanzar 15cm L=girar 90° izq R=girar 90° der")
    print("  U=brazo arriba J=brazo abajo O=pinza abrir C=pinza cerrar")
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
                if char in "WSADXFLRUJOC0123456789":  # comandos que entiende el carro
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
