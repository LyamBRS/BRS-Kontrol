#====================================================================#
# File Information
#====================================================================#
"""
    RGB.py
    =============
    This file includes a class used throughout Kontrol that interfaces
    with the Neopixel driver class to display the lit up BRS logo.
"""
#====================================================================#
# Loading Logs
#====================================================================#
from Libraries.BRS_Python_Libraries.BRS.Debug.LoadingLog import LoadingLog
LoadingLog.Start("AppLoading.py")
#====================================================================#
# Imports
#====================================================================#
#region ------------------------------------------------------ Python
LoadingLog.Import("Python")
#endregion
#region --------------------------------------------------------- BRS
LoadingLog.Import("Libraries")
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
from Libraries.BRS_Python_Libraries.BRS.Hardware.Neopixel.rgbDriverHandler import RGB, RGBModes
from Libraries.BRS_Python_Libraries.BRS.Utilities.Enums import Execution
from Libraries.BRS_Python_Libraries.BRS.GUI.Utilities.colors import GetAccentColor
#endregion
#region -------------------------------------------------------- Kivy
LoadingLog.Import("Kivy")
#endregion
#region ------------------------------------------------------ KivyMD
LoadingLog.Import('KivyMD')
#endregion
#====================================================================#
# Functions
#====================================================================#

#====================================================================#
# Classes
#====================================================================#
class KontrolRGB:
    #region   --------------------------- DOCSTRING
    """
        KontrolRGB:
        ===========
        Summary:
        --------
        This class is an interface class that
        interfaces the RGB driver and class from
        the BRS Python Libraries to work with
        BRS Kontrol.

        This class contains methods and members
        that makes it easier to display status
        and loading animations as well as error
        codes on your Kontrol devices.
    """
    #endregion
    #region   --------------------------- MEMBERS
    canBeUsed:bool = False
    """
        canBeUsed:
        ==========
        Summary:
        --------
        boolean member which is handled
        by the methods of this class.
        It indicates if the class can be used
        by the application.

        Warning:
        --------
        NEVER MANUALLY HANDLE THIS FUCKING MEMBER OK?
        Unless you wanna read it...
        ...
        Thank you! :P
    """
    brightness:float = 1
    """
        brightness:
        ===========
        Summary:
        --------
        Decides how bright the LEDs will be.
        Defaults to 1. In the future, this
        will be saved with your profile's
        informations.
    """
    #endregion
    #region   --------------------------- METHODS
    def Initialize() -> Execution:
        """
            Initialize:
            ===========
            Summary:
            --------
            Initializes the class as well
            as the backend RGB driver and classes.
            If anything else than Passed executions
            are returned at any points, the CanBeUsed
            member will stay set to False.

            Returns:
            --------
            - `Execution.Passed` = RGB can now be used!
            - `Execution.Failed` = No RGB for you! Desktop looking ass.
        """
        Debug.Start("Initialize")

        Debug.Log("Initializing RGB class.")
        result = RGB.StartDriver()
        if(result != Execution.Passed):
            Debug.Error("This class cannot be used")
            Debug.End()
            return Execution.Failed

        Debug.Log("RGB can be used!")
        KontrolRGB.canBeUsed = True
        Debug.End()
        return Execution.Passed
    # -----------------------------------
    def Uninitialize() -> Execution:
        """
            Uninitialize:
            =============
            Summary:
            --------
            Closes the Neopixel driver.
            Call this at the end of your
            application to ensure no
            drivers are still running.
        """
        Debug.Start("Uninitialize")

        if(KontrolRGB.canBeUsed):
            result = RGB.StopDriver()
            if(result != Execution.Passed):
                Debug.Error("Huh... seems like we cant close the Neopixel driver.")
                Debug.End()
                return Execution.Failed
            Debug.Log("Driver successfully stopped")
            Debug.End()
            return Execution.Passed
        else:
            Debug.Error("Cant stop a class that never started")
            Debug.End()
            return Execution.ByPassed
    # -----------------------------------
    def StartUpAnimation(currentLetterToShow:int):
        """
            StartUpAnimation:
            =================
            Summary:
            --------
            This method allows Kontrol to light up
            the BRS logo one letter at the time
            in sync with the startup animation
            when the remote boots up.

            Warning:
            --------
            DO NOT SPAM THIS METHOD, IT WILL SPAM
            SAVE JSON FILES

            Arguments:
            ----------
            - `currentLetterToShow`: 0=B, 1=BR, 2=BRS, 3=Off
        """
        Debug.Start("StartUpAnimation")

        if(KontrolRGB.canBeUsed):
            if(currentLetterToShow == 0):
                Debug.Log("Saved attributes to display B")
                RGB.SetAttributes(colors=[[255,255,255],[0,0,0],[0,0,0]],
                                rgbMode=RGBModes.static,
                                brightness=KontrolRGB.brightness,
                                lerpDelta=1
                                )
                Debug.End()
                return Execution.Passed

            if(currentLetterToShow == 1):
                Debug.Log("Saved attributes to display BR")
                RGB.SetAttributes(colors=[[255,255,255],[255,255,255],[0,0,0]],
                                rgbMode=RGBModes.static,
                                brightness=KontrolRGB.brightness,
                                lerpDelta=1
                                )
                Debug.End()
                return Execution.Passed

            if(currentLetterToShow == 2):
                Debug.Log("Saved attributes to display BRS")
                RGB.SetAttributes(colors=[[255,255,255],[255,255,255],[255,255,255]],
                                rgbMode=RGBModes.static,
                                brightness=KontrolRGB.brightness,
                                lerpDelta=1
                                )
                Debug.End()
                return Execution.Passed

            if(currentLetterToShow == 3):
                Debug.Log("Saved attributes to fade off")
                RGB.SetAttributes(colors=[[0,0,0],[0,0,0],[0,0,0]],
                                rgbMode=RGBModes.static,
                                brightness=KontrolRGB.brightness,
                                lerpDelta=0.04
                                )
                Debug.End()
                return Execution.Passed
            Debug.End()
            return Execution.ByPassed
        else:
            Debug.Error("CLASS CANNOT BE USED")
            Debug.End()
            return Execution.ByPassed
    # -----------------------------------
    def ApploadingAnimation():
        """
            ApploadingAnimation:
            ====================
            Summary:
            --------
            RGB mode set when the application
            is initially loading everything
            after the startup animation is
            finished.
        """
        Debug.Start("ApploadingAnimation")

        if(KontrolRGB.canBeUsed):
            Debug.Log("Getting accent colors")
            accent = GetAccentColor()

            red   = int(accent[0]*255)
            green = int(accent[1]*255)
            blue  = int(accent[2]*255)

            RGB.SetAttributes(colors=[red,green,blue],
                            rgbMode=RGBModes.loading,
                            lerpDelta=0.04,
                            animationDuration=1
                            )

            Debug.End()
            return Execution.Passed
        else:
            Debug.Error("CLASS CANNOT BE USED")
            Debug.End()
            return Execution.ByPassed
    # -----------------------------------
    def DisplayUserError():
        """
            DisplayUserError:
            =================
            Summary:
            --------
            Shows a slow cycling red
            color to the user to help
            indicate that their passwords
            or given information is not OK.
        """
        Debug.Start("DisplayUserError")

        if(KontrolRGB.canBeUsed):
            Debug.Log("Displaying User error")
            RGB.SetAttributes(colors=[255,0,0],
                            rgbMode=RGBModes.cycling,
                            lerpDelta=0.04,
                            animationDuration=5
                            )

            Debug.End()
            return Execution.Passed
        else:
            Debug.Error("CLASS CANNOT BE USED")
            Debug.End()
            return Execution.ByPassed
    # -----------------------------------
    def DisplayDefaultColor():
        """
            DisplayDefaultColor:
            =================
            Summary:
            --------
            Shows the user's
            accent color static as a
            default color when there
            isn't anything that is
            happenning.
        """
        Debug.Start("DisplayDefaultColor")

        if(KontrolRGB.canBeUsed):
            Debug.Log("Getting accent colors")
            accent = GetAccentColor(variant="A700")
            if(accent[0] == 0 and accent[1] == 0 and accent[2] == 0):
                accent = GetAccentColor(variant="900")

            red   = int(accent[0]*255)
            green = int(accent[1]*255)
            blue  = int(accent[2]*255)

            RGB.SetAttributes(colors=[red,green,blue],
                            rgbMode=RGBModes.static,
                            lerpDelta=0.04,
                            animationDuration=1
                            )

            Debug.End()
            return Execution.Passed
        else:
            Debug.Error("CLASS CANNOT BE USED")
            Debug.End()
            return Execution.ByPassed
    # -----------------------------------
    def FastLoadingAnimation():
        """
            FastLoadingAnimation:
            ====================
            Summary:
            --------
            When you get on screens that
            take a while to load in, this
            is the loading animation to
            display.
        """
        Debug.Start("FastLoadingAnimation")

        if(KontrolRGB.canBeUsed):
            Debug.Log("Getting accent colors")
            accent = GetAccentColor(variant="A700")
            if(accent[0] == 0 and accent[1] == 0 and accent[2] == 0):
                accent = GetAccentColor(variant="900")

            red   = int(accent[0]*255)
            green = int(accent[1]*255)
            blue  = int(accent[2]*255)

            RGB.SetAttributes(colors=[red,green,blue],
                            rgbMode=RGBModes.loading,
                            lerpDelta=0.1,
                            animationDuration=0.5
                            )

            Debug.End()
            return Execution.Passed
        else:
            Debug.Error("CLASS CANNOT BE USED")
            Debug.End()
            return Execution.ByPassed
    # -----------------------------------
    def DisplayPopUpAnimation(PopUpType):
        """
            DisplayPopUpAnimation:
            ======================
            Summary:
            --------
            This method's purpose is
            to display a pulsing
            RGB animation of a specific
            color depending on the
            PopUp type that is currently
            displayed to the user.

            Arguments:
            ----------
            - `PopUpType`: Says which type of pop up to display.
        """
        Debug.Start("DisplayPopUpAnimation")
        from ...Pages.PopUps import PopUpTypeEnum

        if(KontrolRGB.canBeUsed):
            Debug.Log("Getting accent colors")

            if(PopUpType == PopUpTypeEnum.FatalError):
                Debug.Log("Displaying FATAL ERROR")
                RGB.SetAttributes(colors=[255,0,0],
                                rgbMode=RGBModes.pulse,
                                lerpDelta=0.04,
                                animationDuration=0.5
                                )
                Debug.End()
                return Execution.Passed

            if(PopUpType == PopUpTypeEnum.Warning):
                Debug.Log("Displaying Warning")
                RGB.SetAttributes(colors=[255,128,0],
                                rgbMode=RGBModes.pulse,
                                lerpDelta=0.04,
                                animationDuration=1.5
                                )
                Debug.End()
                return Execution.Passed
                
            if(PopUpType == PopUpTypeEnum.Question):
                Debug.Log("Displaying Question")
                RGB.SetAttributes(colors=[0,0,255],
                                rgbMode=RGBModes.pulse,
                                lerpDelta=0.04,
                                animationDuration=1.5
                                )
                Debug.End()
                return Execution.Passed

            if(PopUpType == PopUpTypeEnum.Remark):
                Debug.Log("Displaying remark")
                RGB.SetAttributes(colors=[0,128,255],
                                rgbMode=RGBModes.pulse,
                                lerpDelta=0.04,
                                animationDuration=3
                                )
                Debug.End()
                return Execution.Passed
                
            if(PopUpType == PopUpTypeEnum.Custom):
                Debug.Log("Displaying Custom")
                RGB.SetAttributes(colors=[128,128,128],
                                rgbMode=RGBModes.pulse,
                                lerpDelta=0.04,
                                animationDuration=3
                                )
                Debug.End()
                return Execution.Passed

            Debug.Warn("Seems like your pop up type doesn't exist mate.")
            Debug.End()
            return Execution.ByPassed
        else:
            Debug.Error("CLASS CANNOT BE USED")
            Debug.End()
            return Execution.ByPassed        

        Debug.End()
    # -----------------------------------
    def DisplayMinorProblem():
        """
            DisplayMinorProblem:
            ===================
            Summary:
            --------
            Shows a slow pulsing
            orange color as an
            indicator that there
            has been a minor problem
            of some sort.
        """
        Debug.Start("DisplayMinorProblem")

        if(KontrolRGB.canBeUsed):
            RGB.SetAttributes(colors=[255,128,0],
                            rgbMode=RGBModes.pulse,
                            lerpDelta=0.04,
                            animationDuration=3
                            )

            Debug.End()
            return Execution.Passed
        else:
            Debug.Error("CLASS CANNOT BE USED")
            Debug.End()
            return Execution.ByPassed
    # -----------------------------------
    def StartOfHandshake():
        """
            Handshaking:
            ============
            Summary:
            --------
            Shows a very fast cycling
            animations RGB colors and shit
            so the user knows something's
            happenning with their cards.
        """
        Debug.Start("KontrolRGB -> Handshaking")

        if(KontrolRGB.canBeUsed):
            RGB.SetAttributes(colors=[255,255,255],
                            rgbMode=RGBModes.cycling,
                            lerpDelta=1,
                            animationDuration=3
                            )

            Debug.End()
            return Execution.Passed
        else:
            Debug.Error("CLASS CANNOT BE USED")
            Debug.End()
            return Execution.ByPassed
    # -----------------------------------
    def Handshaking():
        """
            Handshaking:
            ============
            Summary:
            --------
            Shows a very fast cycling
            animations RGB colors and shit
            so the user knows something's
            happenning with their cards.
        """
        Debug.Start("KontrolRGB -> Handshaking")

        if(KontrolRGB.canBeUsed):
            RGB.SetAttributes(colors=[255,255,255],
                            rgbMode=RGBModes.cycling,
                            lerpDelta=1,
                            animationDuration=1
                            )

            Debug.End()
            return Execution.Passed
        else:
            Debug.Error("CLASS CANNOT BE USED")
            Debug.End()
            return Execution.ByPassed
    #endregion
    #region   --------------------------- CONSTRUCTOR
    #endregion
    pass
#====================================================================#
LoadingLog.End("AppLoading.py")