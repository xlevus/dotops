import os

ENV_PREFIX = 'DOTOPS_'


class Context(object):
    def __init__(self, prefix):
        self.__dict__['prefix'] = prefix
        self.__dict__['context'] = {}

    def __getattr__(self, name):
        if name in self.context:
            return self.context[name]

        try:
            return self.get_environ(name)
        except KeyError:
            raise AttributeError("'{} is not set.".format(name))

    def __setattr__(self, name, value):
        self.context[name] = value
        self.set_environ(name, value)

    def get(self, name, default=None):
        if name in self.context:
            return self.context[name]

        environ_key = self.environ_key(name)
        if environ_key in os.environ:
            return self.get_environ(name)

        return default

    def environ_key(self, name):
        return '{}{}'.format(self.prefix, name.upper())

    def get_environ(self, name):
        environ_key = self.environ_key(name)
        value = os.environ[environ_key]

        if value in ('True', 'False'):
            return value == 'True'

    def set_environ(self, name, value):
        environ_key = self.environ_key(name)
        os.environ[environ_key] = str(value)


context = Context(ENV_PREFIX)
