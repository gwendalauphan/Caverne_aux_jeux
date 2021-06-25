from os import listdir
from os.path import isfile, join, isdir
root_path = "./"
root = listdir(root_path)

total = 0
def counter(fichiers, path):
    global total
    for file in fichiers:
        lignes = 0
        if isfile(join(path, file)):
            if file.split(".")[1] == "py" and file != "compteur de lignes.py":
                with open(join(path,file), "r") as fichier:
                    temp = fichier.readlines()
                    for i in temp:
                        lignes += 1
                    print(file,  lignes)
                    total += lignes
                    lignes = 0
        elif isdir(join(path, file)) and file != ".git":
            temp = join(path, file)
            counter(listdir(temp), temp)
counter(root, root_path)
print("total de lignes = ", total)
input()
