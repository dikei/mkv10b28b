#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Queue import Queue
from collections import deque
from subprocess import Popen, PIPE, STDOUT
from threading import Thread, Event
import os
import sys
import logging

logger = logging.getLogger(__name__)
ON_POSIX = 'posix' in sys.builtin_module_names


def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        logger.debug(line)
        queue.append(line)
    out.close()


class FileCollection(object):

    def __init__(self):
        self.file_paths = []
        self.output_queue = deque()
        self.file_done = 0
        self.all_done = False
        self.cancel_event = Event()
        self.process = None

    def reset(self):
        self.all_done = False
        self.file_done = 0
        self.output_queue.clear()
        self.cancel_event.clear()

    def convert(self, config):
        self.reset()
        for file_path in self.file_paths:
            if self.cancel_event.is_set():
                break
            basename = os.path.basename(file_path)
            dirname = os.path.dirname(file_path)
            outfile_path = os.path.join(dirname, '[8bit]' + basename)
            try:
                self.process = Popen(
                    [config['x264'], '--preset', config['preset'], '--tune',
                     config['tune'], '--crf', config['crf'], '--quiet',
                     file_path, '--output', outfile_path], stdout=PIPE,
                    stderr=STDOUT, bufsize=1, close_fds=ON_POSIX,
                    universal_newlines=True)
                t = Thread(target=enqueue_output, args=(self.process.stdout, self.output_queue))
                t.daemon = True
                t.start()
                self.process.wait()
            finally:
                self.file_done += 1
        self.all_done = True

    def cancel(self):
        self.cancel_event.set()
        if self.process is not None:
            self.process.terminate()
