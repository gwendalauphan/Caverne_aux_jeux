from tkinter import * #@UnusedWildImport
from tkinter.messagebox import *
from time import sleep
sys.path.append('../Reseau')
from Reseau.client import *
sys.path.append('../Scoreboard')
from Scoreboard.scoreboard import *
from random import randint
#difficultés: 9x9: 10, 16x16: 40, 16x30: 99

#fonction pour renvoyer toutes les cellules adjascentes
around = lambda x, y: [(x-1, y-1), (x-1, y), (x-1, y+1), (x,y+1), (x,y-1), (x+1, y-1), (x+1, y), (x+1, y+1)]

class demineur:
    def __init__(self, user):
        self.score = 0    #record de la session
        self.User = user  #utilisateur qui joue au jeux
        self.level = 0    #difficulté
        self.border = 25  #taille d'une cellule

        #import des images
        self.Number_Image = [PhotoImage(file = "Minesweeper/Images/0.png").subsample(8), PhotoImage(file = "Minesweeper/Images/1.png").subsample(8), PhotoImage(file = "Minesweeper/Images/2.png").subsample(8),\
            PhotoImage(file = "Minesweeper/Images/3.png").subsample(8), PhotoImage(file = "Minesweeper/Images/4.png").subsample(8), PhotoImage(file = "Minesweeper/Images/5.png").subsample(8),\
            PhotoImage(file = "Minesweeper/Images/6.png").subsample(8), PhotoImage(file = "Minesweeper/Images/7.png").subsample(8), PhotoImage(file = "Minesweeper/Images/8.png").subsample(8)]
        self.bomb_Image = PhotoImage(file = "Minesweeper/Images/bomb.png").subsample(8)
        self.Normal_Image = PhotoImage(file = "Minesweeper/Images/facingDown.png").subsample(8)
        self.Flag_Image = PhotoImage(file = "Minesweeper/Images/flagged.png").subsample(8)

        self.level_easy = PhotoImage(file = "Minesweeper/Images/level_easy.png")
        self.level_medium = PhotoImage(file = "Minesweeper/Images/level_medium.png")
        self.level_hard = PhotoImage(file = "Minesweeper/Images/level_hard.png")

        #interface pour afficher les regles
        self.show_rules = Toplevel()
        self.show_rules.title('Règles')
        self.show_rules.geometry('670x530')
        self.show_rules.resizable(False,False)
        self.show_rules.focus_force()
        self.show_rules.protocol("WM_DELETE_WINDOW", self.quit_ranking) #protocole pour controler la fermeture d ela fenetre

        self.fond = PhotoImage(file = "thumbnail/Minesweeper2.png")
        self.Frame_main1_wind2 = Canvas(self.show_rules, relief = GROOVE) #premier frame, celui en dessous
        self.Frame_main1_wind2.create_image(335,265, image = self.fond)
        self.Frame_main1_wind2.pack(ipadx = 670, ipady = 530)
        #self.Fond_Frame_main1_wind2 = PhotoImage(file = "thumbnail/Tete2.png")
        #self.Frame_main1_wind2.create_image(335,265,image =Fond_Frame_main1_wind2)
        self.Frame_main2_wind2 = Frame(self.Frame_main1_wind2,width = 550, height = 425, relief = GROOVE) #second frame, au dessus
        self.Frame_main2_wind2.place(x = 60, y = 45)
        self.Rules = Label(self.Frame_main2_wind2, text = 'Les règles:', font = ("Berlin Sans FB", 23), relief = GROOVE)
        self.Rules.place(x = 200, y =5)

        Label(self.Frame_main2_wind2, text = "Le but du jeu est de décourvrir toutes les mines,\nSans se faire exploser...").place(x = 20, y = 80)
        self.image1 = PhotoImage(file = "Minesweeper/Images/explode.png")
        Label(self.Frame_main2_wind2, image = self.image1).place(x = 450, y = 80)

        Label(self.Frame_main2_wind2, text = "il faut donc révéler les cases avec le clique gauche\n Ne nombre affiché sur la case renseigne sur\n le nombre de bombres adjascentes à celle-ci").place(x = 20, y = 150)

        Label(self.Frame_main2_wind2, text = "Il faut donc placer des drapeaux (clique droit) sur les cases\n contenant des bombes afin de les sécuriser").place(x = 20, y = 220)
        self.image3 = PhotoImage(file = "Minesweeper/Images/flag.png")
        Label(self.Frame_main2_wind2, image = self.image3).place(x = 425, y = 180)

        Label(self.Frame_main2_wind2, text = "Pour gagner, il faut marquer toutes les bombes avec un drapeau.").place(x = 20, y = 275)
        self.image4 = PhotoImage(file = "Minesweeper/Images/win.png")
        Label(self.Frame_main2_wind2, image = self.image4).place(x = 425, y = 275)

        Label(self.Frame_main2_wind2, text = "Il y a trois difficultés, la taille de la grille\n ainsi que le nombre de mines change entre les niveaux.").place(x = 20, y = 310)

        self.Button_Skip = Button(self.Frame_main2_wind2, text = "-Skip-", cursor ='hand2', command = self.quit_rules)
        self.Button_Skip.place(x = 50, y = 370)
        self.show_rules.mainloop()

        self.root = Toplevel() #fenetre principale
        self.root.title("Minesweeper")
        self.root.protocol("WM_DELETE_WINDOW", self.exit)
        self.root.resizable(False,False)
        self.root.focus_force()
        self.root.withdraw() #on masque la fenetre principale le temps de la sélection de la difficulté

        self.difficulty() #on charge la difficulté
        self.root.mainloop()

    def quit_ranking(self): #fonction utilisée pour quitter l'interface des classements
        self.show_rules.destroy()
        self.show_rules.quit()

    def quit_rules(self): #fonction pour passer des regles au classement
        self.Frame_main2_wind2.destroy()
        Scoreboard(self.Frame_main1_wind2, self.show_rules, "Minesweeper", self.User)

    def difficulty(self): #fonction de sélection de la difficulté

        self.root_difficulty = Toplevel()
        self.root_difficulty.title("difficulté")
        self.root_difficulty.resizable(False,False)
        self.root_difficulty.focus_force()
        self.root_difficulty.geometry("300x125")
        self.root_difficulty.protocol("WM_DELETE_WINDOW", print)
        #boutons avec les différentes difficultés
        Button(self.root_difficulty,image = self.level_easy , cursor ='hand2', command = lambda : self.start(0)).place(x = 15, y = 27)
        Button(self.root_difficulty,image = self.level_medium , cursor ='hand2', command = lambda : self.start(1)).place(x = 115, y = 27)
        Button(self.root_difficulty,image = self.level_hard , cursor ='hand2', command = lambda : self.start(2)).place(x = 215, y = 27)
        self.root_difficulty.mainloop()

    def start(self, level): #fontion appelée après la sélection de la difficulté avec level en paramètre
        self.root_difficulty.destroy() #destruction de la fenetre de la difficulté
        self.root_difficulty.quit()
        self.level = level
        if level == 0: #sélection des dimensions et du nombre de mines suivant le niveau sélectionné
            self.dims = (9,9)
            self.mine_Count = 10
        elif level == 1:
            self.dims = (16,16)
            self.mine_Count = 40
        else:
            self.dims = (30, 16)
            self.mine_Count = 99

        self.first = False
        self.root.deiconify()   # affichage de la fenetre principale
        self.root.focus_force() # on force le focus
        #on détermine la taille de la fenetre principale suivant le niveau
        self.root.geometry("%sx%s" % (200 + self.dims[0]*self.border, self.dims[1]*self.border + 50))

        self.Frame_right = Frame(self.root, width = self.dims[0]*self.border , height = self.dims[1]*self.border, bg = 'white')
        self.Frame_left = Frame(self.root, width = 200  , height = self.dims[1]*self.border  , bg = 'white')
        self.Frame_top = Frame(self.root, width = 200 + self.dims[0]*self.border , height = 50, bg = 'lightgrey')

        self.Frame1 = Frame(self.Frame_left, width = 200, height = 2*self.dims[1]*self.border/5)
        self.Frame2 = Frame(self.Frame_left, width = 200, height = 3*self.dims[1]*self.border/5, bg = 'black')

        self.Frame_top.pack(side = TOP)
        self.Frame_left.pack(side = LEFT)
        self.Frame_right.pack(side = RIGHT)
        self.Frame1.pack(side = TOP)
        self.Frame2.pack(side = BOTTOM)

        self.Button_quit = Button(self.Frame_top, text = 'QUIT' ,relief = GROOVE ,font = ("Helvetica", 10), cursor ='hand2',command = self.exit)
        self.Button_quit.place(x = 550, y = 19)

        self.flag_count = 0 #nombre de drapeaux cliqués
        self.label_flag = Label(self.Frame1, text = "Drapeaux restants: {}".format(self.mine_Count))
        self.label_flag.place(x = 20, y = 10)

        self.grid = [[0 for i in range(self.dims[1])] for j in range(self.dims[0])] #création de la grille contenant l'état des cellules

        self.canvas = Canvas(self.Frame_right, width = self.dims[0]*self.border, height = self.dims[1]*self.border, bg = "red", highlightthickness=0)
        self.canvas.bind("<Button>", self.click)
        self.canvas.place(x = 0, y = 0)

        self.list_images = [[0 for i in range(self.dims[1])] for j in range(self.dims[0])] #liste contenant les images de la grille
        for i in range(self.dims[0]):
            for j in range(self.dims[1]): #on initialise la grille avec des images de bouton
                self.list_images[i][j] = self.canvas.create_image(i*self.border + self.border/2, j*self.border + self.border/2, image = self.Normal_Image)

    def exit(self): #fonction appelée pour quiter l'application
        try:
            self.exit_difficulty()
        except: pass
        self.root.destroy()
        self.root.quit()

    def exit_difficulty(self):
        self.root_difficulty.destroy()
        self.root_difficulty.quit()

    def click(self, event): #fonction déclanchée avec un clique de la souris sur le canvas
        x = event.x//self.border #on détermine l'emplacement dans le tableau de la case cliquée
        y = event.y//self.border
        if not(self.first):
            self.first = True
            for _ in range(self.mine_Count): #loop pour placer les bombes
                turn = True
                #boucle pour choisir des coordonées tant qu'on a pas sélectionné un emplacement libre
                while turn == True:
                    temp = (randint(0, self.dims[0]-1), randint(0, self.dims[1]-1))
                    if self.grid[temp[0]][temp[1]] != -1 and not (x+1 >= temp[0] >= x-1 and y+1 >= temp[1] >= y-1):
                        self.grid[temp[0]][temp[1]] = -1
                        turn = False

            #détermination du nombre de bombes voisines par cases
            for i in range(self.dims[0]):
                for j in range(self.dims[1]):
                    if self.grid[i][j] == -1: #on boucle dans les cases
                        for ip, jp in around(i, j): #si c'est une bombe, on ajoute 1 à chaque case autours
                            if self.dims[0] > ip >-1 and self.dims[1] > jp >= 0 and self.grid[ip][jp]!=-1:
                                self.grid[ip][jp] += 1
        if event.num == 1: # si clique gauche
            value = self.grid[x][y] #valeur de la grille à l'amplacement cliqué
            #si l'image est un drapeau, on l'enlève
            if self.canvas.itemconfigure(self.list_images[x][y])["image"][-1] == str(self.Flag_Image):
                self.canvas.itemconfigure(self.list_images[x][y], image = self.Normal_Image)
            elif value == -1: # si il y a une bombe
                count = 0 #on compte le nombre de cases bien identifiées comme étant des bombes
                for i in range(self.dims[0]):
                    for j in range(self.dims[1]):
                        #si il y a une image de drapeau et qu'il y a une bombe à l'emplacement
                        if self.canvas.itemconfigure(self.list_images[i][j])["image"][-1] == str(self.Flag_Image) and self.grid[i][j] == -1:
                            count += 1
                self.end(False, count) #appel de la fonction end de la classe
                return
            elif value > 0: #si on a cliqué sur une case contenant au moins une bombe voisine, on affiche le nombre de voisins
                self.canvas.itemconfigure(self.list_images[x][y], image = self.Number_Image[value])
            elif value == 0: #si il n'y a pas de voisins
                self.canvas.itemconfigure(self.list_images[x][y], image = self.Number_Image[value])
                process = around(x, y) #on crée une liste contenant tous les voisins
                done = process.copy() #liste pour éviter de faire trop de calculs
                while len(process) != 0: # tant qu'il y a des cases à process
                    next_process = []    # liste des prochaines cases à process
                    for x,y in process:  #pour chaque cases de la liste
                        if self.dims[0] > x >-1 and self.dims[1] > y >= 0: #on vérifie que les index appartiennent à la grille
                            value = self.grid[x][y] #récupération de la valeur de la case
                            self.canvas.itemconfigure(self.list_images[x][y], image = self.Number_Image[value])
                            if value == 0: #si la valeur est encore 0
                                for xb,yb in around(x, y): #on ajoute les voisins de cette case à la liste à process
                                    if (xb, yb) not in done:
                                        done.append((xb,yb))
                                        next_process.append((xb, yb))
                    process = next_process #process prend la valeur des cases à vérifier

        elif event.num == 2: #si c'est un clique molette
            #si la case cliquée est un nombre
            if self.canvas.itemconfigure(self.list_images[x][y])["image"][-1] != str(self.Normal_Image) and self.canvas.itemconfigure(self.list_images[x][y])["image"][-1] != str(self.Flag_Image):
                event.num = 1 #on définit l'évènement comme étant un clique gauche
                for xb, yb in around(x, y): #on simule un clique sur toutes les cases autour si ce ne sont pas des drapeaux
                    if self.canvas.itemconfigure(self.list_images[xb][yb])["image"][-1] == str(self.Normal_Image):
                        event.x = xb*self.border
                        event.y = yb*self.border
                        self.click(event)

        elif event.num == 3: #clique droit
            #lors d'un clique droit, on vérifie si l'utilisateur n'a pas déjà posé un drapeau:
            #si oui, on change par un bouton normal; si non, on met un drapeau dans la liste
            if self.canvas.itemconfigure(self.list_images[x][y])["image"][-1] == str(self.Flag_Image):
                self.canvas.itemconfigure(self.list_images[x][y], image = self.Normal_Image)
                self.flag_count -= 1
            elif self.canvas.itemconfigure(self.list_images[x][y])["image"][-1] == str(self.Normal_Image) and self.flag_count < self.mine_Count:
                self.canvas.itemconfigure(self.list_images[x][y], image = self.Flag_Image)
                self.flag_count += 1
            self.label_flag["text"] = "Drapeaux restants: {}".format(self.mine_Count - self.flag_count)
        count = 0 #compte des bombes recouvertes par un drapeau (voir plus haut)
        for i in range(self.dims[0]):
            for j in range(self.dims[1]):
                if self.canvas.itemconfigure(self.list_images[i][j])["image"][-1] == str(self.Flag_Image) and self.grid[i][j] == -1:
                        count += 1
        if count == self.mine_Count: #si toutes les cases sont recouvertes, le joueur à gagné
            self.end(True, count)
        self.canvas.update()

    def end(self, win, count = 0): #fonction appelée à la fin de la partie
        self.canvas.unbind("<Button>")
        if win == False: #si le joueur a perdus, on affiche toutes les bombes
            for x in range(self.dims[0]):
                for y in range(self.dims[1]):
                    if self.grid[x][y] == -1:
                        self.canvas.itemconfigure(self.list_images[x][y], image = self.bomb_Image)
        if count * 50 > self.score: # si le score est supérieur au précédent recors,
                                    # on lui atribue la valeur du nouveau score
            self.score = count* 50 #ajouter le temps
        #on demande au joueur si il vaut recomencer
        question = askquestion("Restart", "Partie finie.\nVeux-tu recommencer?")
        if question == "yes": #si oui, on cache la fenete et on redemande la difficulté
            self.Frame_right.destroy()
            self.Frame_left.destroy()
            self.Frame_top.destroy()
            self.root.withdraw()
            self.difficulty()
        else:
            self.exit() #sinon on quite le jeu


def Minesweeper(user):    # fonction appelée pour lancer le jeu
    jeux = demineur(user) # création de la classe
    return jeux.score     # retour du meilleur score de la session
