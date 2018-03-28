/rdma-tests/interop/testlib/classes
===================================

the *classes* subdirectory holds the network.py module, which initializes and exposes several useful interfaces

Dependencies
------------

The classes depends on a configuration file `hosts.conf` to load the network object information properly.  
This file is very similar to the /etc/hosts file and is stored in the same file as interop.py.

SUMMARY
-------
This README is intended to be a quick reference for these classes.  It is not 
intended to be exhaustive of all the available member functions / variables or functionality.  
It will likely be helpful, however, for architecture / design questions.

network (module)
-------
** This modules represents the network, and has what one would expect a network to have: a bunch of nodes. Always import this and then use one of the nodes in the `nodes` list ** 

`network.nodes`			- a list of Node() objects (see below)

`network.print_status()`		- print all information related to this module

`network.load_nodes()`			- parses the hosts.conf file and loads the network objects

`network.add_node()`			- adds a single Node() object

node (class)
----
** Class that provides user interaction functionality with the node and it's objects: its interfaces and subnet manager. The command() method is important. **

`node.ibif`				- an infiniband Interface() object (see below) 

`node.ethif`				- an ethernet Interface() object (see below)

`node.sm`				- a SubnetManager() object (see below)

`node.command()`			- executes the given command on the node - can be the local node or remote via paramiko

interface (class)
---------
** Class for interface manipulation and info storage **

`interface.ip`				- IPv4 address object (python3 built-in) - can be cast to a str()

`interface.hostname`			- hostname

`interface.aliases`			- list of aliases

`interface.id`	 			- a string identifying the interface

`interface.state`			- current interface state (up|down)

`interface.get_state()`			- uses nmap to get the state of the interface

subnetmanager (class)
-------------
** Class for using the subnet manager **

`subnetmanager.state`			- the last retreived state of the subnet manager - this is not guaranteed to be up-to-date

`subnetmanager.node`			- we pass the node to the subnet manager so we can use node.command()

`subnetmanager.start()`			- starts the subnet manager

`subnetmanager.stop()`			- stops the subnet manager

`subnetmanager.status()`		- gets the current status of the subnet manager


EXAMPLES
--------

The following example code shows the syntax to manipulate one of the node's subnet managers

	>> import interop.testlib.classes.network as network # import the network module
	>> mynode = network.nodes[0]		# select a node 
	>> mynode.sm.status()			# get the status
	'active'
	>> mynode.sm.stop()			# stop the SM
	>> mynode.sm.status()			# get the SM status
	'inactive'
	>> mynode.sm.start()			# start the SM
	>> mynode.sm.status()			# get the status
	'active'


The following example code shows the syntax to run node.command() on one of the node's subnet managers

	>> import interop.testlib.classes.network as network 	# import the network module
	>> print(network.nodes[1].command('ibstat')		# executing ibstat on node[1] in the network.nodes list	
	CA 'mlx5_0'
		CA type: ...
		...
	>> print(network.nodes[0].command('ibstat')		# executing ibstat on node[0] in the network.nodes list	
	CA 'mlx5_0'
		CA type: ...
		...

