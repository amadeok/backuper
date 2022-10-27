
import os
from datetime import datetime


year = 2022; month = 4; day = 1
copy_if_recent = ["fixed", datetime(year, month, day, 0, 0)]
date = copy_if_recent[1].timestamp() -1000

root_copy_from = ["C:\\Users\\amade\\Documents\\Unreal Projects\\VRExpPluginExample-master4.27\\Content\\StylizedAssets\\"]
subfs = ["StylizedWeather", "Medieval_Weapons", "Realistic_Medieval_Weapons_and_Shields_Kit", "FXVillesBloodVFXPack", "HB_MedievalWeapPack3", "FastStylizedProceduralSky2", "FantasyWeapons"]

def backup_folder(root_fld_from, folder):
    global nb_backup_files
    for path, subdirs, files in os.walk(root_fld_from+folder):
        for name in files:
            #print(os.path.join(path, name))
            
            root_target = path.split(root_fld_from)[1]

            curr_src = root_fld_from + root_target + "\\" + name
            os.utime(curr_src, (date, date))
            
for folder in subfs:
    backup_folder(root_copy_from[0], folder)