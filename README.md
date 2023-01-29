![BRS white logo header](BRS_Header.png)
# **Kontrol**
## - Short Q&A
#### 1. *What is "BRS Kontrol"?*
BRS Kontrol is a Linux based remote control. It operates via a Raspberry Pi 3B+ and uses a standard HDMI touchscreen monitor for it's basic interfacing. Kontrol's goal is to control a custom build submarine, or any other supported device through a custom API. It will also support Plug N Play cards which we call BrSpand cards.
#### 2. *What is BrSpand?*
BrSpand is the name we gave to the Plug N Play cards. These cards use USB-C connectors to plug into Kontrol's custom made PCB to perform various types of actions. Each BrSpand card has it's own unique ID as well as unique, but generic functions that Kontrol can interface with. BrSpand cards are also capable of searching GitHub for updates and drivers to install in order for Kontrol to fully use their capabilities. A BrSpand card can serve specific or generic purposes. Such purpose could be a Joystick extension card, or a Debugging card, or an external battery, a WiFi extender, a Bluetooth receiver or anything you might think of. Since they download their own drivers and they use function based communications, they can be as generic as you want them to be.
#### 3. *What framework is used to make Kontrol's GUI?*
At first, we wanted to use C# dot net to build a GUI for Kontrol. However, we realized that multiple people were complaining on forums about its problems on RaspBerries so we opted for an open source python framework; Kivy. We also use KivyMD for a cleaner look that looks like a Material Design compliant UI as best as we could. Keep in mind we are no graphics designers nor Software Engineers.

---
## - Folders & Contents
#### - Quick Summary:
If you want to learn more about this repository's directory tree, or which folders contains what as well as their purpose, please refer to the available diagrams.net documentation. You can access the documentation through the following link:
https://drive.google.com/file/d/148wSuXA7z0FR9rAaGs48DwkEv2R8qK-p/view?usp=share_link.

#### - List of folders:
The following is a quick list of this repository's directory list. If you want a description of each folders and their contents, please refer to the markdown file associated with each folder. They will explain in greater detail their contents and purpose.
- **BrSpand**
    - **Drivers**
    - **Logs**
- **Libraries**
    - **BRS**
    - **Icons**
- **Local**
    - **Drivers**
    - **Profile**
- **Programs**
    - **Pages**

