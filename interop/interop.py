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
import sys
import csv
import pkgutil
import importlib

# Python3 additional modules
#import paramiko

# User Defined Modules 
import testlib
import testlib.validate
from testlib.moduleloader import load_modules
import testlib.classes.network as network
import testlib.test


# Save tty settings
os.system('stty -g > ~/.stty')


# File Locations 
INTEROPDIR = os.path.dirname( __file__ )
LOGPATH = INTEROPDIR +  "/logs"
LOGS =  LOGPATH +  "/error.log"
README = INTEROPDIR + "/../README.md"
OUTPUT = INTEROPDIR + '/output.csv'


##
# Adding Tests 
##
# To add tests to the test framework, simply create a test function in a new or existing file 
# under the /interop/testlib/tests directory. Then create a test object using the Test() class 
# in /interop/testlib/test.py and pass the test function to the new object.  The Test() object 
# will be automatically loaded into interop.py and can be called by test name, or test group, which
# you define when you create the object.
##

##
# Logging notes 
##
# logger.info()  - use for printing test results 
# logger.debug() - use for development and debugging purposes
# logger.error() - use when something is preventing the test from completing
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


def isTest(obj):
    """ Passed to inspect.getmembers
    """
    bool = isinstance(obj, testlib.test.Test)
    return bool

def getTests():
    """Gets the tests
    """
    module_list=[]
    for module in load_modules(__file__, 'testlib', 'testlib'):
        module_list+=inspect.getmembers(module, isTest)
    return module_list


# In this function it will scan through each test looking for a groups attribute. 
# When it hits each test it will create/populate a dictionary with the key as the groups and 
# the values as a list of the tests that are under that group.
def getGroups(tests):
    groupDict=dict()
    # Gets the groups that each test has 
    for key, value in sorted(tests.items()):
        for group in value.get_groups():
            # if the group already exists then append this test to that groups list of values
            if group in groupDict:
                groupDict[group].append([value,key])
            # if the group doesn't exist, then add that group as a key with the test as it's value
            else:
                groupDict[group] = [[value,key]]
    return groupDict

def print_tests(TESTS):
    """ Prints formated tests available for testing 
    """
    # Printing available tests
    if TESTS:
        print("Printing available tests...\n")
        print("\n NAME\t\t\tDESCRIPTION\n ====                   ===========")
        for key, value in sorted(TESTS.items()):
            print(" {}\t\t{}".format(key, value.get_description()))
        print("")


def print_groups(GROUPS):
    """ Prints formatted groups available for testing 
    """
    # Printing groups
    print("Printing available groups...\n")
    for key, group in sorted(GROUPS.items()):
        print("\n GROUP\t\t\t{}".format(key))
        print("=======\t\t\t{}=".format("".join(["=" for char in key])))
        print("\n NAME\t\t\tDESCRIPTION")
        for test in sorted(group):
            print(" {}\t\t{}".format(test[1], test[0].get_description()))
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
            return (-1)

    # Success
    return arg_dict

def print_running(name, iter, total):
    """ Print the running line
    """
    message = "Running:\t[{}]".format(name)
    print(message + ("-" * (100 - len(message) - len(str(iter))) + str(iter) +"/" + str(total)))

def run_tests(tests, verbose):
    """ Handles running tests and verbosity
    """
    iter = 0
    total = len(tests.items())
    for key, test in tests.items():
        iter += 1
        print_running(key, iter, total)
        try:
            if not verbose:
                old_stdout = sys.stdout
                with open('/dev/null', 'w') as f:
                    sys.stdout = f
                    results = test.run()
            else:
                test.run()
        except Exception as e:
            if not verbose:
                sys.stdout = old_stdout
            print(e)
        finally:
            if not verbose:
                sys.stdout = old_stdout
        with open(OUTPUT, 'a+') as f:
            # Use the 'results' variable to print out the pass/fail and comments 
            w = csv.DictWriter(f, test._outputDict.keys())
            w.writeheader()
            w.writerow(test._outputDict)

def main():
    """ Test bench
    """

    ##
    # Creating argument parser
    ##
    parser = argparse.ArgumentParser(description="OFA Interoperability Testing Framework", add_help=False)
    parser.add_argument("-g","--group",help="Specify comma delimited groups of tests to run")
    parser.add_argument("-t","--test",help="Specify comma delimited list of individual tests to run")
    parser.add_argument("-ps","--print_status",action="store_true",help="Prints the current network status based on the hosts.conf file")
    parser.add_argument("-pt","--print_tests",action="store_true" ,help="Prints tests currently available for running")
    parser.add_argument("-pg","--print_groups",action="store_true" ,help="Prints groups currently available for running")
    parser.add_argument("-v", action="store_true",help="Turns off assertion validations")
    parser.add_argument("-d","--debug",action="store_true" ,help="Allows debug statements to print")
    parser.add_argument("-V","--verbose", action="store_true",help="Verbose: shows the output from test scripts in stdout")
    parser.add_argument("-h","--help", action="store_true",help="Prints out additional information")

    ##
    # Interpreting args
    ##

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
        return 0

    # Turns off test assertions
    if not args.v:
        logger.debug("Running unit tests...")
        testlib.validate.run_validations(__file__, 'testlib')

    # Print network status
    if args.print_status:
        network.print_status()
        return 0

    # Print groups and tests
    TESTS=dict(getTests())
    GROUPS=getGroups(TESTS)
    if args.print_groups and args.print_tests:
        print_tests(TESTS)
        print_groups(GROUPS)
        return 0

    # Print groups
    if args.print_groups:
        print_groups(GROUPS)
        return 0

    # Print tests
    if args.print_tests:
        print_tests(TESTS)
        return 0


    # Run all of the tests (expected common use case)
    if not args.group and not args.test:
        logger.debug("Running all of the tests")

        # Iterate through and run tests
        run_tests(TESTS,args.verbose)

    # Run a combination of groups and tests
    if args.group and args.test:

        logger.debug("Running tests in groups: {}".format(args.group))

        # Validate argument and get list (if comma delimited list is given)
        group_arg_list = validate_args(args.group, GROUPS, logger)
        if group_arg_list == -1:
            return -1

        # Validate argument and get list (if comma delimited list is given)
        test_arg_list = validate_args(args.test, TESTS, logger)
        if test_arg_list == -1:
            return -1

        # Remove duplicate tests from grouplist
        test_dict = {}

        for argument in group_arg_list:

            # run each test within that group
            for test in GROUPS[argument]:
                if test[0] not in test_dict.items():
                    test_dict[test[1]] = test[0]

        # Remove duplicate tests from testlist
        for argument in test_arg_list:
            # print the output for each test
            if TESTS[argument] not in test_dict.items():
                test_dict[argument] =  TESTS[argument]

        # Run tests
        run_tests(test_dict,args.verbose)

        return 0

    # Run a group of tests
    if args.group:

        # Validate argument and get list (if comma delimited list is given)
        arg_list = validate_args(args.group, GROUPS, logger)

        # Remove duplicate tests
        test_dict = {}
        for argument in arg_list:

            # GROUPS[argument] returns a list of all the tests within the group 
            for test in GROUPS[argument]:
                if test[0] not in test_dict.items():
                    test_dict[test[1]] = test[0]

        # Run tests 
        run_tests(test_dict,args.verbose)

    # Run a list of tests by name
    if args.test:

        logger.debug("Running tests: {}".format(args.test))

        # Validate argument and get list (if comma delimited list is given)
        arg_list = validate_args(args.test, TESTS,logger)

        # Create the list of tests
        tests = {}
        for argument in arg_list:
            tests[argument] = TESTS[argument]

        # Run the tests
        run_tests(tests,args.verbose)
    logger.debug("sample debug message")


if __name__ == "__main__":
    try:
        main()
        exit()
    except Exception as e:
        raise e
    finally:
        os.system('stty `cat ~/.stty`')
        os.system('stty echo')






