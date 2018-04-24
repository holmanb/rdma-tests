
class SubtestReturnValueError(Exception):
    pass

class Subtest:
    def __init__(self,name=None,test=None,number=None):
        """ Lightweight class for subtests
        """
        self.name=name
        self.test=test
        self.number=number

    def run(self):
        """ Run the subtest
        """
        def validate_output(output):

            # Tests must conform to the output describied in this string
            error =  "ERROR: In test {} {}\n".format(self.name, self.number)
            error += "Tests must return the following format: [bool_pass_or_fail, str_description]\n"
            error += "If tests cannot complete, they should raise TestCannotComplete() exception explaining the error"

            # Validate output
            valid_output = isinstance(output, list) and len(output)==2 and isinstance(output[0], bool) and isinstance(output[1], str)
            if not valid_output:
                raise SubtestReturnValueError(error)

        output = self.test()
        validate_output(output)
        return {"success" : output[0], "comments" : output [1]}

    def __lt__(self, other):
        """ Allows Tests to be sorted.  Default sorting should be by name.
        """
        try:
            return self.number < other.number
        except AttributeError:
            return NotImplemented

