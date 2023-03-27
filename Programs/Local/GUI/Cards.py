#====================================================================#
# File Information
#====================================================================#
"""
    Cards.py
    =============
    This file is used to hold widgts and functions which makes custom
    cards specific to Kontrols application and Kontrol application
    only. Otherwise, cards are created inside BRS_Python_Libraries.
"""
#====================================================================#
# Loading Logs
#====================================================================#
from Libraries.BRS_Python_Libraries.BRS.Debug.LoadingLog import LoadingLog
LoadingLog.Start("Cards.py")
#====================================================================#
# Imports
#====================================================================#
#region ------------------------------------------------------ Python
LoadingLog.Import("Python")
#endregion
#region --------------------------------------------------------- BRS
LoadingLog.Import("Libraries")
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
from Libraries.BRS_Python_Libraries.BRS.GUI.Utilities.references import Shadow, Rounding
#endregion
#region -------------------------------------------------------- Kivy
LoadingLog.Import("Kivy")
from kivy.uix.widget import Widget
#endregion
#region ------------------------------------------------------ KivyMD
LoadingLog.Import('KivyMD')
from kivymd.uix.button import BaseButton
from kivymd.uix.card import MDCard
#endregion
#====================================================================#
# Functions
#====================================================================#

#====================================================================#
# Classes
#====================================================================#
LoadingLog.Class("ButtonCard")
class ButtonCard(BaseButton, Widget):
    #region   --------------------------- DOCSTRING
    ''' 
        ButtonCard:
        ===========
        Summary:
        --------
        This class is used to create a card with button attributes
    '''
    #endregion
    #region   --------------------------- MEMBERS
    #endregion
    #region   --------------------------- METHODS
    #region   -- Public
    def PressedEnd(self, *args):
        """
            Function called by the card once the ripple effect
            comes to an end.
        """
        pass
    #endregion
    #region   -- Private
    # ------------------------------------------------------
    def _RippleHandling(self, object, finished):
        if(finished):
            self.PressedEnd(self)
    # ------------------------------------------------------
    #endregion
    #endregion
    #region   --------------------------- CONSTRUCTOR
    def __init__(self,
                 **kwargs):
        super(ButtonCard, self).__init__(**kwargs)
        Debug.Start("ButtonCard")
        #region --------------------------- Initial check ups

        self.padding = 0
        self.spacing = 0

        self.bind(_finishing_ripple = self._RippleHandling)

        self.Card = MDCard()
        self.Card.elevation = Shadow.Elevation.default
        self.Card.shadow_softness = Shadow.Smoothness.default
        self.Card.radius = Rounding.Cards.default
        #endregion

        self.add_widget(self.Card)
        Debug.End()
    #endregion
    pass
#====================================================================#
LoadingLog.Class("DeviceDriverCard")
class DeviceDriverCard(BaseButton, Widget):
    #region   --------------------------- DOCSTRING
    ''' 
        ButtonCard:
        ===========
        Summary:
        --------
        This class is used to create a card with button attributes
    '''
    #endregion
    #region   --------------------------- MEMBERS
    #endregion
    #region   --------------------------- METHODS
    #region   -- Public
    def PressedEnd(self, *args):
        """
            Function called by the card once the ripple effect
            comes to an end.
        """
        pass
    #endregion
    #region   -- Private
    # ------------------------------------------------------
    def _RippleHandling(self, object, finished):
        if(finished):
            self.PressedEnd(self)
    # ------------------------------------------------------
    #endregion
    #endregion
    #region   --------------------------- CONSTRUCTOR
    def __init__(self,
                 driverName:str="",
                 **kwargs):
        super(DeviceDriverCard, self).__init__(**kwargs)
        Debug.Start("DeviceDriverCard")
        #region --------------------------- Initial check ups
        self.padding = 0
        self.spacing = 0

        self.bind(_finishing_ripple = self._RippleHandling)

        self.Card = MDCard()
        self.Card.elevation = Shadow.Elevation.default
        self.Card.shadow_softness = Shadow.Smoothness.default
        self.Card.radius = Rounding.Cards.default
        self.size = (400,400)
        #endregion

        self.add_widget(self.Card)
        Debug.End()
    #endregion
    pass
#====================================================================#
LoadingLog.End("Cards.py")