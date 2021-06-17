import os
import pandas as pd

import numpy as np
from fnmatch import fnmatch
from difflib import SequenceMatcher
from datetime import datetime, timedelta
from pathlib import Path


known_headers = [
    "patient_id", "time",
    "heart_rate_min","heart_rate_median","heart_rate_max",
    "respiration_rate_min","respiration_rate_median","respiration_rate_max",
    "heart_rate_variability_min","heart_rate_variability_median","heart_rate_variability_max",
    "relative_stroke_volume_min","relative_stroke_volume_median","relative_stroke_volume_max",
    "status","sleep_status"]

episodes = ["heart_rate_min","heart_rate_median","heart_rate_max",
    "respiration_rate_min","respiration_rate_median","respiration_rate_max",
    "heart_rate_variability_min","heart_rate_variability_median","heart_rate_variability_max",
    "relative_stroke_volume_min","relative_stroke_volume_median","relative_stroke_volume_max"]

epi_dict = {
    'Heart Rate': ["heart_rate_min","heart_rate_median","heart_rate_max"],
    'Respiration Rate' : ["respiration_rate_min","respiration_rate_median","respiration_rate_max"],
    'Heart Rate Variability': ["heart_rate_variability_min","heart_rate_variability_median","heart_rate_variability_max"],
    'Relative Stroke Volume': ["relative_stroke_volume_min","relative_stroke_volume_median","relative_stroke_volume_max"]
}

episodes = ["heart_rate_min","heart_rate_median","heart_rate_max",
    "respiration_rate_min","respiration_rate_median","respiration_rate_max",
    "heart_rate_variability_min","heart_rate_variability_median","heart_rate_variability_max",
    "relative_stroke_volume_min","relative_stroke_volume_median","relative_stroke_volume_max"]

plot_settings = ['interval', 'current_full', 'hidePlot', 'hiddenPlots',
         'hideLine', 'hiddenLines', 'Vline_win', 'checked_vline_ax', 'hiddenVline_ax', 'Vlines', 'PrevIntervals',
         'PrevInterval_Objects']

patient_settings = ['start_tick', 'SLEEP', 'HR', 'RESP', 'HRV', 'REL', 'FULL', 'df', 'markerList', 'x_list', 'points', 'texts', 'MarkedIntervals']



#######################################################################################################################
def extract_paths(directory):
    paths = []
    pattern = "*.csv"

    for path, subdirs, files in os.walk(directory):
        for name in files:
            if fnmatch(name, pattern):
                paths.append(os.path.join(path, name))

    return paths


#######################################################################################################################
def read_files(pathList):
    DICT_ID_df = {}
    unknown_id_index = 1

    for path in pathList:
        df = pd.read_csv(path)
        df.columns = df.columns.str.lower()
        new_headers = (set(list(df.columns)).difference(known_headers))
        missing_headers = (set(known_headers).difference(list(df.columns)))

        if len(new_headers) > 0:
            for new in new_headers:
                highest = 0
                for header in missing_headers:
                    ratio = SequenceMatcher(None, new, header).ratio()

                    if ratio > highest:
                        highest = ratio
                        name = header

                if highest > 0:
                    df.rename(columns={new: name}, inplace=True)

        still_missing = (set(known_headers).difference(list(df.columns)))

        if len(still_missing) > 0:
            for i in still_missing:
                if i == 'patient_id':
                    print('WARNING:',path,'does not contain "patient_id". Default ID is given: Unknown patient #',str(unknown_id_index))
                    df[i] = 'Unknown patient #'+str(unknown_id_index)

                else:
                    df[i] = np.nan

        df['time'] = pd.to_datetime(df['time'])
        df['time'] = df['time'].dt.floor('Min')

        df['date'] = df['time'].dt.date
        df['date'] = df['date'].astype(str)

        DICT_ID_df[df['patient_id'].iloc[0]] = df


    return DICT_ID_df



#######################################################################################################################
def GET_DF_FOR_DATE(ID,DATE,DICT_ID_df):
    df = DICT_ID_df[ID]
    df = df[df['date'] == DATE]
    timeList = find_time_gap(df)

    max_dt = max(df['time'])
    min_dt = min(df['time'])
    dt_range = []
    while min_dt <= max_dt:
        dt_range.append(min_dt.strftime("%Y-%m-%d %H:%M:%S"))
        min_dt += timedelta(minutes=1)
    complete_df = pd.DataFrame({'time': dt_range})
    complete_df['time'] = pd.to_datetime(complete_df['time'])
    df = complete_df.merge(df, how='left', on='time')
    df['time'] = df['time'].dt.time
    df['time'] = df['time'].apply(lambda t: t.strftime('%H:%M'))
    df['time'] = df['time'].astype(str)

    markerList = []
    index = df.index
    for time in timeList:
        condition = df['time'] == time
        diff_indices = index[condition][0]
        if pd.isnull(df['heart_rate_median'].loc[diff_indices + 1]):
            markerList.append(time)


    return df,markerList


#######################################################################################################################
def find_time_gap(df):
    df['delta'] = (df['time']-df['time'].shift()).fillna(pd.Timedelta('0 days'))
    df['ans'] = df['delta'].apply(lambda x:x /np.timedelta64(1,'m')).astype('int64') % (24 * 60)

    index = df.index
    condition = df['ans'] > 1
    diff_indices = index[condition]
    diff_indices_list = diff_indices.tolist()

    timeList = []
    for i in diff_indices_list:
        timeList.append(str(df['time'].loc[i].time().strftime('%H:%M')))

    return timeList


#######################################################################################################################
def get_ColorDict():
    ColorDict = {}
    ColorDict["awake"] = "#ef476f"
    ColorDict["wakefulness"] = "#ffd166"
    ColorDict["rem_sleep"] = "#06d6a0"
    ColorDict["shallow_sleep"] = "#118ab2"
    ColorDict["deep_sleep"] = "#073b4c"
    ColorDict[str(np.nan)] = '#F0FFF0'

    return ColorDict


if __name__ == "__main__":
    pathList = extract_paths('/Users/eier/PyCharm_Projects/DATA')
    dictionary = read_files(pathList)
    #print(dictionary.keys())
    #print(dictionary['bee41650-b699-4cac-a838-75f01b2656ae'])


