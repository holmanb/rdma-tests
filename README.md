interop
=======

*A test light-weight flexible framework for executing OFA Interoperability tests*

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

	  -pt, --print_tests    	Prints tests currently available for running

	  -pg, --print_groups   	Prints groups currently available for running

	  -h, --help            	show this help message and exit


EXAMPLES
--------

	./interop.py -h | less

	./interop.py -pt
