import testlib.classes.test as Test



def sample_test1():

    print( "this is running sample_test1 that is imported from /infiniband/sample_tests.py")


def sample_test2():

    print( "this is running sample_test2 that is imported from /infiniband/sample_tests.py")


sampleTest1 = Test.Test(script=sample_test1, name="sample1", description="this is the sample_test1 description", group=["latency_tests","bandwidth_tests"])

sampleTest2 = Test.Test(script=sample_test2)
sampleTest2.set_description("this is the sample_test2 description")
sampleTest2.set_name("sample2")
sampleTest2.add_group("latency_tests")
