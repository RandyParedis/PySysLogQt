"""Main window of the app.

Author: Randy Paredis
Date:   03/12/2020
"""
from PyQt5 import QtWidgets, QtCore, QtGui, uic
import socketserver, datetime, re, os
import logging.handlers

from main.ServerDialog import ServerDialog
from main.Threading import WorkerThread

WINDOW = None

logging.addLevelName(25, "NOTICE")
logging.addLevelName(60, "ALERT")
logging.addLevelName(70, "EMERG")

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

COLORS = {
    "EMERGENCY": (255, 130, 130),
    "ALERT": (255, 130, 130),
    "CRITICAL": (255, 130, 130),
    "ERROR": (255, 153, 94),
    "WARNING": (255, 222, 130),
    "NOTICE": (130, 255, 150),
    "INFO": (130, 220, 255),
    "DEBUG": (212, 212, 212)
}

class SyslogUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = bytes.decode(self.request[0].strip())

        global WINDOW
        WINDOW.add(data)


from main.parser import parse
FILE_PREFIX = 'file://'
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__(flags=QtCore.Qt.WindowFlags())
        uic.loadUi("main/MainWindow.ui", self)
        self.messages.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

        self.server = None
        self.running = False
        self.contents = []
        self.search.textChanged.connect(self.searchTable)

        self.logger = logging.getLogger('PySysLogQt-TestLogger')
        self.logger.setLevel(logging.DEBUG)
        self.handler = None

        self.thread = WorkerThread(self.run)
        self.change()

        global WINDOW
        WINDOW = self

        self.action_Open.triggered.connect(self.open)
        self.action_Save.triggered.connect(self.save)
        self.action_Clear.triggered.connect(self.clear)
        self.action_Change.triggered.connect(self.change)
        self.action_Quit.triggered.connect(self.close)

        self.action_Emergency.triggered.connect(lambda: self.test("EMERG"))
        self.action_Alert.triggered.connect(lambda: self.test("ALERT"))
        self.action_Critical.triggered.connect(lambda: self.test("CRITICAL"))
        self.action_Error.triggered.connect(lambda: self.test("ERROR"))
        self.action_Warning.triggered.connect(lambda: self.test("WARNING"))
        self.action_Notice.triggered.connect(lambda: self.test("NOTICE"))
        self.action_Info.triggered.connect(lambda: self.test("INFO"))
        self.action_Debug.triggered.connect(lambda: self.test("DEBUG"))

        self.action_Id.triggered.connect(lambda b: self.messages.setColumnHidden(0, not b))
        self.action_Date.triggered.connect(lambda b: self.messages.setColumnHidden(1, not b))
        self.action_Time.triggered.connect(lambda b: self.messages.setColumnHidden(2, not b))
        self.action_Host.triggered.connect(lambda b: self.messages.setColumnHidden(3, not b))
        self.action_Application.triggered.connect(lambda b: self.messages.setColumnHidden(4, not b))
        self.action_Facility.triggered.connect(lambda b: self.messages.setColumnHidden(5, not b))
        self.action_Level.triggered.connect(lambda b: self.messages.setColumnHidden(6, not b))
        self.action_Message.triggered.connect(lambda b: self.messages.setColumnHidden(7, not b))

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
        def accept():
            self.end()
            self.clear()
            self.host.setText(dialog.host.text())
            self.port.setValue(dialog.port.value())
            self.start()

        def reject():
            if not self.running:
                self.deleteLater()

        dialog = ServerDialog(self)
        dialog.accepted.connect(accept)
        dialog.rejected.connect(reject)
        dialog.exec_()

    def clear(self):
        self.messages.setRowCount(0)
        self.contents.clear()

    def getAddress(self):
        return self.host.text(), self.port.value()

    def start(self):
        address = self.getAddress()
        if address[0].startswith(FILE_PREFIX):
            self.openFile(address[0][len(FILE_PREFIX):])
            return
        try:
            address = self.getAddress()
            self.server = socketserver.UDPServer(address, SyslogUDPHandler)
            self.handler = logging.handlers.SysLogHandler(address, facility=19)
            self.handler.priority_map = {
                "DEBUG" : "debug",
                "INFO" : "info",
                "NOTICE" : "notice",
                "WARNING" : "warning",
                "ERROR" : "error",
                "CRITICAL" : "critical",
                "ALERT" : "alert",
                "EMERG": "emerg"
            }
            self.logger.addHandler(self.handler)
            self.thread.start()
            return
        except PermissionError as e:
            QtWidgets.QMessageBox.warning(self, str(e), "You don't have permission to listen on this port.\n"
                                                        "The ports below 1024 require root access.")
        except OSError as e:
            QtWidgets.QMessageBox.warning(self, str(e), "The address '%s:%i' is already in use." %
                                          (self.host.text(), self.port.value()))

        # self.change()

    def run(self):
        self.running = True
        self.server.serve_forever(poll_interval=0.5)

    def end(self):
        if self.server:
            self.logger.removeHandler(self.handler)
            self.handler = None
            self.server.shutdown()
            self.running = False

    def closeEvent(self, QCloseEvent):
        self.end()
        super(MainWindow, self).closeEvent(QCloseEvent)

    def add(self, data):
        self.contents.append(data)
        try:
            message = parse(data)
            prio = message.header.pri
            timestamp = message.header.timestamp
            date, time = timestamp.split("T")
            msg = message.message
            host = message.header.hostname
            application = message.header.appname
        except:
            match = re.search(r"^<\d+>", data)
            prio = int(match.group(0)[1:-1])
            date = datetime.date.today()
            time = datetime.datetime.now().time()
            host = application = "unknown"
            msg = data[match.span(0)[1]:-1]

        f = prio // 8
        level = LEVELS[prio % 8]

        row = self.messages.rowCount()
        self.messages.insertRow(row)
        self.messages.setItem(row, 0, QtWidgets.QTableWidgetItem(str(row)))
        self.messages.setItem(row, 1, QtWidgets.QTableWidgetItem(str(date)))
        self.messages.setItem(row, 2, QtWidgets.QTableWidgetItem(str(time)))
        self.messages.setItem(row, 3, QtWidgets.QTableWidgetItem(host))
        self.messages.setItem(row, 4, QtWidgets.QTableWidgetItem(application))
        self.messages.setItem(row, 5, QtWidgets.QTableWidgetItem(FACS[f]))
        self.messages.setItem(row, 6, QtWidgets.QTableWidgetItem(level))
        self.messages.setItem(row, 7, QtWidgets.QTableWidgetItem(msg))
        for i in range(8):
            if i not in [7]:
                self.messages.item(row, i).setTextAlignment(QtCore.Qt.AlignCenter)
            self.messages.item(row, i).setBackground(QtGui.QColor(*COLORS[level]))

    def io(self):
        folder = os.getcwd()
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        return options, folder

    def openFile(self, filename):
        self.end()
        self.clear()
        self.host.setText("file://" + filename)
        with open(filename) as file:
            for data in file:
                data = data.rstrip()
                if len(data) > 0:
                    self.add(data.rstrip())

    # TODO: store timestamp somehow?
    def open(self):
        options, folder = self.io()
        fileName, _ = QtWidgets.QFileDialog \
            .getOpenFileName(self, "Open a File", folder, "All Files (*);;Log Files (*.log);;Text Files (*.txt)",
                             options=options)
        if fileName != "":
            self.openFile(fileName)

    def save(self):
        options, folder = self.io()
        fileName, t = QtWidgets.QFileDialog \
            .getSaveFileName(self, "Save a File", folder, "Log Files (*.log);;Text Files (*.txt);;All Files (*)",
                             options=options)
        if fileName:
            if fileName.count(".") == 0:
                ext = ".log"
                if t.count(".") == 1:
                    ext = t[t.index("."):-1]
                fileName += ext
            with open(fileName, 'w') as file:
                file.write("\n".join(self.contents))

    def test(self, level):
        self.logger.log(logging._nameToLevel[level], "TESTING " + level)
