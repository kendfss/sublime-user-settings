import sublime
import sublime_plugin
from difflib import Differ

class InsertBelowCommand(sublime_plugin.TextCommand):
    def move_down(self):
        self.view.run_command('move', {'by': 'lines', 'forward':True})
        return self.view.sel()[0]

    @property
    def region(self):
        # return sublime.Region(0, len(self.view)-1)
        # return sublime.Region(0, len(self.view)+1)
        return sublime.Region(0, len(self.view))

    @property
    def text(self):
        return self.view.substr(self.region)
    @property
    def lines(self):
        yield from enumerate(self.text.splitlines())




    def region_start(self, region):
        line = self.view.line(region)
        return region.a - line.a

    def pad_lines(self, region):
        # text = self.text.splitlines()
        text = []
        pad = self.region_start(region)
        # for i, line in enumerate(text):
        for i, line in self.lines:
            # text[i] = line.ljust(pad)
            text.append(line.ljust(pad))
        # print('\n'.join(text))
        print(len(self.text.splitlines()), len(text))
        print(len(self.text.splitlines()) == len(text))
        # rs = '\n'.join(map(str.rstrip, text))
        # print(rs == self.text)
        # if not '\n'.join(map(str.rstrip, text)) == self.text:
        # if not rs == self.text:
            # sublime.show(Differ().compare('\n'.join(text), self.text))
            # print(Differ().compare('\n'.join(text), self.text))
        self.view.replace(self.edit, self.region, '\n'.join(text))

    def lines_below(self, region):
        line_index = self.line_number(region)
        print("Region is on line #{}".format(line_index))
        for i, line in self.lines:
            if i > line_index:
                yield i, line

    def line_number(self, region):
        print("Number of Lines:\t{}".format(len(self.text.splitlines())))
        print("Region:\t{}".format(region))
        print("Region start:\t{}".format(self.region_start(region)))

        length = 0

        for i, line in self.lines:
            if length >= region.a:
                print(i)
                return i - 1
            length += len(line)
        return i

        # while length < len(self.view)-1:
        #     line = text[line_index]
        #     length += len(line)
        #     print(line_index)
        #     if length >= region.a:
        #         return line_index
        #     line_index += 1

    def restrip(self):
        text = '\n'.join(map(str.rstrip, self.text.splitlines()))
        self.view.replace(self.edit, self.region, text)

    def replace_line(self, index, new_line):
        text = self.text.splitlines()
        ctr = 0
        for i, line in self.lines:
            ctr += len(line)
            if index == i:
                # text[i] = new_line
                region = sublime.Region(ctr-len(line), ctr)
                self.view.replace(self.edit, region, new_line)
                return



    @staticmethod
    def flatten_selection(region):
        return sublime.Region(region.a, region.a)

    def run(self, edit, text):
        print('\n'*20)
        print(self.region)
        print(len(self.view))
        self.edit = edit
        region = self.flatten_selection(self.view.sel()[0])
        position = self.region_start(region)
        # self.pad_lines(region)
        reach = 0
        print('STARTING')
        for i, line in self.lines_below(region):
            line = line.ljust(position)
            new_line = line[:position+i] + text + line[position+i:]
            print(i)
            print(new_line)
            self.replace_line(i, new_line.rstrip())
        print('STRIPPING')
        self.restrip()
        self.view.insert(edit, region.a, '\n')
        # self.view.run_command('save', {'encoding': self.view.encoding()})

    def input(self, args):
        return InsertReceptionHandler(self.view)


class InsertReceptionHandler(sublime_plugin.TextInputHandler):
    def __init__(self, view):
        self.view = view

    def name(self):
        return "text"

    def placeholder(self):
        return "your input"

    def preview(self, text):
        return ("Characters: {}, Words: {}"
            .format(
                len(text), len(text.split())
            )
        )















