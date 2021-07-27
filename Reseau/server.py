import socket #imports
import select
import pickle
import os

###################--------------Initialisation du serveur---------------###################################
#Host = "192.168.1.30" #ip locale sinon "90.91.3.228"
Host = "localhost"
Port = 8000

if os.path.isfile("./data"): #si le fichier est créé, on charge ce qu'il y a dessus
    with open("data", "rb") as f:
        players = pickle.load(f)
else:
    players = {} #dictionnaire des joueurs

if os.path.isfile("./statistics"): #si le fichier est créé, on charge ce qu'il y a dessus
    with open("statistics", "rb") as f:
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
    with open("data", "wb") as f:
        pickle.dump(players, f)
    with open("statistics", "wb") as f:
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

        print("player {} scored {} in {} with {} parties".format(player, score_max, jeu, count))
        print(players)

        if players[player][jeu] < score_max: #si le score marqué est plus grand que le précédent, on le retiends
            players[player][jeu] = score_max

        #players[player] = {"Tete": 0, "Snake": 0, "Ghost": 0, "Minesweeper": 0, "Tetris": 0, "Pendu": 0, "Pong": 0, "Flappy": 0} #



        #incrémentation du nombre de parties jouées par joueur dans un jeu
        #la moyenne du joueur = nb_parties*moyenne + score
        print(yes1)
        statistics[0][jeu]["player_count"][player][0] += count
        print(yes2)
        statistics[0][jeu]["player_count"][player][1] = ((statistics[0][jeu]["player_count"][player][0]) * statistics[0][jeu]["player_count"][player][1] + score*count) / (statistics[0][jeu]["player_count"][player][0] + count)

        #calcul de la nouvelle moyenne et du nouveau compte total
        statistics[0][jeu]["moyenne"][0] = (statistics[0][jeu]["moyenne"][0] * statistics[0][jeu]["moyenne"][1] + score*count)/(statistics[0][jeu]["moyenne"][1]+count)

        #partie sur le temps joué
        statistics[2][jeu]["player_count"][player] = (statistics[2][jeu]["player_count"][player]*(statistics[0][jeu]["player_count"][player]-count) + time*count)/(statistics[0][jeu]["player_count"][player])


        statistics[2][jeu]["moyenne"] = (statistics[2][jeu]["moyenne"] + time*count)/(statistics[0][jeu]["moyenne"][1] + count)

        #nombre de parties par jeu
        statistics[0][jeu]["moyenne"][1] += count


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
                    if mode = 0:
                        statistics[mode][jeu]['player_count'][list[1]] = [0 , 0]
                    if mode = 2:
                        statistics[mode][jeu]['player_count'][list[1]] = 0


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

print("Ending connections")
for client in client_list: #fin des connections
    client.close()
s.close()
save()
