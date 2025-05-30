from core.grammar.context_free_grammar import ContextFreeGrammar


class ActionsTable:
    def __init__(self, cfg: ContextFreeGrammar) -> None:
        self.cfg = cfg
