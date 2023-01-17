import os 
import filecmp, shutil

 
from datetime import datetime
filepath = "C:\\patt\\some.fbx"

file_name = os.path.basename(filepath)
basepath = filepath.split(file_name)[0]
basename = ''
if '.fbx' in file_name:
    basename =  file_name.split(".fbx")[0]
else:
    basename =  file_name.split(".FBX")[0]
file_name = basename + "_R.fbx"
final_path = basepath + "\\processed\\" + file_name 

print(final_path)

dc = {0: 'not copying', 1: 'newer file', 2: 'prev file non existent', 3: 'user setting'}

copy_unchanged_files = False
#root = "C:\\Users\\amade\\Documents\\Unreal Projects\\toBackup"
# root = "C:\\Users\\amade\\Documents\\Unreal Projects\\VRExpPluginExample-4.26-Locked\\"
# copy_from = "C:\\Users\\amade\\Documents\\Unreal Projects\\VRExpPluginExample-4.26-Locked\\"
#root = "C:\\Users\\amade\\Documents\\Unreal Projects\\VRExpPluginExample-master4.27\\"
root_copy_from = ["C:\\Users\\amade\\Documents\\Unreal Projects\\VRExpPluginExample-master4.27\\"]
copy_from_flds = ['Source', "Content", "Config", "blender"]
#copy_from = [copy_from[0] + fld for fld in copy_from_flds]

#backup_to = ["D:\\soft\\unreal_backup_cpp\\", "E:\\soft\\unreal_backup_cpp\\"  ]
backup_to = ["D:\\soft\\unreal_backup_cpp_4.27\\", "E:\\soft\\unreal_backup_cpp_4.27\\"  ]
date_based__folders = ["Content\\StylizedAssets"]

root_copy_from = ["C:\\Users\\amade\\Documents\\dawd\\"]
backup_to= ["F:\\all\\music\\backup"]
copy_from_flds =[name for name in os.listdir(root_copy_from[0]) if os.path.isdir(root_copy_from[0]+name)]+["."]
folder_nb = 0
folders_to_exclude = ["package\\", "Saved\\", "CachedAssetRegistry", "NativizedBuild", "v16\\", "\\Development", "\\Engine", "\\AdvancedSessions", "\\Intermediate", "\\DebugGame", "\\Binaries", "\\StylizedAssets", "\\DerivedDataCache"]#"LongswordAnimsetPro", "MedievalInfantry", "ExampleContent_CelShader"]
nb_backup_files = 0

year = 2022; month = 4; day = 1
copy_if_recent = ["fixed", datetime(year, month, day, 0, 0)]


def backup_folder(root_fld_from, folder, based_on_date):
    global nb_backup_files
    for path, subdirs, files in os.walk(root_fld_from+folder):
        for name in files:
            #print(os.path.join(path, name))
            
            root_target = path.split(root_fld_from)[1]

            curr_src = root_fld_from + root_target + "\\" + name
            target_path = target_dir + "\\" + root_target
            target_file = target_path +  "\\" + name

            prev_backup_files = [dir_ + "\\" + root_target +  "\\" + name for dir_ in existing_backups]

            def copy():
                global nb_backup_files
                os.makedirs(os.path.dirname(target_file), exist_ok=True)
                shutil.copy2(curr_src, target_file)
                nb_backup_files+=1

            file_check = is_missing_or_older(prev_backup_files, curr_src)

            if not based_on_date:
                
                if not is_excluded(target_file) and file_check != 'not copying':
                    print("Copying: ".ljust(15), curr_src, " reason ", file_check)
                    copy()
                #else:
                    #print("Not copying: ".ljust(15), curr_src)
            else:

                new_time = os.path.getmtime(curr_src)
                t = datetime.fromtimestamp(new_time)
                if t > copy_if_recent[1] and file_check != 'not copying':
                    print("Copying: ".ljust(15), curr_src, " reason ", file_check)
                    copy()

                    
                
                

def is_excluded(path):
    for excl in folders_to_exclude:
        if excl in path:
            return True
    return False
def is_missing_or_older(prev_files, new_file):
    if copy_unchanged_files: 
        return dc.get(3)

    exsisting_count = 0
    for prev_file in prev_files:
        if os.path.isfile(prev_file):
            exsisting_count += 1
    if exsisting_count == 0:
        return 'prev file non existent'\

    n = len(prev_files) -1
    while not os.path.isfile(prev_files[n]):
        n-=1

    #prev_time = os.path.getmtime(prev_files[n])
    #new_time = os.path.getmtime(new_file)
    #delta = prev_time - new_time
    #if os.path.getmtime(prev_files[n]) > os.path.getmtime(new_file):
    if not filecmp.cmp(prev_files[n], new_file):
        return 'difference in file'

    return 'not copying'

for copy_to in backup_to:
    try: os.makedirs(copy_to)
    except: pass
    folder_nb= len(next(os.walk(copy_to))[1])

    existing_backups = [copy_to + "\\" + file for file in next(os.walk(copy_to))[1]]

    now = datetime.now()
    dt_string = now.strftime("_%d-%m-%Y_%H.%M.%S")
    print("date and time =", dt_string)	

    target_dir = os.path.join(copy_to, str(folder_nb).zfill(4) + dt_string)
    #prev_backup_dir = existing_backups[-1]

    try: os.mkdir(target_dir)
    except: print("Error creating folder ", target_dir)

    max_size = 30

    for folder in date_based__folders:
        backup_folder(root_copy_from[0], folder, True)

    for folder in copy_from_flds:
        backup_folder(root_copy_from[0], folder, False)

    if nb_backup_files == 0:
        print("No files backuped, deleting empty dir ", target_dir)
        os.rmdir(target_dir)
