"""Main window of the app.

Author: Randy Paredis
Date:   03/12/2020
"""
from PyQt5 import QtWidgets, QtCore, uic
from main.Extra import resource_path


class ServerDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(ServerDialog, self).__init__(parent, flags=QtCore.Qt.WindowFlags())
        uic.loadUi(resource_path("vendor", "ServerDialog.ui"), self)
