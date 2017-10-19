import os


def GitLog():
    os.chdir(os.path.dirname(os.getcwd()))
    return os.popen('git log --oneline -1').readlines()[0]
