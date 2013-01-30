#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os

class Configuration(object):

    def __init__(self):
        self.config = {
            'version': '0.1',
            'x264': '/usr/bin/x264',
            '--preset': 'veryfast',
            '--tune': 'animation',
            '--crf': '18',
            'mkvmerge': '/usr/bin/mkvmerge',
        }

    def load(self):
        try:
            with open('config.json', 'rb') as infile:
                to_load = json.load(infile)
                if to_load['version'] == self.config['version']:
                    self.config.update(to_load)
        except IOError:
            pass
        except TypeError:
            pass


    def save(self):
        with open('config.json', 'wb') as outfile:
            json.dump(self.config, outfile, indent=4)
