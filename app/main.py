from tkinter import *
import tkinter as tk
from Reseau.client import *
import signal
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
from Utils.utils import *

# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("CaverneAuxJeuxClient")

logger.info("The client app is running.")


def handle_sigint(sig, frame):
    logger.info('Interrupt signal received. Shutting down the client...')
    sys.exit(0)

def handle_sigtstp(sig, frame):
    logger.info('Stop signal received (Ctrl+Z). Shutting down the client...')
    sys.exit(0)

# Configurer les gestionnaires de signaux
signal.signal(signal.SIGINT, handle_sigint)  # Ctrl+C everywhere
# Termination from OS / runner
if hasattr(signal, "SIGTERM"):
    signal.signal(signal.SIGTERM, handle_sigint)

# Ctrl+Break on Windows
if hasattr(signal, "SIGBREAK"):
    signal.signal(signal.SIGBREAK, handle_sigint)

# POSIX-only job control (Ctrl+Z)
if hasattr(signal, "SIGTSTP"):
    signal.signal(signal.SIGTSTP, handle_sigtstp)

def init_ranking_rows(parent):
    """Create 10 reusable rows (labels) in the ranking frame."""
    rows_pseudo = []
    rows_score = []

    # header line (you already create one — keep either yours or this)
    # Label(parent, text="Rang" + " "*8 + "Nom" + " "*24 + "Score", ...).place(x=2, y=50)

    # fixed 10 rows so we can update in place
    for i in range(10):
        lp = Label(parent,
                   text=f"#{i+1} :",
                   bg='#111111', foreground='#00e600', font=("Helvetica", 8))
        lp.place(x=4, y=75 + i*20)
        ls = Label(parent,
                   text="",
                   bg='#111111', foreground='#00e600', font=("Helvetica", 8))
        ls.place(x=160, y=75 + i*20)

        rows_pseudo.append(lp)
        rows_score.append(ls)

    return rows_pseudo, rows_score


# -------------------------
# Button widget wrapper
# -------------------------
class BoutonS:
    """Interactive game button that previously depended on globals.
    Now receives the app context and the canvas explicitly."""
    def __init__(self, app: "App", canvas: tk.Canvas, x, y, jeux, run, name):
        self.app = app
        self.canvas = canvas
        self.jeux = jeux
        self.run = run

        self.image = PhotoImage(file=resource_path(f"thumbnail/{jeux}.png"))
        # keep ref to avoid GC
        app._images.append(self.image)

        canvas.create_text(y*(450/5) + 20, x*(265/4)-90,
                           text=name, font=("Berlin Sans FB", 20), fill="white")
        self.created = canvas.create_image(y*(450/5) + 20, x*(265/4), image=self.image)
        canvas.tag_bind(self.created, "<Button-1>", self.command)

    def command(self, event=None):
        """Run the game, push score, and refresh ranking."""
        self.app.root.withdraw()
        max_score, score, Average_Time, count, death_pos = self.run(self.app.user_name)
        push_score(self.app.user_name, self.jeux, max_score, score, count, Average_Time, death_pos)
        self.app.root.deiconify()

        # Restore scroll binding (if needed)
        self.app.Frame_main['yscrollcommand'] = self.app.scrollY.set

        self.app.populate_ranking()

# -------------------------
# App
# -------------------------
class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # hidden until login finishes
        self.user_name: str = "Unknown"
        self._images = []     # keep PhotoImage references

        # bad-words list
        with open(resource_path('Data/mots.txt'), 'r') as file:
            self.mots_interdits = file.read().split("\n")

        # Build login
        self._build_login()

    # ---------- Login ----------
    def _build_login(self):
        self.login = Tk()
        self.login.title("Connexion")
        self.login.geometry("300x120")
        self.login.grab_set()
        self.login.focus_force()
        self.login.resizable(False, False)
        self.login.protocol("WM_DELETE_WINDOW", self._cancel_login)  # Runs _cancel_login when window is closed

        Label(self.login, text="Entre un pseudo pour jouer").place(x=60, y=15)

        self.entry = Entry(self.login)
        self.entry.place(x=25, y=55, width=170)
        self.entry.focus()

        self.alert = Label(self.login, text="Nom invalide", fg="red")

        Button(self.login, text="Valider", cursor='hand2', command=self.valider).place(x=205, y=54)
        Button(self.login, text="Annuler", command=self._cancel_login).place(x=205, y=85)
        self.login.bind("<Return>", self.valider)

        # center
        sx = self.root.winfo_screenwidth() // 2
        sy = self.root.winfo_screenheight() // 2
        self.login.geometry(f"+{sx-150}+{sy-60}")

    def _cancel_login(self):
        self.login.destroy()
        self.root.destroy()

    def valider(self, event=None):
        temp = self.entry.get().replace(" ", "_")
        if temp == "" or len(temp) > 12:
            self.alert.place(x=50, y=100)
            return
        for elt in self.mots_interdits[:-1]:
            if elt in temp.lower():
                self.alert.place(x=50, y=100)
                return

        self.user_name = temp
        check_add_player(self.user_name)

        self.login.destroy()
        self._build_main()
        self.root.deiconify()



    # ---------- Main UI ----------

    def refresh_ranking(self):
        """Fetch the latest scores and update the 10 rows in place."""
        try:
            scores = get_score_list()  # list like [(name, score), ...]
        except Exception as e:
            # Optional: show an alert if fetching failed
            # You can also log e or display a toast/Label somewhere
            return

        # Update up to 10 rows; clear the rest
        for i in range(10):
            if i < len(scores):
                name, pts = scores[i][0], scores[i][1]
                self.label_pseudo[i].config(text=f"#{i+1} :       {name}")
                try:
                    pts_int = int(pts)
                except Exception:
                    pts_int = pts
                self.label_score[i].config(text=f"{pts_int}")
            else:
                self.label_pseudo[i].config(text=f"#{i+1} :")
                self.label_score[i].config(text="")

    def _build_main(self):
        root = self.root
        root.geometry('1020x600')
        root.title("Menu")
        root.resizable(False, False)
        root.focus_force()

        # Layout frames
        self.Frame_top = Frame(root, bg='#111111')
        self.Frame_top.pack(ipadx=1000, ipady=50, side=TOP)

        self.Frame_left = Frame(root, bg='#111111')
        self.Frame_left.pack(ipadx=100, ipady=500, side=LEFT)

        self.Frame_right = Frame(root, bg='#111111')
        self.Frame_right.pack(ipadx=20, ipady=600, side=RIGHT)

        self.Frame_down = Frame(root, bg='#111111')
        self.Frame_down.pack(ipadx=900, ipady=20, side=BOTTOM)

        self.image_de_fond = PhotoImage(file=resource_path("thumbnail/image_de_fond.png"))
        self._images.append(self.image_de_fond)

        self.Frame_main = Canvas(
            root, highlightthickness=0, borderwidth=2, bg='#111111',
            relief=GROOVE, scrollregion=(0, 0, 250, 1000)
        )
        self.Frame_main.pack(ipadx=900, ipady=530, side=BOTTOM)
        self.Frame_main.create_image(380, 537, image=self.image_de_fond)

        self.scrollY = Scrollbar(root, orient="vertical", cursor='hand2', command=self.Frame_main.yview)
        self.scrollY.place(x=962, y=102, height=456)
        self.Frame_main['yscrollcommand'] = self.scrollY.set

        # Mousewheel cross-platform
        def _on_mousewheel(event):
            delta = int(-1 * (event.delta / 120))
            self.Frame_main.yview_scroll(delta, "units")
        def _on_mousewheel_linux_up(event): self.Frame_main.yview_scroll(-1, "units")
        def _on_mousewheel_linux_down(event): self.Frame_main.yview_scroll(1, "units")

        self.Frame_main.bind("<MouseWheel>", _on_mousewheel)
        self.Frame_main.bind("<Button-4>", _on_mousewheel_linux_up)
        self.Frame_main.bind("<Button-5>", _on_mousewheel_linux_down)

        self.Frame_ranking = Frame(self.Frame_left, width=196, height=280, bg='#111111', relief=GROOVE)
        self.Frame_ranking.place(x=2, y=70)

        # Images
        self.gearImg = PhotoImage(file=resource_path('Parametters/gear.png'))
        self.doorImg = PhotoImage(file=resource_path("Parametters/door.png"))
        self.image_stat = PhotoImage(file=resource_path("Parametters/image_stat.png"))
        self._images += [self.gearImg, self.doorImg, self.image_stat]

        # Top actions
        self.Button_para = Button(
            self.Frame_top, image=self.gearImg, bg="#111111",
            borderwidth=0, highlightthickness=0, cursor="hand2", command=self.para
        )
        self.Button_para.place(x=860, y=25)

        Button(
            self.Frame_top, image=self.image_stat, bg="#111111",
            borderwidth=0, highlightthickness=0, cursor="hand2", command=self.execute
        ).place(x=930, y=20)

        # Titles
        Label(self.Frame_top, text='La Caverne Aux Jeux',
              font=("Berlin Sans FB", 45), bg='#111111', foreground='#00e600',
              relief=GROOVE).place(x=205, y=10)

        Label(self.Frame_ranking, text='Classements',
              font=("Berlin Sans FB", 20), bg='#111111', foreground='#00e600',
              relief=GROOVE).place(x=27, y=5)

        Label(self.Frame_ranking,
              text="Rang" + " "*8 + "Nom" + " "*24 + "Score  ",
              font=("Helvetica", 9), bg='#111111', foreground='#00e600',
              relief=GROOVE).place(x=2, y=50)

        # Ranking rows & initial data
        self.label_pseudo, self.label_score = init_ranking_rows(self.Frame_ranking)
        self.populate_ranking()

        # Refresh button
        Button(self.Frame_left, text="Rafraîchir", cursor='hand2',
               command=self.refresh_ranking, bg="#1e1e1e", fg="#00e600",
               relief=GROOVE).place(x=65, y=350)

        # Game buttons (pass app & canvas explicitly)
        BoutonS(self, self.Frame_main, 2, 1, "Tete", Tete, "Tête chercheuse")
        BoutonS(self, self.Frame_main, 2, 3, "Snake", Snake, "Snake")
        BoutonS(self, self.Frame_main, 5, 3, "Ghost", Ghost, "Tom & Jerry")
        BoutonS(self, self.Frame_main, 5, 5, "Minesweeper", Minesweeper, "Démineur")
        BoutonS(self, self.Frame_main, 2, 5, "Pendu", Pendu, "Pendu")
        BoutonS(self, self.Frame_main, 5, 1, "Tetris", Tetris, "Tetris")
        BoutonS(self, self.Frame_main, 5, 7, "Pong", Pong, "Pong")
        BoutonS(self, self.Frame_main, 2, 7, "Flappy", Flappy_Bird, "Flappy")

        # Friendly footer
        Label(self.Frame_down, text=f"Bienvenue, {self.user_name} !", pady=10,
              bg="#111111", fg="#00e600", font=("Helvetica", 10, "italic")).pack()

    def populate_ranking(self):
        # get and fill ranking
        self.score = get_score_list()
        # if init_ranking_rows built exactly 10 rows, fill up to 10
        for i in range(10):
            if i < len(self.score):
                name, pts = self.score[i][0], self.score[i][1]
                self.label_pseudo[i].config(text=f"#{i+1} :       {name}")
                self.label_score[i].config(text=f"{int(pts)}")
            else:
                self.label_pseudo[i].config(text=f"#{i+1} :")
                self.label_score[i].config(text="")

    # ---------- “Paramètres” panel ----------
    def para(self):
        self.playground = Canvas(self.root, highlightthickness=0, width=800, height=500, bg="#111111")
        self.playground.place(x=200, y=100)
        self.Button_para.config(image=self.doorImg, command=lambda: self.leave_para())
        text = ("Le but de cette application est de s'amuser en jouant à des jeux.\n"
                "Tu peux défier tes amis en comparant leur score au tien\n"
                "sur différents jeux et essayer de faire le meilleur score possible.")
        Label(self.playground, text="Aide", font=("Helvetica", 25),
              bg="#111111", fg="#888888").place(x=300, y=20)
        Label(self.playground, text=text, font=("Helvetica", 10),
              bg="#111111", fg="#888888").place(x=100, y=60)

    def leave_para(self):
        if hasattr(self, "playground"):
            self.playground.destroy()
            del self.playground
        self.Button_para.config(image=self.gearImg, command=self.para)

    # ---------- Stats ----------
    def execute(self, event=None):
        from Stats.Page_selection import Stats
        self.root.withdraw()
        app = Stats(self.user_name)  # your Stats class handles its own UI
        self.root.deiconify()

    # ---------- Start loop ----------
    def run(self):
        self.root.mainloop()

# -------------------------
# Program entry point
# -------------------------
def main():
    # Acquire the singleton guard *before* creating your UI
    _guard_socket = acquire_single_instance(port=54321, logger=logger)  # pick a fixed port for your app

    app = App()
    # keep a reference so the socket isn't GC'ed while the app runs
    app._singleton_guard = _guard_socket

    app.run()

if __name__ == "__main__":
    main()
