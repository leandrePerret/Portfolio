import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt

window= tk.Tk()
window.title('IHM')
window.geometry('1500x850')
window.resizable(False, False)
tab_control = ttk.Notebook(window)
first_tab = ttk.Frame(tab_control)
first_canvas = Canvas(first_tab, width=1500, height=850, background="#2B2B2B")
first_canvas.pack()

temps = []
heur = []
points_rouges_x = []  # Pour stocker les coordonnées x des points qui dépassent les seuils
points_rouges_y = []  # Pour stocker les coordonnées y des points qui dépassent les seuils

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
plt.close('all')

x_values = heur
y_values = temps

current_figure, ax = plt.subplots(figsize=(10, 4.5))################################## modif taille
ax.set_facecolor('lightgray')

# Plot des points normaux
ax.plot(x_values, y_values, label='Données de test', marker='o', markersize=3, linestyle='-')

# Plot des points qui dépassent les seuils en rouge
ax.plot(points_rouges_x, points_rouges_y, 'ro',label ='Point qui dépasse le seuil')  # 'ro' pour les points rouges

ax.grid(True, linestyle='--', linewidth=0.5, color='black')
ax.set_title('Graphique Température en fonction du temps :')
ax.set_xlabel('Heure entre la première et la dernière valeur')    
ax.set_ylabel('Température en °C')
ax.set_ylim(-40, 180)
ax.legend()
ax.axhline(y=20, color='r', linestyle='--', label='Ligne horizontale')
ax.axhline(y=50, color='r', linestyle='--', label='Ligne horizontale')
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
    print("Attention: heur doit avoir au moins deux éléments pour afficher les graduations.")

# Créer un conteneur Frame pour le graphique
graphique_frame = ttk.Frame(window)########################## modifier
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
graphique_frame.place(x=480, y=30)  # Position du conteneur

window.mainloop()