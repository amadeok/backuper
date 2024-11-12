
import os

def get_folder_size(folder_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            # Check if the file exists (avoid broken symlinks)
            if os.path.exists(file_path):
                total_size += os.path.getsize(file_path)
    return total_size

def find_oldest_file(file_list):
    # Initialize variables for tracking the oldest file
    oldest_file = None
    oldest_time = float('inf')  # Use infinity as the initial oldest time

    for file in file_list:
        # Check if the file exists
        if os.path.exists(file):
            # Get the file's modification time
            mod_time = os.path.getmtime(file)
            # Update the oldest file if the current file is older
            if mod_time < oldest_time:
                oldest_time = mod_time
                oldest_file = file

    return oldest_file