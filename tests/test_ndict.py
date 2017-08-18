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

import logging
import pytest

from expatriate import *

class WatcherFixture(Watcher):
    def __init__(self, *args, **kwargs):
        super(WatcherFixture, self).__init__(*args, **kwargs)
        self.changes = []

    def added(self, notifier, addition):
        self.changes.append(('added', addition))

    def updated(self, notifier, updates):
        self.changes.append(('updated', updates))

    def deleted(self, notifier, deletion):
        self.changes.append(('deleted', deletion))

wf = WatcherFixture()
nd = NotifyingDict()
nd.notify(wf)

def test_setitem():
    nd.clear()
    nd['test'] = 'test'
    assert wf.changes[-1] == ('added', ['test'])

def test_del():
    nd.clear()
    nd['test'] = 'test'
    del nd['test']
    assert wf.changes[-1] == ('deleted', ['test'])

def test_pop():
    nd.clear()
    nd['test'] = 'test'
    assert nd.pop('test') == 'test'
    assert wf.changes[-1] == ('deleted', ['test'])

    assert 'test' not in nd
    with pytest.raises(KeyError):
        nd.pop('test')

def test_pop_default():
    nd.clear()
    nd['test'] = 'test'
    assert nd.pop('test', 'default') == 'test'
    assert wf.changes[-1] == ('deleted', ['test'])
    assert nd.pop('test', 'default') == 'default'
    assert wf.changes[-1] == ('deleted', ['test'])

def test_popitem():
    nd.clear()
    nd['test'] = 'test'
    assert nd.popitem() == ('test', 'test')
    assert wf.changes[-1] == ('deleted', ['test'])

def test_clear():
    nd.clear()
    nd['test1'] = 'test1'
    nd['test2'] = 'test2'
    nd.clear()
    assert wf.changes[-1] == ('deleted', ['test1', 'test2'])

def test_update_dict():
    nd.clear()
    nd['test1'] = 'test1'
    nd['test2'] = 'test2'
    nd.update({'test': 'test', 'test1': 'test3'})
    assert wf.changes[-1][0] == 'updated'
    assert sorted(wf.changes[-1][1]) == ['test', 'test1'])

def test_update_iterator():
    nd.clear()
    nd['test1'] = 'test1'
    nd['test2'] = 'test2'
    nd.update((('test', 'test'), ('test1', 'test3')))
    assert wf.changes[-1][0] == 'updated'
    assert sorted(wf.changes[-1][1]) == ['test', 'test1'])

def test_update_kwargs():
    nd.clear()
    nd['test1'] = 'test1'
    nd['test2'] = 'test2'
    nd.update(test='test', test1='test3')
    assert wf.changes[-1][0] == 'updated'
    assert sorted(wf.changes[-1][1]) == ['test', 'test1'])

def test_setdefault():
    nd.clear()
    nd['test'] = 'test'
    assert nd.setdefault('test') == 'test'
    assert nd.setdefault('test2') is None
    assert wf.changes[-1] == ('added', ['test2'])
    assert nd['test2'] is None

def test_setdefault_default():
    nd.clear()
    nd['test'] = 'test'
    assert nd.setdefault('test', 'default') == 'test'
    nd.clear()

    assert nd.setdefault('test', 'default') == 'default'
    assert wf.changes[-1] == ('added', ['test'])
