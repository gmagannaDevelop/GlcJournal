
import os

class Dir(object):
  ''' 
  Class used to enforce the execution 
  of a script on a given path, 
  allowing the use of relative paths.
  '''

  def __init__(self, desired_path : str):
    self.__goal = desired_path

  @property
  def pwd(self) -> str:
    ''' Wrapper for os.path.asbpath('.') 
    '''
    return os.path.abspath('.')

  @property
  def path(self) -> str:
    ''' Returns the path passed to the constructor, 
    i.e. the desired working directory for the script.
    '''
    return self.__goal

  def verify(self) -> bool:
    ''' Check if current path corresponds to
    the desired one (passed to the object constructor).
    '''
    if os.path.abspath('.') == self.__goal:
      return True
    else:
      return False

  def cd_to_goal(self) -> bool:
    ''' Try to change the cwd to the 'goal'
    path. Returns True upon success and False
    if the operation was unsuccessful.
    '''
    try:
      os.chdir(self.__goal)
      return True
    except:
      return False
#
