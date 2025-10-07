import socket
import select
"""IP	La dirección de la casa
Puerto	La puerta específica de la casa
Cliente	Invitado que llama a la puerta
Servidor	Persona que abre la puerta y recibe al invitado"""

HOST = '0.0.0.0' #escucha todas las interfaces/ ej : calle de mi casa
#Eso quiere decir que tu servidor aceptará conexiones tanto desde localhost (127.0.0.1)
#como desde otros dispositivos de tu red local (por ejemplo, tu celular o laptop).

PORT = 5000  # un canal de comunicación específico dentro de una computadora.

#creamos un nuevo socket con socket.socket(tupla  de mi direccion socket.af_inet:
# usaremos ipv4 mi direccion, socket.sock_strem: usaremos un protocolo confiable de conexion 
# que da confiabilidad y hace que los mensajes lleguen en orden)
servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#configuramos con setcokopt las opciones del socket
#sol_socket indica que la opcion es para uno mismo
#so_reuseador permite reusar la misma dirección/IP y
# puerto inmediatamente después de cerrar el servidor.
#No tenemos que programar todo desde cero a nivel de red. 
# La API hace que el TCP/IP funcione por nosotros, con métodos simples de Python.
servidor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
#bind le dice en que ip y puerto  ya estan listo para escuchar conexiones
servidor_socket.bind((HOST, PORT))
#listem() pone el servidor en modo escucha
servidor_socket.listen()

lista_de_sockets = [servidor_socket]  # lista de sockets a monitorizar
clientes = {}  #  nombre de usuario (opcional)

print(f"Servidor escuchando en {HOST}:{PORT}...")

def difundir(mensaje, socket_excluido=None):
    # Para cada cliente conectado
    for cliente_socket in clientes:
        # Si este cliente no es el que envió el mensaje
        if cliente_socket != socket_excluido:
            try:
                # Enviar el mensaje a este cliente
                cliente_socket.send(mensaje)
            except:
                # Si falla, cerrar la conexión de este cliente
                cliente_socket.close()
                # Sacarlo de la lista de sockets que monitoreamos
                lista_de_sockets.remove(cliente_socket)
                # Eliminarlo del registro de clientes
                del clientes[cliente_socket]

while True:
    sockets_a_leer, _, sockets_con_error = select.select(lista_de_sockets, [], lista_de_sockets)
    
    for socket_notificado in sockets_a_leer:
        if socket_notificado == servidor_socket:
            socket_cliente, direccion_cliente = servidor_socket.accept()
            lista_de_sockets.append(socket_cliente)
            clientes[socket_cliente] = f"{direccion_cliente}"
            print(f"Conexión aceptada de {direccion_cliente}")
        else:
            try:
                mensaje = socket_notificado.recv(1024)
                if not mensaje:
                    # El cliente se desconectó
                    print(f"Cliente {clientes[socket_notificado]} desconectó")
                    lista_de_sockets.remove(socket_notificado)
                    del clientes[socket_notificado]
                    continue
                # Difundir mensaje a todos los demás clientes
                difundir(mensaje, socket_excluido=socket_notificado)
            except:
                lista_de_sockets.remove(socket_notificado)
                del clientes[socket_notificado]
                continue                

    # Manejar sockets con errores
    for socket_notificado in sockets_con_error:
        lista_de_sockets.remove(socket_notificado)
        del clientes[socket_notificado]


