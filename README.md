# Remote Control — Carro por WiFi con WeMos

Proyecto para controlar un carro a distancia por WiFi usando una placa **WeMos** (ESP8266/ESP32) como puente entre el ordenador y el vehículo.

## Objetivo

Construir un programa que permita enviar comandos al carro de forma inalámbrica cuando la WeMos/ESP32 está configurada como servidor WebSocket en la misma red (misma WiFi que el PC).

## Estado actual

- **`socket.py`** — Módulo de conexión al carro por **WebSocket** (puerto 80, ruta `/ws`). Expone `connect_socket()`, `send_command()`, `receive_data()` y `close_socket()`.
- **`controlador.py`** — Controlador de alto nivel que usa `socket.py`: clase `CarController` con métodos de movimiento, brazo, pinza y velocidad, más modo interactivo por consola.

---

## Instalación en tu PC

Sigue estos pasos según tu sistema operativo para instalar el programa y usar un entorno virtual (recomendado).

### Requisitos previos

- **Python 3.7 o superior**.
- Dependencia externa: **websocket-client** (ver paso 3).
- Conexión a la misma red WiFi que el ESP32/WeMos del carro.

### 1. Obtener el proyecto

Copia la carpeta del proyecto (con `README.md`, `socket.py`, `controlador.py`, `requirements.txt`, etc.) a tu PC, en la ubicación que prefieras.

### 2. Crear y usar el entorno virtual

Un **entorno virtual** aísla las dependencias del proyecto y evita conflictos con otros programas. Es recomendable usarlo en todos los sistemas.

#### En Linux o macOS

Abre una terminal en la carpeta del proyecto y ejecuta:

```bash
# Crear el entorno virtual (carpeta llamada "venv")
python3 -m venv venv

# Activar el entorno virtual
source venv/bin/activate
```

Verás algo como `(venv)` al inicio de la línea: el entorno está activo.

Para **desactivar** el entorno más tarde:

```bash
deactivate
```

#### En Windows (CMD o PowerShell)

Abre **Símbolo del sistema** o **PowerShell** en la carpeta del proyecto:

```cmd
REM Crear el entorno virtual
python -m venv venv

REM Activar (en CMD)
venv\Scripts\activate.bat
```

En **PowerShell** puede ser necesario permitir scripts. Si da error, ejecuta primero:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Luego activa el entorno:

```powershell
.\venv\Scripts\Activate.ps1
```

Verás `(venv)` al inicio de la línea cuando esté activo.

Para **desactivar**:

```cmd
deactivate
```

### 3. Instalar dependencias

El módulo `socket.py` usa WebSocket; hace falta la librería **websocket-client**. Con el entorno virtual activado:

```bash
# Linux / macOS
pip install -r requirements.txt
```

```cmd
REM Windows
pip install -r requirements.txt
```

### 4. Comprobar que todo funciona

Con el entorno virtual activado:

```bash
# Linux / macOS
python3 -c "import websocket; print('OK')"
```

```cmd
REM Windows
python -c "import websocket; print('OK')"
```

Si imprime `OK`, el entorno está listo para usar el controlador.

### Resumen por sistema

| Sistema   | Crear venv             | Activar venv              |
|----------|------------------------|----------------------------|
| Linux    | `python3 -m venv venv`  | `source venv/bin/activate` |
| macOS    | `python3 -m venv venv`  | `source venv/bin/activate` |
| Windows  | `python -m venv venv`  | `venv\Scripts\activate` (CMD) o `.\venv\Scripts\Activate.ps1` (PowerShell) |

> **Nota:** En Windows, si el comando `python` no existe, prueba `py -m venv venv` y `py` para ejecutar scripts.

---

## Configuración necesaria

El carro (ESP32) debe estar en la misma WiFi que el PC y con el servidor **WebSocket** activo (puerto 80, ruta `/ws`, como en el firmware del carro).

En **`socket.py`** configura la IP (y, si cambias el puerto en el firmware, también `PORT`):

```python
HOST = "192.168.1.100"   # IP del ESP32 en tu red (router o Serial)
PORT = 80                # Puerto por defecto del servidor WebSocket del carro
WS_PATH = "/ws"          # Ruta del WebSocket en el firmware
```

---

## Uso del módulo `socket.py`

Es el módulo de conexión al carro por WebSocket. Funciones disponibles:

| Función | Descripción |
|--------|-------------|
| `connect_socket()` | Conecta al WebSocket del carro. Devuelve la conexión o `None` si falla. |
| `send_command(conexion, command)` | Envía un comando (string, ej. un carácter `'W'`, `'S'`, `'X'`). |
| `receive_data(conexion)` | Recibe mensajes del carro (ej. `"CONNECTED"`, `"ACK:x"`). |
| `close_socket(conexion)` | Cierra la conexión. El carro detiene los motores al desconectar. |

Ejemplo (usar otro nombre al importar para no chocar con el módulo estándar `socket` de Python):

```python
import socket as car_socket

conn = car_socket.connect_socket()
if conn:
    car_socket.send_command(conn, "W")
    print(car_socket.receive_data(conn))  # ej. ACK:W
    car_socket.close_socket(conn)
```

---

## Uso del controlador `controlador.py`

### Modo interactivo

Con el venv activado y el carro encendido en la misma WiFi:

```bash
# Linux / macOS
python3 controlador.py
```

```cmd
REM Windows
python controlador.py
```

En la consola escribe comandos y pulsa Enter. Cada letra se envía al carro. **Q** cierra el programa. Vacío + Enter envía stop.

### Comandos que entiende el carro (un carácter)

| Tecla | Acción en el carro        |
|-------|----------------------------|
| W     | Avanzar                    |
| S     | Retroceder                 |
| A     | Girar izquierda            |
| D     | Girar derecha              |
| X     | Detener motores            |
| F     | Avanzar ~15 cm y parar     |
| L     | Girar 90° izquierda y parar|
| R     | Girar 90° derecha y parar  |
| U     | Brazo arriba               |
| J     | Brazo abajo                |
| O     | Pinza abrir                |
| C     | Pinza cerrar               |
| 0–9   | Velocidad (0 mínima, 9 máxima) |

### Usar la clase `CarController` desde tu propio script

```python
from controlador import CarController

ctrl = CarController()
if ctrl.connect():
    ctrl.forward()
    # ...
    ctrl.stop()
    ctrl.arm_up()
    ctrl.gripper_open()
    ctrl.set_speed(5)
    ctrl.disconnect()
```

Métodos disponibles: `forward()`, `backward()`, `turn_left()`, `turn_right()`, `stop()`, `forward_15cm()`, `turn_90_left()`, `turn_90_right()`, `arm_up()`, `arm_down()`, `gripper_open()`, `gripper_close()`, `set_speed(0-9)`, `send_char(char)`.

---

## Requisitos del proyecto

- Python 3.7+
- **websocket-client** (en `requirements.txt`)
