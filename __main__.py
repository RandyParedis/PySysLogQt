"""PySysLogQt entry point.

Author: Randy Paredis
Date:   03/12/2020
"""

from PyQt5 import QtWidgets
from main.MainWindow import MainWindow
from main.pysyslog import setup
import sys


if __name__ == '__main__':
    import argparse
    NAME = "PySysLogQt"

    parser = argparse.ArgumentParser(prog=NAME, description='Starts a syslog server.')
    parser.add_argument('-H', '--host', dest='host', type=str, nargs='?', const='localhost',
                        help='The host to listen on. Defaults to "localhost".')
    parser.add_argument('-P', '--port', dest='port', type=int, nargs='?', const=1024,
                        help='The port to listen on. Defaults to 1024.')
    parser.add_argument('-c', '--cli', dest='cli', action='store_true',
                        help='When set, the command line interface is used over the GUI.')
    args = parser.parse_args(sys.argv[1:])

    if args.cli:
        host = args.host
        port = args.port
        if host is None:
            host = "localhost"
        if port is None:
            port = 1024
        setup(host, port)
    else:
        app = QtWidgets.QApplication(sys.argv)
        app.setApplicationName(NAME)
        app.setApplicationDisplayName(NAME)

        mainwindow = MainWindow(args.host, args.port)
        mainwindow.show()
        code = app.exec_()
