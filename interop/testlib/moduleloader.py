import re
import os
import importlib
import sys


##
# Note to future developers.  This module utilizes a bit of 
# functional programming out of necessity to walk filepaths
# of arbitrary depth.  Additional functional programming is
# used for terseness.   
# lambda functions and map/filter. Make sure you understand
# before you edit.
##

def load_modules(file_name, PACKAGE, skip_dir=None):
    """ Wrapper to encapsulate dynamically importing plugins
    """

    pysearchre = re.compile('.py$', re.IGNORECASE)

    # Return files in a directory
    load_dir = lambda dir: os.listdir(os.path.join(os.path.dirname(file_name), dir))
    # Module names are *.py files w/out the extension, return the module name
    get_module = lambda py: '.' + os.path.splitext(py)[0]


    def import_dir(path, directory):
        """ Recursively walks directories of the PACKAGE, and imports all submodules, returning the modules
        """

        importmod = '.'.join(path.split('/'))
        modules = []

        # Do recursive lookup on all relecant subdirectories of PACKAGE
        for f in directory:

            # Check that it's not a pycache or non-directory
            if not f.startswith('__') and not f.endswith('.py') and not f.endswith('.csv') and not f.endswith('.log') and not f.endswith('.md'):

                try:
                    modules += import_dir(path+"/"+f, load_dir(path + '/' + f))
                except NotADirectoryError:
                    sys.stderr.write("Need to do some cleanup... attempted to enter {}/{} as a directory\n take a look at {}'s src code for more detail".format(path,f, __file__))

        # modules under testlib are not tests and do not need to by dynamically loaded 
        if skip_dir and (importmod == skip_dir):
            return modules

        # Functional programming here gets the plugins as strings
        plugins = map(get_module, filter(pysearchre.search, directory))

        # Import the plugins
        importlib.import_module(importmod)

        # Compile list and return plugins
        for plugin in plugins:
            if not plugin.startswith('__'):
                modules.append(importlib.import_module(importmod + plugin, package=PACKAGE))
        return modules

    # returns list of plugins after import
    return import_dir(PACKAGE, load_dir(PACKAGE))

