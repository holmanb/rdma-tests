



def sample_test1():

    print( "this is running sample_test1 that is imported from /infiniband/sample_tests.py")


def sample_test2():

    print( "this is running sample_test2 that is imported from /infiniband/sample_tests.py")


TESTS={
        "sample1":sample_test1,
        "sample2":sample_test2
        }

GROUPS={
        "latency_tests": (sample_test1, sample_test2),
        "bandwidth_tests": (sample_test2)
        }
