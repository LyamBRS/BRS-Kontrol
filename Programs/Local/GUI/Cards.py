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
from Libraries.BRS_Python_Libraries.BRS.Utilities.Enums import FileIntegrity
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
from Libraries.BRS_Python_Libraries.BRS.Utilities.LanguageHandler import _
#endregion
#region -------------------------------------------------------- Kivy
LoadingLog.Import("Kivy")
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex
from kivy.graphics import Color, RoundedRectangle
from kivy.graphics.instructions import InstructionGroup
#endregion
#region ------------------------------------------------------ KivyMD
LoadingLog.Import('KivyMD')
from kivymd.app import MDApp
from kivymd.color_definitions import colors
from kivymd.uix.button import BaseButton, MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
#endregion
LoadingLog.Import("Local")
from ..FileHandler.deviceDriver import Get_OtherDeviceButton, GetJson, CheckIntegrity, Get_BluetoothButton, Get_BrSpandButton, Get_InternetButton, Get_KontrolButton, Get_OSButton, Get_ProcessorButton
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
    banner_rect = None
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
    def UpdateBanner(self, *args):
        banner_width = self.RequirementsLayout.width
        banner_height = self.RequirementsLayout.height + 5

        if self.banner_rect:
            self.banner_rect.pos = (self.RequirementsLayout.x, self.RequirementsLayout.y - 6)
            self.banner_rect.size = (banner_width, banner_height)
        else:
            corner:str = Rounding.Cards.default.replace("dp","")
            corner = int(corner)
            with self.RequirementsLayout.canvas.before:
                Color(*self.banner_color)
                self.banner_rect = RoundedRectangle(pos=self.RequirementsLayout.pos, size=(banner_width, banner_height), radius=[corner, corner, corner, corner])
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
        self.Card.orientation = "vertical"
        self.Card.elevation = Shadow.Elevation.default
        self.Card.shadow_softness = Shadow.Smoothness.default
        self.Card.radius = Rounding.Cards.default
        self.size = (400,425)
        #endregion

        #region --------------------------- Widgets
        self.Layout = MDFloatLayout()
        self.Layout.padding = 25
        self.Layout.size_hint = (1,1)

        self.RequirementsLayout = MDBoxLayout()
        self.RequirementsLayout.orientation = "horizontal"
        # self.RequirementsLayout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.RequirementsLayout.size_hint = (1, 0.15)

        self.Icon = MDIconButton(icon = "exclamation", halign = "center", icon_size = 120)
        self.Icon.pos_hint = { 'center_x': 0.5, 'center_y': 0.75 }

        self.Name = MDLabel(text=_("Error"), font_style = "H5", halign = "center")
        self.Name.pos_hint = { 'center_x': 0.5, 'center_y': 0.5 }

        self.Description = MDLabel(text=_("Not Initialized"), halign = "center")
        self.Description.pos_hint = { 'center_x': 0.5, 'center_y': 0.25 }
        #endregion

        #region --------------------------- Integrity Check
        Debug.Log("Checking integrity of -> {driverName}")
        integrity = CheckIntegrity(driverName)

        if(integrity == FileIntegrity.Good):
            Debug.Log("Good integrity")

            Debug.Log("Getting JSON")
            self.json = GetJson(driverName)

            self.name        = self.json.jsonData["Information"]["Name"]
            self.description = self.json.jsonData["Information"]["Description"]
            self.iconPath    = self.json.jsonData["Information"]["IconPath"]
            self.iconType    = self.json.jsonData["Information"]["IconType"]
            self.version     = self.json.jsonData["Information"]["Version"]

            self.needs_OS           = self.json.jsonData["Requirements"]["OS"]
            self.needs_Processor    = self.json.jsonData["Requirements"]["Processor"]
            self.needs_Internet     = self.json.jsonData["Requirements"]["Internet"]
            self.needs_Bluetooth    = self.json.jsonData["Requirements"]["Bluetooth"]
            self.needs_BrSpand      = self.json.jsonData["Requirements"]["BrSpand"]
            self.needs_Kontrol      = self.json.jsonData["Requirements"]["Kontrol"]
            self.needs_OtherDevice  = self.json.jsonData["Requirements"]["OtherDevice"]

            self.OS          = Get_OSButton(self.needs_OS)
            self.Processor   = Get_ProcessorButton(self.needs_Processor)
            self.Internet    = Get_InternetButton(self.needs_Internet)
            self.Bluetooth   = Get_BluetoothButton(self.needs_Bluetooth)
            self.BrSpand     = Get_BrSpandButton(self.needs_BrSpand)
            self.Kontrol     = Get_KontrolButton(self.needs_Kontrol)
            self.OtherDevice = Get_OtherDeviceButton(self.needs_OtherDevice)

            if(self.OS != None):
                Debug.Log("Adding OS icon")
                self.RequirementsLayout.add_widget(self.OS)

            if(self.Processor != None):
                Debug.Log("Adding Processor icon")
                self.RequirementsLayout.add_widget(self.Processor)

            if(self.Internet != None):
                Debug.Log("Adding Internet icon")
                self.RequirementsLayout.add_widget(self.Internet)

            if(self.Bluetooth != None):
                Debug.Log("Adding Bluetooth icon")
                self.RequirementsLayout.add_widget(self.Bluetooth)

            if(self.BrSpand != None):
                Debug.Log("Adding BrSpand icon")
                self.RequirementsLayout.add_widget(self.BrSpand)

            if(self.Kontrol != None):
                Debug.Log("Adding Kontrol icon")
                self.RequirementsLayout.add_widget(self.Kontrol)

            if(self.OtherDevice != None):
                Debug.Log("Adding OtherDevice icon")
                self.RequirementsLayout.add_widget(self.OtherDevice)

            self.Name.text = self.name
            self.Description.text = self.description
            self.Icon.icon = self.iconPath
        else:
            if(integrity == FileIntegrity.Error):
                pass
            elif(integrity == FileIntegrity.Corrupted):
                pass
            elif(integrity == FileIntegrity.Ahead):
                pass
            elif(integrity == FileIntegrity.Outdated):
                pass
            elif(integrity == FileIntegrity.Blank):
                pass
        #endregion


        self.Card.add_widget(self.RequirementsLayout)
        self.Layout.add_widget(self.Icon)
        self.Layout.add_widget(self.Name)
        self.Layout.add_widget(self.Description)
        self.Card.add_widget(self.Layout)
        self.add_widget(self.Card)

        #region --------------------------- Canvas
        # Adding a banner to the top of the card for requirement
        # icons to be layed on.
        color = MDApp.get_running_app().theme_cls.accent_palette
        self.banner_color = get_color_from_hex(colors[color]["500"])
        self.RequirementsLayout.bind(pos=self.UpdateBanner, size=self.UpdateBanner)

        #endregion

        Debug.End()
    #endregion
    pass
#====================================================================#
LoadingLog.Class("WidgetCard")
class WidgetCard(BaseButton, Widget):
    #region   --------------------------- DOCSTRING
    ''' 
        WidgetCard:
        ===========
        Summary:
        --------
        This card is used as a simple widget card displaying
        a single icon in it's center, with a word below it.
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
    #endregion
    #endregion
    #region   --------------------------- CONSTRUCTOR
    def __init__(self,
                 name:str="blank",
                 icon:str="blank",
                 error:bool=False,
                 outlined:bool=False,
                 **kwargs):
        super(WidgetCard, self).__init__(**kwargs)
        Debug.Start("WidgetCard")
        #region --------------------------- Initial check ups
        self.padding = 0
        self.spacing = 0
        self.size = (400,425)

        self.bind(_finishing_ripple = self._RippleHandling)

        Card = MDCard()
        Card.orientation = "vertical"
        Card.elevation = Shadow.Elevation.default
        Card.shadow_softness = Shadow.Smoothness.default
        Card.radius = Rounding.Cards.default
        #endregion

        #region --------------------------- Widgets
        Layout = MDFloatLayout()
        Layout.padding = 25
        Layout.size_hint = (1,1)

        Icon = MDIconButton(icon = icon, halign = "center", icon_size = 200)
        Icon.pos_hint = { 'center_x': 0.5, 'center_y': 0.60 }

        Name = MDLabel(text=name, font_style = "H4", halign = "center")
        Name.pos_hint = { 'center_x': 0.5, 'center_y': 0.25 }

        if(error):
            # icons and text should be red
            Name.theme_text_color = "Error"
            Icon.theme_text_color = "Error"
            Icon.theme_icon_color = "Error"


        Layout.add_widget(Icon)
        Layout.add_widget(Name)
        Card.add_widget(Layout)
        self.add_widget(Card)

        #endregion
        Debug.End()
    #endregion
    pass

#====================================================================#
LoadingLog.End("Cards.py")