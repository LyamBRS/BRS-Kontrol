#====================================================================#
# File Information
#====================================================================#
"""
    AppLoading.py
    =============
    This file is used to control and coordinate the loading of the
    application's various things. It uses a list of things to do where
    each element is paired with a function that returns `True` if an
    error occured and `False` if that loading step was successful.
"""
#====================================================================#
# Loading Logs
#====================================================================#
from Libraries.BRS_Python_Libraries.BRS.Debug.LoadingLog import LoadingLog
LoadingLog.Start("AppLoadingHandler.py")
#====================================================================#
# Imports
#====================================================================#
#region ------------------------------------------------------ Python
import os
from enum import Enum
from functools import partial
#endregion
#region --------------------------------------------------------- BRS
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
from Libraries.BRS_Python_Libraries.BRS.Utilities.LanguageHandler import _
from Libraries.BRS_Python_Libraries.BRS.Network.Web.web import IsWebsiteOnline
from ...Pages.PopUps import PopUpsHandler,Keys,PopUpTypeEnum
#endregion
#region -------------------------------------------------------- Kivy
from kivy.clock import Clock
#endregion
#region ------------------------------------------------------ KivyMD
#endregion
LoadingLog.Log("Import success")
#====================================================================#
# Enums
#====================================================================#
LoadingLog.Log("LoadingStepsEnum")
class LoadingStepsEnum(Enum):
    """
        LoadingSteps:
        ------------
        This enumeration holds all the names of the application's
        loading steps and their short descriptions.
    """
    IntegrityCheck:int = 0
    """
        Step that checks Kontrol's program's to see if
        everything is there.
    """
    EnvironementGathering:int = 1
    """
        Step that gathers system informations.
    """
    InternetCheck:int = 2
    """
        Step that checks if Kontrol has access to the internet.
        If not, some of the next steps are bypassed.
    """
    GitHubCheck:int = 3
    """
        Step that checks if Kontrol can access GitHub's API
    """
    KontrolGitHub:int = 4
    """
        Step that checks if Kontrol is up to date with the
        repository. If not, it gets stored somewhere.
    """
    ProfilesCheck:int = 5
    """
        Step that checks if there is any profiles to choose from.
        If not, the profile creation screen will be the next screen.
    """
    DriversCheck:int = 6
    """
        Step that checks if Kontrol has any drivers available.
    """
    DriversGitHub:int = 7
    """
        If drivers are available, their github repositories are checked
        then checked for any new releases available.
    """
    BrSpandCheck:int = 8
    """
        Step that checks if Kontrol has any BrSpand card's drivers
        downloaded
    """
    BrSpandGitHub:int = 9
    """
        Step that check if the downloaded BrSpand card drivers have
        GitHub repositories and if they are up to date.
    """
# --------------------------------------------------------------------
LoadingLog.Log("ParamEnum")
class ParamEnum(Enum):
    """
        ParamEnum:
        ------------
        This enumeration holds all the data of each loading steps.
        Instead of using strings inside of the dictionary, this is
        used.
    """
    DisplayName:int = 0
    """
        Text that the user will see the loading step is executing
    """
    Function:int = 1
    """
        Function that executes the loading step.
        The function must return `True` if an error ocurred and
        `False` if it executed without any issues.
    """
    ErrorMessage:int = 2
    """
        Parameter where the function will store what happened during
        loading. If an error ocurred during the execution of the
        function, data will be added to a list which will be used to
        generate pop up error windows at the end of the loading process
        to inform the user of what happened.

        That parameter defaults to : `"Not done"`
    """
    ErrorType:int = 3
    """
        Parameter which holds the type of error received by the loading
        step function. See reference for more info.
    """
    Skip:int = 4
    """
        Parameter that holds a boolean value which represents if the
        step can be skipped or not. For example, if the internet check
        fails, there is no point in attempting to connect to each
        driver's GitHub repositories to check for updates.

        - `True`: Can be skipped
        - `False`: Default value, need to execute this loading step
    """
    ErrorCallBackFunction:int = 5
    """
        Parameter that holds the loading step's call back function
        which is only executed if the loading step's execution
        function returns an error (`True`).

        For example, the internet check CallBackFunction would
        set the skip of all GitHub functions to `True`.
    """
# --------------------------------------------------------------------
LoadingLog.Log("ErrorTypeEnum")
class ErrorTypeEnum(Enum):
    """
        ErrorTypeEnum:
        ------------
        This enumeration holds each types of error that a loading step
        function can result. This is usually used in their callback
        function which is only executed if they returned `True`.
    """
    Default:int = -1
    """ The step has yet to be executed """
    Success:int = 0
    """ The loading step was successful """
    Corruption:int = 1
    """ Loading step found a corruption """
    Exception:int = 2
    """ An exception occured while executing the step """
    Warning:int = 3
    """ The step needs to warn the user of something """
    CriticalError:int = 4
    """ The step found a critical error and the application cannot launch """
    NoConnection:int = 5
    """ The step could not execute due to no connection """
    APIOutOfRequest:int = 6
    """ The step could not execute because the API used ran out of requests """
#====================================================================#
# Functions
#====================================================================#
LoadingLog.Log("IntegrityCheck")
def IntegrityCheck() -> bool:
    #region ---- DocString
    """
        IntegrityCheck:
        ---------------
        This loading step function check's if anything critical is
        missing from Kontrol's repository. Here is the list of folders
        and files it validates:
        - Are all the main folders found
        - Are all BrSpand folders found
        - Are all Libraries folders found
        - Are all Local folders found
        - Are all Programs folder found
        - Are all Programs/Local folders found
        - Are all Programs/Pages pages found
        - Is all BRS logos icons found
        - Is there any Cache.json file inside of the Cache folder
        - Is there at least one language pack
        Returns:
            `bool`: `True`: Error occured. `False`: Successfully executed
    """
    #endregion
    Debug.Start("IntegrityCheck")

    #region ---- Step 0 -> Creating variables
    Debug.Log("Step 0 -> Creating variables")
    workingDirectory = os.getcwd()
    mainFolders = os.listdir(workingDirectory)
    ProgramsFolders = os.listdir(workingDirectory + "\\Programs")
    LocalFolders = os.listdir(workingDirectory + "\\Local")
    LibrariesFolders = os.listdir(workingDirectory + "\\Libraries")
    BrSpandFolders = os.listdir(workingDirectory + "\\BrSpand")
    IconFiles = os.listdir(workingDirectory + "\\Libraries\\Icons\\Logo")
    CacheFiles = os.listdir(workingDirectory + "\\Local\\Cache")
    LanguagePacksFolders = os.listdir(workingDirectory + "\\Local\\Languages\\locale")
    missingFilesList = []
    missingFiles = False

    def Temp_BatchCheck(filesFound,fileToFind:str,missingFilesList:list) -> bool:
        """
            Replaces copy pasted code.
            Checks if a file is within a list.
            If not, it adds it's name to a list of missing files.
        """
        if(fileToFind in filesFound):
            return False
        else:
            Debug.Error(f">>> Missing: {fileToFind}")
            missingFilesList.append(fileToFind + " ")
            return True
    #endregion
    #region ---- Step 1 -> Application's folder integrity
    Debug.Log("Step 1 -> Application's folder integrity")

    # Batch checking critical files
    if(Temp_BatchCheck(mainFolders,".git",missingFilesList)): missingFiles=True
    if(Temp_BatchCheck(mainFolders,".gitmodules",missingFilesList)): missingFiles=True
    if(Temp_BatchCheck(mainFolders,"Application.py",missingFilesList)): missingFiles=True
    if(Temp_BatchCheck(mainFolders,"BrSpand",missingFilesList)): missingFiles=True
    if(Temp_BatchCheck(mainFolders,"Libraries",missingFilesList)): missingFiles=True
    if(Temp_BatchCheck(mainFolders,"Local",missingFilesList)): missingFiles=True
    if(Temp_BatchCheck(mainFolders,"Programs",missingFilesList)): missingFiles=True

    # Generate error message
    if missingFiles:
        LoadingSteps[LoadingStepsEnum.IntegrityCheck][ParamEnum.ErrorType] = ErrorTypeEnum.Corruption
        LoadingSteps[LoadingStepsEnum.IntegrityCheck][ParamEnum.ErrorMessage] = _("Critical file(s)/folder(s) missing: ") + str(missingFilesList)
        Debug.Error(">>> Critical files missing. Aborting.")
        Debug.End()
        return True
    else:
        Debug.Log(">>> SUCCESS")
    #endregion
    #region ---- Step 2 -> BrSpand folder integrity
    Debug.Log("Step 2 -> BrSpand folder integrity")

    # Batch checking critical files
    if(Temp_BatchCheck(BrSpandFolders,"Drivers",missingFilesList)): missingFiles=True
    if(Temp_BatchCheck(BrSpandFolders,"Logs",missingFilesList)): missingFiles=True

    # Generate error message
    if missingFiles:
        LoadingSteps[LoadingStepsEnum.IntegrityCheck][ParamEnum.ErrorType] = ErrorTypeEnum.Corruption
        LoadingSteps[LoadingStepsEnum.IntegrityCheck][ParamEnum.ErrorMessage] = _("Critical BrSpand file(s)/folder(s) missing: ") + str(missingFilesList)
        Debug.Error(">>> Critical files missing. Aborting.")
        Debug.End()
        return True
    else:
        Debug.Log(">>> SUCCESS")
    #endregion
    #region ---- Step 3 -> Libraries folder integrity
    Debug.Log("Step 3 -> Libraries folder integrity")

    # Batch checking critical files
    if(Temp_BatchCheck(LibrariesFolders,"BRS_Python_Libraries",missingFilesList)): missingFiles=True
    if(Temp_BatchCheck(LibrariesFolders,"Icons",missingFilesList)): missingFiles=True

    # Generate error message
    if missingFiles:
        LoadingSteps[LoadingStepsEnum.IntegrityCheck][ParamEnum.ErrorType] = ErrorTypeEnum.Corruption
        LoadingSteps[LoadingStepsEnum.IntegrityCheck][ParamEnum.ErrorMessage] = _("Critical Libraries file(s)/folder(s) missing: ") + str(missingFilesList)
        Debug.Error(">>> Critical files missing. Aborting.")
        Debug.End()
        return True
    else:
        Debug.Log(">>> SUCCESS")
    #endregion
    #region ---- Step 4 -> Local folder integrity
    Debug.Log("Step 4 -> Local folder integrity")

    # Batch checking critical files
    if(Temp_BatchCheck(LocalFolders,"Cache",missingFilesList)): missingFiles=True
    if(Temp_BatchCheck(LocalFolders,"Drivers",missingFilesList)): missingFiles=True
    if(Temp_BatchCheck(LocalFolders,"Languages",missingFilesList)): missingFiles=True
    if(Temp_BatchCheck(LocalFolders,"Profiles",missingFilesList)): missingFiles=True

    # Generate error message
    if missingFiles:
        LoadingSteps[LoadingStepsEnum.IntegrityCheck][ParamEnum.ErrorType] = ErrorTypeEnum.Corruption
        LoadingSteps[LoadingStepsEnum.IntegrityCheck][ParamEnum.ErrorMessage] = _("Critical Local file(s)/folder(s) missing: ") + str(missingFilesList)
        Debug.Error(">>> Critical files missing. Aborting.")
        Debug.End()
        return True
    else:
        Debug.Log(">>> SUCCESS")
    #endregion
    #region ---- Step 5 -> Programs folder integrity
    Debug.Log("Step 5 -> Programs folder integrity")

    # Batch checking critical files
    if(Temp_BatchCheck(ProgramsFolders,"Pages",missingFilesList)): missingFiles=True
    if(Temp_BatchCheck(ProgramsFolders,"Local",missingFilesList)): missingFiles=True

    # Generate error message
    if missingFiles:
        LoadingSteps[LoadingStepsEnum.IntegrityCheck][ParamEnum.ErrorType] = ErrorTypeEnum.Corruption
        LoadingSteps[LoadingStepsEnum.IntegrityCheck][ParamEnum.ErrorMessage] = _("Critical Program file(s)/folder(s) missing: ") + str(missingFilesList)
        Debug.Error(">>> Critical files missing. Aborting.")
        Debug.End()
        return True
    else:
        Debug.Log(">>> SUCCESS")
    #endregion
    #region ---- Step 6 -> Icons integrity
    Debug.Log("Step 6 -> Icons integrity")

    # Batch checking critical files
    if(Temp_BatchCheck(IconFiles,"Black_BRS_B.png",missingFilesList)): missingFiles=True
    if(Temp_BatchCheck(IconFiles,"Black_BRS_R.png",missingFilesList)): missingFiles=True
    if(Temp_BatchCheck(IconFiles,"Black_BRS_S.png",missingFilesList)): missingFiles=True
    if(Temp_BatchCheck(IconFiles,"Black_BRS_K.png",missingFilesList)): missingFiles=True
    if(Temp_BatchCheck(IconFiles,"White_BRS_B.png",missingFilesList)): missingFiles=True
    if(Temp_BatchCheck(IconFiles,"White_BRS_R.png",missingFilesList)): missingFiles=True
    if(Temp_BatchCheck(IconFiles,"White_BRS_S.png",missingFilesList)): missingFiles=True
    if(Temp_BatchCheck(IconFiles,"White_BRS_K.png",missingFilesList)): missingFiles=True

    # Generate error message
    if missingFiles:
        LoadingSteps[LoadingStepsEnum.IntegrityCheck][ParamEnum.ErrorType] = ErrorTypeEnum.Warning
        LoadingSteps[LoadingStepsEnum.IntegrityCheck][ParamEnum.ErrorMessage] = _("Warning, some icons are missing: ") + str(missingFilesList)
        Debug.Warn(">>> Some icons are missing. Not critical to application's execution")
    else:
        Debug.Log(">>> SUCCESS")
    #endregion
    #region ---- Step 7 -> Checking Cache
    Debug.Log("Step 7 -> Checking Cache")
    missingFiles = False

    # Batch checking critical files
    if(Temp_BatchCheck(CacheFiles,"Cache.json",missingFilesList)): missingFiles=True

    # Generate error message
    if missingFiles:
        LoadingSteps[LoadingStepsEnum.IntegrityCheck][ParamEnum.ErrorType] = ErrorTypeEnum.Warning
        LoadingSteps[LoadingStepsEnum.IntegrityCheck][ParamEnum.ErrorMessage] = _("Warning, cache was not found. Parameters will not be saved when quitting.: ")
        Debug.Warn(">>> No cache was found.")
    else:
        Debug.Log(">>> SUCCESS")
    #endregion
    #region ---- Step 8 -> Checking Language packs
    Debug.Log("Step 7 -> Checking language packs")
    missingFiles = False

    # Batch checking critical files
    if(len(LanguagePacksFolders) == 0):
        Debug.Error(">>> No language packs can be found")
        LoadingSteps[LoadingStepsEnum.IntegrityCheck][ParamEnum.ErrorType] = ErrorTypeEnum.Warning
        LoadingSteps[LoadingStepsEnum.IntegrityCheck][ParamEnum.ErrorMessage] = _("No language packs found. The application will only work in default english.")
    else:
        Debug.Log(">>> SUCCESS")
    #endregion

    #region ---- Step 99 -> Handle execution ending
    Debug.Log("Step 99 -> Handle execution ending")

    if(LoadingSteps[LoadingStepsEnum.IntegrityCheck][ParamEnum.ErrorType] == ErrorTypeEnum.Default):
        LoadingSteps[LoadingStepsEnum.IntegrityCheck][ParamEnum.ErrorType] = ErrorTypeEnum.Success
        LoadingSteps[LoadingStepsEnum.IntegrityCheck][ParamEnum.ErrorMessage] = "Success"
        Debug.Log("Integrity check was successful")
        Debug.End()
        return False
    else:
        Debug.Warn("Integrity check needs to execute callback")
        Debug.End()
        return True
    #endregion
LoadingLog.Log("IntegrityCheck_CallBack")
def IntegrityCheck_CallBack() -> bool:
    """
        IntegrityCheck_CallBack:
        ------------------------
        This function is the error call back function of that specific
        loading step function. It's goal is to handle the `ErrorType`
        received and decide if the application can continue.

        It handles if other steps should be skipped, appends warning
        pop ups, error pop ups and so on.

        Returns:
            - `bool`: `True`: Application must be stopped. `False`: Application can continue
    """
    Debug.Start("IntegrityCheck_CallBack")

    # Check if function was executed
    if(LoadingSteps[LoadingStepsEnum.IntegrityCheck][ParamEnum.ErrorType] == ErrorTypeEnum.Default):
        Debug.Error("Callback executed while error type is default.")
        PopUpsHandler.Add(PopUpTypeEnum.FatalError, "alert-octagon", _("Fatal loading error"), False)
        Debug.End()
        return True
    else:
        if(LoadingSteps[LoadingStepsEnum.IntegrityCheck][ParamEnum.ErrorType] == ErrorTypeEnum.Warning):
            Debug.Warn("Some things were not right. Appending warning windows for future display")
            PopUpsHandler.Add(PopUpTypeEnum.Warning, "alert", LoadingSteps[LoadingStepsEnum.IntegrityCheck][ParamEnum.ErrorMessage], False)
            Debug.End()
            return False

        if(LoadingSteps[LoadingStepsEnum.IntegrityCheck][ParamEnum.ErrorType] == ErrorTypeEnum.Corruption):
            Debug.Error("Something corrupted. Application is not safe to use.")
            PopUpsHandler.Add(PopUpTypeEnum.FatalError, "file-hidden", LoadingSteps[LoadingStepsEnum.IntegrityCheck][ParamEnum.ErrorMessage], False)
            Debug.End()
            return True

        if(LoadingSteps[LoadingStepsEnum.IntegrityCheck][ParamEnum.ErrorType] == ErrorTypeEnum.CriticalError):
            Debug.Error("Critical Fatal error happened. Application cannot safely continue")
            PopUpsHandler.Add(PopUpTypeEnum.FatalError, "alert-octagon", LoadingSteps[LoadingStepsEnum.IntegrityCheck][ParamEnum.ErrorMessage], False)
            Debug.End()
            return True

    Debug.Log("Callback was called for no reasons.")
    Debug.End()
#--------------------------------------------------------------------#
LoadingLog.Log("InternetCheck")
def InternetCheck() -> bool:
    #region ---- DocString
    """
        InternetCheck:
        ---------------
        This loading step function check's if Kontrol has access to
        the internet.
        
        Returns:
            `bool`: `True`: Error occured. `False`: Internet can be reached
    """
    #endregion
    Debug.Start("InternetCheck")
    if(IsWebsiteOnline()):
        LoadingSteps[LoadingStepsEnum.InternetCheck][ParamEnum.ErrorType] = ErrorTypeEnum.NoConnection
        LoadingSteps[LoadingStepsEnum.InternetCheck][ParamEnum.ErrorMessage] = _("Failed to verify internet connection.")
        Debug.Error(">>> Internet connection failed to be verified.")
        Debug.End()
        return True
    else:
        Debug.Log(">>> SUCCESS")
        LoadingSteps[LoadingStepsEnum.InternetCheck][ParamEnum.ErrorType] = ErrorTypeEnum.Success
        LoadingSteps[LoadingStepsEnum.InternetCheck][ParamEnum.ErrorMessage] = _("Good")
        return False
LoadingLog.Log("IntegrityCheck_CallBack")
def InternetCheck_CallBack() -> bool:
    """
        IntegrityCheck_CallBack:
        ------------------------
        This function is the error call back function of that specific
        loading step function. It's goal is to handle the `ErrorType`
        received and decide if the application can continue.

        It handles if other steps should be skipped, appends warning
        pop ups, error pop ups and so on.

        Returns:
            - `bool`: `True`: Application must be stopped. `False`: Application can continue
    """
    Debug.Start("InternetCheck_CallBack")

    # Check if function was executed
    if(LoadingSteps[LoadingStepsEnum.InternetCheck][ParamEnum.ErrorType] == ErrorTypeEnum.Default):
        Debug.Error("Callback executed while error type is default. Function needs to be executed prior to callback")
        PopUpsHandler.Add(PopUpTypeEnum.FatalError, "alert-octagon", _("Fatal loading error"), True)
        Debug.End()
        return True
    else:
        if(LoadingSteps[LoadingStepsEnum.IntegrityCheck][ParamEnum.ErrorType] == ErrorTypeEnum.Warning):
            Debug.Warn("Some things were not right. Appending warning windows for future display")
            PopUpsHandler.Add(PopUpTypeEnum.Warning, "alert", LoadingSteps[LoadingStepsEnum.InternetCheck][ParamEnum.ErrorMessage], True)
            Debug.End()
            return False

        if(LoadingSteps[LoadingStepsEnum.IntegrityCheck][ParamEnum.ErrorType] == ErrorTypeEnum.CriticalError):
            Debug.Error("Critical Fatal error happened. Application cannot safely continue")
            PopUpsHandler.Add(PopUpTypeEnum.FatalError, "alert-octagon", LoadingSteps[LoadingStepsEnum.InternetCheck][ParamEnum.ErrorMessage], True)
            Debug.End()
            return True

        if(LoadingSteps[LoadingStepsEnum.IntegrityCheck][ParamEnum.ErrorType] == ErrorTypeEnum.NoConnection):
            Debug.Error("No internet connection could be found. GitHub checks will be skipped.")
            LoadingSteps[LoadingStepsEnum.GitHubCheck][ParamEnum.Skip] = True
            LoadingSteps[LoadingStepsEnum.KontrolGitHub][ParamEnum.Skip] = True
            LoadingSteps[LoadingStepsEnum.BrSpandGitHub][ParamEnum.Skip] = True
            LoadingSteps[LoadingStepsEnum.DriversGitHub][ParamEnum.Skip] = True
            PopUpsHandler.Add(PopUpTypeEnum.Remark, "wifi-off", LoadingSteps[LoadingStepsEnum.InternetCheck][ParamEnum.ErrorMessage], True)
            Debug.End()
            return True

    Debug.Log("Callback was called for no reasons.")
    Debug.End()
#====================================================================#
# Main Function
#====================================================================#
LoadingLog.Log("LoadApplication")
def LoadApplication(updateFunction, setMaxFunction) -> bool:
    """
        LoadApplication:
        ================
        The function which loads all the loading steps one by one,
        handling errors and callbacks of each individual steps as well
        as screen updates.

        Parameters:
        -----------
        - `updateFunction`: function that updates the loading widget.
        Need to have 2 input parameters. First one being a string and second being a integer.
        The string will be used to display the loading message while the integer is used to update the loading bar.
        - `setMaxFunction`: Function that sets how many total steps needs
        to be executed before the loading is finished. Needs 1 int input parameter.

        Returns:
        --------
        The function will return a `bool` value which if `True`,
        an error occured which prevents the application from loading
        at all. If `False`, the application can be executed.

        Notes:
        ------
        After having called this, there is potentially some warning
        or error screens that needs to be displayed to the user.
    """
    Debug.Start("LoadApplication")
    Debug.Log("Setting max loading steps")
    setMaxFunction(len(LoadingSteps))
    count:dict = {0:0.0}
    delay = 0

    for step in LoadingSteps.items():
        delay=delay+1
        Clock.schedule_once(partial(ExecuteStep,updateFunction,step,count),0)
    Debug.End()

def ExecuteStep(updateFunction,step, count:dict, *args):
    step = step[1]
    Debug.Log(f"{step[ParamEnum.DisplayName]}")

    # Update screen with new loading message
    if(step[ParamEnum.Skip]):
        updateFunction(_("Skipped"), count[0])
    else:
        updateFunction(step[ParamEnum.DisplayName], count[0])

        # Execute the loading step functions and callbacks
        if(step[ParamEnum.Function] != None):
            if(step[ParamEnum.Function]()):
                Debug.Log("Function returned an error. Calling callback.")
                if(step[ParamEnum.ErrorCallBackFunction] != None):
                    if(step[ParamEnum.ErrorCallBackFunction]()):
                        Debug.Log("-------------------------------------------------")
                        Debug.Error("Application cannot continue executing.")
                        Debug.Log("-------------------------------------------------")
                    else:
                        Debug.Log("Application can continue safely.")
                else:
                    Debug.Error("NO CALLBACK FUNCTION FOUND")
            else:
                Debug.Log("COMPLETE SUCCESS")
        else:
            Debug.Error("No loading step function to execute.")

        # Increase loading wheel count and update loading wheel
    count[0] = count[0] + 1.0
    updateFunction(step[ParamEnum.DisplayName], count[0])
#====================================================================#
# Loading steps
#====================================================================#
LoadingLog.Log("LoadingSteps")
LoadingSteps = {
    LoadingStepsEnum.IntegrityCheck : {
        ParamEnum.DisplayName : "Checking self integrity",
        ParamEnum.ErrorMessage : "Not done",
        ParamEnum.ErrorType : ErrorTypeEnum.Default,
        ParamEnum.ErrorCallBackFunction : IntegrityCheck_CallBack,
        ParamEnum.Function : IntegrityCheck,
        ParamEnum.Skip : False,
    },
    LoadingStepsEnum.EnvironementGathering : {
        ParamEnum.DisplayName : "Gathering system information",
        ParamEnum.ErrorMessage : "Not done",
        ParamEnum.ErrorType : ErrorTypeEnum.Default,
        ParamEnum.ErrorCallBackFunction : None,
        ParamEnum.Function : None,
        ParamEnum.Skip : False,
    },
    LoadingStepsEnum.InternetCheck : {
        ParamEnum.DisplayName : "Checking internet connection",
        ParamEnum.ErrorMessage : "Not done",
        ParamEnum.ErrorType : ErrorTypeEnum.Default,
        ParamEnum.ErrorCallBackFunction : InternetCheck_CallBack,
        ParamEnum.Function : InternetCheck,
        ParamEnum.Skip : False,
    },
    LoadingStepsEnum.GitHubCheck : {
        ParamEnum.DisplayName : "Connecting to GitHub's API",
        ParamEnum.ErrorMessage : "Not done",
        ParamEnum.ErrorType : ErrorTypeEnum.Default,
        ParamEnum.ErrorCallBackFunction : None,
        ParamEnum.Function : None,
        ParamEnum.Skip : False,
    },
    LoadingStepsEnum.DriversCheck : {
        ParamEnum.DisplayName : "Checking available Kontrol drivers",
        ParamEnum.ErrorMessage : "Not done",
        ParamEnum.ErrorType : ErrorTypeEnum.Default,
        ParamEnum.ErrorCallBackFunction : None,
        ParamEnum.Function : None,
        ParamEnum.Skip : False,
    },
    LoadingStepsEnum.BrSpandCheck : {
        ParamEnum.DisplayName : "Checking available BrSpand drivers",
        ParamEnum.ErrorMessage : "Not done",
        ParamEnum.ErrorType : ErrorTypeEnum.Default,
        ParamEnum.ErrorCallBackFunction : None,
        ParamEnum.Function : None,
        ParamEnum.Skip : False,
    },
    LoadingStepsEnum.KontrolGitHub : {
        ParamEnum.DisplayName : "Checking Kontrol's version",
        ParamEnum.ErrorMessage : "Not done",
        ParamEnum.ErrorType : ErrorTypeEnum.Default,
        ParamEnum.ErrorCallBackFunction : None,
        ParamEnum.Function : None,
        ParamEnum.Skip : False,
    },
    LoadingStepsEnum.DriversGitHub : {
        ParamEnum.DisplayName : "Checking Drivers versions",
        ParamEnum.ErrorMessage : "Not done",
        ParamEnum.ErrorType : ErrorTypeEnum.Default,
        ParamEnum.ErrorCallBackFunction : None,
        ParamEnum.Function : None,
        ParamEnum.Skip : False,
    },
    LoadingStepsEnum.BrSpandGitHub : {
        ParamEnum.DisplayName : "Checking BrSpand drivers versions",
        ParamEnum.ErrorMessage : "Not done",
        ParamEnum.ErrorType : ErrorTypeEnum.Default,
        ParamEnum.ErrorCallBackFunction : None,
        ParamEnum.Function : None,
        ParamEnum.Skip : False,
    },
}
"""
    LoadingSteps:
    =============
    This dictionary contains all Kontrol's application loading steps
    as well as their functions, loading names and other parameters.

    - Loading steps can be found listed in their enumerations: 
    :ref:`LoadingStepsEnum`.
    - Step parameters can be found listed in their enumerations:
    :ref:`ParamEnum`.
"""
#====================================================================#
LoadingLog.End("AppLoadingHandler.py")