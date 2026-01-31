import socket  # Libreria para conexiones de red, nos permite comunicarme en tiempo real con el carro

HOST = 'Ip que se encuentre asociada al carro configurado con la placa wemos'
PORT = 'Puerto que se encuentre asociada al carro configurado con la placa wemos'

# Funcion para conectar al socket del carro
def connect_socket():
    try:
        socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.connect((HOST, PORT))
        return socket
    except socket.error as e:
        print(f"Error al conectar al socket: {e}")
        return None

# Funcion para enviar comandos al carro
def send_command(socket, command):
    try:
        socket.send(command.encode())
        return True
    except socket.error as e:
        print(f"Error al enviar comando: {e}")
        return False

# Funcion para recibir datos del carro
def receive_data(socket):
    try:
        data = socket.recv(1024)
        return data.decode()
    except socket.error as e:
        print(f"Error al recibir datos: {e}")
        return None

# Funcion para cerrar la conexion con el carro
def close_socket(socket):
    try:
        socket.close()
        return True
    except socket.error as e:
        print(f"Error al cerrar la conexion: {e}")
        return False
