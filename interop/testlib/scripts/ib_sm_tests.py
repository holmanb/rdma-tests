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

def nodeSelection():
    #gets two nodes to send to test1_1
    network.load_nodes()

    # disable all SMs in the cluster
    print("stopping all active subnet managers")
    for node in network.nodes:
        if node.sm.status() == 'active':
            node.sm.stop()

    for x in range(0, len(network.nodes)):
        for y in range(0, len(network.nodes)):
            #if the nodes are identical, skip this iteration
            if y == x:
                continue
            node1 = network.nodes[x]
            node2 = network.nodes[y]

            #run the test with those nodes
            print("running tests on nodes: ",node1.ethif.aliases[0]," and ",node2.ethif.aliases[0])
            test1_1(node1, node2)

            #stopping the subnet managers on each node used
            node1.sm.stop()
            node2.sm.stop()


    
def test1():
    network.load_nodes()
    print("printing status of all nodes")
    for node in network.nodes:
        print(node.sm.status())
    
    print()

    # disable all SMs in the cluster
    print("stopping all active subnet managers")
    for node in network.nodes:
        if node.sm.status() == 'active':
            node.sm.stop()

    # verify all SMs are disabled
    print("printing status of all nodes")
    for node in network.nodes:
        print(node.sm.status())

    return [True, "sample comment from sample_test2"]


def test1_1(node1, node2):
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

    matchObj = re.findall( r".*NodeDescription.*\.\.\.(.*) .*", output[0])
    if matchObj:
        print(matchObj)
    ethernet_aliases = []
    for node in network.nodes:
        if(node.ethif):
            ethernet_aliases.append(node.ethif.aliases[0])

    print(ethernet_aliases)
    print()

    del output


    # using the ibdiagnet tool with the -r option, verify that the running SM is the master

    # Start a SM on the second machine in the current pair

#def test2():
    # Verify that the SMs behave according to the SM priority rules. Use "# ibdiagnet -r" again.

Test1 = subtest.Subtest(test=test1, name="ib sm subtest 1", number='1')
Table5 = Test.Test(tests=[Test1],  description="ib sm test")

