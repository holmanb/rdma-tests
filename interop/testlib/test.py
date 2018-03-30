#!/usr/bin/python3


class Test:

    def __init__(self, description=None, script=None, args=None, group=None, outputDict=None):
        """ Creates a common interface for all tests.
        """
        self._name = script.__name__
        self._description = description
        self._script = script
        self._args = args
        self._group=[]
        self._outputDict ={}
        if group:
            self.add_group(group)

    def __lt__(self, other):
        """ Allows Tests to be sorted.  Default sorting should be by name.
        """
        try:
            return self._name < other._name
        except AttributeError:
            return NotImplemented
    def get_name(self):
        """ Get the test name.  This name can be used with `./interop.py -t [name]` to execute this test.
        """
        return self._name

    def run(self):
        """ Executes the test.
        """
        if self._args is not None: 
            self._outputDict = {"name" : self._name, "success" : "success condition", "comments" : "placeholder comments"}
            return self._script(self._args)
        else:
            self._outputDict = {"name" : self._name, "success" : "success condition", "comments" : "placeholder comments"}
            return self._script()

    def get_description(self):
        return self._description

    def set_description(self, description):
        self._description = description

    def add_group(self, group):
        """ accepts a string as a group, or a list of groups
        """

        # Add single group
        if isinstance(group, str):
            self._group.append(group)

        # Add a list/of groups
        elif isinstance(group, list):
            self._group += group
        else:
            raise TypeError
        return self

    def get_groups(self):
        return self._group

def validate():
    pass

if __name__ == "__main__":
    validate()
