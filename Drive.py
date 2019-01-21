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

    def __init__(self, credentials_file: str = 'mycreds.txt',
        content_file: str = 'journal.jl'):
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

    def update(self):
        pass


# END Drive

''''
file1 = drive.CreateFile({'title': 'Automata.txt'})
# ^ Create GoogleDriveFile instance with title 'Hello.txt'.
file1.SetContentString('Automataaa')
# ^ Set content of the file from given string.
file1.Upload()
print(drive)
'''
