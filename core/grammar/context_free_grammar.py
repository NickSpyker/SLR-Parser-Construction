from core.grammar.production import Symbol, Production
from dataclasses import dataclass
from typing import List


@dataclass
class ContextFreeGrammar:
    start_symbol: Symbol
    productions: List[Production]
