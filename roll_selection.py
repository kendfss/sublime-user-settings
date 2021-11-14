"""
The builtin transpose command acts on selections, this one acts on characters within selections
"""

import sublime
import sublime_plugin
from itertools import chain


def splitall(splitters, target, empties=False):
    splitters = iter(splitters)
    result = target.split(next(splitters))
    for splitter in splitters:
        result = list(chain.from_iterable(i.split(splitter) for i in result))
    yield from (filter(None, result), result)[empties]


def isint(content):
    if not content:
        return False
    content = str(content)
    numeric = all(map(str.isnumeric, splitall('.-', content)))
    periods = content.count('.')
    negs = content.count('-')
    if periods > 1 or negs > 1 or not numeric:
        raise ValueError
    elif periods == 0:
        return True
    elif not any(map(int, content.split('.')[-1])):
        return True
    return False

def roll(text, boost):
    boost = int(boost)
    while boost > 0:
        text = text[-1] + text[:-1]
        boost -= 1    
    while boost < 0:
        text = text[1:] + text[0]
        boost += 1
    return text

def resplit(text, lengths):
    parts = []
    text = iter(text)
    for length in lengths:
        part = ''
        while length:
            part += next(text)
            length -= 1
        parts.append(part)
    return parts

class RollSelectionCommand(sublime_plugin.TextCommand):
    def run(self, edit, boost:int, parallel:bool=False):
        if len(self.view.sel()[0]):
            if parallel:
                for region in self.view.sel():
                    text = self.view.substr(region)
                    self.view.replace(edit, region, roll(text, boost))
            else:
                substrs = tuple(map(self.view.substr, self.view.sel()))
                lengths = tuple(map(len, substrs))
                text = roll(''.join(substrs), boost)
                parts = resplit(text, lengths)
                for region, part in zip(self.view.sel(), parts):
                    self.view.replace(edit, region, part)
            

    def input(self, args):
        return RollDirectionHandler(self.view)

class RollDirectionHandler(sublime_plugin.TextInputHandler):
    def __init__(self, view):
        self.view = view

    def name(self):
        return "boost"

    def placeholder(self):
        return "boost"

    def preview(self, boost):
        if isint(boost) and len(text:=''.join(map(self.view.substr, self.view.sel()))):
            return roll(text, boost)

