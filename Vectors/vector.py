from math import sin, cos, sqrt

class Vector: #classe vecteur
    def __init__(self, x, y): #le vecteur est initialisé avec un x et un y
        self.x = x
        self.y = y

    def __str__(self): #fonction pour print un vecteur
        return "Vector (%d, %d)" % (self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def mag(self): #retourne la longeur du vecteur (sa magnétude)
        return sqrt(self.x**2 + self.y**2)

    def normalize(self): #fonction pour normaliser la norme du vecteur à une valeur comprise entr 0 et 1
        m = self.mag()
        if m != 0 and  m!=1:
            self.div(m)

    def mult(self, n): #fonction pour multiplier les coordonées du vecteur par un nombre
        self.x *= n
        self.y *= n

    def div(self, n): #fonction pour diviser les coordonées du vecteur par un nombre
        self.x /= n
        self.y /= n

    def add(self, other): #fonction pour ajouter un nombre au vecteur
        self.x += other.x
        self.y += other.y

    def setMag(self, n): # fonction pour définir la norme du vecteur
        self.normalize() # on la normalise
        self.mult(n)     # puis on la multiplie par le nombre

    def rotate(self, angle): #fonction pour appliquer une rotation au vecteur
        temp = self.x
        self.x = self.x*cos(angle) - self.y*sin(angle) # ces calculs sont le résultat du produit matriciel
        self.y = temp*sin(angle) + self.y*cos(angle)   # entre le vecteur et une matrice de rotation de l'angle donné

    def integer(self): #convertit les composantes en entier relatif
        self.x = int(round(self.x))
        self.y = int(round(self.y))
