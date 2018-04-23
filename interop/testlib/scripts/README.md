scripts
=======

the */scripts* subdirectory is intended for storing pluggable test scripts
 
Summary
-------
This README is intended to be a quick reference for script writing.  This test framework has some pluggable functionality that makes 
test writing quick and easy.  

Test Writing Instructions
-------------------------
1. It is recommended, but not required to create a new .py file for your new test.  This can be placed in any directory or subdirectory under /scripts.
2. In your new file, create a function that runs your test. 
3. Create a `Test()` object, and assign it to an instance variable.  In the instansiation of the object, pass the function to the `Test()`
e.g. `myTest=Test(script=myFunction)`
4. Optionally assign the test to a group or several groups, and give the test object a description.
5. Your new test is now executable by interop.py.  It is callable by the name of the object variable `interop.py -t myTest` or by the 
group name `interop.py -g myGroup`.  Try running `interop.py -pt` or `interop.py -pg` to see your test. 


Last Updated
------------
4-16-2018
