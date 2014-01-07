import cStringIO
import tokenize
import unittest

import pylint

from mock import patch

from pinax.checkers.style import QuotationStyleChecker


class QuotationTest(unittest.TestCase):

    @patch("pylint.lint.PyLinter.add_message")
    def test_single_quote_fail(self, AddMessageMock):
        s = cStringIO.StringIO("def function_called('some string', 23):")
        tokens = tokenize.generate_tokens(s.readline)
        linter = pylint.lint.PyLinter()
        checker = QuotationStyleChecker(linter)
        checker.process_tokens(tokens)
        AddMessageMock.assert_called_with("C9801", 1, None, None)

    @patch("pylint.lint.PyLinter.add_message")
    def test_single_quote_multiline_fail(self, AddMessageMock):
        s = cStringIO.StringIO("""
def function_called("some string", 23):
    x = 1
    s = 'This is a valid "entry"'
    y = 500
    return 'Invalid'
""")
        tokens = tokenize.generate_tokens(s.readline)
        linter = pylint.lint.PyLinter()
        checker = QuotationStyleChecker(linter)
        checker.process_tokens(tokens)
        AddMessageMock.assert_called_with("C9801", 6, None, None)

    @patch("pylint.lint.PyLinter.add_message")
    def test_single_quote_multiple_tokens_fail(self, AddMessageMock):
        s = cStringIO.StringIO("""
def function_called("some string", 23):
    x = 1
    s = 'This is an invalid string'
    y = 500
    return 'Invalid'
""")
        tokens = tokenize.generate_tokens(s.readline)
        linter = pylint.lint.PyLinter()
        checker = QuotationStyleChecker(linter)
        checker.process_tokens(tokens)
        self.assertEquals(AddMessageMock.call_count, 2)

    @patch("pylint.lint.PyLinter.add_message")
    def test_single_quote_wrap_double_pass(self, AddMessageMock):
        s = cStringIO.StringIO("""
def function_called('some "inner" string', 23):
""")
        tokens = tokenize.generate_tokens(s.readline)
        linter = pylint.lint.PyLinter()
        checker = QuotationStyleChecker(linter)
        checker.process_tokens(tokens)
        self.assertEquals(AddMessageMock.call_count, 0)
