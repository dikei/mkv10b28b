#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

from data.configuration import Configuration
from data.file_collection import FileCollection
from gui.file_collection_model import FileCollectionModel

#noinspection PyOldStyleClasses
class MainWindow(QtGui.QMainWindow):

    add_files_signal = QtCore.pyqtSignal()
    update_file_collection = QtCore.pyqtSignal()

    def __init__(self):
        super(MainWindow, self).__init__()

        self.config = Configuration()
        self.config.load()

        self.file_collection = FileCollection()
        self.file_collection_model = FileCollectionModel(self.file_collection)

        self.initGUI()
        self.connect_signal()

    def initGUI(self):
        self.resize(800, 600)
        self.setWindowTitle('10bit to 8bit GUI')

        central_widget = QtGui.QWidget()
        self.setCentralWidget(central_widget)

        central_widget.setLayout(QtGui.QHBoxLayout())

        file_list = QtGui.QListView()
        file_list.setModel(self.file_collection_model)
        central_widget.layout().addWidget(file_list)

        btn_groups = QtGui.QWidget()
        central_widget.layout().addWidget(btn_groups)
        btn_groups.setLayout(QtGui.QVBoxLayout())

        self.add_btn = QtGui.QPushButton("Add files")
        btn_groups.layout().addWidget(self.add_btn)

        self.del_btn = QtGui.QPushButton("Remove files")
        btn_groups.layout().addWidget(self.del_btn)

        self.start_btn = QtGui.QPushButton("Start converting")
        btn_groups.layout().addWidget(self.start_btn)

    def connect_signal(self):
        self.update_file_collection.connect(self.file_collection_model.update)
        self.add_btn.clicked.connect(self.add_files)

    def add_files(self):
        file_paths = QtGui.QFileDialog(self).getOpenFileNames()
        self.file_collection.file_path.extend(file_paths)
        self.update_file_collection.emit()




