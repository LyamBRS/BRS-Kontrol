import subprocess
import time


output = """
    GPIO 1: level=1 fsel=0 func=INPUT pull=DOWN
    GPIO 2: level=0 fsel=0 func=INPUT pull=DOWN
    GPIO 3: level=1 fsel=0 func=INPUT pull=UP
    GPIO 4: level=0 fsel=0 func=INPUT pull=UP
    GPIO 5: level=1 fsel=0 func=INPUT pull=NONE
    GPIO 6: level=1 fsel=0 func=OUTPUT pull=DOWN
    GPIO 7: level=1 fsel=0 alt=2 func=INPUT pull=DOWN
    GPIO 8: level=1 fsel=0 alt=1 func=INPUT pull=DOWN
    GPIO 9: level=1 fsel=0 alt=0 func=INPUT pull=DOWN
"""


def GetGpioNumber(line:str):

    if(type(line) != str):
        return None

    if("GPIO" not in line):
        return None

    try:
        line = line.split(":")[0]
        line = line.replace("GPIO","")
        line = int(line)
        return line
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
        print(f"GPIO {newNumber} is now {newNumber}")

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


previousGPIO = None
while True:
    if(previousGPIO == None):
        previousGPIO = GetAllGPIOInformation()
    currentGPIO = GetAllGPIOInformation()

    for gpioNumber in range(len(currentGPIO)):
        CompareAndPrintGPIODict(previousGPIO[gpioNumber], currentGPIO[gpioNumber])

    previousGPIO = currentGPIO.copy()
    time.sleep(1)
