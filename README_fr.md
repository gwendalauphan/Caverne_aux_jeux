# Caverne aux Jeux

### 👉 [🇬🇧 English version](README.md)

pyinstaller --onefile --add-data 'app/Data/*:Data/' --add-data 'app/Fantome/Ressources/Images/*:Fantome/Ressources/Images/' --add-data 'app/Flappy_Bird/Ressources/*:Flappy_Bird/Ressources/' --add-data 'app/Minesweeper/Images/*:Minesweeper/Images/' --add-data 'app/Parametters/*:Parametters/' --add-data 'app/Pendu/ressources/*:Pendu/ressources/' --add-data 'app/Pong/res/*:Pong/res/' --add-data 'app/Snake/images/*:Snake/images/' --add-data 'app/Tete_chercheuse/image/*:Tete_chercheuse/image/'   --add-data 'app/Tetris/Images/*:Tetris/Images/' --add-data 'app/thumbnail/*:thumbnail/'  --hidden-import='PIL._tkinter_finder' --windowed --noconsole app/main.py

pyinstaller --onefile --windowed --noconsole app/Reseau/server.py

Répertoire avec le projet d'ISN de fin d'année

plein de mini-jeux
-> morpion, snake, puissance 4, pac man, tetris, robot tete chercheuse, qui-est-ce?, space invaders,
pendu, pong, demineur, phantôme

## mardi 26 mars 2019:
début du projet et assemblage des idées

début de la tete chercheuse

Mise en place du repository GitHub avec syncronisation entre les ordinateurs.

## mercredi 27 mars 2019:
début réseau: Script pour transmetre un dictionnaire par TCP connection possible par pusieurs clients et la connection/déconnection est gérée

Finalisation du jeu de tête chercheuse

début de la création de l'interface principale

## Jeudi 28 mars 2019:
Bug de duplication du robot après 2ème essai
Bug : Inversement du sens du robot après 2ème essai
Bug sur le timer

Ajout de textures pour le jeux tête chercheuse et ajout pièces pour avoir un bonus de point

### hébergement du serveur sur raspberry: le serveur est acessible en permanence


## Vendredi 29 mars 2019:
ajout de l'interface avec les règles du jeux et gestion de la fin ajout de la page du scoreboard au début du jeu

envoi du scoreboard avec les 10 meilleurs joueurs et stockage des données dans un fichier

Amélioration de la page des rêgles

## Samedi 30 mars 2019:
création de la classe scoreboard

création d'une fonction pour avoir les 10 meilleurs joueurs dans un jeu spécifique

## Dimanche 31 mars 2019:
création du classement Total dans la page principale

Ajout de la demande du pseudo au départ

serveur: ajout d'une fonction pour récupérer le score d'un joueur en particulier

## Lundi 1 avril 2019:
Finalisation des détails de tete chercheuse, il ne rest plus qu'à créer une jolie interface graphique
Début de Snake: création du jeu a l'aide d'une classe englobant tout le jeux
Recherche et découpage des images du serpent ainsi que de la pomme.

## Mardi 2 avril 2019:
Snake: affichage des images fin de la mécanique de jeux

### Tete chercheuse fini
Snake fonctionnel avec gestion du score et mort
Début de Fantome, mise en place de la grille et du niveau (Bug le liste)??

## Mercredi 3 avril 2019:
Continuer Fantome et finir Snake
Gros Bug d'algo de fantome, commencement du démineur.
Faire l'inversement de Tom(image)

## Jeudi 4 avril 2019:
Penser à la bombe du snake en dessous de 50 de longueur/Faire peut etre une fin au cas où on gagnerait la partie/ penser a pouvoir changer les touches

Graphique du snake en devellopement

Fin des règles du snake

fin du système de jeux du démineur

## Vendredi 5 avril 2019:
débug serveur, début de Pendu, interface de Snake et Fantome, ajout de la liste de mots français

## Dimanche 7 avril 2019:
Fin du pendu, le jeu est totalement fonctionnel

### Snake finis

## Lundi 8 avril 2019:
début et fin des mécaniques de snake

explication du fonctionnement de pong et création des fichiers

## Mercredi 18 Avril
reprise du projet
ajout des meilleurs joueurs pour le snake et le tetris

partie graphique améliorée

## Dimanche 21 Avril 2019

amélioration de l'algorithme de placement des bombes démineur

### Fantome finis

## Lundi 22 Avril 2019:

correction algorithme démineur, correction niveaux Tetris

ajout de la barre de scroll dans le menus principal pour faire défiler les jeux

## Jeudi 25 Avril 2019:

Début de Flappy Bird

## Luni 28 Avril 2019:

Fin du jeu Flappy Bird avec commentaires détaillés

Début de la partie aide dans le menu

## CI/CD

This project uses GitHub Actions for continuous integration:

- On every push and pull request, the workflow:
  - Installs dependencies and runs a test command to ensure the project starts without errors.
  - Builds and tests the Docker container.
  - Builds standalone executables for Linux and Windows using PyInstaller.

- On release, the workflow:
  - Uploads the built executables as release artifacts for both Linux and Windows.

C'est moi qui est tout pensé sur comment on allait agencer les jeux, le score board, les regles, la disposition des element, le titre, les couleurs

et je suis 100% daccord que t as fait le reseau
