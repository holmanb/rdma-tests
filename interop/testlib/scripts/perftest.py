import testlib.test as test
import testlib.subtest as subtest
import testlib.classes.network as network

import socket
import errno
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
    finalout = [True, ""]
    print(out1)
    print(out2)
    for i in [out1, out2]:
        if not i:
            print("skipping output: {}".format(i))
            continue
        if not i[0]:
            finalout[1]+=i[1]
            finalout[0] = False
    return finalout


def get_ib_dev_name(node):
    out=node.command('ibv_devinfo')
    if out[1]:
        sys.stderr.write(out[1])

    # The mess below just gets the device name from the first line of ib_devinfo
    return out[0].split('\n')[0].split()[1]

def is_port_open(node, port):
    """ is the specified port open on this node?
    """
    stdout = node.command("lsof -i :{}".format(port))[0].strip()
    return False if stdout else True

def get_open_port(node, default):
    """ returns the next available port if default isn't open
    """
    port=default
    while(not is_port_open(node, port)):
        print("port: {} is currently in use on node {}".format(port, node.ethif.ip))
        port+=1
    return port

def get_interesting_output(output):
    o = ""
    out_flag = False
    for line in output[0].split('\n'):
        if not line.strip():
            continue
        if line.strip()[0] == "#":
            print(line)
            o+=line
            out_flag = True
            continue
        if out_flag is True:
            out_flag = False
            print(line)
            o+=line
    #print(output[0])
    if output[1]:
        print("errors:\n[{}]".format(output[1]))
    return output

def small_read():

    def kill_zombies(node,command):
        print(node.command("pkill -x {}".format(command))[1])

    def read_bw(server, client,default_port=18515):

        # need to figure out how to get device name 
        device_server = get_ib_dev_name(server)
        device_client = get_ib_dev_name(client)

        # need to figure out how to check if default port is active 
        #default_port = 18515
        available_port = get_open_port(server, default_port)
    #    available_port_client = get_open_port(client, default_port)

        # check to see if perfest is in use - wait 500 ms and try again if so
        cmd_server = "ib_read_bw -d {} -i 1 -p {} -s 1 -n 25000 -m 2048 -F".format(device_server, available_port)
        cmd_client = "ib_read_bw -d {} -i 1 -p {} -s 1 -n 25000 -m 2048 {} -F".format(device_client, available_port, str(server.ibif.ip))

        def cmd(func, command, result, key):
            """ Used for getting returned output from the threads
            """
            result[key] = func(command)

        threads=[]
        results = dict()
        threads.append(threading.Thread(target=cmd, args=[server.command, cmd_server,results,"server"]))
        threads.append(threading.Thread(target=cmd, args=[client.command, cmd_client,results,"client"]))

        print("starting threads:")
        print("on [{}] running: [{}]".format(server.ethif.ip, cmd_server))
        print("on [{}] running: [{}]".format(client.ethif.ip, cmd_client))
        for thread in threads:
            thread.start()
            time.sleep(0.5)

        # The next couple of lines are funky, but this allows the KeyboardInterrupt 
        # to be recognized
        try:
            threads[1].join()
        except KeyboardInterrupt:
            print("Exception got caught,killing zombies")
            kill_zombies(server, cmd_server.split()[0])
            kill_zombies(client, cmd_client.split()[0])

            # Output the results  
            print("Printing perftest results")
            out = results['server']
            get_interesting_output(out)
            print("server: {}".format(server.ethif.ip))
            out = results['client']
            get_interesting_output(out)
            print("client: {}".format(client.ethif.ip))
            raise KeyboardInterrupt

        print("Printing perftest results")
        out = results['client']
        get_interesting_output(out)
        print("client: {}".format(client.ethif.ip))

        try:
            threads[0].join()
        except KeyboardInterrupt:
            print("Exception got caught,killing zombies")
            kill_zombies(server, cmd_server.split()[0])
            kill_zombies(client, cmd_client.split()[0])

            # Output the results  
            print("Printing perftest results")
            out = results['server']
            print("server: {}".format(server.ethif.ip))
            get_interesting_output(out)
            out = results['client']
            print("client: {}".format(client.ethif.ip))
            get_interesting_output(out)
            raise KeyboardInterrupt

        print("Printing perftest results")
        out = results['server']
        print("server: {}".format(server.ethif.ip))
        get_interesting_output(out)


        print("threads done")




        out = results['client']
        print("client: {}".format(client.ethif.ip))

        get_interesting_output(out)

        print("Done printing perftest results")
        print("sleeping")
        time.sleep(5)
        print("waking")
    return [False, "THIS ISN'T THE ACTUAL OUTPUT, THIS TEST IS WIP"]

    perftest(network.nodes[1],network.nodes[2],read_bw)

subtest1 = subtest.Subtest(test=small_read, name="Small RDMA Send", number='1')

subtests=[subtest1]
IBPerftest = test.Test(tests=subtests, description="Tests core RDMA operations across a network, validates operation of endpoints at the RDMA level.")

