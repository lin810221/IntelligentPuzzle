import configparser
import datetime
import os
import sys


# Remove all pictures
def remove_pic():
    directory = './'
    for filename in os.listdir(directory):
        if filename.endswith('.png') and filename.startswith('(Result)'):
            file_path = os.path.join(directory, filename)
            os.remove(file_path)

# Get current time with format setting
def get_time(time_format):
    return datetime.datetime.now().strftime(time_format)

# ini setting config
def get_config(ini_file):
    config = configparser.ConfigParser()
    config.read(ini_file, encoding='utf-8')
    return config

# Deal with command line info.
def get_cli():
    len_argv = len(sys.argv)
    
    
    if len_argv == 1:
        print('Your script name: ', sys.argv[0])
    
    elif len_argv == 3:
        para1, para2 = sys.argv[1], sys.argv[2]
        return para1, para2
    
    else:
        print('Error: Out of specification')
        sys.exit(1)
