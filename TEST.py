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

otp_files = []
flash_files = []

for file_name in files:
    if "otp" in file_name.lower():
        otp_files.append(file_name)
    
    elif "flash" in file_name.lower():
        flash_files.append(file_name)

print(f'OTP LIST: {otp_files}\n')
print(f'FLASH LIST: {flash_files}\n')

for file_name in files:
    base, extension = os.path.splitext(file_name)
    print(f'BASE: {base}')
    print(f'EXT: {extension}\n')
