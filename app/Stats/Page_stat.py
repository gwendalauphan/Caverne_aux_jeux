import sys
from tkinter import *
import tkinter as tk
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib.pyplot import imshow, show, colorbar
import numpy as np


sys.path.append('../Reseau')
from Reseau.client import *

class App_stat:
    def __init__(self, master, fig):
        self.frame_stat_main = Frame(master)
        self.frame_stat_main.pack(fill = BOTH, expand=True)

        self.quitbutton = Button(self.frame_stat_main, text="Quitter", fg="red", command=self.back_home )
        self.quitbutton.pack(side = TOP)


        self.canvas = FigureCanvasTkAgg(fig, self.frame_stat_main)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.frame_stat_main)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.canvas._tkcanvas.pack(expand=True)

    def back_home(self):
        self.canvas.get_tk_widget().destroy()
        self.toolbar.destroy()
        plt.close(self.canvas.figure)
        self.frame_stat_main.destroy()
        


class Graph_1_exe(App_stat):
    def __init__(self, master,user_name,x0,y0, x1,title, Legend1, Legend2,name_y_axe):
        ind = np.arange(len(x0))  # the x locations for the groups
        width = 0.35  # the width of the bars

        fig, ax = plt.subplots(figsize=(7, 5))
        if x1 == []:
            rects1 = ax.bar(ind, x0, width,
                            label=Legend1)

        else:
            rects1 = ax.bar(ind - width/2, x0, width,
                            label=Legend1)
            rects2 = ax.bar(ind + width/2, x1, width,
                            label=Legend2)

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel(name_y_axe)
        ax.set_title(title, weight = 'bold')
        ax.set_xticks(ind)
        plt.gca().xaxis.set_tick_params(labelsize = 8)

        ax.set_xticklabels(y0)
        ax.legend()
        fig.tight_layout()
        super().__init__(master,fig)
    

class Graph_2_exe(App_stat):
    def __init__(self, master, user_name, x0, title,Legend1,lequel): #, user_name, grille)

        grille = np.zeros((20, 20), dtype = int)
        for elt in x0:
            grille[abs(elt[1]-19),abs(elt[0])] += x0[elt]

        fig, ax = plt.subplots(figsize=(5, 5))
        im = plt.imshow(grille, cmap=plt.cm.jet) # later use a.set_data(new_data)
        ax.set_xlim(-0.25, 19.25)
        ax.set_ylim(-0.25, 19.25)
        fig.suptitle(title, weight = 'bold')
        cbar = plt.colorbar()
        cbar.set_label(Legend1)
        super().__init__(master,fig)


class Graph_3_exe(App_stat):
    def __init__(self, master,user_name, x0,title,Legend1,lequel):
        x =[]
        y =[]
        for key, value in x0.items():
            for _ in range(value):
                x.append(key[0])
                y.append(abs(key[1]-19))

        fig, ax = plt.subplots(figsize=(5, 10), dpi= 100)
        if lequel == 'Snake':
            ax.set_xlim(-0.25, 19.25)
            ax.set_ylim(-0.25, 19.25)
            ax.set_aspect('equal')
        fig.suptitle(title, weight = 'bold')
        # Create the Scatter Plot
        ax.scatter(x, y, color="blue", s=500, alpha=0.1, linewidths=1)
        #fig.tight_layout()
        super().__init__(master,fig)


class Graph_4_exe(App_stat):
    def __init__(self, master,user_name,score_app,game, x1,title,title2, Legend1, Legend2,name_y_axe):
        fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(aspect="equal"),dpi = 90)
        explode = []

        for score in score_app:
            explode.append(score/40000)

        def func(pct, score_app):
            absolute = int(pct/100*sum(score_app))
            return "{:.1f}%\n({:d} pts)".format(pct, absolute)

        wedges, texts, autotexts = ax.pie(score_app, explode=explode, labels=game, autopct=lambda pct: func(pct, score_app),
                colors = ['red', 'green', 'yellow', 'blue', 'orange', 'pink', 'lightgrey','brown','purple'],pctdistance = 0.7, labeldistance = 1.2,shadow=True, startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        ax.legend(wedges, game, title=title2,loc="center right", bbox_to_anchor=(0.6, 0.2, 0.5, 0.5))

        plt.setp(autotexts, size=7)
        fig.tight_layout()

        fig.suptitle(title, weight = 'bold', fontsize=12, x = 0.15, y = 0.96)
        super().__init__(master,fig)

class Graph_5_exe(App_stat):
    def __init__(self, master,user_name,x0,title, label_y,label_x):
        #game = x0 un dico
        x_att = []
        x_att2 = []
        x_att3 = []
        mycolors = ['red', 'blue', 'green', 'orange', 'brown', 'grey', 'pink', 'olive', 'deeppink', 'steelblue', 'firebrick', 'mediumseagreen']
        fig = plt.figure(figsize=(16,10), dpi= 75)
        for i,score in enumerate(x0):
            x_att = []
            x_att2 = []
            for y in x0[score]:
                x_att.append(y)
                x_att2.append(x0[score][y])
            plt.plot(x_att,x_att2, color=mycolors[i], label=score)
            plt.text(len(x_att2)-0.95 ,x_att2[-1], score, fontsize=10, color=mycolors[i])
            x_att3.append(max(x_att2))

        plt.xlim(-0.1, len(x_att2)-1)
        plt.ylabel(label_y,fontsize=12)
        plt.xlabel(label_x,fontsize=12)
        #plt.yscale('symlog', nonposy='clip')
        tick_val = [0,int((3/4)*(max(x_att3))),int((max(x_att3))/2),int((3/4)*(max(x_att3))),int(max(x_att3))]
        plt.yticks(tick_val)
        plt.title(title, fontsize=20, weight = 'bold')
        plt.gca().spines["top"].set_alpha(0.0)
        plt.gca().spines["bottom"].set_alpha(0.5)
        plt.gca().spines["right"].set_alpha(0.0)
        plt.gca().spines["left"].set_alpha(0.5)
        plt.legend(loc='upper right', ncol=2, fontsize=10)
        super().__init__(master,fig)
