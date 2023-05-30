#====================================================================#
# File Information
#====================================================================#
"""
    actions.py
    =============
    This file's purpose is to hold all the actions that Batiscan can
    execute from :ref:`Controls` in BRS_Python_Libraries. This
    includes functions and methods to extract values from binders as
    well as threads to constantly read from them and execute changes
    if something changes in them.
"""
#====================================================================#
# Loading Logs
#====================================================================#
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import LoadingLog
LoadingLog.Start("actions.py")
#====================================================================#
# Imports
#====================================================================#
#region ------------------------------------------------------ Python
# LoadingLog.Import("Python")
#endregion
#region --------------------------------------------------------- BRS
LoadingLog.Import("Libraries")
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
from Libraries.BRS_Python_Libraries.BRS.PnP.controls import SoftwareAxes, SoftwareButtons
from Local.Drivers.Batiscan.Programs.Controls.controls import BatiscanControls
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
batiscanAxesActions = {
    SoftwareAxes.pitch_up    : {"description" : "Pitch upwards"},
    SoftwareAxes.pitch_down  : {"description" : "Pitch downwards"},
    SoftwareAxes.roll_left   : {"description" : "Roll left"},
    SoftwareAxes.roll_right  : {"description" : "Roll right"},
    SoftwareAxes.yaw_left    : {"description" : "turn left"},
    SoftwareAxes.yaw_right   : {"description" : "turn right"},
    SoftwareAxes.up          : {"description" : "pitch camera up"},
    SoftwareAxes.down        : {"description" : "pitch camera down"}
}
"""
    A list of all the software axes being used by Batiscan when its
    GUI is loaded and going and their associated descriptions. 
    The names within this list are extracted from :ref:`Controls`. 
    :ref:`SoftwareAxis`
"""

batiscanButtonsActions = {
   SoftwareButtons.fill         : {"description" : "Fills the ballast"},
   SoftwareButtons.empty        : {"description" : "Empty the ballast"},
   SoftwareButtons.reset        : {"description" : "Resets batiscasn"},
   SoftwareButtons.forward      : {"description" : "Full speed forward"},
   SoftwareButtons.backward     : {"description" : "Full speed backward"},
   SoftwareButtons.up           : {"description" : "Pitch up"},
   SoftwareButtons.down         : {"description" : "Pitch down"},
   SoftwareButtons.left         : {"description" : "Yaw left"},
   SoftwareButtons.right        : {"description" : "Yaw right"},
   SoftwareButtons.on           : {"description" : "Turn On lights"},
   SoftwareButtons.off          : {"description" : "Turn Off lights"},
   SoftwareButtons.custom_1     : {"description" : "Surface immediately"},
   SoftwareButtons.custom_2     : {"description" : "Turn on/off camera"},
}
"""
    A list of all the software buttons being used by Batiscan when its
    GUI is loaded and going and their associated descriptions. 
    The names within this list are extracted from :ref:`Controls`. 
    :ref:`SoftwareButtons`
"""
#====================================================================#
# Classes
#====================================================================#
# LoadingLog.Class("BatiscanValues")
class BatiscanActions:
    # region   --------------------------- DOCSTRING
    """
        BatiscanActions:
        ================
        Summary:
        ========
        Class that contains method that are called
        by threads to update current wanted values
        based off the changes in states of hardware
        that might be binded to batiscan.
    """
    # endregion
    # region   --------------------------- MEMBERS

    # endregion
    # region   --------------------------- METHODS
    def LightsWantedOn():
        BatiscanControls.wantedLeftLight = True
        BatiscanControls.wantedRightLight = True

    def LightsWantedOff():
        BatiscanControls.wantedLeftLight = False
        BatiscanControls.wantedRightLight = False
    # endregion
    # region   --------------------------- CONSTRUCTOR
    # endregion
    pass
#====================================================================#
LoadingLog.End("values.py")