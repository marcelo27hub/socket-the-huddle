import socket
import threading

# Datos del servidor
DIRECCION_SERVIDOR = '192.168.100.86'  # La IP del servidor
PUERTO = 5000                           # Puerto por donde se conecta

# Crear socket del cliente
socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_cliente.connect((DIRECCION_SERVIDOR, PUERTO))

# Función para recibir mensajes del servidor
def recibir_mensajes():
    while True:
        try:
            mensaje = socket_cliente.recv(1024).decode('utf-8')
            if mensaje:
                print(f"\n{mensaje}\n> ", end="")
        except:
            print("Se perdió la conexión con el servidor.")
            break

# Crear un hilo para recibir mensajes en segundo plano
threading.Thread(target=recibir_mensajes, daemon=True).start()

print("Conectado al servidor. Escribe tus mensajes:")

# Bucle principal para enviar mensajes
while True:
    mensaje_a_enviar = input("> ")
    if mensaje_a_enviar.lower() == "/exit":
        break
    try:
        socket_cliente.send(mensaje_a_enviar.encode('utf-8'))
    except:
        print("No se pudo enviar el mensaje.")
        break

# Cerrar conexión
socket_cliente.close()
