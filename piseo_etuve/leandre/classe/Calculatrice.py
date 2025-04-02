class Calculatrice :
    
    from math import exp
    import time as time
    import json
    from Queue import Queue
    import os
    import sys
    sys.path.append(os.path.dirname(os.path.realpath(__file__))+"/../../Maxime/Trames_Piseo/") 
    from CEtuve import Etuve
    sys.path.append(os.path.dirname(os.path.realpath(__file__))+"/../")
    import configLecter
    
    infos = dict
    pathToJson = str
    verif = Queue
    etuve = Etuve
    
    def __init__(self):
        pass

    def calcul(self,temp:float,second:float,since:float,base:float,type:int=0,fonction:str=""):
        #Fais le calcul de température actuelle en fonction de trois type de fonction.
        if type == 0 :
                case1 = ((temp-base)/second)*(self.time.time() - since)+base < temp and base < temp
                case2 = ((temp-base)/second)*(self.time.time() - since)+base > temp and base > temp
                if case1 or case2: #Fonction Affine
                    return ((temp-base)/second)*(self.time.time() - since)+base 
                else:
                    return  temp
        elif type == 1 :
                return ((temp - base) * (1 - self.exp(-(self.time.time() - since)/(second/7)))) + base #Fonction logarithme
        elif type == 2 :
                return fonction
            
    def api(self):
        """Récupère la configuration du .env"""
        self.infos = self.configLecter.set(self.os.path.dirname(self.os.path.realpath(__file__))+"/../../")
        """Chemin vers le data.json"""
        self.pathToJson = self.os.path.dirname(self.os.path.realpath(__file__)) + "/data.json"    
        with open(self.pathToJson,'w',encoding='utf8') as file:
            """Initialise le fichier data.json"""
            file.write("{\"temperature\":0,\"second\":0,\"since\":0,\"base\":0,\"type\":0,\"done\":true,\"host\":\"0.0.0.0\",\"port\":0}")
            file.close
        self.verif = self.Queue(self.infos["queueLenght"])
        while True:
            with open(self.pathToJson,'r',encoding='utf8') as file: #Lis les données dans le data.json
                data = self.json.loads(file.read())
            if data['done'] == False: # Vérifie si il y a une consigne non finie
                self.etuve = self.Etuve(data['host'],data['port'])
                currentTemperature =  self.calcul(data['temperature'],data['second'],data['since'],data['base'],data['type'])
                #Calcul la valeur actuelle de température qu'il faut donner à l'étuve.
                self.verif.append(float(format(self.etuve.readTemperature(),'.2f')))
                self.etuve.setTemperature(currentTemperature) #Envoie de la température à l'étuve.
                if self.verif.delta(data['temperature']) and len(self.verif.data) == self.verif.limit and self.time.time() > data['second'] + data['since']: #Si toutes les valeurs de la queue sont proches de la valeur finale
                    self.etuve.setTemperature(data['temperature']) # alors on met l'étuve à la température finale
                    with open(self.pathToJson,'w',encoding='utf8') as file: # Et on marque dans data.json que la consigne est finie
                        file.write("{\"temperature\":%s,\"second\":%s,\"since\":%s,\"done\":true,\"base\":%s,\"host\":\"%s\",\"port\":%s}" % (data['temperature'],data['second'],data['since'],data['base'],data['host'],data['port']))
                del self.etuve
            self.time.sleep(float(self.infos["sleep"]))


if __name__ == "__main__":
    calcul = Calculatrice()
    calcul.api()