# Caverne aux Jeux

[![License](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey?style=for-the-badge)](https://creativecommons.org/licenses/by-nc/4.0/) [![GitHub stars](https://img.shields.io/github/stars/gwendalauphan/Caverne_aux_jeux?style=for-the-badge)](https://github.com/gwendalauphan/Caverne_aux_jeux/stargazers) [![GitHub release](https://img.shields.io/github/v/release/gwendalauphan/Caverne_aux_jeux?style=for-the-badge)](https://github.com/gwendalAuphan/game-platform/releases) [![GitHub last commit](https://img.shields.io/github/last-commit/gwendalauphan/Caverne_aux_jeux?style=for-the-badge)](https://github.com/gwendalauphan/Caverne_aux_jeux/commits/main)



### 👉 [🇫🇷 Version française](README_fr.md)

## Authors

* [Gwendal Auphan](https://github.com/gwendalauphan)
* [Dorian Gaspar](https://github.com/dogasp)

**Caverne aux Jeux** is a mini-games platform that I built together with my friend [Dorian Gaspar](https://github.com/dogasp).
It includes a server mode that allows players to save their scores and check leaderboards.
Originally, this was our **final high school project**, but driven by our passion for coding, we decided to push it further.
After being abandoned for several years, I decided to modernize it and add some developer-oriented features.

![Caverne aux Jeux - Intro](docs/assets/CaverneAuxJeux_0.png)

## Table of Contents

- [Caverne aux Jeux](#caverne-aux-jeux)
    - [👉 🇫🇷 Version française](#--version-française)
  - [Authors](#authors)
  - [Table of Contents](#table-of-contents)
  - [Description](#description)
    - [Available mini-games](#available-mini-games)
    - [Potential future games](#potential-future-games)
  - [Video](#video)
- [🚀 Quick Start – Caverne aux Jeux](#-quick-start--caverne-aux-jeux)
  - [1. Download the game](#1-download-the-game)
  - [2. Run the game](#2-run-the-game)
    - [Simple mode (client only)](#simple-mode-client-only)
    - [Client-server mode (multiplayer and score saving)](#client-server-mode-multiplayer-and-score-saving)
  - [3. Advanced method (developers)](#3-advanced-method-developers)
    - [Clone the repository](#clone-the-repository)
    - [Run with Python](#run-with-python)
    - [Build with Makefile](#build-with-makefile)
    - [Docker Compose](#docker-compose)
  - [4. Dependencies](#4-dependencies)
- [👩‍💻 Developer Guide](#-developer-guide)
  - [Clone and contribute](#clone-and-contribute)
  - [Requirements](#requirements)
  - [CI/CD](#cicd)
  - [Documentation](#documentation)
- [License](#license)


## Description

The idea behind the app is to bring together several mini-games, with a **competitive twist**.
Each mini-game has its own scoring system, and scores are stored on a server.
Users can play, view their own scores, and check the global leaderboards.

The server side is quite interesting, though not very conventional. To be honest, it’s not really at the same level as the client app — but keep in mind we were just beginners at the time.
The server communicates directly via sockets with the client and saves data in plain files.

The game was originally created in **French only**, and there is no English in-game translation.

### Available mini-games

* Fantome
* Flappy Bird
* Minesweeper
* Hangman
* Pong
* Snake
* Seeker Head
* Tetris

### Potential future games

* Connect Four
* Pac-Man
* Guess Who?
* Space Invaders
* Tic-Tac-Toe

---

## Video

[![Caverne aux Jeux - Trailer](docs/assets/CaverneAuxJeux_1.png)](https://github.com/user-attachments/assets/0a5b37ea-5928-44da-a21e-fda9c0c20f7d)

---

# 🚀 Quick Start – Caverne aux Jeux

## 1. Download the game

The easiest way to install the game is to download a **release**:
👉 [Caverne aux Jeux Releases](https://github.com/gwendalauphan/Caverne_aux_jeux/releases)

Choose the version for your operating system:

* **Windows**
* **Linux**
* **macOS** (use the Linux binary, launching is the same as Linux)

After downloading, you will have two executables:

* `client.exe` → the game
* `server.exe` → the server (optional)

---

## 2. Run the game

> **Note :** Under **Linux** and **macOS**, the launch procedure is identical. The commands to run the game are the same.

### Simple mode (client only)

```bash
./client # (under Linux and macOS)
./client.exe # (under Windows)
```

* Enter a **username**.
* Select a game and start playing.

### Client-server mode (multiplayer and score saving)

1. Start the server:

   ```bash
   ./server # (under Linux and macOS)
   ./server.exe # (under Windows)
   ```
2. Then start the client:

   ```bash
   ./client # (under Linux and macOS)
   ./client.exe # (under Windows)
   ```

* Game data will then be stored server-side.

---

## 3. Advanced method (developers)

> **Note :** Under **Linux** and **macOS**, the launch procedure is identical. The commands to run the game are the same.
>
### Clone the repository

```bash
git clone https://github.com/gwendalauphan/Caverne_aux_jeux.git
cd Caverne_aux_jeux
```

### Run with Python

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m app.Reseau.server   # server
python -m app.main            # client
```

### Build with Makefile

```bash
make build-linux
make run-linux
```

### Docker Compose

```bash
xhost +local:docker
cd docker
docker compose up -d
xhost -local:docker
```

---

## 4. Dependencies

> **Note :** Under **macOS**, you can use Homebrew to install the necessary packages. (`brew install python3-tk make`).
> T
```bash
sudo apt update
sudo apt install python3 python3-tk make
```
For launching with Docker, ensure that Docker and Docker Compose are installed and configured correctly.

👉 For more details, check the [User Guide](./docs/user_guide.md).

---

# 👩‍💻 Developer Guide

## Clone and contribute

```bash
git clone https://github.com/gwendalauphan/Caverne_aux_jeux.git
cd Caverne_aux_jeux
```

You can contribute by:

* **Forking** the repository and opening a **Pull Request**.
* **Reporting bugs or ideas** via **issues**.

---

## Requirements

Development requires:

* **Python 3** and **tkinter**
* **make**, **docker**, **docker compose**
* **Poetry** (dependency management)

Install dependencies:

```bash
poetry install
```

Useful commands before committing:

```bash
poetry run black .     # formatting
poetry run flake8 .    # linting
poetry run pylint .    # static analysis
poetry run mypy .      # type checking
poetry run pytest tests/  # unit tests
```

Export dependencies:

```bash
poetry export -f requirements.txt --output requirements.txt --without-hashes
poetry export -f requirements.txt --output build_requirements.txt --only build --without-hashes
poetry export -f requirements.txt --output test_requirements.txt --only test --without-hashes
```

---

## CI/CD

The project uses **GitHub Actions** for code quality:

* **On each push/pull request**: dependency installation, linting, tests, Docker build, Linux/Windows executables build.
* **On each release**: automatic publishing of Linux and Windows executables as artifacts.

---

## Documentation

Full documentation is available in the `docs/` folder:

* [User Guide](docs/user_guide.md)
* [Developer Guide](docs/developer_guide.md)
* [Project Report](docs/Rapport_Caverne_aux_jeux.pdf)
* [Project Presentation](docs/Prez_Caverne_aux_jeux.pdf)
* [Changelog](docs/Changelog.md)

To **convert** Markdown documentation to PDF:

```bash
docker run --rm -v "$(pwd)":/data -u $(id -u):$(id -g) \
fpod/pandoc-weasyprint   --from=markdown   --to=html5 \
--resource-path=.:docs --pdf-engine=weasyprint   --metadata author="Gwendal Auphan" \
--metadata lang=fr-FR   -c style.css   -o user_guide.pdf user_guide.md
```

---

👉 Full guide: [Developer Guide](./docs/developer_guide.md)

# License
This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0).

© 2025 Auphan Gwendal & Dorian Gaspar.
You must provide attribution to the original authors when using or sharing this project.
Commercial use is prohibited unless explicit permission is obtained.

