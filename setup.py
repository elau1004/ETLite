# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Edward Lau <elau1004@netscape.net>
# Licensed under the MIT License.
#
from setuptools import setup, find_packages

# This is the minimal version of file to get things started
# TODO:
# add all the dependencies
# fine tune the file
setup(
    name='etlite',
    version='0.1.0',
    author='Edward Lau',
    author_email='elau1004@aim.com',
    url='https://github.com/elau1004/ETLite',

    description='A lightweight framework to host your ETL data-pipeline ',
    long_description=open('README.md').read(),
    license='MIT license',
    
    packages=find_packages(),
    include_package_data=False,
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        etlite=etlite.runner:start
    ''',
)

    
