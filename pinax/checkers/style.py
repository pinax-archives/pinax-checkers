import sys
import tokenize

from pylint.interfaces import IRawChecker
from pylint.checkers import BaseChecker


class PinaxStyleChecker(BaseChecker):
    def process_module(self, node):
        """
        extracts encoding from the stream and decodes each line, so that
        international text's length is properly calculated.
        """
        stream = node.file_stream
        stream.seek(0)  # XXX may be removed with astng > 0.23
        readline = stream.readline
        if sys.version_info < (3, 0):
            if node.file_encoding is not None:
                readline = lambda: stream.readline().decode(
                    node.file_encoding,
                    "replace"
                )
        self.process_tokens(tokenize.generate_tokens(readline))


class QuotationStyleChecker(PinaxStyleChecker):
    """
    Check for use of double-quotes instead of single-quotes
    """
    
    __implements__ = IRawChecker
    
    name = "quotation"
    msgs = {
        "C9801": (
            "Single-quotes are in use instead of double-quotes",
            "Pinax coding standard requires double-quotes instead of "
            "single-quotes."
        ),
    }
    options = ()
    
    def process_tokens(self, tokens):
        for (tok_type, token, start, _, _) in tokens:
            if tok_type == 3:
                if token.startswith("'") and token.endswith("'"):
                    if '"' not in token:
                        self.add_message("C9801", line=start[0])


def get_offset(line):
    if line.isspace():
        return len(line) - 1
    return len(line) - len(line.lstrip())


class IndentationStyleChecker(PinaxStyleChecker):
    """
    Check for blank lines to be indented to the same level as the previous
    line.
    """
    
    __implements__ = IRawChecker
    
    name = "indentation"
    msgs = {
        "C9901": (
            "Line indent doesn't match block (Expected: %s, Got: %s)",
            "Blank lines are indented to the appropriate level for the block "
            "they are in."
        ),
        "C9902": (
            "Blank Line is Indented Too Much.",
            "A Blank Line has been indented too much."
        ),
    }
    options = ()
    
    def process_tokens(self, tokens):
        last_indent = None
        last_lines = []
        handled = set()
        
        for (tok_type, _, start, _, line) in tokens:
            if tok_type == 54 and line.isspace():
                offset = get_offset(line)
                if last_indent is None:
                    last_indent = offset
                    last_lines.append(start[0])
                elif offset != last_indent:
                    self.add_message("C9902", line=start[0])
                else:
                    last_lines.append(start[0])
            else:
                if not start[0] in handled:
                    if last_indent is not None:
                        offset = get_offset(line)
                        if offset != last_indent:
                            for lineno in last_lines:
                                self.add_message(
                                    "C9901",
                                    line=lineno,
                                    args=(offset, last_indent)
                                )
                        last_indent = None
                        last_lines = []
                    handled.add(start[0])


def register(linter):
    linter.register_checker(QuotationStyleChecker(linter))
    linter.register_checker(IndentationStyleChecker(linter))
