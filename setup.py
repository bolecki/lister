#!/usr/bin/env python

from setuptools import setup

setup(
    # GETTING-STARTED: set your app name:
    name='lister',
    # GETTING-STARTED: set your app version:
    version='0.1',
    # GETTING-STARTED: set your app description:
    description='OpenShift Lister App',
    # GETTING-STARTED: set author name (your name):
    author='Brian Olecki',
    # GETTING-STARTED: set author email (your email):
    author_email='bolecki019@gmail.com',
    # GETTING-STARTED: set author url (your url):
    url='https://github.com/bolecki',
    # GETTING-STARTED: define required django version:
    install_requires=[
        'Django==1.8.4'
    ],
    dependency_links=[
        'https://pypi.python.org/simple/django/'
    ],
)
