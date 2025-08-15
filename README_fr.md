# Caverne aux Jeux

### 👉 [🇬🇧 English version](README.md)

---

0.0 Auteurs
0. Introduction / Description
1. Video
2. Table des matières
3. Lancement du jeu
4. User Guide (lien)
5. Developer Guide
6. Comment contribuer au projet
7. Notes techniques
8. Documentation
9. Troubleshooting
10. FAQ

Introduction
Caverne aux Jeux est une plateforme de mini-jeux que j'ai réalisé avec mon ami [Dorian Gaspar](https://github.com/DorianGaspar). Elle dispose d'un mode serveur qui permet aux joueurs d'enregistrer leurs scores et de consulter les classements. A la base, il s'agissait du projet de fin d'année pour le bac, mais poussé par la passion du code, nous avons poussé le projet plus loin. Laissé à l'abandon pedant plusieurs années, j'ai décidé de le remettre au goût du jour ainsi que d'ajouter des fonctionnalités orienté développeur.

Description
Le principe de l’application est de réunir plusieurs mini-jeux, incluant un aspect compétitif. Chaque mini jeu a un mécanisme de scoring propre, et les scores sont enregistrés sur un serveur. L'application permet aux utilisateurs de jouer à ces jeux, de consulter leurs scores, et de voir les classements globaux. La partie serveur est assez intéressante car elle n'est pas du tout conventionnelle. A vrai, je dirais qu'elle n'est pas vraiment au niveau de l'application, il faut se mettre dans le contexte que nous n'étions que de jeunes débutants à l'époque. Ainsi le serveur communique directement en sockets avec l'application et enregistre les données en dur dans des fichiers.
Le jeu a été créé en Francais, et il n'existe pas de version anglaise.

Mini jeux présents :

- Fantome
- Flappy Bird
- Minesweeper
- Pendu
- Pong
- Snake
- Tete Chercheuse
- Tetris

Futur jeux potentiels:
- puissance 4
- pac man
- qui-est-ce ?
- space invaders
- morpion

Video
[!Caverne aux Jeux - Trailer](https://github.com/user-attachments/assets/0a5b37ea-5928-44da-a21e-fda9c0c20f7d)

Lancement du jeu
Il y a plusieurs manières de lancer le jeu :
- via python
- via docker
- via un exécutable

Chaque manière de lancer le jeu a ses propres spécificités et peut nécessiter des configurations différentes.
Python est privilégié pour le développement et les tests, docker peut être utilisé pour créer des environnements isolés et reproductibles, tandis que l'exécutable permet de lancer le jeu sans dépendances externes.

Pour lancer le jeu avec python, il suffit de:
- créer un environnement virtuel
- installer les dépendances
- lancer le serveur et le client

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m app.main
python -m app.Reseau.server
```
Pour docker, il suffit d'autoriser l'accès à l'affichage X11 et de lancer les conteneurs avec Docker Compose.
```bash
xhost +local:docker
cd docker
docker compose up
docker compose down
xhost -local:docker
```

Enfin via les fichiers exécutables. Il suffit d'autoriser leur exécution (surtout sous windows).
Sous linux, utiliser le makefile:
```bash
make run-linux
```
Sous windows, penser à autoriser l'exécution des fichiers .exe et désactiver les règles de sécurité pour ces fichiers.
Puis cliquez sur les fichiers .exe pour les exécuter, server.exe puis main.exe.

Guide du développeur
Faire le guide du développeur

### Comment contribuer au projet

Ajouter un paquet aux requirements, tu dois d'abord l'ajouter via Poetry :

```bash
cd backend
poetry add <package_name>
# ou pour les tests
poetry add --dev <package_name>
```

Puis, pour exporter les dépendances :

```bash
poetry export -f requirements.txt --output requirements.txt --without-hashes
# ou pour les tests
poetry export -f requirements.txt --output tests/requirements.txt --without-hashes --all-groups
```

---

## Poetry

### Plugins

* [https://pypi.org/project/poetry-plugin-export/](https://pypi.org/project/poetry-plugin-export/)

### Commandes utiles

Commandes à lancer avant de committer des modifications ou de contribuer au projet :

```bash
cd backend

# Installer tous les paquets listés dans pyproject.toml
poetry install

poetry run black .
poetry run flake8 .
poetry run pylint .
poetry run mypy .
poetry run pytest tests/

poetry export -f requirements.txt --output requirements.txt --without-hashes
poetry export -f requirements.txt --output build_requirements.txt --only build --without-hashes
poetry export -f requirements.txt --output test_requirements.txt --only test --without-hashes

```


Notes techniques
Le projet utilise:
python, pyinstaller, tkinter, matplotlib, sockets, docker, poetry, github actions, makefile

Pour convertir la documentation en PDF:
```bash
docker run --rm -v "$(pwd)":/data -u $(id -u):$(id -g) pandoc/latex --output=docs/user_guide.pdf docs/user_guide.md
```

## CI/CD

This project uses GitHub Actions for continuous integration:

- On every push and pull request, the workflow:
  - Installs dependencies and runs a test command to ensure the project starts without errors.
  - Builds and tests the Docker container.
  - Builds standalone executables for Linux and Windows using PyInstaller.

- On release, the workflow:
  - Uploads the built executables as release artifacts for both Linux and Windows.

Documentation
Vous pouvez trouver plus d'informations dans la documentation du projet, disponible dans le dossier `docs/`.
- [Rapport du projet](docs/Rapport_Caverne_aux_jeux.pdf)
- [Présentation du projet](docs/Prez_Caverne_aux_jeux.pdf)

Troubleshooting
Sous windows, faire bien attention à continuer malgré les avertissements de sécurité concernant l'exécution des fichiers .exe.
Penser à regarder la sécurité si le fichier exe a disparu et est considéré comme un trojan.

FAQ
