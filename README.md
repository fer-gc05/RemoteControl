# Remote Control — Carro por WiFi con WeMos

Proyecto para controlar un carro a distancia por WiFi usando una placa **WeMos** (ESP8266/ESP32) como puente entre el ordenador y el vehículo.

## Objetivo

Construir un programa que permita enviar comandos al carro de forma inalámbrica cuando la WeMos está configurada como servidor en la misma red (misma WiFi que el PC).

## Estado actual

- **Listo:** script de conexión por socket (`socket.py`) para comunicarse con el carro cuando la WeMos está configurada como servidor TCP en la red.

---

## Instalación en tu PC

Sigue estos pasos según tu sistema operativo para instalar el programa y usar un entorno virtual (recomendado).

### Requisitos previos

- **Python 3.7 o superior** (el proyecto solo usa la librería estándar `socket`, no hay dependencias externas).
- Conexión a la misma red WiFi que la WeMos del carro.

### 1. Obtener el proyecto

Copia la carpeta del proyecto (con `README.md` y `socket.py`) a tu PC, en la ubicación que prefieras.

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

### 3. Instalar dependencias (opcional)

Este proyecto no usa paquetes externos; solo la librería estándar de Python. Si más adelante añades un `requirements.txt`, instala con:

```bash
# Linux / macOS (con el venv activado)
pip install -r requirements.txt
```

```cmd
REM Windows (con el venv activado)
pip install -r requirements.txt
```

### 4. Comprobar que todo funciona

Con el entorno virtual activado:

```bash
# Linux / macOS
python3 -c "import socket; print('OK')"
```

```cmd
REM Windows
python -c "import socket; print('OK')"
```

Si imprime `OK`, Python y el módulo `socket` están listos.

### Resumen por sistema

| Sistema   | Crear venv           | Activar venv              |
|----------|----------------------|----------------------------|
| Linux    | `python3 -m venv venv` | `source venv/bin/activate` |
| macOS    | `python3 -m venv venv` | `source venv/bin/activate` |
| Windows  | `python -m venv venv`  | `venv\Scripts\activate` (CMD) o `.\venv\Scripts\Activate.ps1` (PowerShell) |

> **Nota:** En Windows, si el comando `python` no existe, prueba `py -m venv venv` y `py` para ejecutar scripts.

---

## Configuración necesaria

Para que el script funcione, la WeMos debe estar configurada así:

1. **Conectada a la misma red WiFi** que el ordenador desde el que ejecutas el programa.
2. **Actuando como servidor TCP:** escuchando en una IP y un puerto concretos.
3. Debes conocer la **IP** asignada a la WeMos en tu red (p. ej. desde el router o imprimiéndola en el firmware) y el **puerto** donde abre el servidor.

En `socket.py` debes configurar:

```python
HOST = '192.168.1.XXX'   # IP de la WeMos en tu red
PORT = 12345             # Puerto donde escucha el servidor en la WeMos
```

Sustituye `192.168.1.XXX` por la IP real de tu WeMos y `12345` por el puerto que uses en el firmware.

## Uso del módulo `socket.py`

El script ofrece estas funciones:

| Función | Descripción |
|--------|-------------|
| `connect_socket()` | Conecta al socket del carro (WeMos). Devuelve el socket o `None` si falla. |
| `send_command(socket, command)` | Envía un comando (string) al carro. |
| `receive_data(socket)` | Recibe hasta 1024 bytes de respuesta del carro. |
| `close_socket(socket)` | Cierra la conexión con el carro. |

