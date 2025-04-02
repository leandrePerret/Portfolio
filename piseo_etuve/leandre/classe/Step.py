TYPE_AUTOMATIC = 0 #Type d'étape qui n'attend rien
TYPE_USER = 1 #Type d'étape qui attend l'utilisateur
TYPE_PROGRAM = 2 #Type d'étape qui attend la fin d'un processus

class Step:
    
    idStep = int #Id de l'étape
    until = int #Temps que met l'étuve à monté à une température en seconde
    temperature = float #Température à laquelle l'étuve monte durant cette étape en °C.
    type = int #Type
    file = dict
    
    def __init__(self,idStep:int=0,until:int=0,temperature:float=0,type=0,file:dict={"path":"","command":"","argument":"","type":True}):
        self.idStep = idStep
        self.until = until
        self.temperature = temperature
        self.type = type
        self.file = file