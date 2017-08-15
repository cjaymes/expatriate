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
import math
import re

from .xpath import *

logger = logging.getLogger(__name__)

class Node(object):
    def __init__(self, document=None, document_order=-1, parent=None):
        self._document = document
        self._document_order = document_order
        self.parent = parent

    def resolve_prefix(self, prefix):
        if self.parent is not None:
            return self.parent.resolve_prefix(prefix)
        else:
            raise UnknownPrefixException('Unknown prefix: ' + str(prefix))

    def namespace_prefix(self, namespace_uri):
        if self.parent is not None:
            return self.parent.namespace_prefix(namespace_uri)
        else:
            raise UnknownNamespaceException('Unknown namespace uri: ' + str(namespace_uri))

    def _parse_name(self):
        if ':' in self.name:
            prefix, colon, local_name = self.name.partition(':')

            namespace = self.resolve_prefix(prefix)
        else:
            prefix = None
            namespace = self.resolve_prefix(prefix)
            local_name = self.name

        # using object.__setattr__ for __setattr__ safety
        object.__setattr__(self, 'prefix', prefix)
        object.__setattr__(self, 'namespace', namespace)
        object.__setattr__(self, 'local_name', local_name)

    def __setattr__(self, name, value):
        if name == 'name':
            object.__setattr__(self, name, value)
            self._parse_name()
        elif name == 'prefix':
            object.__setattr__(self, name, value)
            object.__setattr__(self, 'namespace', self.resolve_prefix(prefix))
            if self.prefix is not None:
                object.__setattr__(self, 'name', self.prefix + ':' + self.local_name)
        elif name == 'namespace':
            object.__setattr__(self, name, value)
            if self.namespace is not None:
                object.__setattr__(self, 'prefix', self.namespace_prefix(self.namespace))
            if self.prefix is not None:
                object.__setattr__(self, 'name', prefix + ':' + self.local_name)
        elif name == 'local_name':
            object.__setattr__(self, name, value)
            if self.prefix is not None:
                object.__setattr__(self, 'name', prefix + ':' + self.local_name)
        else:
            object.__setattr__(self, name, value)

    def _tokenize(self, expr):
        tokens = []

        parens = 0
        braces = 0

        t = ''
        for i, char in enumerate(expr):
            if len(t) > 0:
                if t[0] in '\'"':
                    # string literal
                    t += char
                    if char == t[0] and t[-1] != '\\':
                        tokens.append(t)
                        t = ''
                elif t == '-':
                    tokens.append(t)
                    t = char
                elif t == '.' and char != '.':
                    tokens.extend(['self', '::', 'node', '(', ')'])
                    t = char
                elif re.fullmatch(r'[0-9][0-9.]*', t) and (char.isdigit() or char == '.'):
                    t += char
                elif t[0] == '$' and char.isalpha():
                    t += char
                elif t.isspace():
                    # skip space
                    t = char
                elif t in ':/.!<>':
                    if t + char in ['::', '//', '..', '!=', '<=', '>=']:
                        t += char
                        if t == '//':
                            tokens.extend(['/', 'descendant-or-self', '::', 'node', '(', ')', '/'])
                        elif t == '..':
                            tokens.extend(['parent', '::', 'node', '(', ')'])
                        else:
                            tokens.append(t)
                        t = ''
                    else:
                        tokens.append(t)
                        t = char
                elif t == '@':
                    tokens.extend(['attribute', '::'])
                    t = char
                elif t == '(':
                    tokens.append(t)
                    t = char
                    parens += 1
                elif t == ')':
                    tokens.append(t)
                    t = char
                    parens -= 1
                elif t == '[':
                    tokens.append(t)
                    t = char
                    braces += 1
                elif t == ']':
                    tokens.append(t)
                    t = char
                    braces -= 1
                elif t in ',\'"*|+=':
                    tokens.append(t)
                    t = char
                elif char.isalnum() or char == '-':
                    t += char
                else:
                    tokens.append(t)
                    t = char
            else:
                if char.isspace():
                    continue
                t += char

        # append final token if there is one
        if t == '.':
            tokens.extend(['self', '::', 'node', '(', ')'])
        elif t.isspace():
            pass
        elif t == ')':
            tokens.append(t)
            parens -= 1
        elif t == ']':
            tokens.append(t)
            braces -= 1
        elif t != '':
            tokens.append(t)

        if parens != 0 or braces != 0:
            raise XPathSyntaxException('Paren or brace expression not closed')

        return tokens

    def xpath(self, expr, version=1.0, variables={}, add_functions={}):
        if version != 1.0:
            raise NotImplementedError('Only XPath 1.0 has been implemented')

        if self._document is None:
            raise ValueError("Can't resolve xpath expression on Node not attached to a document")

        logger.debug('********************************************')
        logger.debug('Tokenizing xpath expression: ' + str(expr))

        tokens = self._tokenize(expr)
        logger.debug('Tokens: ' + str(tokens))

        functions = Function.FUNCTIONS.copy()
        functions.update(add_functions)

        stack = []
        for i, token in enumerate(tokens):
            if token == '(':
                e = Expression()
                logger.debug('Starting sub expression ' + str(e))
                stack.append(e)
            elif token == ')':
                if len(stack) <= 1:
                    continue

                logger.debug('End of ' + str(stack[-1]))
                if i > 0 and tokens[i-1] == '(':
                    # don't add empty Expression
                    stack.pop()
                    logger.debug('Ignoring empty expression')
                elif len(stack) > 1:
                    e = stack.pop()
                    logger.debug('Adding ' + str(e) + ' to ' + str(stack[-1]))
                    stack[-1].children.append(e)
                # else just let it on the stack
            elif token == '[':
                p = Predicate()
                stack.append(p)
                logger.debug('Starting predicate ' + str(p))
                e = Expression()
                stack.append(e)
                logger.debug('Starting sub expression ' + str(e))
            elif token == ']':
                logger.debug('End of ' + str(stack[-1]))
                if i > 0 and tokens[i-1] == '[':
                    # don't add empty predicate
                    stack.pop()
                    stack.pop()
                    logger.debug('Ignoring empty expression & predicate')
                else:
                    while(len(stack) > 1 and not isinstance(stack[-1], Predicate)):
                        i = stack.pop()
                        logger.debug('Adding ' + str(i) + ' to ' + str(stack[-1]))
                        stack[-1].children.append(i)
                    p = stack.pop()
                    if not isinstance(stack[-1], Axis):
                        raise SyntaxException('Expecting Axis on stack before predicate')
                    logger.debug('Adding ' + str(p) + ' to ' + str(stack[-1]))
                    stack[-1].children.append(p)
            elif token  == '::':
                # already processed axis
                pass
            elif token == ':':
                # already processed QNameNodeTest
                pass
            elif token == '*':
                if i > 0 and tokens[i-1] not in [
                    '::', '(', '[', ',', 'and', 'or', 'mod', 'div',
                    '*', '/', '//', '|', '+', '-', '=', '!=', '<', '<=',
                    '>', '>=']:
                    o = Operator(token)
                    o.children.append(stack.pop())
                    stack.append(o)
                    logger.debug('Pushed ' + str(stack[-1]) + ' on stack')
                else:
                    if len(stack) == 0 or not isinstance(stack[-1], Axis):
                        # use implicit axis
                        a = Axis('child')
                        stack.append(a)
                        logger.debug('Pushed ' + str(stack[-1]) + ' on stack')
                    nt = AnyNodeTest(stack[-1].get_principal_node_type())
                    stack[-1].children.append(nt)
                    logger.debug('Adding ' + str(nt) + ' to children of ' + str(stack[-1]))
            elif token == ',':
                try:
                    while(not isinstance(stack[-1], Function)):
                        i = stack.pop()
                        logger.debug('Adding ' + str(i) + ' to children of ' + str(stack[-1]))
                        stack[-1].children.append(i)
                except IndexError:
                    raise SyntaxException('Unable to add argument to function')

                logger.debug('Starting new expression ' + str(e) + ' for function argument')
                e = Expression()
                stack.append(e)
                logger.debug('Pushed ' + str(stack[-1]) + ' on stack')
            elif token[0] in '\'"':
                l = Literal(token[1:-1])
                stack.append(l)
                logger.debug('Pushed ' + str(stack[-1]) + ' on stack')
            elif re.fullmatch(r'[0-9.]+', token):
                if '.' in token:
                    l = Literal(float(token))
                else:
                    l = Literal(int(token))

                if len(stack) > 0 and isinstance(stack[-1], Operator):
                    op = stack.pop()
                    op.children.append(l)
                    logger.debug('Added ' + str(l) + ' to children of ' + str(op))
                    stack.append(op)
                else:
                    stack.append(l)
                logger.debug('Pushed ' + str(stack[-1]) + ' on stack')
            elif token == '-' and ( \
                len(stack) == 0 \
                or isinstance(stack[-1], Operator) \
                or (i > 0 and tokens[i-1] in ('(', ',', '[')) \
            ):
                o = Operator('negate')
                stack.append(o)
                logger.debug('Pushed ' + str(stack[-1]) + ' on stack')
            elif token in Operator.OPERATORS and i > 0 and tokens[-1] not in [
                '::', '(', '[', ',', 'and', 'or', 'mod', 'div',
                '*', '/', '//', '|', '+', '-', '=', '!=', '<', '<=',
                '>', '>=',
            ]:
                o = Operator(token)
                o.children.append(stack.pop())
                stack.append(o)
                logger.debug('Pushed ' + str(stack[-1]) + ' on stack')
            elif token == '/':
                if i == 0:
                    s = RootStep(self._document)
                else:
                    while(len(stack) > 0 and not isinstance(stack[-1], Step)):
                        i = stack.pop()
                        if len(stack) > 0:
                            logger.debug('Adding ' + str(i) + ' to children of ' + str(stack[-1]))
                            stack[-1].children.append(i)

                    if len(stack) == 0 or not isinstance(stack[-1], Step):
                        logger.debug('Step is not the last item on the stack')
                        parent_step = Step()
                        logger.debug('Adding ' + str(i) + ' to children of ' + str(parent_step))
                        parent_step.children.append(i)
                        stack.append(parent_step)
                        logger.debug('Pushed ' + str(stack[-1]) + ' on stack')
                    s = Step()
                stack.append(s)
                logger.debug('Pushed ' + str(stack[-1]) + ' on stack')
            elif token == 'Infinity':
                stack.append(Literal(math.inf))
                logger.debug('Pushed ' + str(stack[-1]) + ' on stack')
            elif token == 'NaN':
                stack.append(Literal(math.nan))
                logger.debug('Pushed ' + str(stack[-1]) + ' on stack')
            elif re.fullmatch(r'[a-zA-Z0-9_-]+', token):
                if len(stack) > 0 and isinstance(stack[-1], Axis):
                    if token in TypeNodeTest.NODE_TYPES:
                        stack[-1].children.append(TypeNodeTest(token))
                        logger.debug('Added ' + str(stack[-1].children[-1]) + ' to children of ' + str(stack[-1]))
                    elif len(tokens) > i+1 and tokens[i+1] == ':':
                        stack.append(QNameNodeTest(token))
                        logger.debug('Pushed ' + str(stack[-1]) + ' on stack')
                    else:
                        stack[-1].children.append(NCNameNodeTest(token))
                        logger.debug('Added ' + str(stack[-1].children[-1]) + ' to children of ' + str(stack[-1]))
                elif len(tokens) > i+1 and tokens[i+1] == '::':
                    if token not in Axis.AXES:
                        raise XPathSyntaxException('Unknown axis: ' + str(token))
                    a = Axis(token)
                    stack.append(a)
                    logger.debug('Pushed ' + str(stack[-1]) + ' on stack')
                elif len(tokens) > i+1 and tokens[i+1] == '(':
                    if token in Function.FUNCTIONS:
                        f = Function(token, Function.FUNCTIONS[token])
                        stack.append(f)
                        logger.debug('Pushed ' + str(stack[-1]) + ' on stack')
                    elif token in TypeNodeTest.NODE_TYPES:
                        if len(stack) == 0 or not isinstance(stack[-1], Axis):
                            stack.append(Axis('child'))
                            logger.debug('Pushed ' + str(stack[-1]) + ' on stack')
                        nt = TypeNodeTest(token)
                        stack[-1].children.append(nt)
                        logger.debug('Added ' + str(nt) + ' to children of ' + str(stack[-1]))
                    else:
                        raise XPathSyntaxException('Unknown function or node type test: ' + str(token))
                elif token == 'true':
                    stack.append(Literal(True))
                    logger.debug('Pushed ' + str(stack[-1]) + ' on stack')
                elif token == 'false':
                    stack.append(Literal(False))
                    logger.debug('Pushed ' + str(stack[-1]) + ' on stack')
                elif token in Operator.OPERATORS and i > 0 and tokens[-1] not in [
                    '::', '(', '[', ',', 'and', 'or', 'mod', 'div', '*', '/',
                    '//', '|', '+', '-', '=', '!=', '<', '<=', '>', '>=']:
                    o = Operator(token)
                    o.children.append(stack.pop())
                    stack.append(o)
                    logger.debug('Pushed ' + str(stack[-1]) + ' on stack')
                elif len(tokens) > i+1 and tokens[i+1] == ':':
                    # first part of a qname test
                    if len(stack) == 0 or not isinstance(stack[-1], Axis):
                        stack.append(Axis('child'))
                        logger.debug('Pushed ' + str(stack[-1]) + ' on stack')
                    nt = QNameNodeTest(token)
                    stack.append(nt)
                    logger.debug('Pushed ' + str(stack[-1]) + ' on stack')
                elif i > 0 and tokens[i-1] == ':':
                    # second part of a qname test
                    if len(stack) == 0 or not isinstance(stack[-1], QNameNodeTest):
                        raise SyntaxException('Expecting QNameNodeTest on stack; got second half of QName')
                    nt = stack.pop()
                    nt.name += ':' + token
                    if len(stack) == 0 or not isinstance(stack[-1], Axis):
                        raise SyntaxException('Expecting Axis on stack; finished QNameNodeTest')
                    stack[-1].children.append(nt)
                    logger.debug('Added ' + str(nt) + ' to ' + str(stack[-1]))
                else:
                    # has to be a ncname test
                    if len(stack) == 0 or not isinstance(stack[-1], Axis):
                        stack.append(Axis('child'))
                        logger.debug('Pushed ' + str(stack[-1]) + ' on stack')
                    nt = NCNameNodeTest(token)
                    stack[-1].children.append(nt)
                    logger.debug('Added ' + str(nt) + ' to children of ' + str(stack[-1]))
            else:
                raise XPathSyntaxException('Unknown token: ' + str(token))

        while(len(stack) > 1):
            i = stack.pop()
            logger.debug('Adding ' + str(i) + ' to children of ' + str(stack[-1]))
            stack[-1].children.append(i)
        i = stack.pop()
        logger.debug('Final pop off stack got ' + str(i))

        # TODO need to make sure node set items are unique
        logger.debug('********************************************')
        logger.debug('Evaluating ' + str(i))
        return i.evaluate(self, 1, 1, variables)

    def __str__(self):
        return self.__class__.__name__ + ' ' + hex(id(self))

    def __repr__(self):
        # just for pytest output
        return self.__str__()

    def get_type(self):
        raise NotImplementedError('get_type has not been implemented in class ' + self.__class__.__name__)

    def escape(self, text):
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        return text

    def unescape(self, text):
        text = text.replace('&amp;', '&')
        text = text.replace('&lt;', '<')
        text = text.replace('&gt;', '>')
        text = text.replace('"', '&quot;')
        text = text.replace("'", '&apos;')
        return text
