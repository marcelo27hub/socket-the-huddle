import socket
import select
"""IP	La dirección de la casa
Puerto	La puerta específica de la casa
Cliente	Invitado que llama a la puerta
Servidor	Persona que abre la puerta y recibe al invitado"""

host = '0.0.0.0' #escucha todas las interfaces/ ej : calle de mi casa
port = 5000  # un canal de comunicación específico dentro de una computadora.
