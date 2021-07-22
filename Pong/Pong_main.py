from tkinter import * #@UnusedWildImport
from tkinter.messagebox import *
from time import sleep, time
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
        self.show_rules.title('Règles')
        self.show_rules.geometry('670x530')
        self.show_rules.resizable(False,False)
        self.show_rules.focus_force()
        self.show_rules.protocol("WM_DELETE_WINDOW", self.quit_ranking)

        self.image1 = PhotoImage(file = "Pong/res/first_image.png")
        self.image2 = PhotoImage(file = "Pong/res/second_image.png")
        self.image3 = PhotoImage(file = "Pong/res/third_image.png")


        self.Frame_main1_wind2 = Canvas(self.show_rules, bg = 'white', relief = GROOVE)
        self.Frame_main1_wind2.pack(ipadx = 670, ipady = 526)
        self.Fond_Frame_main1_wind2 = PhotoImage(file = "Pong/res/regles_pong.png")
        self.Frame_main1_wind2.create_image(335,263,image =self.Fond_Frame_main1_wind2)
        self.Frame_main2_wind2 = Frame(self.Frame_main1_wind2,width = 550, height = 425, relief = GROOVE)
        self.Frame_main2_wind2.place(x = 60, y = 45)
        self.Rules = Label(self.Frame_main2_wind2, text = 'Les règles:', font = ("Berlin Sans FB", 23), relief = GROOVE)
        self.Rules.place(x = 200, y =5)

        first_label = Label(self.Frame_main2_wind2, text = "Le but du jeu est de renvoyer la \n balle le plus longtemps possible, \n tu dois alors déplacer la table verticalement")
        self.Frame_main2_wind2.after(1000, lambda: first_label.place(x = 20, y = 80))

        first_image = Label(self.Frame_main2_wind2, image = self.image1)
        self.Frame_main2_wind2.after(1500, lambda: first_image.place(x = 360, y = 57))

        second_label = Label(self.Frame_main2_wind2, text = "La balle peut aussi rebondir sur les murs, \n il te faut alors prévoir sa trajectoire")
        self.Frame_main2_wind2.after(2500, lambda: second_label.place(x = 20, y = 190))

        third_image = Label(self.Frame_main2_wind2, image = self.image2)
        self.Frame_main2_wind2.after(3500, lambda: third_image.place(x = 360, y = 180))

        third_label = Label(self.Frame_main2_wind2, text = "Tu dois donc tenir le plus longtemps \n avec la balle qui change de directions")
        self.Frame_main2_wind2.after(4000, lambda: third_label.place(x = 20, y = 290))

        fourth_image = Label(self.Frame_main2_wind2, image = self.image3)
        self.Frame_main2_wind2.after(4500, lambda: fourth_image.place(x = 325, y = 305))

        self.Button_Skip = Button(self.Frame_main2_wind2, text = "-Skip-", cursor ='hand2', command = self.quit_rules)
        self.Button_Skip.place(x = 150, y = 370)
        self.show_rules.mainloop()
        """#################----------------- début du jeu ----------------#################### """
        self.root = Toplevel()
        self.root.geometry("902x552")
        self.root.protocol("WM_DELETE_WINDOW", self.exit)
        self.root.resizable(False,False)
        self.root.title('Pong')
        self.root.focus_force()
        self.pressing = False
        self.score = 0
        self.launch = -1
        self.count = 0
        self.death_pos = []
        self.average_score = []


        ##########-----------Import des photos------------------###############################
        self.raquette_pong = PhotoImage(file = "Pong/res/raquette_pong.png")
        self.button_start_image = PhotoImage(file = "Pong/res/button_start.png")
        self.title_pong = PhotoImage(file = "Pong/res/title_pong.png")
        self.femme_pong = PhotoImage(file = "Pong/res/femme_pong.png")

        ########-----------Frames Principaux------------#######################################
        self.Frame_left = Frame(self.root, width = 200, height = 500, bg = 'white')
        self.Frame_top = Frame(self.root, width = 900, height = 50, highlightthickness=0, bg = 'black')

        ########-----------Frames Secondaires------------#######################################
        self.Frame1 = Canvas(self.Frame_left, width = 200, height = 200, bg = 'black')
        self.Frame2 = Frame(self.Frame_left, width = 200, height = 300, bg = 'black')
        self.Frame_right = Frame(self.root, width = 700, height = 500,  highlightthickness=0,bg = 'black')
        #######-----------Package des Frames-------------####################################
        self.Frame_top.pack(side = TOP)
        self.Frame_left.pack(side = LEFT)
        self.Frame1.pack(side = TOP)
        self.Frame2.pack(side = BOTTOM)
        self.Frame_right.pack(side = RIGHT)

        ########-------------Différents Canvas--------------------#############################
        self.Frame_main_game = Canvas(self.Frame2, width = 200, height = 300, bg = 'black', highlightthickness=0)
        self.Canvas_dessine = Canvas(self.Frame_right, width = 700, height = 500, bg = "black", highlightthickness=0)

        self.Frame_main_game.place(x = 0, y = 0)
        self.Canvas_dessine.place(x = 0, y = 0)

        #######----------Dessins-----------####################
        self.Frame_main_game.create_image(100,150, image = self.raquette_pong)

        self.Image_femme_pong = Label(self.Frame_top, image = self.femme_pong, bg= 'black', borderwidth = 0)
        self.Image_femme_pong.place(x = 140, y = 0)

        self.Image_title = Label(self.Frame_top, image = self.title_pong, borderwidth = 0)
        self.Image_title.place(x = 456,y = 0)

        self.rayon = 75
        self.width = 700
        self.height = 500
        self.Best_Player = get_game_score_list("Pong")[0]

        self.time_start = time()
        self.start()

        self.root.mainloop()

    def start(self):
        self.count += 1
        self.Canvas_dessine.delete("all")

        self.start_button = Button(self.Frame1, image = self.button_start_image, borderwidth = 0, relief = FLAT, bg = 'black', cursor ='hand2',activebackground = 'black', highlightthickness = 0,  command = self.resume)
        self.start_button.place(x = 39, y = 40)

        self.Pause_Button = Button(self.Frame_top, text = "PAUSE", font = ("Helvetica", 15),fg = 'white', bg = 'black', borderwidth = 0, relief = FLAT, cursor ='hand2', command = self.pause_command)
        self.Pause_Button.place(x = 720, y = 8)

        self.Quit_button = Button(self.Frame_top, text = 'QUIT',font = ("Helvetica", 15),fg = 'white', bg = 'black', borderwidth = 0, relief = FLAT, cursor ='hand2', command = self.exit)
        self.Quit_button.place(x = 820, y = 8)

        self.run = True
        self.touch = 0
        self.speed = 0
        self.paused = True

        self.player = Board(10, self)
        self.bot = Board(self.width-10, self)
        self.ball = Ball(self)

        self.root.bind("<Return>", self.resume)
        self.root.bind("<space>", self.pause_command)
        self.update()

        self.start_button.configure(state = "normal")

    def resume(self, event = None):
        if self.paused == True:
            self.paused = False
            self.root.bind("<KeyPress>", self.start_move)
            self.root.bind("<KeyRelease>", self.stop_move)
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
        self.start_button.configure(state = "disabled")
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
        if self.paused == False:
            self.root.after(25, self.update)

    def pause_command(self, event = None):
        if self.paused == False:
            self.start_button.configure(state = "normal")
            self.root.unbind("<KeyPress>")
            self.root.unbind("KeyRelease")
            self.paused = True
        else:
            self.paused = False
            self.root.bind("<KeyPress>", self.start_move)
            self.root.bind("<KeyRelease>", self.stop_move)
            self.update()

    def dead(self, looser):
        self.start_button.configure(state = "normal")
        self.paused = True
        self.average_score.append(self.touch * 50)
        self.death_pos.append((0, self.player.pos.y/self.height))
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
        self.vitesse.setMag(10)

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
            toApply += randrange(-int(abs(self.vitesse.y)), int(abs(self.vitesse.y))+1) #un peux d'aléatoire...
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
    jeux = pong(user)
    return (jeux.score*50, sum(jeux.average_score)/jeux.count, (time()-jeux.time_start)/jeux.count, jeux.count, jeux.death_pos)   #renvois les données
