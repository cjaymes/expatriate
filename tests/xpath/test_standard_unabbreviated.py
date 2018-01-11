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

logging.basicConfig(level=logging.DEBUG)

doc = Document()
doc.parse('''<?xml version='1.0' encoding='utf-8'?>
<doc xmlns="http://jaymes.biz">
    <chapter name="[0]">
        <title name="[0][0]">Figures</title>
        <figure name="[0][1]">1</figure>
        <figure name="[0][2]">2</figure>
        <figure name="[0][3]">3</figure>
        <figure name="[0][4]">4</figure>
        <figure name="[0][5]">5</figure>
        <figure name="[0][6]">6</figure>
        <figure name="[0][7]">7</figure>
        <figure name="[0][8]">8</figure>
        <figure name="[0][9]">9</figure>
        <figure name="[0][10]">10</figure>
        <figure name="[0][11]">11</figure>
        <figure name="[0][12]">12</figure>
        <figure name="[0][13]">13</figure>
        <figure name="[0][14]">14</figure>
        <figure name="[0][15]">15</figure>
        <figure name="[0][16]">16</figure>
        <figure name="[0][17]">17</figure>
        <figure name="[0][18]">18</figure>
        <figure name="[0][19]">19</figure>
    </chapter>
    <chapter name="[1]" type="information">
        <title name="[1][0]">Introduction</title>
        text node [1][1]
        <div name="[1][2]">
            <div name="[1][2][0]">
                <para name="[1][2][0][0]" type="warning">Context para 1</para>
                <para name="[1][2][0][1]">text node [1][2][0][1][0]</para>
                <para name="[1][2][0][2]" type="warning">
                    text node [1][2][0][2][0]
                    <para name="[1][2][0][2][1]"></para>
                </para>
            </div>
            <para name="[1][2][1]">Context para 3</para>
            <figure name="[1][2][2]"></figure>
            <figure name="[1][2][3]"></figure>
            <figure name="[1][2][4]"></figure>
            <figure name="[1][2][5]"></figure>
            <figure name="[1][2][6]"></figure>
            <figure name="[1][2][7]"></figure>
            <figure name="[1][2][8]"></figure>
            <figure name="[1][2][9]"></figure>
            <figure name="[1][2][10]"></figure>
            <figure name="[1][2][11]"></figure>
        </div>
        <para name="[1][3]">text node [1][3][0]</para>
        <para name="[1][4]">text node [1][4][0]</para>
    </chapter>
    <chapter name="[2]">
        <title name="[2][0]">text node [2][0][0]</title>
        <para name="[2][1]" type="warning">text node [2][1][0]</para>
        <para name="[2][2]" type="warning">text node [2][2][0]</para>
        <figure name="[2][3]">30</figure>
        <figure name="[2][4]">31</figure>
        <figure name="[2][5]">32</figure>
        <figure name="[2][6]">33</figure>
        <figure name="[2][7]">34</figure>
        <figure name="[2][8]">35</figure>
        <figure name="[2][9]">36</figure>
        <figure name="[2][10]">37</figure>
        <figure name="[2][11]">38</figure>
        <figure name="[2][12]">39</figure>
    </chapter>
    <chapter name="[3]">
        <title name="[3][0]">text node [3][0][0]</title>
        <para name="[3][1]" type="warning">text node [3][1][0]</para>
        <para name="[3][2]" type="warning">text node [3][2][0]</para>
        <olist name="[3][3]">
            <item name="[3][3][0]">text node [3][3][0][0]</item>
            <item name="[3][3][1]">text node [3][3][0][1]</item>
        </olist>
        <para name="[3][4]" type="warning">text node [3][4][0]</para>
        <para name="[3][5]" type="warning">text node [3][5][0]</para>
        <para name="[3][6]">text node [3][6][0]</para>
        <figure name="[3][7]">40</figure>
        <figure name="[3][8]">41</figure>
        <figure name="[3][9]">42</figure>
        <para name="[3][10]" type="warning">text node [3][10][0]</para>
    </chapter>
    <chapter name="[4]">
        <title name="[4][0]">text node [4][0][0]</title>
        <section name="[4][1]">
        </section>
        <section name="[4][2]">
        </section>
    </chapter>
    <appendix name="[5]">
        <title name="[5][0]">text node [5][0][0]</title>
        <employee name="[5][1]" secretary="Jane">John</employee>
        <employee name="[5][2]">Jane</employee>
        <employee name="[5][3]" secretary="Charles" assistant="Cecil">Charleen</employee>
        <employee name="[5][4]">Charles</employee>
        <employee name="[5][5]" assistant="Chuck">Cecil</employee>
    </appendix>
    <appendix name="[6]">
    </appendix>
    <appendix name="[7]">
    </appendix>
</doc>
''')

@pytest.mark.parametrize(
    "test, result",
    (
        # 0
        (doc.root_element[1].xpath('child::para'), [
            doc.root_element[1][3],
            doc.root_element[1][4],
        ]),
        # 1
        (doc.root_element[1].xpath('child::*'), [
            doc.root_element[1][0],
            doc.root_element[1][2],
            doc.root_element[1][3],
            doc.root_element[1][4],
        ]),
        # 2
        (doc.root_element[1].xpath('child::text()'), [
            doc.root_element[1][1],
        ]),
        # 3
        (doc.root_element[1].xpath('child::node()'), [
            doc.root_element[1][0],
            doc.root_element[1][1],
            doc.root_element[1][2],
            doc.root_element[1][3],
            doc.root_element[1][4],
        ]),
        # 4
        (doc.root_element[1].xpath('attribute::name'), [
            doc.root_element[1].attribute_nodes['name'],
        ]),
        # 5
        (doc.root_element[1].xpath('attribute::name'), [
            doc.root_element[1].attribute_nodes['name'],
        ]),
        # 6
        (doc.root_element[1].xpath('attribute::*'), [
            doc.root_element[1].attribute_nodes['name'],
            doc.root_element[1].attribute_nodes['type'],
        ]),
        # 7
        (doc.root_element[1].xpath('descendant::para'), [
            doc.root_element[1][2][0][0],
            doc.root_element[1][2][0][1],
            doc.root_element[1][2][0][2],
            doc.root_element[1][2][0][2][1],
            doc.root_element[1][2][1],
            doc.root_element[1][3],
            doc.root_element[1][4],
        ]),
        # 8
        (doc.root_element[1][2][0][0].xpath('ancestor::div'), [
            doc.root_element[1][2][0],
            doc.root_element[1][2],
        ]),
        # 9
        (doc.root_element[1][2][0].xpath('ancestor-or-self::div'), [
            doc.root_element[1][2][0],
            doc.root_element[1][2],
        ]),
        # 10
        (doc.root_element[1][2].xpath('ancestor-or-self::div'), [
            doc.root_element[1][2],
        ]),
        # 11
        (doc.root_element[1][2][0][2].xpath('descendant-or-self::para'), [
            doc.root_element[1][2][0][2],
            doc.root_element[1][2][0][2][1],
        ]),
        # 12
        (doc.root_element[1][2][0][2].xpath('self::para'), [
            doc.root_element[1][2][0][2],
        ]),
        # 13
        (doc.root_element[1].xpath('self::para'), [
        ]),
        # 14
        (doc.root_element.xpath('child::chapter/descendant::para'), [
            doc.root_element[1][2][0][0],
            doc.root_element[1][2][0][1],
            doc.root_element[1][2][0][2],
            doc.root_element[1][2][0][2][1],
            doc.root_element[1][2][1],
            doc.root_element[1][3],
            doc.root_element[1][4],
            doc.root_element[2][1],
            doc.root_element[2][2],
            doc.root_element[3][1],
            doc.root_element[3][2],
            doc.root_element[3][4],
            doc.root_element[3][5],
            doc.root_element[3][6],
            doc.root_element[3][10],
        ]),
        # 15
        (doc.root_element.xpath('child::*/child::para'), [
            doc.root_element[1][3],
            doc.root_element[1][4],
            doc.root_element[2][1],
            doc.root_element[2][2],
            doc.root_element[3][1],
            doc.root_element[3][2],
            doc.root_element[3][4],
            doc.root_element[3][5],
            doc.root_element[3][6],
            doc.root_element[3][10],
        ]),
        # 16
        (doc.root_element.xpath('/'), [
            doc,
        ]),
        # 17
        (doc.root_element.xpath('/descendant::para'), [
            doc.root_element[1][2][0][0],
            doc.root_element[1][2][0][1],
            doc.root_element[1][2][0][2],
            doc.root_element[1][2][0][2][1],
            doc.root_element[1][2][1],
            doc.root_element[1][3],
            doc.root_element[1][4],
            doc.root_element[2][1],
            doc.root_element[2][2],
            doc.root_element[3][1],
            doc.root_element[3][2],
            doc.root_element[3][4],
            doc.root_element[3][5],
            doc.root_element[3][6],
            doc.root_element[3][10],
        ]),
        # 18
        (doc.root_element[3].xpath('/descendant::olist/child::item'), [
            doc.root_element[3][3][0],
            doc.root_element[3][3][1],
        ]),
        # 19
        (doc.root_element[3].xpath('child::para[position()=1]'), [
            doc.root_element[3][1],
        ]),
        # 20
        (doc.root_element[3].xpath('child::para[position()=last()]'), [
            doc.root_element[3][10],
        ]),
        # 21
        (doc.root_element[3].xpath('child::para[position()=last()-1]'), [
            doc.root_element[3][6],
        ]),
        # 22
        (doc.root_element[3].xpath('child::para[position()>1]'), [
            doc.root_element[3][2],
            doc.root_element[3][4],
            doc.root_element[3][5],
            doc.root_element[3][6],
            doc.root_element[3][10],
        ]),
        # 23
        (doc.root_element[0].xpath('following-sibling::chapter[position()=1]'), [
            doc.root_element[1],
        ]),
        # 24
        (doc.root_element[2].xpath('preceding-sibling::chapter[position()=1]'), [
            doc.root_element[1],
        ]),
        # 25
        (doc.root_element.xpath('/descendant::figure[position()=42]'), [
            doc.root_element[3][9],
        ]),
        # 26
        (doc.root_element.xpath('/child::doc/child::chapter[position()=5]/child::section[position()=2]'), [
            doc.root_element[4][2],
        ]),
        # 27
        (doc.root_element[3].xpath('child::para[attribute::type="warning"]'), [
            doc.root_element[3][1],
            doc.root_element[3][2],
            doc.root_element[3][4],
            doc.root_element[3][5],
            doc.root_element[3][10],
        ]),
        # 28
        (doc.root_element[3].xpath('child::para[attribute::type=\'warning\'][position()=5]'), [
            doc.root_element[3][10],
        ]),
        # 29
        (doc.root_element[3].xpath('child::para[position()=5][attribute::type="warning"]'), [
        ]),
        # 30
        (doc.root_element[3].xpath('child::para[position()=4][attribute::type="warning"]'), [
            doc.root_element[3][5],
        ]),
        # 31
        (doc.root_element.xpath('child::chapter[child::title=\'Introduction\']'), [
            doc.root_element[1],
        ]),
        # 32
        (doc.root_element.xpath('child::chapter[child::title]'), [
            doc.root_element[0],
            doc.root_element[1],
            doc.root_element[2],
            doc.root_element[3],
            doc.root_element[4],
        ]),
        # 33
        (doc.root_element.xpath('child::*[self::chapter or self::appendix]'), [
            doc.root_element[0],
            doc.root_element[1],
            doc.root_element[2],
            doc.root_element[3],
            doc.root_element[4],
            doc.root_element[5],
            doc.root_element[6],
            doc.root_element[7],
        ]),
        # 34
        (doc.root_element.xpath('child::*[self::chapter or self::appendix][position()=last()]'), [
            doc.root_element[7],
        ]),
    )
)
def test_xpath(test, result):
    assert test == result
