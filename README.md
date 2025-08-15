# Caverne aux Jeux

### 👉 [🇫🇷 Version française](README_fr.md)

Video
[![Caverne aux Jeux - Trailer](docs/CaverneAuxJeux.png)](https://github.com/user-attachments/assets/0a5b37ea-5928-44da-a21e-fda9c0c20f7d)

Video
[![Caverne aux Jeux - Trailer](docs/CaverneAuxJeux.png)](docs/CaverneAuxJeux.mp4)


docker run --rm -v "$(pwd)":/data -u $(id -u):$(id -g) pandoc/latex --output=docs/user_guide.pdf docs/user_guide.md

## CI/CD

This project uses GitHub Actions for continuous integration:

- On every push and pull request, the workflow:
  - Installs dependencies and runs a test command to ensure the project starts without errors.
  - Builds and tests the Docker container.
  - Builds standalone executables for Linux and Windows using PyInstaller.

- On release, the workflow:
  - Uploads the built executables as release artifacts for both Linux and Windows.

