"""PySysLogQt entry point.

Author: Randy Paredis
Date:   03/12/2020
"""

from PyQt5 import QtWidgets
from main.MainWindow import MainWindow
import sys


if __name__ == '__main__':
    NAME = "PySysLogQt"
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName(NAME)
    app.setApplicationDisplayName(NAME)

    mainwindow = MainWindow()
    mainwindow.show()
    code = app.exec_()
