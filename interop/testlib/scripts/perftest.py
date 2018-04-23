import testlib.test as test
import testlib.subtest as subtest
import testlib.classes.network as network

import time
import threading

# 13.5 TI RDMA Basic Interop

# Checks for the following:
# Inconsistent prformance levels.
# Incorrect data after completion of RDMA exchanges
# Failure of RDMA operations
# Inability to establish connections between endpoints

def perftest(node1, node2, test_function):
    """ Runs both nodes as server/client.  Comments areonly passed for fails
    """
    out1 = test_function(node1, node2)
    out2 = test_function(node2, node1)
    finalout = [True, ""j
    for i in (out1, out2):
        if not i[0]:
            finalout[1]+=i[1]
            finalout[0] = False
    return finalout

def small_read():
    def read_bw(server, client):

        # need to figure out how to get device name 
        device_server = None
        device_client = None

        # need to figure out how to check if default port is active 
        available_port_server = None
        available_port_client = None

        # check to see if perfest is in use - wait 500 ms and try again if so
        cmd_server = "ib_read_bw -d {} -i {} -s 1 -n 25000 -m 2048 -F".format(device_server, available_port_server)
        cmd_client = "ib_read_bw -d {} -i {} -s 1 -n 25000 -m 2048 {} -F".format(device_client, available_port_client, str(server.ibif.ip))

        def cmd(func, command, result, key):
            """ Used for getting returned output from the threads
            """
            result[key] = func(command)

        threads=[]
        results = dict()
        threads.append(threading.Thread(target=cmd, args=[server.command, cmd_server,results,"server"]))
        threads.append(threading.Thread(target=cmd, args=[client.command, cmd_client,results,"client"]))

        print("starting threads")
        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()
        print("threads done")

        # Output the results  
        print("Printing perftest results")
        for output in results['server']:
            print(output)
        for output in results['client']:
            print(output)
        print("Done printing perftest results")

    perftest(network.node[1],network.node[2],read_bw)
    time.sleep(0.5)

subtest1 = subtest.Subtest(test=small_read, "Small RDMA Send", number='1')
IBPerftest = test.Test(tests=subtests, description="Tests core RDMA operations across a network, validates operation of endpoints at the RDMA level.")

