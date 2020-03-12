"""Main window of the app.

Author: Randy Paredis
Date:   03/12/2020
"""
from PyQt5 import QtWidgets, QtCore, uic


class ServerDialog(QtWidgets.QDialog):
    def __init__(self):
        super(ServerDialog, self).__init__(flags=QtCore.Qt.WindowFlags())
        uic.loadUi("main/ServerDialog.ui", self)