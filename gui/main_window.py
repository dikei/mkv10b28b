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

        self.init_gui()
        self.connect_signal()

    def init_gui(self):
        self.resize(800, 600)
        self.setWindowTitle('10bit to 8bit GUI')

        self.setCentralWidget(QtGui.QWidget())

        self.centralWidget().setLayout(QtGui.QHBoxLayout())

        self.list_view = QtGui.QListView()
        self.list_view.setModel(self.file_collection_model)
        self.list_view.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)

        self.centralWidget().layout().addWidget(self.list_view)

        btn_groups = QtGui.QWidget()
        self.centralWidget().layout().addWidget(btn_groups)
        btn_groups.setLayout(QtGui.QVBoxLayout())

        self.add_btn = QtGui.QPushButton("Add files")
        btn_groups.layout().addWidget(self.add_btn)

        self.del_btn = QtGui.QPushButton("Remove files")
        btn_groups.layout().addWidget(self.del_btn)

        self.start_btn = QtGui.QPushButton("Start converting")
        btn_groups.layout().addWidget(self.start_btn)

    def connect_signal(self):
        #Synchronize between native file_collection and file_collection_model
        self.update_file_collection.connect(self.file_collection_model.update)

        #Connect add files signal
        self.add_btn.clicked.connect(self.add_files)

        #Connect remove files signal
        self.del_btn.clicked.connect(self.remove_files)

    def add_files(self):
        file_paths = QtGui.QFileDialog(self).getOpenFileNames()
        self.file_collection.file_path.extend(file_paths)
        self.update_file_collection.emit()

    def remove_files(self):
        select_model = self.list_view.selectionModel()
        del_paths = set(__i.data() for __i in select_model.selectedIndexes())
        new_path = [path for path in self.file_collection.file_path if path not in del_paths]
        self.file_collection.file_path = new_path
        self.update_file_collection.emit()


