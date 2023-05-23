#====================================================================#
# File Information
#====================================================================#
"""
    driver.py
    =========
    Summary:
    --------
    This file contains the high level classes and functions made to
    interface an on board addon card such as an Accelerometer.
"""
#====================================================================#
# Loading Logs
#====================================================================#
from token import EXACT_TOKEN_TYPES
from Libraries.BRS_Python_Libraries.BRS.Debug.LoadingLog import LoadingLog
LoadingLog.Start("driver.py")
#====================================================================#
# Imports
#====================================================================#
#region ------------------------------------------------------ Python
LoadingLog.Import("Python")
import os
#endregion
#region --------------------------------------------------------- BRS
LoadingLog.Import("Libraries")
# from ...Utilities.Information import Information
# from ...Utilities.FileHandler import JSONdata, CompareKeys, AppendPath
from Libraries.BRS_Python_Libraries.BRS.Utilities.Enums import Execution
from Libraries.BRS_Python_Libraries.BRS.Utilities.Information import Information
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
from Libraries.BRS_Python_Libraries.BRS.Hardware.Accelerometer.ADXL343 import ADXL343
from Libraries.BRS_Python_Libraries.BRS.Utilities.FileHandler import JSONdata, AppendPath
from Libraries.BRS_Python_Libraries.BRS.Utilities.addons import AddonFoundations, AddonInfoHandler, AddonEnum
from Libraries.BRS_Python_Libraries.BRS.PnP.controls import Controls
#endregion
#region -------------------------------------------------------- Kivy
# LoadingLog.Import("Kivy")
#endregion
#region ------------------------------------------------------ KivyMD
# LoadingLog.Import('KivyMD')
#endregion
#====================================================================#
# Variables
#====================================================================#
_EmptyJsonStructure:dict = {
    "version" : 0.1,
    "name" : "Accelerometer",
    "saved-profiles" : {

    }
}

hardwareControlsTemplate:dict = {
                        "axes" : { 
                                "x-positive" : {  "binded" : False, 
                                                  "bindedTo" : None,
                                                  "getter" : ADXL343.GetValue_X_Positive},
                                "x-negative" : { "binded" : False, 
                                                 "bindedTo" : None,
                                                 "getter" : ADXL343.GetValue_X_Negative},
                                "y-positive" : {  "binded" : False, 
                                                  "bindedTo" : None,
                                                  "getter" : ADXL343.GetValue_Y_Positive},
                                "y-negative" : { "binded" : False, 
                                                  "bindedTo" : None,
                                                  "getter" : ADXL343.GetValue_Y_Negative},
                                "z-positive" : { "binded" : False, 
                                                  "bindedTo" : None,
                                                  "getter" : ADXL343.GetValue_Z_Positive},
                                "z-negative" : { "binded" : False, 
                                                  "bindedTo" : None,
                                                  "getter" : ADXL343.GetValue_Z_Negative}
                        }
}

profileExample = {
    "hardware" : {
                    "axes" : { 
                                "x-positive" : {  "binded" : False, 
                                                  "bindedTo" : None,
                                                  "getter" : None},
                                "x-negative" : { "binded" : False, 
                                                 "bindedTo" : None,
                                                 "getter" : None},
                                "y-positive" : {  "binded" : False, 
                                                  "bindedTo" : None,
                                                  "getter" : None},
                                "y-negative" : { "binded" : False, 
                                                  "bindedTo" : None,
                                                  "getter" : None},
                                "z-positive" : { "binded" : False, 
                                                  "bindedTo" : None,
                                                  "getter" : None},
                                "z-negative" : { "binded" : False, 
                                                  "bindedTo" : None,
                                                  "getter" : None}
                            },
                    "buttons" : {
                    } 
    },
    "actions" : {

    }
}

#====================================================================#
# Classes
#====================================================================#
class Accelerometer(AddonFoundations):
    #region   --------------------------- DOCSTRING
    """
        Accelerometer:
        ==============
        Summary:
        --------
        This class handles the backend of trying
        to interface an accelerometer addon card
        with the Raspberry Pi.
    """
    #endregion
    #region   --------------------------- MEMBERS
    profileData:JSONdata = None

    hardwareControls:dict = {
        "axes" : {
                    "x-positive" : {  "binded" : False,
                                     "bindedTo" : None,
                                     "getter" : ADXL343.GetValue_X_Positive},
                    "x-negative" : { "binded" : False,
                                     "bindedTo" : None,
                                     "getter" : ADXL343.GetValue_X_Negative},
                    "y-positive" : {  "binded" : False,
                                     "bindedTo" : None,
                                     "getter" : ADXL343.GetValue_Y_Positive},
                    "y-negative" : { "binded" : False,
                                     "bindedTo" : None,
                                     "getter" : ADXL343.GetValue_Y_Negative},
                    "z-positive" : { "binded" : False,
                                     "bindedTo" : None,
                                     "getter" : ADXL343.GetValue_Z_Positive},
                    "z-negative" : { "binded" : False,
                                     "bindedTo" : None,
                                     "getter" : ADXL343.GetValue_Z_Negative}
                 }
    }

    loadedProfileName:str = None

    addonInformation:AddonInfoHandler = None
    #endregion
    #region   --------------------------- METHODS
    #region ----------------------- ADDON
    def Launch() -> Execution:
        """
            Launch:
            =======
            Summary:
            --------
            Launches the accelerometer addon.
            returns Execution to indicate how
            the launch went.

            Returns:
            --------
            - `Execution.Passed` = Addon was launched.
            - `Execution.Failed` = Error occured
            - `Execution.Incompatibility` = Failed to verify for compatibility.
        """
        Debug.Start("Launch")

        Debug.Log("Creating AddonInfoHandler")
        Accelerometer.addonInformation = AddonInfoHandler(
            "Accelerometer",
            "ADXL343 on board accelerometer hardware extension.",
            "0.0.1",
            "hardware",
            None,
            False,
            True,
            False,
            False,
            "integrated-circuit-chip",
            Accelerometer.Launch,
            Accelerometer.Stop,
            Accelerometer.Uninstall,
            Accelerometer.Update,
            Accelerometer.GetState,
            Accelerometer.ClearProfile,
            Accelerometer.SaveProfile,
            Accelerometer.ChangeProfile,
            Accelerometer.LoadProfile,
            Accelerometer.UnloadProfile,
            Accelerometer.PeriodicCallback,
            Accelerometer.GetAllHardwareControls,
            Accelerometer.GetAllSoftwareActions,
            Accelerometer.ChangeButtonActionBinding,
            Accelerometer.ChangeAxisBinding,
            Accelerometer.UnbindButtonBinding,
            Accelerometer.UnbindAxisBinding,
            Accelerometer.ChangeButtonActionBinding,
            Accelerometer.ChangeAxisActionBinding
        )

        result = Accelerometer.VerifyForExecution()
        if(result != Execution.Passed):
            Debug.Error("The addon cannot run on your device.")
            Debug.Log("Adding addon to application...")
            Accelerometer.addonInformation.DockAddonToApplication(False)
            Debug.End()
            return result

        result = ADXL343.StartDriver()
        if(result != Execution.Passed):
            Debug.Error("Failed to start backend driver ADXl343")
            Accelerometer.addonInformation.DockAddonToApplication(False)
            Debug.End()
            return Execution.Failed

        Debug.Log("Addon started successfully.")
        Debug.Log("Adding addon to application...")
        Accelerometer.addonInformation.DockAddonToApplication(True)
        Accelerometer.state = True
        Debug.End()
        return Execution.Passed
    # -----------------------------------
    def Stop() -> Execution:
        """
            Stop:
            ==========
            Summary:
            --------
            Stops the addon from running.
            Closes the thread that is running it.
            Gone, reduced to atoms.
            Oh, and it unbinds stuff too.
        """
        Debug.Start("Stop")

        if(Accelerometer.state == True):
            Debug.Log("Stopping ADXL343")
            result = ADXL343.StopDriver()
            if(result != Execution.Passed):
                Debug.Error("Error when trying to stop ADXL343")
                Debug.End()
                return Execution.Failed
            Debug.Log("ADXL343 is now OFF")
            Accelerometer.profileData.SaveFile()
            Debug.End()
            return Execution.Passed
        else:
            Debug.Log("Unecessary. ADXL343 is not running.")
            Debug.End()
            return Execution.Unecessary
    # -----------------------------------
    def GetAllHardwareControls() -> Execution:
        """
            GetAllHardwareControls:
            =======================
            Summary:
            --------
            Returns a dictionary of all
            the current hardware controls
            of this addon.

            Returns:
            --------
            - `Execution.Failed` = Something fucked up.
            - `dict` see :ref:`hardwareControls`
        """
        if(Accelerometer.state == True):
            Debug.Start("Accelerometer -> GetAllHardwareControls")
            Debug.End()
            return Accelerometer.hardwareControls
        else:
            Debug.Log("Unecessary. ADXL343 is not running.")
            Debug.End()
            return Execution.ByPassed
    # -----------------------------------
    def LoadProfile(profileToLoad: str) -> Execution:
        """
            LoadProfile:
            ============
            Summary:
            --------
            This function loads a profile
            saved in the JSONs of this addon.
            if no profiles are found with this
            name, default values are loaded
            and the profile is created.
        """
        Debug.Start("Accelerometer -> LoadProfile")

        if(Accelerometer.state == True):
            Debug.Log(f"Trying to load {profileToLoad} from Profiles.json")

            try:
                profile = Accelerometer.profileData.jsonData["saved-profiles"][profileToLoad]
                Debug.Log(f"{profileToLoad} was found in the JSON.")
            except:
                Debug.Log(f"{profileToLoad} doesn't exist in the JSON... Creating it.")
                Accelerometer._AddNewProfile(profileToLoad)

                Debug.Log("Saving JSON file...")
                saved = Accelerometer.profileData.SaveFile()
                if(not saved):
                    Debug.Error("Failed to save JSON file...")
                    Debug.End()
                    return Execution.Failed
                Debug.Log("Success")
                profile = Accelerometer.profileData.jsonData["saved-profiles"][profileToLoad]

            Debug.Log(f"Loading {profileToLoad}'s data.")
            Accelerometer.loadedProfileName = profileToLoad
            result = Accelerometer._LoadProfileBindsInApplication()
            if(result != Execution.Passed):
                Debug.Error(f"Failed to keybinds of {Accelerometer.loadedProfileName} into the Controls class.")
                Debug.End()
                return result
            
            Debug.Log("Profile loaded in successfully.")
            Debug.End()
            return Execution.Passed
        else:
            Debug.Warn("Accelerometer is not running.")
            Debug.End()
            return Execution.ByPassed
    # -----------------------------------
    def UnloadProfile(profileToUnload: str) -> Execution:
        """
            UnloadProfile:
            ============
            Summary:
            --------
            Unloads a specified profile from
            the addon. This does not turn off
            the addon.

            Usually used when someone is logging
            out of their profiles.
        """
        Debug.Start("Accelerometer -> UnloadProfile")

        if(Accelerometer.state == True):
            Debug.Log(f"Unloading the current profile.")
            result = Accelerometer._UnbindEverything()
            if(result != Execution.Passed):
                Debug.Error(f"_UnbindEverything returned error code: {result}")
                Debug.End()
                return result

            Debug.Log("Clearing saved profile's name.")
            Accelerometer.loadedProfileName = None
        else:
            Debug.Warn("Accelerometer is not running.")
            Debug.End()
            return Execution.ByPassed
    # -----------------------------------
    def SaveProfile(profileToSave: str = None) -> Execution:
        """
            SaveProfile:
            ============
            Summary:
            --------
            Attempts to save either the
            currently loaded profile, or
            a specific profile with the
            currently loaded informations.
        """
        Debug.Start("SaveProfile")

        if(Accelerometer.state == True):
            if(Accelerometer.loadedProfileName == None and profileToSave == None):
                Debug.Error("No profiles were loaded in the class.")
                Debug.End()
                return Execution.Failed

            if(profileToSave == None):
                Debug.Log("Saving loaded profile.")
                profileToSave = Accelerometer.loadedProfileName

            existing = Accelerometer._DoesProfileExist(profileToSave)
            if(not existing):
                Debug.Log(f"{profileToSave} does not exist. Creating it.")
                Accelerometer._AddNewProfile(profileToSave)
                Accelerometer._PutBindsInProfile(profileToSave)
            else:
                Debug.Log(f"Putting live binds in {profileToSave}")
                Accelerometer._PutBindsInProfile(profileToSave)

            saved = Accelerometer.profileData.SaveFile()
            if(not saved):
                Debug.Error("Saving failed.")
                Debug.End()
                return Execution.Failed

            Debug.Log(">>> SUCCESS")
            Debug.End()
            return Execution.Passed
        else:
            Debug.Log("Unecessary. ADXL343 is not running.")
            Debug.End()
            return Execution.ByPassed
    # -----------------------------------
    def ClearProfile(profileToClear: str) -> Execution:
        """
            ClearProfile:
            =============
            Summary:
            --------
            Attempts to clear a given profile
            from the cache of this addon.
        """
        Debug.Start("ClearProfile")
        if(Accelerometer.profileData.jsonData == None):
            Debug.Error("No json is loaded. Accelerometer cannot delete anything.")
            Debug.End()
            return Execution.ByPassed

        existing = Accelerometer._DoesProfileExist(profileToClear)
        if(not existing):
            Debug.Warn(f"Accelerometer has no cached data for {profileToClear}")
            Debug.End()
            return Execution.Unecessary

        savedProfiles:dict = Accelerometer.profileData.jsonData["saved-profiles"]
        savedProfiles.pop(profileToClear)
        Debug.Log(f"{profileToClear} no longer exists in Accelerometer's cached profiles.")
        Accelerometer.profileData.jsonData["saved-profiles"] = savedProfiles
        Accelerometer.profileData.SaveFile()
        Debug.End()
        return Execution.Passed
    # -----------------------------------
    def ChangeAxisBinding(nameOfSoftwareAxis: str, nameOfHardwareAxis: str) -> Execution:
        """
            ChangeAxisBinding:
            ==================
            Summary:
            --------
            This method attempts to firstly
            un-bind anything binded to
            :ref:`nameOfHardwareAxis` then
            tries to bind it to :ref:`nameOfSoftwareAxis`

            Arguments:
            ----------
            - `nameOfSoftwareAxis` : Axis taken from SoftwareAxis in controls.py
            - `nameOfHardwareAxis` : Hardware axis to bind to :ref:`nameOfSoftwareAxis`
        """
        Debug.Start(AddonEnum.ChangeAxisBinding)

        if(Accelerometer.state == True):
            result = Accelerometer.UnbindAxisBinding(nameOfSoftwareAxis)
            if(result != Execution.Passed and result != Execution.Unecessary):
                Debug.Error(f"Failed to unbind software axis: {nameOfSoftwareAxis}")
                Debug.End()
                return Execution.Failed

            result = Accelerometer._UnbindHardwareAxis(nameOfHardwareAxis)
            if(result != Execution.Passed and result != Execution.Unecessary):
                Debug.Error(f"Failed to unbind hardware axis: {nameOfHardwareAxis}")
                Debug.End()
                return Execution.Failed

            Debug.Log(f"The accelerometer no longer holds bindings for the software axis: {nameOfSoftwareAxis} as well as the hardware axis: {nameOfHardwareAxis}")

            result = Accelerometer._BindAxis(nameOfSoftwareAxis, nameOfHardwareAxis)
            if(result != Execution.Passed):
                Debug.Error(f"Something went wrong when trying to bind {nameOfHardwareAxis} to {nameOfSoftwareAxis}")
                Debug.End()
                return result

            Debug.Log(f"Saving {Accelerometer.loadedProfileName}'s new binds.")
            Accelerometer._PutBindsInProfile(Accelerometer.loadedProfileName)

            saved = Accelerometer.profileData.SaveFile()
            if(not saved):
                Debug.Log("Failed to save Profile.json")
                Debug.End()
                return Execution.Crashed

            Debug.Log(">>> Success")
            Debug.End()
            return Execution.Passed
        else:
            Debug.Log("Unecessary. ADXL343 is not running.")
            Debug.End()
            return Execution.ByPassed
    # -----------------------------------
    def UnbindAxisBinding(nameOfSoftwareAxis:str) -> Execution:
        """
            UnbindAxisBinding:
            ==================
            Summary:
            --------
            This method attempts to
            un-bind anything binded to
            :ref:`nameOfSoftwareAxis`.

            Arguments:
            ----------
            - `nameOfSoftwareAxis` : Axis taken from SoftwareAxis in controls.py that needs to be unbinded.
        """
        Debug.Start(AddonEnum.UnbindAxisBinding)

        if(Accelerometer.state):
            whateverAxisHadItBinded = Accelerometer._WhoHasThatAxisBinded(nameOfSoftwareAxis)
            if(whateverAxisHadItBinded == Execution.Unecessary):
                Debug.Log(f"{nameOfSoftwareAxis} isn't currently binded by the Accelerometer.")
                Debug.End()
                return Execution.Unecessary

            result = Accelerometer._UnbindSoftwareAxis(nameOfSoftwareAxis, whateverAxisHadItBinded)
            if(result != Execution.Passed):
                Debug.Log(f"Error occured when unbinding {nameOfSoftwareAxis}. Return code: {result}")

            Debug.Log("Updating profile with new informations.")
            Accelerometer._PutBindsInProfile(Accelerometer.loadedProfileName)
            Accelerometer.profileData.SaveFile()
            Debug.Log(">>> Success")
            Debug.End()
            return Execution.Passed
        else:
            Debug.Warn("Accelerometer is not running.")
            Debug.End()
            return Execution.ByPassed
    #endregion
    #region --------------------- PRIVATE
    def _UnbindEverything():
        """
            _UnbindEverything:
            ===================
            Summary:
            --------
            This private method's goal is
            to unload all the binds as
            well as the current profile.
        """
        Debug.Start("_UnbindEverything")

        for hardwareAxis, data in Accelerometer.hardwareControls["axes"].items():
            Debug.Log(f"Unbinding {hardwareAxis} from the Accelerometer.")
            result = Accelerometer._UnbindHardwareAxis(hardwareAxis)
            if(result != Execution.Passed and result != Execution.Unecessary):
                Debug.Error(f"Fatal error occured when trying to unbind {hardwareAxis}. Return code: {result}")
                Debug.End()
                return Execution.Failed

        Debug.Log("Everything has been un-binded.")
        Debug.End()
        return Execution.Passed
    # -----------------------------------
    def _UnbindHardwareAxis(nameOfHardwareAxis:str):
        """
            _UnbindHardwareAxis:
            ============
            Summary:
            --------
            This method tries to unbind
            a given hardware axis both from
            local dictionaries as well as from
            the Controls class.
        """
        Debug.Start("_UnbindHardwareAxis")

        Debug.Log(f"Getting what is binded to {nameOfHardwareAxis}")
        whatItsBindedTo = Accelerometer.hardwareControls["axes"][nameOfHardwareAxis]["bindedTo"]
        if(whatItsBindedTo == None):
            Debug.Log(f"{nameOfHardwareAxis} isn't binded to any software axis.")
            Debug.End()
            return Execution.Passed

        Debug.Log(f"Unbinding {nameOfHardwareAxis} from {whatItsBindedTo}")
        result = Controls.UnbindAxis("Accelerometer", nameOfSoftwareAxis=whatItsBindedTo)
        if(result != Execution.Passed):
            Debug.Log(f"Failed to unbind {nameOfHardwareAxis} from {whatItsBindedTo}")
            Debug.End()
            return result

        Accelerometer.hardwareControls["axes"][nameOfHardwareAxis]["binded"] = False
        Accelerometer.hardwareControls["axes"][nameOfHardwareAxis]["bindedTo"] = None
        Debug.Log(f"{nameOfHardwareAxis} is now default values.")

        Debug.End()
        return Execution.Passed
    # -----------------------------------
    def _UnbindSoftwareAxis(nameOfSoftwareAxis:str, nameOfHardwareAxis:str):
        """
            _UnbindSoftwareAxis:
            ============
            Summary:
            --------
            This method tries to unbind
            a given hardware axis both from
            local dictionaries as well as from
            the Controls class.
        """
        Debug.Start("_UnbindSoftwareAxis")

        Debug.Log(f"Unbinding {nameOfHardwareAxis} from {nameOfSoftwareAxis} in the Controls class.")
        result = Controls.UnbindAxis("Accelerometer", nameOfSoftwareAxis=nameOfSoftwareAxis)
        if(result != Execution.Passed):
            Debug.Log(f"Failed to unbind {nameOfHardwareAxis} from {nameOfSoftwareAxis}")
            Debug.End()
            return result

        Accelerometer.hardwareControls["axes"][nameOfHardwareAxis]["binded"] = False
        Accelerometer.hardwareControls["axes"][nameOfHardwareAxis]["bindedTo"] = None
        Debug.Log(f"{nameOfHardwareAxis} is now default values.")

        Debug.End()
        return Execution.Passed
    # -----------------------------------
    def _BindAxis(nameOfSoftwareAxis:str, nameOfHardwareAxis:str):
        """
            _BindAxis:
            ============
            Summary:
            --------
            This method tries to bind
            a given hardware axis both from
            local dictionaries as well as from
            the Controls class.
        """
        Debug.Start("_BindAxis")

        Debug.Log(f"Binding {nameOfHardwareAxis} to {nameOfSoftwareAxis} in Controls class.")
        result = Controls.BindAxis("Accelerometer", nameOfSoftwareAxis, nameOfHardwareAxis, Accelerometer.hardwareControls["axes"][nameOfHardwareAxis]["getter"])
        if(result != Execution.Passed):
            Debug.Log(f"Failed to bind {nameOfHardwareAxis} to {nameOfSoftwareAxis} with error code: {result}")
            Debug.End()
            return result

        Accelerometer.hardwareControls["axes"][nameOfHardwareAxis]["binded"] = True
        Accelerometer.hardwareControls["axes"][nameOfHardwareAxis]["bindedTo"] = nameOfSoftwareAxis
        Debug.Log(f"{nameOfHardwareAxis} is now binded to {nameOfSoftwareAxis}.")

        Debug.End()
        return Execution.Passed
    # -----------------------------------
    def _WhoHasThatAxisBinded(nameOfSoftwareAxis:str):
        """
            _WhoHasThatAxisBinded:
            ======================
            Summary:
            --------
            Checks if any of the hardware
            axis binded that software axis.
            If so, the name of the hardware
            axis is returned.
        """
        Debug.Start("_WhoHasThatAxisBinded")

        for hardwareAxis, axisData in Accelerometer.hardwareControls["axes"].items():
            if(axisData["bindedTo"] == nameOfSoftwareAxis):
                Debug.Log(f"{nameOfSoftwareAxis} is binded to {hardwareAxis}")
                Debug.End()
                return hardwareAxis

        Debug.Log(f"No axis has {nameOfSoftwareAxis} binded to them.")
        Debug.End()
        return Execution.Unecessary
    # -----------------------------------
    def _InitializeProfileJson() -> Execution:
        """
            _InitializeProfileJson:
            =======================
            Summary:
            --------
            Attempts to load a JSON at a specific
            path or creates it if it doesn't exist.
        """
        Debug.Start("_InitializeProfileJson")

        path = os.getcwd()
        path = AppendPath(path, "/Local/Hardware/Accelerometer/")

        Accelerometer.profileData = JSONdata("Profiles", path)
        if(Accelerometer.profileData.jsonData == None):
            Debug.Warn("No profile json file found for Accelerometer")
            Accelerometer.profileData.CreateFile(_EmptyJsonStructure)
            Accelerometer.profileData = JSONdata("Profiles", path)
            if(Accelerometer.profileData.jsonData == None):
                Debug.Error("Failed to create and load JSON after second attempt.")
                Debug.End()
                return Execution.Failed
            Debug.Log("New JSON created.")
        Debug.End()
        return Execution.Passed
    # -----------------------------------
    def _LoadProfileBindsInApplication() -> Execution:
        """
            _LoadProfileBindsInApplication:
            ===============================
            Summary:
            --------
            Loads a profile's saved hardware binds
            into the application's Controls class.

            Will return errors if some could not be
            loaded.

            Will update the hardwareControl dictionary
            of this class with what could be loaded
            and what couldn't.
        """ 
        Debug.Start("_LoadProfileBindsInApplication")

        if(Accelerometer.loadedProfileName == None):
            Debug.Error("saved profile name is None. Something fucked up.")
            Debug.End()
            return Execution.Failed

        profile = Accelerometer.profileData.jsonData["saved-profiles"][Accelerometer.loadedProfileName]
        hardwareAxes = profile["hardware"]["axes"]

        for hardwareAxis, data in hardwareAxes.items():
            Debug.Log(f"Loading {hardwareAxis}...")

            if(data["bindedTo"] == None):
                Debug.Log(">>> SKIPPED: not specified.")
            else:
                bindedTo = data["bindedTo"]
                getter = data["getter"]

                result = Controls.BindAxis("Accelerometer", bindedTo, hardwareAxis, getter)
                if(result != Execution.Passed):
                    Debug.Warn(f"Failed to bind {hardwareAxis} to {bindedTo} as Kontrol")
                    Accelerometer.hardwareControls["axes"][hardwareAxis]["binded"] = False,
                    Accelerometer.hardwareControls["axes"][hardwareAxis]["bindedTo"] = None
                else:
                    Accelerometer.hardwareControls["axes"][hardwareAxis]["binded"] = True,
                    Accelerometer.hardwareControls["axes"][hardwareAxis]["bindedTo"] = bindedTo

        Debug.End()
        return Execution.Passed
    # -----------------------------------
    def _AddNewProfile(nameOfProfile) -> Execution:
        """
            _AddNewProfile:
            ===============
            Adds a new profile to the JSON data.
            Does not save it tho.
        """
        Debug.Start("_AddNewProfile")
        Accelerometer.profileData.jsonData["saved-profiles"][nameOfProfile] = profileExample
        Debug.Log(f"Default parameters set for {nameOfProfile}")
        Debug.End()
        return Execution.Passed
    # -----------------------------------
    def _DoesProfileExist(nameOfProfile) -> bool:
        """
            _DoesProfileExist:
            ===============
            tells you if a profile exist in that JSON file.
        """
        Debug.Start("_DoesProfileExist")

        profiles = Accelerometer.profileData.jsonData["saved-profiles"]

        if nameOfProfile in profiles:
            Debug.Log(f"{nameOfProfile} is already in the JSON")
            Debug.End()
            return True
        else:
            Debug.Log(f"{nameOfProfile} is not in the JSON")
            Debug.End()
            return False
    # -----------------------------------
    def _PutBindsInProfile(profileToSaveBinds:str):
        """
            _PutBindsInProfile:
            ===================
            Summary:
            --------
            Function that puts the current hardwarecontrol
            binds into a specified profile.

            Does not check if it exists.
        """
        Debug.Start("_PutBindsInProfile")
        Debug.Log(f"Updating {profileToSaveBinds}'s bindings")
        for axis in Accelerometer.profileData.jsonData["saved-profiles"][profileToSaveBinds]["hardware"]["axes"]:
            Accelerometer.profileData.jsonData["saved-profiles"][profileToSaveBinds]["hardware"]["axes"][axis]["binded"] = Accelerometer.hardwareControls["axes"][axis]["binded"]
            Accelerometer.profileData.jsonData["saved-profiles"][profileToSaveBinds]["hardware"]["axes"][axis]["bindedTo"] = Accelerometer.hardwareControls["axes"][axis]["bindedTo"]
        Debug.End()
    # -----------------------------------
    def VerifyForExecution() -> Execution:
        """
            VerifyForExecution:
            ===================
            Summary:
            --------
            Function that returns Execution.Passed
            if the hardware and software allows
            ADXL343 to interface with Kontrol.
            Otherwise, Execution.Failed is returned.
        """
        Debug.Start("VerifyHardware")

        if(not Information.initialized):
            Debug.Error("Information class is not initialized")
            Debug.End()
            return Execution.Failed

        # if(Information.platform != "Linux"):
            # Debug.Error("This addon only works on Linux.")
            # Debug.End()
            # return Execution.Incompatibility

        result = Accelerometer._InitializeProfileJson()
        if(result != Execution.Passed):
            Debug.Error("JSON could not be created and loaded.")
            Debug.End()
            return Execution.Failed

        Debug.Log("Seems alright.")
        Debug.End()
        return Execution.Passed
    #endregion
    #endregion
    #region   --------------------------- CONSTRUCTOR
    #endregion
    pass
#====================================================================#
LoadingLog.End("driver.py")