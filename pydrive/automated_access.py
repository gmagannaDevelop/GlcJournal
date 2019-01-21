
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


gauth = GoogleAuth()
gauth.LoadCredentialsFile("mycreds.txt")

if gauth.credentials is None:
  gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
  gauth.Refresh()
else:
  gauth.Authorize()

gauth.SaveCredentialsFile("mycreds.txt")

drive = GoogleDrive(gauth)

file1 = drive.CreateFile({'title': 'Automata.txt'})  # Create GoogleDriveFile instance with title 'Hello.txt'.
file1.SetContentString('Automataaa') # Set content of the file from given string.
file1.Upload()
print(drive)
