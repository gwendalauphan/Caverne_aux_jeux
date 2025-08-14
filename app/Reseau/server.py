import socket #imports
import select
import pickle
import signal
import socket
import sys
import os
import logging
import threading
import tkinter as tk
from tkinter import scrolledtext

from pathlib import Path

# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from Utils.utils import *

# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("CaverneAuxJeuxServer")

logger.info("The server app is running.")




###################--------------Initialisation du serveur---------------###################################
#Host = "192.168.1.30" #ip locale sinon "90.91.3.228"

HOST = '0.0.0.0'
PORT = 8000

app_name = "Game_Caverne"

if getattr(sys, 'frozen', False):
    # Exécuté sous forme de bundle PyInstaller
    if os.name == "nt": # Windows
        data_directory = Path.home() / "AppData" / "Local" / app_name
    elif os.name == "posix": # Linux
        data_directory = Path.home() / ".local" / "share" / app_name

else:
    # Exécuté sous forme de script Python
    data_directory = Path(__file__).resolve().parent

data_directory.mkdir(parents=True,exist_ok=True)  # Crée le répertoire s'il n'existe pas

data_players_directory = "{}/data_players".format(data_directory)
#créer le dossier data_players s'il n'existe pas
if not os.path.isdir(resource_path(data_players_directory)):
    os.mkdir(resource_path(data_players_directory))

# Chemin vers le fichier
data_file_path = resource_path("{}/data".format(data_players_directory))
statistics_file_path = resource_path("{}/statistics".format(data_players_directory))
logger.info(data_file_path)

# Vérifiez si le fichier existe
if os.path.isfile(data_file_path):
    # Si le fichier est créé, on charge ce qu'il y a dessus
    with open(data_file_path, "rb") as f:
        players = pickle.load(f)
else:
    players = {} #dictionnaire des joueurs

if os.path.isfile(statistics_file_path): #si le fichier est créé, on charge ce qu'il y a dessus
    with open(statistics_file_path, "rb") as f:
        statistics = pickle.load(f)
else:
    statistics = [{"Tete": {"moyenne":[0, 0], "player_count":{}}, "Snake": {"moyenne":[0, 0], "player_count":{}}, "Ghost": {"moyenne":[0, 0], "player_count":{}}, "Minesweeper": {"moyenne":[0, 0], "player_count":{}},\
         "Tetris": {"moyenne":[0, 0], "player_count":{}}, "Pendu": {"moyenne":[0, 0], "player_count":{}}, "Pong": {"moyenne":[0, 0], "player_count": {}},  "Flappy": {"moyenne":[0, 0], "player_count":{}} }, \
         {"Snake": {}, "Minesweeper": {}, "Flappy": {}, "Pong": {}}, \
         {"Tete": {"moyenne": 0, "player_count":{}}, "Snake": {"moyenne":0, "player_count":{}}, "Ghost": {"moyenne":0, "player_count":{}}, "Minesweeper": {"moyenne":0, "player_count":{}},\
         "Tetris": {"moyenne":0, "player_count":{}}, "Pendu": {"moyenne":0, "player_count":{}}, "Pong": {"moyenne":0, "player_count": {}}, "Flappy": {"moyenne":0, "player_count":{}} }]
    #scores, nombre de parties / emplacements de mort / temps joué

#########################-----------Fonction Save-------------------####################################
def save(): #fonction pour sauvegarder les scores des joueurs dans le fichier
    with open(data_file_path, "wb") as f:
        pickle.dump(players, f)
    with open(statistics_file_path, "wb") as f:
        pickle.dump(statistics, f)


####################----------------Fonction Process--------------------------###################################

def process(msg): #fonction pour décider de ce qu'il faut retourner au client
    global players, statistics
    list = msg.split(" ") #on split
    command = list[0] #la commande est le premier mot, on le stocke pour plus de simplicité

    """################--------------Condition pour l'ajout du nouveau meilleur score----------#############################"""
    ##########################
    #list[1] = nom du joueur
    #list[3] = score du joueur
    #list[2] = jeu auquel le joueur joue
    #########################

    """################--------------Condition pour l'ajout du nouveau meilleur score----------#############################"""

    if command == "add":     #si la commande est add, on ajoute le score
        player = list[1]
        jeu = list[2]
        score_max = float(list[3])
        score = float(list[4])
        count = int(list[5])
        time = float(list[6])

        #allo Snake 160      100.0    2              9.517096400260925 [(9, 19), (17, 19)]
        #nom jeu score max  moyen   nb parties             time

        logger.debug("player {} scored {} in {} with {} parties".format(player, score_max, jeu, count))

        if players[player][jeu] < score_max: #si le score marqué est plus grand que le précédent, on le retiends
            players[player][jeu] = score_max

        #players[player] = {"Tete": 0, "Snake": 0, "Ghost": 0, "Minesweeper": 0, "Tetris": 0, "Pendu": 0, "Pong": 0, "Flappy": 0} #


        #incrémentation du nombre de parties jouées par joueur dans un jeu
        #la moyenne du joueur = nb_parties*moyenne + score

        statistics[0][jeu]["player_count"][player][0] += count
        statistics[0][jeu]["moyenne"][1] += count


        if statistics[0][jeu]["player_count"][player][0] != 0:
            #moyenne de scorer du joueur
            statistics[0][jeu]["player_count"][player][1] = ((statistics[0][jeu]["player_count"][player][0]-count) * statistics[0][jeu]["player_count"][player][1] + score*count) / (statistics[0][jeu]["player_count"][player][0])

            #temps moyen du joueur
            statistics[2][jeu]["player_count"][player] = (statistics[2][jeu]["player_count"][player]*(statistics[0][jeu]["player_count"][player][0]-count) + time)/(statistics[0][jeu]["player_count"][player][0])



        if statistics[0][jeu]["moyenne"][1]+count != 0:
            #calcul de la nouvelle moyenne et du nouveau compte total
            statistics[0][jeu]["moyenne"][0] = (statistics[0][jeu]["moyenne"][0] * (statistics[0][jeu]["moyenne"][1]-count) + score*count)/(statistics[0][jeu]["moyenne"][1])

            #Temps en moyenne par partie
            statistics[2][jeu]["moyenne"] = (statistics[2][jeu]["moyenne"]*(statistics[0][jeu]["moyenne"][1]-count) + time)/(statistics[0][jeu]["moyenne"][1])

        #nombre de parties par jeu



        if jeu in ["Snake", "Pong", "Minesweeper", "Flappy"]: #compte des emplacements de mort dans le jeu Snake
            pos = eval("".join(list[7:]))

            try:
                statistics[1][jeu][player]
            except: statistics[1][jeu][player] = {}

            for place in pos:
                try:
                    statistics[1][jeu][player][place] += 1
                except:
                    statistics[1][jeu][player][place] = 1

        save()
        return b"ok" #le retour n'est pas important

        """################--------------Condition pour l'ajout du Classement Total----------#############################"""

    elif command == "list": #si c'est la liste, on sérialise le dictionnaire et on l'envois
        total_score = []
        for player in players.keys(): #pour chaque joueur, on calcule son score total et on l'ajoute dans une liste
            sum = 0
            for jeu in players[player].values():
                sum += jeu
            total_score.append((player, sum))
        total_score.sort(key = lambda list: list[1], reverse = True) #on trie la liste et on renvois les 10 premiers éléments
        return pickle.dumps(total_score[:10])

        """################--------------Condition pour l'ajout du Classement du jeu----------#############################"""

    elif command == "game_list": #si c'est la liste, on sérialise le dictionnaire et on l'envois
        total_score = []
        for player in players.keys(): #pour chaque joueur, on calcule son score total et on l'ajoute dans une liste
            total_score.append((player, players[player][list[1]]))
        total_score.sort(key = lambda list: list[1], reverse = True) #on trie la liste et on renvois les 10 premiers éléments
        return pickle.dumps(total_score[:10])

        """##################----------------Envois du score d'un joueur------------------------#############################"""
    elif command == "player_score":
        return pickle.dumps(players[list[1]])

    elif command == "statistics_get":
        return pickle.dumps(statistics)


        """##################----------------Ajout d'un nouveau joueur------------------------#############################"""
    elif command == "check_new_player":
        if (list[1] not in players):
            players[list[1]] = {"Tete": 0, "Snake": 0, "Ghost": 0, "Minesweeper": 0, "Tetris": 0, "Pendu": 0, "Pong": 0, "Flappy": 0} #création d'un nouveau joueur
            for mode in range(len(statistics)):
                for jeu in statistics[mode]:
                    if mode == 0:
                        statistics[mode][jeu]['player_count'][list[1]] = [0 , 0]
                    if mode == 2:
                        statistics[mode][jeu]['player_count'][list[1]] = 0


def handle_sigint(sig, frame):
    logger.info('Interrupt signal received. Shutting down the server...')
    save()
    sys.exit(0)

def handle_sigtstp(sig, frame):
    logger.info('Stop signal received (Ctrl+Z). Shutting down the server...')
    save()
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

class TkLogHandler(logging.Handler):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record):
        msg = self.format(record)
        self.text_widget.after(0, self.text_widget_insert, msg)

    def text_widget_insert(self, msg):
        self.text_widget.insert(tk.END, msg + '\n')
        self.text_widget.see(tk.END)

# --- Fixed Apple-style ToggleSwitch with ON/OFF visible ---
class ToggleSwitch(tk.Canvas):
    def __init__(self, master, width=60, height=34, padding=2,
                 on_color="#34C759", off_color="#E5E5EA", knob_color="#FFFFFF",
                 text_on="ON", text_off="OFF", initial=False, command=None, **kwargs):
        super().__init__(master, width=width, height=height, highlightthickness=0,
                         bg=master.cget("bg"), **kwargs)
        self.w = width
        self.h = height
        self.r = (height - 2*padding) // 2
        self.pad = padding
        self.on_color = on_color
        self.off_color = off_color
        self.knob_color = knob_color
        self.command = command
        self.text_on = text_on
        self.text_off = text_off
        self._state = bool(initial)

        # track parts
        self.track_left = self.create_oval(0,0,0,0, outline="", fill="")
        self.track_rect = self.create_rectangle(0,0,0,0, outline="", fill="")
        self.track_right = self.create_oval(0,0,0,0, outline="", fill="")

        # text labels INSIDE the switch
        self.label_on = self.create_text(self.w*0.28, self.h/2, text=self.text_on,
                                         fill="white", font=("Arial", int(self.h/2.9), "bold"))
        self.label_off = self.create_text(self.w*0.72, self.h/2, text=self.text_off,
                                          fill="white", font=("Arial", int(self.h/2.9), "bold"))

        # knob on top
        self.knob = self.create_oval(0, 0, 0, 0, outline="", fill=self.knob_color)

        self.bind("<Button-1>", self._toggle)
        self.configure(cursor="hand2")
        self._redraw()

    def _toggle(self, _event=None):
        self.set(not self._state)
        if self.command:
            self.command(self._state)

    def set(self, value: bool):
        value = bool(value)
        if value != self._state:
            self._state = value
            self._redraw()

    def get(self) -> bool:
        return self._state

    def _redraw(self):
        # track color
        color = self.on_color if self._state else self.off_color
        for item in (self.track_left, self.track_rect, self.track_right):
            self.itemconfig(item, fill=color)

        p, r, w, h = self.pad, self.r, self.w, self.h
        self.coords(self.track_left, p, p, p+2*r, p+2*r)
        self.coords(self.track_rect, p+r, p, w-p-r, h-p)
        self.coords(self.track_right, w-p-2*r, p, w-p, p+2*r)

        # knob position
        if self._state:
            cx = w - p - r
            self.itemconfig(self.label_on, state="normal")
            self.itemconfig(self.label_off, state="hidden")
        else:
            cx = p + r
            self.itemconfig(self.label_on, state="hidden")
            self.itemconfig(self.label_off, state="normal")

        cy = p + r
        self.coords(self.knob, cx-r, cy-r, cx+r, cy+r)
        self.itemconfig(self.knob, fill=self.knob_color)

# --- Updated ServerApp layout ---
class ServerApp:
    def __init__(self, master):
        self.master = master
        master.title("Caverne Aux Jeux Server")
        master.geometry("600x400")

        self.is_running = False
        self.server_thread = None
        self.stop_event = threading.Event()

        # Top bar frame
        top = tk.Frame(master)
        top.pack(fill=tk.X, pady=10, padx=10)

        # Label + toggle aligned on left
        tk.Label(top, text="Start/Stop Server").pack(side=tk.LEFT, padx=(0,8))
        self.toggle = ToggleSwitch(top, initial=False, command=self.on_toggle)
        self.toggle.pack(side=tk.LEFT)

        # Quit button on right
        self.quit_btn = tk.Button(top, text="Quit", command=self.quit_app)
        self.quit_btn.pack(side=tk.RIGHT)

        # Logs
        self.log_text = scrolledtext.ScrolledText(master, state='normal', height=20)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0,10))

        self.tk_handler = TkLogHandler(self.log_text)
        self.tk_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(self.tk_handler)

        self.log_text.insert(tk.END, "Server GUI ready.\n")
        self.log_text.see(tk.END)

        master.protocol("WM_DELETE_WINDOW", self.on_close)

        # Auto-start server
        self.toggle.set(True)
        self.start_server()

    # The toggle callback receives True/False
    def on_toggle(self, want_on: bool):
        if want_on and not self.is_running:
            self.start_server()
        elif not want_on and self.is_running:
            self.stop_server()

    def start_server(self):
        self.stop_event.clear()
        self.server_thread = threading.Thread(target=self.run_server, daemon=True)
        self.server_thread.start()
        self.is_running = True
        self._log("Server starting...")

    def stop_server(self):
        self.stop_event.set()
        self._log("Stopping server...")
        # Optionally wait briefly for clean shutdown (non-blocking UI)
        self.master.after(100, self._check_stopped)

    def _check_stopped(self):
        # If thread ended, reflect state; else check again soon
        if self.server_thread and not self.server_thread.is_alive():
            self.is_running = False
            self.toggle.set(False)
            self._log("Server stopped.")
        else:
            self.master.after(100, self._check_stopped)

    def run_server(self):
        try:
            start_server(HOST, PORT, self.stop_event)
        except Exception as e:
            logger.error(f"Server error: {e}")
        finally:
            # Ensure UI reflects stopped state on exit of thread
            self.is_running = False
            self.master.after(0, lambda: self.toggle.set(False))

    def quit_app(self):
        # Stop server if needed, then exit
        self.stop_event.set()
        if self.server_thread and self.server_thread.is_alive():
            # avoid freezing UI: poll until stopped
            self._log("Closing server and quitting...")
            self.master.after(100, self._quit_when_stopped)
        else:
            self.on_close()

    def _quit_when_stopped(self):
        if self.server_thread and self.server_thread.is_alive():
            self.master.after(100, self._quit_when_stopped)
        else:
            self.on_close()

    def on_close(self):
        self.stop_event.set()
        try:
            save()  # your function
        except Exception:
            pass
        self.master.destroy()

    def _log(self, msg: str):
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)

def start_server(host, port, stop_event=None):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(5)
    logger.info(f"Server is listening on port {port}")

    launched = True
    client_list = []

    try:
        while launched and (stop_event is None or not stop_event.is_set()):
            # Gérer les demandes de nouvelles connexions
            connection_asked, _, _ = select.select([s], [], [], 0.05)

            for connection in connection_asked:
                client_socket, _ = connection.accept()
                ip, port = client_socket.getpeername()
                logger.info(f"Client {ip} from Port {port} connected")
                client_list.append(client_socket)

            # Gérer les messages entrants des clients connectés
            try:
                clients_to_read, _, _ = select.select(client_list, [], [], 0.05)
            except select.error:
                pass
            else:
                for client in clients_to_read:
                    #try: #on essaye de décoder le message
                    msg = client.recv(1024).decode("utf-8")
                    answer = process(msg) #on créé la réponse suivant la demande
                    if type(answer) == type(None):
                        client_list.remove(client)
                        client.close()
                        logger.info(f"Client {ip} from Port {port} disconnected - Reason: Msg type None")
                    else:
                        client.send(answer)
                        # Remove and close client after response
                        client_list.remove(client)
                        client.close()
                        logger.info(f"Client {ip} from Port {port} disconnected - Answer sent to client")
                    if msg == "end":
                        launched = False
                #except: client_list.remove(client)#si on ne peut pas lire le message, c'est que le socket n'est pas valide donc le client est déconnecté, on le supprime de la liste
                #si on a une erreur, cela veut dire que le client s'est déconnecté, on le supprime

    finally:
        for client in client_list:
            client.close()
        s.close()
        logger.info("Server socket closed.")

if __name__ == '__main__':
    # Acquire the singleton guard *before* creating your UI
    _guard_socket = acquire_single_instance(port=54322, logger=logger)  # pick a fixed port for your app
    import argparse
    parser = argparse.ArgumentParser(description="Caverne Aux Jeux Server")
    parser.add_argument('--no-gui', action='store_true', help='Run server without GUI')
    args = parser.parse_args()

    if args.no_gui:
        start_server(HOST, PORT)
        save()
    else:
        root = tk.Tk()
        app = ServerApp(root)
        root.mainloop()
        save()
