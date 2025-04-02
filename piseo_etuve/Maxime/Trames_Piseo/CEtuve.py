import socket
import struct

class Etuve():
    host = str
    port = int 
   
    def __init__(self,host,port): # Initialisation des attributs host et port
        self.host, self.port = host, port 

    def __send_modbus_request_read(self, unit_id, function_code, start_address, count):
        transaction_id = 1 # id de la transaction (sert à associer requêtes et réponses entre le maitre et l'esclave)
        protocol_id = 0 # Identifiant de protocole (0 = message modbus standard)
        length = 6  # Longueur de l'entête Modbus
        header = struct.pack('>HHH', transaction_id, protocol_id, length) # Construction de l'entête
        pdu = struct.pack('>BBHH', unit_id, function_code, start_address, count)# Construction du Protocol Data Unit
        modbus_request = header + pdu # Construction de la requête Modbus complète

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: #Création du socket TCP
            s.connect((self.host, self.port)) #Connexion à l'étuve
            s.sendall(modbus_request) # Envoi de la requête Modbus
            response = s.recv(1024) # Réception de la réponse de l'étuve
        
        return response 

    def __send_modbus_request_write(self, unit_id, function_code, start_address, value):
        transaction_id = 1
        protocol_id = 0
        float_bytes = struct.pack('>f', value) # Conversion de float à bytes en format big endian
        reg2, reg1 = struct.unpack('>HH', float_bytes) # Division des bytes en 2 registres
        # On inverse les deux registres sinon les valeurs sont éronées 
        length = 11  # Longueur pour l'en-tête, l'adresse, le nombre de registres, le nombre d'octets, et les données
        header = struct.pack('>HHH', transaction_id, protocol_id, length)
        pdu = struct.pack('>BBHHBHH', unit_id, function_code, start_address, 2, 4, reg1, reg2)
        
        modbus_request = header + pdu
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host,self.port))
            s.sendall(modbus_request)
            response = s.recv(1024)
        
        return response
    
    def __parse_modbus_float_response(self,response):
        if not response or len(response) < 9: # Vérfication de la validité de la réponse 
            print("Réponse invalide ou trop courte.")
            return None

        _, _, _, _, _, byte_count = struct.unpack('>HHHBBB', response[:9]) # Extractions des premiers bytes de la réponse
        data = response[9:9+byte_count] # Extraction des données 
        
        if len(data) == 4: #Vérification de la longueur des données
            
            reg1, reg2 = struct.unpack('>HH', data[:4]) #Division des données en deux registres
            modicon_float = struct.unpack('<f', struct.pack('<HH', reg1, reg2))[0]# Conversion des registres de float en little-endian
            return modicon_float
        else:
            print("Longueur de données inattendue pour un float.")
            return None

    def readTemperature(self): # Méthode de lecture de la température actuelle
        return self.__parse_modbus_float_response(self.__send_modbus_request_read(0xFF,4,0x10D2,2))

    def readSetPoint(self): # Méthode de lecture de la température cible
        return self.__parse_modbus_float_response(self.__send_modbus_request_read(0xFF,4,0x10B2,2))
    
    def setTemperature(self,value:float): # Méthode d'écriture de la température cible
        return self.__send_modbus_request_write(0xFF, 16, 4428,value)

    