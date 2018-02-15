#!/usr/bin/python
import argparse
import logging

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-g","--group",help="Specify comma delimited groups of tests to run")
    parser.add_argument("-t","--test",help="Specify comma delimited list of individual tests to run")


    args = parser.parse_args()

    if not args.group and not args.test:
        print("Running all of the tests")
    if args.group:
        print("Running tests in groups: {}".format(args.group))
    if args.test:
        print("Running tests: {}".format(args.test))




if __name__ == "__main__":
    main()
