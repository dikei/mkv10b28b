#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

from data.configuration import Configuration
from data.file_collection import FileCollection
from gui.file_collection_model import FileCollectionModel
from gui.worker import ConvertWorker, ParserWorker

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

        self.parse_worker = ParserWorker(self.file_collection)
        self.convert_worker = ConvertWorker(self.file_collection, self.config)

        self.init_gui()
        self.connect_signal()

    def init_gui(self):
        self.resize(800, 600)
        self.setWindowTitle('MKV 10bit to 8bit GUI')

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

        self.progress_dialog = QtGui.QProgressDialog("Starting..", "Cancel", 0 ,0)
        self.progress_dialog.setModal(True)
        self.progress_dialog.setWindowTitle("Converting in process..")

    def connect_signal(self):
        #Synchronize between native file_collection and file_collection_model
        self.update_file_collection.connect(self.file_collection_model.update)

        #Connect add files signal
        self.add_btn.clicked.connect(self.add_files)

        #Connect remove files signal
        self.del_btn.clicked.connect(self.remove_files)

        #Connect start convert signal
        self.start_btn.clicked.connect(self.start_convert)

        self.convert_worker.start_convert.connect(self.progress_dialog.show)
        self.parse_worker.update_status.connect(self.statusBar().showMessage)
        self.parse_worker.update_status.connect(self.progress_dialog.setLabelText)
        self.parse_worker.update_progress.connect(self.progress_dialog.setValue)
        self.parse_worker.all_done.connect(self.progress_dialog.hide)
        self.progress_dialog.canceled.connect(self.convert_worker.cancel)

    def add_files(self):
        file_paths = QtGui.QFileDialog(self).getOpenFileNames(self,
            "Choose files to convert", ".", "Matroska video (*.mkv)")
        self.file_collection.file_paths.extend(file_paths)
        self.update_file_collection.emit()

    def remove_files(self):
        select_model = self.list_view.selectionModel()
        del_paths = set(__i.data() for __i in select_model.selectedIndexes())
        new_path = [path for path in self.file_collection.file_paths if path not in del_paths]
        self.file_collection.file_paths = new_path
        self.update_file_collection.emit()

    def start_convert(self):
        self.progress_dialog.setRange(0, len(self.file_collection.file_paths))
        self.convert_worker.start()
        self.parse_worker.start()

    def closeEvent(self, QCloseEvent):
        self.config.save()
        super(MainWindow, self).closeEvent(QCloseEvent)
