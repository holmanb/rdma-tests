import testlib.test as Test
import testlib.classes.network as network

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
""""


# In this test, all active SMs on the fabric which are going to be tested, must be from the same 
# vendor. They will be tested pairwise; two at a time.

def test1():
    #gets two nodes to send to test1_1
    node0 = network.nodes[0]
    node1 = network.nodes[1]

    #run the test with those nodes
    test1_1(node0, node1)


def test1_1(node1, node2):
    # disable all SMs in the cluster then start a SM on either machine in a chosen pair.
    for node in network.nodes:
        if node.sm.status() == 'active'
            node.sm.stop()

    node1.sm.start()
    
    # run "saquery" on a node in the fabric
    output = node1.command('saquery')
    ## verify that all nodes in the cluster are presetn in the output
    output = node1.ibif.get_state()
    print(output)


    # using the ibdiagnet tool with the -r option, verify that the running SM is the master

    # Start a SM on the second machine in the current pair

def test2():
    # Verify that the SMs behave according to the SM priority rules. Use "# ibdiagnet -r" again.

Test1 = Test.Test(script=test1,  description="ib sm test")