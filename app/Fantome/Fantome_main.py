import sys
from tkinter import * #@UnusedWildImport
from tkinter.messagebox import *
from time import sleep, time
sys.path.append('../Reseau')
from Reseau.client import *
sys.path.append('../Scoreboard')
from Scoreboard.scoreboard import *
from random import randint
from Fantome.Ressources.data.map_ghost import*
from math import*
from Utils.utils import *


class ghost:
    def __init__(self, user):

        self.User_name = user
        self.show_rules = Toplevel()
        self.show_rules.title('Règles')
        self.show_rules.geometry('670x530')
        self.show_rules.resizable(False,False)
        self.show_rules.focus_force()
        self.show_rules.protocol("WM_DELETE_WINDOW", self.quit_ranking)
        self.level = 1
        self.score = 0
        self.count = 1

        self.Jerry_1 = PhotoImage(file = resource_path("Fantome/Ressources/Images/Jerry_1.png"))
        self.keyboard_fantome = PhotoImage(file = resource_path("Fantome/Ressources/Images/keyboard_fantome.png"))
        self.Jerry_3 = PhotoImage(file = resource_path("Fantome/Ressources/Images/Jerry_3.png"))
        self.Jerry_2 = PhotoImage(file = resource_path("Fantome/Ressources/Images/Jerry_2.png"))

        self.main = PhotoImage(file = resource_path("Parametters/main2.png"))
        self.next_image = PhotoImage(file = resource_path("Parametters/next2.png"))
        self.fond_ecran = PhotoImage(file = resource_path("Parametters/fond_ecran.png"))
        self.replay = PhotoImage(file = resource_path("Parametters/replay2.png"))

        self.Frame_main1_wind2 = Canvas(self.show_rules, bg = 'red', relief = GROOVE)
        self.Frame_main1_wind2.pack(ipadx = 670, ipady = 526)
        self.Fond_Frame_main1_wind2 = PhotoImage(file = resource_path("thumbnail/Ghost2.png"))
        self.Frame_main1_wind2.create_image(335,263,image =self.Fond_Frame_main1_wind2)
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
        self.CANVAS1.create_image(60, 35,image = self.Jerry_1)
        self.CANVAS2.create_image(50, 35,image = self.keyboard_fantome)
        self.CANVAS2.create_rectangle(2,2,98,68, outline='black')

    #------------------2-----------------------------------------------------------------
        self.Rules3 = Label(self.Frame_main2_wind2, text = "Mais Attention !! Tom va plus vite que toi car il peut \n\
        se déplacer en diagonale. Tom se déplace par \n rapport à Jerry et fait tout pour se rapprocher." ,font = ("Berlin Sans FB", 12))
        self.Frame_main2_wind2.after(2000, lambda: self.Rules3.place(x = 30, y = 202))

        self.CANVAS3 = Canvas(self.Frame_main2_wind2,  width = 100, height = 100)
        self.Frame_main2_wind2.after(2500, lambda: self.CANVAS3.place(x = 400, y = 183 ))
        self.CANVAS3.create_image(50,50, image = self.Jerry_3)

    #------------------3------------------------------------------------------------------
        self.Rules4 = Label(self.Frame_main2_wind2, text = "L'astuce est alors de bloquer le robot grâce\n\
        aux bloques disposés sur la carte",font = ("Berlin Sans FB", 12))
        self.Frame_main2_wind2.after(3500, lambda: self.Rules4.place(x = 40, y = 315))
#
        self.CANVAS4 = Canvas(self.Frame_main2_wind2, width = 130, height = 95)
        self.Frame_main2_wind2.after(4000, lambda: self.CANVAS4.place(x = 388, y = 293 ))
        self.CANVAS4.create_image(65, 47,image = self.Jerry_2)

    #------------------Skip------------------------------------------------------------------
        self.Button_Skip = Button(self.Frame_main2_wind2, text = "-Skip-", cursor ='hand2', command = self.quit_rules)
        self.Button_Skip.place(x = 200, y = 390)
        self.show_rules.mainloop()

        """#################----------------- début du jeu ----------------#################### """
        self.root = Toplevel()
        self.root.geometry("700x550")
        self.root.protocol("WM_DELETE_WINDOW", self.exit)
        self.root.resizable(False,False)
        self.root.title('Tom vs Jerry')
        self.root.focus_force()
        ########---------Import Photos interface----------###########################
        self.Tom_vs_Jerry = PhotoImage(file = resource_path("Fantome/Ressources/Images/Tom_vs_Jerry.png"))
        #########-----------Import des photos-------------#################################
        self.Jerry_image = PhotoImage(file = resource_path("Fantome/Ressources/Images/Jerry.png"))
        self.Tom_image_left = PhotoImage(file = resource_path("Fantome/Ressources/Images/Tom_left.png"))
        self.Tom_image_right = PhotoImage(file = resource_path("Fantome/Ressources/Images/Tom_right.png"))
        self.Fromage_image = PhotoImage(file = resource_path("Fantome/Ressources/Images/fromage.png"))
        self.Fromage_Jerry_image = PhotoImage(file = resource_path("Fantome/Ressources/Images/Fromage_Jerry.png"))
        self.Tom_right_image = PhotoImage(file = resource_path("Fantome/Ressources/Images/Tom_Jerry.png"))
        #######-----------Images en Mini-----------------####################################
        self.Jerry_image_mini = PhotoImage(file = resource_path("Fantome/Ressources/Images/Jerry_mini.png"))
        self.Tom_image_left_mini = PhotoImage(file = resource_path("Fantome/Ressources/Images/Tom_left_mini.png"))
        self.Tom_image_right_mini = PhotoImage(file = resource_path("Fantome/Ressources/Images/Tom_right_mini.png"))
        self.Fromage_image_mini = PhotoImage(file = resource_path("Fantome/Ressources/Images/fromage_mini.png"))
        self.Fromage_Jerry_image_mini = PhotoImage(file = resource_path("Fantome/Ressources/Images/Fromage_Jerry_mini.png"))
        self.Tom_right_image_mini = PhotoImage(file = resource_path("Fantome/Ressources/Images/Tom_Jerry_mini.png"))

        ########-----------Frames Principaux------------#######################################
        self.Frame_left = Frame(self.root, width = 200, height = 500, bg = 'white')
        self.Frame_top = Frame(self.root, width = 700, height = 50, bg = 'black')

        ########-----------Frames Secondaires------------#######################################
        self.Frame1 = Frame(self.Frame_left, width = 200, height = 200, bg = 'black')
        self.Frame2 = Frame(self.Frame_left, width = 200, height = 300, bg = 'black')
        self.Canvas_dessine = Canvas(self.Frame2, width = 190, height = 288, bg = 'white',highlightthickness=0)

        #######-----------Package des Frames-------------####################################
        self.Frame_top.pack(side = TOP)
        self.Frame_left.pack(side = LEFT)
        self.Frame1.pack(side = TOP)
        self.Frame2.pack(side = BOTTOM)
        self.Canvas_dessine.place(x = 5, y = 5)

        ######-----------Elements du jeu-----------------##########################################
        self.Canvas_dessine.create_image(100, 190, image = self.Tom_vs_Jerry)

        self.sentence = Label(self.Frame2, text = "Attrape Moi \n Si Tu Peux !!!",font = ("Berlin Sans FB", 15), bg = 'white')
        self.sentence.place(x = 45, y = 60)

        self.canvas_show_time = Canvas(self.Frame1, bg = 'black',highlightthickness=0)
        self.canvas_show_time.place(x = 10, y = 30)
        self.show_time = Label(self.canvas_show_time, text = "Temps: %s" %str(0), foreground = 'blue2', bg = 'black',font = ("Berlin Sans FB", 24))
        self.show_time.pack(padx= 3, pady = 3)


        self.Button_quit = Button(self.Frame_top, text = 'QUIT' ,foreground = 'red2',activebackground = 'red2',bg = 'black' ,font=("Berlin Sans FB", 15), cursor ='hand2',command = self.exit)
        self.Button_quit.place(x = 600, y = 5)


        self.start()
        self.time_start = time()
        self.time_num()

        self.root.mainloop()

    def quit_rules(self):
        self.Frame_main2_wind2.destroy()
        Scoreboard(self.Frame_main1_wind2, self.show_rules, "Ghost", self.User_name)

    def quit_ranking(self):
        self.show_rules.destroy()
        self.show_rules.quit()

    def exit(self):
        self.root.destroy()
        self.root.quit()

    def start(self):
        self.root.focus_force()
        self.root.bind("<Key>", self.move_Jerry)

        self.nbcases = (7, 8, 10, 13)
        self.length = 500/self.nbcases[self.level - 1]
        self.fantome = []
        self.Best_Score = 0
        self.time_game = 0
        self.move = 0
        self.control_variable = 0
        self.control_variable2 = 0
        self.grid = [[(0) for i in range(self.nbcases[self.level - 1])] for j in range((self.nbcases[self.level - 1]))]

        ########------------Frames Pricipaux-------------########################################
        self.Frame_right = Frame(self.root, width = 500, height = 500, bg = 'black')
        #######-----------Package des Frames-------------####################################
        self.Frame_right.pack(side = RIGHT)
        ######-----------Elements du jeu-----------------##########################################
        self.canvas_show_score = Canvas(self.Frame1, bg = 'black', highlightthickness=0)
        self.canvas_show_score.place(x = 10, y = 110)
        self.show_score = Label(self.canvas_show_score, text = "Score: %s" %str(int(self.score)), bg = 'black', font = ("Berlin Sans FB", 24), foreground = 'red2')
        self.show_score.pack(padx = 3, pady = 3)

        self.Title_level = Label(self.Frame_top, text = "Level %s" %str(self.level), foreground = 'white', bg= 'black', font=("Berlin Sans FB", 26))
        self.Title_level.place(x = 315, y = 4)


        self.table = Canvas(self.Frame_right, width = 500, height = 500, bg = "#1a1a1a",highlightthickness=0)
        self.table.pack(fill = BOTH)
        for i in range(self.nbcases[self.level - 1]):
            self.table.create_line((self.length)*i,0,(self.length)*i,500,fill = 'blue')
        for j in range(self.nbcases[self.level - 1]):
            self.table.create_line(0,(self.length)*j,500,(self.length)*j, fill = 'blue')

        for j in range(self.nbcases[self.level - 1]):
            for i in range(self.nbcases[self.level - 1]):
                self.grid[i][j] = level_map[self.level - 1][(j*self.nbcases[self.level - 1])+i]

                if self.nbcases[self.level - 1] <= 10:
                    if self.grid[i][j] == 'X':
                        self.table.create_rectangle(self.length* i, self.length* j,self.length* (i+1), self.length*(j+1), fill = 'red')
                    elif self.grid[i][j] == 'R':
                        self.robot = self.table.create_image(self.length* i +self.length/2, self.length* j +self.length/2, image = self.Jerry_image)
                    elif self.grid[i][j] == 'F':
                        self.Tom = self.table.create_image(self.length* i +self.length/2, self.length* j +self.length/2, image = self.Tom_image_left)
                        self.fantome.append(self.Tom)
                    elif self.grid[i][j] == 'D':
                        self.Drapeau = self.table.create_image(self.length* i +self.length/2, self.length* j +self.length/2, image = self.Fromage_image)
                elif self.nbcases[self.level - 1] > 10:
                    if self.grid[i][j] == 'X':
                        self.table.create_rectangle(self.length* i, self.length* j,self.length* (i+1), self.length*(j+1), fill = 'red')
                    elif self.grid[i][j] == 'R':
                        self.robot = self.table.create_image(self.length* i +self.length/2, self.length* j +self.length/2, image = self.Jerry_image_mini)
                    elif self.grid[i][j] == 'F':
                        self.Tom = self.table.create_image(self.length* i +self.length/2, self.length* j +self.length/2, image = self.Tom_image_left_mini)
                        self.fantome.append(self.Tom)
                    elif self.grid[i][j] == 'D':
                        self.Drapeau = self.table.create_image(self.length* i +self.length/2, self.length* j +self.length/2, image = self.Fromage_image_mini)

    def move_Jerry(self, event = None):
        pos_x, pos_y = self.table.coords(self.robot)
        symb = event.keysym
        self.dir_Jerry = [0,0]
        if symb == "Right": #[1,0]
            self.dir_Jerry = [1,0]
        elif symb == "Down": #[0, 1]
            self.dir_Jerry = [0,1]
        elif symb == "Left": #[-1,0]
            self.dir_Jerry = [-1,0]
        elif symb == "Up":#[0, -1]
            self.dir_Jerry = [0, -1]

        self.newpos_x_Jerry = pos_x + self.dir_Jerry[0]*self.length
        self.newpos_y_Jerry = pos_y + self.dir_Jerry[1]*self.length
        self.new_grid_x_Jerry = int(self.newpos_x_Jerry//self.length)
        self.new_grid_y_Jerry = int(self.newpos_y_Jerry//self.length)
        if 0 <= self.newpos_x_Jerry <= 500 and 0 <= self.newpos_y_Jerry <= 500:
            if self.grid[self.new_grid_x_Jerry][self.new_grid_y_Jerry] != 'X':
                self.table.move(self.robot, self.dir_Jerry[0]*self.length, self.dir_Jerry[1]*self.length)
                if symb == "Right" or symb == "Down" or symb == "Left" or symb == "Up":
                    self.move_Tom(pos_x + self.dir_Jerry[0]*self.length, pos_y + self.dir_Jerry[1]*self.length)
                    self.move += 1
        self.table.update()

    def move_Tom(self, last_x, last_y):
        for elt in range(len(self.fantome)):
            self.newpos_x = last_x
            self.newpos_y = last_y
            self.dir_Tom = [0,0]
            list_dir = [[0, -1],[-1, -1],[-1, 0],[-1, 1],[0, 1],[1, 1],[1, 0],[1, -1], [0,0]]
            distance =[]
            list =[]

            self.pos_x_tom, self.pos_y_tom = self.table.coords(self.fantome[elt])
            for i in list_dir:
                if 0 <= self.pos_x_tom + i[0]*self.length < 500 and 0 <= self.pos_y_tom+i[1]*self.length <= 500:
                    if self.grid[int(self.pos_x_tom//self.length + i[0])][int(self.pos_y_tom//self.length + i[1])] == "0" or self.grid[int(self.pos_x_tom//self.length + i[0])][int(self.pos_y_tom//self.length + i[1])] == "F":
                        distance.append((sqrt (((self.pos_x_tom + i[0]*self.length-self.newpos_x)**2)+ ((self.pos_y_tom+i[1]*self.length- self.newpos_y)**2)) , i))

            distance.sort(key = lambda list: list[0])
            list = [j[1] for j in distance]

            self.newpos_x_Tom = self.pos_x_tom +list[0][0]*self.length
            self.newpos_y_Tom = self.pos_y_tom + list[0][1]*self.length
            self.new_grid_x_Tom = int(self.newpos_x_Tom//self.length)
            self.new_grid_y_Tom = int(self.newpos_y_Tom//self.length)

            if self.nbcases[self.level - 1] <= 10:
                if list[0][0] == 1:
                    self.table.itemconfigure(self.fantome[elt], image = self.Tom_image_right)
                else:
                    self.table.itemconfigure(self.fantome[elt], image = self.Tom_image_left)
            elif self.nbcases[self.level - 1] > 10:
                if list[0][0] == 1:
                    self.table.itemconfigure(self.fantome[elt], image = self.Tom_image_right_mini)
                else:
                    self.table.itemconfigure(self.fantome[elt], image = self.Tom_image_left_mini)


            self.table.move(self.fantome[elt], list[0][0]*self.length, list[0][1]*self.length)
            self.verif(self.new_grid_x_Jerry,self.new_grid_y_Jerry,self.new_grid_x_Tom,self.new_grid_y_Tom)
        self.table.update()

    def verif(self,next_jerry_x, next_jerry_y,next_tom_x, next_tom_y):
        if self.nbcases[self.level - 1] <= 10:
            if self.grid[next_jerry_x][next_jerry_y] == "D":
                self.table.itemconfigure(self.Drapeau, image = self.Fromage_Jerry_image)
                self.table.itemconfigure(self.robot,  image = self.Fromage_Jerry_image)
                self.root.unbind("<Key>")
                self.command_user("win")
            elif next_jerry_x == next_tom_x and next_jerry_y == next_tom_y:
                self.table.itemconfigure(self.Tom, image = self.Tom_right_image)
                self.table.itemconfigure(self.robot,  image = self.Tom_right_image)
                self.root.unbind("<Key>")
                self.command_user("dead")
        elif self.nbcases[self.level - 1] > 10:
            if self.grid[next_jerry_x][next_jerry_y] == "D":
                self.table.itemconfigure(self.Drapeau, image = self.Fromage_Jerry_image_mini)
                self.table.itemconfigure(self.robot,  image = self.Fromage_Jerry_image_mini)
                self.root.unbind("<Key>")
                self.command_user("win")
            elif next_jerry_x == next_tom_x and next_jerry_y == next_tom_y:
                self.table.itemconfigure(self.Tom, image = self.Tom_right_image_mini)
                self.table.itemconfigure(self.robot,  image = self.Tom_right_image_mini)
                self.root.unbind("<Key>")
                self.command_user("dead")

    def time_num(self):

        self.time_game+=1
        self.root.after(1000,self.time_num)
        self.show_time['text'] = "Temps: %s" %str(self.time_game)

    def command_user(self, x):
        if x=="exit_menu":
            self.canvas_question.destroy()
            self.exit()

        elif x=="next":
            self.canvas_show_score.destroy()
            self.canvas_question.destroy()
            self.level += 1
            if self.level == len(level_map)+1:  # si le joueur a atteint la fin de la liste des niveaux
                self.exit()
                return
            self.Frame_right.destroy()               # destruction des frames
            self.start()

        elif x=="dead":
            try:
                self.table.destroy()
            except: pass
            self.score_temp = 0
            self.canvas_question = Canvas(self.Frame_right, width = 482, height = 300, highlightthickness=0)
            self.canvas_question.place(x=9,y=100)
            self.canvas_question.create_image(241, 150, image = self.fond_ecran)
            self.canvas_question.create_text(232, 100, text ='Perdu !! \n Veux-tu recommencer ?', font = ("Berlin Sans FB", 14))
            answer1 = Button(self.canvas_question, text = " Oui ",command = lambda: self.command_user("restart2"),cursor ='hand2',fg = 'white', bg = 'black', font = ("Helvetica", 12)).place(x = 120, y = 150)
            answer2 = Button(self.canvas_question, text = " Non ",command = self.exit,cursor ='hand2',fg = 'white', bg = 'black', font = ("Helvetica", 12)).place(x = 300, y = 150)

        elif x=="win":
            try:
                self.canvas_question.destroy()
            except: pass
            try:
                self.table.destroy()
            except: pass
            self.control_variable +=1
            if self.control_variable == 1:
                self.score_temp = (10000/(self.move*0.8 + self.time_game*0.2)) * self.level
                self.score += self.score_temp
            self.control_variable2 +=1
            if self.control_variable2 == 1:
                self.show_score["text"] = "Score: %s"%str(int(self.score))
                self.canvas_question = Canvas(self.Frame_right, width = 482, height = 300, highlightthickness=0)
                self.canvas_question.place(x=9,y=100)
                self.canvas_question.create_image(241, 150, image = self.fond_ecran)
                self.canvas_question.create_text(90, 110, text = 'Recommencer', font = ("Berlin Sans FB", 20))
                self.canvas_question.create_text(241, 110, text = 'Suivant', font = ("Berlin Sans FB", 20))
                self.canvas_question.create_text(390, 110, text = 'Menu', font = ("Berlin Sans FB", 20))
                Button(self.canvas_question,image = self.replay, highlightthickness=0, borderwidth = 0, command = lambda: self.command_user("restart_question"),cursor ='hand2', font = ("Helvetica", 10)).place(x = 60, y = 150)
                Button(self.canvas_question,image = self.main,highlightthickness=0, borderwidth = 0,command = lambda: self.command_user("exit_menu"),cursor ='hand2', font = ("Helvetica", 10)).place(x = 360, y = 150)
                Button(self.canvas_question,image = self.next_image,highlightthickness=0, borderwidth = 0,command = lambda: self.command_user("next"),cursor ='hand2', font = ("Helvetica", 10)).place(x = 211, y = 150)

        elif x=="restart_question":
            self.count += 1
            self.control_variable2 = 0
            self.canvas_question.destroy()
            self.canvas_question = Canvas(self.Frame_right, width = 482, height = 300, highlightthickness = 0)
            self.canvas_question.place(x=9,y=100)
            self.canvas_question.create_image(241, 150, image = self.fond_ecran)
            self.canvas_question.create_text(232, 100, text = 'Perdu !! \n Veux-tu recommencer ?', font = ("Berlin Sans FB", 14))
            answer1 = Button(self.canvas_question, text = " Oui ",command = lambda: self.command_user("restart2"),cursor ='hand2',fg = 'white', bg = 'black', font = ("Helvetica", 12)).place(x = 120, y = 150)
            answer2 = Button(self.canvas_question, text = " Non ",command = lambda: self.command_user("win"),cursor ='hand2',fg = 'white', bg = 'black', font = ("Helvetica", 12)).place(x = 300, y = 150)
        elif x=="restart2":
            self.canvas_show_score.destroy()
            try:
                self.canvas_question.destroy()
            except: pass
            self.Table = Canvas(self.Frame_right,width = 500, height = 500, bg ='white', highlightthickness=0)
            self.score -= 50*(self.level) + self.score_temp
            self.update()

    def update(self):
        self.Frame_right.destroy()               # destruction des frames
        self.start()

def Ghost(User):
  jeux = ghost(User)
  return (jeux.score, jeux.score, (time()-jeux.time_start), jeux.count, [])
