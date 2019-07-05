from setuptools import setup
import os,sys
from  help import package

os.system("python -m pip install --upgrade pip")

for pack in package:
    os.system(f"pip install {pack}")


os.system("pip freeze > requirements.txt")
#setup(


#)