import argparse
import logging

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-g","--group",help="Specify group of tests to run")
    parser.add_argument("-t","--test",help="Specify individual tests to run")
    


    print("Hello world")
    args = parser.parse_args()
    if not args.group and not args.test:
        print("Running all of the test")


    print(args.group) 



if __name__ == "__main__":
    main()
