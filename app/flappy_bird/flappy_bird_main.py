from tkinter import Toplevel, PhotoImage, Canvas, Frame, Label, Button, GROOVE
from tkinter.messagebox import askquestion
from time import time
from random import randint
from typing import Optional

from app.Utils.utils import resource_path
from app.Reseau.client import get_game_score_list
from app.Scoreboard.scoreboard import Scoreboard

# Font size variables
FONT_SIZE_SMALL = 10
FONT_SIZE_MEDIUM = 12
FONT_SIZE_BIG = 20


class Bird:  # pylint: disable=too-many-instance-attributes
    """UI and logic for the Flappy Bird player entity and main game windows."""

    # -------------------------------------------------------------------------------------
    # Construction & windows
    # -------------------------------------------------------------------------------------
    def __init__(self, user: str) -> None:  # pylint: disable=too-many-statements
        # --- Constants / config
        self.user_name: str = user

        # --- Metrics & history
        self.best_score: int = 0
        self.count: int = 0
        self.average_score: list[int] = []
        self.death_pos: list[int] = []

        # --- UI windows & frames (initialized to None, then created)
        self.show_rules: Optional[Toplevel] = None
        self.root: Optional[Toplevel] = None
        self.frame_main1_wind2: Optional[Canvas] = None
        self.frame_main2_wind2: Optional[Frame] = None
        self.frame_main_game: Optional[Canvas] = None
        self.frame_right: Optional[Frame] = None
        self.canvas_show_time: Optional[Canvas] = None
        self.canvas_world: Optional[Canvas] = None
        self.canvas_ground: Optional[Canvas] = None

        # --- Images / sprites placeholders
        self.fond_frame_main1_wind2: Optional[PhotoImage] = None
        self.image1: Optional[PhotoImage] = None
        self.image3: Optional[PhotoImage] = None
        self.image4: Optional[PhotoImage] = None
        self.ground_image: Optional[PhotoImage] = None
        self.hand_image: Optional[PhotoImage] = None
        self.image: Optional[PhotoImage] = None
        self.title: Optional[PhotoImage] = None
        self.fond_decor: Optional[PhotoImage] = None

        self.liste_image: list[PhotoImage] = []
        self.background: list[PhotoImage] = []
        self.liste_nombres: list[PhotoImage] = []
        self.tap: list[PhotoImage] = []

        # --- Game state (avoid W0201 by declaring here)
        self.play: bool = False
        self.press: bool = False
        self.wait: bool = True
        self.verite: bool = True

        self.i: int = 0
        self.compte: int = 0
        self.count_image: float = 8.0
        self.time_game: int = 0
        self.time_start: float = time()

        # Bird kinematics
        self.x: float = 0.0
        self.y: float = -2.9
        self.vitesse: float = 0.0
        self.vitesse_wait: float = 0.0

        # Score digits
        self.u: int = 0
        self.d: int = 0
        self.c: int = 0

        # Canvas items ids (ints)
        self.ground: Optional[int] = None
        self.tap1: Optional[int] = None
        self.tap2: Optional[int] = None
        self.hand: Optional[int] = None
        self.image_bird: Optional[int] = None
        self.image_unite: Optional[int] = None
        self.image_bird_true: Optional[int] = None

        # Pipes (created in start())
        self.tuyau0 = None
        self.tuyau1 = None
        self.tuyau2 = None
        self.tuyau3 = None

        # Coordinates cache
        self.x_center_bird: float = 0.0
        self.y_center_bird: float = 0.0

        # UI labels
        self.rules: Optional[Label] = None
        self.show_time: Optional[Label] = None
        self.button_skip: Optional[Button] = None

        # Pipes positions
        self.y_pipe_down = 0
        self.y_pipe_top = 0

        self.image_game_over = None  # id Canvas de l'image 'Game Over'
        self.game_over_img_small = None  # PhotoImage: GO réduit
        self.game_over_img_big = None  # PhotoImage: GO zoomé

        self.question = ""  # réponse du askquestion

        self.image_dizaine = None  # id Canvas du chiffre des dizaines
        self.image_centaine = None  # id Canvas du chiffre des centaines

        # Build UI
        self._build_rules_window()
        self._build_main_window()

    # -------------------------------------------------------------------------------------
    # UI builders
    # -------------------------------------------------------------------------------------
    def _build_rules_window(self) -> None:
        self.show_rules = Toplevel()
        self.show_rules.title("Règles")
        self.show_rules.geometry("670x530")
        self.show_rules.resizable(False, False)
        self.show_rules.focus_force()
        self.show_rules.protocol("WM_DELETE_WINDOW", self.quit_ranking)

        self.frame_main1_wind2 = Canvas(self.show_rules, bg="red", relief=GROOVE)
        self.frame_main1_wind2.pack(ipadx=670, ipady=526)
        self.fond_frame_main1_wind2 = PhotoImage(file=resource_path("thumbnail/Flappy2.png"))
        self.frame_main1_wind2.create_image(335, 263, image=self.fond_frame_main1_wind2)
        self.frame_main2_wind2 = Frame(self.frame_main1_wind2, width=550, height=425, relief=GROOVE)
        self.frame_main2_wind2.place(x=60, y=45)
        self.rules = Label(
            self.frame_main2_wind2,
            text="Les règles:",
            font=("Berlin Sans FB", 23),
            relief=GROOVE,
        )
        self.rules.place(x=200, y=5)

        first_label = Label(
            self.frame_main2_wind2,
            text="Le but du jeu est de faire avancer l'oiseau\n entre les tuyaux",
        )
        self.frame_main2_wind2.after(1000, lambda: first_label.place(x=20, y=80))
        self.image1 = PhotoImage(file=resource_path("flappy_bird/Ressources/rules1.png"))
        first_image = Label(self.frame_main2_wind2, image=self.image1)
        self.frame_main2_wind2.after(1500, lambda: first_image.place(x=380, y=57))

        second_label = Label(
            self.frame_main2_wind2,
            text=("Pour ce faire, tu peux utiliser la bar espace\n ou le clic souris\n " "pour que l'oiseau fasse un bond"),
        )
        self.frame_main2_wind2.after(2500, lambda: second_label.place(x=20, y=190))
        self.image3 = PhotoImage(file=resource_path("flappy_bird/Ressources/rules2.png"))
        third_image = Label(self.frame_main2_wind2, image=self.image3)
        self.frame_main2_wind2.after(3000, lambda: third_image.place(x=380, y=200))

        third_label = Label(
            self.frame_main2_wind2,
            text=("Mais attention, si tu touche un tuyau ou le sol,\n l'oiseau meurt"),
        )
        self.frame_main2_wind2.after(4000, lambda: third_label.place(x=20, y=290))
        self.image4 = PhotoImage(file=resource_path("flappy_bird/Ressources/rules3.png"))
        fourth_image = Label(self.frame_main2_wind2, image=self.image4)
        self.frame_main2_wind2.after(4500, lambda: fourth_image.place(x=350, y=300))

        self.button_skip = Button(self.frame_main2_wind2, text="-Skip-", cursor="hand2", command=self.quit_rules)
        self.button_skip.place(x=150, y=370)
        self.show_rules.mainloop()

    def _build_main_window(self) -> None:
        self.root = Toplevel()
        self.root.geometry("900x620")
        self.root.protocol("WM_DELETE_WINDOW", self.exit)
        self.root.resizable(False, False)
        self.root.title("Flappy Bird")
        self.root.focus_force()

        # Load sprites
        self.liste_image = [PhotoImage(file=resource_path(f"flappy_bird/Ressources/{i}.png")) for i in range(2, 31)]
        self.background = [PhotoImage(file=resource_path(f"flappy_bird/Ressources/decor{k + 1}.png")) for k in range(6)]
        self.liste_nombres = [PhotoImage(file=resource_path(f"flappy_bird/Ressources/u{p}.png")) for p in range(10)]

        self.ground_image = PhotoImage(file=resource_path("flappy_bird/Ressources/ground.png"))
        self.tap = [
            PhotoImage(file=resource_path("flappy_bird/Ressources/tap_right.png")),
            PhotoImage(file=resource_path("flappy_bird/Ressources/tap_left.png")),
        ]
        self.hand_image = PhotoImage(file=resource_path("flappy_bird/Ressources/hand.png"))
        self.image = PhotoImage(file=resource_path("flappy_bird/Ressources/game_over.png"))
        self.title = PhotoImage(file=resource_path("flappy_bird/Ressources/title.png"))
        self.fond_decor = PhotoImage(file=resource_path("flappy_bird/Ressources/fond_decor.png"))

        self.build_game()
        self.root.mainloop()

    # -------------------------------------------------------------------------------------
    # Menu / rules window callbacks
    # -------------------------------------------------------------------------------------
    def quit_rules(self) -> None:
        if self.frame_main2_wind2 is not None:
            self.frame_main2_wind2.destroy()
        Scoreboard(self.frame_main1_wind2, self.show_rules, "Flappy", self.user_name)

    def quit_ranking(self) -> None:
        assert self.show_rules is not None
        self.show_rules.destroy()
        self.show_rules.quit()

    def exit(self) -> None:
        assert self.root is not None
        self.root.destroy()
        self.root.quit()

    def test_press(self, _event=None) -> None:  # pylint: disable=unused-argument
        """Handle player input to initiate a jump."""
        self.play = True
        self.press = True
        self.i = 0

    # -------------------------------------------------------------------------------------
    # Game building & loop
    # -------------------------------------------------------------------------------------
    def build_game(self) -> None:
        """Set up game canvases and initial state."""
        assert self.root is not None
        self.root.focus_force()
        self.root.protocol("WM_DELETE_WINDOW", self.exit)
        self.root.bind("<space>", self.test_press)
        self.root.bind("<Button-1>", self.test_press)

        # Reset state for a new run
        self.x = 0.0
        self.y = -2.9
        self.vitesse = 0.0
        self.vitesse_wait = 0.0
        self.compte = 0
        self.count_image = 8.0
        self.time_game = 0
        self.play = False
        self.wait = True
        self.press = False
        self.verite = True
        self.u = self.d = self.c = 0

        # Frames
        self.frame_main_game = Canvas(self.root, width=900, height=620, bg="white", highlightthickness=0)
        self.frame_right = Frame(self.frame_main_game, width=700, height=550, bg="black")

        self.frame_main_game.place(x=0, y=0)
        self.frame_right.place(x=187, y=60)
        self.frame_main_game.create_image(450, 310, image=self.fond_decor)

        # Title & messages (wrapped lines for C0301)
        self.frame_main_game.create_image(537, 32, image=self.title)
        self.frame_main_game.create_text(
            100,
            250,
            text="Attention aux tuyaux !!!! ",
            fill="white",
            font=("Berlin Sans FB", FONT_SIZE_SMALL),
        )
        self.frame_main_game.create_image(30, 290, image=self.liste_image[2])
        self.frame_main_game.create_image(90, 330, image=self.liste_image[12])
        self.frame_main_game.create_image(150, 390, image=self.liste_image[22])

        self.frame_main_game.create_text(
            95,
            460,
            text="A savoir...",
            fill="white",
            font=("Berlin Sans FB", FONT_SIZE_SMALL),
        )
        self.frame_main_game.create_text(
            95,
            490,
            text="Une grosse surprise\n t'attend à la fin",
            fill="white",
            font=("Berlin Sans FB", FONT_SIZE_MEDIUM),
        )

        bestplayer = get_game_score_list("Flappy")[0]
        self.frame_main_game.create_text(
            85,
            120,
            text="Meilleur joueur:",
            fill="white",
            font=("Berlin Sans FB", FONT_SIZE_MEDIUM),
        )
        self.frame_main_game.create_text(
            85,
            135,
            text=f"{int(bestplayer[1] / 100)} points",
            fill="white",
            font=("Berlin Sans FB", FONT_SIZE_MEDIUM),
        )

        self.canvas_show_time = Canvas(self.frame_main_game, bg="black", highlightthickness=0)
        self.canvas_show_time.place(x=20, y=30)
        self.show_time = Label(
            self.canvas_show_time,
            text="Temps: 0",
            foreground="white",
            bg="black",
            font=("Berlin Sans FB", FONT_SIZE_BIG),
        )
        self.show_time.pack(padx=3, pady=3)

        # World & ground
        self.canvas_world = Canvas(self.frame_right, width=1700, height=500, highlightthickness=0)
        self.canvas_world.place(x=0, y=0)
        self.canvas_ground = Canvas(self.frame_right, width=900, height=70, highlightthickness=0)
        self.canvas_ground.place(x=0, y=500)
        self.canvas_world.create_image(350, 250, image=self.background[randint(0, 5)])
        self.ground = self.canvas_ground.create_image(450, 35, image=self.ground_image)

        # Tap hint images
        self.tap1 = self.canvas_world.create_image(285, 250, image=self.tap[1])
        self.tap2 = self.canvas_world.create_image(415, 250, image=self.tap[0])
        self.hand = self.canvas_world.create_image(350, 300, image=self.hand_image)

        # Bird idle image & unit score
        self.image_bird = self.canvas_world.create_image(350, 220, image=self.liste_image[int(self.count_image)])
        self.image_unite = self.canvas_world.create_image(350, 30, image=self.liste_nombres[self.u])

        self.wait_game()

    def wait_game(self, _event=None) -> None:  # pylint: disable=unused-argument
        """Idle animation until the first press."""
        if not self.play:
            # Oscillate bird up/down
            delta = 0.9
            if self.wait:
                self.vitesse_wait += delta
                self.canvas_world.move(self.image_bird, 0, self.vitesse_wait)
                if self.vitesse_wait > 7:
                    self.wait = False
                    self.vitesse_wait = 0.0
            else:
                self.vitesse_wait -= delta
                self.canvas_world.move(self.image_bird, 0, self.vitesse_wait)
                if self.vitesse_wait < -7:
                    self.wait = True
                    self.vitesse_wait = 0.0
            self.root.after(75, self.wait_game)
        else:
            self.move_bird_begin()
            self.time_num()

    def move_bird_begin(self) -> None:
        """Slide ground and move the bird to starting x before gameplay."""
        # Remove hint images
        for item in (self.tap1, self.tap2, self.hand):
            if item is not None:
                self.canvas_world.delete(item)

        vitesse = -12  # ground speed
        x, _ = self.canvas_ground.coords(self.ground)
        x1, _ = self.canvas_world.coords(self.image_bird)
        self.canvas_ground.move(self.ground, vitesse, 0)
        if x < 260:
            self.canvas_ground.coords(self.ground, 450, 35)

        if x1 + vitesse > 100:
            # Idle vertical oscillation while moving left
            delta = 0.9
            if self.wait:
                self.vitesse_wait += delta
                self.canvas_world.move(self.image_bird, vitesse, self.vitesse_wait)
                if self.vitesse_wait > 7:
                    self.wait = False
                    self.vitesse_wait = 0.0
            else:
                self.vitesse_wait -= delta
                self.canvas_world.move(self.image_bird, vitesse, self.vitesse_wait)
                if self.vitesse_wait < -7:
                    self.wait = True
                    self.vitesse_wait = 0.0
            self.root.after(50, self.move_bird_begin)
        else:
            self.canvas_world.coords(self.image_bird, 125, 220)
            self.press = False
            self.start()

    def time_num(self) -> None:
        if self.verite:
            self.time_game += 1
            self.root.after(1000, self.time_num)
            self.show_time["text"] = f"Temps: {self.time_game}"

    def start(self) -> None:
        """Create pipes and the controllable bird, then start the update loop."""
        self.canvas_world.delete(self.image_bird)
        self.root.focus_force()
        # Pipes (class Pipe must be provided by your project)
        self.tuyau0 = Pipe(self)
        self.tuyau1 = Pipe(self)
        self.tuyau2 = Pipe(self)
        self.tuyau3 = Pipe(self)

        self.tuyau0.create_pipe(1100, 350)
        self.tuyau1.create_pipe(1500, randint(200, 400))
        self.tuyau2.create_pipe(1900, randint(100, 300))
        self.tuyau3.create_pipe(2300, randint(100, 400))

        self.image_bird_true = self.canvas_world.create_image(125, 220, image=self.liste_image[int(self.count_image)])
        self.canvas_world.tag_raise(self.image_unite)
        self.update()

    def update(self) -> None:
        """Main update loop dispatcher."""
        if self.verite:
            self._move_ground()
            for _ in range(6):
                self._move_bird_step()
                self._move_pipes()
            self.root.after(48, self.update)

    # -------------------------------------------------------------------------------------
    # Helpers to reduce branching (fix R0912)
    # -------------------------------------------------------------------------------------
    def _move_ground(self) -> None:
        x, _ = self.canvas_ground.coords(self.ground)
        self.canvas_ground.move(self.ground, -12, 0)
        if x < 260:
            self.canvas_ground.coords(self.ground, 450, 35)

    def _move_bird_step(self) -> None:
        """One physics tick for the bird (split ascend/descend)."""
        # Perform multiple micro-steps for smoother motion
        if self.press:
            self._ascend_step()
        else:
            self._descend_step()

    def _ascend_step(self) -> None:
        self.i += 1
        self.vitesse = 0.0
        self.x_center_bird, self.y_center_bird = self.canvas_world.coords(self.image_bird_true)
        self.canvas_world.move(self.image_bird_true, self.x, self.y)
        self.canvas_world.itemconfigure(self.image_bird_true, image=self.liste_image[int(self.count_image)])
        if self.i >= 27:
            self.press = False
            self.count_image = 0.5
        else:
            self.count_image = max(0.0, self.count_image - 1.2)

    def _descend_step(self) -> None:
        # Adjust inclination image index
        if self.count_image < 25:
            self.count_image = self.count_image * (1.1 if self.count_image > 5 else 1.04)
            self.count_image = min(self.count_image, 25.0)
            self.vitesse += 0.06
            self.x_center_bird, self.y_center_bird = self.canvas_world.coords(self.image_bird_true)
            if (self.y_center_bird + self.vitesse + 25) > 500:
                self.canvas_world.coords(self.image_bird_true, self.x_center_bird, 475)
                self.verif_bird(0, 0, dead=True)
            else:
                self.canvas_world.move(self.image_bird_true, self.x, self.vitesse)
                self.canvas_world.itemconfigure(self.image_bird_true, image=self.liste_image[int(self.count_image)])
        else:
            self.vitesse += 0.06
            self.x_center_bird, self.y_center_bird = self.canvas_world.coords(self.image_bird_true)
            if (self.y_center_bird + self.vitesse + 25) > 500:
                self.canvas_world.coords(self.image_bird_true, self.x_center_bird, 475)
                self.verif_bird(0, 0, dead=True)
            else:
                self.canvas_world.move(self.image_bird_true, self.x, self.vitesse)

    def _move_pipes(self) -> None:
        # Move pipes each tick
        self.tuyau0.move_pipe()
        self.tuyau1.move_pipe()
        self.tuyau2.move_pipe()
        self.tuyau3.move_pipe()

    # #########################################################################################################################
    # La fonction Bird_move sert à déplacer l'oiseau de bas en haut ou de haut en bas. Elle sert aussi à changer l'inclinaison
    # de la tête de l'oiseau en fonction de la vitesse de descente. Tout d'abord, on place toute la fonction dans une boucle qui
    # se répète 6 fois afin de faire plus de calculs et d'être plus précis.
    # L'oiseau va donc commencer à descendre puisque la dernière valeur de self.press = False.

    # Pour la montée, self.press = True grâce au click du joueur, l'oiseau va donc monter de 2.9 pixels multiplié par 6 toutes
    # les 50 ms. Pour éviter que l'oiseau ne s'envole vers l'infini, on pose i = 0 et à chaque tour on l'incrémente de 1, ainsi au
    # bout de 30 calculs la fonction s'arrete et l'oiseau aura monté de 87 pixels en 250 ms. En ce qui concerne l'inclinaison de
    # l'oiseau, on connait la derniere valeur de l'image de la descente avec self.count_image, on va lui soustraire à chaque boucle
    # -1,2. La liste_image contient 30 images de l'oiseau ce qui permet d'avoir une bonne précision sur l'inclinaison de l'oiseau.
    # A la fin, quand i == 30, self.press = False et l'oiseau va alors descendre.

    # Pour la descente, self.press = False, on fait toujours tourner l'algorithme dans la boucle for pour la même raison.
    # On sépare tout d'abord l'algo en 2 partie, la 1ère où self.count_image < 27 et l'autre où self.count_image > 29. On sépare de
    # cette manière afin de ne pas augmenter self.count_image lorsqu'on est à la dernière image pour éviter d'avoir l'erreur
    # (IndexError: list index out of range) car self.count_image augmente à chaque boucle. Pour simuler une chute de l'oiseau,
    # on multiplie self.count_image par 1.04 et par 1.1 si  self.count_image > 5. Après avoir fait ceci, on passe au déplacement de
    # l'oiseau, on commence alors par incrémenter la vitesse de +0.055 à chaque boucle. En même temps que de déplacer l'oiseau,
    # on vérifie aussi si l'oiseau ne touche pas le sol avec if (self.y_center_bird +self.vitesse + 25) > 500, ainsi si cette condition
    # est vérifiée, on place l'oiseau à y = 475 afin d'être sûr qu'il touche bien sans dépasser le sol, on appelle la fonction vérif
    # qui nous sert à afficher le Game Over et self.verite = False afin d'arrêter la boucle de la fonction update.
    # #########################################################################################################################

    def verif_bird(self, y_pipe_center_top, y_pipe_center_down, dead=False):
        """Vérifie si l'oiseau touche un tuyau/le sol, puis lance l'animation de fin."""
        if self.verite:
            # Utiliser des variables locales (on a tout de même des attributs pré-déclarés pour éviter W0201).
            y_pipe_down = y_pipe_center_down - 250  # haut du tuyau bas
            y_pipe_top = y_pipe_center_top + 250  # bas du tuyau haut

            # Collision avec sol/tuyau ?
            if y_pipe_down < self.y_center_bird + 24 or self.y_center_bird - 24 < y_pipe_top or dead:
                # Bloque les inputs pour éviter les états incohérents
                self.root.unbind("<Button-1>")
                self.root.unbind("<space>")
                self.verite = False

                # Prépare deux versions de l'image 'Game Over' et conserve les références
                # (important en Tkinter pour éviter que GC ne les détruise)
                self.game_over_img_small = self.image.subsample(4)  # ~25%
                self.game_over_img_big = self.image.zoom(2)  # 200%

                # Affiche d’abord la petite
                self.image_game_over = self.canvas_world.create_image(350, 250, image=self.game_over_img_small)

                # Puis transition vers la grande
                self.canvas_world.after(500, self.ending)
                self.canvas_world.after(1000, lambda: self.ending(True))

                if dead:
                    # mort par sol : pas de descente d’attente
                    self.root.after(2000, self.dead)
                else:
                    # mort par tuyau : descente d’attente
                    self.wait_dead()
                    self.root.after(2000, self.dead)

    def ending(self, zoom=False):  # fonction pour afficher l'annimation de l'apparition du game over
        if zoom:
            self.image = self.image.zoom(2)  # affichage de l'image zoomée de 200% à la 2nd exécution de la fonction
        else:
            self.image = self.image.subsample(2)  # la première fois que la fonction est appelée, on affiche l'image réduite à 200%
        self.canvas_world.itemconfig(self.image_game_over, image=self.image)

    def wait_dead(self):
        """Fait descendre l'oiseau mort jusqu'au sol, devant l'image 'Game Over'."""
        x, y = self.canvas_world.coords(self.image_bird_true)  # On récupère les coordonnées de l'oiseau au moment de sa mort
        self.canvas_world.tag_raise(self.image_game_over)  # On le place au premier plan devant les tuyaux
        if y + self.vitesse + 25 < 500:  # Condition pour savoir si il a atteint le sol ou non
            self.count_image += 1.5  # On augmente count_image pour augmenter l'inclinaison
            if (
                self.count_image < 25
            ):  # Si self.count_image < 25, on continue à itemconfigure avec image = self.liste_image[int(abs(self.count_image))]
                self.canvas_world.itemconfigure(self.image_bird_true, image=self.liste_image[int(abs(self.count_image))])
                self.vitesse += 0.5  # On augmente la vitesse de descente
                self.canvas_world.move(self.image_bird_true, self.x, self.vitesse)  # On déplace l'oiseau
            else:  # Si self.count_image > 25, on fait les mêmes déplacements en mettant l'inclinaison à image = self.liste_image[28]
                self.canvas_world.itemconfigure(self.image_bird_true, image=self.liste_image[28])
                self.vitesse += 0.5  # On augmente la vitesse de descente
                self.canvas_world.move(self.image_bird_true, self.x, self.vitesse)  # On déplace l'oiseau
            self.root.after(25, self.wait_dead)  # On éxécute la fonction tant que l'oiseau n'a pas touché le sol
        else:  # Si il touche le sol, la boucle s'arrête et on place l'oiseau à y = 475 pour être sur qu'il ne dépasse pas le sol
            self.canvas_world.coords(self.image_bird_true, x, 475)

    def dead(self):
        """Post-mortem : mise à jour scores/états et proposition de restart."""
        self.count += 1
        self.average_score.append(self.compte * 100)

        y_death = 0 if self.y_center_bird < 0 else (self.y_center_bird / 475)
        self.death_pos.append((9, int(y_death * 19)))

        # Bloque la fermeture pendant le prompt
        self.root.protocol("WM_DELETE_WINDOW", print)

        self.best_score = max(self.best_score, self.compte * 100)

        self.question = askquestion("RESTART", "Perdu!\nVeux-tu recommencer")
        if self.question == "yes":  # si l'utilisateur veut recommencer, on regenère l'affichage
            self.frame_right.destroy()  # destruction des frames
            self.frame_main_game.destroy()  #
            self.build_game()  # reconstruction de la fenètre
        else:
            self.exit()  # sinon, on quitte l'application

    def count_score(self):  # Fonction servant à afficher le socre au milieu en haut de la partie en cours
        if self.compte == 10:  # Si le compte = 10, on crée l'image du chiffre des dizaines
            self.image_dizaine = self.canvas_world.create_image(322, 30, image=self.liste_nombres[self.d])
        elif self.compte == 100:  # Si le compte = 100, on crée l'image du chiffre des centaines
            self.image_centaine = self.canvas_world.create_image(304, 30, image=self.liste_nombres[self.c])
        count = str(self.compte)
        self.canvas_world.itemconfigure(
            self.image_unite, image=self.liste_nombres[int(count[-1])]
        )  # On itemconfigure le chiffre des unités à chaque fois
        self.canvas_world.tag_raise(self.image_unite)  # On met en avant devant les tuyaux à chaque fois
        if len(count) > 1:
            self.canvas_world.itemconfigure(
                self.image_dizaine, image=self.liste_nombres[int(count[-2])]
            )  # On itemconfigure le chiffre des dizaines si il le faut
            self.canvas_world.tag_raise(self.image_dizaine)  # On met en avant le chiffre des centaines devant les tuyaux
            if len(count) > 2:
                self.canvas_world.itemconfigure(
                    self.image_centaine, image=self.liste_nombres[int(count[-3])]
                )  # On itemconfigure le chiffre des centaines si il le faut
                self.canvas_world.tag_raise(self.image_centaine)  # On met en avant le chiffre des centaines devant les tuyaux

        self.canvas_world.tag_raise(self.image_bird_true)  # On met en avant l'oiseau à chaque fois


class Pipe:  # pylint: disable=too-many-arguments, too-many-instance-attributes
    def __init__(self, parent):  # Argument qui sert à récupérer les variables de la classe Flappy
        self.parent = parent
        self.move_x = -2  # Vitesse de déplacement des tuyaux
        self.test = PhotoImage(file=resource_path("flappy_bird/Ressources/test.png"))  # Tuyau du bas
        self.test3 = PhotoImage(file=resource_path("flappy_bird/Ressources/test3.png"))  # Tuyau du haut
        self.length_pipe = 500  # Taille de l'image des tuyaux, utile pour les calculs de placement du tuyau

        # ---- Initialized to satisfy pylint W0201 ----
        self.y_pipe_top = 0
        self.y_pipe_down = 0
        self.top_pipe = None
        self.down_pipe = None
        self.x_center_top_pipe = 0
        self.y_center_top_pipe = 0
        self.x_center_down_pipe = 0
        self.y_center_down_pipe = 0
        # ---------------------------------------------

    def create_pipe(self, x_pipe, y_pipe):  # Fonction servant à créer l'image du tuyau
        self.y_pipe_top = y_pipe - 75  # Permet de créer l'espace entre les 2 tuyaux
        self.y_pipe_down = y_pipe + 75  # ce qui fait un écart de 150 pixels
        self.top_pipe = self.parent.canvas_world.create_image(
            x_pipe + 75, self.y_pipe_top - self.length_pipe / 2, image=self.test3
        )  # Création du tuyau haut
        self.down_pipe = self.parent.canvas_world.create_image(
            x_pipe + 75, self.y_pipe_down + self.length_pipe / 2, image=self.test
        )  # Création du tuyau bas

    def move_pipe(self):  # Fonction servant à déplacer le tuyau à l'horizontal
        self.parent.canvas_world.move(self.top_pipe, self.move_x, 0)  # Déplacement des 2 tuyaux
        self.parent.canvas_world.move(self.down_pipe, self.move_x, 0)
        # On récupère les coordonnées des 2 tuyaux
        self.x_center_top_pipe, self.y_center_top_pipe = self.parent.canvas_world.coords(self.top_pipe)
        self.x_center_down_pipe, self.y_center_down_pipe = self.parent.canvas_world.coords(self.down_pipe)
        self.verif_pipe()  # On appelle verif_pipe à chaque déplacement du tuyau

    def verif_pipe(self):  # Fonction servant à vérifier si le tuyau est dans des intervalles donnés
        if self.x_center_top_pipe + 65 < 0:
            # Si le tuyau a quitté l'écran, on le supprime et on le recrée à droite
            self.parent.canvas_world.delete(self.top_pipe)  # Suppression du haut
            self.parent.canvas_world.delete(self.down_pipe)  # Suppression du bas
            self.create_pipe(randint(1425, 1475), randint(100, 400))  # Nouveau tuyau

        if 40 < self.x_center_top_pipe < 210:  # Au niveau de l'oiseau
            self.parent.verif_bird(self.y_center_top_pipe, self.y_center_down_pipe)

        # Le tuyau vient de dépasser l'oiseau
        if 100 >= self.x_center_top_pipe + 60 > 98:
            self.parent.compte += 1
            self.parent.count_score()


def launch_flappy_bird(user):  # fonction pour commencer le jeu
    jeux = Bird(user)  # création de l'instance
    if jeux.count != 0:
        return (
            jeux.best_score,
            sum(jeux.average_score) / jeux.count,
            (time() - jeux.time_start) / jeux.count,
            jeux.count,
            jeux.death_pos,
        )  # renvoi des données
    return (0, 0, 0, 0, [])
