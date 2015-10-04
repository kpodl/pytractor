#!/usr/bin/env python
# Copyright 2014 Konrad Podloucky
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Setuptools script for building pytractor.
"""

from setuptools import setup, find_packages
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pytractor',

    version='0.1.0',

    description='Selenium testing for Angular.js apps',
    long_description=long_description,

    url='https://github.com/kpodl/pytractor',

    author='Konrad Podloucky',
    author_email='konrad+pytractor@crunchy-frog.org',

    license='Apache 2.0',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',

        'License :: OSI Approved :: Apache Software License',

        'Programming Language :: Python :: 2.7',
    ],

    keywords='selenium angular.js testing',

    package_dir={'': 'src'},

    packages=find_packages('src'),

    # For package data see MANIFEST.in
    include_package_data=True,

    install_requires=[
        'selenium>=2.47.3'
    ],

    tests_require = [
        'nose>=1.3.7',
        'mock>=1.0.1,<1.1.0'  # >= 1.1.0 seems to be broken.
    ],
    test_suite = 'nose.collector'
)
