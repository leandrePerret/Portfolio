import subprocess
import os
import threading

pathToFile = os.path.dirname(os.path.realpath(__file__))
verif=subprocess.Popen(["pip", "install", "-r", "%s/../requirements.txt" % pathToFile], 
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) # Vérifie que toutes les bibliothèques soient bien installées.
verif.wait()

import configLecter



info = configLecter.set("./") # Récupère toutes les données du .env


def django():
    """Lance le serveur Django"""
    subprocess.run("python %s/apiEtuve/manage.py migrate" % pathToFile)
    subprocess.run("python %s/apiEtuve/manage.py runserver %s:%s" % (pathToFile, info["host"], info["port"]),shell=True)
djangoT = threading.Thread(target=django)
djangoT.start()

if info["api"] == "true":
    def server():
        #Si [DEBUG] API = True alors on lance un serveur modbus sur le port 502
        subprocess.run("python %s/../Maxime/Trames_Piseo/Final_modbus_server.py" % pathToFile,shell=True)
    serverT = threading.Thread(target=server)
    serverT.start()

def calcul():
    #Lance la calculatrice
    subprocess.run("python %s/classe/Calculatrice.py" % pathToFile,shell=True)
calculT = threading.Thread(target=calcul)
calculT.start()




