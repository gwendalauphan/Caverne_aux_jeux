# Caverne aux Jeux

### 👉 [🇫🇷 Version française](README_fr.md)

## Authors

* [Gwendal Auphan](https://github.com/gwendalauphan)
* [Dorian Gaspar](https://github.com/dogasp)

**Games Cavern** is a mini-games platform I developed with my friend [Dorian Gaspar](https://github.com/dogasp).
It features a server mode that allows players to save their scores and view leaderboards.
Originally, it was our high-school final year project, but driven by our passion for coding, we took it further.
After being left aside for several years, I decided to modernize it and add developer-oriented features.

![Games Cavern - Intro](docs/assets/CaverneAuxJeux_0.png)

## Table of Contents

- [Caverne aux Jeux](#caverne-aux-jeux)
    - [👉 🇫🇷 Version française](#--version-française)
  - [Authors](#authors)
  - [Table of Contents](#table-of-contents)
  - [Description](#description)
    - [Available mini-games](#available-mini-games)
    - [Potential future games](#potential-future-games)
  - [Video](#video)
  - [Running the game](#running-the-game)
    - [Run with Python](#run-with-python)
    - [Run with Docker](#run-with-docker)
    - [Run via executables](#run-via-executables)
      - [Linux](#linux)
      - [Windows](#windows)
  - [User Guide](#user-guide)
  - [Developer Guide](#developer-guide)
  - [How to contribute](#how-to-contribute)
    - [Poetry](#poetry)
      - [Plugins](#plugins)
      - [Useful commands](#useful-commands)
  - [Technical Notes](#technical-notes)
    - [CI/CD](#cicd)
  - [Documentation](#documentation)
  - [Troubleshooting](#troubleshooting)
  - [FAQ](#faq)

---

## Description

The goal of the application is to gather several mini-games with a competitive aspect.
Each game has its own scoring system, and scores are saved on a server.
Players can enjoy the games, check their own scores, and view global leaderboards.

The server part is quite interesting because it’s unconventional — honestly, not at the same level as the application itself.
We have to remember: at the time, we were just beginners.
The server communicates directly via sockets with the client application and stores data in plain files.

The game was originally created in French and there is no English version.

### Available mini-games

* Ghost (Fantome)
* Flappy Bird
* Minesweeper
* Hangman (Pendu)
* Pong
* Snake
* Homing Head (Tête Chercheuse)
* Tetris

### Potential future games

* Connect Four (Puissance 4)
* Pac-Man
* Guess Who? (Qui-est-ce ?)
* Space Invaders
* Tic-Tac-Toe (Morpion)

---

## Video

[![Games Cavern - Trailer](docs/assets/CaverneAuxJeux_1.png)](https://github.com/user-attachments/assets/0a5b37ea-5928-44da-a21e-fda9c0c20f7d)

---

## Running the game

There are several ways to run the game:

* with Python
* with Docker
* with a standalone executable

Each method has its own specificities and may require different configurations.
Python is best for development and testing, Docker can be used to create isolated and reproducible environments, and the executable allows running the game without external dependencies.

### Run with Python

To run the game with Python:

* Create a virtual environment
* Install dependencies
* Launch both the server and the client

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m app.main
python -m app.Reseau.server
```

### Run with Docker

With Docker, simply allow X11 display access and run the containers with Docker Compose:

```bash
xhost +local:docker
cd docker
docker compose up
docker compose down
xhost -local:docker
```

### Run via executables

Finally, you can use the standalone executables.
Make sure to allow execution (especially on Windows).

#### Linux

Use the Makefile:

```bash
make run-linux
```

#### Windows

Allow execution of `.exe` files and disable security rules blocking them.
Then run them by double-clicking: first `server.exe`, then `main.exe`.

---

## User Guide

*User Guide (link)*

* See **docs/user\_guide.md** (Markdown version).
* A PDF version can be generated (see *Technical Notes* section).

---

## Developer Guide

To be done.

---

## How to contribute

When adding a package to the requirements, first add it using **Poetry**:

```bash
cd backend
poetry add <package_name>
# or for test dependencies
poetry add --dev <package_name>
```

Then export dependencies:

```bash
poetry export -f requirements.txt --output requirements.txt --without-hashes
# or for tests
poetry export -f requirements.txt --output tests/requirements.txt --without-hashes --all-groups
```

### Poetry

#### Plugins

* [https://pypi.org/project/poetry-plugin-export/](https://pypi.org/project/poetry-plugin-export/)

#### Useful commands

Run these before committing changes or contributing to the project:

```bash
cd backend

# Install all packages listed in pyproject.toml
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

## Technical Notes

The project uses:

* Python, PyInstaller, Tkinter, Matplotlib, Sockets, Docker, Poetry, GitHub Actions, Makefile.

To convert documentation to PDF:

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

You can find more information in the project’s documentation, available in the `docs/` folder:

* [Project Report](docs/Rapport_Caverne_aux_jeux.pdf)
* [Project Presentation](docs/Prez_Caverne_aux_jeux.pdf)

---

## Troubleshooting

On Windows, make sure to proceed despite security warnings when running `.exe` files.
If an `.exe` file disappears and is flagged as a trojan, check your security settings.

---

## FAQ

To be done.

---

If you’d like, I can now also **proofread and adapt this English version so it sounds fully native and polished for GitHub**. That would make it read more smoothly and feel professional. Would you like me to do that next?
