from tkinter import * #@UnusedWildImport
from tkinter.messagebox import *
from time import sleep
sys.path.append('../Reseau')
from Reseau.client import *
sys.path.append('../Scoreboard')
from Scoreboard.scoreboard import *
sys.path.append('../Vectors')
from Vectors.vector import *
from random import randrange
from Fantome.Ressources.data.map_ghost import*
from math import pi

class pong:
    def __init__(self, user):
        self.user = user
        self.show_rules = Toplevel()
        self.pressing = False
        self.score = 0
        self.launch = -1
        self.show_rules.title('Règles')
        self.show_rules.geometry('670x530')
        self.show_rules.resizable(False,False)
        self.show_rules.focus_force()
        self.show_rules.protocol("WM_DELETE_WINDOW", self.quit_ranking)

        self.Frame_main1_wind2 = Canvas(self.show_rules, bg = 'red', relief = GROOVE)
        self.Frame_main1_wind2.pack(ipadx = 670, ipady = 530)
        #self.Fond_Frame_main1_wind2 = PhotoImage(file = "thumbnail/Tete2.png")
        #self.Frame_main1_wind2.create_image(335,265,image =Fond_Frame_main1_wind2)
        self.Frame_main2_wind2 = Frame(self.Frame_main1_wind2,width = 550, height = 425, relief = GROOVE)
        self.Frame_main2_wind2.place(x = 60, y = 45)
        self.Rules = Label(self.Frame_main2_wind2, text = 'Les règles:', font = ("Berlin Sans FB", 23), relief = GROOVE)
        self.Rules.place(x = 200, y =5)

        #détail des rêgles

        self.Rules2 = Label(self.Frame_main2_wind2, text = "Le but est que Jerry puisse arriver \n\
        au fromage sans que Tom l'attrape. \n Pour cela tu pourras utiliser les flèches \n du keyboard afin de déplacer Jerry", font = ("Berlin Sans FB", 12))
        self.Frame_main2_wind2.after(500, lambda: self.Rules2.place(x = 40, y = 70))

        self.CANVAS1 = Canvas(self.Frame_main2_wind2, width = 120, height = 70)
        self.CANVAS2 = Canvas(self.Frame_main2_wind2, width = 100, height = 70)
        self.Frame_main2_wind2.after(1000, lambda: self.CANVAS1.place(x = 388, y = 35))
        self.Frame_main2_wind2.after(1000, lambda: self.CANVAS2.place(x = 400, y = 106))
        #self.CANVAS1.create_image(60, 35,image = self.Jerry_1)
        #self.CANVAS2.create_image(50, 35,image = self.keyboard_fantome)
        self.CANVAS2.create_rectangle(2,2,98,68, outline='black')

        #------------------2-----------------------------------------------------------------
        self.Rules3 = Label(self.Frame_main2_wind2, text = "Mais Attention !! Tom va plus vite que toi car il peut \n\
        se déplacer en diagonale. Tom se déplace par \n rapport à Jerry et fait tout pour se rapprocher." ,font = ("Berlin Sans FB", 12))
        self.Frame_main2_wind2.after(2000, lambda: self.Rules3.place(x = 30, y = 202))

        self.CANVAS3 = Canvas(self.Frame_main2_wind2,  width = 100, height = 100)
        self.Frame_main2_wind2.after(2500, lambda: self.CANVAS3.place(x = 400, y = 183 ))
        #self.CANVAS3.create_image(50,50, image = self.Jerry_3)

        #------------------3------------------------------------------------------------------
        self.Rules4 = Label(self.Frame_main2_wind2, text = "L'astuce est alors de bloquer le robot grâce\n\
        aux bloques disposés sur la carte",font = ("Berlin Sans FB", 12))
        self.Frame_main2_wind2.after(3500, lambda: self.Rules4.place(x = 40, y = 315))

        self.CANVAS4 = Canvas(self.Frame_main2_wind2, width = 130, height = 95)
        self.Frame_main2_wind2.after(4000, lambda: self.CANVAS4.place(x = 388, y = 293 ))
        #self.CANVAS4.create_image(65, 47,image = self.Jerry_2)

        #------------------Skip------------------------------------------------------------------
        self.Button_Skip = Button(self.Frame_main2_wind2, text = "-Skip-", cursor ='hand2', command = self.quit_rules)
        self.Button_Skip.place(x = 200, y = 390)
        self.show_rules.mainloop()

        """#################----------------- début du jeu ----------------#################### """
        self.root = Toplevel()
        self.root.geometry("902x552")
        self.root.protocol("WM_DELETE_WINDOW", self.exit)
        self.root.resizable(False,False)
        self.root.title('Pong')
        self.root.focus_force()

        ########-----------Frames Principaux------------#######################################
        self.Frame_left = Frame(self.root, width = 200, height = 500, bg = 'white')
        self.Frame_top = Frame(self.root, width = 700, height = 50, bg = 'lightgrey')

        ########-----------Frames Secondaires------------#######################################
        self.Frame1 = Frame(self.Frame_left, width = 200, height = 200)
        self.Frame2 = Frame(self.Frame_left, width = 200, height = 300, bg = 'black')

        #######-----------Package des Frames-------------####################################
        self.Frame_top.pack(side = TOP)
        self.Frame_left.pack(side = LEFT)
        self.Frame1.pack(side = TOP)
        self.Frame2.pack(side = BOTTOM)

        self.rayon = 75

        self.Frame_right = Frame(self.root, width = 700, height = 500, bg = 'white')
        self.Frame_right.pack(side = RIGHT)

        self.Canvas_dessine = Canvas(self.Frame_right, width = 700, height = 500, bg = "black", highlightthickness=0)
        self.Canvas_dessine.place(x = 0, y = 0)
        self.width = 700
        self.height = 500
        self.Best_Player = get_game_score_list("Pong")[0]

        self.start()

        self.root.mainloop()

    def start(self):
        self.root.bind("<KeyPress>", self.start_move)
        self.root.bind("<KeyRelease>", self.stop_move)
        self.Canvas_dessine.delete("all")
        self.run = True
        self.touch = 0
        self.speed = 0

        self.player = Board(10, self)
        self.bot = Board(self.width-10, self)
        self.ball = Ball(self)
        self.update()

    def start_move(self, event):
        if not(self.pressing):
            self.pressing = True
            self.move(event)

    def move(self, event):
        keyCode = event.keysym
        if self.player.pos.y + 50 < self.height and keyCode == "Down":
            self.player.pos.y += 7
        elif self.player.pos.y-50 > 0 and keyCode == "Up":
            self.player.pos.y -= 7
        if self.pressing == True:
            self.root.after(25, lambda: self.move(event))

    def stop_move(self, event):
        self.pressing = False

    def exit(self): #fonction appelée pour quiter l'application
        self.run = False
        self.root.destroy()
        self.root.quit()

    def quit_ranking(self): #fonction utilisée pour quitter l'interface des classements
        self.show_rules.destroy()
        self.show_rules.quit()

    def quit_rules(self): #fonction pour passer des regles au classement
        self.Frame_main2_wind2.destroy()
        Scoreboard(self.Frame_main1_wind2, self.show_rules, "Pong", self.user)

    def update(self):
        self.Canvas_dessine.delete("all")
        self.Canvas_dessine.create_text(290, 35, text = "Score actuel:", fill = "white", font = ("Helvetica", 10))
        self.Canvas_dessine.create_text(430, 35, text = "Meilleur score par {}:".format(self.Best_Player[0]), fill = "white", font = ("Helvetica", 10))

        best = str(int(self.Best_Player[1]/50))
        self.bestUnit = PhotoImage(file = "Pong/res/" + best[-1] + ".png")
        self.Canvas_dessine.create_image(435, 75, image = self.bestUnit)
        if len(best) > 1:
            self.bestDix = PhotoImage(file = "Pong/res/" + best[-2] + ".png")
            self.Canvas_dessine.create_image(410, 75, image = self.bestDix)
            if len(best) > 2:
                self.bestCent = PhotoImage(file = "Pong/res/" + best[-3] + ".png")
                self.Canvas_dessine.create_image(385, 75, image = self.bestCent)

        temp = str(self.touch)
        self.scoreUnit = PhotoImage(file = "Pong/res/" + temp[-1] + ".png")
        self.Canvas_dessine.create_image(300, 75, image = self.scoreUnit)
        if len(temp) > 1:
            self.scoreDix = PhotoImage(file = "Pong/res/" + temp[-2] + ".png")
            self.Canvas_dessine.create_image(275, 75, image = self.scoreDix)
            if len(temp) > 2:
                self.scoreCent = PhotoImage(file = "Pong/res/" + temp[-3] + ".png")
                self.Canvas_dessine.create_image(250, 75, image = self.scoreCent)

        self.Canvas_dessine.create_rectangle(2,2,698,498, outline = "white")
        self.Canvas_dessine.create_line(349,0,349,498, fill = "white", dash = (10,10))
        self.Canvas_dessine.create_oval(349-self.rayon, 249 - self.rayon, 349 + self.rayon, 249 + self.rayon,outline = 'white')
        if self.launch:
            self.ball.launch(self.launch)

        self.player.show()
        self.bot.show()
        self.ball.update()
        self.root.after(25, self.update)

    def dead(self, looser):
        self.launch = looser
        if self.touch > self.score:
            self.score = self.touch
        self.touch = 0

class Board:
    def __init__(self, x, parent):
        self.parent = parent
        self.pos = Vector(x, parent.height/2)

    def show(self):
        if self.pos.x > self.parent.width/2:
            gap = self.parent.ball.pos.y - self.pos.y
            if self.pos.y + gap/2 + 50 <= self.parent.height and self.pos.y + gap/2 - 50 >= 0:
                self.pos.y += gap#/10
        self.parent.Canvas_dessine.create_rectangle(self.pos.x-10, self.pos.y-50, self.pos.x+10, self.pos.y+50, fill = "white")


class Ball:
    def __init__(self, parent):
        self.pos = Vector(parent.width/2, parent.height/2)
        self.parent = parent

    def launch(self, direction):
        self.parent.launch = 0
        self.pos = Vector(self.parent.width/2, self.parent.height/2)
        self.vitesse = Vector(direction, 0)
        theta = randrange(-70,70)/100
        self.vitesse.rotate(theta)
        self.vitesse.setMag(4)

    def update(self):
        if self.pos.y + 20 > self.parent.height:
            self.vitesse.y *= -1
            self.pos.y = self.parent.height-20

        if self.pos.y-20 < 0:
            self.vitesse.y *= -1
            self.pos.y = 20

        if self.pos.x + 20 > self.parent.width-20:
            if self.parent.bot.pos.y - 55 > self.pos.y or self.pos.y > self.parent.bot.pos.y + 55:
                self.parent.dead(-1)
                return 0
            offset = self.parent.bot.pos.y - self.pos.y
            toApply = mapping(offset, -55, 55, 4, -4)
            toApply += randrange(-int(abs(self.vitesse.y/1.2)), int(abs(self.vitesse.y/1.2))+1) #un peux d'aléatoire...
            temp = self.vitesse.mag()
            self.vitesse.y += toApply
            self.vitesse.setMag(temp)

            self.vitesse.x *= -1
            self.pos.x = self.parent.width-40
            self.vitesse.setMag(self.vitesse.mag() + 0.5)
            if self.vitesse.mag() > 20:
                self.vitesse.setMag(20)

        elif self.pos.x-20 < 20:
            if self.parent.player.pos.y - 60 > self.pos.y or self.pos.y > self.parent.player.pos.y + 60:
                self.parent.dead(1)
                return 0
            offset = self.parent.player.pos.y - self.pos.y
            toApply = mapping(offset, -60, 60, 2, -2)
            temp = self.vitesse.mag()
            self.vitesse.y += toApply
            self.vitesse.setMag(temp)

            self.vitesse.x *= -1
            self.parent.touch += 1
            self.pos.x = 40
            self.vitesse.setMag(self.vitesse.mag() + 0.5)
            if self.vitesse.mag() > 20:
                self.vitesse.setMag(20)

        self.pos.add(self.vitesse)
        self.parent.Canvas_dessine.create_oval(self.pos.x-20, self.pos.y-20, self.pos.x+20, self.pos.y+20, fill = "white")

def mapping(value, istart, iend, ostart, oend): 
    return ostart + (oend - ostart) * ((value - istart)/(iend - istart))

def Pong(user):
    game = pong(user)
    return game.score*50
