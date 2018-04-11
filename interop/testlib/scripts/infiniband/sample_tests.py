import testlib.test as Test
import testlib.classes.network as network
import time

def IBFabricInit():
    for node in network.nodes:
        if node.is_up():
            if(node.sm.status() == "inactive"):
                node.sm.start()
            ibstat = node.command("ibstat").split("\n")
            # Getting the system name, then putting it into format that ibdiagnet wants
            # from 0x<systemguid> to S<systemguid>
            for lines in ibstat:
                if "System image GUID:" in lines:
                    stat2 = lines.split()
                    systemGUID = "S" + stat2[-1][2:]

            #Generating a topology file
            node.command("ibdiagnet -wt 'topology'")
            #Clearing all port counters
            node.command("ibdiagnet -pc")
            #Waiting for 17 seconds per the specification requirements
            time.sleep(17)
            #Sending 1000 node descriptions
            node.command("ibdiagnet -c 1000")
            #Generating fabric report, use /tmp/ibdiagnet.sm file to see running s
            node.command("ibdiagnet")
            #Skipping the building of GUID list for now
            #Comparing current topology against topology file made at beginning of test
            Stdout = node.command("ibdiagnet -t 'topology' -s '{}'".format(systemGUID))
            print(Stdout)
            string = "perfectly matches the discovered fabric"
            string2 = "No bad Guids were found"
            string3 = "No illegal PM counters values were found"

            f = open('/var/cache/ibutils/ibdiagnet.log', 'r')
            contents = f.readlines()
            for line in contents:
                if string in line:
                    print("Topology from before and after test matches")
                if string2 in line:
                    print("No illegal PM counters")
                if string3 in line:
                    print("No bad Guids found")

            f.close()
        else:
            print("{} is not currently active, running tests on other active nodes".format(node.ethif.id))

def sample_test1():

    print( "this is running sample_test1 that is imported from /infiniband/sample_tests.py")


def sample_test2():

    print( "this is running sample_test2 that is imported from /infiniband/sample_tests.py")

IBFabricInit = Test.Test(script=IBFabricInit, description="Currently tests the fabric initialization of the master node using opensm as subnet manager")

sampleTest1 = Test.Test(script=sample_test1,  description="this is the sample_test1 description", group=["latency_tests","bandwidth_tests"])

sampleTest2 = Test.Test(script=sample_test2)
sampleTest2.set_description("this is the sample_test2 description")
sampleTest2.add_group("latency_tests")
