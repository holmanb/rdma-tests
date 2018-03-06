#!/usr/bin/python3


class Test:

    def __init__(self, name=None, description=None, script=None, args=None, group=None, outputDict=None):
        """ Creates a common interface for all tests.
        """

        self._name = name
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

    def run(self):
        """ Executes the test.
        """
        if self._args is not None: 
            self._outputDict = {"name" : self._name, "success" : "success condition", "comments" : "placeholder comments"}
            return self._script(self._args)
        else:
            self._outputDict = {"name" : self._name, "success" : "success condition", "comments" : "placeholder comments"}
            return self._script()

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

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
    ##
    # The following assertions are intended to verify modifications to this class.  
    # Please execute this file directly after making modifications
    ##
    testing_the_test = Test("MyName", "My name is a simple test", lambda x:x*2, 5)
    description = "quick description"
    testing_the_test.set_description(description)
    assert testing_the_test.run() == 10, "Test class is broken" 
    assert testing_the_test.get_description() == description, "Test class is broken"
    assert testing_the_test.get_groups() == [], "Test class is broken"
    assert Test(group="group2").get_groups()[0]=="group2", "Test class groups is broken"
    assert Test().add_group(["group1","group2"]).get_groups()==["group1","group2"], "Test class groups is broken"
    testing_the_test.add_group("group1")
    assert testing_the_test.get_groups()[0] == "group1", "Test class groups is broken"



if __name__ == "__main__":
    validate()
