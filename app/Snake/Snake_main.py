import sys
from tkinter import *  # @UnusedWildImport
from tkinter.messagebox import *
from time import time

sys.path.append("../Reseau")
from app.Reseau.client import *

sys.path.append("../Scoreboard")
from app.Scoreboard.scoreboard import *

sys.path.append("../Vectors")
from app.Vectors.vector import *
from random import randint
from app.Utils.utils import resource_path

"""--------------------------------Directions-------------------------"""
# 0 = droite
# 1 = bas
# 2 = gauche
# 3 = haut
# 4 = haut vers droite
# 5 = bas vers droite
# 6 = bas vers gauche
# 7 = haut vers gauche


class snake:
    def __init__(self, user):
        self.User_name = user  # pseudo du joueur actuel
        self.Best_Score = 0  # meilleur score de la session
        self.average_score = [0]
        self.count = 0
        self.death_pos = []
        self.show_rules = Toplevel()
        self.show_rules.title("Règles")
        self.show_rules.geometry("670x530")
        self.show_rules.resizable(False, False)
        self.show_rules.focus_force()
        self.show_rules.protocol("WM_DELETE_WINDOW", self.quit_ranking)

        self.Frame_main1_wind2 = Canvas(self.show_rules, bg="red", relief=GROOVE)
        self.Frame_main1_wind2.pack(ipadx=670, ipady=530)

        self.Fond_Frame_main1_wind2 = PhotoImage(file=resource_path("thumbnail/Snake2.png"))
        self.Frame_main1_wind2.create_image(335, 265, image=self.Fond_Frame_main1_wind2)

        self.Frame_main2_wind2 = Frame(self.Frame_main1_wind2, width=550, height=425, relief=GROOVE)
        self.Frame_main2_wind2.place(x=60, y=58)
        self.Rules = Label(self.Frame_main2_wind2, text="Les règles:", font=("Berlin Sans FB", 23), relief=GROOVE)
        self.Rules.place(x=200, y=5)

        # détail des rêgles

        self.Rules2 = Label(
            self.Frame_main2_wind2,
            text="Le but est que le serpent mange des pommes \n pour qu'il puisse grandir et gagner la partie ",
            font=("Berlin Sans FB", 12),
        )
        self.Frame_main2_wind2.after(500, lambda: self.Rules2.place(x=45, y=70))

        self.CANVAS1 = Canvas(self.Frame_main2_wind2, width=150, height=60)
        self.Frame_main2_wind2.after(1000, lambda: self.CANVAS1.place(x=375, y=60))
        self.snake_ex_image = PhotoImage(file=resource_path("Snake/images/snake_ex_image.png"))
        self.CANVAS1.create_image(75, 30, image=self.snake_ex_image)

        # ------------------2-----------------------------------------------------------------
        self.Rules3 = Label(
            self.Frame_main2_wind2,
            text="Pour cela, tu as à disposition les flèches \n du clavier qui te permettront de déplacer.",
            font=("Berlin Sans FB", 12),
        )
        self.Frame_main2_wind2.after(2000, lambda: self.Rules3.place(x=35, y=170))

        self.CANVAS2 = Canvas(self.Frame_main2_wind2, width=150, height=104)
        self.Frame_main2_wind2.after(2500, lambda: self.CANVAS2.place(x=375, y=150))
        self.keyboard_snake = PhotoImage(file=resource_path("Snake/images/keyboard_snake.png"))
        self.CANVAS2.create_image(73, 51, image=self.keyboard_snake)
        self.CANVAS2.create_rectangle(2, 2, 148, 102, outline="black")

        # ------------------3------------------------------------------------------------------
        self.Rules4 = Label(
            self.Frame_main2_wind2,
            text="Cependant attention tu peux mourir en rencontrant \n\
        le mur, ou en te retournant sur toi même.",
            font=("Berlin Sans FB", 12),
        )
        self.Frame_main2_wind2.after(3500, lambda: self.Rules4.place(x=20, y=300))

        self.CANVAS3 = Canvas(self.Frame_main2_wind2, width=90, height=62)
        self.CANVAS4 = Canvas(self.Frame_main2_wind2, width=90, height=62)
        self.Frame_main2_wind2.after(4000, lambda: self.CANVAS3.place(x=402, y=267))
        self.Frame_main2_wind2.after(4000, lambda: self.CANVAS4.place(x=402, y=332))
        self.mur_snake = PhotoImage(file=resource_path("Snake/images/mur_snake.png"))
        self.mort_snake = PhotoImage(file=resource_path("Snake/images/mort_snake.png"))
        self.CANVAS3.create_image(45, 31, image=self.mur_snake)
        self.CANVAS4.create_image(45, 31, image=self.mort_snake)
        # ------------------Skip------------------------------------------------------------------
        self.Button_Skip = Button(self.Frame_main2_wind2, text="-Skip-", cursor="hand2", command=self.quit_rules)
        self.Button_Skip.place(x=200, y=390)
        self.show_rules.mainloop()

        self.root = Toplevel()
        self.root.geometry("702x577")
        self.root.bind("<space>", self.pause_command)
        self.root.protocol("WM_DELETE_WINDOW", self.exit)
        self.root.resizable(False, False)
        self.root.title("Snake")
        self.root.focus_force()

        # import de toutes les images du jeu

        self.Start_image = PhotoImage(file=resource_path("Snake/images/play.png"))
        self.Fruit_Image = PhotoImage(file=resource_path("Snake/images/Fruit.png"))

        self.Head_Image = [
            PhotoImage(file=resource_path("Snake/images/Head_Right.png")),
            PhotoImage(file=resource_path("Snake/images/Head_Down.png")),
            PhotoImage(file=resource_path("Snake/images/Head_Left.png")),
            PhotoImage(file=resource_path("Snake/images/Head_Up.png")),
        ]

        self.Body_Image = [
            PhotoImage(file=resource_path("Snake/images/Horizontal.png")),
            PhotoImage(file=resource_path("Snake/images/Vertical.png")),
            PhotoImage(file=resource_path("Snake/images/Horizontal.png")),
            PhotoImage(file=resource_path("Snake/images/Vertical.png")),
            PhotoImage(file=resource_path("Snake/images/Angle_Right_Top.png")),
            PhotoImage(file=resource_path("Snake/images/Angle_Right_Down.png")),
            PhotoImage(file=resource_path("Snake/images/Angle_Left_Down.png")),
            PhotoImage(file=resource_path("Snake/images/Angle_Left_Top.png")),
        ]

        self.Queue_Image = [
            PhotoImage(file=resource_path("Snake/images/Queue_Right.png")),
            PhotoImage(file=resource_path("Snake/images/Queue_Down.png")),
            PhotoImage(file=resource_path("Snake/images/Queue_Left.png")),
            PhotoImage(file=resource_path("Snake/images/Queue_Up.png")),
        ]

        self.main = PhotoImage(file=resource_path("Parametters/main2.png"))
        self.next_image = PhotoImage(file=resource_path("Parametters/next2.png"))
        self.fond_ecran = PhotoImage(file=resource_path("Parametters/fond_ecran.png"))
        self.replay = PhotoImage(file=resource_path("Parametters/replay2.png"))

        self.time_start = time()
        self.start()  # fonction pour initialiser l'interface
        self.root.mainloop()

    def quit_rules(self):  # fonction pour quiter les rêgles et passer au classement
        self.Frame_main2_wind2.destroy()
        Scoreboard(self.Frame_main1_wind2, self.show_rules, "Snake", self.User_name, 60, 58)

    def quit_ranking(self):  # fonction pour quiter l'interface avec les regles et les scoreboards
        self.show_rules.destroy()
        self.show_rules.quit()

    def start(self):  # fonction d'initialisation
        try:
            self.Frame_right.destroy()  # destruction des frames
            self.Frame_left.destroy()
            self.Frame_top.destroy()
        except:
            pass
        self.root.protocol("WM_DELETE_WINDOW", self.exit)
        self.root.bind("<Return>", self.start_game)
        self.root.bind("<Key>", self.rotate)
        self.root.focus_force()
        self.grid = [[[0, 0, 0] for i in range(20)] for j in range(20)]
        # pour chaque élément de la grille, on a le temps de vie et la direction de la partie du serpent;
        # le troisième élément de la liste est utilisé pour les angles
        self.length_max = 2  # longeur du serpent
        self.fruit = Vector(-1, -1)  # position du fruit
        self.dir = Vector(1, 0)  # direction du serpent initialisée à droite
        self.next_Rotation = 0  # prochaine rotation, sélectionnée à droite aussi
        self.pos = Vector(0, 10)  # position actuelle du serpent
        self.grid[0][10] = [2, 0, 0]  # valeur de la grille à l'emplacement du serpent
        self.pause = True  # valeur de la pause

        #######-------------Import des photos------------####################################
        self.Snake_python = PhotoImage(file=resource_path("Snake/images/Snake_python.png"))
        self.bulle = PhotoImage(file=resource_path("Snake/images/bulle.png"))
        self.name_snake = PhotoImage(file=resource_path("Snake/images/name_snake.png"))

        ########------------Frames Pricipaux-------------########################################
        self.Frame_top = Frame(self.root, width=702, height=80, bg="black")
        self.Frame_right = Frame(self.root, width=502, height=502, bg="black")
        self.Frame_left = Frame(self.root, width=200, height=502, bg="black")

        ########-----------Frames Secondaires-----------######################################
        self.Frame1 = Frame(self.Frame_left, width=200, height=177, bg="black")
        self.Frame2 = Frame(self.Frame_left, width=200, height=325, bg="black")
        self.Canvas_Frame2 = Canvas(self.Frame2, width=190, height=316, bg="white")

        #######-----------Package des Frames-------------##################################

        self.Frame_top.pack(side=TOP)
        self.Frame_right.pack(side=RIGHT)
        self.Frame_left.pack(side=LEFT)
        self.Frame1.pack(side=TOP)
        self.Frame2.pack(side=BOTTOM)
        self.Canvas_Frame2.place(x=3, y=2)

        #########------------Labels et autres-----------##################################

        self.Button_quit = Button(
            self.Frame_top,
            text="QUIT",
            activebackground="#00cc00",
            foreground="#00cc00",
            bg="black",
            font=("Helvetica", 15),
            cursor="hand2",
            command=self.exit,
        )
        self.Button_quit.place(x=610, y=19)

        self.grille = Canvas(self.Frame_right, width=501, height=501, bg="#1a1a1a", highlightthickness=0)
        self.grille.place(x=0, y=0)

        self.Title_level = Label(self.Frame_top, bg="black", image=self.name_snake)
        self.Title_level.place(x=220, y=0)

        self.Canvas_Frame2.create_image(80, 240, image=self.Snake_python)
        self.Canvas_Frame2.create_image(103, 83, image=self.bulle)

        self.show_conseils = Label(
            self.Canvas_Frame2, text="Why do pythons live \n on land?  Because it's\n above C level.", bg="white", font=("Helvetica", 10)
        )
        self.show_conseils.place(x=38, y=50)

        self.Pause_Button = Button(
            self.Frame_top,
            text="PAUSE",
            activebackground="#00cc00",
            foreground="#00cc00",
            bg="black",
            font=("Helvetica", 15),
            cursor="hand2",
            command=self.pause_command,
        )
        self.Pause_Button.place(x=510, y=19)

        self.start_button = Button(
            self.Frame1, image=self.Start_image, cursor="hand2", bg="#00cc00", activebackground="black", command=self.start_game
        )
        self.start_button.place(x=50, y=15)

        self.Score = Label(
            self.Frame1, text="Score : 0", foreground="green2", background="black", relief=GROOVE, font=("Berlin Sans FB", 20)
        )
        self.Score.place(x=45, y=130)

        bestplayer = get_game_score_list("Snake")[0]
        self.best_label = Label(
            self.Frame_top, text="Meilleur joueur:\n{} avec {} points".format(bestplayer[0], int(bestplayer[1])), bg="black", fg="#00cc00"
        )  # je te laisse la mise en forme
        self.best_label.place(x=30, y=15)

        self.sweet()  # fonction pour placer le fruit

    def start_game(self, event=None):  # fonction appelée par le bouton commencer
        self.Frame_right.config(cursor="none")
        self.start_button["state"] = "disabled"
        self.pause = False  # pause est enlevée
        if self.pause == False:
            self.root.unbind("<Return>")
        self.update()  # le serpent bouge

    def pause_command(self, event=None):  # fonction pour mettre le bouton en pause
        if self.pause == False:  # si le jeu n'est pas en pause, on le pause
            self.root.unbind("<Key>")
            self.pause = True
            self.Frame_right.config(cursor="arrow")
        else:  # sinon, on le relance avec la fonction update
            self.pause = False
            self.Frame_right.config(cursor="none")
            self.update()

    def update(self):  # fonciton pour actualiser la position du serpent
        if self.pause == False:  # si la pause n'est pas enclenchée
            newX = self.pos.x + self.dir.x  # on prends les coordonées du peochain point
            newY = self.pos.y + self.dir.y
            self.grid[self.pos.x][self.pos.y] = [self.length_max, convert_dir(self.dir, True), self.next_Rotation]
            # définition de la pièce du corps juste après la tête pour lui appliquer une rotation

            if self.verif(newX, newY) == True:  # si la vérification renvois True
                self.pos = Vector(newX, newY)  # on assigne la prochaine position au serpent
                for i in range(20):
                    for j in range(20):
                        if self.grid[i][j][0]:  # chaque partie du serpent perds de la vie
                            self.grid[i][j][0] -= 1
                # si la prochaine rotation est différente de la direction actuelle, on lui atribue la direction actuelle
                if self.next_Rotation != convert_dir(self.dir, True):
                    self.next_Rotation = convert_dir(self.dir, True)
                self.grid[newX][newY] = [self.length_max, convert_dir(self.dir, True), convert_dir(self.dir, True)]
            else:
                self.dead()  # la la vérification renvois False, le joueur a perdu
        if self.pause == False:  # revérification car la fonction prends trop de temps à s'executer
            self.grille.delete("all")  # on régénère la grille en détruisant tout et en recréant tout

            for i in range(20):
                for j in range(20):
                    if self.grid[i][j][0] == 0:
                        self.grille.create_rectangle(i * 25, j * 25, (i + 1) * 25, (j + 1) * 25, outline="#1a1a1a", fill="#1a1a1a")

                    elif self.grid[i][j][0] == 1:
                        self.grille.create_image(i * 25 + 13, j * 25 + 13, image=self.Queue_Image[self.grid[i][j][1]])

                    elif self.grid[i][j][0] == self.length_max:
                        self.grille.create_image(i * 25 + 13, j * 25 + 13, image=self.Head_Image[self.grid[i][j][1]])

                    else:
                        self.grille.create_image(i * 25 + 13, j * 25 + 13, image=self.Body_Image[self.grid[i][j][2]])

            self.grille.create_rectangle(0, 0, 500, 500)

            self.grille.create_image(self.fruit.x * 25 + 13, self.fruit.y * 25 + 13, image=self.Fruit_Image)
            self.root.bind("<Key>", self.rotate)
            self.root.after(150, self.update)  # la fonction update s'éxécute toues les 150 ms soit 6.6 Fps

    def sweet(self):  # fonction pour placer un fruit
        verite = True
        while verite:  # tant qu'on a pas une position valide, on tire des emplacements
            x = randint(0, 19)
            y = randint(0, 19)
            # les conditions sont: pas à l'emplacement du joueur ni au même endroit que précédement
            if self.grid[x][y][0] == 0 and x != self.fruit.x and y != self.fruit.y:
                verite = False
                self.fruit = Vector(x, y)
            # pick a random cords
            # while cords isn't a snake part

    def verif(self, x, y):  # fonction de vérification si des coordonées sont valides
        # il faut que x et x soient compris dans les dimensions du tableau et qu'il n' ait pas de partie du serpent à cet endroit la
        if x < 0 or x > 19 or y < 0 or y > 19 or self.grid[x][y][0] != 0:
            return False  # si les conditions ne sont pas respectées, on revois False
        elif Vector(x, y) == self.fruit:  # si on arrive sur les coordonées du fruit
            for i in range(20):
                for j in range(20):
                    if self.grid[i][j][0]:  # on incrémente la vie de chaque parties de 1
                        self.grid[i][j][0] += 1
            self.length_max += 1  # on augmente la taille du serpent de 1
            self.Score["text"] = "Score : {}".format((self.length_max - 2) * 40)  # actualisation du score
            self.sweet()  # on replace un fruit
        return True  # revois de True si la case ne possède rien ou si le joueur a mangé un fruit

    def exit(self):  # si on décide de quiter la fenètre
        try:
            self.question.destroy()
            self.question.quit()
        except:
            pass
        self.pause = True  # on pause le jeu pour stopper la fonction update
        self.root.destroy()  # et on quite la fenetre principale
        self.root.quit()

    def rotate(self, event=None):  # fonction appelée par appuis d'une touche
        symb = event.keysym
        dir = -1  # initialisation de la direction à une valeur implosible
        if symb == "Right":  # série de if pour déterminer la direction suivant la touche pressée
            dir = 0
        elif symb == "Down":
            dir = 1
        elif symb == "Left":
            dir = 2
        elif symb == "Up":
            dir = 3
        if dir != -1:  # si la direction a été changée
            old = convert_dir(self.dir, True)  # on convertis l'ancienne direction
            if dir == old or dir == (old + 2) % 4:
                # si l'ancienne rotation est la même que la nouvelle à pi près, on finis la fonction car pas de changement
                return False
            else:  # sinon, calcul de l'index de la coudée
                if (dir == 0 and old == 1) or (dir == 3 and old == 2):
                    self.next_Rotation = 4
                elif (dir == 0 and old == 3) or (dir == 1 and old == 2):
                    self.next_Rotation = 5
                elif (dir == 1 and old == 0) or (dir == 2 and old == 3):
                    self.next_Rotation = 6
                elif (dir == 2 and old == 1) or (dir == 3 and old == 0):
                    self.next_Rotation = 7
                self.dir = convert_dir(dir)  # conversion de la nouvelle direction en matrice
        self.root.unbind("<Key>")

    def dead(self):
        self.Frame_right.config(cursor="arrow")
        self.count += 1
        self.death_pos.append((self.pos.x, self.pos.y))
        self.start_button["state"] = "disabled"  # si le joueur est mort
        self.Pause_Button["state"] = "disabled"  # on désactive le bouton de la pause
        self.pause = True  # on arrête la boucle du update
        if (self.length_max - 2) * 40 > self.Best_Score:  # si on a fait un meilleur score que l'ancien on l'enregistre
            self.Best_Score = (self.length_max - 2) * 40
        self.average_score.append((self.length_max - 2) * 40)
        self.canvas_question = Canvas(self.Frame2, width=196, height=325, highlightthickness=0, bg="black")
        self.canvas_question.place(x=2, y=0)
        self.canvas_question.create_image(100, 163, image=self.fond_ecran)
        self.canvas_question.create_text(93, 100, text="             Perdu !! \n Veux-tu recommencer ?", font=("Berlin Sans FB", 12))
        answer1 = Button(
            self.canvas_question, text=" Oui ", command=self.start, cursor="hand2", fg="white", bg="black", font=("Helvetica", 12)
        ).place(x=30, y=150)
        answer2 = Button(
            self.canvas_question, text=" Non ", command=self.exit, cursor="hand2", fg="white", bg="black", font=("Helvetica", 12)
        ).place(x=120, y=150)
        # sinon, on quitte l'application


def convert_dir(dir, mat=False):  # dir correspond à l'entrée et mat, si c'est une matrice ou non qui est entrée
    if mat == True:  # série de ifs pour faire la conversion
        if dir == Vector(1, 0):
            return 0
        elif dir == Vector(0, 1):
            return 1
        elif dir == Vector(-1, 0):
            return 2
        elif dir == Vector(0, -1):
            return 3
    else:
        if dir == 0:
            return Vector(1, 0)
        elif dir == 1:
            return Vector(0, 1)
        elif dir == 2:
            return Vector(-1, 0)
        elif dir == 3:
            return Vector(0, -1)


def Snake(User):  # fonction pour commencer le jeu
    jeux = snake(User)  # création de l'instance
    if jeux.count != 0:
        return (
            jeux.Best_Score,
            sum(jeux.average_score) / jeux.count,
            (time() - jeux.time_start) / jeux.count,
            jeux.count,
            jeux.death_pos,
        )  # renvois les données
    else:
        return (0, 0, 0, 0, [])
