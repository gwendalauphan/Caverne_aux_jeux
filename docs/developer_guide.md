# Developer Guide – Caverne aux Jeux

**Authors**:

* *Gwendal Auphan*
* *Dorian Gaspar*

---

# Table of Contents

- [Developer Guide – Caverne aux Jeux](#developer-guide--caverne-aux-jeux)
- [Table of Contents](#table-of-contents)
- [Introduction](#introduction)
- [Clone and Contribute](#clone-and-contribute)
  - [Contribute to the Project](#contribute-to-the-project)
- [Technical Architecture](#technical-architecture)
  - [Main Technologies](#main-technologies)
- [Requirements and Installation](#requirements-and-installation)
  - [Poetry](#poetry)
  - [Recommended Plugin](#recommended-plugin)
  - [Installing Dependencies](#installing-dependencies)
- [Development and Contribution](#development-and-contribution)
  - [Useful Commands](#useful-commands)
- [Build and Execution](#build-and-execution)
  - [Makefile](#makefile)
  - [Docker Compose](#docker-compose)
  - [Running with Python](#running-with-python)
- [CI/CD](#cicd)
  - [On each push and pull request](#on-each-push-and-pull-request)
  - [On each release](#on-each-release)
- [Documentation](#documentation)
- [Additional Resources](#additional-resources)

---

# Introduction

This document is intended for developers who want to contribute to the **Caverne aux Jeux** project.
It describes the technical architecture, the technologies used, as well as the development practices (build, tests, CI/CD).

---

# Clone and Contribute

To clone the project locally:

```bash
git clone https://github.com/gwendalauphan/Caverne_aux_jeux.git
cd Caverne_aux_jeux
```

## Contribute to the Project

You can contribute in several ways:

* **Fork** the GitHub repository, develop your changes, and submit a **Pull Request**.
* Open an **issue** if you want to report a bug, suggest an improvement, or ask a question.

All contributions (code, documentation, tests, ideas) are welcome.

---

# Technical Architecture

The project is based on a simple architecture:

* **Client (`client.exe`)**: graphical interface allowing the user to log in with a simple *username* and play the available games.
* **Server (`server.exe`)**: application that centralizes and stores game data for multiple users via **TCP sockets**.

## Main Technologies

* **Python 3**
* **Tkinter** (UI)
* **Matplotlib** (charts and scores)
* **Sockets** (network communication)
* **Docker & Docker Compose** (reproducible environment)
* **PyInstaller** (build Windows/Linux executables)
* **Poetry** (dependency management)
* **Makefile** (build and automation)
* **GitHub Actions** (CI/CD)

---

# Requirements and Installation

> **Note :** Under **Linux** and **macOS**, the installation procedure is identical. Under macOS, you can use Homebrew to install the necessary packages.

## Poetry

The project uses **Poetry** to manage dependencies and packaging configuration.

## Recommended Plugin

* [poetry-plugin-export](https://pypi.org/project/poetry-plugin-export/)

## Installing Dependencies

On Linux and macOS:

```bash
sudo apt update
sudo apt install python3 python3-tk make docker.io docker-compose
# macOS : brew install python3 tk make
```
For launching with Docker, ensure that Docker and Docker Compose are installed and configured correctly.


Check if `python3-tk` is installable:

```bash
apt-cache policy python3-tk
```

Then install project dependencies:

```bash
cd Caverne_aux_jeux
poetry install
```

---

# Development and Contribution

## Useful Commands

Before contributing or committing changes:

```bash
cd Caverne_aux_jeux

# Export dependencies
poetry export -f requirements.txt --output requirements.txt --without-hashes
poetry export -f requirements.txt --output build_requirements.txt --only build --without-hashes
poetry export -f requirements.txt --output test_requirements.txt --only test --without-hashes

# Formatting and checks
poetry run black .
poetry run flake8 .
poetry run pylint .
poetry run mypy .

# Unit tests
poetry run pytest tests/
```

---

# Build and Execution

> **Note :** Under **Linux** and **macOS**, the build and execution commands are identical.

## Makefile

Main targets are:

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

Example for Linux:

```bash
make build-linux
make run-linux
```

## Docker Compose

```bash
xhost +local:docker    # Allow X11 access
cd docker
docker compose up -d
xhost -local:docker    # Revoke X11 access
```

## Running with Python

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Start the server
python -m app.Reseau.server

# Start the client
python -m app.main
```

---

# CI/CD

The project uses **GitHub Actions** to automate builds and tests:

## On each push and pull request

* Install dependencies
* Run tests (unit + linting)
* Build and test the Docker container
* Build Linux and Windows executables

## On each release

* Automatically upload Linux and Windows executables as **release artifacts**

---

# Documentation

Documentation is available in the `docs/` folder:

* [Report](https://github.com/gwendalauphan/Caverne_aux_jeux/blob/main/docs/Rapport_Caverne_aux_jeux.pdf)
* [Presentation](https://github.com/gwendalauphan/Caverne_aux_jeux/blob/main/docs/Prez_Caverne_aux_jeux.pdf)
* [User Guide](https://github.com/gwendalauphan/Caverne_aux_jeux/blob/main/docs/user_guide.md)
* [Changelog](https://github.com/gwendalauphan/Caverne_aux_jeux/blob/main/docs/Changelog.md)

To **convert** Markdown documentation to PDF:

```bash
docker run --rm -v "$(pwd)":/data \
-w /data/docs   -u $(id -u):$(id -g) \
fpod/pandoc-weasyprint   --from=markdown   --to=html5 \
--pdf-engine=weasyprint   --metadata author="Gwendal Auphan" \
--metadata lang=fr-FR   -c style.css   -o user_guide.pdf user_guide.md
```

---

# Additional Resources

* Official repository: [Caverne aux Jeux](https://github.com/gwendalauphan/Caverne_aux_jeux)
* Python Docs: [https://docs.python.org/3/](https://docs.python.org/3/)
* Poetry: [https://python-poetry.org/](https://python-poetry.org/)
* PyInstaller: [https://pyinstaller.org/](https://pyinstaller.org/)
* Tkinter: [https://docs.python.org/3/library/tkinter.html](https://docs.python.org/3/library/tkinter.html)
