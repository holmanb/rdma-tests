import Test



def sample_test1():

    print( "this is running sample_test1 that is imported from /infiniband/sample_tests.py")


def sample_test2():

    print( "this is running sample_test2 that is imported from /infiniband/sample_tests.py")


sampleTest1_obj = Test.Test(script=sample_test1, name="sample1", description="this is the sample_test1 description")

sampleTest2_obj = Test.Test(script=sample_test2)
sampleTest2_obj.set_description("this is the sample_test2 description")
sampleTest2_obj.set_name("sample2")

TESTS={
     sampleTest1_obj.get_name():sampleTest1_obj,
     sampleTest2_obj.get_name():sampleTest2_obj
        }

GROUPS={
        "latency_tests": [sampleTest1_obj, sampleTest2_obj],
        "bandwidth_tests": [sampleTest1_obj]
        }
