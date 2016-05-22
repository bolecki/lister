#!/usr/bin/env python

from __future__ import print_function

import string
import random
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
path = BASE_DIR + "/../../lister/lister/secrets.py"

# Get ascii Characters numbers and punctuation (minus quote characters as they could terminate string).
chars = ''.join([string.ascii_letters, string.digits, string.punctuation]).replace('\'', '').replace('"', '').replace('\\', '')

SECRET_KEY = ''.join([random.SystemRandom().choice(chars) for i in range(50)])

with open(path, 'wb') as file:
    file.write("SECRET_KEY = '{key}'".format(key=SECRET_KEY))
