class Queue:
    """
    Liste de type queue, sa taille est définit dans le constructeur via l'attribut 'limit'.
    """
    data = []
    limit = 0
    
    def __init__(self,limit:int):
        self.limit = int(limit)
    
    def append(self,value:float):
        """Ajoute une valeur à la queue, en cas de surcharge, supprime la première."""
        if len(self.data) >= self.limit and self.limit > 0:
            for i in range(len(self.data)-1):
                self.data[i] = self.data[i+1]
            self.data.pop()
            self.data.append(value)
        else:
            self.data.append(value) 
    
    def delta(self,value:float,extremum:float=1):
        """Renvoie 'True' si toutes les valeurs de la queue ont une différence avec la valeur rentrée en attribut, inférieur à l'extremum """
        for values in self.data:
            if not -extremum < (value - values) < extremum:
                return False
        return True
    
    def reset(self):
        """Remet la queue à 0"""
        self.data = []
    
    def __str__(self):
        return str(self.data)