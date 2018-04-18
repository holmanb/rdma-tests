interop
=======

*A light-weight and flexible framework for executing OFA Interoperability tests*

interop is a simple test framework. By default it will run all available tests, but individual tests or groups of tests may be specified.  Additional tests may be added with ease. 


Installation 
------------

This program should be straightforward to run with once dependencies are installed. This framework and its install script is developed for CentOS 7.  
Other RPM based distros may work as well with little to no modification.  

	$ git clone https://github.com/holmanbph/rdma-tests.git

	$ sudo bash rdma-tests/install.sh


Runtime Options
---------------

	  -g GROUP, --group GROUP 	Specify comma delimited groups of tests to run

	  -t TEST, --test TEST  	Specify comma delimited list of individual tests to run

	  -d, --debug           	Allows debug statements to print

	  -ps, --print_status		Prints out the status of the network

	  -pt, --print_tests    	Prints tests currently available for running

	  -pg, --print_groups   	Prints groups currently available for running

	  -v      		        Toggles validation tests 	

	  -V,  --verbose		Prints test output

	  -h, --help            	show this help message and exit


Test Development
----------------

 Tests can be written and executed without making any modifications to interop.py. To utilize this pluggable 
 functionality, simply write a test function or functions, and store it under /interop/testlib/scripts or any
 subdirectory of the scripts directory.  Once the script is in the appropriate directory, create a Test() object  
 (from /testlib/test.py), within your script file.  Pass your test function to the `script` argument.  Add groups 
 and a discription as seems appropriate.  Your test should now be executable using `./interop.py -t [your_function_name]` 
 and `interop.py -g [your_group_name]`. 


Test Library
------------
 There is a test library for common functionality that is helpful for writing test scripts.  It has its own `README.md` file.
 The library and its documentation can be found under interop/testlib/classes


EXAMPLES
--------

	./interop.py -h | less		# the help page

	./interop.py -pt		# Will print all tests available for execution

	./interop.py -t test1,test2	# Will execute test1 and test2, assuming test1 and test2 exist

	./interop.py -ps		# Prints the network status (SM info, interface info, etc)

	./interop.py -g group1		# Executes all groups in group1

	
