#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from PyQt4 import QtCore

class ConvertWorker(QtCore.QThread):

    def __init__(self, file_collection, config):
        super(ConvertWorker, self).__init__()
        self.file_collection = file_collection
        self.config = config

    def run(self):
        self.file_collection.convert(self.config.config)


class ParserWorker(QtCore.QThread):

    update_status = QtCore.pyqtSignal('QString')
    all_done = QtCore.pyqtSignal('bool')

    def __init__(self, collection):
        super(ParserWorker, self).__init__()
        self.file_collection = collection

    def run(self):
        self.all_done.emit(False)
        while not self.file_collection.all_done:
            try:
                output = self.file_collection.output_queue.pop().strip()
            except IndexError:
                output = ''
            if output:
                self.update_status.emit(output)
            time.sleep(1)
        self.update_status.emit('Done!')
        self.all_done.emit(True)
