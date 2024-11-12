import os 
import filecmp, shutil
from datetime import datetime

import argparse
import psutil
import app_logging
import logging
from utils_ import get_folder_size, find_oldest_file

# parser = argparse.ArgumentParser(description="Process some arguments.")
# parser.add_argument('--proc', type=str, help="Specify the process to check for")
# args = parser.parse_args()
# if args.proc:
#     # logging.info(f"Proc arg: {args.proc}")
#     # if is_process_running(args.proc):
#     #     print("Studio One.exe is running.")
#     # else:
#     #     print("Studio One.exe is not running.")
    
# else:
#     logging.info("No --proc argument was provided.")
    
# def is_process_running(process_name):
#     for process in psutil.process_iter(['name']):
#         if process.info['name'] == process_name:  return True
#     return False

dc = {0: 'not copying', 1: 'newer file', 2: 'prev file non existent', 3: 'user setting'}

copy_unchanged_files = False
username = os.getenv("username")
#root = f"C:\\Users\\{username}\\Documents\\Unreal Projects\\toBackup"
# root = f"C:\\Users\\{username}\\Documents\\Unreal Projects\\VRExpPluginExample-4.26-Locked\\"
# copy_from = f"C:\\Users\\{username}\\Documents\\Unreal Projects\\VRExpPluginExample-4.26-Locked\\"
#root = f"C:\\Users\\{username}\\Documents\\Unreal Projects\\VRExpPluginExample-master4.27\\"
# root_copy_from = [f"C:\\Users\\{username}\\Documents\\Unreal Projects\\VRExpPluginExample-master4.27\\"]
# copy_from_flds = ['Source', "Content", "Config", "blender"]
#copy_from = [copy_from[0] + fld for fld in copy_from_flds]

#backup_to = ["D:\\soft\\unreal_backup_cpp\\", "E:\\soft\\unreal_backup_cpp\\"  ]
# backup_to = ["D:\\soft\\unreal_backup_cpp_4.27\\", "E:\\soft\\unreal_backup_cpp_4.27\\"  ]
# date_based__folders = ["Content\\StylizedAssets"]
date_based__folders = []
root_copy_from = f"C:\\Users\\{username}\\Documents\\Studio One\\Songs\\"
backup_to= ["K:\\all\\music\\backup\\Sync\\OneDrive"]
copy_from_flds =["."]#[name for name in os.listdir(root_copy_from[0]) if os.path.isdir(root_copy_from[0]+name)]+["."]
folder_nb = 0
folders_to_exclude = ["package\\", "Saved\\", "CachedAssetRegistry", "NativizedBuild", "v16\\", "\\Development", "\\Engine", "\\AdvancedSessions", "\\Intermediate", "\\DebugGame", "\\Binaries", "\\StylizedAssets", "\\DerivedDataCache"]#"LongswordAnimsetPro", "MedievalInfantry", "ExampleContent_CelShader"]
# nb_backup_files = 0

year = 2022; month = 4; day = 1
copy_if_recent = ["fixed", datetime(year, month, day, 0, 0)]
extensions = [".song", ".mscz", ".ass", ".css", ".csv", ".txt", ".mid"]



class context():
    def __init__(self) -> None:
        self.nb_backup_files = 0
        self.target_dir = None
        self.existing_backups = None
        self.folder_nb = 0
        self.max_file_versions = 2
        self.exclude_with_string = "Autosave"
        self.fld_size = 0
        self.file_version_threshold =  4e+9 # 4gb
        self.delete_older = False
        

def backup_folder(root_fld_from, folder, based_on_date, ctx:context):
    # global nb_backup_files
    assert(ctx.max_file_versions != 1)
    for path, subdirs, files in os.walk(root_fld_from+folder):
        
        # for s in subdirs:
        #     root_target = path.split(root_fld_from)[1]
        #     td = os.path.join(target_dir, root_target, s )
        #     os.makedirs(td, exist_ok=True)

        for name in files:
            if not file_has_extension(name, extensions) or ctx.exclude_with_string and ctx.exclude_with_string in name:
                continue

            root_target = path.split(root_fld_from)[1]

            curr_src = root_fld_from + root_target + "\\" + name
            target_path = ctx.target_dir + "\\" + root_target
            target_file = target_path +  "\\" + name

            prev_backup_files = [dir_ + "\\" + root_target +  "\\" + name for dir_ in ctx.existing_backups]

            def copy():
                # global nb_backup_files
                os.makedirs(os.path.dirname(target_file), exist_ok=True)
                shutil.copy2(curr_src, target_file)
                ctx.nb_backup_files+=1

            file_check = is_missing_or_older(prev_backup_files, curr_src, ctx)

            if not based_on_date:
                
                if not is_excluded(target_file) and file_check != 'not copying':
                    logging.info(f"Copying: ({file_check:<26}) {curr_src}" )
                    copy()
                #else:
                    #logging.info("Not copying: ".ljust(15), curr_src)
            else:

                new_time = os.path.getmtime(curr_src)
                t = datetime.fromtimestamp(new_time)
                if t > copy_if_recent[1] and file_check != 'not copying':
                    logging.info(f"Copying: ({file_check:<26}) {curr_src}" )
                    # logging.info("Copying: ".ljust(15), curr_src, " reason ", file_check)
                    copy()

                    
                
def file_has_extension(filename, extensions_):
    return filename.endswith(tuple(extensions_))

def is_excluded(path):
    for excl in folders_to_exclude:
        if excl in path:
            return True
    return False

def is_missing_or_older(prev_files, new_file, ctx:context):
    if copy_unchanged_files: 
        return dc.get(3)

    prev_files_exist = []
    prev_files_exist_all = []
    exsisting_count = 0
    for prev_file in prev_files:
        ex = os.path.isfile(prev_file)
        prev_files_exist_all.append(ex)
        if ex:
            exsisting_count += 1
            prev_files_exist.append(prev_file)

            
    if exsisting_count == 0:
        return 'prev file non existent'
    elif ctx.delete_older and  exsisting_count > 1 and exsisting_count >= ctx.max_file_versions:
        oldest = find_oldest_file(prev_files_exist)
        os.remove(oldest)
        ind = prev_files.index(oldest)
        prev_files_exist_all[ind] = False
        logging.info(f"--> Removing oldest version file ({exsisting_count} >= {ctx.max_file_versions}) {oldest}")
    
    n = len(prev_files) -1
    while not prev_files_exist_all[n]:# os.path.isfile(prev_files[n]):
        n-=1

    #prev_time = os.path.getmtime(prev_files[n])
    #new_time = os.path.getmtime(new_file)
    #delta = prev_time - new_time
    #if os.path.getmtime(prev_files[n]) > os.path.getmtime(new_file):
    if not filecmp.cmp(prev_files[n], new_file):
        return 'difference in file'

    return 'not copying'

def main_task():
    for copy_to in backup_to:
        os.makedirs(copy_to, exist_ok=1)
        
        ctx = context()
        ctx.fld_size = get_folder_size(copy_to)
        ctx.delete_older = ctx.fld_size > ctx.file_version_threshold
        
        flds = next(os.walk(copy_to))[1]
        ctx.folder_nb = len(flds)

        ctx.existing_backups = [copy_to + "\\" + file for file in flds if file != "Documents" and file != "Attachments"]
        
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d_%H.%M.%S")
        logging.info(f"date and time = { dt_string}")	

        # target_dir = os.path.join(copy_to, str(folder_nb).zfill(4) + dt_string)
        ctx.target_dir = os.path.join(copy_to,  dt_string)
        #prev_backup_dir = existing_backups[-1]

        try: os.mkdir(ctx.target_dir)
        except: logging.error(f"Error creating folder {ctx.target_dir}", )

        for folder in date_based__folders:
            backup_folder(root_copy_from, folder, True, ctx)

        for folder in copy_from_flds:
            backup_folder(root_copy_from, folder, False, ctx)

        if ctx.nb_backup_files == 0:
            logging.info(f"No files backuped, deleting empty dir {ctx.target_dir}")
            os.rmdir(ctx.target_dir)


if __name__ == "__main__":
    main_task()
    