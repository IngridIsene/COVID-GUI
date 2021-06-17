import sys
import pickle
from PyQt5.QtWidgets import QApplication
from os import path
from functions import extract_paths,read_files
from Classes.choice_window import Choice_window
import os
from pathlib import Path

# PATHS
MAIN_PATH = str(Path(os.path.dirname(__file__)).parent.absolute()) # /Users/user/PyCharm_Projects
EXCEL_PATH = MAIN_PATH+'/EXCEL'
GUI_PATH = MAIN_PATH+'/GUI'
PICKLE_PATH = GUI_PATH+'/PICKLE'
DATA_PATH = MAIN_PATH+'/DATA'


if __name__ == "__main__":
    if path.exists(PICKLE_PATH+'/pickle.pkl') == False:
        pathList = extract_paths(DATA_PATH)
        DICT_ID_df = read_files(pathList)

        objects = [pathList, DICT_ID_df]
        file = open(PICKLE_PATH+'/pickle.pkl', "wb")
        pickle.dump(objects, file)
        file.close()

    elif path.exists(PICKLE_PATH+'/pickle.pkl') == True:
        objects = pickle.load(open(PICKLE_PATH + "/pickle.pkl", "rb"))
        pickled_pathList = objects[0]
        pickled_DICT_ID_df = objects[1]

        current_pathList = extract_paths(DATA_PATH)
        new_files = (set(list(current_pathList)).difference(pickled_pathList))

        if bool(new_files) == True:
            print('pickled pathList:',pickled_pathList)
            print('current pathList:',current_pathList)
            print('new paths:', new_files)


        DICT = read_files(new_files)
        for k, v in DICT.items():
            pickled_DICT_ID_df[k] = v

        objects = [current_pathList, pickled_DICT_ID_df]
        file = open(PICKLE_PATH + '/pickle.pkl', "wb")
        pickle.dump(objects, file)
        file.close()






    if path.exists(PICKLE_PATH+'/plot_settings.pkl') == False:
        plot_settings = {}
        with open(PICKLE_PATH+'/plot_settings.pkl', "wb") as f:
            pickle.dump(plot_settings, f)

    if path.exists(PICKLE_PATH+'/patient_settings.pkl') == False:
        patient_settings = {}
        with open(PICKLE_PATH+'/patient_settings.pkl', "wb") as f:
            pickle.dump(patient_settings, f)



    app = QApplication(sys.argv)
    window = Choice_window()
    sys.exit(app.exec_())