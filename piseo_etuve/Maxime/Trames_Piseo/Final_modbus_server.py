import socket
import struct
import threading
import os

setpoint_temperature = 0 #Définition de la température cible initiale pour faire les tests

#Fonction pour convertir de float à 2 registres 
def float_to_modbus_registers(value):
    #Convertir la valeur de float à bytes (little endian)
    float_bytes = struct.pack('<f', value)
    #Diviser les 4 octets en deux entiers de 2 octets 
    reg1, reg2 = struct.unpack('<HH', float_bytes)
    return reg1, reg2
#Fonction pour convertir 2 registres en float
def modbus_registers_to_float(reg1, reg2):
    #Combine les deux entiers de 2 octets en 4 octets
    float_bytes = struct.pack('<HH', reg1, reg2)
    #Convertir les 4 octets en une valeur float
    value = struct.unpack('<f', float_bytes)[0]
    return value

#Fonction pour gérer la connexion d'un client 
def handle_client_connection(client_socket):
    global setpoint_temperature
    while True:
        #Boucle pour recevoir des requêtes du client
        request = client_socket.recv(1024)
        if not request:
            break

        # Décomposer l'entête modbus TCP de la requête
        transaction_id, protocol_id, length, unit_id, function_code, start_address, count_or_byte_count = struct.unpack('>HHHBBHH', request[:12])
        #Si le code de fonction est 4, c'est une lecture 
        if function_code == 4:  
            # Demande de lecture de la température actuelle (4306)
            if start_address == 0x10D2:  
                #On met en dur une valeur pour faire des tests
                """
                with open(os.path.dirname(os.path.realpath(__file__))+"\\temp.txt","r") as f:
                    temperature_actuelle = float(f.readline())
                """
                temperature_actuelle = setpoint_temperature
                #Préparation des données de la température actuelle
                data = struct.pack('>HH', *float_to_modbus_registers(temperature_actuelle))
            #Lecture de la température cible (4274)
            elif start_address == 0x10B2:  
                #Préparation des données de la température cible
                data = struct.pack('>HH', *float_to_modbus_registers(setpoint_temperature))
            #Calcul de la longueur de la réponse
            length = 3 + len(data)
            #Construction de la réponse
            response = struct.pack('>HHHBB', transaction_id, protocol_id, length, unit_id, function_code) + struct.pack('B', len(data)) + data

        # 16 = Écriture de plusieurs registres 
        elif function_code == 16:  
            # Écriture du setpoint de température (4306)
            if start_address == 0x114C:  
                #Obtenir le compte d'octets directement depuis la requête
                byte_count = request[12]  
                # Decomposer les valeurs des registres depuis la requête
                reg_values = struct.unpack('>HH', request[13:17])
                #Mettre à jour la température cible avec la valeur convertie de registres à float
                setpoint_temperature = modbus_registers_to_float(reg_values[0], reg_values[1])  
                #Construction de la réponse
                response = struct.pack('>HHHBBHH', transaction_id, protocol_id, 6, unit_id, function_code, start_address, 2)
            else:
                continue #Si l'adresse ne correspond pas, ignorer la requête
        else:
            continue #Si code de fonction ne correspond pas, ignorer la requête
        #Envoyer la réponse au client
        client_socket.send(response)

#Fonction pour démarrer la fausse étuve
def start_modbus_tcp_server(host, port):
    #Création du socket TCP/IP
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #Liaison du socket au port et à l'adresse IP hôte
    server.bind((host, port))
    #Mettre la fausse étuve en écoute pour les connexions entrantes
    server.listen(5)
    print(f"Listening on {host}:{port}")
    
    try:
        while True:
            # Accepter les nouvelles connexions
            client_sock, address = server.accept()
            print(f"Accepted connection from {address[0]}:{address[1]}")
            #Création d'un nouveau thread pour gérer la connexion du client
            client_handler = threading.Thread(target=handle_client_connection, args=(client_sock,))
            client_handler.start()
    finally:
        #Fermer le serveur en cas d'interruption
        server.close()

if __name__ == "__main__":
    #Adresse de connexion
    HOST = socket.gethostbyname(socket.gethostname())
    #Port de connexion
    PORT = 502
    #Démarre le serveur avec le port / ip qu'on lui a attribué
    start_modbus_tcp_server(HOST, PORT)