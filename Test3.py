import time
import threading
import random
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug, LoadingLog
from Libraries.BRS_Python_Libraries.BRS.Utilities.Enums import Execution
from Libraries.BRS_Python_Libraries.BRS.Utilities.Information import Information
from Libraries.BRS_Python_Libraries.BRS.Utilities.bfio import BFIO, Plane, PrintPlane

hardwareRequest = Plane(20, [], [])
Debug.enableConsole = True
PrintPlane(hardwareRequest)





