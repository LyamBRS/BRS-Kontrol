#====================================================================#
# File Information
#====================================================================#
""" Handles loading, saving and creating new profiles """
#====================================================================#
# Imports
#====================================================================#
from Libraries.BRS_Python_Libraries.BRS.Utilities.FileHandler import JSONdata,FilesFinder
#====================================================================#
# Global accessibles
#====================================================================#
profileStructure = {
    "ProfileConfig": {
        "CanDelete" : True,  # False, True
        "Type" : "Template", #"Template", "Add", "Guest", "Normal", "Temporary"
    },
    "Generic" : {
        "Username" : "Username",
        "Password" : "",
        "IconType" : "Kivy",
        "IconPath" : "account-outline"
    },
    "Theme" : {
        "Style" : "Light",
        "Primary" : "Purple",
        "Accent" : "Teal",
        "Duration" : 0.5,
    },
    "Settings" : {
        "TO DO":None
    }
}
#====================================================================#
# Functions
#====================================================================#
Profiles: FilesFinder = None
"""
    Loaded profiles by the application. This is globally accessible to all
    screens and menus.

    This is built at the very start of the application loading, and stores
    all the available profile files.
"""
#====================================================================#
# Classes
#====================================================================#