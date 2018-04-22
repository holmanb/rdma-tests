import testlib.test as test
import testlib.subtest as subtest
import testlib.classes.network as network

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
    finalout = [True, ""]
    for i in (out1, out2):
        if not i[0]:
            finalout[1]+=i[1]
            finalout[0] = False
    return finalout
        
def small_read():
    def read_bw(node1, node2):
        client = "ib_read_bw -d {} -i {} -s 1 -n 25000 -m 2048 -f" 
        server = "ib_read_bw -d {} -i {} -s 1 -n 25000 -m 2048 -R -x 0 -o 4"

    perftest(network.node[1],ndetwork.node[2],read_bw)

subtest1 = subtest.Subtest(test=small_read, "Small RDMA Send", number='1')
IBPerftest = test.Test(tests=subtests, description="Tests core RDMA operations across a network, validates operation of endpoints at the RDMA level."
