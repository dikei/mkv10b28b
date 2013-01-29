#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os

class Configuration(object):

    def __init__(self):
        self.config = {}

    def load(self):
        try:
            with open('config.json', 'rb') as infile:
                self.config = json.loads(infile)
        except IOError:
            pass
        except TypeError:
            pass


    def save(self):
        with open('config.json', 'wb') as outfile:
            self.config = json.dumps(outfile)
