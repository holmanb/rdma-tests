#!/usr/bin/python3


class Test:

    def __init__(self, name, description, script, args):
        """ Used for creating a common interface for all tests.
        """

        self._name = name
        self._description = description
        self._script = script
        self._args = args

    def run(self):
        return self._script(self._args)

    def get_name(self):
        return self._name

    def get_description(self):
        return self._description

if __name__ == "__main__":
    testing_the_test = Test("MyName", "My name is a simple test", lambda x:x*2, 5)
    assert testing_the_test.run() == 10, "Test class is broken" 
