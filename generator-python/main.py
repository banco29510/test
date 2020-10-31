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
    #print(dir)


    if os.path.isdir(dir):
        shutil.rmtree(dir, onerror=remove_readonly) # supprime le dossier

    repo = git.Repo.clone_from("https://github.com/banco29510/score_test.git", dir)

    remote_refs = repo.remote().refs

    # liste des branches du dépot
    for ref in remote_refs:
        if ref.name == """origin/master""":
            repo.git.checkout(ref.name)  # changer de branche sur main

            print("liste des commits :")
            fifty_first_commits = list(repo.iter_commits('main', max_count=50))
            print(fifty_first_commits)





    repo.commit('5888125c71572ca266cab9911ae042eedbaea142')
    #print(repo.heads)
    #print(repo.head.commit.tree)
    ##print(list(repo.index.iter_blobs()))


    print(list(repo.index.iter_blobs()))
    print(list(repo.head.commit.tree.traverse()))
    print(repo.index)
    for (_path, _stage), entry in repo.index.entries.items():
        print(_path)
        print(_stage)
        print(entry)
        file_contents = repo.git.show('{}:{}'.format("5888125c71572ca266cab9911ae042eedbaea142", entry.path)) # recupere le contenu du fichier
        #print(file_contents)

    # repo.heads.master
    #repo.commit('master')


    #repo.git.checkout('main')
    #a.git.checkout.master

    file = open("filename.md", "w+")
    file.write("---\r\n")
    file.write("title: \"My First Post\"\r\n")
    file.write("date: 2020-10-28T08:44:03+01:00\r\n")
    file.write("draft: true\r\n")
    file.write("---\r\n")

    print(dir + "README.md")
    if os.path.isfile(dir+"README.md"):
        readme = open(dir+"README.md", "w+")
        #print(readme.read())
        file.write(readme.read()+"\r\n")

    file.close()

    print("génération du site")

    os.chdir(str(os.path.dirname(__file__)+"/.."))
    os.system("hugo -D")


if __name__ == "__main__":
    main()

