from tkinter import *  # @UnusedWildImport
import sys
from tkinter.messagebox import *
from tkinter.font import Font
from time import time

sys.path.append("../Reseau")
from app.Reseau.client import *

sys.path.append("../Scoreboard")
from app.Scoreboard.scoreboard import *

sys.path.append("../Vectors")
from app.Vectors.vector import *
from app.Tetris.tiles import *
from random import choice
from app.Utils.utils import *


class Tile:  # classe utilisée pour gérer les formes géométrique
    def __init__(self, pattern):
        self.pos = Vector(3, 0)  # position de la pièce, initiée au centre de la grille
        self.pattern = pattern[0]  # grille correspondant au placement des éléments
        self.letter = pattern[1]  # lettre correspondant à la forme
        self.index = 0  # index de la rotation
        self.lifetime = 0  # détaction de la fin du jeu

    def update(self, state, parent):  # fonction pour afficher la pièce à chaque mise à jour
        for i in range(4):
            for j in range(4):
                if (
                    self.pattern[self.index][i][j] != "_"
                ):  # on boucle dans le pattern et si on trouve autre chose que du vide (symbolisé par "_")
                    if state == 0:  # si on veut faire bouger la pièce, on l'actualise
                        parent.canvas.create_image(
                            (i + self.pos.x) * (parent.width / 10) + parent.width / 20,
                            (j + self.pos.y) * (parent.height / 22) + parent.height / 44,
                            image=parent.image_tiles[self.letter],
                        )
                        if self.verify(i, j, parent) == True:  # et on vérifie si elle peut desscendre
                            return 0  # si elle ne peut pas, on arrete la fonction
                    elif state == 2:  # si on veut seulement l'afficher
                        parent.canvas.create_image(
                            (i + self.pos.x) * (parent.width / 10) + parent.width / 20,
                            (j + self.pos.y) * (parent.height / 22) + parent.height / 44,
                            image=parent.image_tiles[self.letter],
                        )
                    else:  # si on veut l'afficher sur le côté, pour la prochaine pièce
                        parent.next_Canvas.create_image(
                            i * parent.width / 10 + parent.width / 20,
                            j * parent.height / 22 + parent.height / 44,
                            image=parent.image_tiles[self.letter],
                        )
        if state == 0:  # si on veut le déplacer
            self.pos.y += 1  # on le fait déscendre
            self.lifetime += 1  # on incrémente sa durée de vie, le joueur n'a pas perdus

    def verify(self, x, y, parent):  # fonction de vérification si on vient de compléter une ligne
        testX = x + int(self.pos.x)  # calcul des coordonées à tester pour la prochaine chute
        testY = y + int(self.pos.y) + 1
        if testY == 22 or parent.grid[testX][testY] != "":  # si on atteind le bas de la fenetre ou que la prochaine case n'est pas vide
            for i in range(4):
                for j in range(4):
                    if self.pattern[self.index][i][j] != "_":  # pour chaque cases du pattern si cette case n'est pas vide
                        parent.grid[int(i + self.pos.x)][int(self.pos.y + j)] = self.pattern[self.index][i][
                            j
                        ]  # on atribue à la grid les cases du pattern
            rowCount = 0  # variable pour compter le nombre de lignes completées
            j = 0
            while j < 22:  # on boucle dans chaque ligne
                row = True  # on initialise à vrai
                for i in range(10):  # pour chaque cases de la liste on vérifie si il n'est pas vide
                    if parent.grid[i][j] == "":
                        row = False  # si il est vide, on passe row à False
                if row == True:
                    rowCount += 1
                    for k in range(10):
                        parent.grid[k][j] = ""
                    for k in range(j, 0, -1):
                        for i in range(10):
                            parent.grid[i][k] = parent.grid[i][k - 1]
                    j -= 1
                j += 1
            if rowCount == 1:
                parent.score += 4 * (parent.speed // 2 + 1)
            elif rowCount == 2:
                parent.score += 10 * (parent.speed // 2 + 1)
            elif rowCount == 3:
                parent.score += 30 * (parent.speed // 2 + 1)
            elif rowCount == 4:
                parent.score += 120 * (parent.speed // 2 + 1)
            if parent.score > parent.Best_score:
                parent.Best_score = parent.score

            if rowCount and parent.Total_Row % 10 + rowCount >= 10:
                parent.speed += 2

            parent.Total_Row += rowCount
            parent.aff_level["text"] = "Level = {}".format(int((parent.speed) / 2 + 1))
            parent.aff_score["text"] = "Score = {}".format(parent.score)
            parent.current = parent.next
            parent.next = Tile(choice([(L, "L"), (J, "J"), (I, "I"), (O, "O"), (Z, "Z"), (S, "S"), (T, "T")]))
            parent.next_Canvas.delete("all")

            if self.lifetime == 0:
                parent.run = False
                parent.end()
            return True
        return False

    def border(self, coeff, parent):
        for i in range(4):
            for j in range(4):
                if self.pattern[self.index][i][j] != "_":
                    if (
                        i + self.pos.x + coeff == 10
                        or j + self.pos.y == 22
                        or i + self.pos.x + coeff == -1
                        or parent.grid[int(self.pos.x) + i + coeff][int(self.pos.y) + j] != ""
                    ):
                        return False
        return True

    def check(self, parent):
        toTry = (self.index + 1) % len(self.pattern)
        for i in range(4):
            for j in range(4):
                if self.pattern[toTry][i][j] != "_" and (
                    (self.pos.x + i == 10 or self.pos.x == -1) or parent.grid[self.pos.x + i][self.pos.y + j] != ""
                ):
                    return False
        return True


class tetris:
    def __init__(self, user):
        self.user = user
        self.Best_score = 0
        self.height = 420  # modulable
        self.width = 220
        self.paused = False
        self.average_score = []
        self.count = 0

        self.show_rules = Toplevel()
        self.show_rules.title("Règles")
        self.show_rules.geometry("670x530")
        self.show_rules.resizable(False, False)
        self.show_rules.protocol("WM_DELETE_WINDOW", self.quit_ranking)  # protocole pour controler la fermeture d ela fenetre
        self.show_rules.focus_force()

        self.Frame_main1_wind2 = Canvas(self.show_rules, bg="red", relief=GROOVE)  # premier frame, celui en dessous
        self.Frame_main1_wind2.pack(ipadx=670, ipady=530)
        self.Fond_Frame_main1_wind2 = PhotoImage(file=resource_path("thumbnail/Tetris2.png"))
        self.Frame_main1_wind2.create_image(335, 265, image=self.Fond_Frame_main1_wind2)
        self.Frame_main2_wind2 = Frame(self.Frame_main1_wind2, width=550, height=425, relief=GROOVE)  # second frame, au dessus
        self.Frame_main2_wind2.place(x=60, y=45)

        first_label = Label(
            self.Frame_main2_wind2,
            text="Tu disposes de pièces qui descendent du ciel\n pour intéragir, tu peux utiliser\n les touches directionelles",
        )
        self.Frame_main2_wind2.after(1000, lambda: first_label.place(x=20, y=80))

        self.image1 = PhotoImage(file=resource_path("Tetris/Images/rules1.png"))
        first_image = Label(self.Frame_main2_wind2, image=self.image1)
        self.Frame_main2_wind2.after(1500, lambda: first_image.place(x=380, y=57))

        second_label = Label(
            self.Frame_main2_wind2, text="La flèche du haut fait tourner la pièce\n et les autres dirigent la pièce suivant la direction"
        )
        self.Frame_main2_wind2.after(2500, lambda: second_label.place(x=20, y=170))

        self.image3 = PhotoImage(file=resource_path("Tetris/Images/rules2.png"))
        third_image = Label(self.Frame_main2_wind2, image=self.image3)
        self.Frame_main2_wind2.after(3000, lambda: third_image.place(x=380, y=200))

        third_label = Label(self.Frame_main2_wind2, text="Tu gagnes des points lorsque tu complètes des lignes")
        self.Frame_main2_wind2.after(4000, lambda: third_label.place(x=20, y=230))

        fourth_label = Label(self.Frame_main2_wind2, text="Mais attention, si le tas atteints le haut,\n tu as perdu!!!")
        self.Frame_main2_wind2.after(4500, lambda: fourth_label.place(x=200, y=300))

        self.Button_Skip = Button(self.Frame_main2_wind2, text="-Skip-", cursor="hand2", command=self.quit_rules)
        self.Button_Skip.place(x=30, y=370)

        self.show_rules.mainloop()

        self.root = Toplevel()
        self.root.geometry("420x420")
        self.root.protocol("WM_DELETE_WINDOW", self.exit)
        self.root.title("Tetris")
        self.root.configure(background="#31363b")
        self.root.resizable(False, False)
        self.root.focus_force()
        self.image_tiles = {
            "I": PhotoImage(file=resource_path("Tetris/Images/I.png")),
            "L": PhotoImage(file=resource_path("Tetris/Images/L.png")),
            "O": PhotoImage(file=resource_path("Tetris/Images/O.png")),
            "J": PhotoImage(file=resource_path("Tetris/Images/J.png")),
            "Z": PhotoImage(file=resource_path("Tetris/Images/Z.png")),
            "S": PhotoImage(file=resource_path("Tetris/Images/S.png")),
            "T": PhotoImage(file=resource_path("Tetris/Images/T.png")),
        }

        Label(self.root, text="Tetris", font=Font(size=35)).place(x=260, y=30)
        Label(self.root, text="Next:", font=Font(size=25)).place(x=272, y=180)
        self.aff_score = Label(self.root, text="Score = 0", font=Font(size=20))
        self.aff_score.place(x=245, y=130)
        self.aff_level = Label(self.root, text="Level = 1", font=Font(size=20))
        self.aff_level.place(x=245, y=90)

        bestplayer = get_game_score_list("Tetris")[0]
        self.best_label = Label(
            self.root, text="Meilleur joueur:\n{} avec {} points".format(bestplayer[0], int(bestplayer[1]))
        )  # je te laisse la mise en forme
        self.best_label.place(x=245, y=350)

        self.time_start = time()
        self.start()

        self.root.mainloop()

    def exit(self):  # fonction appelée pour quiter l'application
        self.run = False
        self.root.destroy()
        self.root.quit()

    def quit_ranking(self):  # fonction utilisée pour quitter l'interface des classements
        self.show_rules.destroy()
        self.show_rules.quit()

    def quit_rules(self):  # fonction pour passer des regles au classement
        self.Frame_main2_wind2.destroy()
        Scoreboard(self.Frame_main1_wind2, self.show_rules, "Tetris", self.user)

    def start(self):
        self.count += 1
        self.root.bind("<Key>", self.KeyPressed)
        self.canvas = Canvas(self.root, width=self.width, height=self.height, bg="grey", highlightthickness=0)
        self.next_Canvas = Canvas(self.root, width=4 * self.width / 10, height=4 * self.height / 22, bg="#31363b")
        self.next_Canvas.place(x=270, y=230)
        self.canvas.place(x=0, y=0)
        self.grid = [["" for i in range(22)] for j in range(10)]
        self.current = Tile(choice([(L, "L"), (J, "J"), (I, "I"), (O, "O"), (Z, "Z"), (S, "S"), (T, "T")]))
        self.next = Tile(choice([(L, "L"), (J, "J"), (I, "I"), (O, "O"), (Z, "Z"), (S, "S"), (T, "T")]))
        self.run = True
        self.speed = 0
        self.score = 0
        self.Total_Row = 0
        self.frame_count = 0
        self.update()

    def update(self):
        if self.run == True:
            self.frame_count += 1
            if self.frame_count % int((35 - self.speed) / 3) == 0:
                self.current.update(0, self)
            self.canvas.delete("all")
            for i in range(len(self.grid)):
                for j in range(len(self.grid[i])):
                    if self.grid[i][j] != "":
                        self.canvas.create_image(
                            i * (self.width / 10) + self.width / 20,
                            j * (self.height / 22) + self.height / 44,
                            image=self.image_tiles[self.grid[i][j]],
                        )
            self.ghost()
            self.current.update(2, self)
            self.next.update(1, self)
            self.root.after(40, self.update)

    def ghost(self):  # fonction pour afficher l'apperçus en bas de la fenetre
        offset = 0
        search = True
        while search:
            for i in range(4):
                for j in range(4):
                    if self.current.pattern[self.current.index][i][j] != "_":
                        x = i + int(self.current.pos.x)
                        y = j + int(self.current.pos.y) + offset
                        if y == 22 or self.grid[x][y] != "":
                            offset -= 2
                            search = False
            offset += 1
        for i in range(4):
            for j in range(4):
                if self.current.pattern[self.current.index][i][j] != "_":
                    self.canvas.create_rectangle(
                        (self.current.pos.x + i) * (self.width / 10),
                        (self.current.pos.y + offset + j) * (self.height / 22),
                        (self.current.pos.x + 1 + i) * (self.width / 10),
                        (self.current.pos.y + 1 + j + offset) * (self.height / 22),
                        fill="darkgrey",
                        width=0,
                    )

    def KeyPressed(self, event):
        if event.keysym == "space":
            if self.run == True:
                self.run = False
            else:
                self.run = True
                self.update()
        keyCode = event.keysym
        if self.run == True:
            if keyCode == "Down":
                self.current.update(0, self)

            elif keyCode == "Right":
                if self.current.border(1, self) == True:
                    self.current.pos.x += 1

            elif keyCode == "Left":
                if self.current.border(-1, self) == True:
                    self.current.pos.x -= 1

            elif keyCode == "Up":
                if self.current.check(self) == True:
                    self.current.index = (self.current.index + 1) % len(self.current.pattern)

    def end(self):
        self.average_score.append(self.score)
        self.root.unbind("<Key>")
        question = askquestion("RESTART", "La partie est finie\n veux-tu recommencer?")
        if question == "yes":
            self.canvas.destroy()
            self.next_Canvas.destroy()
            self.start()
        else:
            self.exit()


def Tetris(user):
    jeux = tetris(user)
    if jeux.count != 0:
        return (
            jeux.Best_score,
            sum(jeux.average_score) / jeux.count,
            (time() - jeux.time_start) / jeux.count,
            jeux.count,
            [],
        )  # renvois les données
    else:
        return (0, 0, 0, 0, [])
