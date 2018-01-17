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
from expatriate.publishsubscribe import *


class SubscriberFixture(Subscriber):
    def __init__(self, *args, **kwargs):
        super(SubscriberFixture, self).__init__(*args, **kwargs)
        self.changes = []

    def _data_added(self, notifier, id_, item):
        self.changes.append(('added', id_, item))

    def _data_updated(self, notifier, id_, old_item, new_item):
        self.changes.append(('updated', id_, old_item, new_item))

    def _data_deleted(self, notifier, id_, deleted_item):
        self.changes.append(('deleted', id_, deleted_item))

wf = SubscriberFixture()
pd = PublishingDict()
pd.subscribe(wf)

def test_setitem():
    pd.clear()
    pd['test'] = 'test'
    assert wf.changes[-1] == ('added', 'test', 'test')

def test_del():
    pd.clear()
    pd['test'] = 'test'
    del pd['test']
    assert wf.changes[-1] == ('deleted', 'test', 'test')

def test_pop():
    pd.clear()
    pd['test'] = 'test'
    assert pd.pop('test') == 'test'
    assert wf.changes[-1] == ('deleted', 'test', 'test')

    assert 'test' not in pd
    with pytest.raises(KeyError):
        pd.pop('test')

def test_pop_default():
    pd.clear()
    pd['test'] = 'test'
    assert pd.pop('test', 'default') == 'test'
    assert wf.changes[-1] == ('deleted', 'test', 'test')
    assert pd.pop('test', 'default') == 'default'
    assert wf.changes[-1] == ('deleted', 'test', 'test')

def test_popitem():
    pd.clear()
    pd['test'] = 'test'
    assert pd.popitem() == ('test', 'test')
    assert wf.changes[-1] == ('deleted', 'test', 'test')

def test_clear():
    pd.clear()
    pd['test1'] = 'test1'
    pd['test2'] = 'test2'
    pd.clear()
    assert wf.changes[-2] == ('deleted', 'test1', 'test1')
    assert wf.changes[-1] == ('deleted', 'test2', 'test2')

def test_update_dict():
    pd.clear()
    pd['test1'] = 'test1'
    pd['test2'] = 'test2'
    pd.update({'test': 'test', 'test1': 'test3'})
    assert wf.changes[-2] == ('updated', 'test', None, 'test')
    assert wf.changes[-1] == ('updated', 'test1', 'test1', 'test3')

def test_update_iterator():
    pd.clear()
    pd['test1'] = 'test1'
    pd['test2'] = 'test2'
    pd.update((('test', 'test'), ('test1', 'test3')))
    assert wf.changes[-2] == ('updated', 'test', None, 'test')
    assert wf.changes[-1] == ('updated', 'test1', 'test1', 'test3')

def test_update_kwargs():
    pd.clear()
    pd['test1'] = 'test1'
    pd['test2'] = 'test2'
    pd.update(test='test', test1='test3')
    assert wf.changes[-2] == ('updated', 'test', None, 'test')
    assert wf.changes[-1] == ('updated', 'test1', 'test1', 'test3')

def test_setdefault():
    pd.clear()
    pd['test'] = 'test'
    assert pd.setdefault('test') == 'test'
    assert pd.setdefault('test2') is None
    assert wf.changes[-1] == ('added', 'test2', None)
    assert pd['test2'] is None

def test_setdefault_default():
    pd.clear()
    pd['test'] = 'test'
    assert pd.setdefault('test', 'default') == 'test'
    pd.clear()

    assert pd.setdefault('test', 'default') == 'default'
    assert wf.changes[-1] == ('added', 'test', 'default')
