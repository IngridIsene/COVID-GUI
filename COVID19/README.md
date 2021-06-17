# COVID19


In the following it is assumed that GUI will be installed in a folder, COVID, which will be placed directly under the home folder which will be ~/ on MAC/Linux or C:\ on Windows. The setup instruction will use a default folder structure. 

Furthermore, GUI is developed using Python version 3.9.2 which can be downloaded from [Python](https://www.python.org/downloads/) for various operating systems. We cannot gurantee that it will work for older or newer version. In case of problems our install instructions incudes setting up a virtual environment. The instructions will set up a virtual environment called GUI. In the example we will make a directory .venv under the home directory.

You will need to use the Command Line on Windows or Terminal on MAC to give the instruction to the computer that is needed to install GUI. 

You will also need [Git](https://git-scm.com/downloads) installed on your computer to be able to install and update GUI.

# MAC/Linux
## Setting up default catalog structure and pull source code from github

```
mkdir ~/COVID
mkdir ~/COVID/EXCEL
mkdir ~/COVID/DATA
```
The COVID folder is the root directory for all directories used in this default structure. Data will be placed under DATA and the excel files is stored in the EXCEL folder. **THE CSV FILES CONTAINING THE PATIENT DATA MUST MANUALLY BE PLACED UNDER THE DATA FOLDER**. 

# Cloning, virtual enviroment setup and installing packages

GUI can be cloned from GitHub, using the terminal command. 
```
git clone --branch=main https://github.com/withya1809/COVID19.git ~/COVID/GUI
```
After using git clone, one must create another folder named Pickle. This is for storing settings related to the program. 
```
mkdir ~/COVID/GUI/PICKLE
```

Future updates can be made simply by giving the following commands:
```
cd ~/COVID/GUI
git pull
```
The virtual environment can be made according to:
```
mkdir ~/.venv
python3.9 -m venv ~/.venv/GUI
```
The required packages is installed in the virtual environment:
```
cd ~/COVID/GUI
source ~/.venv/GUI/bin/activate
pip install --upgrade pip
pip install wheel
pip install -r requirements.txt

```
# Procedure for running resprog

The following code must be run each time you want to run the program:
```
cd ~/COVID/GUI
source ~/.venv/GUI/bin/activate
python3 main.py
```


# WINDOWS
Setting up default catalog structure
```
md C:\COVID
md C:\COVID\EXCEL
md C:\COVID\DATA
```

# Cloning, virtual enviroment setup and installing packages

GUI can be cloned from GitHub, using the terminal command. After using git clone, one must create another folder named Pickle. This is for storing settings related to the program. 
```
git clone --branch=main https://github.com/withya1809/COVID19.git C:\COVID\GUI
md ~/COVID/GUI/PICKLE
```
Future updates can be made simply by giving the following commands:
```
cd C:\COVID\GUI
git pull
```
The virtual environment can be made according to:
```
md C:\.venv
python3.9 -m venv C:\.venv\GUI
```
The required packages is installed in the virtual environment:
```
cd C:\COVID\GUI
C:\.venv\GUI\Scripts\activate
pip install --upgrade pip
pip install wheel
pip install -r requirements.txt

```
# Procedure for running resprog

The following code must be run each time you want to run the program:
```
C:\.venv\GUI\Scripts\activate
cd C:\COVID\GUI
python3 main.py
```

