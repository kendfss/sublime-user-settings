import sublime
import sublime_plugin


#####   DEBUG   #####
#####   DEBUG   #####
#####   DEBUG   #####
#####   DEBUG   #####
import inspect
show = lambda name, enum=True: ([print("%r \t %r" % (i, e) if enum else e) for i, e in enumerate(name)], None)[-1]
getsource = lambda name, enum=False: (show(inspect.getsource(name).splitlines(), enum), None)[-1]
scan = lambda term, object=sublime: (show(filter(lambda x: term in x.lower(), dir(object))), None)[-1]
#####   /DEBUG   #####
#####   /DEBUG   #####
#####   /DEBUG   #####
#####   /DEBUG   #####

class DeleteFileCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        print(self.view.file_name())
        print('fuck')
        print(self.view)
        # self.view.insert(edit, 0, "Hello, World!")
        path = self.view.file_name()
        self.view.run_command('select_all')
        print(path)
