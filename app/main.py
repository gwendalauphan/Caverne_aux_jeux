from tkinter import *
from Reseau.client import *
from tkinter import font
import sys
import logging
sys.path.append('../')

from Tete_chercheuse.tete_chercheuse import *
from Snake.Snake_main import *
from Fantome.Fantome_main import *
from Minesweeper.minesweeper import *
from Pendu.pendu import *
from Tetris.tetris import *
from Pong.Pong_main import*
from Flappy_Bird.Flappy_Bird_main import*
from Stats.Page_selection import*
from Utils.utils import *

# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("CaverneAuxJeuxClient")

logger.info("The client app is running.")



class BoutonS: #classe pour gérer les boutons interactifs
    def __init__(self, x, y, jeux, run, name): # a besoin de ligne, colone, ne nom du jeux et la commande our executer le jeu
        self.image = PhotoImage(file = resource_path("thumbnail/" + jeux + ".png")) #on charge l'immage correspondante au jeu
        Frame_main.create_text(y*(450/5) + 20, x*(265/4)- 90, text = name, font = ("Berlin Sans FB", 20), fill = "white")
        self.created = Frame_main.create_image(y*(450/5) + 20, x*(265/4), image = self.image)
        Frame_main.tag_bind(self.created, "<Button-1>", self.command)
        self.jeux = jeux
        self.run = run

    def command(self, event = None): #fonction executée lors du clique sur le boutton
        global label_pseudo, label_score, score
        root_main.withdraw() #on masque l'interface principale
        max_score, score, Average_Time, count, death_pos = self.run(User_name) #on execute le jeu
        push_score(User_name, self.jeux, max_score, score, count, Average_Time, death_pos) #on envois au serveur le score de la partie
        root_main.deiconify() #on fait réapparaite la fenetre principale
        Frame_main['yscrollcommand'] = scrollY.set #rappel de la bare de scroll

        for label in label_score:
            label.destroy()
        for label in label_pseudo:
            label.destroy()

        score = get_score_list()

        label_pseudo = []
        label_score = []
        for i in range(len(score)): #pour chaque éléments de la liste recue, on affiche le pseudo et le score
            label_pseudo.append(Label(Frame_ranking,text = "#{} :       {}".format(i+1, score[i][0]),bg = '#111111', foreground = 'green2',font = ("Helvetica", 8)))
            label_pseudo[-1].place(x = 4, y = 75 +i*20)
            label_score.append(Label(Frame_ranking, text = "{}".format(str(int(score[i][1]))),bg = '#111111', foreground = 'green2',font = ("Helvetica", 8)))
            label_score[-1].place(x = 160, y = 75 +i*20)

        for i in range(10-len(score)): #si jamais la liste est plus petite que 10, on affiche des emplacements vides
            label_pseudo.append(Label(Frame_ranking,text = "#{} :".format(i+1+len(score)),bg = '#111111', foreground = 'green2',font = ("Helvetica", 8)))
            label_pseudo[-1].place(x = 4, y = 75 + 20*len(score) +i*20)

User_name = "Unknown"

with open(resource_path('Data/mots.txt'), 'r') as file:
    mots = file.read()
    mots_interdits = mots.split("\n")

def valider(event = None):
    global User_name
    temp = entry.get().replace(" ", "_")
    if temp == "" or len(temp) > 12:
        alert.place(x = 50, y = 100)
        return
    for elt in mots_interdits[:-1]:
        if elt in temp.lower():
            alert.place(x = 50, y = 100)
            return
    User_name = temp
    check_add_player(User_name)
    root_user.destroy()
    root_user.quit()

def para():
    playground = Canvas(root_main, highlightthickness = 0,width = 800, height = 500, bg = "#111111")
    playground.place(x = 200, y = 100)
    Button_para.config( image = door, command = lambda: leave_para(playground))
    text = "Le but de cette application est de s'ammuser en jouant a des jeux.\nTu peux défier tes amis en comparant leur score au tien\nsur différents jeux et essayer de faire le meilleur score possible."
    Label(playground, text = "Aide", font = ("Helvetica", 25), bg = "#111111", fg = "#888888").place(x = 300, y = 20)
    Label(playground, text = text, font = ("Helvetica", 10), bg = "#111111", fg = "#888888").place(x = 100, y = 60)

def execute(event = None):
    root_main.withdraw()
    app = Stats(User_name)
    root_main.deiconify()

        
    
    

def leave_para(playground):
    playground.destroy()
    Button_para.config(image = gearImg, command = para)

root_user = Tk()
root_user.geometry("300x120")
root_user.bind("<Return>", valider)
root_user.focus_force()

Label(root_user, text = "Entre un pseudo pour jouer").place(x = 100, y = 30)

entry = Entry(root_user)
entry.place(x = 25, y = 80)
entry.focus()

alert = Label(root_user, text = "Nom invalide", fg = "red")

confirm = Button(root_user, text = "valider",cursor ='hand2', command = valider)
confirm.place(x = 225, y = 80)

root_user.mainloop()

root_main = Tk()
root_main.geometry('1020x600')
root_main.title("Menu")
root_main.resizable(False,False)
root_main.focus_force()
#########################-----Création de la forme de la page----------------------#######################################
Frame_top = Frame(root_main, bg ='#111111') #création des pannels
Frame_top.pack(ipadx = 1000, ipady =50, side = TOP)

Frame_left = Frame(root_main, bg ='#111111')
Frame_left.pack(ipadx = 100, ipady =500,side = LEFT)

Frame_right = Frame(root_main, bg ='#111111')
Frame_right.pack(ipadx = 20, ipady = 600,side = RIGHT)

Frame_down = Frame(root_main, bg ='#111111')
Frame_down.pack(ipadx = 900, ipady = 20,side = BOTTOM)

image_de_fond = PhotoImage(file = resource_path("thumbnail/image_de_fond.png"))

Frame_main = Canvas(root_main,highlightthickness=0, borderwidth = 2, bg = '#111111', relief=GROOVE, scrollregion = (0, 0, 250, 1000))
Frame_main.pack(ipadx = 900, ipady =530,side = BOTTOM)
Frame_main.create_image(380, 537, image = image_de_fond)
#Frame_main.create_image(450,889, image = image_de_fond)

scrollY = Scrollbar(root_main, orient = "vertical", cursor = 'hand2', command = Frame_main.yview)
scrollY.place(x = 962, y = 102, height = 456)

Frame_main['yscrollcommand'] = scrollY.set
Frame_main.bind("<MouseWheel>", lambda event: Frame_main.yview_scroll(int(-1*(event.delta/120)), "units"))

Frame_ranking = Frame(Frame_left, width = 196 , height =280 , bg = '#111111', relief = GROOVE)
Frame_ranking.place(x = 2, y = 70)

gearImg = PhotoImage(file = resource_path('Parametters/gear.png'))
door = PhotoImage(file = resource_path("Parametters/door.png"))
image_stat = PhotoImage(file = resource_path("Parametters/image_stat.png"))

Button_para = Button(Frame_top, image = gearImg, bg = "#111111", borderwidth = 0, highlightthickness = 0, cursor = "hand2", command = para)
Button_para.place(x = 860, y = 25)
Button_stats = Button(Frame_top,image = image_stat, bg = "#111111", borderwidth = 0, highlightthickness = 0, cursor = "hand2", command = execute)
Button_stats.place(x = 930, y = 20)
score = get_score_list() #récupération du scoreboard

#############---------Création des labels et autres au contour du Frame_main-------#########################

Title_main = Label(Frame_top, text = 'La Caverne Aux Jeux',font = ("Berlin Sans FB", 45), bg ='#111111', foreground = '#00e600', relief = GROOVE)
Title_main.place(x = 205, y = 10)

Title_ranking = Label(Frame_ranking, text = 'Classements',font = ("Berlin Sans FB", 20), bg = '#111111', foreground = '#00e600', relief = GROOVE)
Title_ranking.place(x = 27, y = 5)

################---------Création du Classement-----------------------------################################
Label(Frame_ranking, text = "Rang" + " "*8 + "Nom" + " "*24 + "Score  " ,font = ("Helvetica",9), bg = '#111111', foreground = '#00e600', relief = GROOVE).place(x = 2, y = 50) #légende
label_pseudo = []
label_score = []
for i in range(len(score)): #pour chaque éléments de la liste recue, on affiche le pseudo et le score
    label_pseudo.append(Label(Frame_ranking,text = "#{} :       {}".format(i+1, score[i][0]),bg = '#111111', foreground = '#00e600',font = ("Helvetica", 8)))
    label_pseudo[-1].place(x = 4, y = 75 +i*20)
    label_score.append(Label(Frame_ranking, text = "{}".format(str(int(score[i][1]))),bg = '#111111', foreground = '#00e600',font = ("Helvetica", 8)))
    label_score[-1].place(x = 160, y = 75 +i*20)

for i in range(10-len(score)): #si jamais la liste est plus petite que 10, on affiche des emplacements vides
    label_pseudo.append(Label(Frame_ranking,text = "#{} :".format(i+1+len(score)),bg = '#111111', foreground = '#00e600',font = ("Helvetica", 8)))
    label_pseudo[-1].place(x = 4, y = 75 + 20*len(score) +i*20)

for i in range(9):
    Frame_main.rowconfigure(i, minsize = 30, pad = 20)
    Frame_main.columnconfigure(i, minsize = 25, pad = 10)

#############----------Création du tableau et des Labels du Frame_main--------------#################################

bouton_0 = BoutonS(2, 1, "Tete", Tete, "Tête chercheuse")
bouton_1 = BoutonS(2, 3, "Snake", Snake, "Snake")
bouton_2 = BoutonS(5, 3, "Ghost", Ghost, "Tom & Jerry")
bouton_3 = BoutonS(5, 5, "Minesweeper", Minesweeper, "Démineur")
bouton_4 = BoutonS(2, 5, "Pendu", Pendu, "Pendu")
bouton_5 = BoutonS(5, 1, "Tetris", Tetris, "Tetris")
bouton_6 = BoutonS(5, 7, "Pong", Pong, "Pong")
bouton_7 = BoutonS(2, 7, "Flappy", Flappy_Bird, "Flappy")


root_main.mainloop()

root_main.quit()