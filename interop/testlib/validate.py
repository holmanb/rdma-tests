#!/usr/bin/python3

##
# validate.py
# 
# executes tests that validate that the software is working as intended
##
import testlib
import testlib.test as testclass
from testlib.moduleloader import load_modules


def run_validations(file_name, PACKAGE, skip_dir=None):
    """ This function runs all assertion validations.  Import and run future validations in this script.
    """
    for module in load_modules(file_name,PACKAGE, skip_dir):
        testclass.validate()

if __name__ == "__main__":
    main()

