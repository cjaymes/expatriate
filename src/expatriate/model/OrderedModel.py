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

import expatriate
import importlib
import logging
import os.path
import re
import sys

from .Model import Model
from .List import List as ModelList
from .Dict import Dict as ModelDict
from .Child import Child as ModelChild
from .decorators import *
from .exceptions import *

logger = logging.getLogger(__name__)

class OrderedModel(Model):
    def __init__(self):
        # child_map must be first to prevent recursion of __getattr__
        self._child_map = {}
        self._children_values = []
        self._children_el_defs = []
        self._children_keys = []

        self._references = {}

        super().__init__()

    def __setattr__(self, name, value):
        '''
        setattr override to keep track of indexes etc.
        '''

        try:
            object.__getattribute__(self, '_child_map')
        except:
            # not initialzed yet, just pass through
            object.__setattr__(self, name, value)

        # keep index of 'id' attrs
        if name == 'id':
            if self._parent is not None:
                self._parent._references[value] = self
        if name == 'parent' and hasattr(self, 'id'):
            self._parent._references[self.id] = self

        if name in self._child_map:
            # capture element assignment
            el_def = self._child_map[name].el_def
            if isinstance(self._child_map[name], ModelList):
                if isinstance(value, list):
                    # wrap in ModelList
                    self._child_map[name] = ModelList(self, el_def, value)
                else:
                    raise ValueError('Trying to assign ' + value.__class__.__name__ + ' type to ' + name + ' attribute, but expecting list')
            elif isinstance(self._child_map[name], ModelDict):
                if isinstance(value, dict):
                    # wrap in ModelDict
                    self._child_map[name] = ModelDict(self, el_def, value)
                else:
                    raise ValueError('Trying to assign ' + value.__class__.__name__ + ' type to ' + name + ' attribute, but expecting dict')
            elif isinstance(self._child_map[name], ModelChild):
                # wrapped in ModelChild
                self._remove_child(self._child_map[name].value)
                self._child_map[name].value = value
                self._append_child_for(value, self._child_map[name].el_def)
            else:
                raise ValueError('Child map entry for ' + name + ' is set to an unsupported type')
        else:
            # process as regular attribute
            object.__setattr__(self, name, value)

    def __getattr__(self, name):
        '''
        getattr override to keep track of indexes etc.
        '''

        try:
            object.__getattribute__(self, '_child_map')
        except:
            # not initialzed yet, just return __getattribute__
            return object.__getattribute__(self, name)

        if name in self._child_map:
            if isinstance(self._child_map[name], ModelChild):
                return self._child_map[name].value
            else:
                return self._child_map[name]
        else:
            raise AttributeError('Attribute ' + name + ' was not found in '
                + self.__class__.__name__ + ': ' + str(self._child_map.keys()))

    def _append_child_for(self, value, el_def, key=None):
        self._children_values.append(value)
        self._children_el_defs.append(el_def)
        self._children_keys.append(key)

    def _remove_child(self, value):
        try:
            i = self._children_values.index(value)
            del self._children_values[i]
            del self._children_el_defs[i]
            del self._children_keys[i]
        except ValueError:
            pass

    def find_reference(self, ref):
        '''
        find child that matches reference *ref*
        '''

        if ref in self._references:
            return self._references[ref]
        else:
            for c in self._children_values:
                try:
                    return c.find_reference(ref)
                except:
                    pass

        raise ReferenceException('Could not find reference ' + ref
            + ' within ' + str(self))
