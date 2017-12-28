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

from collections import UserList
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class List(UserList):
    def __init__(self, model, element_def, *args, **kwargs):
        super(List, self).__init__(*args, **kwargs)
        self._model = model
        self.element_def = element_def

    def __setitem__(self, index, value):
        # remove former value from self._model._children_values
        if index < len(self.data):
            former_value = self.data[index]
            self._model._remove_child(former_value)

        # add new value to self._model._children_values
        self._model._append_child_for(value, self.element_def)

        super(List, self).__setitem__(index, value)

    def __delitem__(self, index):
        # remove former value from self._model._children_values
        if index < len(self.data):
            former_value = self.data[index]
            self._model._remove_child(former_value)

        super(List, self).__delitem__(index)

    def insert(self, index, value):
        # add new value to self._model._children_values
        self._model._append_child_for(value, self.element_def)

        super(List, self).insert(index, value)

    #TODO __contains__, __iter__, __reversed__, index, and count
    #TODO reverse, and __iadd__

    def append(self, value):
        # add new value to self._model._children_values
        self._model._append_child_for(value, self.element_def)

        super(List, self).append(value)

    def extend(self, lst):
        for value in lst:
            # add new value to self._model._children_values
            self._model._append_child_for(value, self.element_def)

        super(List, self).extend(lst)

    def pop(self, i=-1):
        value = super(List, self).pop(i)

        # remove former value from self._model._children_values
        self._model._remove_child(value)
        return value

    def remove(self, value):
        # remove former value from self._model._children_values
        self._model._remove_child(value)

        super(List, self).remove(value)
