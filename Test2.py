import os
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
from Programs.Local.Updating.GitUpdating import DownloadLatestVersion, _DeleteOtherKontrolVersions
from Libraries.BRS_Python_Libraries.BRS.Network.APIs.GitHub import GitHub
from kivymd.uix.progressbar import MDProgressBar
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

class FUCK():
    def GoodDownload():
        return
    def FailedDownload():
        return

GitHub.CurrentTag = "0.0.0"
GitHub.LatestTag = "0.0.2"
# DownloadLatestVersion(MDProgressBar, FUCK)
_DeleteOtherKontrolVersions()
