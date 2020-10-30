import re, os, shutil, math, pathlib
import sqlite3
import git

def main ():

    print("Début de la génération")



    dir = str(os.path.dirname(__file__)+"/score/")
    print(dir)
    git.Repo.clone_from("https://github.com/banco29510/score_test.git", dir)


    if os.path.isdir(dir):
        shutil.rmtree(dir, ignore_errors=True)
    else:
        os.mkdir(dir)


if __name__ == "__main__":
    main()