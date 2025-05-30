from core.lexer.token import TokenType
from dataclasses import dataclass
from typing import Tuple, Union


Symbol = Union[str, TokenType]


@dataclass(frozen=True)
class Production:
    lhs: Symbol
    rhs: Tuple[Symbol, ...]
