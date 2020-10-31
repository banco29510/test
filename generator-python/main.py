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
        #conn.execute('''CREATE TABLE score (id text, name text, url text)''')
        conn.commit()
    else:
        conn = sqlite3.connect('database.db')




    conn.close()

    print("Géneration des pages")


    dir = str(os.path.dirname(__file__)+"/score/")


    if os.path.isdir(dir):
        shutil.rmtree(dir, onerror=remove_readonly) # supprime le dossier

    repo = git.Repo.clone_from("https://github.com/banco29510/score_test.git", dir)

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
            for (_path, _stage), entry in repo.index.entries.items():
                print(_path)

                file_contents = repo.git.show('{}:{}'.format(fifty_first_commits[0],
                                                             entry.path))  # recupere le contenu du fichier

                if _path == "README.md":
                    file = open("filename.md", "w+")
                    file.write("---\r\n")
                    file.write("title: \"My First Post\"\r\n")
                    file.write("date: 2020-10-28T08:44:03+01:00\r\n")
                    file.write("draft: true\r\n")
                    file.write("---\r\n")

                    file.write(file_contents + "\r\n") # ajoute le contenu dans le fichier

                    file.close()


    print("génération du site")

    os.chdir(str(os.path.dirname(__file__)+"/.."))
    os.system("hugo -D")


if __name__ == "__main__":
    main()

