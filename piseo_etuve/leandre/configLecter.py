import os
import socket
from dotenv import load_dotenv

    
def set(path):
    """
    Récupérer le .env et retourne ses valeurs.
    """
    load_dotenv(path+".env")
    if os.getenv("HOST").lower() == "default":
        host = socket.gethostbyname(socket.gethostname()) # Si host == default alors host = ipAddress machine
    else:
        host = os.getenv("HOST")
        
    if os.getenv("PORT").lower() == "default":
        port = 5555 # Si port == default alors port = 5555
    else:
        port = os.getenv("PORT")
    return {"host":host,"port":port,"api":os.getenv("API").lower(),"django":os.getenv("DJANGO").lower(),"sleep":os.getenv("SLEEP"),"queueLenght":os.getenv("QUEUELENGHT")} #Retourne toutes les valeurs.