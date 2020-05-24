"""This file contains variables and functions that can be called from anywhere.

Author: Randy Paredis
Date:   05/24/2020
"""

import sys, os

LEVELS = {
    0: "EMERGENCY",
    1: "ALERT",
    2: "CRITICAL",
    3: "ERROR",
    4: "WARNING",
    5: "NOTICE",
    6: "INFO",
    7: "DEBUG"
}

RLEVELS = { LEVELS[k]:k for k in LEVELS }
RLEVELS["EMERG"] = 0
RLEVELS["INFORMATION"] = 6

FACS = {
    0: "Kernel",
    1: "User-Level",
    2: "Mail System",
    3: "System Daemons",
    4: "Security 1",
    5: "Internal",
    6: "Line Printer",
    7: "Network News",
    8: "UUCP",
    9: "Clock Daemon",
    10: "Security 2",
    11: "FTP Daemon",
    12: "NTP",
    13: "Log Audit",
    14: "Log Alert",
    15: "Scheduling",
    16: "Local 0",
    17: "Local 1",
    18: "Local 2",
    19: "Local 3",
    20: "Local 4",
    21: "Local 5",
    22: "Local 6",
    23: "Local 7"
}

RFACS = { FACS[k]:k for k in FACS}



def resource_path(*relative_paths):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, *relative_paths)
