# Guide du Développeur – Caverne aux Jeux

**Auteurs** :

* *Gwendal Auphan*
* *Dorian Gaspar*

---

# Table des matières

- [Guide du Développeur – Caverne aux Jeux](#guide-du-développeur--caverne-aux-jeux)
- [Table des matières](#table-des-matières)
- [Introduction](#introduction)
- [Cloner et contribuer](#cloner-et-contribuer)
  - [Contribuer au projet](#contribuer-au-projet)
- [Architecture technique](#architecture-technique)
  - [Technologies principales](#technologies-principales)
- [Prérequis et installation](#prérequis-et-installation)
  - [Poetry](#poetry)
  - [Plugin recommandé](#plugin-recommandé)
  - [Installation des dépendances](#installation-des-dépendances)
- [Développement et contribution](#développement-et-contribution)
  - [Commandes utiles](#commandes-utiles)
- [Compilation et exécution](#compilation-et-exécution)
  - [Makefile](#makefile)
  - [Docker Compose](#docker-compose)
  - [Exécution en Python](#exécution-en-python)
- [CI/CD](#cicd)
  - [Sur chaque push et pull request](#sur-chaque-push-et-pull-request)
  - [Sur chaque release](#sur-chaque-release)
- [Documentation](#documentation)
- [Ressources supplémentaires](#ressources-supplémentaires)
- [Licence](#licence)

---

# Introduction

Ce document est destiné aux développeurs qui souhaitent contribuer au projet **Caverne aux Jeux**.
Il présente l’architecture technique, les technologies utilisées, ainsi que les pratiques de développement (build, tests, CI/CD).

---

# Cloner et contribuer

Pour récupérer le projet localement :

```bash
git clone https://github.com/gwendalauphan/Caverne_aux_jeux.git
cd Caverne_aux_jeux
```

## Contribuer au projet

Vous pouvez contribuer de plusieurs manières :

* **Forker** le dépôt GitHub, développer vos modifications, puis proposer une **Pull Request**.
* Ouvrir une **issue** si vous souhaitez signaler un bug, suggérer une amélioration ou poser une question.

Toutes les contributions (code, documentation, tests, idées) sont les bienvenues.

---

# Architecture technique

Le projet repose sur une architecture simple :

* **Client (`client.exe`)** : interface graphique permettant à l’utilisateur de se connecter avec un simple *username* et de jouer aux différents jeux.
* **Serveur (`server.exe`)** : application qui centralise et stocke les données de jeu de plusieurs utilisateurs via des **sockets TCP**.

## Technologies principales

* **Python 3**
* **Tkinter** (UI)
* **Matplotlib** (graphiques et scores)
* **Sockets** (communication réseau)
* **Docker & Docker Compose** (environnement reproductible)
* **PyInstaller** (génération d’exécutables Windows/Linux)
* **Poetry** (gestion des dépendances)
* **Makefile** (build et automatisation)
* **GitHub Actions** (CI/CD)

---

# Prérequis et installation

> **Note :** Sous **Linux** et **macOS**, la procédure d'installation et de lancement est identique. Sous macOS, utilisez Homebrew pour installer les dépendances système.

## Poetry

Le projet utilise **Poetry** pour gérer les dépendances et la configuration du packaging.

## Plugin recommandé

* [poetry-plugin-export](https://pypi.org/project/poetry-plugin-export/)

## Installation des dépendances

Sous Linux **et macOS** :

```bash
sudo apt update
sudo apt install python3 python3-tk make
# macOS : brew install python3 tk make
```
Pour le lancement avec Docker, assurez-vous que Docker et Docker Compose sont installés et configurés correctement.

Vérifiez que `python3-tk` est installable :

```bash
apt-cache policy python3-tk
```

Ensuite, installez les dépendances du projet :

```bash
cd Caverne_aux_jeux
poetry install
```

---

# Développement et contribution

## Commandes utiles

Avant de contribuer ou de committer des modifications :

```bash
cd Caverne_aux_jeux

# Export des dépendances
poetry export -f requirements.txt --output requirements.txt --without-hashes
poetry export -f requirements.txt --output build_requirements.txt --only build --without-hashes
poetry export -f requirements.txt --output test_requirements.txt --only test --without-hashes

# Formatage et vérifications
poetry run black .
poetry run flake8 .
poetry run pylint .
poetry run mypy .

# Tests unitaires
poetry run pytest tests/
```

---

# Compilation et exécution

> **Note :** Sous **Linux** et **macOS**, les commandes de compilation et d'exécution sont identiques.

## Makefile

Les cibles principales sont :

```bash
make help
# -->
Available targets:
  build-linux          Build Linux executables with PyInstaller
  build-linux-debug    Build Linux executables with PyInstaller (debug mode)
  build-windows        Build Windows executables with PyInstaller
  build-windows-debug  Build Windows executables with PyInstaller (debug mode)
  run-linux            Run Linux server+client
  run-windows          Run Windows server+client
  clean                Remove build artifacts
```

Exemple pour Linux :

```bash
make build-linux
make run-linux
```

## Docker Compose

```bash
xhost +local:docker    # Autoriser l’accès X11
cd docker
docker compose up -d
xhost -local:docker    # Retirer l’accès X11
```

## Exécution en Python

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Lancer le serveur
python -m app.Reseau.server

# Lancer le client
python -m app.main
```

---

# CI/CD

Le projet utilise **GitHub Actions** pour automatiser les builds et tests :

## Sur chaque push et pull request

* Installation des dépendances
* Lancement des tests (unitaires + linting)
* Build et test du conteneur Docker
* Build des exécutables Linux et Windows

## Sur chaque release

* Upload automatique des exécutables Linux et Windows dans les **artifacts de release**.

---

# Documentation

La documentation est disponible dans le dossier `docs/` :

  * [Rapport](https://github.com/gwendalauphan/Caverne_aux_jeux/blob/main/docs/Rapport_Caverne_aux_jeux.pdf)
  * [Présentation](https://github.com/gwendalauphan/Caverne_aux_jeux/blob/main/docs/Prez_Caverne_aux_jeux.pdf)
  * [Guide de l'utilisateur](https://github.com/gwendalauphan/Caverne_aux_jeux/blob/main/docs/user_guide_fr.md)
  * [Changelog](https://github.com/gwendalauphan/Caverne_aux_jeux/blob/main/docs/Changelog.md)

Pour **convertir** la documentation Markdown en PDF :

```bash
docker run --rm -v "$(pwd)":/data \
-w /data/docs   -u $(id -u):$(id -g) \
fpod/pandoc-weasyprint   --from=markdown   --to=html5 \
--pdf-engine=weasyprint   --metadata author="Gwendal Auphan" \
--metadata lang=fr-FR   -c style.css   -o user_guide.pdf user_guide.md
```

---

# Ressources supplémentaires

* Dépôt officiel : [Caverne aux Jeux](https://github.com/gwendalauphan/Caverne_aux_jeux)
* Documentation Python : [https://docs.python.org/3/](https://docs.python.org/3/)
* Poetry : [https://python-poetry.org/](https://python-poetry.org/)
* PyInstaller : [https://pyinstaller.org/](https://pyinstaller.org/)
* Tkinter : [https://docs.python.org/3/library/tkinter.html](https://docs.python.org/3/library/tkinter.html)

# Licence
Ce projet est sous licence Creative Commons Attribution - Pas d’Utilisation Commerciale 4.0 International (CC BY-NC 4.0).

© 2025 Auphan Gwendal & Dorian Gaspar.
Vous devez mentionner les auteurs originaux lors de l’utilisation ou du partage de ce projet.
L’utilisation commerciale est interdite sauf autorisation expresse des auteurs.
