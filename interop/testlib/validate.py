#!/usr/bin/python3

##
# validate.py
# 
# executes tests that validate that the software is working as intended
##

import testlib.testclass as testclass


def run_validations():
    """ This function runs all assertion validations.  Import and run future validations in this script.
    """

    testclass.validate()

