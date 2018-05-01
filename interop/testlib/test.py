#!/usr/bin/python3

from testlib.subtest import Subtest

class TestReturnValueError(Exception):
    pass

class TestCannotComplete(Exception):
    pass

class TestInitializationError(Exception):
    pass

class Test:

    def __init__(self, description=None, script=None, args=None, group=None, tests=None):
        """ Creates a common interface for all tests.
        """
        self._description = description
        self._script = script
        self._args = args
        self._group=[]
        self._tests = tests
        if group:
            self.add_group(group)

        # Sanity checks, fail early
        if not script:
            TestInitializationError("You'll need an executable test")
        if not description:
            TestInitializationError("Just give us a few words to describe your test, please")
        if not tests:
            TestInitializationError("Need a list of subtests to execute")
        if not isinstance(tests, list):
            TestInitializationError("Need to initialize the test object with a list of subtests")

        # Make sure it's a test
        for test in tests:
            if not isinstance(test, Subtest):
                TestInitializationError("Need a list of subtests to execute")

    def get_scripts(self):
        """ Get the callable scripts
        """
        return self._tests

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

        def validate_output(output):

            # Tests must conform to the output describied in this string
            error =  "Tests must return the following format: [bool_pass_or_fail, str_description]\n"
            error += "If tests cannot complete, they should raise TestCannotComplete() exception explaining the error"

            # Validate output
            valid_output = isinstance(output, list) or len(output)==2 or isinstance(output[0], bool) or isinstance(output[1], str)
            if not valid_output:
                raise TestReturnValueError(error)

        if self._args is not None:

            # Run the test script
            output = self._script(self._args)

            # Validate the test script
            validate_output(output)

            # Dict for readablity
            return {"success" : output[0], "comments" : output [1]}
        else:

            # Run test script
            output = self._script()

            # Validate the test script
            validate_output(output)

            # Dict for readablity
            return {"success" : output[0], "comments" : output [1]}

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
