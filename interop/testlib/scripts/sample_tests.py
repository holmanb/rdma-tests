import testlib.test as Test
import testlib.subtest as subtest
import testlib.classes.network as network
import time
import os




def CounterErrors(query):
    count = 0
    for lines in query:
        if "Error" in lines and "#" not in lines:
            countTmp = lines.split(".")
            count += int(countTmp[-1])
    return count

def IBFabricInit():
    topology_file = '/tmp/topology'
    eCount = 0
    nodeSuccess = []
    for node in network.nodes:
        if node.is_up():
            if(node.sm.status() == "inactive"):
                node.sm.start()

            #Generating a topology file
            node.command("ibnetdiscover --cache '{}'".format(topology_file))

            #Waiting for 17 seconds per the specification requirements
            time.sleep(17)
            Stdout = node.command("ibnetdiscover --diff '{}'".format(topology_file))
            print(Stdout[0])

            #Getting the port counters(to check for bad one) from perfquery to mimic ibdiagnet
            perfQuery1 = node.command("perfquery -a")[0].split("\n")
            eCount += CounterErrors(perfQuery1)
            perfQuery2 = node.command("perfquery -E")[0].split("\n")
            eCount += CounterErrors(perfQuery2)
            perfQuery3 = node.command("perfquery -x")[0].split("\n")
            eCount += CounterErrors(perfQuery3)

            #Getting all the system GUIDs and verifying none of them are the same
            ibGuids = node.command("ibnetdiscover")[0].split("\n")
            guidList = []
            for lines in ibGuids:
                if "sysimgguid" in lines:
                    guidTmp = lines.split("0x")
                    guidList.append(guidTmp[-1])

            #Initializing the conditions for the successful completion of fabric initialization
            topology_matches = False
            no_illegal_counters = False
            no_bad_guids = False

            #Verifying that the conditions have been met
            if eCount == 0:
                no_illegal_counters = True
                print("No illegal PM counters found")
            if len(Stdout[0]) == 0:
                topology_matches = True
                print("Topology from before and after test matches")
            if len(guidList) == len(set(guidList)):
                no_bad_guids = True
                print("No bad GUIDs were found")
            node.command('rm ' +topology_file)


            # Remove the topology file
            print(topology_file)
            if os.path.exists(topology_file):
                os.remove(topology_file)

            # If matches, then true
            if topology_matches and no_illegal_counters and no_bad_guids:
                nodeSuccess.append(True)
            else:
                nodeSuccess.append(False)

            # Reasonable comments printed on failure
            comments = ""
            if not topology_matches:
                comments += "*Topology before & after doesn't match on {}".format(node.ethif.id)
            if not no_illegal_counters:
                comments += "*Illegal PM counters found, {} in total".format(eCount)
            if not no_bad_guids:
                comments += "*Bad GUIDs found on {}".format(node.ethif.id)


        else:
            print("{} is not currently active, running tests on other active nodes".format(node.ethif.id))
    for node in network.nodes:
        node.sm.stop()
    if all(nodeSuccess) == True:
        return [True, comments]
    else:
        return [False, comments]


#function for removing the destination node's ib0 address from sending nodes
#arp table then pinging with specified options and packet size
def pingTests(node, size, ibipAddr):
    node.command("ip neigh flush {}".format(ibipAddr))
    node.command("ping -i 0.2 -t 3 -c 10 -s {} {}".format(size, ibipAddr))

def PingNodesStepA
    for nodeSRC in network.nodes:
        nodeSRC.sm.start()
        time.sleep(2)
        ibAddrSRC = nodeSRC.ibif.id

        #verifying the SM started is master 
        isMaster = nodeSRC.command("sminfo")[0].split("_")
        master = isMaster[-1]
        if master == "MASTER":

            #pinging all nodes with specified packet sizes as long as the ib
            #interface is not the same as the source node
            for nodeDEST in network.node:
                if nodeDEST.ibif.id != ibAddrSRC:
                    for size in packetSize:
                    pingTests(nodeSRC, packetSize, nodeDEST.ibif.id)
        else:
            smNotMaster = "The Subnet Manager being used did not successfully become master."
            return(smNotMaster)

def IB_IPoIBConnectModeStepA():

    packetSize = [511,1025,2044,8192,32768,65492]

    #function for removing the destination node's ib0 address from sending nodes
    #arp table then pinging with specified options and packet size
    def pingTests(node, size, ibipAddr):
        node.command("ip neigh flush {}".format(ibipAddr))
        node.command("ping -i 0.2 -t 3 -c 10 -s {} {}".format(size, ibipAddr))

    #setting the mode to connected on all nodes and verifying
    for node in network.nodes:
        node.command("echo 'connected' > /sys/class/net/ib0/mode")
    for node in network.nodes:
        if node.command("grep -e 'datagram' -e 'connected' /sys/class/net/ib0/mode")[0] == 'connected':
            print("{} is in connected mode\n".format(node.ethif.id))
        else:
            print("{} is not in connected mode\n".format(node.ethif.id))

    #stopping all sm's in the system, then verifying they are inactive
    for node in network.nodes:
        node.sm.stop();
    for node in network.nodes:
        if node.sm.status() == "inactive":
            continue
        else:
            return("{}'s sm has not been shut off, please restart test.".format(node.ethif.id))

    #verifying all nodes are up before continuing with tests
    for node in network.nodes:
        if node.is_up():
            continue
        else:
            return("{} is down, please restart and try the test again.".format(node.ethif.id))

    PingNodesStepA()




def sample_test1():

    print( "this is running sample_test1 that is imported from /infiniband/sample_tests.py")
    return [True, "sample comment from sample_test1"]


def sample_test2():

    print( "this is running sample_test2 that is imported from /infiniband/sample_tests.py")
    return [False, "sample comment from sample_test2"]


test = subtest.Subtest(test=IBFabricInit, name="IB Fabric Initialization", number='1')
IBFabricInit = Test.Test(tests=[test], description="Currently tests the fabric initialization of the master node using opensm as subnet manager")
IPoIBCMpings = subtest.Subtest(test=IB_IPoIBConnectModeStepA, name = "Step A Connect Mode ping tests", number = '1')

IB_IPoIBConnectMode = Test.Test(tests=[test], description= "Pings all nodes from each other node after flushing the destination ib0 address from sending nodes arp table")
sample1 = subtest.Subtest(test=sample_test2, name="Sample test 2", number='2')
sample2 = subtest.Subtest(test=sample_test1, name="Sample test 1", number='1')
sampleTest1 = Test.Test(tests=[sample1,sample2],  description="this is the sample_test1 description", group=["latency_tests","bandwidth_tests"])

#sampleTest2 = Test.Test(script=[sample_test2])
#sampleTest2.set_description("this is the sample_test2 description")
#sampleTest2.add_group("latency_tests")

