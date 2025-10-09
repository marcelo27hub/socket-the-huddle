import socket #enchufe virtual
import threading #para que corrar mas programas (hilos)
import time

# Datos del servidor
DIRECCION_SERVIDOR = '127.0.0.1'  # La IP del servidor
PUERTO = 5000                           # Puerto por donde se conecta

def conectar(): #conectar con el servidor 
    while True:#bucle para que se intente una y mas veces
        try:
            # Creamos un socket y nos conectamos al servidor usando su IP y puerto
            socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_cliente.connect((DIRECCION_SERVIDOR, PUERTO))
            print("Conectado al servidor.")
            return socket_cliente
        except:
            #si hay un error o se fue a donde no se el clinte le damos unos segundos para que se intente conectar
            print("No se pudo conectar al servidor, reintentando en 3 segundos...")
            time.sleep(3)

def recibir_mensajes(socket_cliente): #canal donde llegan los datos desde el servidor
    while True: # correra todo el tiempo 
        try:
            mensaje = socket_cliente.recv(1024).decode('utf-8') #convertinos los mensajes de bytes a string 
            if mensaje:
                print(f"\n{mensaje}\n> ", end="") #si envia un mensaje en la siguiente linea le aparece (>) para que siga enviando 
            else:
                #si no envio nada le cerramos la conexion
                print("\nConexión cerrada por el servidor.")
                socket_cliente.close()
                break
        except:
            #si no hay luego ni un mensaje 
            #le cerramos el servidor
            print("\nSe perdió la conexión con el servidor.")
            socket_cliente.close()
            break
#conectar al cliente
socket_cliente = conectar()
# Abrimos un hilo en segundo plano que estará recibiendo mensajes del servidor
# Esto permite que el cliente pueda enviar mensajes mientras escucha los que llegan
# daemon=True asegura que el hilo termine automáticamente si cerramos el programa principal
threading.Thread(target=recibir_mensajes, args=(socket_cliente,), daemon=True).start()

# Primer input: nombre de usuario
nombre = input(socket_cliente.recv(1024).decode('utf-8') + "> ")
socket_cliente.send(nombre.encode('utf-8'))

while True:#un bucle para que esto corra
    mensaje_a_enviar = input("> ") #lo que escriba el cliente se guarda aca
    # Si el usuario escribe "/salir", avisamos al servidor y cerramos la conexión
    if mensaje_a_enviar.lower() == "/salir":
        socket_cliente.send(mensaje_a_enviar.encode('utf-8'))
        break
    #manejo de errores
    try:
        #si no se quiere salir enviamos en bytes los mensajes al servidor
        socket_cliente.send(mensaje_a_enviar.encode('utf-8'))
    except:
        #si hay un error  o no envio un mensaje el cliente intenta conectarse nuevamente
        print("No se pudo enviar el mensaje, intentando reconectar...")
        socket_cliente = conectar()
        socket_cliente.send(nombre.encode('utf-8'))
#cerramos todo por que salio el cliente
socket_cliente.close()