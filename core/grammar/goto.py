# Construction des états LR(0) (items avec fermeture et goto)
def closure(items, productions):
    """
    Calcule la fermeture d'un ensemble d'items LR(0).
    items : ensemble de tuples (lhs, rhs, dot_pos)
    productions : liste de (lhs, rhs_list)
    """
    nonterminals = set(p[0] for p in productions)
    closure_set = set(items)
    changed = True
    while changed:
        changed = False
        for (lhs, rhs, dot) in list(closure_set):
            # Si le point est avant un non-terminal B, on ajoute B -> • gamma
            if dot < len(rhs):
                B = rhs[dot]
                if B in nonterminals:
                    for (A, prod_rhs) in productions:
                        if A == B:
                            new_item = (A, tuple(prod_rhs), 0)
                            if new_item not in closure_set:
                                closure_set.add(new_item)
                                changed = True
    return closure_set

def goto(items, X, productions):
    """
    Calcul la transition GOTO(I, X) pour un ensemble d'items I et un symbole X.
    """
    moved = set()
    for (lhs, rhs, dot) in items:
        if dot < len(rhs) and rhs[dot] == X:
            moved.add((lhs, rhs, dot+1))
    return closure(moved, productions) if moved else set()

def construct_LR0_items(productions, start_symbol):
    """
    Construit la collection canonique des ensembles d'items LR(0).
    Renvoie la liste d'états (ensembles d'items) et la table de transitions goto (state,sym)->state.
    """
    # Ajouter l'axiome augmenté S' -> S
    augmented = ('S\'', [start_symbol])
    prods = [augmented] + productions
    # État initial
    I0 = closure({('S\'', tuple([start_symbol]), 0)}, prods)
    states = [I0]
    transitions = {}  # (state_index, symbole) -> state_index
    changed = True
    while changed:
        changed = False
        for i, I in enumerate(states):
            for X in {sym for (lhs, rhs, dot) in I if dot < len(rhs) for sym in [rhs[dot]]}:
                J = goto(I, X, prods)
                if J:
                    if J not in states:
                        states.append(J)
                        changed = True
                    j = states.index(J)
                    transitions[(i, X)] = j
    return states, transitions

# # Exemple d'utilisation : on extrait l'axiome comme lhs de la première production
# productions = [
#     ('E', ['T', 'E2']),
#     ('E2', ['+', 'T', 'E2']),
#     ('E2', []),
#     ('T', ['F', 'T2']),
#     ('T2', ['*', 'F', 'T2']),
#     ('T2', []),
#     ('F', ['(', 'E', ')']),
#     ('F', ['id'])
# ]
# start_symbol = 'E'
# states, transitions = construct_LR0_items(productions, start_symbol)
# print(f"Nombre d'états LR(0): {len(states)}")
# for i, I in enumerate(states):
#     print(f"État {i}:")
#     for item in I:
#         lhs, rhs, dot = item
#         rhs_with_dot = list(rhs)
#         rhs_with_dot.insert(dot, '•')
#         print(f"  {lhs} -> {' '.join(rhs_with_dot)}")
