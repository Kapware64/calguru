"""Assertion helper methods"""


class Assertions(object):
    """
    Methods to perform commonly-used assertions; utilized by unittest methods
    """

    @staticmethod
    def assert_bad_op_error(unit_test_class, op_func, correct_error,
                            func_success_msg, **op_func_args):
        """
        Check that an input invalid operation raises correct error.

        :param unit_test_class: Class to call assertions from.
        :param op_func: Function of operation that should fail and raise error
        :param correct_error: Error that should be raised
        :param func_success_msg: Message to display if op_func doesn't raise
        any error
        :param op_func_args: Dictionary of arguments to be used for
        calling op_func. Key/value pairs are arranged as such:
        {<arg name>: <arg value>}
        """

        # Whether any error is raised
        error_raised = False

        try:
            # Perform operation
            op_func(**op_func_args)
        except correct_error:  # Correct error is raised
            error_raised = True
        except:  # Error is raised, but it is not the correct one
            error_raised = True
            unit_test_class.assertTrue(
                False, msg="Incorrect error is raised for invalid operation.")

        # No error is raised
        if not error_raised:
            unit_test_class.assertTrue(False, msg=func_success_msg)
