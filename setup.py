#!/usr/bin/env python

# Copyright 2016 Casey Jaymes

# This file is part of Expatriate.
#
# Expatriate is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Expatriate is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Expatriate.  If not, see <http://www.gnu.org/licenses/>.

from glob import glob
from os.path import join
from os.path import dirname
import re
from setuptools import find_packages
from setuptools import setup

with open(join(dirname(__file__), 'README.md'), 'r') as f:
    readme = f.read()

try:
   import pypandoc
   with open(join(dirname(__file__), 'README.rst'), 'w') as f:
       f.write(pypandoc.convert('README.md', 'rst'))
except (IOError, ImportError):
   pass

with open(join(dirname(__file__), 'CHANGELOG.md'), 'r') as f:
    changelog = f.read()

try:
   import pypandoc
   with open(join(dirname(__file__), 'CHANGELOG.rst'), 'w') as f:
       f.write(pypandoc.convert('CHANGELOG.md', 'rst'))
except (IOError, ImportError):
   pass

with open(join(dirname(__file__), 'requirements.txt'), 'r') as f:
    install_requires = list(f)

setup(name='Expatriate',
    version='0.1',
    license='LGPL',
    description='Library wrapping expat for parsing and generating XML',
    long_description='%s\n%s' % (
        re.compile('^.. start-badges.*^.. end-badges', re.M | re.S).sub('', readme),
        re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', changelog),
    ),
    author='Casey Jaymes',
    author_email='cjaymes@gmail.com',
    url='https://github.com/cjaymes/expatriate',
    packages=find_packages(),
    classifiers=[
        # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 3 - Alpha',

        'Environment :: Other Environment',

        'Intended Audience :: Developers',

        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',

        'Operating System :: OS Independent',

        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',

        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Markup :: XML',
    ],
    keywords=[
        'XML',
    ],
    #python_requires='>=3.5',
    install_requires=install_requires,
    tests_require=[
        'pytest',
    ],
    zip_safe=True,
    include_package_data=True,
)
