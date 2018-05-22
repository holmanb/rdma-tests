scripts
=======

the */scripts* subdirectory is intended for storing pluggable test scripts
 
Summary
-------
This README is intended to be a quick reference for script writing.  This test framework has some pluggable functionality that makes 
adding new tests quick and easy. To write a new test, follow the instructions below.  It may be helpful to look at the code of existing 
tests as examples. 

Test Writing Instructions
-------------------------
1. It is recommended, but not required to create a new .py file for your new test.  This can be placed in any directory or subdirectory 
under /scripts.
2. In your new file, create a function that runs your test. 
3. Create a `Subtest()` object, and pass it the test function and name/number. 
4. Create a `Test()` object, and assign it to an instance variable.  In the Test object instansiation, pass it a list that contains all of
your Subtest objects. 
e.g. `myTest=Test(tests=[subtest1, subtest2], description="a short description for future users")`
5. Optionally assign the test to a group or several groups, and give the test object a description.
6. Your new test is now executable by interop.py.  It is callable by the name of the object variable `interop.py -t myTest` and if you 
made it a part of a group, it is also callable by the group name `interop.py -g myGroup`.  
7. Try running `interop.py -pt` or `interop.py -pg` to verify that your test is plugged into the framework. 



Last Updated
------------
5-22-2018
