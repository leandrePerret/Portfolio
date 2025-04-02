class Experimentation:
    
    from Step import Step
    from Analysis import Analysis
    from tkinter import filedialog
    from threading import Thread
    import subprocess
    import json
    import os
    import sys
    sys.path.append(os.path.dirname(os.path.realpath(__file__))+"/../../Maxime/Trames_Piseo/") 
    from CEtuve import Etuve
    from Queue import Queue
    import matplotlib.pyplot as plt
    import time
    from datetime import datetime
    from Calculatrice import Calculatrice
    
    __calculatrice = Calculatrice
    __connect = bool # True si connecter à une étuve
    __dataAnalysis = list # Tableau des données analysées
    dataStep = list # Tableau contenant les étapes de l'expérimentation
    __date = str # Date + heure du lancement de l'expérimentation
    __delta = float
    __etuve = Etuve # Etuve connectée
    execution = bool # Si en IHM en exécution
    __graph = plt # Graphe via la bibliothèque Pyplot
    inProgress = bool # Si l'expérimentation est en cours
    queueLenght = int
    __setPoint = float
    stabilityTerm = float
    temperature = float #Température de l'étuve
    __threadForExperimentation = Thread
    __threadForFile = Thread # Thread permettant l'exécution d'un fichier
    __threadForLecter = Thread # Thread permettant la lecture de la température    
    __timeOfStep = str # heure du lancement d'une étape
    timeToRead = float # Temps d'attente entre deux lecture de température
    __user = str # Nom de l'utilisateur
    fileToLaunch = str # Chemin vers le fichier global à exécuter  
    
    def __init__(self):
        
        self.__user = self.os.environ.get("USERNAME")
        self.__etuve = self.Etuve("172.17.100.108",502)
        self.__connect = False
        self.timeToRead = 1
        self.__threadForLecter = self.Thread(target=self.__tempLecter)
        self.__threadForLecter.start()
        self.dataStep = list()
        self.__dataAnalysis = list()
        self.inProgress = False
        self.execution = True
        self.__date = self.datetime.today().strftime('%Y/%m/%dT%H:%M:%S')
        self.__calculatrice = self.Calculatrice()
        self.__delta = 1
        self.stabilityTerm = 0
        self.queueLenght = 4
        self.__graph = self.plt
        self.temperature = 0
        
    def __tempLecter(self):
        """Méthode lisant la température toutes les self.timeToRead secondes"""
        while self.execution: # tant que l'appli s'exécute
            try :
                self.temperature = float(self.__etuve.readTemperature()) # Je lis la température
                print("Température de l'étuve : " + str(self.temperature) + "\nSetPoint actuel : " + str(self.__setPoint))
                if self.inProgress: # Si une expérimentation est en cours, je l'ajoute à mes données et je met la température de l'étuve au setPoint$
                    self.__appendAnalysis()
                    self.__etuve.setTemperature(self.__setPoint)
                self.__connect = True # Si j'y arrive je dis que l'étuve est connectée
            except:
                self.__connect = False # Sinon l'étuve n'est pas connectée
            self.time.sleep(self.timeToRead)
    
    def setEtuve(self,host:str,port:int):
        """Méthode se connectant à une étuve"""
        self.__etuve = self.Etuve(host,port)

    def isConnect(self):
        try:
            self.__etuve.readTemperature()
            return True
        except:
            return False
        
    def launchExperimentation(self,queueLenght:int=4,delta:float=1,stabilityTerm:float=0):
        self.queueLenght = queueLenght
        self.__delta = delta
        self.stabilityTerm = stabilityTerm
        self.__dataAnalysis = []
        self.__threadForExperimentation = self.Thread(target=self.__experimentation)
        self.__threadForExperimentation.start()
    
    def __experimentation(self):
        """Méthode s'occupant du déouler d'une expérimentation"""
        try :
            self.temperature = self.__etuve.readTemperature() 
            self.__connect = True
        except:
            self.__connect = False
        # Vérifie si une étuve est bien connectée et lance l'expérimentation si il y en a une
        if self.__connect:
            verif = self.Queue(self.queueLenght) # Queue permettant de vérifier la stabilité de la température
            stepList = self.dataStep.copy() # Récupération des étapes données
            self.inProgress = True # Booléan permettant de savoir si l'utilisateur à demander la fin de l'expérimentation
            while self.inProgress and self.execution: # Tant que l'expérimentation ou le programme n'est pas arrêté
                if stepList != []: # Si il reste des étapes à faire
                    verif.reset()
                    startTemp = self.__etuve.readTemperature()
                    self.__timeOfStep = self.time.time() # Récupération température, temps de base de l'étape et réinitialisation de la queue
                    while self.inProgress and self.execution and float(stepList[0].until) > (self.time.time()-self.__timeOfStep): # Tant que tout s'exécute et qu'on est dans l'étape
                        self.__setPoint = self.__calculatrice.calcul(float(stepList[0].temperature),float(stepList[0].until),self.__timeOfStep,startTemp,1)
                        verif.append(self.temperature)
                        self.time.sleep(self.timeToRead) # L'on fait le calcul de la valeur que l'on doit envoyer à l'étuve puis l'on ajoute la dernière température lue de l'étuve dans la queue
                    self.__setPoint = float(stepList[0].temperature)
                    while not (verif.delta(stepList[0].temperature,self.__delta) or len(verif.data) != verif.limit or stepList[0].until + self.stabilityTerm > (self.time.time()-self.__timeOfStep)) and self.inProgress and self.execution:
                        verif.append(self.temperature) # Tant que c'est pas stable l'on continue de vérifier la stabilité
                        self.time.sleep(self.timeToRead)
                    if self.inProgress and self.execution :
                        self.__launchFile(stepList[0].file) # Lancement du fichier
                    stepList.pop(0)
                else: # Si toutes les étapes sont faites alors fin de l'expérimentation.
                    self.__etuve.setTemperature(self.__setPoint)
                    self.inProgress = False
        else:
            return False
        
    def __launchFile(self=None,file:dict={"path":"","command":"","argument":"","type":False}):
        """
        Fonction qui permet de lancer un programme, attend la fin si c'est un python sinon n'attend rien.
        """
        file = {"path":self.fileToLaunch,"command":"","argument":"","type":False} #Récupération du fichier à ouvrir
        
        if ".py" == file["path"][-3:]:
            self.subprocess.run("python \""+file["path"]+"\" "+file["argument"], shell=True) # Ouverture en python si python
            return True
        else:
            self.subprocess.run("start \""+file["path"]+"\" "+file["argument"], shell=True) # Sinon lancement du fichier
            return True
        #En dessous c'est en cours de dev.
        """      
        if file["command"]:
            self.subprocess.run(file["command"], shell=True)
            return True
        try:
            if file["type"]:
                
                if not self.os.path.exists(self.os.path.dirname(self.os.path.realpath(__file__)) + "/test.txt"):
                    file = open(self.os.path.dirname(self.os.path.realpath(__file__)) + "/test.txt","x")
                    file.write("true")
                    file.close()
                
                if file["path"]:    
                    
                        if ".py" == file["path"][-3:]:
                            self.subprocess.run("python \""+file["path"]+"\" "+file["argument"], shell=True)
                            return True
                        else:
                            self.subprocess.run("start \""+file["path"]+"\" "+file["argument"], shell=True)
                            return True

                elif file["command"]:
                    self.subprocess.run((file["command"]))
                    
                else:
                    return "No file or command give."
                    
            else:
                if file["path"]:  
                    if ".py" == file["path"][-3:]:
                        self.subprocess.run("python \""+file["path"]+"\" "+file["argument"], shell=True)
                        return True
                    else:
                        self.subprocess.run("start \""+file["path"]+"\" "+file["argument"], shell=True)
                        return True
                            
                if file["command"]:
                    self.subprocess.run(file["command"], shell=True)
                    return True
                
            return "No file or command gived"
        
        except:
            return "Impossible to run file"
        """

    def importData(self):
        """
        Méthode qui récupère un fichier JSON et insère les données au sein des propriétés
        """
        data = self.json.loads(open(self.filedialog.askopenfilename(filetypes=[('Fichier JSON', '*.json')]),'r',encoding='utf8').read()) #Ouvre le fichier JSON
        self.__date = data["date"] # Récupère la date de l'expérimentation
        self.__dataAnalysis = []
        for values in data["analysis"]:
            self.__dataAnalysis.append(self.Analysis(values["date"],values["temperature"])) # Récupère les données analysées
            
        self.dataStep = []
        for values in data["step"]:
            self.dataStep.append(self.Step(values["idStep"],values["until"],values["temperature"],values["type"],values["file"])) # Récupère les étapes de l'expérimentation
            
    def exportData(self):
        """
        Méthode qui permet d'exporter les données sous le format JSON
        """
        file = open(self.filedialog.asksaveasfilename(filetypes=[('Fichier JSON', '*.json')],defaultextension=[".json"]),'w',encoding='utf8')
        analysis = []
        step = []
        for values in self.__dataAnalysis:
            analysis.append(values.__dict__)
        for values in self.dataStep:
            step.append(values.__dict__)
        self.json.dump({"user":self.__user,"date":self.__date,"analysis":analysis,"step":step},file,ensure_ascii=False)
        file.close()
    
    def popStep(self):
        """
        Méthode qui permet d'enlever la dernière étape mise au sein des étapes.
        """
        self.dataStep.pop(-1)
        self.__protectId()
        
    def appendStep(self,step:Step):
        """
        Méthode qui permet d'ajouter une étape au sein des étapes.
        """
        self.dataStep.append(step)
        self.__protectId()
        
    def __appendAnalysis(self):
        """
        Méthode qui permet d'ajouter une mesure de température au sein des données de mesure de température.
        """
        self.__dataAnalysis.append(self.Analysis(self.datetime.today().strftime('%Y/%m/%dT%H:%M:%S'),self.temperature))
        
    def __protectId(self):
        """
        Méthode qui permet de n'avoir jamais deux étapes avec le même ID
        """
        for i in range(len(self.dataStep)):
            self.dataStep[i].id = i
            
    def createGraph(self):
        """
        Méthode qui crée le graphe   
        """
        self.__graph.figure(figsize=(13, 6)) # Formatte la taille du graphe
        
        self.__graph.subplot(12) # Crée un premier graphe
        self.__graph.plot(self.__dataList["time"],self.__dataList["temperature"]) # Place les points de température en fonction du temps
        self.__graph.xlabel('Temps (en seconde)') # Labéllise l'axe x
        self.__graph.ylabel('Température (en °C)') # Labéllise l'axe y
        
        self.__graph.suptitle('Température et hygrométrie en fonction du temps') # Titre le graphe
    
    # NON MISE A JOUR
    
    def save(self):
        from tkinter import filedialog
        """
        Méthode qui sauvegarde le graphe au format png
        """
        
        self.__graph.savefig(filedialog.asksaveasfilename(filetypes=[('Fichier PNG', '*.png')],defaultextension=[".png"])) # Sauvegarde le graphe

    def reset(self):
        """
        Méthode qui réinitialise les propriétés de la classe
        """

        self.__dataList = [[],[],[]] 
        self.__graph = self.plt 
    
    def show(self):
        """
        Montre le graphe
        """
        self.__graph.show()
        
    def __inSecond(self,date:str):
        """
        Méthode Convertissant une date en seconde.
        Trouve le delta en seconde entre la date donnée en argument à celle du 1er Janvier 1970 via la bibliothèque 'datetime'
        """
        from datetime import datetime
        date = datetime.strptime(date, '%Y/%m/%dT%H:%M:%S')
        return (date - datetime(1970, 1, 1)).total_seconds()
    
    def close(self):
        self.execution = False