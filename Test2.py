import os
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
from Programs.Local.Updating.GitUpdating import DeleteOtherKontrolVersions
def get_last_directory(path):
    """
    Returns the last directory of a given path.
    """
    return os.path.basename(os.path.normpath(path))


currentPath = os.getcwd()
print(f"current path: {currentPath}")

folder = get_last_directory(currentPath)
print(f"current folder: {folder}")

Debug.enableConsole = True
DeleteOtherKontrolVersions()
