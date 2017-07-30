# Copyright 2016 Casey Jaymes

# This file is part of PySCAP.
#
# PySCAP is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PySCAP is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PySCAP.  If not, see <http://www.gnu.org/licenses/>.

import importlib
import pkgutil
import sys

import expatriate

def iter_packages(pkg):
    if sys.platform != 'win32' and 'windows' in pkg.__name__.lower():
        # windows modules frequently fail to import on non-windows
        return

    for m_finder, m_name, m_ispkg in pkgutil.iter_modules(path=pkg.__path__):
        mod = importlib.import_module(pkg.__name__ + '.' + m_name, pkg.__name__)
        if m_ispkg:
            iter_packages(mod)

def test_importable():
    iter_packages(expatriate)
