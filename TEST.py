import os
import shutil


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



def filter_direct_name(files):
    cache_files = []
    
    first_file = files[0]

    if 'otp' in first_file.lower():
        for file_name in files:
            if 'otp' not in file_name.lower():
                print(f'Error:File {file_name} should contain "otp"')
                return []
            else:
                cache_files.append(file_name)
                
    elif 'flash' in first_file.lower():
        for file_name in files:
            if 'flash' not in file_name.lower():
                print(f'Error:File {file_name} should contain "flash"')
                return []
            else:
                cache_files.append(file_name)
    else:
        print('The first file name does not contain "otp" or "flash"')
        return []
                
    return cache_files                



files = get_files_name(folder_path)
cache_files = filter_direct_name(files)
#print(cache_files)



new_file_names = []



step = len(cache_files)

for i in range(step):
    file_name = cache_files[i]
    base, extension = os.path.splitext(file_name)
    base = base.split('_img')[0]
    

    for j in range(i+1, 9, step):
        new_file_names.append(f'{base}_img_{j:02d}{extension}')

print(new_file_names)


original_file_path = os.path.join(folder_path, cache_files[0])

output_folder_path = os.path.join(folder_path, 'output')
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)


for new_file_name in new_file_names:
    new_file_path = os.path.join(output_folder_path, f'{new_file_name}')
    shutil.copy(original_file_path, new_file_path)
