from core.lexer.token import TokenType
from dataclasses import dataclass
from typing import Tuple, Union


Symbol = Union[str, TokenType]


class Production:
    lhs: Symbol
    rhs: Tuple[Symbol, ...]

    def __init__(self, lhs: Symbol, rhs: Tuple[Symbol, ...]):
        self.lhs = lhs
        self.rhs = rhs
