# Calcul des ensembles FIRST et FOLLOW
def compute_first(productions):
    """
    Calcule l'ensemble FIRST pour chaque symbole (terminaux et non-terminaux).
    productions : liste de (lhs, rhs), avec rhs une liste de symboles.
    """
    nonterminals = set(p[0] for p in productions)
    symbols = set(nonterminals)
    for _, rhs in productions:
        symbols.update(rhs)
    terminals = symbols - nonterminals

    # Initialisation : FIRST(term) = {term}, FIRST(nonterm) = {}
    FIRST = {sym: set() for sym in symbols}
    for t in terminals:
        FIRST[t].add(t)
    epsilon = ''  # on représente ε par la chaîne vide

    changed = True
    while changed:
        changed = False
        for lhs, rhs in productions:
            if not rhs:
                # A -> ε
                if epsilon not in FIRST[lhs]:
                    FIRST[lhs].add(epsilon)
                    changed = True
            else:
                # Calcul de FIRST(rhs) séquentiellement
                first_rhs = set()
                for symbol in rhs:
                    first_rhs |= (FIRST[symbol] - {epsilon})
                    if epsilon not in FIRST[symbol]:
                        break
                else:
                    # Si tous les symboles de rhs contiennent ε, on ajoute ε
                    first_rhs.add(epsilon)
                if not first_rhs.issubset(FIRST[lhs]):
                    FIRST[lhs] |= first_rhs
                    changed = True
    return FIRST

def compute_follow(productions, FIRST, start_symbol):
    """
    Calcule l'ensemble FOLLOW pour chaque non-terminal.
    start_symbol : symbole de départ de la grammaire.
    """
    nonterminals = set(p[0] for p in productions)
    FOLLOW = {A: set() for A in nonterminals}
    FOLLOW[start_symbol].add('$')  # $ signe de fin de chaîne
    epsilon = ''

    changed = True
    while changed:
        changed = False
        for lhs, rhs in productions:
            trailer = FOLLOW[lhs].copy()
            # On parcourt rhs de droite à gauche
            for symbol in reversed(rhs):
                if symbol in nonterminals:
                    if not trailer.issubset(FOLLOW[symbol]):
                        FOLLOW[symbol] |= trailer
                        changed = True
                    if epsilon in FIRST[symbol]:
                        # Si symbol peut produire ε, on fusionne trailer avec FIRST(symbol) sans ε
                        trailer |= (FIRST[symbol] - {epsilon})
                    else:
                        trailer = FIRST[symbol].copy()
                else:
                    # Symbol est terminal : trailer devient FIRST(symbol) (soit lui-même)
                    trailer = FIRST[symbol].copy()
    return FOLLOW
