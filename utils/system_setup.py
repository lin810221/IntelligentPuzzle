import configparser
import sys

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
