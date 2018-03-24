#!/usr/bin/python3


##
# Name: interop.py
# Description: 
# This is the test execution engine for running RDMA tests for the OFA Interoperability test plan.
# It allows user selection of individual tests, or test groups to be run.                 
##

# Python3 Standard Library modules 
import inspect
import argparse
import logging
import os
import re
import csv
import pkgutil
import importlib

# Python3 additional modules
#import paramiko

# User Defined Modules 
import testlib
import testlib.validate
from testlib.moduleloader import load_modules


# File Locations 
INTEROPDIR = os.path.dirname( __file__ )
LOGPATH = INTEROPDIR +  "/logs"
LOGS =  LOGPATH +  "/error.log"
README = INTEROPDIR + "/../README.md"
OUTPUT = INTEROPDIR + '/output.csv'


##
# Adding Files and Tests 
##
# when adding more source files, make sure to import them (see above)
# after importing them, make sure to concatenate all of the files' TESTS 
# and GROUPS dictionaries into the variables TESTS and GROUPS as seen below
# this will allow the arguments to be called properly
# see the sample test file for more details
##
def isTest(obj):
    """ Passed to inspect.getmembers
    """
    return isinstance(obj, testlib.test.Test)

def getTests():
    """Gets the tests
    """
    module_list=[]
    for module in load_modules(__file__, 'testlib', 'testlib'):
        module_list+=inspect.getmembers(module, isTest)
    return module_list

TESTS=dict(getTests())

# In this function it will scan through each test looking for a groups attribute. 
# When it hits each test it will create/populate a dictionary with the key as the groups and 
# the values as a list of the tests that are under that group.
def getGroups():
    groupDict=dict()
    # Gets the groups that each test has 
    for key, value in sorted(TESTS.items()):
        for group in value.get_groups():
            # if the group already exists then append this test to that groups list of values
            if group in groupDict:
                groupDict[group].append(value)
            # if the group doesn't exist, then add that group as a key with the test as it's value
            else:
                groupDict[group] = [value]
    return groupDict

GROUPS=getGroups()




##
# Logging notes 
##
# logger.info()  - use for printing test results 
# logger.debug() - use for development and debugging purposes
# logger.error() - use when something is preventing the test from completing
##


def print_tests(args):
    """ Prints formated tests available for testing 
    """
    # Printing available tests
    if args.print_tests:
        print("Printing available tests...\n")
        print("\n NAME\t\t\tDESCRIPTION\n ====                   ===========")
        for key, value in sorted(TESTS.items()):
            print(" {}\t\t{}".format(key, value.get_description()))
        print("")


def print_groups(args):
    """ Prints formatted groups available for testing 
    """
    # Printing groups
    print("Printing available groups...\n")
    for key, group in sorted(GROUPS.items()):
        print("\n GROUP\t\t\t{}".format(key))
        print("=======\t\t\t{}=".format("".join(["=" for char in key])))
        print("\n NAME\t\t\tDESCRIPTION")
        for value in sorted(group):
            print(" {}\t\t{}".format(value.get_name(), value.get_description()))
        print("")



def validate_args(args, dictionary, logger):
    """ Validates lists of tests or lists of groups.
        Returns a list of tests or groups to be roun.
    """

    # split the args on / or ,
    arg_dict = re.split(r"[/,]+", args)

    for key in arg_dict:
        try:
            dictionary[key]

        except KeyError:

            # Fail
            for dict_key,value in dictionary.items():
                logger.debug("key: {} value{}".format(dict_key,value))
            logger.error("{} is not a valid input.  Use {} -pt or {} -pg to print options".format(key,os.path.basename(__file__),os.path.basename(__file__)))
            exit(-1)

    # Success
    return arg_dict


def main():
    """ Test bench
    """


    ##
    # Setting up logger
    ##
    logger = logging.getLogger('rdma_parent')
    logger.setLevel(logging.DEBUG)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(levelname)s-%(message)s')


    # Make a LOG file if it doesn't exist
    if not os.path.exists(LOGPATH):
        os.makedirs(LOGPATH)

    # create file handler which logs debug messages
    fh = logging.FileHandler(LOGS)
    fh.setLevel(logging.DEBUG)


    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)

    # create file handler which logs debug messages
    feh = logging.FileHandler(LOGS)
    feh.setLevel(logging.ERROR)

    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    feh.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    logger.addHandler(feh)

    ##
    # Creating argument parser
    ##
    parser = argparse.ArgumentParser(description="OFA Interoperability Testing Framework", add_help=False)
    parser.add_argument("-g","--group",help="Specify comma delimited groups of tests to run")
    parser.add_argument("-t","--test",help="Specify comma delimited list of individual tests to run")
    parser.add_argument("-d","--debug",action="store_true" ,help="Allows debug statements to print")
    parser.add_argument("-pt","--print_tests",action="store_true" ,help="Prints tests currently available for running")
    parser.add_argument("-pg","--print_groups",action="store_true" ,help="Prints groups currently available for running")
    parser.add_argument("-v", action="store_true",help="Turns off assertion validations")
    parser.add_argument("-h","--help", action="store_true",help="Prints out additional information")

    # Running parser
    args = parser.parse_args()

    # Print debug statements if it receives -d argument
    if args.debug:
        db = logging.StreamHandler()
        db.setLevel(logging.DEBUG)
        db.setFormatter(formatter)
        logger.addHandler(db)

    # Prints help
    if args.help:
        with open(README) as file:
            for line in file:
                print(line,end="")
        exit(0)

    # Turns off test assertions
    if not args.v:
        logger.debug("Running unit tests...")
        testlib.validate.run_validations(__file__, 'testlib')

    # Print groups and tests
    if args.print_groups and args.print_tests:
        print_tests(args)
        print_groups(args)
        exit(0)

    # Print groups
    if args.print_groups:
        print_groups(args)
        exit(0)

    # Print tests
    if args.print_tests:
        print_tests(args)
        exit(0)




    ##
    # Interpreting args
    ##

    # Run all of the tests (expected common use case
    if not args.group and not args.test:
        logger.debug("Running all of the tests")

        # Iterate through and run tests
        for key, test in TESTS.items():
            test.run()
            with open(OUTPUT, 'a+') as f:
                w = csv.DictWriter(f, test._outputDict.keys())
                w.writeheader()
                w.writerow(test._outputDict)

    # Run a group of tests
    if args.group:
        logger.debug("Running tests in groups: {}".format(args.group))

        # Validate argument
        arg_list = validate_args(args.group, GROUPS, logger)

        # Remove duplicate tests
        test_list = set()
        for argument in arg_list:

            # GROUPS[argument] returns a list of all the tests within it
            # run each test within that group
            test_list |= set([test for test in GROUPS[argument]])

        # Run all tests
        for test in test_list:
            logger.debug("running test: {}".format(test.get_name()))
            test.run()

    # Run a list of tests by name
    if args.test:

        logger.debug("Running tests: {}".format(args.test))

        # Validate argument
        arg_list = validate_args(args.test, TESTS,logger)
        for argument in arg_list: 
            logger.debug("running test {}".format(argument))

            # Use argument as dictionary key and catch bad values
            TESTS[argument].run()

    #logger.error("sample error message")
    logger.debug("sample debug message")


if __name__ == "__main__":
    main()

