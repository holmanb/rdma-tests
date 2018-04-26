import testlib.test as Test
import testlib.subtest as subtest
import testlib.classes.network as network
import re

"""
Test 1: Basic sweep test 
Verify that all SMs are NOT ACTIVE (after receiving
the SMSet of SMInfo to DISABLE) and that the selected SM (SM1) is
the master.

Test 2: SM Priority test 
Verify Subnet and SM's behavior according to the SM's priority.

Test 3: Failover - Disable SM1
Disable the master SM and verify that the standby SM becomes the
master and configures the cluster accordingly.

Test 4: Failover - Disable SM2
Disable the master SM and verify that the standby SM becomes the
master and configures the cluster accordingly.
"""


# In this test, all active SMs on the fabric which are going to be tested, must be from the same 
# vendor. They will be tested pairwise; two at a time.
    
def test1():
    network.load_nodes()

    # disable all SMs in the cluster
    print("stopping all active subnet managers")
    for node in network.nodes:
        if node.sm.status() == 'active':
            node.sm.stop()

    # verify all SMs are disabled
    print("verifying status of all nodes:")
    for node in network.nodes:
        if node.sm.status() == 'inactive':
            print("{}= inactive".format(node.ethif.aliases[0]))
        elif node.sm.status() == 'active':
            return [False, "Subnet manager is active on node: {}".format(node.ethif.aliases[0])]
        else:
            return [False, "Subnet manager is in undefined state ( {} ) on node: {}".format(node.sm.status(), node.ethif.aliases[0])]

    return [True, "All SMs were succesfully disabled"]

def test2():
    # Getting a base list of all the guids on the network
    netdisocver_output = network.nodes[0].command("sudo ibnetdiscover")
    netdiscover_guid_list = re.findall( r"sysimgguid=0x(.*)", netdisocver_output[0])

    #saquery_output = network.nodes[0].command("sudo saquery")
    #saquery_sys_guid_list = re.findall( r"sys_guid.*0x(.*)", netdisocver_output[0])
    #saquery_node_guid_list = re.findall( r"node_guid.*0x(.*)", netdisocver_output[0])
    #saquery_port_guid_list = re.findall( r"port_guid.*0x(.*)", netdisocver_output[0])

    #gets two nodes to send to test2
    for x in range(0, len(network.nodes)):
        for y in range(0, len(network.nodes)):
            #if the nodes are identical, skip this iteration
            if y == x:
                continue
            node1 = network.nodes[x]
            node2 = network.nodes[y]

            #run the test with those nodes
            print("running tests on nodes: ",node1.ethif.aliases[0]," and ",node2.ethif.aliases[0])
            nodePairs(node1, node2, netdiscover_guid_list)

            #stopping the subnet managers on each node used
            node1.sm.stop()
            node2.sm.stop()

    return [True, "test 2 completed successfully"]

def nodePairs(node1, node2, guid_list):
    print("starting", node1.ethif.aliases[0], " subnet manager")
    # if starting fails try again up to 5 times
    counter = 0
    while not node1.sm.start() and counter < 5:
        print("{} failed to start. Trying again: {}".format(node1.ethif.aliases[0],counter))
        counter += 1

    
    # run "saquery" on a node in the fabric
    #output = node1.command("sudo saquery | grep \"NodeDescription\" | sed 's/.*\.\.\.//' | sed 's/\s.*$//'")
    print("Running saquery on ", node1.ethif.aliases[0])
    output = node1.command("sudo saquery -t 5000")
    ## verify that all nodes in the cluster are presetn in the output

    # was not getting output consistently from saquery so checking again
    counter = 0
    while not output[0] and counter < 10:
        print("Output was empty trying again: ", counter)
        print("[{}]".format(output[0]))
        output_error = " ".join(output[1].split("\n"))
        print("Error: ", output_error)
        output = node1.command("sudo saquery -t 5000")
        counter += 1

    saquery_guid_list = re.findall( r".*node_guid.*0x(.*)", output[0])
    if saquery_guid_list:
        print(saquery_guid_list)

    # for node in network.nodes:
    #     if(node.ethif):
    #         ethernet_aliases.append(node.ethif.aliases[0])

    print()

    # Verifying all nodes are present in saquery output
    compare_value = set(guid_list) & set(saquery_guid_list)
    if compare_value != len(guid_list):
        return [False, "Could not verify all nodes are present in saquery on node: {}".format(node1.ethif.aliases[0])]

    del output

    # using the ibdiagnet tool with the -r option, verify that the running SM is the master

    # Start a SM on the second machine in the current pair

#def test2():
    # Verify that the SMs behave according to the SM priority rules. Use "# ibdiagnet -r" again.

Test1 = subtest.Subtest(test=test1, name="ib sm subtest 1", number='1')
Test2 = subtest.Subtest(test=test2, name="ib sm subtest2", number='2')
Table5 = Test.Test(tests=[Test1, Test2],  description="ib sm test")

