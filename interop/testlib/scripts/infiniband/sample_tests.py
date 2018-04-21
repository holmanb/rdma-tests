import testlib.test as Test
import testlib.subtest as subtest
import testlib.classes.network as network
import time
import os


def IBFabricInit():
    topology_file = '/tmp/topology'

    for node in network.nodes:
        if node.is_up():
            if(node.sm.status() == "inactive"):
                node.sm.start()
            ibstat = node.command("ibstat")[0].split("\n")

            # Getting the system name, then putting it into format that ibdiagnet wants
            # from 0x<systemguid> to S<systemguid>
            for lines in ibstat:
                if "System image GUID:" in lines:
                    stat2 = lines.split()
                    systemGUID = "S" + stat2[-1][2:]

            #Generating a topology file
            node.command("ibdiagnet -wt '{}'".format(topology_file))

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
            print(Stdout[0])
            string = "perfectly matches the discovered fabric"
            string2 = "No bad Guids were found"
            string3 = "No illegal PM counters values were found"

            f = open('/var/cache/ibutils/ibdiagnet.log', 'r')
            contents = f.readlines()
            topology_matches = False
            no_illegal_counters = False
            no_bad_guids = False
            for line in contents:
                if string in line:
                    print("Topology from before and after test matches")
                    topology_matches = True
                if string2 in line:
                    print("No illegal PM counters")
                    no_illegal_counters = True
                if string3 in line:
                    print("No bad Guids found")
                    no_bad_guids = True
            node.command('rm ' +topology_file)

            f.close()

            # Remove the topology file
            print(topology_file)
            if os.path.exists(topology_file):
                os.remove(topology_file)

            # If matches, then true
            if topology_matches and no_illegal_counters and no_bad_guids:
                return [True, ""]

            # Reasonable comments printed on failure
            comments = ""
            if not topology_matches:
                comments += "Topology from before and after test doesn't match\n"
            if not no_illegal_counters:
                comments += "Illegal PM counters fount\n"
            if not no_bad_guids:
                comments += "Bad GUIDs found"

            return [False, comments] 

        else:
            print("{} is not currently active, running tests on other active nodes".format(node.ethif.id))

        

def sample_test1():

    print( "this is running sample_test1 that is imported from /infiniband/sample_tests.py")
    return [True, "sample comment from sample_test1"]


def sample_test2():

    print( "this is running sample_test2 that is imported from /infiniband/sample_tests.py")
    return [False, "sample comment from sample_test2"]


test = subtest.Subtest(test=IBFabricInit, name="IB Fabric Initialization", number='1')
IBFabricInit = Test.Test(tests=[test], description="Currently tests the fabric initialization of the master node using opensm as subnet manager")

sample1 = subtest.Subtest(test=sample_test2, name="Sample test 2", number='2')
sample2 = subtest.Subtest(test=sample_test1, name="Sample test 1", number='1')
sampleTest1 = Test.Test(tests=[sample1,sample2],  description="this is the sample_test1 description", group=["latency_tests","bandwidth_tests"])

#sampleTest2 = Test.Test(script=[sample_test2])
#sampleTest2.set_description("this is the sample_test2 description")
#sampleTest2.add_group("latency_tests")

