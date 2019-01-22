'''
Drive.py is a single-class module. the Drive class
allows simple manipulation of files. Designed to work
with a single file locally which will be constantly
backed up on Google Drive.
'''
import os

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


class Drive(object):
    ''' A simple, single-purpose-specific, wrapper
    for PyDrive.
    '''

    def __init__(self, credentials_file: str = 'mycreds.txt'):
        ''' Initialize the drive object with a default credentials_file,
        which should be in the same directory as the script. A file can be
        specified providing the relative or absolute path.
        '''
        self.__gauth = GoogleAuth()
        try:
            self.__gauth.LoadCredentialsFile(credentials_file)
        except Exception:
            pass
        if self.__gauth.credentials is None:
            # Platform-specific handling of missing credentials.
            if os.uname().sysname == 'Linux':
                self.__gauth.LocalWebserverAuth()
            elif (os.uname().sysname == 'Darwin' and\
                    'iPhone' in os.uname().machine):
                import console
                console.alert('ERROR: Manual authentication needed.')
                self.__gauth.LocalWebserverAuth()
            else:
                raise Exception
        elif self.__gauth.access_token_expired:
            self.__gauth.Refresh()
        else:
            self.__gauth.Authorize()
        self.__gauth.SaveCredentialsFile(credentials_file)
        self.__drive = GoogleDrive(self.__gauth)
    # END __init__

    @property
    def drive(self):
        return self.__drive

    def file_exists(self, some_file: str, query: str = '') -> bool:
        ''' Query Drive to verify the existence of a given file.
        The provided string 'some_file' should correpond EXACTLY
        to the name that appears on GoogleDrive.
        If no query is provided, the default _query will yield
        all files in the root folder.
        Useful links on query syntax:
            https://pythonhosted.org/PyDrive/filelist.html
            https://developers.google.com/drive/api/v2/search-parameters
        '''
        file_list = self.__query_drive(query)
        if some_file in [_file['title'] for _file in file_list]:
            return True
        else:
            return False

    def update(self, file_name: str, path: str = ''):
        file_list = self.__query_drive()
        titles = [_file['title'] for _file in file_list]
        if path:
            path_to_file = os.path.join(path, file_name)
        else:
            path_to_file = file_name
        if file_name in titles:
            _index = titles.index(file_name)
            _gdrive_file = file_list[_index]
        else:
            _gdrive_file = self.__drive.CreateFile({'title': file_name})
        try:
            _gdrive_file.SetContentFile(path_to_file)
            _gdrive_file.Upload()
            return True
        except (BaseException, FileNotFoundError):
            return False

    def __query_drive(self, query: str = '') -> list:
        ''' Helper method returning a list of files.
        A wrapper for the call:
            self.__drive.ListFile(_query).GetList()
        Default query:
            {'q': "'root' in parents and trashed=false"}
        '''
        if query:
            _query = query
        else:
            _query = {'q': "'root' in parents and trashed=false"}
        file_list = self.__drive.ListFile(_query).GetList()
        return file_list

# END Drive
