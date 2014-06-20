"""This module holds logic responsible for turning JSON representations into usable UI descriptions, i.e.
Python objects representing modes and options.
"""

import json

from . import option
from . import mode
from . import shared
from . import errors


def makelines(s, maxlen):
    lines = []
    words = s.split(' ')
    line = ''
    i = 0
    while i < len(words):
        word = words[i]
        if len(line + word) <= maxlen-1:
            line += (word + ' ')
            i += 1
        else:
            lines.append(line)
            line = ''
    if line: lines.append(line)
    return lines


def _getoptionlines(mode, indent='    ', level=1):
    lines = []
    for scope in ['global', 'local']:
        if mode.options(group=scope): lines.append( ('str', indent*(level) + '{0} options:'.format(scope)) )
        for o in mode.options(group=scope):
            s = ''
            s += (o['short'] if o['short'] else '    ')
            if o['short'] and o['long']: s += ', '
            s += (o['long'] if o['long'] else '')
            if o.params():
                s += '='
                s += ' '.join(['<{0}>'.format(i) for i in o.params()])
            lines.append( ('option', indent*(level+1) + s, o) )
        if mode.options(group=scope): lines.append( ('str', '') )
    return lines


class Helper:
    def __init__(self, progname, mode):
        self._mode = mode
        self._indent = {'string': '    ', 'level': 0}
        self._usage = []
        self._progname = progname
        self._maxlen = 140
        self._opt_desc_start = 0
        self._lines = []

    def addUsage(self, line):
        self._usage.append(line)
        return self

    def setmaxlen(self, n):
        self._maxlen = n
        return self

    def _genusage(self):
        usage_head = 'usage: {0} '.format(self._progname)
        usage_indent = len(usage_head) * ' '
        usage_lines = []
        if self._usage: usage_lines.append( ('str', usage_head + self._usage[0]) )
        for line in self._usage[1:]: usage_lines.append( ('str', usage_indent + line) )
        self._lines.extend(usage_lines)
        if self._lines: self._lines.append( ('str', '') )

    def _genintrolines(self, mode, level=0):
        lines = []
        for i in makelines(mode._help, self._maxlen-len(self._indent['string']*level)): lines.append( ('str', (self._indent['string']*level) + i) )
        if mode._help: lines.append( ('str', '') )
        return lines

    def _genmodelines(self, mode, level=0, name='', deep=True):
        lines = []
        if name: self._lines.append( ('str', ((self._indent['string']*level) + name)) )
        self._lines.extend(self._genintrolines(mode, level=level+1))
        self._lines.extend(_getoptionlines(mode, level=level+1))
        if mode.modes(): self._lines.append( ('str', ((self._indent['string']*(level+1)) + 'commands:')) )
        for m in sorted(mode.modes()):
            submode = mode.getmode(m)
            if deep:
                lines.extend(self._genmodelines(submode, name=m, level=level+2))
            else:
                text = m
                if submode._help: text += ' - {0}'.format(submode._help)
                first = makelines(text, self._maxlen)[0]
                lines.append( ('str', ((self._indent['string']*(level+2)) + first)) )
                for l in makelines(text[len(first):], (self._maxlen-len(m)-3)):
                    indent = self._indent['string']*(level+2)
                    padding = ' ' * (len(m) + 3) # the +3 is for ' - ' string separating mode name from description, to be included in padding
                    l = '{0}{1}{2}'.format(indent, padding, l)
                    lines.append( ('str', l) )
                if submode._help: lines.append( ('str', '') )
        return lines

    def gen(self, deep=True):
        self._genusage()
        self._lines.extend(self._genmodelines(mode=self._mode, deep=deep))
        return self

    def render(self):
        for i in self._lines:
            if i[0] == 'option':
                if len(i[1]) > self._opt_desc_start: self._opt_desc_start = len(i[1])
        self._opt_desc_start += 2

        lines = []
        for no, i in enumerate(self._lines):
            if i[0] == 'str':
                type, string = i
            elif i[0] == 'option':
                type, string, opt = i
                while len(string) < self._opt_desc_start: string += ' '
                string += ('- {0}'.format(opt['help']) if opt['help'] else '')
            else:
                raise Exception('line {0}: unknown type: {1}: {2}'.format(no, i[0], i))
            lines.append(string)
        while lines:
            if lines[-1] == '': lines.pop(-1)
            else: break
        return '\n'.join(lines)
