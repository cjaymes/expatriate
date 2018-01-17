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
pd = PublishingList()
pd.subscribe(wf)

def test_setitem_int():
    pd.clear()
    pd.append('test')
    pd[0] = 'test2'
    assert wf.changes[-1] == ('updated', 0, 'test', 'test2')

def test_setitem_slice():
    pd.clear()
    pd.append('test')
    pd.append('test1')
    pd.append('test2')
    pd[1:3] = ['test3', 'test4']
    assert wf.changes[-2] == ('updated', 1, 'test1', 'test3')
    assert wf.changes[-1] == ('updated', 2, 'test2', 'test4')
    assert pd == ['test', 'test3', 'test4']

def test_del():
    pd.clear()
    pd.append('test')
    del pd[0]
    assert wf.changes[-1] == ('deleted', 0, 'test')
    assert pd == []

def test_pop():
    pd.clear()
    pd.append('test')
    assert pd.pop() == 'test'
    assert wf.changes[-1] == ('deleted', 0, 'test')
    assert pd == []

    assert len(pd) == 0
    with pytest.raises(IndexError):
        pd.pop()

def test_pop_idx():
    pd.clear()
    pd.append('test')
    pd.append('test1')
    pd.append('test2')
    assert pd.pop(1) == 'test1'
    assert wf.changes[-1] == ('deleted', 1, 'test1')
    assert pd == ['test', 'test2']

def test_clear():
    pd.clear()
    pd.append('test1')
    pd.append('test2')
    pd.clear()
    assert wf.changes[-2] == ('deleted', 0, 'test1')
    assert wf.changes[-1] == ('deleted', 1, 'test2')
    assert pd == []

def test_append():
    pd.clear()
    pd.append('test1')
    pd.append('test2')
    assert wf.changes[-2] == ('added', 0, 'test1')
    assert wf.changes[-1] == ('added', 1, 'test2')
    assert pd == ['test1', 'test2']

def test_extend():
    pd.clear()
    pd.append('test1')
    pd.append('test2')
    pd.extend(['test3', 'test4'])
    assert wf.changes[-2] == ('added', 2, 'test3')
    assert wf.changes[-1] == ('added', 3, 'test4')
    assert pd == ['test1', 'test2', 'test3', 'test4']

def test_remove():
    pd.clear()
    pd.append('test1')
    pd.append('test2')
    pd.append('test3')
    pd.remove('test2')
    assert wf.changes[-2] == ('deleted', 1, 'test2')
    assert wf.changes[-1] == ('updated', 1, 'test2', 'test3')
    assert pd == ['test1', 'test3']
