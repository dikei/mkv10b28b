#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore

#noinspection PyOldStyleClasses
class FileCollectionModel(QtGui.QStandardItemModel):

    def __init__(self, file_collection):
        super(FileCollectionModel, self).__init__()
        self.file_collection = file_collection

    def update(self):
        self.clear()
        for file in self.file_collection.file_paths:
            self.appendRow(QtGui.QStandardItem(file))

