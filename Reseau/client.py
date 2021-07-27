import socket #imports
import pickle
from time import sleep

#Host = "92.91.130.103" #création des variables 0 au lieu de 5
Host = "localhost"
Port = 8000

def push_score(pseudo, game, score_max, score, count, time, pos = []):
    """pour ajouter un score après une partie

    pseudo: nom du joueur
    game: nom du jeu
    score_max: score maximal de la session
    score: liste des scores des parties jouées
    count: nombre de parties jouées
    time: temps passé a faire ces parties
    pos: emplacement de mort, facultatif """

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #création du socket
    s.settimeout(0.4)
    try:
        s.connect((Host, Port)) #on lie l'adresse ip et le port
    except:
        return
    msg_To_send = "add {} {} {} {} {} {} {}".format(pseudo, game, score_max, score, count, time, pos) #on envois la commande pour ajouter la partie actuelle
    s.send(msg_To_send.encode())
    sleep(0.4)
    s.recv(1024) #la réponse n'est pas utile mais il y en a une
    s.close()

def get_score_list():
    """ récupérer le scoreboard"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #création du socket
    s.settimeout(0.4)
    try:
        s.connect((Host, Port)) #on lie l'adresse ip et le port
    except:
        return [("Hors Ligne", 0)]
    s.send(b"list") #on demande la liste
    response = s.recv(1024)
    response = pickle.loads(response) #on désérialise la réponse pour récupérer un dictionnaire
    s.close()
    return response #on renvois le scoreboard

def get_game_score_list(game):
    """ récupérer le scoreboard pour un jeu spécifique"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #création du socket
    s.settimeout(0.4)
    try:
        s.connect((Host, Port)) #on lie l'adresse ip et le port
    except:
        return [("Hors Ligne", 0)]
    s.send("game_list {}".format(game).encode("utf-8")) #on demande la liste
    response = s.recv(1024)
    response = pickle.loads(response) #on désérialise la réponse pour récupérer un dictionnaire
    s.close()
    return response #on renvois le scoreboard

def get_player_score(User_name):
    """récupération des scores d'un joueur"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #création du socket
    s.settimeout(0.4)
    try:
        s.connect((Host, Port)) #on lie l'adresse ip et le port
    except:
        return {"Tete": 0, "Snake": 0, "Ghost": 0, "Minesweeper": 0, "Tetris": 0, "Pendu": 0, "Pong": 0, "Flappy": 0}
    s.send("player_score {}".format(User_name).encode("utf-8")) #on demande la liste
    response = s.recv(1024)
    response = pickle.loads(response) #on désérialise la réponse pour récupérer un dictionnaire
    s.close()
    return response #on renvois le scoreboard

def get_statistics():
    """récupération des données statistiques récoltées"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #création du socket
    s.settimeout(1)
    try:
        s.connect((Host, Port)) #on lie l'adresse ip et le port
    except:
        return [{"Tete": {"moyenne":[0, 0], "player_count":{}}, "Snake": {"moyenne":[0, 0], "player_count":{}}, "Ghost": {"moyenne":[0, 0], "player_count":{}}, "Minesweeper": {"moyenne":[0, 0], "player_count":{}},\
         "Tetris": {"moyenne":[0, 0], "player_count":{}}, "Pendu": {"moyenne":[0, 0], "player_count":{}}, "Pong": {"moyenne":[0, 0], "player_count": {}}, "Flappy": {"moyenne":[0, 0], "player_count":{}} }, \
         {"Snake": {}, "Minesweeper": {}, "Flappy": {}, "Pong": {}}, \
         {"Tete": {"moyenne": 0, "player_count":{}}, "Snake": {"moyenne":0, "player_count":{}}, "Ghost": {"moyenne":0, "player_count":{}}, "Minesweeper": {"moyenne":0, "player_count":{}},\
         "Tetris": {"moyenne":0, "player_count":{}}, "Pendu": {"moyenne":0, "player_count":{}}, "Pong": {"moyenne":0, "player_count": {}}, "Flappy": {"moyenne":0, "player_count":{}} }]
    s.send("statistics_get ".encode("utf-8")) #on demande la liste
    response = b""
    while True:
        packet = s.recv(4096)
        response += packet
        if len(packet) < 4096:
            break

    response = pickle.loads(response) #on désérialise la réponse pour récupérer un dictionnaire

    s.close()

    return response
