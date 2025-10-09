"""IP	La dirección de la casa
Puerto	La puerta específica de la casa
Cliente	Invitado que llama a la puerta
Servidor	Persona que abre la puerta y recibe al invitado"""


import socket #enchufe virtual 
import select #para monitorear multiples sockets

IP_LOCAL= '127.0.0.1' #solo mi computadora
PUERTO = 5000  # un canal de comunicación específico dentro de una computadora.

#asociamos (ipv4 + tcp un protocolo confiable que me garantiza seguridad
# y que los mensajes me llegue en orden)
servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#configuramos el servidor para que trabaje por si mismo y se reuse el ip y el puerto despues de cerrar el servidor
servidor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )

#hacemos que nuestro servidor pueda escuchar nuevas clonexiones con una ip y un puerto 
servidor_socket.bind((IP_LOCAL, PUERTO))

#ponemos nuestro servidor en modo escucha
servidor_socket.listen()


lista_de_sockets = [servidor_socket]  # lista de sockets a monitorizar
clientes = {}  #  nombre de usuario (opcional)


print(f"Servidor escuchando en {IP_LOCAL}: {PUERTO}...")

def difundir_en_chat(mensaje, socket_excluido=None):
    # Para cada cliente conectado
    for cliente_socket in clientes:
        # Si este cliente no es el que envió el mensaje
        if cliente_socket != socket_excluido:
            try:
                #mandamos los bytes del cliente al chat
                cliente_socket.send(mensaje)
            except:
                # Si falla, cerrar la conexión de este cliente
                cliente_socket.close()
                # Sacarlo de la lista de sockets que monitoreamos
                lista_de_sockets.remove(cliente_socket)
                # Eliminarlo del registro de clientes
                del clientes[cliente_socket]

while True:
    try:
        sockets_listos, _, sockets_problematicos = select.select(lista_de_sockets, [], lista_de_sockets) #revisar los que tienen datos para leer y los que tienen errores
        
        #iterar por todos los sockets listos
        for socket_notificado in sockets_listos:
            #para los que se quieren conectar
            if socket_notificado == servidor_socket: # Si el socket listo es el servidor, significa que un nuevo cliente quiere conectarse
                nuevo_cliente, direccion_del_cliente = servidor_socket.accept()
                nuevo_cliente.send("Bienvenido! Escribí tu nombre de usuario: ".encode('utf-8'))
                lista_de_sockets.append(nuevo_cliente)
                clientes[nuevo_cliente] = None  #el nombre aun no lo sabemos
            
            # Procesamos mensajes de clientes ya conectados
            else:
                try:
                    mensaje = socket_notificado.recv(1024)
                    if not mensaje:
                        #el cliente se desconecto si no hay mensaje
                        nombre = clientes[socket_notificado] or str(socket_notificado)
                        print(f"cliente {nombre} se deconecto! ")
                        #lo sacamos de la lista de sockets
                        lista_de_sockets.remove(socket_notificado)
                        del clientes[socket_notificado]
                        continue
                    #revisamos si el cliente aun no tiene nombre 
                    if clientes[nuevo_cliente] is None:
                        #cambiamos a string los bytes
                        nombre = mensaje.decode('utf-8').strip()
                        clientes[socket_notificado] = nombre
                        socket_notificado.send(f"¡Hola {nombre}! Ahora podés enviar mensajes.".encode('utf-8'))
                        difundir_en_chat(f"{nombre} se unió al chat.".encode('utf-8'), quien_envio=socket_notificado)
                        print(f"{nombre} se conectó desde {socket_notificado.getpeername()}")
                    else:
                        #ya esta conectado al chat y ya tiene nombre
                        nombre = clientes[socket_notificado]
                        texto = mensaje.decode('utf-8').strip()
                        if texto.lower() == "salir": #para que el cliente salga
                            socket_notificado.send("Te desconectaste del chat.".encode('utf-8'))
                            lista_de_sockets.remove(socket_notificado)
                            del clientes[socket_notificado]
                            socket_notificado.close()
                            difundir_en_chat(f"{nombre} se desconectó.".encode('utf-8'))
                            print(f"{nombre} cerró la conexión")
                        else:
                            #si no se quiere salir pues sigue mandanos mensajes normales
                            difundir_en_chat(f"{nombre}: {texto}".encode('utf-8'), quien_envio=socket_notificado)
                except:
                    #si ocurre un error al recibir un mensaje o procesar mensaje
                    lista_de_sockets.remove(socket_notificado)
                    del clientes[socket_notificado]
                    continue
                # Manejo de errores
        for socket_notificado in sockets_problematicos:
            lista_de_sockets.remove(socket_notificado)
            del clientes[socket_notificado]

        # Comando del servidor para apagarlo
        comando = input()
        if comando.lower() == "salir":
            print("Servidor apagándose...")
            for sock in lista_de_sockets:
                if sock != servidor_socket:
                    sock.send("Servidor se está apagando.".encode('utf-8'))
                    sock.close()
            servidor_socket.close()
            break      
    #por si intenta salir con control c
    except KeyboardInterrupt:
        print("Servidor interrumpido manualmente.")
        for sock in lista_de_sockets:
            if sock != servidor_socket:
                sock.close()
        servidor_socket.close()
        break     
                        
    
                     
                                              
                        
                        
                        
                        
                    
                    
                        
                        
                        
                    
                    
                    
                    
                
                
                
                
                
                
            
        
        
    
        
        

