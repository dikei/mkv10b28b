#!/usr/bin/env python
# -*- coding: utf-8 -*-

class FileCollection(object):

    def __init__(self):
        self.file_path = []

    def convert(self):
        raise NotImplementedError
