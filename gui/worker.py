#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from PyQt4 import QtCore

class ConvertWorker(QtCore.QThread):

    start_convert = QtCore.pyqtSignal()

    def __init__(self, file_collection, config):
        super(ConvertWorker, self).__init__()
        self.file_collection = file_collection
        self.config = config

    def run(self):
        self.start_convert.emit()
        self.file_collection.convert(self.config.config)

    def cancel(self):
        self.file_collection.cancel()

class ParserWorker(QtCore.QThread):

    update_status = QtCore.pyqtSignal('QString')
    update_progress = QtCore.pyqtSignal('int')
    all_done = QtCore.pyqtSignal()

    def __init__(self, collection):
        super(ParserWorker, self).__init__()
        self.file_collection = collection

    def run(self):
        done = 0
        self.update_status.emit('Starting..')
        while not self.file_collection.all_done:
            try:
                output = self.file_collection.output_queue.pop().strip()
            except IndexError:
                output = ''
            if output:
                self.update_status.emit(output)
            if self.file_collection.file_done > done:
                done = self.file_collection.file_done
                self.update_progress.emit(done)
            time.sleep(2)
        self.update_status.emit('Done!')
        self.all_done.emit()
