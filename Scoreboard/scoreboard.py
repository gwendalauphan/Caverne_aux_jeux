from tkinter import *
sys.path.append('../')
from Reseau.client import *

class Scoreboard:
    def __init__(self, parent, root, jeux, User_name, posx = 60, posy = 45):
        self.parent = parent
        self.root = root
        self.root.title('Classement')
        self.root.focus_force()

        TopFrame = Frame(parent, width = 550, height = 425, relief = GROOVE) #frame contenant le scoreboard
        TopFrame.place(x = posx, y = posy)

        ranking_game = Label(TopFrame, text = 'Classement du jeu', font = ("Berlin Sans FB", 35), relief = GROOVE) #titre
        ranking_game.place(x = 90, y= 20 )

        players = get_game_score_list(jeux) #on obtient la liste des meilleurs joueurs sur le jeu lancé
        Label(TopFrame, text = "Rang" + " "*8 + "Nom" + " "*28 + "Score    " ,font = ("Helvetica",15), relief = GROOVE).place(x = 70, y = 90) #légende

        for i in range(len(players)): #pour chaque éléments de la liste recue, on affiche le pseudo et le score
            Label(TopFrame,text = "#{} :       {}".format(i+1, players[i][0]),font = ("Helvetica", 15)).place(x = 85, y = 120 +i*26)
            Label(TopFrame, text = "{}".format(str(int(players[i][1]))),font = ("Helvetica", 15)).place(x = 385, y = 120 +i*26)
        for i in range(10-len(players)): #si jamais la liste est plus petite que 10, on affiche des emplacements vides
            Label(TopFrame,text = "#{} :".format(i+1+len(players)),font = ("Helvetica", 15)).place(x = 85, y = 120 + 25*len(players) +i*26)

        User_score = get_player_score(User_name)

        Label(TopFrame, text = "Votre Score: {}".format(str(int(User_score[jeux]))) ,font = ("Helvetica",15), relief = GROOVE).place(x = 50, y = 390)
        Bouton_continue = Button(TopFrame, text = 'Continuer...-->',font = ("Berlin Sans FB", 15), cursor ='hand2' , command = self.quit_ranking)
        TopFrame.after(1000, lambda: Bouton_continue.place(x = 350,y = 380))


    def quit_ranking(self):
        self.root.destroy()
        self.root.quit()
