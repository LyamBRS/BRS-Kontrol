# **Local**
## - Description
The local folder is where files specific to a certain Kontrol device are located. These files are generated or created by Kontrol and are unique to each remote controller. These files are copied and saved each time Kontrol updates itself. The content of this folder is thus passed from versions to versions locally.

The content of the local folder is basically user specific files. It contains profile settings, all the configuration of every BrSpand cards seen by the specific Kontrol device, the generic drivers downloaded for any BrSpand cards that were ever connected to this specific Kontrol remote controller and so on. You can see it as a "temp" folder.

## - Folders & Contents
#### - Quick Summary:
If you want to learn more about this repository's directory tree, or which folders contains what as well as their purpose, please refer to the available diagrams.net documentation. You can access the documentation through the following link:
https://drive.google.com/file/d/148wSuXA7z0FR9rAaGs48DwkEv2R8qK-p/view?usp=share_link.

#### - List of folders:
The following is a quick list of this folder's directories. If you want a description of each folders and their contents, please refer to the markdown file associated with each folder. They will explain in greater detail their contents and purpose.
- **Local**
    - **Drivers** - Drivers downloaded by BrSpand cards that connected to Kontrol.
    - **Profiles** - User profiles and their associated settings and configurations for the cards they connected while using their profiles
    - **Languages** - folders containing language files used by the application to display various texts. Has US_English and CAN_French by default. Adding a language to the list is fairly simple. Copy and paste one of the folders, rename it with COUNTRY_Language, edit the .po files in the new folder, run _Compiler.py and you should have a new language available for use. If some words are missing, they default to english.
    - **Cache** - Holds the cached data by the application for so that it can remember previous settings when it re-opens later. Deleting the contents of this folder has no effect as if they are corrupted or deleted, they will be rebuilt when the application closes on normal circumstances.