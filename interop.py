#!/usr/bin/python


##
# Name: interop.py
# Description: This is intended for running RDMA tests for the OFA Interoperability test plan 
##

import argparse
import logging


##
# Logging notes 
##
# logger.info()  - use for printing test results 
# logger.debug() - use for development and debugging purposes
# logger.error() - use when something is preventing the test from completing
##

def main():

    # Creating argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-g","--group",help="Specify comma delimited groups of tests to run")
    parser.add_argument("-t","--test",help="Specify comma delimited list of individual tests to run")
    parser.add_argument("-d","--debug",action="store_true" ,help="Allows debug statements to print")

    # Running parser
    args = parser.parse_args()

    # Setting up logging 
    # create logger with 'spam_application'
    logger = logging.getLogger('rdma_parent')
    logger.setLevel(logging.DEBUG)

    # create file handler which logs even debug messages
    fh = logging.FileHandler('debug_rdma.log')
    fh.setLevel(logging.DEBUG)

    # Set debug level if receives -d argument
    if args.debug:
        db = logging.StreamHandler()
        db.setLevel(logging.DEBUG)
        logger.addHandler(db)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(name)s-%(levelname)s-%(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    # Interpreting args
    if not args.group and not args.test:
        logger.info("Running all of the tests")

    if args.group:
        logger.info("Running tests in groups: {}".format(args.group))

    if args.test:
        logger.info("Running tests: {}".format(args.test))

    logger.error("sample error message")
    logger.debug("sample debug message")


if __name__ == "__main__":
    main()
