from CEtuve import Etuve
import socket

mkbinder115 = Etuve(socket.gethostbyname(socket.gethostname()),502) #Création de l'objet mkbinder115 en indiquant l'adresse ip et le port de l'étuve en argument
#Lecture de la température cible actuelle
print("Température cible actuelle : " + str(mkbinder115.readSetPoint()))
#Lecture de la température actuelle
print("Température actuelle : " + str(mkbinder115.readTemperature()))
setpoint = float(input("Veuillez saisir la température cible que vous souhaitez atteindre: "))
mkbinder115.setTemperature(setpoint)
#Ecriture de la température cible
print("Nouvelle température cible : " + str(mkbinder115.readSetPoint()))
#Lecture à nouveau de la température cible après modification