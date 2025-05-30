from core.lexer.lexer import Lexer, ScanState
from core.error.error import Error


def parse(buffer: str) -> str:
    lexer = Lexer(buffer)
    tokens = lexer.scan()
    if lexer.scan_state == ScanState.FAILURE:
        return Error.build_lexer_error_msg(lexer)
    return f"{tokens}"
