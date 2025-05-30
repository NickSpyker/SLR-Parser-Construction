from core.grammar.first_follow import compute_first, compute_follow
from core.grammar.goto import construct_LR0_items


class ActionsTable:
    def __init__(self, productions, start_symbol):
        self.productions = productions
        self.start_symbol = start_symbol
        # Calcul des FIRST et FOLLOW
        self.FIRST = compute_first(productions)
        self.FOLLOW = compute_follow(productions, self.FIRST, start_symbol)
        # Construction des états LR(0) et transitions
        states, transitions = construct_LR0_items(productions, start_symbol)
        self.states = states
        # Table ACTION initialement vide
        self.table = {i: {} for i in range(len(states))}
        # Remplissage des entrées SHIFT et ACCEPT/REDUCE
        for i, I in enumerate(states):
            for (lhs, rhs, dot) in I:
                # 1) SHIFT : A -> α • a β avec a terminal
                if dot < len(rhs):
                    a = rhs[dot]
                    if a not in [prod[0] for prod in productions]:  # a est terminal si ce n'est pas un lhs
                        # S'il existe une transition sur ce terminal
                        if (i, a) in transitions:
                            j = transitions[(i, a)]
                            self.table[i][a] = ('shift', j)
                else:
                    # 2) REDUCE ou ACCEPT : item final A -> α •
                    if lhs == "S'":
                        # Acceptation si c'est l'item S' -> S •
                        self.table[i]['$'] = ('accept',)
                    else:
                        # Pour chaque symbole dans FOLLOW(lhs), on réduit
                        prod_index = productions.index((lhs, rhs))
                        for a in self.FOLLOW[lhs]:
                            # Ne pas écraser une action existante : vérifier conflit
                            if a in self.table[i]:
                                # Conflit possible (non-SLR(1) si ce cas se produit)
                                pass
                            else:
                                self.table[i][a] = ('reduce', prod_index)

    def __str__(self):
        # Affichage lisible de la table ACTION
        lines = []
        for i, actions in self.table.items():
            row = f"Etat {i}: " + ", ".join(f"{sym}: {act}" for sym, act in actions.items())
            lines.append(row)
        return "\n".join(lines)

class GotoTable:
    def __init__(self, productions, start_symbol):
        # Utilise la même construction d'états que ActionsTable
        states, transitions = construct_LR0_items(productions, start_symbol)
        self.table = {i: {} for i in range(len(states))}
        for (i, X), j in transitions.items():
            # On ne met dans GOTO que si X est un non-terminal
            if X in [prod[0] for prod in productions]:
                self.table[i][X] = j

    def __str__(self):
        # Affichage lisible de la table GOTO
        lines = []
        for i, gotos in self.table.items():
            row = f"Etat {i}: " + ", ".join(f"{sym}: {state}" for sym, state in gotos.items())
            lines.append(row)
        return "\n".join(lines)
