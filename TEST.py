import os


#folder_path = input("Input folder PATH: ")

folder_path = 'D:\RENAME'

def get_files_name(folder_path):
    try:
        # Get all files & folders in the directory
        items = os.listdir(folder_path)
    
        # Filter out folders and kepp only file names
        files = [item for item in items if os.path.isfile(os.path.join(folder_path, item))]

        return files
    
    except FileNotFoundError:
        print("Folder not found.")
    
    except PermissionError:
        print("Permission denied to access the folder.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

files = get_files_name(folder_path)

def filter_direct_name(files):
    cache_files = []
    
    first_file = files[0]

    if 'otp' in first_file.lower():
        for file_name in files:
            if 'otp' not in file_name.lower():
                print(f'Error:File {file_name} should contain "otp"')    
            else:
                cache_files.append(file_name)
                
    elif 'flash' in first_file.lower():
        for file_name in files:
            if 'flash' not in file_name.lower():
                print(f'Error:File {file_name} should contain "flash"')    
            else:
                cache_files.append(file_name)
    else:
        print('The first file name does not contain "otp" or "flash"')
                
    return cache_files                


cache_files = filter_direct_name(files)
print(cache_files)
