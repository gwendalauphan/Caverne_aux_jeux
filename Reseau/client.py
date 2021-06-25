import socket #imports
import pickle

Host = "92.91.130.103" #création des variables
Port = 1243

def push_score(pseudo, game, score):
    """pour ajouter un score après une partie """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #création du socket
    s.settimeout(0.2)
    try:
        s.connect((Host, Port)) #on lie l'adresse ip et le port
    except:
        return
    msg_To_send = "add {} {} {}".format(pseudo, game, score) #on envois la commande pour ajouter la partie actuelle
    s.send(msg_To_send.encode())
    s.recv(1024) #la réponse n'est pas utile mais il y en a une
    s.close()

def get_score_list():
    """ récupérer le scoreboard"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #création du socket
    s.settimeout(0.2)
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
    s.settimeout(0.2)
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
    s.settimeout(0.2)
    try:
        s.connect((Host, Port)) #on lie l'adresse ip et le port
    except:
        return {"Tete": 0, "Snake": 0, "Ghost": 0, "Minesweeper": 0, "Tetris": 0, "Pendu": 0, "Pong": 0, "Space": 0}
    s.send("player_score {}".format(User_name).encode("utf-8")) #on demande la liste
    response = s.recv(1024)
    response = pickle.loads(response) #on désérialise la réponse pour récupérer un dictionnaire
    s.close()
    return response #on renvois le scoreboard
#https://pythonprogramming.net/pickle-objects-sockets-tutorial-python-3/
