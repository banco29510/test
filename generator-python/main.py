import re, os, shutil, math, pathlib, stat, cmd
import sqlite3
import git

# function pour la suppression du dossier
def remove_readonly(func, path, _):
    "Clear the readonly bit and reattempt the removal"
    os.chmod(path, stat.S_IWRITE)
    func(path)

def main ():

    print("Début de la génération")

    print("Vérification de la base de données des partitions")
    database = str(os.path.dirname(__file__) + "/database.db")
    if os.path.isfile(database):
        conn = sqlite3.connect('database.db')
        # Create table
        conn.execute('''CREATE TABLE score (id text, name text, url text)''')
        conn.commit()
    else:
        conn = sqlite3.connect('database.db')




    conn.close()

    print("Géneration des pages")


    dir = str(os.path.dirname(__file__)+"/score/")
    print(dir)


    if os.path.isdir(dir):
        shutil.rmtree(dir, onerror=remove_readonly) # supprime le dossier


    git.Repo.clone_from("https://github.com/banco29510/score_test.git", dir)

    file = open("filename.md", "w+")
    file.write("---\r\n")
    file.write("title: \"My First Post\"\r\n")
    file.write("date: 2020-10-28T08:44:03+01:00\r\n")
    file.write("draft: true\r\n")
    file.write("---\r\n")
    file.write("README.md\r\n")
    file.close()

    print("génération du site")
    os.system("hugo -D")


if __name__ == "__main__":
    main()

