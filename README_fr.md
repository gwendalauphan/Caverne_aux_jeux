# Caverne aux Jeux

### 👉 [🇬🇧 English version](README.md)

## Auteurs

* [Gwendal Auphan](https://github.com/gwendalauphan)
* [Dorian Gaspar](hhttps://github.com/dogasp)

Caverne aux Jeux est une plateforme de mini‑jeux que j'ai réalisée avec mon ami [Dorian Gaspar](https://github.com/dogasp). Elle dispose d'un mode serveur qui permet aux joueurs d'enregistrer leurs scores et de consulter les classements. À la base, il s'agissait du projet de fin d'année pour le bac, mais, poussés par la passion du code, nous avons porté le projet plus loin. Laissé à l'abandon pendant plusieurs années, j'ai décidé de le remettre au goût du jour et d'ajouter des fonctionnalités orientées développeur.

![Caverne aux Jeux - Intro](docs/assets/CaverneAuxJeux_0.png)

## Table des matières

- [Caverne aux Jeux](#caverne-aux-jeux)
    - [👉 🇬🇧 English version](#--english-version)
  - [Auteurs](#auteurs)
  - [Table des matières](#table-des-matières)
  - [Description](#description)
    - [Mini‑jeux présents](#minijeux-présents)
    - [Futurs jeux potentiels](#futurs-jeux-potentiels)
  - [Vidéo](#vidéo)
  - [Lancement du jeu](#lancement-du-jeu)
    - [Lancer avec Python](#lancer-avec-python)
    - [Lancer avec Docker](#lancer-avec-docker)
    - [Lancer via exécutables](#lancer-via-exécutables)
      - [Linux](#linux)
      - [Windows](#windows)
  - [Guide utilisateur](#guide-utilisateur)
  - [Guide du développeur](#guide-du-développeur)
  - [Comment contribuer au projet](#comment-contribuer-au-projet)
    - [Poetry](#poetry)
      - [Plugins](#plugins)
      - [Commandes utiles](#commandes-utiles)
  - [Notes techniques](#notes-techniques)
    - [CI/CD](#cicd)
  - [Documentation](#documentation)
  - [Troubleshooting](#troubleshooting)
  - [FAQ](#faq)


## Description

Le principe de l’application est de réunir plusieurs mini‑jeux, incluant un aspect compétitif. Chaque mini‑jeu a un mécanisme de scoring propre, et les scores sont enregistrés sur un serveur. L'application permet aux utilisateurs de jouer à ces jeux, de consulter leurs scores, et de voir les classements globaux.

La partie serveur est assez intéressante car elle n'est pas conventionnelle. À vrai dire, je dirais qu'elle n'est pas vraiment au niveau de l'application : il faut se remettre dans le contexte, nous n'étions que de jeunes débutants à l'époque. Ainsi, le serveur communique directement en sockets avec l'application et enregistre les données en dur dans des fichiers.

Le jeu a été créé en français, et il n'existe pas de version anglaise.

### Mini‑jeux présents

* Fantome
* Flappy Bird
* Minesweeper
* Pendu
* Pong
* Snake
* Tete Chercheuse
* Tetris

### Futurs jeux potentiels

* puissance 4
* pac man
* qui-est-ce ?
* space invaders
* morpion

---

## Vidéo

[![Caverne aux Jeux - Trailer](docs/assets/CaverneAuxJeux_1.png)](https://github.com/user-attachments/assets/0a5b37ea-5928-44da-a21e-fda9c0c20f7d)

---

## Lancement du jeu

Il y a plusieurs manières de lancer le jeu :

* via python
* via docker
* via un exécutable

Chaque manière de lancer le jeu a ses propres spécificités et peut nécessiter des configurations différentes.
Python est privilégié pour le développement et les tests, docker peut être utilisé pour créer des environnements isolés et reproductibles, tandis que l'exécutable permet de lancer le jeu sans dépendances externes.

### Lancer avec Python

Pour lancer le jeu avec python, il suffit de :

* créer un environnement virtuel
* installer les dépendances
* lancer le serveur et le client

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m app.main
python -m app.Reseau.server
```

### Lancer avec Docker

Pour docker, il suffit d'autoriser l'accès à l'affichage X11 et de lancer les conteneurs avec Docker Compose.

```bash
xhost +local:docker
cd docker
docker compose up
docker compose down
xhost -local:docker
```

### Lancer via exécutables

Enfin via les fichiers exécutables. Il suffit d'autoriser leur exécution (surtout sous Windows).

#### Linux

Utiliser le Makefile :

```bash
make run-linux
```

#### Windows

Penser à autoriser l'exécution des fichiers `.exe` et désactiver les règles de sécurité pour ces fichiers.
Puis cliquez sur les fichiers `.exe` pour les exécuter : `server.exe` puis `main.exe`.

---

## Guide utilisateur

*User Guide (lien)*

* Consulter **docs/user\_guide.md** (version Markdown).
* Une version PDF peut être générée (voir la section *Notes techniques*).

---

## Guide du développeur

Faire le guide du développeur

---

## Comment contribuer au projet

Ajouter un paquet aux requirements, tu dois d'abord l'ajouter via **Poetry** :

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

### Poetry

#### Plugins

* [https://pypi.org/project/poetry-plugin-export/](https://pypi.org/project/poetry-plugin-export/)

#### Commandes utiles

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

---

## Notes techniques

Le projet utilise :

* python, pyinstaller, tkinter, matplotlib, sockets, docker, poetry, github actions, makefile

Pour convertir la documentation en PDF :

```bash
docker run --rm -v "$(pwd)":/data -u $(id -u):$(id -g) pandoc/latex --output=docs/user_guide.pdf docs/user_guide.md
```

### CI/CD

This project uses GitHub Actions for continuous integration:

* On every push and pull request, the workflow:

  * Installs dependencies and runs a test command to ensure the project starts without errors.
  * Builds and tests the Docker container.
  * Builds standalone executables for Linux and Windows using PyInstaller.

* On release, the workflow:

  * Uploads the built executables as release artifacts for both Linux and Windows.

---

## Documentation

Vous pouvez trouver plus d'informations dans la documentation du projet, disponible dans le dossier `docs/`.

* [Rapport du projet](docs/Rapport_Caverne_aux_jeux.pdf)
* [Présentation du projet](docs/Prez_Caverne_aux_jeux.pdf)

---

## Troubleshooting

Sous Windows, faire bien attention à continuer malgré les avertissements de sécurité concernant l'exécution des fichiers `.exe`.

Penser à regarder la sécurité si le fichier `.exe` a disparu et est considéré comme un trojan.

---

## FAQ

Reste à faire
