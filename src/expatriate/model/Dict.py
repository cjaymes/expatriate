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

from collections import UserDict
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Dict(UserDict):
    def __init__(self, model, element_def, *args, **kwargs):
        super(Dict, self).__init__(*args, **kwargs)
        self._model = model
        self.element_def = element_def

    def __setitem__(self, key, value):
        # remove former value from self._model._children_values
        if key in self.data:
            former_value = self.data[key]
            self._model._remove_child(former_value)

        # add new value to self._model._children_values
        self._model._append_child_for(value, self.element_def, key)

        super(Dict, self).__setitem__(key, value)

    def __delitem__(self, key):
        # remove former value from self._model._children_values
        if key in self.data:
            former_value = self.data[key]
            self._model._remove_child(former_value)

        super(Dict, self).__delitem__(key, value)

    #TODO __contains__, keys, items, values, get, __eq__, and __ne__
    #TODO setdefault

    def pop(self, key, default=None):
        if default is None:
            value = super(Dict, self).pop(key)
        else:
            value = super(Dict, self).pop(key, default)

        # remove former value from self._model._children_values
        self._model._remove_child(value)
        return value

    def popitem(self):
        key, value = super(Dict, self).popitem()

        # remove former value from self._model._children_values
        self._model._remove_child(value)
        return key, value

    def clear(self):
        for value in self.data.values():
            self._model._remove_child(value)

        super(Dict, self).clear()

    def update(self, other=None, **kwargs):
        if other is None or len(other) <= 0:
            for k,v in kwargs:
                self.__setitem__(k, v)
        else:
            for k in other:
                self.__setitem__(k, other[k])

    def setdefault(self, key, default=None):
        if default is not None and key not in self.data:
            # add new value to self._model._children_values
            self._model._append_child_for(value, self.element_def, key)

        return super(Dict, self).setdefault(key, default)
