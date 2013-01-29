#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sip
api_v2 = ['QDate', 'QDateTime', 'QString', 'QTextStream',
          'QTime', 'QUrl', 'QVariant']
for api in api_v2:
    sip.setapi(api, 2)

import sys
from PyQt4 import QtGui, QtCore
from gui.main_window import MainWindow

def main():
    app = QtGui.QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
