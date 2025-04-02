import tkinter as tk

# Créer une fenêtre
fenetre = tk.Tk()
fenetre.title("Exemple de fenêtre tkinter")

# Ajouter un label
label = tk.Label(fenetre, text="Bonjour, monde!")
label.pack()

# Ajouter un bouton
bouton = tk.Button(fenetre, text="Cliquez-moi!")
bouton.pack()

# Lancer la boucle principale
fenetre.mainloop()
