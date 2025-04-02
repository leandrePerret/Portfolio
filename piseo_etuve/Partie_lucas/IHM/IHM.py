from tkinter import *
from tkinter import ttk
# from CEtuve import Etuve
import tkinter as tk 
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import time
from tkinter import Text
from tkinter import filedialog
from math import cos, sin, pi
from tkinter import messagebox
import sys
import os
from threading import Thread
#sys.path.append(os.path.dirname(os.path.realpath(__file__))+"/../../leandre/classe/")
sys.path.append(os.path.dirname(os.path.realpath(__file__))+"/../../leandre/classe/")
from Experimentation import Experimentation
from Step import Step
from Analysis import Analysis
from pathlib import Path

matplotlib.use('TkAgg')
file_path = ''
enCours = bool
Data = Experimentation()

root = tk.Tk()
root.geometry('1500x800')
root.title('PISEO')


tab_control = ttk.Notebook(root)
first_tab = ttk.Frame(tab_control)
second_tab = ttk.Frame(tab_control)


tab_control.add(first_tab, text='Accueil') #onglet acceuil
tab_control.add(second_tab, text='Historique')#Onglet Historique

tab_control.pack(expand=1, fill="both")

first_canvas = Canvas(first_tab, width=1500, height=800, background="#fefefe")
first_canvas.pack()

second_canvas = Canvas(second_tab, width=1500, height=800, background="#fefefe")
second_canvas.pack()

###############################################################################################################################
#Jauge température

class JaugeTemperature(tk.Canvas):
    
    temperature = int

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(width=300, height=200)
        self.temperature = 0



    def set_temperature(self, temperature):
        self.temperature = temperature
        self.redessinerTemp()

    def redessinerTemp(self, ):
        self.delete("jauge")
        centre_x, centre_y = 150, 150
        rayon_exterieur = 100
        rayon_interieur = 80
        angle_depart = 180  # Début de l'arc
        angle_fin = 0    # Fin de l'arc
        angle_plein = angle_depart + ((self.temperature+40) / 180) * (angle_fin - angle_depart)
        x_depart = centre_x - rayon_exterieur * cos(angle_depart * pi / 180)
        y_depart = centre_y + rayon_exterieur * sin(angle_depart * pi / 180)
        x_fin = centre_x - rayon_exterieur * cos(angle_fin * pi / 180)
        y_fin = centre_y + rayon_exterieur * sin(angle_fin * pi / 180)
        self.create_arc(centre_x - rayon_exterieur, centre_y - rayon_exterieur,
                        centre_x + rayon_exterieur, centre_y + rayon_exterieur,
                        start=angle_depart, extent=angle_fin - angle_depart, fill="lightgrey", outline="black", width=2, tags="jauge")
        self.create_arc(centre_x - rayon_exterieur, centre_y - rayon_exterieur,
                        centre_x + rayon_exterieur, centre_y + rayon_exterieur,
                        start=angle_depart, extent=angle_plein - angle_depart, fill="red", outline="black", width=2, tags="jauge")
        self.create_arc(centre_x - rayon_interieur, centre_y - rayon_interieur,
                        centre_x + rayon_interieur, centre_y + rayon_interieur,
                        start=angle_depart, extent=angle_fin - angle_depart, fill="lightgrey", outline="black", width=2, tags="jauge")

        self.create_line(centre_x, centre_y, x_depart, y_depart, fill="black", width=2, tags="jauge")
        self.create_line(centre_x, centre_y, x_fin, y_fin, fill="black", width=2, tags="jauge")
    
jaugeTemp = JaugeTemperature(first_canvas)
    
def main():
        global current_figure
        Temperature = float("{:.2f}".format(Data.temperature))
        print(Temperature)
        tempFinale = Temperature * (180/220) + (180/220*40) #32.72
        jaugeTemp = JaugeTemperature(first_canvas)   # Crée la jauge dans first_canvas
        jaugeTemp.set_temperature(tempFinale)  # Température initiale (-40°C)
        first_canvas.create_window(1350, 700, window=jaugeTemp)  # Place la jauge dans first_canvas
        # températureJauge
        tempJauge_label = ttk.Label(text= str(float(format(float(Temperature),'2f'))) + ' C°')
        tempJauge_label.pack()
        first_canvas.create_window(1230, 625, window=tempJauge_label)
        current_figure = plt.figure(figsize=(8, 4.5), num=1, clear=True)# modif taille
# Ajout de la jauge de temperature dans first_canvas
main()

#################################################################################################################################
#fichie

NameFile = ttk.Label(
    root,
    text='Fichier ouvert : Aucun'
    )

###############################################################################################################
#bouton explorateur de fichier et affichage du fichier selectionné
def explo():
    global file_path
    file_path = filedialog.askopenfilename()
    NameFile.config(text='Fichier ouvert : ' + file_path)


imageDossier = Image.open(os.path.dirname(os.path.realpath(__file__))+"/Image/dossier2.jpg")
imageDossierRedimentionner = imageDossier.resize((50,50))
image_tkC = ImageTk.PhotoImage(imageDossierRedimentionner)
ExplorateurBt= ttk.Button(root,image=image_tkC,command=explo)
ExplorateurBt.pack(pady=20)

########################################################################################################################################
#bouton ajouter
temp_defaut = 20
duree_defaut = 5
def popup_add():
    pop = Toplevel(root)
    pop.geometry("200x250")
    pop.title("Ajouter")



    # température
    temp_label = ttk.Label(pop, text="Température cible : ")
    temp_label.pack()

   
    temp_entry = ttk.Entry(pop)
    temp_entry.pack(pady= 20)
    temp_entry.focus()
    temp_entry.insert(0,temp_defaut)
    

    # Durée
    duree_label = ttk.Label(pop, text="Durée cible")
    duree_label.pack()

    duree_entry = ttk.Entry(pop)
    duree_entry.pack(pady= 20)
    duree_entry.insert(0,duree_defaut)

    
    # boutton appliquer 
    def apply():
        print('la temp est : ',temp_entry.get(),'C°')
        print('la durée est : ',duree_entry.get() , 'min')
        Tableau.param(temp_entry.get(), duree_entry.get())
        Data.appendStep(Step(temperature=float(temp_entry.get()),until=float(duree_entry.get())*60,file={"path":file_path,"command":"","argument":"","type":False}))
        pop.destroy()
        majTable(Tableau)
        
    apply_button = ttk.Button(pop, text="Appliquer", command= apply)
    apply_button.pack(pady= 20)



##########################################################################################################################################
#modifier
# Ajoutez cette fonction à votre code existant
def modifier_dernier_element(monTableau):
    if monTableau.data:
        dernier_pas = monTableau.data[-1]  # Récupère le dernier élément du tableau Data.steps
        pop = Toplevel(root)
        pop.geometry("200x250")
        pop.title("Modifier dernier élément")

        # température
        temp_label = ttk.Label(pop, text="Nouvelle température cible : ")
        temp_label.pack()

        temp_entry = ttk.Entry(pop)
        temp_entry.pack(pady=20)
        temp_entry.focus()


        # Durée
        duree_label = ttk.Label(pop, text="Nouvelle durée cible (en min) : ")
        duree_label.pack()

        duree_entry = ttk.Entry(pop)
        duree_entry.pack(pady=20)

        # Fonction d'application des modifications
        def apply():
            print('Nouvelle température :', temp_entry.get(), 'C°')
            print('Nouvelle durée :', duree_entry.get(), 'min')
            dernier_pas.temperature = float(temp_entry.get())
            dernier_pas.until = float(duree_entry.get()) * 60
            pop.destroy()

        apply_button = ttk.Button(pop, text="Appliquer", command=apply)
        apply_button.pack(pady=20)
    else:
        print("Le tableau est vide, impossible de modifier le dernier élément.")




    
# Zone etpapes
etape_background = first_canvas.create_rectangle(10, 10, 450, 600, fill="#D8D8D8" )
# Zone config
config_background = first_canvas.create_rectangle(15, 15, 445, 45, fill="#A9A9A9" )
#label partie config
label_conf = Label(text="Partie Configuration", background="#A9A9A9")
first_canvas.create_window(230, 30, window=label_conf)

#label tolerance
label_tolerance = Label(text="Tolerance \nTemperature", background="#D8D8D8")
first_canvas.create_window(75, 70, window=label_tolerance)

#zone de saisie tolerance
tolerance_defaut = 0.5
tolerance_entry = ttk.Entry(first_canvas)
tolerance_entry.pack()
tolerance_entry.insert(0,tolerance_defaut)
first_canvas.create_window(85, 100, window=tolerance_entry)

#label adresse
label_ip = Label(text="Adresse IP", background="#D8D8D8")
first_canvas.create_window(230, 70, window=label_ip)

#zone de saisie adresse ip
ip_default = "172.17.100.108"
adresse_entry = ttk.Entry(first_canvas)
adresse_entry.pack()
adresse_entry.insert(0,ip_default)
first_canvas.create_window(225, 100, window=adresse_entry)

#label port
label_port = Label(text="Port", background="#D8D8D8")
first_canvas.create_window(355, 70, window=label_port)

#zone de saisie port
port_default = 502
port_entry = ttk.Entry(first_canvas)
port_entry.pack()
port_entry.insert(0,port_default)
first_canvas.create_window(365, 100, window=port_entry)

# Création du bouton ajouter
bt_add = ttk.Button(root, text="Ajouter", command=popup_add)
bt_add.pack(pady=20)

########################################################################################################################################
#bouton supprimer

def delete():
    Tableau.suppr()
    Data.popStep()
    majTable(Tableau)

# Création du bouton
bt_suppr = ttk.Button(root, text="Supprimer", command=delete)
bt_suppr.pack(pady=20)

########################################################################################################################################
#bouton importer

def importer():
    try :
        Data.importData()
        Tableau.reset()
        if Data.dataStep:
            for values in Data.dataStep:
                Tableau.param(values.temperature, format(float(values.until)/60,".2f"))
            majTable(Tableau)
    except:
        pass

# Création du bouton importer
bt_import = ttk.Button(root, text="Importer", command= importer)
bt_import.pack(pady=20)


########################################################################################################################################
#bouton modifier 

def modifier():
    modifier_dernier_element()

# Création du bouton modifier
bt_modif = ttk.Button(root, text="Modifier", command= modifier)
bt_modif.pack(pady=20)

########################################################################################################################################
#bouton exporter

def Enregistrer():
    Data.exportData()
    

# Création du bouton enregistrer
bt_enregistrer = ttk.Button(root, text="Enregistrer", command= Enregistrer)
bt_enregistrer.pack(pady=20)

########################################################################################################################################

#bouton connexion

def Connexion():
    pass
    

# Création du bouton connexion
bt_Connect = ttk.Button(root, text="Connexion à l'étuve", command= lambda: Data.setEtuve(str(adresse_entry.get()),int(port_entry.get())))
bt_Connect.pack(pady=20)
#######################################################################################################################################
#label port
label_EtatConnxion = Label(text="Étuve non connectée", background="#D8D8D8", fg="red")
first_canvas.create_window(1350, 550, window=label_EtatConnxion)

#######################################################################################################################################
#tableau
class Table(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.data = []
        self.widgets = []
        self.create_table()

    def param(self, param_temp, param_duree):
        self.data.append([(param_temp, 'C°'), (param_duree, 'min')])
        self.create_table()

    def suppr(self):
        if self.data:
            for widget in self.widgets[-2:]:  # Supposer toujours 2 widgets par ligne
                widget.destroy()
            self.widgets = self.widgets[:-2]
            self.data.pop()
            print("Dernier élément supprimé")
            print("Element restant : ", self.data)
        else:
            print("Le tableau est vide.")
    
    def reset(self):
        while self.data:
            for widget in self.widgets[-2:]:  # Supposer toujours 2 widgets par ligne
                widget.destroy()
            self.widgets = self.widgets[:-2]
            self.data.pop()
    # def modif(self):
        


    def create_table(self):
        # Suppression de tous les widgets existants pour une reconstruction propre
        for widget in self.widgets:
            widget.destroy()
        self.widgets = []
        
        # Création du tableau
        for i, row in enumerate(self.data):
            row_widgets = []
            for j, value in enumerate(row):
                label = tk.Label(self, text=value, borderwidth=1, relief="solid", width=12, font=20)
                label.grid(row=i, column=j, padx=5, pady=5)
                row_widgets.append(label)
            self.widgets.extend(row_widgets)
    

  
Tableau = Table(first_canvas)
Tableau.pack()
first_canvas.create_window(215, 250, window=Tableau )

#######################################################################################################################################

class Chrono(tk.Frame):
    TempReel = []
    DureeReel = []
    inProgress = bool
    def __init__(self):
        super().__init__()
        
        self.temps_debut = 0

        self.label_temps = tk.Label(self, text="00:00:00", font=("Helvetica", 24))
        self.label_temps.pack(pady=10)

        self.LancerExp = ttk.Button(root,text='     Lancer\nl\'expérience',command=self.LancerExperience, width= 40)
        first_canvas.create_window(600, 500, window=self.LancerExp)
        threadForVerif = Thread(target=self.verif)
        threadForVerif.start()
        self.inProgress = False
    # start & stop
    
    def LancerExperience(self):

            if not Data.inProgress and not self.inProgress:
                Data.setEtuve(str(adresse_entry.get()),int(port_entry.get()))
                if not Data.isConnect():
                    messagebox.showerror('Erreur avec l\'étuve', 'Pas d\'étuve connectée à l\'host et port indiqués')
                    return
                self.TempReel = []
                self.DureeReel = []
                self.temps_debut = time.time()
                Data.inProgress = True
                self.inProgress = True
                Data.fileToLaunch = file_path
                Data.launchExperimentation()
                self.LancerExp.config(text='    Annuler \nl\'expérience')
                bt_add.config(state='disabled')
                bt_modif.config(state='disabled')
                bt_suppr.config(state='disabled')
                bt_import.config(state='disabled')
                bt_enregistrer.config(state='disabled')
                bt_Connect.config(state='disabled')
                port_entry.config(state= 'disabled')
                adresse_entry.config(state= 'disabled')
                tolerance_entry.config(state= 'disabled')
                self.label_temps.config(text="00:00:00")
                self.update_chrono()
            else:
                Data.inProgress = False
                self.inProgress = False
                self.LancerExp.config(text='     Lancer\nl\'expérience')
                bt_add.config(state='normal')
                bt_modif.config(state='normal')
                bt_suppr.config(state='normal')
                bt_import.config(state='normal')
                bt_enregistrer.config(state='normal')
                bt_Connect.config(state='normal')
                port_entry.config(state= 'normal')
                adresse_entry.config(state= 'normal')
                tolerance_entry.config(state= 'normal')
                self.temps_debut = 0
                #enCours = FALSE
        
    def verif(self):
        while Data.execution:
            if self.inProgress:
                while Data.inProgress and Data.execution:
                    time.sleep(1)
                if self.LancerExp.cget('text') !='     Lancer\nl\'expérience':
                    self.LancerExperience()
            time.sleep(1)


    #update crhono toute les secondes
    def update_chrono(self):
#        if enCours:
        if Data.inProgress:
            temps_actuel = time.time() - self.temps_debut
            heures = int(temps_actuel // 3600)
            minutes = int((temps_actuel % 3600) // 60)
            secondes = int(temps_actuel % 60)
            temps_format = f"{heures:02d}:{minutes:02d}:{secondes:02d}"
            self.label_temps.config(text=temps_format)
            self.after(1000, self.update_chrono)
            temp = float(format(float(Data.temperature),'2f'))
            #temp = (int)(Path(os.path.dirname(os.path.realpath(__file__))+"/../temperature.txt").read_text())
            self.TempReel.append(temp)
            self.DureeReel.append(temps_actuel/60)
            majTableReel(self.DureeReel,self.TempReel)


#afficher pipo
pipo = Chrono()
pipo.pack()
first_canvas.create_window(600, 400, window=pipo)




########################################################################################################################################
#mise en page
first_canvas.create_window(75, 700, window=ExplorateurBt)
first_canvas.create_window(175, 675, window=NameFile)
first_canvas.create_window(100, 575, window=bt_add)
first_canvas.create_window(350, 575, window=bt_suppr)
first_canvas.create_window(225, 575, window=bt_modif)
first_canvas.create_window(275, 625, window=bt_import)
first_canvas.create_window(150, 625, window=bt_enregistrer)
first_canvas.create_window(225, 150, window=bt_Connect)

#image piseo
img= Image.open(os.path.dirname(os.path.realpath(__file__))+"/Image/piseo.png")
resize_imageB = img.resize((250, 125)) #redimentionner 
imgB = ImageTk.PhotoImage(resize_imageB)
imgPiseo=tk.Label(root,image=imgB, width=250,height=125,background="#2B2B2B", border=0)
imgPiseo.pack()
first_canvas.create_window(600, 80, window=imgPiseo)

#image ort
img= Image.open(os.path.dirname(os.path.realpath(__file__))+"/Image/ort.png")
resize_imageC = img.resize((250, 150)) #redimentionner 
imgC = ImageTk.PhotoImage(resize_imageC)
imgOrt=tk.Label(root,image=imgC, width=250,height=150,background="#2B2B2B", border=0)
imgOrt.pack()
first_canvas.create_window(600, 225, window=imgOrt)

########################################################################################################################################
#graph

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt




temps = []
heur = []
points_rouges_x = []  # Pour stocker les coordonnées x des points qui dépassent les seuils
points_rouges_y = []  # Pour stocker les coordonnées y des points qui dépassent les seuils
x_values = []
y_values = []
x_Reel = []
y_Reel = []
# for i in range(len(data_temp)): 
#     temps.append(data_temp[i]["temp"])
#     timestamp = datetime.strptime(data_temp[i]["Heure"], "%d/%m/%Y %H:%M:%S")
#     heure_seulement = timestamp.strftime("%H:%M:%S")
#     heur.append(heure_seulement)
    
#     # Vérifier si la température dépasse les seuils
#     if data_temp[i]["temp"] > seuil_temp_max or data_temp[i]["temp"] < seuil_temp_min:
        # points_rouges_x.append(heure_seulement)
        # points_rouges_y.append(data_temp[i]["temp"])

# Fermer la figure précédente s'il y en a une
#plt.close('all')

def majTable(leTableau):
    Temps = 0
    x_values.clear()
    y_values.clear()
    x_values.append(0)
    y_values.append(0)

   
    for i in range(len(leTableau.data)):
        if (Data.queueLenght * Data.timeToRead) > Data.stabilityTerm:
            Temps = Temps + (float)(leTableau.data[i][1][0]) + Data.queueLenght * Data.timeToRead / 60
        else:
            Temps = Temps + (float)(leTableau.data[i][1][0]) + Data.stabilityTerm / 60
        #temps *60 car le graphique affiche des minute et le fichier des secondes
        x_values.append(Temps)
        y_values.append((float)(leTableau.data[i][0][0]))
        traceTable()

def majTableReel(DureeTable, TemperatureTable):
    x_Reel.clear()
    y_Reel.clear()
    for i in range(len(DureeTable)):
        x_Reel.append((float)(DureeTable[i]))
    for i in range(len(TemperatureTable)):
        y_Reel.append(TemperatureTable[i])
    traceTable()

def traceTable():
    current_figure.clf()
    ax = current_figure.add_subplot()
    # x_values = [15,30,50,60]
    # y_values = [10,82,132,45]

    # x_Reel = [12,30,45,52]
    # y_Reel = [15.2,18.6,62.9,132.5]

    
    ax.set_facecolor('lightgray')

    # Plot des points normaux
    toto = ax.plot(x_values, y_values, label='Données de prévision', marker='x', markersize=5, linestyle='-')

    # Plot réel
    ax.plot(x_Reel, y_Reel, label='Données réelle', marker='o', markersize=5, linestyle='-')

    # Plot des points qui dépassent les seuils en rouge
    ax.plot(points_rouges_x, points_rouges_y, 'ro',label ='Point qui dépasse le seuil')  # 'ro' pour les points rouges

    ax.grid(True, linestyle='--', linewidth=0.5, color='black')
    ax.set_title('Graphique Température en fonction du temps :')
    ax.set_xlabel('Temps en minute')
    ax.set_ylabel('Température en °C')
    ax.set_ylim(-40,180)
    ax.legend()
    # ax.axhline(y=20, color='r', linestyle='--', label='Ligne horizontale')
    # ax.axhline(y=50, color='r', linestyle='--', label='Ligne horizontale')
    ax.fill_between(x_values, y_values, color='#DCEEF9', label='Zone sous la courbe')
    # Afficher l'heure à côté des points rouges
    for i in range(len(points_rouges_x)):
        ax.annotate(f"{points_rouges_x[i]}", (points_rouges_x[i], points_rouges_y[i]), textcoords="offset points", xytext=(-10,10), ha='center')

    # Afficher seulement la première et la dernière valeur sur l'axe des x
    if len(heur) >= 2:
        x_ticks = [heur[0], heur[-1]]
        ax.set_xticks(x_ticks)
        ax.set_xticklabels([f'{heur[0]}', f'{heur[-1]}'])
    else:
        pass

    # Créer un conteneur Frame pour le graphique
    graphique_frame = ttk.Frame(first_canvas)
    graphique_frame.pack()

    # Ajouter le graphique à l'interface Tkinter dans le Frame
    canvas = FigureCanvasTkAgg(current_figure, master=graphique_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Ajouter une barre d'outils pour le graphique
    toolbar = NavigationToolbar2Tk(canvas, graphique_frame)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    # Positionner le conteneur Frame avec le graphique et la barre d'outils
    graphique_frame.place(x=750, y=10)  # Position du conteneur

traceTable()

#############################################################################################################################################

def jauge():
    while Data.execution:
        main()
        if Data.isConnect():
            label_EtatConnxion.config(text="Étuve connectée", fg="green")
        else:
            label_EtatConnxion.config(text="Étuve non connectée", background="#D8D8D8", fg="red")
        time.sleep(1)

threadJauge = Thread(target=jauge)
threadJauge.start()

        
root.mainloop()
Data.close() # Fin du programme, extinction des threads