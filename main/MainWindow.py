"""Main window of the app.

Author: Randy Paredis
Date:   03/12/2020
"""
from PyQt5 import QtWidgets, QtCore, QtGui, uic
import socketserver, datetime, re

from main.ServerDialog import ServerDialog
from main.Threading import WorkerThread

TABLE = None

class SyslogUDPHandler(socketserver.BaseRequestHandler):
    levels = {
        0: "EMERGENCY",
        1: "ALERT",
        2: "CRITICAL",
        3: "ERROR",
        4: "WARNING",
        5: "NOTICE",
        6: "INFO",
        7: "DEBUG"
    }

    facs = {
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

    colors = {
        "EMERGENCY": (255, 130, 130),
        "ALERT": (255, 130, 130),
        "CRITICAL": (255, 130, 130),
        "ERROR": (255, 153, 94),
        "WARNING": (255, 222, 130),
        "NOTICE": (130, 255, 150),
        "INFO": (130, 220, 255),
        "DEBUG": (212, 212, 212)
    }

    def handle(self):
        data = bytes.decode(self.request[0].strip())
        match = re.search(r"^<\d+>", data)
        prio = int(match.group(0)[1:-1])

        socket = self.request[1]
        f = socket.fileno()
        level = self.levels[prio ^ (f << 3)]

        global TABLE
        row = TABLE.rowCount()
        TABLE.insertRow(row)
        TABLE.setItem(row, 0, QtWidgets.QTableWidgetItem(str(datetime.date.today())))
        TABLE.setItem(row, 1, QtWidgets.QTableWidgetItem(str(datetime.datetime.now().time())))
        TABLE.setItem(row, 2, QtWidgets.QTableWidgetItem(self.facs[f]))
        TABLE.setItem(row, 3, QtWidgets.QTableWidgetItem(level))
        TABLE.setItem(row, 4, QtWidgets.QTableWidgetItem(data[match.span(0)[1]:-1]))
        for i in range(5):
            if i in [2, 3]:
                TABLE.item(row, i).setTextAlignment(QtCore.Qt.AlignCenter)
            TABLE.item(row, i).setBackground(QtGui.QColor(*self.colors[level]))

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__(flags=QtCore.Qt.WindowFlags())
        uic.loadUi("main/MainWindow.ui", self)
        self.server = None
        self.pb_change.clicked.connect(self.change)
        self.search.textChanged.connect(self.searchTable)

        global TABLE
        TABLE = self.messages

        self.thread = WorkerThread(self.run)
        self.change()

    def searchTable(self, text):
        # TODO: fancy search
        #       - Wildcards
        #       - Column selectors
        #       - ...
        global TABLE
        for r in range(TABLE.rowCount()):
            if text != "" and \
                text.lower() not in " ".join([x.lower() for x in [TABLE.item(r, i).text() for i in range(5)]]):
                TABLE.hideRow(r)
            else:
                TABLE.showRow(r)

    def change(self):
        self.end()

        dialog = ServerDialog()
        dialog.exec_()
        self.host.setText(dialog.host.text())
        self.port.setValue(dialog.port.value())

        self.start()

    def start(self):
        # TODO: catch "address already in use"
        self.server = socketserver.UDPServer((self.host.text(), self.port.value()), SyslogUDPHandler)
        self.thread.start()

    def run(self):
        # print("STARTED")
        self.server.serve_forever(poll_interval=0.5)

    def end(self):
        if self.server:
            self.server.shutdown()
            # print("ENDED")

    def closeEvent(self, QCloseEvent):
        self.end()
        super(MainWindow, self).closeEvent(QCloseEvent)