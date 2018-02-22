#!/usr/bin/python3


class Test:

    def __init__(self, name=None, description=None, script=None, args=None):
        """ Creates a common interface for all tests.
        """

        self._name = name
        self._description = description
        self._script = script
        self._args = args

    def __lt__(self, other):
        """ Allows Tests to be sorted.  Default sorting should be by name.
        """
        try:
            return self._name < other._name
        except AttributeError:
            return NotImplemented

    def run(self):
        """ Executes the test.
        """
        if self._args is not None:
            return self._script(self._args)
        else:
            return self._script()

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_description(self):
        return self._description

    def set_description(self, description):
        self._description = description

    def get_description(self):
        return self._description

if __name__ == "__main__":
    testing_the_test = Test("MyName", "My name is a simple test", lambda x:x*2, 5)
    description = "quick description"
    testing_the_test.set_description(description)
    assert testing_the_test.run() == 10, "Test class is broken" 
    assert testing_the_test.get_description() == description, "Test class is broken"

