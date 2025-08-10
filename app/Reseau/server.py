import socket #imports
import select
import pickle
import signal
import socket
import sys
import os
import logging

from pathlib import Path

# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("CaverneAuxJeuxServer")

logger.info("The server app is running.")

def resource_path(relative_path):
    try:
        # Support pour les applications empaquetées avec PyInstaller
        base_path = Path(sys._MEIPASS)
    except Exception:
        # Utilisation du chemin du répertoire du script main.py pour les exécutions non empaquetées
        base_path = Path(__file__).resolve().parent.parent

    # Construction du chemin complet
    full_path = base_path / relative_path

    return str(full_path)



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

def start_server(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(5)
    logger.info(f"Server is listening on port {port}")

    launched = True
    client_list = []  # liste des clients connectés

    try:
        while launched:
            # Gérer les demandes de nouvelles connexions
            connection_asked, wlist, xlist = select.select([s], [], [], 0.05)

            for connection in connection_asked:
                client_socket, addr = connection.accept()
                logger.info(f"Connected to {addr[0]}")
                client_list.append(client_socket)

            # Gérer les messages entrants des clients connectés
            try:
                clients_to_read, wlist, xlist = select.select(client_list, [], [], 0.05)
            except select.error:
                pass
            else:
                for client in clients_to_read:
                    #try: #on essaye de décoder le message
                    msg = client.recv(1024).decode("utf-8")
                    answer = process(msg) #on créé la réponse suivant la demande
                    if type(answer) == type(None):
                        client_list.remove(client)
                    else:
                        client.send(answer) #et on renvois cette réponse
                    if msg == "end": #si un utilisateur envoie end , on stoppe le serveur
                        launched = False
                #except: client_list.remove(client)#si on ne peut pas lire le message, c'est que le socket n'est pas valide donc le client est déconnecté, on le supprime de la liste
                #si on a une erreur, cela veut dire que le client s'est déconnecté, on le supprime

    finally:
        for client in client_list:
            client.close()
        s.close()
        logger.info("Server socket closed.")

if __name__ == '__main__':
    start_server(HOST, PORT)

save()
