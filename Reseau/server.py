import socket #imports
import select
import pickle
import os

###################--------------Initialisation du serveur---------------###################################
Host = "192.168.1.30" #ip locale sinon "90.91.3.228"
Port = 1243

if os.path.isfile("./data"): #si le fichier est créé, on charge ce qu'il y a dessus
    with open("data", "rb") as f:
        players = pickle.load(f)
else:
    players = {} #dictionnaire des joueurs


#########################-----------Fonction Save-------------------####################################
def save(): #fonction pour sauvegarder les scores des joueurs dans le fichier
    with open("data", "wb") as f:
        pickle.dump(players, f)

####################----------------Fonction Process--------------------------###################################

def process(msg): #fonction pour décider de ce qu'il faut retourner au client
    global players
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

        print("player {} scored {} in {}".format(list[1], list[3], list[2]))
        try:
            if players[list[1]][list[2]] < float(list[3]): #si le score marqué est plus grand que le précédent, on le retiends
                players[list[1]][list[2]] = float(list[3])
        except:
            players[list[1]] = {"Tete": 0, "Snake": 0, "Ghost": 0, "Minesweeper": 0, "Tetris": 0, "Pendu": 0, "Pong": 0, "Space": 0, "Flappy": 0}
            players[list[1]][list[2]] = float(list[3])
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
        try:
            players[list[1]]["Tete"] < 0
        except:
            players[list[1]] = {"Tete": 0, "Snake": 0, "Ghost": 0, "Minesweeper": 0, "Tetris": 0, "Pendu": 0, "Pong": 0, "Space": 0, "Flappy": 0} #création d'un nouveau joueur
        return pickle.dumps(players[list[1]])


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #création du socket
s.bind((Host, Port)) #on lie l'adresse ip et le ports
s.listen(5) #nombre de connections simultanées entrantes acceptées
print("Server is listening port {}.".format(Port))

launched = True
client_list = [] #liste des clients connectés
while launched == True: #tant que cette vairable est vraie, le serveur tourne

    connection_asked, wlist, xlist = select.select([s], [], [], 0.05) #on regarde les clients qui veullent commencer une connection

    for connection in connection_asked: #on accepte les connections et on stocke les sockets
        clientsocket, adress = connection.accept()
        print("connected to {}".format(adress[0]))
        client_list.append(clientsocket) #on ajoute les clients cceptés à la liste des clients

    Client_To_Read = []

    try:
        Client_To_Read, wlist, xlist = select.select(client_list, [], [], 0.05) #si possible, on regarde les messages envoyés par les clients
    except select.error:
        pass
    else:
        for client in Client_To_Read: #pour chaque client, on observe le message envoyé
            try: #on essaye de décoder le message
                msg = client.recv(1024).decode("utf-8")
                answer = process(msg) #on créé la réponse suivant la demande
                client.send(answer) #et on renvois cette réponse
                if msg == "end": #si un utilisateur envoie end , on stoppe le serveur
                    launched = False
            except: #si on ne peut pas lire le message, c'est que le socket n'est pas valide donc le client est déconnecté, on le supprime de la liste
                print("lost connection")
                client_list.remove(client) #si on a une erreur, cela veut dire que le client s'est déconnecté, on le supprime

print("Ending connections")
for client in client_list: #fin des connections
    client.close()
s.close()
save()
print(players.keys())
print(players[player].values())
