
import os
import json


def save(data: dict = {}, logfile: str = 'journal.jl') -> bool:
    ''' Convert a dictionary to a
    JSON string and append it to a file.
    If the specified file does not exist,
    the function will create it.
    Returns:
        True if logging is completed without errors.
        False if some error ocurred.
    '''
    if not data:
        return False
    location, _file = os.path.split(logfile)
    if location:
        try:
            if _file not in os.listdir(location):
                open(logfile, 'a').close()  # create file
        except (BaseException, PermissionError) as e:
            print(e)
            return False
    try:
        with open(logfile, 'a') as f:
            f.write(json.dumps(data)+'\n')
        return True
    except (BaseException, PermissionError) as e:
        print(e)
        return False
