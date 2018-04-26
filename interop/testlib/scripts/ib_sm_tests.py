import testlib.test as Test
import testlib.subtest as subtest
import testlib.classes.network as network
import re
import time

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

    # wait a few seconds for all SMs to stop
    time.sleep(3)

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
    netdiscover_guid_list = re.findall(
        r"sysimgguid=0x(.*)", netdisocver_output[0])

    #saquery_output = network.nodes[0].command("sudo saquery")
    #saquery_sys_guid_list = re.findall( r"sys_guid.*0x(.*)", netdisocver_output[0])
    #saquery_node_guid_list = re.findall( r"node_guid.*0x(.*)", netdisocver_output[0])
    #saquery_port_guid_list = re.findall( r"port_guid.*0x(.*)", netdisocver_output[0])

    # gets two nodes to send to test2
    for x in range(0, len(network.nodes)):
        for y in range(0, len(network.nodes)):
            # if the nodes are identical, skip this iteration
            if y == x:
                continue
            node1 = network.nodes[x]
            node2 = network.nodes[y]

            # run the test with those nodes
            print("\n--------------------")
            print("running tests on nodes: ",
                  node1.ethif.aliases[0], " and ", node2.ethif.aliases[0])
            return_value = nodePairs(node1, node2, netdiscover_guid_list)
            if return_value[0] == False:
                return[False, return_value[1]]

            # stopping the subnet managers on each node used
            node1.sm.stop()
            node2.sm.stop()
            # Waiting a few seconds for SMs to stop
            print("waiting for {} and {} sm to stop".format(node1.ethif.aliases[0], node2.ethif.aliases[0]))
            time.sleep(3)
            # Verify those SMs are down
            if node1.sm.status() == "active":
                return [False, "{} subnet manager did not turn off!".format(node1.ethif.aliases[0])]
            if node2.sm.status() == "active":
                return [False, "{} subnet manager did not turn off!".format(node2.ethif.aliases[0])]



    return [True, "test 2 completed successfully"]


def nodePairs(node1, node2, guid_list):
    # get node1 and node2 guid and lid
    node1_ibstat_output = node1.command("sudo ibstat")
    node1_guid = str(re.search(r"Node GUID.*0x(.*)",
                               node1_ibstat_output[0])[1]).strip()
    node1_lid = str(
        re.search(r"SM lid:(.*)", node1_ibstat_output[0])[1]).strip()

    node2_ibstat_output = node2.command("sudo ibstat")
    node2_guid = str(re.search(r"Node GUID.*0x(.*)",
                               node2_ibstat_output[0])[1]).strip()
    node2_lid = str(
        re.search(r"SM lid:(.*)", node2_ibstat_output[0])[1]).strip()

    print("starting", node1.ethif.aliases[0], " subnet manager")
    # if starting fails try again up to 5 times
    counter = 0
    while not node1.sm.start() and counter < 5:
        print("{} failed to start. Trying again: {}".format(
            node1.ethif.aliases[0], counter))
        counter += 1
        if counter == 5:
            return [False, "Subnet manager on node {} failed to start".format(node1.ethif.aliases[0])]

    # wait 3 seconds for sm to start
    print("Waiting for SM on {} to start".format(node1.ethif.aliases[0]))
    time.sleep(3)

    

    # run "saquery" on a node in the fabric
    #output = node1.command("sudo saquery | grep \"NodeDescription\" | sed 's/.*\.\.\.//' | sed 's/\s.*$//'")
    print("Running saquery on ", node1.ethif.aliases[0])
    output = node1.command("sudo saquery -t 5000")

    # was not getting output consistently from saquery so checking again
    counter = 0
    while not output[0] and counter < 10:
        print("Output was empty trying again: ", counter)
        print("[{}]".format(output[0]))
        output_error = " ".join(output[1].split("\n"))
        print("Error: ", output_error)
        output = node1.command("sudo saquery -t 5000")
        counter += 1

    saquery_guid_list = re.findall(r".*node_guid.*0x(.*)", output[0])


    # Verifying all nodes are present in saquery output
    compare_value = set(guid_list) & set(saquery_guid_list)
    if len(compare_value) != len(guid_list):
        return [False, "Could not verify all nodes are present in saquery on node: {}".format(node1.ethif.aliases[0])]
    else:
        print("Nodes were successfully verified and existing")

    print("running sminfo on {} to check if it's master".format(node1.ethif.aliases[0]))
    # using sminfo, verify that the running SM is the master
    sminfo_output = ["",""]
    counter = 0
    while not sminfo_output[0] and counter < 10:
        sminfo_output = node1.command("sudo sminfo -L {}".format(node1_lid))
        if "SMINFO_MASTER" in sminfo_output[0]:
            print("Node1 ({}) correctly reported being the master node".format(node1.ethif.aliases[0]))
        elif "iberror: failed: query" in sminfo_output[0] and counter < 9:
            print("sminfo on node1 ({}) failed with error:{} Trying again...".format(node1.ethif.aliases[0],sminfo_output))
            time.sleep(1)
            print("checking that subnet manager is in fact turned on. SM state: {}".format(node1.sm.status()))
            sminfo_output[0] = ""
        counter += 1

    if "SMINFO_MASTER" not in sminfo_output[0]:
        return [False, "Node1({}) is not reporting to be the master node. Output from sminfo: {}".format(node1.ethif.aliases[0],sminfo_output)]
        
    return [True, "Node pair successfully tested"]

    # Start a SM on the second machine in the current pair

Test1 = subtest.Subtest(test=test1, name="ib sm subtest 1", number='1')
Test2 = subtest.Subtest(test=test2, name="ib sm subtest2", number='2')
Table5 = Test.Test(tests=[Test1, Test2],  description="ib sm test")
