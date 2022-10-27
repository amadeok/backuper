import os, filecmp, shutil

source_path = "C:\\Users\\amade\\Documents\\Unreal Projects\\VRExpPluginExample-4.26-Locked\\"
target_path = '\\\\LAPTOP-40OC0U0E\\VRExpPluginExample-4.26-Locked\\'

source_path = "E:\\amadeo\\SwordKing\\"
target_path = "C:\\Users\\amade\\Documents\\Unreal Projects\\SwordKing503\\"
#ret = open(path)
#for f in os.walk(path):
   #print(f)

folder_to_sync = ['Source', "Content", "Config"]
#folder_to_sync = ['Source']
#folder_to_sync = ['Source', "Content"]
specific_flds = ["C:\\Users\\amade\\Documents\\Unreal Projects\\VRExpPluginExample-4.26-Locked\\Plugins\\VRExpansionPlugin\\VRExpansionPlugin\\Source"]

max_file_size_mb = 20000;

directory_contents = os.listdir(source_path)
print(directory_contents)

source_file = ""
target_file = ""

def sync_folder(folder):
    for path, subdirs, files in os.walk(folder):
        for name in files:
            if os.path.getsize(path+"\\"+name) < max_file_size_mb*1000*1000:
                source_file = path + "\\" + name
                target_file = target_path+ source_file.split(source_path)[1]

                if os.path.isfile(target_file):
                    if not filecmp.cmp(source_file, target_file):
                        print("Copying: ".ljust(15), source_file, " to ", target_file, " files are different")
                        os.makedirs(os.path.dirname(target_file), exist_ok=True)
                        shutil.copy2(source_file, target_file)
                    else:
                        print("Not copying: ".ljust(15), source_file, " files are the same")
                else: 
                    print("Copying: ".ljust(15), source_file, " to ", target_file, " target file doesn't exist")
                    os.makedirs(os.path.dirname(target_file), exist_ok=True)
                    shutil.copy2(source_file, target_file)
            else:
                print("Not copying: ".ljust(15), path+"\\"+name, "files is greater than ", max_file_size_mb, " megabytes")

for fld in specific_flds:
    sync_folder(fld)


for dir in directory_contents:
    if dir in folder_to_sync:
        sync_folder(source_path + dir)






    # for path, subdirs, files in os.walk(dir):
    #     for name in files:
    #         #print(os.path.join(path, name))
            
    #         root_target = path.split(root)[1]

    #         curr_src = copy_from + root_target + "\\" + name
    #         target_path = target_dir + "\\" + root_target
    #         target_file = target_path +  "\\" + name
            
    #         prev_backup_files = [dir_ + "\\" + root_target +  "\\" + name for dir_ in existing_backups]

    #         file_check = is_missing_or_older(prev_backup_files, curr_src)

    #         if not is_excluded(target_file) and file_check != 'not copying':
    #             print("Copying: ".ljust(15), curr_src, " to ", target_file, " reason ", file_check)
    #             os.makedirs(os.path.dirname(target_file), exist_ok=True)
    #             shutil.copy2(curr_src, target_file)
    #             nb_backup_files+=1
    #         else:
    #             print("Not copying: ".ljust(15), curr_src)


