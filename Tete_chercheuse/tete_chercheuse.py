from tkinter import * #@UnusedWildImport
from tkinter.messagebox import *
from Tete_chercheuse.data import *
from time import sleep, time
sys.path.append('../Reseau')
from Reseau.client import *
sys.path.append('../Scoreboard')
from Scoreboard.scoreboard import *
sys.path.append('../Vectors')
from Vectors.vector import *
from math import pi

##################----------Variables------------######################################
#'0' correpond à une case vide
#'X' correspond à une case pleine (mur)
#'R' correpond à la case associée au robot
#'P' correpond à la case associée à l'arrivée (drapeau)
#'C' correpond aux palettes, où l'on ajoute un obstacle
#'S' correspond à une (petite) pièce/récompense
#'B' correspond à une (grosse) pièce/récompense
#'E' correspond au robot arrivé
#meilleur score possible: 4163,9
########################################################################################

class application:
    def __init__(self, user):
        self.User_name = user #nom d'utilisateur
        self.rules_game() #on execute les rêgles du jeu et le scoreboard

        self.root_tete = Toplevel() #fenetre principale
        self.root_tete.geometry('700x550')
        self.root_tete.protocol("WM_DELETE_WINDOW", self.exit)
        self.root_tete.title("Tete Chercheuse")
        self.root_tete.resizable(False,False)
        self.root_tete.focus_force()
        #############------------variables----------########################
        self.score = [50] #initialisation de la liste des scores
        self.index_robot = 0 #la ou le robot regarde
        self.nbcases_width = self.nbcases_height = 10 #dimensions
        self.cell_width = 500/self.nbcases_width #dimensions des cellules
        self.cell_height = 500/self.nbcases_height
        self.score_star = 0            #bonnus des pièces
        self.time_game = 0
        self.score_temp = 0

        self.table = [[0 for i in range(self.nbcases_width)] for j in range(self.nbcases_height)]#tableau
        self.level = 1 #niveau

        ########---------Import Photos------------------###############################################
        self.robot = [PhotoImage(file = "Tete_chercheuse/image/robot_right.png"), PhotoImage(file = "Tete_chercheuse/image/robot_front.png"), PhotoImage(file = "Tete_chercheuse/image/robot_left.png"), PhotoImage(file = "Tete_chercheuse/image/robot_back.png")]
        self.restart_button_image = PhotoImage(file = "Tete_chercheuse/image/start.png")
        self.Flag = PhotoImage(file = "Tete_chercheuse/image/flag.png")
        self.End = PhotoImage(file = "Tete_chercheuse/image/robot_flag.png")
        self.Caisse = PhotoImage(file = "Tete_chercheuse/image/caisse.png")
        self.Wall = PhotoImage(file = "Tete_chercheuse/image/mur.ppm")
        self.Fond_Frame_main1_wind2 = PhotoImage(file = "thumbnail/Tete2.png")
        self.Yellow_Coin = PhotoImage(file = "Tete_chercheuse/image/yellow_coin.ppm")
        self.Red_Coin = PhotoImage(file = "Tete_chercheuse/image/red_coin.ppm")
        self.Guide_tete = PhotoImage(file = "Tete_chercheuse/image/brain.png")
        self.Bulle_image = PhotoImage(file = "Tete_chercheuse/image/bulle.png")


        self.main = PhotoImage(file = "Parametters/main2.png")
        self.next_image = PhotoImage(file = "Parametters/next2.png")
        self.fond_ecran = PhotoImage(file = "Parametters/fond_ecran.png")
        self.replay = PhotoImage(file = "Parametters/replay2.png")


        ########------------Frames Pricipaux-------------########################################
        self.Frame_top = Frame(self.root_tete, width = 700, height = 50, bg = 'lightgrey')
        self.Frame_right = Frame(self.root_tete, width = 500, height = 500, bg = 'black')
        self.Frame_left = Frame(self.root_tete, width = 200, height = 500, bg = 'red')

        ########-----------Frames Secondaires-----------######################################
        self.Frame1 = Frame(self.Frame_left, width = 200, height =200, bg = 'gold')
        self.Frame2 = Frame(self.Frame_left, width = 200, height =300, bg = 'black')

        self.Title_level = Label(self.Frame_top, text = "Level 1", font=("Helvetica", 20), relief = GROOVE)

        self.Canvas_dessine = Canvas(self.Frame2, bg = 'white',width = 188, height =290)

        #######-----------Package des Frames-------------##################################
        self.Frame_top.pack(side = TOP)
        self.Frame_right.pack(side = RIGHT)
        self.Frame_left.pack(side = LEFT)

        self.Frame1.pack(side = TOP)
        self.Frame2.pack(side = BOTTOM)
        self.Canvas_dessine.place(x = 4, y =4)

        self.Title_level.place(x = 315, y = 5)

        #########------------Labels et autres-----------##################################

        self.Button_start = Button(self.Frame1,relief = GROOVE,activebackground = 'black' ,bg = 'black', cursor ='hand2', image = self.restart_button_image,command = self.start)
        self.Button_start.place(x = 20, y = 27)

        self.Button_quit = Button(self.Frame_top, text = 'QUIT' ,relief = GROOVE ,font = ("Helvetica", 10), cursor ='hand2',command = self.exit)
        self.Button_quit.place(x = 550, y = 19)

        self.Button_restart = Button(self.Frame_top, text = "RESTART", relief = GROOVE,cursor ='hand2', font = ("Helvetica", 10),command = self.restart_button)
        self.Button_restart.place(x = 600, y = 19)

        self.show_time = Label(self.Frame1, text = "Time: %s" %str(0), font = ("Helvetica", 10), relief =GROOVE)
        self.show_time.place(x = 110, y = 170)

        self.show_score = Label(self.Frame1, text = "Score: %s" %str(sum(self.score)), font = ("Helvetica", 10), relief = GROOVE)
        self.show_score.place(x = 25, y = 170)

        self.show_count = Label(self.Frame1, text = "Nombre de palettes: %s" %str(0), font = ("Helvetica", 10), relief = GROOVE)
        self.show_count.place(x = 31, y = 130)

        self.Canvas_dessine.create_image(86,215 ,image = self.Guide_tete)
        self.Canvas_dessine.create_image(100,68, image= self.Bulle_image)

        self.show_conseils = Label(self.Canvas_dessine, text = "Conseil: Je te propose \n d'être sûr de ton trajet \n avant de commencer",bg = 'white', font = ("Helvetica", 9))
        self.show_conseils.place(x = 32, y =38 )

        ###############-----------Lancement des fonctions-------------######################
        self.time_num()
        self.time_start = time()
        self.restart2()
        self.update()

        self.root_tete.mainloop()

    #fonction pour afficher les regles du jeu
    def rules_game(self):
        self.show_rules = Toplevel()

        self.show_rules.title('Règles')
        self.show_rules.geometry('670x530')
        self.show_rules.protocol("WM_DELETE_WINDOW", self.quit_ranking)
        self.show_rules.focus_force()
        self.show_rules.resizable(False,False)

    ################-----------Création des Frames de la fenetre secondaire----------##############
        self.Frame_main1_wind2 = Canvas(self.show_rules, relief = GROOVE)
        self.Frame_main1_wind2.pack(ipadx = 670, ipady = 530)

        self.Fond_Frame_main1_wind2 = PhotoImage(file = "thumbnail/Tete2.png")
        self.Frame_main1_wind2.create_image(335,265,image =self.Fond_Frame_main1_wind2)

        self.Frame_main2_wind2 = Frame(self.Frame_main1_wind2,width = 550, height = 425, relief = GROOVE)
        self.Frame_main2_wind2.place(x = 60, y = 45)
    ###############---------Création des regles avec animations--------------####################

        Label(self.Frame_main2_wind2, text = 'Les règles:', font = ("Berlin Sans FB", 23), relief = GROOVE).place(x = 200, y =5)

    #------------------1----------------------------------------------------------------
        #détail d'une rêgle
        Rules1 = Label(self.Frame_main2_wind2, text = "Le but est que le robot arrive au drapeau.\n", font = ("Berlin Sans FB", 12))
        self.Frame_main2_wind2.after(500, lambda: Rules1.place(x = 45, y = 70)) #affichage après un délais

        self.first_photo1 = PhotoImage(file = "Tete_chercheuse/image/first_photo.png") #import de l'image
        Label1 = Label(self.Frame_main2_wind2, image = self.first_photo1)
        self.Frame_main2_wind2.after(1000, lambda: Label1.place(x = 380, y = 60 )) #placement du canvas

    #------------------2-----------------------------------------------------------------
        Rules2 = Label(self.Frame_main2_wind2, text = 'Pour cela, tu as à disposition des caisses \n\
        qui te permettront de dévier le robot.',font = ("Berlin Sans FB", 12))
        self.Frame_main2_wind2.after(2000, lambda: Rules2.place(x = 40, y = 150))

        self.first_photo2 = PhotoImage(file = "Tete_chercheuse/image/second_photo.png")
        Label2 = Label(self.Frame_main2_wind2, image = self.first_photo2)
        self.Frame_main2_wind2.after(2500, lambda: Label2.place(x = 390, y = 140 ))

    #------------------3------------------------------------------------------------------
        Rules3 = Label(self.Frame_main2_wind2, text = "A chaque fois que le robot rencontre un obstacle,\n il tourne à SA droite sinon il va toujours tout droit.",font = ("Berlin Sans FB", 12))
        self.Frame_main2_wind2.after(3500, lambda: Rules3.place(x = 20, y = 240))

        self.first_photo3 = PhotoImage(file = "Tete_chercheuse/image/third_photo.png")
        Label3 = Label(self.Frame_main2_wind2, image = self.first_photo3)
        self.Frame_main2_wind2.after(4000, lambda: Label3.place(x = 350, y = 230 ))

    #------------------4-------------------------------------------------------------------
        Rules4 = Label(self.Frame_main2_wind2, text = "Enfin tu peux rencontrer des pièces rouges et \n\
        jaunes, en passant dessus tu gagneras des points. \n\
        Les rouges rapportent plus de points que les jaunes.",font = ("Berlin Sans FB", 12))
        self.Frame_main2_wind2.after(5000, lambda: Rules4.place(x = 17, y = 320))

        self.first_photo4 = PhotoImage(file = "Tete_chercheuse/image/four_photo.png")
        Label4 = Label(self.Frame_main2_wind2, image = self.first_photo4)
        self.Frame_main2_wind2.after(5500, lambda: Label4.place(x = 380, y = 320 ))

    #--------------5------------------------------------
        self.Bouton_skip = Button(self.Frame_main2_wind2, text = '-Skip-',font = ("Helvetica", 10),cursor ='hand2', relief = GROOVE,command = self.quit_rules)
        self.Bouton_skip.place(x = 200, y = 390)

        self.show_rules.mainloop()

    def quit_ranking(self): #fonction pour quitter la fenetre des rêgles et du classement
        self.show_rules.destroy()
        self.show_rules.quit()

    def quit_rules(self): #fonction pour quiter les rêgles et aller sur les classements
        self.Frame_main2_wind2.destroy()
        Scoreboard(self.Frame_main1_wind2, self.show_rules, "Tete", self.User_name) #appel de la classe du scoreboard

    """######################------------------Début du Jeu---------------------------########################################"""

    def click(self, event): #fonction appelée lors du clique de la souris sur le canvas
        x = event.x                 #on récupère la position de la souris sur l'écran
        y = event.y

        i = int(x//self.cell_width) #on convertit la position de la souris en indice pour le tableau
        j = int(y//self.cell_height)

        if self.table[i][j] == "0":   # si on se trouve sur une case vide
            self.table[i][j] = "C"    # on ajoute une caisse
            self.box_placed+=1        # et on incrémente le nombre de caisses en actualisant l'affichage
            self.show_count['text'] = "Nombre de palettes: %s" %str(self.box_placed)
        elif self.table[i][j] == "C": # si on clique sur une caisse
            self.table[i][j] = "0"    # on l'enlève
            self.box_placed-=1        # on décrémente le compteur en actualisant l'affichage
            self.show_count['text'] = "Nombre de palettes: %s" %str(self.box_placed)
        self.update()

    def update(self, Print_Score = True): #fonction pour regénérer l'affichage
        self.verite = True
        try:
            self.Table.delete("all") #on supprime tout ce qu'il y a sur le canvas
        except: pass
        for i in range(self.nbcases_width): #recréation des lignes
            self.Table.create_line((self.cell_width)*i,0,(self.cell_width)*i,500)
        for j in range(self.nbcases_height):
            self.Table.create_line(0,(self.cell_width)*j,500,(self.cell_width)*j)

        self.Table.create_rectangle(2,2,500,500) #contours
        for i in range(10): #pour chaques cases, on regarde ce qu'il y a dans le tableau et on crée l'affichage correspondant
            for j in range(10):
                if (self.table[i][j])=='X':
                    self.Table.create_image(self.cell_width* i + self.cell_width/2, self.cell_height* j + self.cell_height/2, image = self.Wall)
                elif self.table[i][j] == "C":
                    self.Table.create_image(self.cell_width* i + self.cell_width/2, self.cell_height* j + self.cell_height/2, image = self.Caisse)
                elif (self.table[i][j])=='R':
                    self.Table.create_image(self.cell_width* i + self.cell_width/2, self.cell_height* j + self.cell_height/2, image = self.robot[self.index_robot])
                elif (self.table[i][j])=='P':
                    self.Table.create_image(self.cell_width* i + self.cell_width/2, self.cell_height* j + self.cell_height/2, image = self.Flag)
                elif (self.table[i][j])=='S':
                    self.Table.create_image(self.cell_width* i + self.cell_width/2, self.cell_height* j + self.cell_height/2, image = self.Yellow_Coin)
                elif (self.table[i][j])=='B':
                    self.Table.create_image(self.cell_width* i + self.cell_width/2, self.cell_height* j + self.cell_height/2, image = self.Red_Coin)
                elif self.table[i][j] == "E":
                    self.Table.create_image(self.cell_width* i + self.cell_width/2, self.cell_height* j + self.cell_height/2, image = self.End)
        self.root_tete.update()

        if Print_Score == True: #on peut appeler la fonction update sans actualiser le score
            self.show_score["text"] = "Score: %s" %str(int(sum(self.score))) #actualisation du score

    def exit_menu(self):
        self.score[-1] += self.score_temp
        self.exit()

    def next(self):
        self.score[-1] += self.score_temp     # on atribue au dernier niveau joué le score gardé en mémoire
        self.score.append(50*(self.level+1))  # création d'un nouveau slot dans la liste des scores pour le nouveau niveau initié avec une valeur car il y a un malus appliqué dans la foction restart
        self.level += 1                  # incrémentation du niveau
        if self.level == len(Levels)+1:  # si le joueur a atteint la fin de la liste des niveaux
            self.verite = False
            self.score[-1] = 0           # le dernier score ne doit pas avoir d'offset
            self.exit()                  # on quitte le jeu en arretant la fonction
            return
        self.Title_level["text"] = "Level {}".format(self.level) #actualisation de l'affichage
        self.restart2()                   # régénération de l'affichage

    def end_game(self):
        try:
            self.Table.destroy()
        except: pass
        try:
            self.canvas_question.destroy()
        except: pass
        if self.Score_calculated is False:
            self.Score_calculated = True
            self.score_temp = (10000/(self.box_placed*10 + self.time_game*0.2) + self.score_star) * self.level #calcul du score
        self.show_score["text"] = "Score: %s"%str(int(sum(self.score + [self.score_temp]))) #on actualise l'affichage
        self.Button_restart["state"] = "disabled" #désactivation du bouton restart
        self.canvas_question = Canvas(self.Frame_right, width = 482, height = 300, highlightthickness = 0)
        self.canvas_question.place(x=9,y=100)
        self.canvas_question.create_image(241, 150, image = self.fond_ecran)
        self.canvas_question.create_text(90, 110, text = 'Recommencer', font = ("Berlin Sans FB", 20))
        self.canvas_question.create_text(241, 110, text = 'Suivant', font = ("Berlin Sans FB", 20))
        self.canvas_question.create_text(390, 110, text = 'Menu', font = ("Berlin Sans FB", 20))
        Button(self.canvas_question,image = self.replay, highlightthickness=0, borderwidth = 0, command = self.restart_question,cursor ='hand2', font = ("Helvetica", 10)).place(x = 60, y = 150)
        Button(self.canvas_question,image = self.main,highlightthickness=0, borderwidth = 0,command = self.exit_menu,cursor ='hand2', font = ("Helvetica", 10)).place(x = 360, y = 150)
        Button(self.canvas_question,image = self.next_image,highlightthickness=0, borderwidth = 0,command = self.next,cursor ='hand2', font = ("Helvetica", 10)).place(x = 211, y = 150)

    def restart_question(self):
        self.canvas_question.destroy()
        self.canvas_question = Canvas(self.Frame_right, width = 482, height = 300, highlightthickness = 0)
        self.canvas_question.place(x=9,y=100)
        self.canvas_question.create_image(241, 150, image = self.fond_ecran)
        self.canvas_question.create_text(232, 100, text ='             Perdu !! \n Veux-tu recommencer ?', font = ("Berlin Sans FB", 14))
        answer1 = Button(self.canvas_question, text = " Oui ",command = self.restart2,cursor ='hand2',fg = 'white', bg = 'black', font = ("Helvetica", 12)).place(x = 120, y = 150)
        answer2 = Button(self.canvas_question, text = " Non ",command = self.end_game,cursor ='hand2',fg = 'white', bg = 'black', font = ("Helvetica", 12)).place(x = 300, y = 150)

        self.box_placed = 0 #nombre de box que l'utilisateur a posé sur la map
        self.time_game = 0 #temps pris par le joueur pour résoudre l'agnime

    def restart2(self):
        try:
            self.canvas_question.destroy()
        except: pass
        try:
            self.Table.destroy()
        except: pass
        self.Table = Canvas(self.Frame_right,width = 500, height = 500, bg ='white', highlightthickness=0)
        self.Table.pack(fill = BOTH)
        self.Score_calculated = False
        self.Button_restart["state"] = "normal" #on réactive le bouton restart
        self.index_robot = 0 #on repositionne le robot à droite
        self.score[-1] -= 50*self.level #pénalité
        self.Button_start["state"] = "normal" #réactivation du bouton start
        self.time_game = self.box_placed = self.score_star = 0 #on réinitaialise des variables de jeu
        self.show_time['text'] = "Temps: %s" %str(self.time_game) #actualisation des affichages
        self.show_count['text'] = "Nombre de palettes: %s" %str(self.box_placed)

        self.Table.bind("<Button-1>", self.click)  #rebind du clique droit
        for i in range(self.nbcases_width):
            for j in range(self.nbcases_height):
                self.table[i][j] = Levels[self.level-1][(j*self.nbcases_width)+i] #réinitialisation de la table
        self.update()

    def time_num(self): #fonciton pour incrémenter le temps
        self.time_game+=1 # incrémentation de la variable
        self.show_time['text'] = "Temps: %s" %str(self.time_game) #actualisation de l'affichage
        self.root_tete.after(1000,self.time_num) #rappel de la fonction après 1 seconde (1000 ms)

    def start(self): #fonction pour faire bouger le robot
        self.Table.unbind("<Button-1>")          # on désactive le clique et le bouton start
        self.Button_start["state"] = "disabled"
        dir = Vector(1, 0)                       # vecteur de mouvement, par défaut, on va a droite
        for i in range(self.nbcases_width):
            for j in range(self.nbcases_height): # on récupère la position du robot en parcourant la liste
                if self.table[i][j] == "R":
                    pos = Vector(i, j)
                    break
        reminder = {} # pour vérifier le nombre de fois qu'on est passé a un meme endroit
        self.run = True    # variable vraie tant qu'on execute la boucle
        while self.run == True:
            sleep(0.4) #on fait avancer le robot toutes les 0.4 secondes
            self.table[pos.x][pos.y] = "0" # on remplace la case où il était par une case vide
            x = pos.x + dir.x #calcul de la prochaine position
            y = pos.y - dir.y

            if self.nbcases_width > x >= 0 and self.nbcases_height > y >= 0 and self.table[x][y]!= 'X' and self.table[x][y]!= 'C':
                if self.table[x][y] == "0": #si la prochaine position est dans le tableau et que la prochaine case est libre
                    pos = Vector(x, y) #on lui assigne la nouvelle position
                    try:
                        reminder[(pos.x, pos.y)] += 1     # on essaye d'ajouter 1 à la position actuelle
                        if reminder[(pos.x, pos.y)] > 4:  # si on est passé plus de 4 fois au meme endroit, on restart
                            self.run = False
                            self.restart2()
                            return
                    except:
                        reminder[(pos.x, pos.y)] = 1 #si impossible de ajouter 1 c'est que la clef n'est pas crée, on l'initialise a 1

                elif self.table[x][y] == "S": #si la prochaine case est une petite pièce
                    pos = Vector(x, y)        # on lui atribue la nouvelle position
                    self.score_star += 50    # ajout du bonnus
                    self.table[x][y] = "0"   # et on vide la case

                elif self.table[x][y] == "B": #même chose si la prochaine case est une grosse pièce
                    pos = Vector(x, y)
                    self.score_star += 150
                    self.table[x][y] = "0"


                elif self.table[x][y] == "P": #si la prochaine case est le drapeau
                    self.table[x][y] = "E" #on change la case actuelle à réussi pour afficher avec le drapeau
                    self.run = False #on arrete la boucle
                    self.end_game()  #fin du jeu
                    return      # fin de la fonction

            else:                                       # sinon, on a un obstacle devant le robot
                #dir = Vector(dir.y, -dir.x)             # rotation d'une matrice [a, b] par -PI/2 en faisant [b, -a]
                dir.rotate(-pi/2)
                dir.integer()
                self.index_robot = (self.index_robot + 1)%4   # affichage de la rotation

            self.table[pos.x][pos.y] = "R"             # on place la robot dans la grille à sa position actuelle
            self.update()

    def restart_button(self): #si on clique sur le bouton pour restart
        self.run = False #on arrete la boucle
        self.restart2()   #restart de l'application

    def exit(self): #fonction pour quitter, elle se charge de détruire les fenètres lancées
        if self.verite == True:
            self.score[-1] += self.score_temp
        self.count = 1
        self.root_tete.destroy()
        self.root_tete.quit()

def Tete(user): #fonction principale
    jeux = application(user)
    if jeux.count !=0:
        return (sum(jeux.score), sum(jeux.score)/jeux.count, (time()-jeux.time_start)/jeux.count, jeux.count, []) #retour du score total du joueur sur tout les niveaux joués
    else:
      return (0, 0, 0, 0, [])
