#!/usr/bin/env python3
import re, os, shutil, math, pathlib, stat, cmd, time,sys
import sqlite3
import git


def main ():

    print("Début de la génération")

    print("Vérification de la base de données des partitions")

    database = str(os.path.dirname(__file__) + "/database.db")
    if not os.path.isfile(database):
        conn = sqlite3.connect('database.db')
        conn.execute('''CREATE TABLE score (id INTEGER PRIMARY KEY, name text, url text)''')
        conn.commit()
    else:
        conn = sqlite3.connect('database.db')

    # recuperer l'ensemble des dépots
    depots = []
    for row in conn.execute('''SELECT * FROM score '''):
        print(row)
        depots.append(row)

    conn.close()

    print("Géneration des pages")

    for depot in depots:
        print(depot[1])
        dir = str(os.path.dirname(__file__) + "/" +depot[1]+"/")

        if os.path.isdir(dir):
            shutil.rmtree(dir, ignore_errors=True)  # supprime le dossier

        repo = git.Repo.clone_from(depot[2], dir)

        remote_refs = repo.remote().refs

        # liste des branches du dépot
        for ref in remote_refs:
            if ref.name == """origin/master""":
                repo.git.checkout(ref.name)  # changer de branche sur master

                print("liste des commits :")
                fifty_first_commits = list(repo.iter_commits(ref.name, max_count=10))
                print(fifty_first_commits[0])
                repo.commit(fifty_first_commits[0]) # choisit le dernier commit

                # liste des fichiers dans le commit
                files = []
                for (_path, _stage), entry in repo.index.entries.items():
                    files.append(_path)
                    print(_path)
                print(files)

                file_contents = repo.git.show('{}:{}'.format(fifty_first_commits[0],
                                                             entry.path))  # recupere le contenu du fichier

                if _path == "README.md":
                    file = open(str(os.path.dirname(__file__)+"/../content/posts/"+str(depot[1])+".md"), "w+")
                    file.write("---\r\n")
                    file.write("title: \""+str(depot[1])+"\"\r\n")
                    file.write("date: 2020-10-28T08:44:03+01:00\r\n")
                    file.write("draft: true\r\n")
                    file.write("---\r\n")

                    file.write(file_contents + "\r\n") # ajoute le contenu dans le fichier

                    file.close()

        print("supp du dossier qui ne fonctionne pas: " + dir)
        shutil.rmtree(dir, ignore_errors=True)  # supprime le dossier



    print("génération du site")

    os.chdir(str(os.path.dirname(__file__)+"/.."))
    os.system("hugo -D")


if __name__ == "__main__":
    main()

