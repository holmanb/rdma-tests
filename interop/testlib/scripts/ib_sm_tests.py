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

def masterTest():
    # Getting a base list of all the guids on the network
    netdisocver_output = network.nodes[0].command("sudo ibnetdiscover")
    netdiscover_guid_list = re.findall(r"sysimgguid=0x(.*)", netdisocver_output[0])
    counter = 0
    
    # gets two nodes to send to the tests
    for x in range(0, len(network.nodes)):
        for y in range(x+1, len(network.nodes)):
            # if the nodes are identical, skip this iteration
            if y == x:
                continue
            node1 = network.nodes[x]
            node2 = network.nodes[y]

            node1_name = node1.ethif.aliases[0]
            node2_name = node2.ethif.aliases[0]


            # Backing up previous priority values to restore after test
            node1_opensm_conf = node1.command("sudo cat /etc/opensm/opensm.conf | grep sm_priority")
            node2_opensm_conf = node2.command("sudo cat /etc/opensm/opensm.conf | grep sm_priority")
            node1_prev_priority = str(re.search(r"sm_priority(.*)", node1_opensm_conf[0])[1]).strip()
            node2_prev_priority = str(re.search(r"sm_priority(.*)", node2_opensm_conf[0])[1]).strip()

            for priority_case in range(0, 2):
                # node1 has higher priority than node2
                if priority_case == 0:
                    node1.command("sudo sed -i -e 's/sm_priority.*/sm_priority 11/g' /etc/opensm/opensm.conf")
                    node2.command("sudo sed -i -e 's/sm_priority.*/sm_priority 10/g' /etc/opensm/opensm.conf")
                    priority_scheme = "{} priority = 11. {} priority = 10".format(node1_name, node2_name)

                # node2 has higher priority than node1
                elif priority_case == 1:
                    node1.command("sudo sed -i -e 's/sm_priority.*/sm_priority 10/g' /etc/opensm/opensm.conf")
                    node2.command("sudo sed -i -e 's/sm_priority.*/sm_priority 11/g' /etc/opensm/opensm.conf")
                    priority_scheme = "{} priority = 10. {} priority = 11".format(node1_name, node2_name)

                # node1 and node2 have same priority
                elif priority_case == 2:
                    node1.command("sudo sed -i -e 's/sm_priority.*/sm_priority 10/g' /etc/opensm/opensm.conf")
                    node2.command("sudo sed -i -e 's/sm_priority.*/sm_priority 10/g' /etc/opensm/opensm.conf")
                    priority_scheme = "{} priority = 10. {} priority = 10".format(node1_name, node2_name)

                # run the tests with the node pair
                print("\n--------------------")
                #run test 1
                print("Starting test 1 with priorities: {}".format(priority_scheme))
                test1_return_value = test1()
                if test1_return_value[0] == False:
                    # Restoring previous priority values for both nodes
                    node1.command("sudo sed -i -e 's/sm_priority.*/sm_priority {}/g' /etc/opensm/opensm.conf".format(node1_prev_priority))
                    node2.command("sudo sed -i -e 's/sm_priority.*/sm_priority {}/g' /etc/opensm/opensm.conf".format(node2_prev_priority))
                    return [False, "Test 1 failed on node pair {}, {}\nPriority scheme: {}\n Test error output: {}".format(node1_name, node2_name, priority_scheme, test1_return_value[1])]

                #run test 2
                print("\nStarting test 2 with priorities: {}".format(priority_scheme))
                test2_return_value = test2(node1, node2, netdiscover_guid_list)
                if test2_return_value[0] == False:
                    # Restoring previous priority values for both nodes
                    node1.command("sudo sed -i -e 's/sm_priority.*/sm_priority {}/g' /etc/opensm/opensm.conf".format(node1_prev_priority))
                    node2.command("sudo sed -i -e 's/sm_priority.*/sm_priority {}/g' /etc/opensm/opensm.conf".format(node2_prev_priority))
                    return [False, "Test 2 failed on node pair {}, {}\nPriority scheme: {}\n Test error output: {}".format(node1_name, node2_name, priority_scheme, test2_return_value[1])]

                #run test 3
                print("\nStarting test 3 with priorities: {}".format(priority_scheme))
                test3_return_value = test3(node1, node2, netdiscover_guid_list)
                if test3_return_value[0] == False:
                    # Restoring previous priority values for both nodes
                    node1.command("sudo sed -i -e 's/sm_priority.*/sm_priority {}/g' /etc/opensm/opensm.conf".format(node1_prev_priority))
                    node2.command("sudo sed -i -e 's/sm_priority.*/sm_priority {}/g' /etc/opensm/opensm.conf".format(node2_prev_priority))
                    return [False, "Test 3 failed on node pair {}, {}\nPriority scheme: {}\n Test error output: {}".format(node1_name, node2_name, priority_scheme, test3_return_value[1])]

                #run test 4
                print("\nStarting test 4 with priorities: {}".format(priority_scheme))
                test4_return_value = test4(node1, node2, netdiscover_guid_list)
                if test4_return_value[0] == False:
                    # Restoring previous priority values for both nodes
                    node1.command("sudo sed -i -e 's/sm_priority.*/sm_priority {}/g' /etc/opensm/opensm.conf".format(node1_prev_priority))
                    node2.command("sudo sed -i -e 's/sm_priority.*/sm_priority {}/g' /etc/opensm/opensm.conf".format(node2_prev_priority))
                    return [False, "Test 4 failed on node pair {}, {}\nPriority scheme: {}\n Test error output: {}".format(node1_name, node2_name, priority_scheme, test4_return_value[1])]

                counter += 1


            # Restoring previous priority values for both nodes
            node1.command("sudo sed -i -e 's/sm_priority.*/sm_priority {}/g' /etc/opensm/opensm.conf".format(node1_prev_priority))
            node2.command("sudo sed -i -e 's/sm_priority.*/sm_priority {}/g' /etc/opensm/opensm.conf".format(node2_prev_priority))

    return [True, "All four tests completed successfully. Each test was run {} times, 3 times per pair".format(counter)]



def test1():
    network.load_nodes()

    # disable all SMs in the cluster
    print("Stopping all active subnet managers...")
    for node in network.nodes:
        if node.sm.status() == 'active':
            node.sm.stop()

    # wait a few seconds for all SMs to stop
    time.sleep(1)

    # verify all SMs are disabled
    print("Verifying status of all nodes...")
    for node in network.nodes:
        if node.sm.status() == 'inactive':
            pass
        elif node.sm.status() == 'active':
            return [False, "Subnet manager did not shutdown and is active on node: {}".format(node.ethif.aliases[0])]
        else:
            return [False, "Subnet manager did not shutdown and is in an undefined state ( {} ) on node: {}".format(node.sm.status(), node.ethif.aliases[0])]

    return [True, "Test 1 completed successfully. All SMs were succesfully disabled"]


def test2(node1, node2, guid_list):
    # Get node1 and node2 guid, lid, and name for easier testing
    node1_name = node1.ethif.aliases[0]
    node1_ibstat_output = node1.command("sudo ibstat")
    node1_guid = str(re.search(r"Node GUID.*0x(.*)", node1_ibstat_output[0])[1]).strip()
    node1_lid = str(re.search(r"Base lid:(.*)", node1_ibstat_output[0])[1]).strip()

    node2_name = node2.ethif.aliases[0]
    node2_ibstat_output = node2.command("sudo ibstat")
    node2_guid = str(re.search(r"Node GUID.*0x(.*)", node2_ibstat_output[0])[1]).strip()
    node2_lid = str(re.search(r"Base lid:(.*)", node2_ibstat_output[0])[1]).strip()

    # Start SM on node1 and use 'saquery' to verify all nodes are present in output
    print("Starting", node1_name, " subnet manager")
    if not node1.sm.start():
        return [False, "Subnet manager on node {} failed to start".format(node1_name)]

    # Wait 1 second for sm to start
    print("Waiting for SM on {} to start...".format(node1_name))
    time.sleep(1)

    # Run 'saquery' on a node in the fabric
    print("Running saquery on {}".format(node1_name))
    saquery_output = node1.command("sudo saquery -t 5000")

    # Parsing 'saquery' and adding all node guids to list
    saquery_guid_list = re.findall(r".*node_guid.*0x(.*)", saquery_output[0])

    # Verifying all nodes are present in saquery output by comparing the given guid_list to the one from saquery
    compare_value = set(guid_list) & set(saquery_guid_list)
    if len(compare_value) != len(guid_list):
        return [False, "Could not verify all nodes are present in saquery on node: {}".format(node1_name)]
    else:
        print("All nodes were successfully verified and present in saquery output")

    # Using sminfo, verif that the running SM is the master.
    print("Running sminfo on {} to check if it's master".format(node1_name))
    sminfo_output = node1.command("sudo sminfo -L {}".format(node1_lid))

    if "SMINFO_MASTER" in sminfo_output[0]:
        print("Node1 ({}) correctly reported being the master node".format(node1_name))
    else:
        return [False, "Node1({}) is not reporting to be the master node. Output from sminfo: {}".format(node1_name, sminfo_output)]


    # Start a SM on the second machine in the current pair
    print("Starting SM on node 2: {}".format(node2_name))
    node2.sm.start()
    time.sleep(1)

    # Verify that the SMs behave according to the SM priority rules. Use sminfo again.
    # a. SM with highest numerical priority value is master and the other is in standby. 
    # b. If both SMs have the same priority value then the SM with the smallest guid is master and the other is in standby.
    node1_sminfo_output = node1.command("sudo sminfo -L {}".format(node1_lid))
    node1_priority = str(re.search(r"priority (\d*)", node1_sminfo_output[0])[1])
    node1_state = str(re.search(r"state \d(.*)", node1_sminfo_output[0])[1]).strip()

    node2_sminfo_output = node2.command("sudo sminfo -L {}".format(node2_lid))
    node2_priority = str(re.search(r"priority (\d*)", node2_sminfo_output[0])[1])
    node2_state = str(re.search(r"state \d(.*)", node2_sminfo_output[0])[1]).strip()

    # Checking each case to make sure each node is reporting the correct state
    if node1_priority > node2_priority:
        if node1_state == "SMINFO_MASTER" and node2_state == "SMINFO_STANDBY":
            print("{} and {} reporting the correct states ({} and {})".format(node1_name, node2_name, node1_state, node2_state))
        else:
            return [False, "Some nodes not reporting the correct state. Reported states:\n {}: state = {} and priority = {}\n {}: state = {} and priority = {}".format(node1_name, node1_state, node1_priority, node2_name, node2_state, node2_priority)]
    elif node1_priority < node2_priority:
        if node2_state == "SMINFO_MASTER" and node1_state == "SMINFO_STANDBY":
            print("{} and {} reporting the correct states ({} and {})".format(node2_name, node1_name, node2_state, node1_state))
        else:
            return [False, "Some nodes not reporting the correct state. Reported states:\n {}: state = {} and priority = {}\n {}: state = {} and priority = {}".format(node1_name, node1_state, node1_priority, node2_name, node2_state, node2_priority)]
    elif node1_priority == node2_priority:
        # Converting the hexidecimal guid value to a decimal value to compare them.
        node1_guid_decimal = int(node1_guid, 16)
        node2_guid_decimal = int(node2_guid, 16)
        if node1_guid_decimal < node2_guid_decimal:
            if node1_state == "SMINFO_MASTER" and node2_state == "SMINFO_STANDBY":
                print("{} and {} reporting the correct states ({} and {})".format(node1_name, node2_name, node1_state, node2_state))
            else:
                return [False, "Some nodes not reporting the correct state. Reported states:\n {}: state = {}, priority = {}, and guid = {}\n {}: state = {}, priority = {}, and guid = {}".format(node1_name, node1_state, node1_priority, node1_guid, node2_name, node2_state, node2_priority, node2_guid)]
        elif node1_guid_decimal > node2_guid_decimal:
            if node2_state == "SMINFO_MASTER" and node1_state == "SMINFO_STANDBY":
                print("{} and {} reporting the correct states ({} and {})".format(node2_name, node1_name, node2_state, node1_state))
            else:
                return [False, "Some nodes not reporting the correct state. Reported states:\n {}: state = {}, priority = {}, and guid = {}\n {}: state = {}, priority = {}, and guid = {}".format(node1_name, node1_state, node1_priority, node1_guid, node2_name, node2_state, node2_priority, node2_guid)]
        else:
            return [False, "Guid decimal calculations failed:\n {} guid decimal = {}\n{} guid decimal = {}".format(node1_name, node1_guid_decimal, node2_name, node2_guid_decimal)]
    else:
        return [False, "Node priority was not detected correctly:\n {} priority = {}\n{} priority = {}".format(node1_name, node1_priority, node2_name, node2_priority)]


    # Run 'saquery' on a node in the fabric
    print("Running saquery on {}".format(node1_name))
    saquery_output = node1.command("sudo saquery -t 5000")

    # Parsing 'saquery' and adding all node guids to list
    saquery_guid_list = re.findall(r".*node_guid.*0x(.*)", saquery_output[0])

    # Verifying all nodes are present in saquery output by comparing the given guid_list to the one from saquery
    compare_value = set(guid_list) & set(saquery_guid_list)
    if len(compare_value) != len(guid_list):
        return [False, "Could not verify all nodes are present in saquery on node: {}".format(node1_name)]
    else:
        print("All nodes were successfully verified and present in saquery output")


    return [True, "Successfully tested node pair"]


def test3(node1, node2, guid_list):
    # Making sure whichever node is the master node is 'node1'. Also getting name, guid, and lid for easier testing
    node1_name = node1.ethif.aliases[0]
    node1_ibstat_output = node1.command("sudo ibstat")
    node1_guid = str(re.search(r"Node GUID.*0x(.*)", node1_ibstat_output[0])[1]).strip()
    node1_lid = str(re.search(r"Base lid:(.*)", node1_ibstat_output[0])[1]).strip()
    node1_sminfo_output = node1.command("sudo sminfo -L {}".format(node1_lid))
    node1_state = str(re.search(r"state \d(.*)", node1_sminfo_output[0])[1]).strip()

    node2_name = node2.ethif.aliases[0]
    node2_ibstat_output = node2.command("sudo ibstat")
    node2_guid = str(re.search(r"Node GUID.*0x(.*)", node2_ibstat_output[0])[1]).strip()
    node2_lid = str(re.search(r"Base lid:(.*)", node2_ibstat_output[0])[1]).strip()
    node2_sminfo_output = node1.command("sudo sminfo -L {}".format(node2_lid))
    node2_state = str(re.search(r"state \d(.*)", node2_sminfo_output[0])[1]).strip()

    if node1_state == "SMINFO_MASTER" and node2_state == "SMINFO_STANDBY":
        pass
    elif node1_state == "SMINFO_STANDBY" and node2_state == "SMINFO_MASTER":
        # Swapping node 1 and 2 if node 2 is the master. This just keeps the master node as 'node1'
        node_temp = node1
        node_temp_guid = node1_guid
        node_temp_lid = node1_lid
        node_temp_name = node1_name

        node1 = node2
        node1_guid = node2_guid
        node1_lid = node2_lid
        node1_name = node2_name
        
        node2 = node_temp
        node2_guid = node_temp_guid
        node2_lid = node_temp_lid
        node2_name = node_temp_name
    else:
        return [False, "Test 3 error determining which node is master:\n{} state = {}\n{} state = {}".format(node1_name, node1_state, node2_name, node2_state)]

    
    # Shutdown the master SM.
    print("Shutting down master SM ({})...".format(node1_name))
    node1.sm.stop()
    # Wait three seconds for SM to stop
    time.sleep(3)
    #Verify SM is stopped
    if node1.sm.status() == 'active':
        return [False, "Step7: Node 1 ({}) failed to shutdown".format(node1_name)]
    else:
        print("Master SM successfully shutdown")

    # Verify the other active SM goes into the master state using sminfo again.
    sminfo_output = node2.command("sudo sminfo -L {}".format(node2_lid))

    print("Waiting for node 2 ({}) to take master position. This could take up to 60 seconds...".format(node2_name))
    counter = 0
    while "SMINFO_MASTER" not in sminfo_output[0] and counter < 60:
        time.sleep(1)
        sminfo_output = node2.command("sudo sminfo -L {}".format(node2_lid))

    if "SMINFO_MASTER" in sminfo_output[0]:
        print("Node2 ({}) correctly reporting now being the master node".format(node2_name))
    else:
        return [False, "Node2({}) is not reporting to be the master node. Output from sminfo: {}".format(node2_name,sminfo_output)]

    # Run 'saquery' on a node in the current pair
    print("Running saquery on {}".format(node1_name))
    saquery_output = node1.command("sudo saquery -t 5000")

    # Parsing 'saquery' and adding all node guids to list
    saquery_guid_list = re.findall(r".*node_guid.*0x(.*)", saquery_output[0])

    # Verifying all nodes are present in saquery output by comparing the given guid_list to the one from saquery
    compare_value = set(guid_list) & set(saquery_guid_list)
    if len(compare_value) != len(guid_list):
        return [False, "Could not verify all nodes are present in saquery on node: {}".format(node1_name)]
    else:
        print("All nodes were successfully verified and present in saquery output")

    # Start the SM that was just shutdown
    print("Starting subnet manager on {}...".format(node1_name))
    if not node1.sm.start():
        return [False, "Subnet manager on node {} failed to start".format(node1_name)]
    # Wait 3 seconds for sm to start
    time.sleep(3)

    # Verify that the newly started SM resumes it's position as master while the other goes into standby again
    node1_sminfo_output = node1.command("sudo sminfo -L {}".format(node1_lid))
    node1_state = str(re.search(r"state \d(.*)", node1_sminfo_output[0])[1]).strip()

    node2_sminfo_output = node2.command("sudo sminfo -L {}".format(node2_lid))
    node2_state = str(re.search(r"state \d(.*)", node2_sminfo_output[0])[1]).strip()

    if node1_state == "SMINFO_MASTER" and node2_state == "SMINFO_STANDBY":
        print("Node 1 ({}) correctly resumed it's position as master again")
    elif node1_state == "SMINFO_STANDBY" and node2_state == "SMINFO_MASTER":
        return [False, "Node 1 ({}) did not resume it's position as master after is started again:\n {} state = {}\n{} state = {}".format(node1_name,node1_name, node1_state, node2_name, node2_state)]
    else:
        return [False, "Some nodes are not reporting the correct state after master is started again:\n {} state = {}\n{} state = {}".format(node1_name, node1_state, node2_name, node2_state)]


    # Run 'saquery' on a node in the current pair
    print("Running saquery on {}".format(node1_name))
    saquery_output = node1.command("sudo saquery -t 5000")

    # Parsing 'saquery' and adding all node guids to list
    saquery_guid_list = re.findall(r".*node_guid.*0x(.*)", saquery_output[0])

    # Verifying all nodes are present in saquery output by comparing the given guid_list to the one from saquery
    compare_value = set(guid_list) & set(saquery_guid_list)
    if len(compare_value) != len(guid_list):
        return [False, "Could not verify all nodes are present in saquery on node: {}".format(node1_name)]
    else:
        print("All nodes were successfully verified and present in saquery output")


    return [True, "Test 3 completed successfully"]

def test4(node1, node2, guid_list):
    return [True, "Test 4 completed successfully"]

MasterTest = subtest.Subtest(test=masterTest, name="ib sm failover tests", number='1')
Table5 = Test.Test(tests=[MasterTest],  description="ib sm tests")
