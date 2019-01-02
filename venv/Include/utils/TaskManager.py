import collections

class Task(object):
    def __init__(self, name, func, data):
        self.name = name
        self.func = func
        self.data = data
        self.active = False
        return

    def start(self):
        self.active = True

    def update(self, dt):
        self.func(dt, self.data)

    def stop(self):
        self.active = False


class TaskManager(object):
    def __init__(self):
        self.tasks = collections.OrderedDict()

    def update(self, dt):
        for key in self.tasks.keys():
            self.tasks[key].update(dt)

    def add(self, key, task):
        self.tasks[key] = task

    def stop(self, key):
        if key in self.tasks:
            self.tasks[key].stop()

    def start(self, key):
        if key in self.tasks:
            self.tasks[key].start()

    def remove(self, key):
        if key in self.tasks:
            del self.tasks[key]
