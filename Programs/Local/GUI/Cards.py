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
from cgitb import text
from Libraries.BRS_Python_Libraries.BRS.Debug.LoadingLog import LoadingLog
from Libraries.BRS_Python_Libraries.BRS.Network.Web.web import IsWebsiteOnline
from Libraries.BRS_Python_Libraries.BRS.Utilities.Enums import Execution, FileIntegrity
from Libraries.BRS_Python_Libraries.BRS.Utilities.FileHandler import JSONdata
from Libraries.BRS_Python_Libraries.BRS.Utilities.Information import Information
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
from Libraries.BRS_Python_Libraries.BRS.Network.APIs.GitHub import ManualGitHub, RepoLinkIsValid, StringToGitLink
#endregion
#region -------------------------------------------------------- Kivy
LoadingLog.Import("Kivy")
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex
from kivy.graphics import Color, RoundedRectangle
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
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDFillRoundFlatIconButton
from Libraries.BRS_Python_Libraries.BRS.GUI.Inputs.textfield import VirtualKeyboardTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.behaviors import TouchBehavior
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
LoadingLog.Class("DeviceDriverInstallerCard")
class DeviceDriverInstallerCard(BaseButton, Widget):
    #region   --------------------------- DOCSTRING
    ''' 
        DeviceDriverInstallerCard:
        ===========
        Summary:
        --------
        This class is a widget class that builds a search card used
        to download device drivers from the internet to a specific
        folder path on Kontrol.
    '''
    #endregion
    #region   --------------------------- MEMBERS
    #endregion
    #region   --------------------------- METHODS
    #region   -- Public

    def CheckInternet(self, *args):
        """
            Function that checks if internet is available.
            Updates the card according to the execution
            result.
        """
        pass

    def on_valid_repository(self, *args):
        """
            on_valid_repository:
            ====================
            Summary:
            --------
            Callback function executed when
            the user enters a valid git
            repository in the search bar.
            Replace this by your own function.
        """
        pass

    def DownloadRepository(self, *args):
        """
            DownloadRepository:
            ===================
            Summary:
            --------
            Function that checks if internet is available.
            Then attempts to download the repository found
            in it's search bar.
        """
        Debug.Start("DownloadRepository")
        link = StringToGitLink(self.SearchBox.text)
        if(link == Execution.Failed):
            Debug.Error(f"Failed to parse {self.SearchBox.text} into a repository.")
            self.Set_RepositoryNotFound()
            Debug.End()
            return

        if(RepoLinkIsValid(link)):
            Debug.Error(f"{link} is a valid repository.")
            self.on_valid_repository(link)
            self.Set_Normal()
        else:
            Debug.Error(f"{link} is not a valid repository.")
            self.Set_RepositoryNotFound()
        Debug.End()
    #endregion
    #region   -- Private
    # ------------------------------------------------------
    def _RippleHandling(self, object, finished):
        if(finished):
            # Check if WiFi is online
            online = IsWebsiteOnline()
            if(not online):
                # remaining = ManualGitHub.GetRequestsLeft()
                # Debug.Log(f"Requests left: {remaining}")
                # if(remaining > 0):
                self.DownloadRepository()
                # else:
                    # self.Set_NoGitHubRequests()
            else:
                self.Set_NoWifi()
            pass
    # ------------------------------------------------------
    def Set_NoWifi(self):
        """
            Updates the card to display no wifi
        """
        Debug.Start("Set_NoWifi")
        self.BottomButton.icon = "reload"
        self.BottomButton.text = _("Retry")
        self.MiddleIcon.icon = "wifi-remove"
        self.InformationLabel.text = _("No internet connection. Device drivers cannot be installed.")
        self.SearchBox.disabled = True
        self.SearchBox.text = ""
        Debug.End()

    def Set_Normal(self):
        """
            Updates the card to display regular
            information.
        """
        Debug.Start("Set_Normal")
        self.BottomButton.icon = "search-web"
        self.BottomButton.text = _("Search GitHub")
        self.MiddleIcon.icon = "github"
        self.InformationLabel.text = _("Search GitHub for device drivers to install")
        self.SearchBox.disabled = False
        self.SearchBox.text = ""
        Debug.End()

    def Set_RepositoryNotFound(self):
        """
            Updates the card to display the fact
            that no github repository could be
            found based off the search field.
        """
        Debug.Start("Set_RepositoryNotFound")
        self.BottomButton.icon = "magnify"
        self.BottomButton.text = _("Search GitHub")
        self.MiddleIcon.icon = "magnify-close"
        self.InformationLabel.text = _("No repository could be found with that link.")
        self.SearchBox.disabled = False
        self.SearchBox.text = ""
        Debug.End()

    def Set_NoGitHubRequests(self):
        """
            Updates the card to display no Github
            request.
        """
        Debug.Start("Set_NoGitHubRequests")
        self.BottomButton.icon = "reload"
        self.BottomButton.text = _("Retry")
        self.MiddleIcon.icon = "github"
        self.InformationLabel.text = _("You ran out of GitHub API requests. Wait up to an hour.")
        self.SearchBox.disabled = True
        self.SearchBox.text = ""
        Debug.End()
    #endregion
    #endregion
    #region   --------------------------- CONSTRUCTOR
    def __init__(self,
                 **kwargs):
        super(DeviceDriverInstallerCard, self).__init__(**kwargs)
        Debug.Start("DeviceDriverInstallerCard")
        #region --------------------------- Initial check ups

        self.padding = 0
        self.spacing = 0

        self.Card = MDCard()
        self.Card.orientation = "vertical"
        self.Card.elevation = Shadow.Elevation.default
        self.Card.shadow_softness = Shadow.Smoothness.default
        self.Card.radius = Rounding.Cards.default
        self.size = (400,425)
        self.ripple_alpha = 0
        #endregion

        #region --------------------------- Widgets
        self.Layout = MDFloatLayout()
        self.Layout.padding = 25
        self.Layout.size_hint = (1,1)

        self.BottomButton = MDFillRoundFlatIconButton(
                                icon = "search-web",
                                text = _("Search"),
                                font_style = "H4",
                            )
        self.BottomButton.rounded_button = False
        self.BottomButton.pos_hint = {'center_x': 0.5, 'center_y': 0.075}
        self.BottomButton.size_hint = (1, None)
        self.BottomButton.bind(_finishing_ripple = self._RippleHandling)

        self.MiddleIcon = MDIconButton(
                                icon = "github",
                                disabled = True,
                                icon_size = 150,
                                pos_hint = {'center_x': 0.5, 'center_y': 0.75}
                            )
        self.MiddleIcon.pos_hint = {'center_x': 0.5, 'center_y': 0.60}

        self.InformationLabel = MDLabel(
                                text = _("Search for a device driver repository to download."),
                                font_style = "H6",
                            )
        self.InformationLabel.pos_hint = {'center_x': 0.5, 'center_y': 0.25}
        self.InformationLabel.size_hint = (0.75, None)

        self.SearchBox = VirtualKeyboardTextField(
            hint_text = _("Search") + " GitHub",
            pos_hint = {'center_x': 0.5, 'center_y': 0.925}
        )
        self.SearchBox.size_hint = (0.75, None)

        self.Layout.add_widget(self.SearchBox)
        self.Layout.add_widget(self.MiddleIcon)
        self.Layout.add_widget(self.InformationLabel)
        self.Layout.add_widget(self.BottomButton)
        self.Card.add_widget(self.Layout)

        if(Information.CanUse.Internet):
            Debug.Log("internet can be used.")
            self.Set_Normal()
        else:
            self.Set_NoWifi()
        #endregion

        self.add_widget(self.Card)
        Debug.End()
    #endregion
    pass
#====================================================================#
LoadingLog.Class("DeviceDriverCard")
class DeviceDriverCard(BaseButton, TouchBehavior, Widget):
    #region   --------------------------- DOCSTRING
    '''
        DeviceDriverCard:
        =================
        Summary:
        --------
        This class is used to create a card with button attributes
    '''
    #endregion
    #region   --------------------------- MEMBERS
    banner_rect = None

    json:JSONdata = None
    """
        json:
        =====
        Summary:
        --------
        A :ref:`JSONdata` object
        representing the device driver's
        Config.json which holds basic
        information about the device driver
        that this card is representing.
    """
    #endregion
    #region   --------------------------- METHODS
    #region   -- Public
    def PressedEnd(self, *args):
        """
            Function called by the card once the ripple effect
            comes to an end.
        """
        pass

    def LongPressed(self, name:str):
        """
            LongPressed:
            ============
            Summary:
            --------
            Called by this widget's :ref:`on_long_touch`
            Overwrite this with a function that uses
            a string as a parameter.
        """
        pass

    def on_long_touch(self, *args):
        """
            on_long_touch:
            ==============
            Summary:
            --------
            Internal function that
            calls :ref:`LongPressed`
            DO NOT OVERWRITE.
        """
        self.LongPressed(self.name)
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
        self.size = (400,425)

        self.bind(_finishing_ripple = self._RippleHandling)

        self.Card = MDCard()
        self.Card.orientation = "vertical"
        self.Card.elevation = Shadow.Elevation.default
        self.Card.shadow_softness = Shadow.Smoothness.default
        self.Card.radius = Rounding.Cards.default
        #endregion

        #region --------------------------- Widgets
        self.Layout = MDFloatLayout()
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
        Debug.Log(f"Checking integrity of -> {driverName}")
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

        self.Name = MDLabel(text=name, font_style = "H4", halign = "center")
        self.Name.pos_hint = { 'center_x': 0.5, 'center_y': 0.25 }

        if(error):
            # icons and text should be red
            self.Name.theme_text_color = "Error"
            Icon.theme_text_color = "Error"
            Icon.theme_icon_color = "Error"


        Layout.add_widget(Icon)
        Layout.add_widget(self.Name)
        Card.add_widget(Layout)
        self.add_widget(Card)

        #endregion
        Debug.End()
    #endregion
    pass
#====================================================================#
#====================================================================#
LoadingLog.Class("ListCard")
class ListCard(BaseButton, Widget):
    #region   --------------------------- DOCSTRING
    ''' 
        ListCard:
        ===========
        Summary:
        --------
        This class is used to create a card that displays a dictionary
        with a title associated with it.
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
        banner_width = self.TitleLayout.width
        banner_height = self.TitleLayout.height + 5

        if self.banner_rect:
            self.banner_rect.pos = (self.TitleLayout.x, self.TitleLayout.y - 6)
            self.banner_rect.size = (banner_width, banner_height)
        else:
            corner:str = Rounding.Cards.default.replace("dp","")
            corner = int(corner)
            with self.TitleLayout.canvas.before:
                Color(*self.banner_color)
                self.banner_rect = RoundedRectangle(pos=self.TitleLayout.pos, size=(banner_width, banner_height), radius=[corner, corner, corner, corner])
    #endregion
    #endregion
    #region   --------------------------- CONSTRUCTOR
    def __init__(self,
                 dictionary:dict,
                 title:str="",
                 **kwargs):
        super(ListCard, self).__init__(**kwargs)
        Debug.Start("ListCard")
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
        self.disabled = True
        #endregion

        #region --------------------------- Widgets
        self.Layout = MDFloatLayout()
        self.Layout.padding = 25
        self.Layout.size_hint = (1,1)

        self.TitleLayout = MDBoxLayout()
        self.TitleLayout.orientation = "horizontal"
        # self.RequirementsLayout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.TitleLayout.size_hint = (1, 0.15)

        self.Name = MDLabel(text=title, font_style = "H4", halign = "center")
        self.Name.pos_hint = { 'center_x': 0.5, 'center_y': 0.5 }

        self.ListLayout = MDGridLayout()
        self.ListLayout.cols = 2
        self.ListLayout.pos_hint = { 'center_x': 0.5, 'center_y': 0.5 }
        #endregion

        #region --------------------------- Array handling
        Debug.Log("Putting keys and values in card")

        for key in dictionary.keys():
            value = dictionary[key]

            value = MDLabel(text=str(value), halign = "center")
            key   = MDLabel(text=str(key), halign = "center")

            self.ListLayout.add_widget(key)
            self.ListLayout.add_widget(value)
        #endregion

        self.TitleLayout.add_widget(self.Name)
        self.Layout.add_widget(self.ListLayout)
        self.Card.add_widget(self.TitleLayout)
        self.Card.add_widget(self.Layout)
        self.add_widget(self.Card)

        #region --------------------------- Canvas
        # Adding a banner to the top of the card for requirement
        # icons to be layed on.
        color = MDApp.get_running_app().theme_cls.accent_palette
        self.banner_color = get_color_from_hex(colors[color]["500"])
        self.TitleLayout.bind(pos=self.UpdateBanner, size=self.UpdateBanner)

        #endregion

        Debug.End()
    #endregion
    pass
#====================================================================#
LoadingLog.End("Cards.py")