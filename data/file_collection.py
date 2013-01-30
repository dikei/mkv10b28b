#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Queue import Queue
from collections import deque
from subprocess import Popen, PIPE, STDOUT
from threading import Thread
import os
import sys

def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.append(line)
    out.close()

ON_POSIX = 'posix' in sys.builtin_module_names

class FileCollection(object):

    def __init__(self):
        self.file_paths = []
        self.output_queue = deque()
        self.file_done = 0
        self.all_done = False

    def convert(self, config):
        self.all_done = False
        for file_path in self.file_paths:
            basename = os.path.basename(file_path)
            dirname = os.path.dirname(file_path)
            outfile_path = os.path.join(dirname, '[8bit]' + basename)
            try:
                p = Popen([config['x264'],
                           '--preset', config['preset'],
                           '--tune', config['tune'],
                           '--crf', config['crf'],
                           '--quiet',
                           file_path, '--output', outfile_path],
                          stdout=PIPE,
                          stderr=STDOUT,
                          bufsize=1, close_fds=ON_POSIX,
                          universal_newlines=True)
                t = Thread(target=enqueue_output, args=(p.stdout, self.output_queue))
                t.daemon = True
                t.start()
                p.wait()
            finally:
                self.file_done += 1
        self.all_done = True
        self.output_queue.clear()
