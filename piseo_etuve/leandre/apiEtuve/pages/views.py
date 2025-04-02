from django.shortcuts import render
from pyModbusTCP.client import ModbusClient
from django.core.files import File
import os
import time
import sys
import json
sys.path.append(os.path.dirname(os.path.realpath(__file__))+"\\..\\..\\..\\Maxime\\Trames_Piseo\\")
from CEtuve import Etuve
sys.path.append(os.path.dirname(os.path.realpath(__file__))+"\\..\\..\\")
import configLecter

pathToJson = os.path.dirname(os.path.realpath(__file__)) + "\\..\\..\\classe\\data.json" #Chemin vers le data.json contenant les consignes.
infos = configLecter.set(os.path.dirname(os.path.realpath(__file__))+"\\..\\..\\..\\") # Récupère les infoss du .env

def connectTo(request_iter,host,port):
    """Tente de se connecter à l'étuve demandée, en cas d'échec renvoie False"""
    try:
        global client
        client = Etuve(host,port)
        client.readSetPoint()
        return True
    except:
        return False

def index(request_iter):
    return  render(request_iter,'index.html')

def consign(request_iter,host,port,temperature,second,type=0):
    """Récupère les données consignées et les met en forme dans le data.json"""
    result = {
        "host":host,
        "port": port,
        "consignTemperature":float(temperature),
        "consignSecond":int(second),
        "type":type,
        "statut": 0,
        "message": ""
    }
    if connectTo(request_iter,host,port):
        with open(pathToJson , "w") as f:
            file = File(f)
            data = (temperature,second,time.time(),format(client.readTemperature(),'.2f'),type,host,port)
            file.write("{\"temperature\":%s,\"second\":%s,\"since\":%s,\"base\":%s,\"type\":%s,\"done\":false,\"host\":\"%s\",\"port\":%s,\"function\":\"\"}" % data)
            file.close()
            f.close()
            result["statut"]=200
            result["message"]=f"Values have been consigned on {host}:{port}"
    else:
        result["statut"]=400
        result["message"]=f"Error 400 : No server found at {host}:{port}"
    return render(request_iter,"result.html",context={"result":result,"title":"consign"})

def read(request_iter,host,port):
    """Permet de récupérer les données de l'étuve"""
    result = {
        "host":host,
        "port": port,
        "temperature":0.0,
        "consignTemperature":0.0,
        "consignSecond":0,
        "done":True,
        "statut": 0,
        "message": ""
    }
    
    if connectTo(request_iter,host,port):
            data = json.loads(open(pathToJson,'r',encoding='utf8').read())
            result["temperature"]=format(client.readTemperature(),'.2f')
            result["consignTemperature"]=data["temperature"]
            result["consignSecond"]=data["second"]
            result["done"] = data["done"]
            result["statut"]=200
            result["message"]=f"Values have been read on {host}:{port}"
    else:
        result["statut"]=400
        result["message"]=f"Error 400 : No server found at {host}:{port}"
    return render(request_iter,"result.html",context={"result":result,"title":"read"})

def readTemperature(request_iter,host,port):
    """Permet de lire la température de l'étuve"""
    result = {
        "host":host,
        "port": port,
        "temperature":0.0,
        "statut": 0,
        "message": ""
    }
    
    if connectTo(request_iter,host,port):
        result["temperature"]=format(client.readSetPoint(),'.2f')
        result["statut"]=200
        result["message"]=f"Value have been read on {host}:{port}"
    else:
        result["statut"]=400
        result["message"]=f"Error 400 : No server found at {host}:{port}"
    return render(request_iter,"result.html",context={"result":result,"title":"readTemperature"})

def readConsign(request_iter):
    """Permet de lire la consigne actuellement en cours."""
    result = {
        "host": 0,
        "port": '0.0.0.0',
        "consignTemperature":0.0,
        "consignSecond":0,
        "done":True,
        "statut": 0,
        "message": ""
    }
    
    data = json.loads(open(pathToJson,'r',encoding='utf8').read())
    result["consignTemperature"]=data["temperature"]
    result["consignSecond"]=data["second"]
    result["host"] = data["host"]
    result["port"] = data["port"]
    result["done"] = data["done"]
    result["statut"]=200
    result["message"]=f"Values have been read"
    return render(request_iter,"result.html",context={"result":result,"title":"consign"})
"""
def badConsign(request_itter):
    return render(request_itter,"result.html",context={"result":{"statut":400,"message":"URL not fine : respect consign/host/port/temperature/second"}})

def badReadConsign(request_itter):
    return render(request_itter,"result.html",context={"result":{"statut":400,"message":"URL not fine : respect readConsign/host/port/temperature/second"}})

def badReadTemperature(request_itter):
    return render(request_itter,"result.html",context={"result":{"statut":400,"message":"URL not fine : respect readTemperature/host/port/temperature/second"}})

def badRead(request_itter):
    return render(request_itter,"result.html",context={"result":{"statut":400,"message":"URL not fine : respect read/host/port/temperature/second"}})
"""
def custom_404(request, exception):
    return render(request,"result.html",context={"result":{"statut":404,"message":"Page not found, check URL"}})