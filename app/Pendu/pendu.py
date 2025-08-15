import sys
from tkinter import *  # @UnusedWildImport
from tkinter.messagebox import *
from time import sleep, time

sys.path.append("../Reseau")
from app.Reseau.client import *

sys.path.append("../Scoreboard")
from app.Scoreboard.scoreboard import *
from random import choice
from tkinter.font import Font
from app.Utils.utils import *

# difficulté: nombre de lettres différentes par mot: facile: <= 4, moyen: 4 < x < 8, difficile: >= 8
find = lambda mot, lettre: [i for i, car in enumerate(mot) if car == lettre]

accent = ["é", "è", "ê", "à", "ù", "û", "ç", "ô", "î", "ï", "â"]
sans_accent = ["e", "e", "e", "a", "u", "u", "c", "o", "i", "i", "a"]


class pendu:
    def __init__(self, user):
        self.user = user
        self.score = 0
        self.count = 0
        self.average_score = []
        with open(resource_path("Pendu/ressources/liste_francais.txt"), encoding="iso-8859-1") as f:
            self.data = f.read().lower().split("\n")
        # elements du pendu
        self.elements = [
            lambda: self.canvas.create_rectangle(50, 350, 150, 370, fill="sienna4"),
            lambda: self.canvas.create_rectangle(90, 350, 110, 50, fill="sienna4"),
            lambda: self.canvas.create_rectangle(110, 50, 350, 70, fill="sienna4"),
            lambda: self.canvas.create_polygon([(110, 120), (110, 150), (170, 70), (145, 70)], fill="sienna4"),
            lambda: self.canvas.create_rectangle(300, 71, 310, 110, fill="burlywood3", width=0),
            lambda: self.canvas.create_oval(290, 110, 320, 140, width=5, outline="tan1"),
            lambda: self.canvas.create_rectangle(302, 140, 307, 200, fill="tan1", outline="tan1"),
            lambda: self.canvas.create_polygon([(302, 160), (302, 165), (270, 135), (270, 130)], fill="tan1", outline="tan1"),
            lambda: self.canvas.create_polygon([(307, 160), (307, 166), (335, 136), (335, 130)], fill="tan1", outline="tan1"),
            lambda: self.canvas.create_polygon([(302, 192), (302, 200), (270, 237), (270, 230)], fill="tan1", outline="tan1"),
            lambda: self.canvas.create_polygon([(307, 192), (307, 200), (335, 237), (335, 230)], fill="tan1", outline="tan1"),
        ]

        for i in range(len(self.data)):
            self.data[i] = [self.data[i], letter_count(remove_accent(self.data[i]))]

        self.show_rules = Toplevel()
        self.show_rules.title("Règles")
        self.show_rules.geometry("670x530")
        self.show_rules.resizable(False, False)
        self.show_rules.focus_force()
        self.show_rules.protocol("WM_DELETE_WINDOW", self.quit_ranking)  # protocole pour controler la fermeture d ela fenetre

        self.level_easy = PhotoImage(file=resource_path("Minesweeper/Images/level_easy.png"))
        self.level_medium = PhotoImage(file=resource_path("Minesweeper/Images/level_medium.png"))
        self.level_hard = PhotoImage(file=resource_path("Minesweeper/Images/level_hard.png"))

        self.image1 = PhotoImage(file=resource_path("Pendu/ressources/rules1.png"))
        self.image3 = PhotoImage(file=resource_path("Pendu/ressources/rules2.png"))
        self.image4 = PhotoImage(file=resource_path("Pendu/ressources/rules3.png"))

        self.Frame_main1_wind2 = Canvas(self.show_rules, bg="red", relief=GROOVE)  # premier frame, celui en dessous
        self.Frame_main1_wind2.pack(ipadx=670, ipady=530)
        self.Frame_main2_wind2 = Canvas(self.Frame_main1_wind2, width=550, height=425, relief=GROOVE)  # second frame, au dessus
        self.Frame_main2_wind2.place(x=60, y=45)

        self.Fond_Frame_main1_wind2 = PhotoImage(file=resource_path("Pendu/ressources/image_fond.png"))
        self.Frame_main1_wind2.create_image(335, 265, image=self.Fond_Frame_main1_wind2)

        self.Rules = Label(self.Frame_main2_wind2, text="Les règles:", font=("Berlin Sans FB", 23), relief=GROOVE)
        self.Rules.place(x=200, y=5)

        first_label = Label(self.Frame_main2_wind2, text="Le but du jeu est de trouver le mot mystère")
        self.Frame_main2_wind2.after(1000, lambda: first_label.place(x=20, y=80))

        first_image = Label(self.Frame_main2_wind2, image=self.image1)
        self.Frame_main2_wind2.after(1500, lambda: first_image.place(x=350, y=75))

        second_label = Label(
            self.Frame_main2_wind2, text="Pour ce faire, tu peux proposer des lettres \n en espérant qu'elle appartient au mot"
        )
        self.Frame_main2_wind2.after(2500, lambda: second_label.place(x=20, y=170))

        third_image = Label(self.Frame_main2_wind2, image=self.image3)
        self.Frame_main2_wind2.after(3000, lambda: third_image.place(x=365, y=150))

        third_label = Label(
            self.Frame_main2_wind2,
            text="Mais attention, tu rentre une mauvaise lettre,\n le pendu apparait\n et tu perds au bout de 11 fautes",
        )
        self.Frame_main2_wind2.after(4000, lambda: third_label.place(x=20, y=290))

        fourth_image = Label(self.Frame_main2_wind2, image=self.image4)
        self.Frame_main2_wind2.after(4500, lambda: fourth_image.place(x=345, y=253))

        self.Button_Skip = Button(self.Frame_main2_wind2, text="-Skip-", cursor="hand2", command=self.quit_rules)
        self.Button_Skip.place(x=100, y=380)
        self.show_rules.mainloop()

        self.root = Toplevel()  # fenetre principale
        self.root.geometry("600x500")
        self.root.protocol("WM_DELETE_WINDOW", self.exit)
        self.root.resizable(False, False)
        self.root.title("Pendu")
        self.root.focus_force()
        self.root.withdraw()  # on masque la fenetre principale le temps de la sélection de la difficulté
        self.time_start = time()

        self.difficulty()  # on charge la difficulté
        self.root.mainloop()

    def exit(self):  # fonction appelée pour quiter l'application
        try:
            self.root_difficulty.destroy()
            self.root_difficulty.quit()
        except:
            pass
        self.root.destroy()
        self.root.quit()

    def quit_ranking(self):  # fonction utilisée pour quitter l'interface des classements
        self.show_rules.destroy()
        self.show_rules.quit()

    def quit_rules(self):  # fonction pour passer des regles au classement
        self.Frame_main2_wind2.destroy()
        Scoreboard(self.Frame_main1_wind2, self.show_rules, "Pendu", self.user)

    def difficulty(self):  # fonction de sélection de la difficulté
        self.count += 1
        self.root_difficulty = Toplevel()
        self.root_difficulty.resizable(False, False)
        self.root_difficulty.focus_force()
        self.root_difficulty.title("Selectionne une difficulté")
        self.root_difficulty.geometry("300x125")
        self.root_difficulty.protocol("WM_DELETE_WINDOW", print)
        # boutons avec les différentes difficultés
        Button(self.root_difficulty, image=self.level_easy, cursor="hand2", command=lambda: self.start(0)).place(x=15, y=27)
        Button(self.root_difficulty, image=self.level_medium, cursor="hand2", command=lambda: self.start(1)).place(x=115, y=27)
        Button(self.root_difficulty, image=self.level_hard, cursor="hand2", command=lambda: self.start(2)).place(x=215, y=27)
        self.root_difficulty.mainloop()

    def start(self, level):  # fontion appelée après la sélection de la difficulté avec level en paramètre
        self.entred = []
        self.root_difficulty.destroy()  # destruction de la fenetre de la difficulté
        self.root_difficulty.quit()
        self.level = level
        if level == 0:
            self.selection = [list[0] for list in self.data if 4 > list[1] and len(list[0]) > 3]
        elif level == 1:
            self.selection = [list[0] for list in self.data if 5 >= list[1] >= 4 and len(list[0]) > 3]
        elif level == 2:
            self.selection = [list[0] for list in self.data if list[1] > 5 and len(list[0]) > 3]
        self.word = choice(self.selection)  # mot a trouver
        self.word_accentless = remove_accent(self.word)  # mot a trouver sans les accents

        self.root.deiconify()
        self.root.focus_force()

        self.error_Count = 0
        self.canvas = Canvas(self.root, width=400, height=400, highlightthickness=0)
        self.canvas.place(x=200, y=100)
        start = ""
        for char in self.word:
            if char != " ":
                start += "_ "
            else:
                start += "  "
        self.result = Label(self.root, text="{}".format(start), font=Font(family="Helvetica", size=32, weight="bold"))
        self.result.place(x=30, y=20)

        self.entry = Entry(self.root)
        self.entry.place(x=30, y=200)
        self.entry.bind("<Return>", self.check)
        self.entry.focus()
        self.message_error_1 = Label(self.root, text="Tu dois saisir une seule lettre", fg="red")
        self.message_error_2 = Label(self.root, text="Lettre déjà saisie", fg="red")
        Button(self.root, text="Valider", cursor="hand2", command=self.check).place(x=160, y=195)

        self.Entered_Label = Label(self.root, text="")  # Label qui sert à voir les lettres qu'on a déjà entré
        self.Entered_Label.place(x=30, y=100)

    def check(self, event=None):
        lettre = self.entry.get().lower()  # On enregistre la lettre sasie avec la variable lettre
        self.entred.append(lettre)  # On la rajoute dans les lettre entrées
        self.message_error_1.place_forget()  # On efface le message d'erreur à chaque fois
        self.message_error_2.place_forget()  # On efface le message d'erreur à chaque fois
        self.entry.delete(0, len(lettre))  # On supprime à chaque fois ce que le joueur a écrit précédement
        if len(lettre) == 1:
            if lettre in self.word_accentless:  ####--- le joueur a trouvé une lettre alors: --###
                if lettre not in self.Entered_Label["text"]:  # On vérifie si la personne a déjà rentré la lettre
                    self.Entered_Label["text"] += " " + lettre  # On rajoute la lettre dans la liste des lettres fausses
                    old = self.result["text"]  # old est le text du label self.result
                    index = find(self.word_accentless, lettre)  # index est la position de la lettre trouvée dans le mot
                    for i in range(len(index)):  # len(index) est le nombre de lettres trouvées
                        self.result["text"] = (
                            old[: index[i] * 2] + self.word[index[i]] + old[index[i] * 2 + 1 :]
                        )  # le *2 sert aux espaces entre les lettres
                        #  old[:index[i]*2] représente ce qu'il y a avant la lettre trouvée
                        #  self.word[index[i]] est la lettre trouvée
                        #  old[index[i]*2+1:] représente ce qu'il y a après la lettre trouvée
                        old = self.result["text"]
                    if old.replace(" ", "") == self.word:  # Si le mot est fini:
                        self.end(True)  # Le joueur a gagné
                else:
                    self.message_error_2.place(x=30, y=230)
            else:  ####--- le joueur s'est trompé alors: --###
                if (
                    lettre not in self.Entered_Label["text"]
                ):  # On vérifie si la personne a déjà rentré la lettre et si elle fait un caractère
                    self.Entered_Label["text"] += " " + lettre  # On rajoute la lettre dans la liste des lettres fausses
                    self.elements[self.error_Count]()  # On rajoute un élément du pendu
                    self.error_Count += 1  # On incrémente le nombre d'erreurs
                    if self.error_Count == 11:  # Si le nombre d'erreurs = 11:
                        self.end(False)  # le joueur a perdu la partie
                elif lettre in self.entred:  # Si la lettre a déjà été entrée est trop longue
                    self.message_error_2.place(x=30, y=230)  # On lui envoie un message d'erreur
        else:
            self.message_error_1.place(x=30, y=230)

    def end(self, win):
        scored = (self.level + 1) * 50 * win * 2 * (len(self.entred) - self.error_Count) / (1 + self.error_Count)
        self.average_score.append(scored)
        if scored > self.score:
            self.score = scored
        self.entry.unbind("<Return>")

        mess = "\nVeux-tu recommencer ?"
        if win == False:
            mess = "Perdu! le mot était {}".format(self.word) + mess
        else:
            mess = "Gagné" + mess
        question = askquestion("Restart", mess)
        if question == "yes":  # si oui, on cache la fenete et on redemande la difficulté
            self.restart()
        else:
            self.exit()  # sinon on quite le jeu

    def restart(self):
        self.root.withdraw()
        for wg in self.root.winfo_children():
            wg.destroy()
        self.difficulty()


def remove_accent(word):
    for i in range(len(accent)):
        word = word.replace(accent[i], sans_accent[i])
    return word


def letter_count(word):
    lettre = []
    for letter in word:
        if letter not in lettre:
            lettre.append(letter)
    return len(lettre)


def Pendu(user):
    jeux = pendu(user)
    if jeux.count != 0:
        return (
            jeux.score,
            sum(jeux.average_score) / jeux.count,
            (time() - jeux.time_start) / jeux.count,
            jeux.count,
            [],
        )  # renvois du meilleur score
    else:
        return (0, 0, 0, 0, [])
