# Architecture

This is intended for helping new contributers understand the most important modules in the project.  
The general functionality of each module is explained, but the location of these modules in the directory
tree is omitted due to the likelyhood of change and the fact that it is small and hopefully intuitive.
***


## Important Modules
module names and their functionalities are given below

### interop.py	
	test execution engine 
	runs all available tests by default
	handles test execution (`-t <test>` / `-g <group>`)
	handles test printing (`-pt` / `-pg`)
	IO (stdout / stderr / text file)
	uses argparse for argument parsing
	does runtime test loading

### test.py
	defines the Test class
	Test objects are loaded from the /scripts subdirectory at runtime for execution / printing
	Test object stores a test description and Subtest objects 
	Test provides groups list for associating tests to be run

### subtest.py
	defines the Subtest class
	Subtest is initialized with a test name, a function, and the OFA test number

### network.py
	used to simplify test writing
	initializes and stores objects for manipulating the network
	includes a list member variable of node objects
	includes switch objects

### node.py
	used to simplify test writing
	accessed via the network module
	has a method: command(), which executes a command passed to it on the remote node and returns stdout & stderr
	has interface objects for getting alias, ip address, and hostname

