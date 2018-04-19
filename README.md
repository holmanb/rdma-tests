interop
=======
*A light-weight framework for executing OFA Interoperability tests*


Summary
-------
Interop is a simple test framework. If executed without options it will run all available tests. Individual tests or groups of tests may be 
executed by passing arguments. Additional tests using python3 may be added with ease. The `interop.py` script handles test output and 
logging, as well as test loading, selection, and execution.   


Installation 
------------
This program should be straightforward to run with once dependencies are installed. This framework has been developed for CentOS 7 and SUSE
(SLES 15). Other RPM based distros may work as well with little modification.  

	$ git clone https://github.com/holmanbph/rdma-tests.git

	$ cd rdma-tests && sudo bash install.sh

	$ cd interop 

	$ ./interop.py 


Runtime Options
---------------
	  -g GROUP, --group GROUP 	Specify comma delimited groups of tests to run

	  -t TEST, --test TEST  	Specify comma delimited list of individual tests to run

	  -d, --debug           	Allows debug statements to print

	  -pt, --print_tests    	Prints available tests

	  -pg, --print_groups   	Prints available groups 

	  -ps, --print_status		Prints out the status of the network (interface statuses, subnet manager statuses, etc), 
					this is a functionality of the network.py module that is pretty handy at times.

	  -v      		        Toggles validation tests 	

	  -V,  --verbose		Prints test output

	  -h, --help            	show this help message and exit


Adding Tests
------------
The execution engine, `interop.py`, looks in the directories and subdirectories of `/rdma-tests/interop/testlib/scripts/` for tests to run.
The `interop.py` script provides plugin loading of tests via the following functionality. Tests are defined using the Test() object. To 
call a test by name, use the name of the variable that it is assigned to with the -t option. The Test() object is used to dynamically load 
it into the test framework at runtime.   This allows the options for printing available tests and groups (`-pt` and `-pg`) to automatically 
be updated when a new test is written, The same functionality allows individual tests and groups (`-t <test1>[,test2[, testn]]` and 
`-g <group1>[,group2[, groupn]]`) to be automatically updated/reloaded during runtime as well. This pluggable functionality users to write 
a new test and execute them with `interop.py` without making any changes to the `interop.py` script. See the readme in 
`/rdma-tests/interop/testlib/scripts/` or at <https://github.com/holmanbph/rdma-tests/tree/master/interop/testlib/scripts>. 


Test Library
------------
 There is a small library that provides common functionality that is helpful for writing test scripts.  It has its own `README.md` file.
 The library and its documentation can be found under `/rdma-tests/interop/testlib/classes/` or at the following link: 
 <https://github.com/holmanbph/rdma-tests/tree/master/interop/testlib/scripts>.  


Examples
--------

	./interop.py -h | less		# the help page

	./interop.py -pt		# Will print all tests available for execution

	./interop.py -t test1,test2	# Will execute test1 and test2, assuming test1 and test2 exist

	./interop.py -ps		# Prints the network status (SM info, interface info, etc)

	./interop.py -g group1		# Executes all groups in group1


Contribution
------------
Please report bugs by opening a ticket at <https://github.com/holmanbph/rdma-tests/issues>. Contributions are welcome via pull request. 
	
