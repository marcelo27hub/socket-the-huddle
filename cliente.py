import socket #enchufe virtual
import threading #para que corrar mas programas (hilos)
import time

# Datos del servidor
DIRECCION_SERVIDOR = '127.0.0.1'  # La IP del servidor
PUERTO = 5000 # Puerto por donde se conecta
#el cliente aun no tiene nombre
nombre_usuario = None

def conectar(intentos = 3): #conectar con el servidor 
    for intentos in range(1, intentos + 1):
        try:
            # Creamos un socket y nos conectamos al servidor usando su IP y puerto
            socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_cliente.connect((DIRECCION_SERVIDOR, PUERTO))
            print("Conectado al servidor.")
            return socket_cliente
        except:
            #si hay un error o se fue a donde no se el clinte le damos unos segundos para que se intente conectar
            print("No se pudo conectar al servidor, reintentando en 2 segundos...")
            time.sleep(2)

def recibir_mensajes(socket_cliente): #canal donde llegan los datos desde el servidor
    while True: # correra todo el tiempo 
        try:
            mensaje = socket_cliente.recv(1024).decode('utf-8') #convertinos los mensajes de bytes a string 
            if not  mensaje:
                print("\n Conexion cerrada por el servidor") #si envia un mensaje en la siguiente linea le aparece (>) para que siga enviando 
                break           
            if "Servidor se está apagando" in mensaje:
                print("\n El servidor se apagó. Cerrando cliente...")
                break
            print(f"{mensaje}")  # cada mensaje ya tiene salto de línea
        except:
            print("\n Se perdió la conexión con el servidor.")
            break
    try:
        socket_cliente.close()
    except:
        pass
while True:    
    #conectar al cliente
    socket_cliente = conectar()
    if not socket_cliente:
        break

    #primer input: nombre de usuario solo si no tiene
    if not nombre_usuario:
        mensaje_bienvenida = socket_cliente.recv(1024).decode('utf-8')
        print(mensaje_bienvenida)  # mostrar la bienvenida separada
        nombre_usuario = input().strip()
        while not nombre_usuario:
            nombre_usuario = input("Debes ingresar un nombre: ").strip()
        socket_cliente.send(nombre_usuario.encode('utf-8'))
    else:
        socket_cliente.send(nombre_usuario.encode('utf-8'))

    # Abrimos un hilo en segundo plano que estará recibiendo mensajes del servidor
    # Esto permite que el cliente pueda enviar mensajes mientras escucha los que llegan
    # daemon=True asegura que el hilo termine automáticamente si cerramos el programa principal
    threading.Thread(target=recibir_mensajes, args=(socket_cliente,), daemon=True).start()
    

    while True:#un bucle para que esto corra
        mensaje_a_enviar = input() #lo que escriba el cliente se guarda aca
        # Si el usuario escribe "/salir", avisamos al servidor y cerramos la conexión
        if mensaje_a_enviar.lower() == "/salir":
            try:
                socket_cliente.send(mensaje_a_enviar.encode('utf-8'))
                socket_cliente.close()
            except:
                pass
            opcion = input("¿Querés reconectarte? (s/n): ").strip().lower()
            if opcion != "s":
                print("👋 Cliente cerrado.")
                exit()    
            else:
                print(" Intentando reconectar...\n")
                break
                
        #manejo de errores
        try:
            #si no se quiere salir enviamos en bytes los mensajes al servidor
            socket_cliente.send(mensaje_a_enviar.encode('utf-8'))
        except:
            #si hay un error  o no envio un mensaje el cliente intenta conectarse nuevamente
            print("⚠️ Conexión perdida.")
            break