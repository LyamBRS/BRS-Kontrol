import subprocess
import time

abolishedGPIONumbers = []

#region ------------------------------- GPIO Analyzing
def GetGpioNumber(line:str):

    if(type(line) != str):
        return None

    if("GPIO" not in line):
        return None

    try:
        line = line.split(":")[0]
        line = line.replace("GPIO","")
        line = int(line)

        if line not in abolishedGPIONumbers:
            return line
        else:
            return None
    except:
        return None

def GetGPIOLevel(line:str):
    if(type(line) != str):
        return False

    if("level" not in line):
        return False

    try:
        line = line.split("level=")[1][0]
        return int(line)
    except:
        return False

def GetGPIOPullMode(line:str) -> str:
    if(type(line) != str):
        return False

    if("pull" not in line):
        return False

    try:
        line = line.split("pull=")[1]
        return line
    except:
        return False

def GetGPIOFunction(line:str) -> str:
    if(type(line) != str):
        return False

    if("func" not in line):
        return False

    try:
        line = line.split("func=")[1]
        line = line.split("pull=")[0]
        line = line.strip()
        return line
    except:
        return False

def GetGPIOfunctionSelect(line:str) -> int:
    if(type(line) != str):
        return False

    if("fsel" not in line):
        return False

    try:
        line = line.split("fsel=")[1]
        line = line.split(" ")[0]
        line = line.strip()
        return int(line)
    except:
        return False

def GetGPIOAlt(line:str) -> int:
    if(type(line) != str):
        return None

    if("fsel" not in line):
        return None

    try:
        line = line.split("alt=")[1]
        line = line.split(" ")[0]
        line = line.strip()
        return int(line)
    except:
        return None

def GetGPIOInfoFromLine(line:str) -> dict:
    if(type(line) != str):
        return None

    if("BANK" in line):
        return None

    gpioNumber      = GetGpioNumber(line)
    if(gpioNumber == None):
        return None
    level           = GetGPIOLevel(line)
    pullMode        = GetGPIOPullMode(line)
    function        = GetGPIOFunction(line)
    functionSelect  = GetGPIOfunctionSelect(line)
    alt             = GetGPIOAlt(line)

    returnedDictionary = {
        "gpio" : gpioNumber,
        "level" : level,
        "pull-mode" : pullMode,
        "function" : function,
        "function-selected" : functionSelect,
        "alt-selected" : alt
    }
    return returnedDictionary

def GetAllGPIOInformation() -> list:
    command = 'sudo raspi-gpio get'
    output = subprocess.check_output(command, shell=True, universal_newlines=True)

    resultedList = []
    for line in output.splitlines():
        information = GetGPIOInfoFromLine(line)
        if(information != None):
            resultedList.append(information)
    return resultedList

def CompareAndPrintGPIODict(oldDict:dict, newDict:dict):

    oldNumber = oldDict["gpio"]
    newNumber = newDict["gpio"]
    oldLevel = oldDict["level"]
    newLevel = newDict["level"]
    oldPullMode = oldDict["pull-mode"]
    newPullMode = newDict["pull-mode"]
    oldFunction = oldDict["function"]
    newFunction = newDict["function"]
    oldFunctionSelected = oldDict["function-selected"]
    newFunctionSelected = newDict["function-selected"]
    oldAltSelected = oldDict["alt-selected"]
    newAltSelected = newDict["alt-selected"]

    changesOccured:bool = False

    if(oldNumber != newNumber):
        changesOccured = True
        print(f"GPIO {oldNumber} is now GPIO {newNumber}")

    if(oldLevel != newLevel):
        changesOccured = True
        level = "HIGH" if newLevel==1 else "LOW"
        print(f"GPIO {newNumber}'s level is now {newLevel}")

    if(oldPullMode != newPullMode):
        changesOccured = True
        print(f"GPIO {newNumber} is pulling {newPullMode} instead of {oldPullMode}")

    if(oldFunction != newFunction):
        changesOccured = True
        print(f"GPIO {newNumber}'s func is now {newFunction} instead of {oldFunction}")

    if(oldFunctionSelected != newFunctionSelected):
        changesOccured = True
        print(f"GPIO {newNumber}'s fsec is now {newFunctionSelected} instead of {oldFunctionSelected}")

    if(oldAltSelected != newAltSelected):
        changesOccured = True
        print(f"GPIO {newNumber}'s alt is now {newAltSelected} instead of {oldAltSelected}")

    if(changesOccured):
        print("=================================")
#endregion

#region ------------------------------- BrSpand Detecting

def IsRightBrSpandOccupied(gpioList:list) -> bool:
    """
        Returns `True` if a card is connected.
        Returns `False` if no cards are connected.
    """

    gpio19Level:int = None
    gpio20Level:int = None
    gpio21Level:int = None

    for gpio in gpioList:
        if(gpio["gpio"] == 19):
            gpio19Level = gpio["level"]
        elif(gpio["gpio"] == 20):
            gpio20Level = gpio["level"]
        elif(gpio["gpio"] == 21):
            gpio21Level = gpio["level"]

    if(gpio19Level == 1 and gpio20Level == 1 and gpio21Level == 1):
        # Nothing is connected at all.
        return False
    else:
        return True

def IsLeftBrSpandOccupied(gpioList:list) -> bool:
    """
        Returns `True` if a card is connected.
        Returns `False` if no cards are connected.
    """

    gpio13Level:int = None
    gpio12Level:int = None
    gpio26Level:int = None
    gpio27Level:int = None

    for gpio in gpioList:
        if(gpio["gpio"] == 13):
            gpio13Level = gpio["level"]
        elif(gpio["gpio"] == 12):
            gpio12Level = gpio["level"]
        elif(gpio["gpio"] == 26):
            gpio26Level = gpio["level"]
        elif(gpio["gpio"] == 27):
            gpio27Level = gpio["level"]

    if(gpio13Level == 0 and gpio12Level == 0 and gpio26Level == 1 and gpio27Level == 1):
        # Nothing is connected at all.
        return False
    else:
        return True

def IsRightBrSpandUsable(gpioList:list) -> bool:
    """
        Returns `True` if a card is connected.
        Returns `False` if no cards are connected.
    """

    gpio19Level:int = None
    gpio20Level:int = None
    gpio21Level:int = None

    for gpio in gpioList:
        if(gpio["gpio"] == 19):
            gpio19Level = gpio["level"]
        elif(gpio["gpio"] == 20):
            gpio20Level = gpio["level"]
        elif(gpio["gpio"] == 21):
            gpio21Level = gpio["level"]

    if(gpio19Level == 0 and gpio20Level == 0 and gpio21Level == 1):
        return True
    if(gpio19Level == 0 and gpio20Level == 1 and gpio21Level == 0):
        # it aint usable
        return False

def IsLeftBrSpandUsable(gpioList:list) -> bool:
    """
        Returns `True` if a card is usable.
        Returns `False` if a card is not usable.
        Returns `None` if the inputs aren't understood
    """

    gpio13Level:int = None
    gpio12Level:int = None
    gpio26Level:int = None
    gpio27Level:int = None

    for gpio in gpioList:
        if(gpio["gpio"] == 13):
            gpio13Level = gpio["level"]
        elif(gpio["gpio"] == 12):
            gpio12Level = gpio["level"]
        elif(gpio["gpio"] == 26):
            gpio26Level = gpio["level"]
        elif(gpio["gpio"] == 27):
            gpio27Level = gpio["level"]

    if(gpio13Level == 0 and gpio12Level == 0 and gpio26Level == 0 and gpio27Level == 0):
        # Card cannot be used
        return False
    if(gpio13Level == 1 and gpio12Level == 1 and gpio26Level == 0 and gpio27Level == 0):
        # card can be used
        return True
#endregion

while True:
    currentGPIO = GetAllGPIOInformation()

    rightIsOccupied = IsRightBrSpandOccupied(currentGPIO)
    leftIsOccupied = IsLeftBrSpandOccupied(currentGPIO)
    rightCanBeUsed = IsRightBrSpandOccupied(currentGPIO)
    leftCanBeUsed = IsLeftBrSpandOccupied(currentGPIO)

    print("==============================")
    if(rightIsOccupied):
        if(rightCanBeUsed):
            print("Right: A valid BrSpand card is plugged in.")
        else:
            print("Right: An invalid BrSpand card is plugged in.")
    else:
        print("Right: Nothing is plugged in.")

    if(leftIsOccupied):
        if(leftCanBeUsed):
            print("Left: A valid BrSpand card is plugged in.")
        else:
            print("Left: An invalid BrSpand card is plugged in.")
    else:
        print("Left: Nothing is plugged in.")

    time.sleep(1)