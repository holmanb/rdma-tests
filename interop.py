#!/usr/bin/python3


##
# Name: interop.py
# Description: This is intended for running RDMA tests for the OFA Interoperability test plan 
##

# Default classes
import argparse
import logging
import infiniband.sample_tests as sample_tests
import os
import re

# User Defined Classes 
import Test

##
# Adding Files and Tests 
##
# when adding more source files, make sure to import them (see above)
# after importing them, make sure to concatenate all of the files' TESTS 
# and GROUPS dictionaries into the variables TESTS and GROUPS as seen below
# this will allow the arguments to be called properly
# see the sample test file for more details
##

TESTS=sample_tests.TESTS
GROUPS=sample_tests.GROUPS

# This defines the log files location for ease of changing location 
LOGS = "./logs/"

##
# Logging notes 
##
# logger.info()  - use for printing test results 
# logger.debug() - use for development and debugging purposes
# logger.error() - use when something is preventing the test from completing
##


### IGNORE THESE TWO CLASSES, I'M JUST DOING A 
### BIT OF EXPERIMENTATION HERE
#class Tests:
#    _persist_methods = ['get', 'save', 'delete']
#
#    def __init__(self, persister):
#        self._persister = persister
#
#    def __getattr__(self, attribute):
#        if attribute in self._persist_methods:
#            return getattr(self._persister, attribute)
#class Test:
#    def get(self):
#        print("ping test")


def validate_args(args, dictionary, logger):

        # split the args on / or ,
        arg_dict = re.split(r"[/,]+", args)

        for key in arg_dict: 
            try:
                dictionary[key]
            except KeyError:
                for dict_key,value in dictionary.items():
                    logger.debug("key: {} value{}".format(dict_key,value))
                logger.error("{} is not a valid input.  Use {} -p to print options".format(key, os.path.basename(__file__)))
                exit(-1)
        return arg_dict


def main():

    ##
    # Creating argument parser
    ##
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-g","--group",help="Specify comma delimited groups of tests to run")
    parser.add_argument("-t","--test",help="Specify comma delimited list of individual tests to run")
    parser.add_argument("-d","--debug",action="store_true" ,help="Allows debug statements to print")
    parser.add_argument("-pt","--print_tests",action="store_true" ,help="Prints tests currently available for running")
    parser.add_argument("-pg","--print_groups",action="store_true" ,help="Prints groups currently available for running")

    # Running parser
    args = parser.parse_args()

    if args.print_tests:
        print("Printing available tests...\n")
        print("\n NAME\t\t\tDESCRIPTION\n ====                   ===========")
        for key, value in sorted(TESTS.items()):
            print(" {}\t\t{}".format(key, value.get_description()))
        exit(0)

    if args.print_groups:
        print("Printing available groups...\n")
        for key, group in sorted(GROUPS.items()):
            print("\n GROUP\t\t\t{}".format(key))
            print("=======\t\t\t{}=".format("".join(["=" for char in key])))
            print("\n NAME\t\t\tDESCRIPTION")
            for value in sorted(group):
                print(" {}\t\t{}".format(value.get_name(), value.get_description()))
            print("")
        exit(0)

    ##
    # Setting up logging 
    ##
    logger = logging.getLogger('rdma_parent')
    logger.setLevel(logging.DEBUG)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(levelname)s-%(message)s')


    # Make a LOG file if it doesn't exist
    if not os.path.exists(LOGS):
        os.makedirs(LOGS)

    # create file handler which logs debug messages
    fh = logging.FileHandler(LOGS + 'debug.log')
    fh.setLevel(logging.DEBUG)

    # Print debug statements if it receives -d argument
    if args.debug:
        db = logging.StreamHandler()
        db.setLevel(logging.DEBUG)
        db.setFormatter(formatter)
        logger.addHandler(db)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)

    # create file handler which logs debug messages
    feh = logging.FileHandler(LOGS + 'error.log')
    feh.setLevel(logging.ERROR)

    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    feh.setFormatter(logging.ERROR)

    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    logger.addHandler(feh)

    ##
    # Interpreting args
    ##

    # Run all of the tests (expected common use case
    if not args.group and not args.test:
        logger.debug("Running all of the tests")

        # Iterate through and run tests
        for key, test in TESTS.items():
            test.run()

    # Run a group of tests
    if args.group:
        logger.debug("Running tests in groups: {}".format(args.group))
        print("not implimented yet")

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
