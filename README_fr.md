# Caverne aux Jeux

### 👉 [🇬🇧 English version](README.md)

---

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
poetry export -f requirements.txt --output tests/requirements.txt --without-hashes --all-groups
```

Répertoire avec le projet d'ISN de fin d'année

plein de mini-jeux
-> morpion, snake, puissance 4, pac man, tetris, robot tete chercheuse, qui-est-ce?, space invaders,
pendu, pong, demineur, phantôme

docker run --rm -v "$(pwd)":/data -u $(id -u):$(id -g) pandoc/latex --output=docs/user_guide.pdf docs/user_guide.md

## CI/CD

This project uses GitHub Actions for continuous integration:

- On every push and pull request, the workflow:
  - Installs dependencies and runs a test command to ensure the project starts without errors.
  - Builds and tests the Docker container.
  - Builds standalone executables for Linux and Windows using PyInstaller.

- On release, the workflow:
  - Uploads the built executables as release artifacts for both Linux and Windows.

