"""Sections 4.4.3–4.4.4 — LL(1) table construction and table-driven predictive parser."""

from grammar import EPSILON, END_MARKER
from first_follow import first_of_string


def build_ll1_table(grammar, first, follow):
    table = {}
    is_ll1 = True

    for head, alt in grammar.all_productions():
        fa = first_of_string(first, alt)

        for a in fa:
            if a != EPSILON:
                key = (head, a)
                if key in table:
                    is_ll1 = False
                else:
                    table[key] = (head, alt)

        if EPSILON in fa:
            for b in follow[head]:
                key = (head, b)
                if key in table:
                    is_ll1 = False
                else:
                    table[key] = (head, alt)

    return table, is_ll1


def parse_ll1(grammar, table, input_string):
    """Algorithm 4.34 — Non-recursive predictive parser."""
    stack = [END_MARKER, grammar.start]
    symbols = list(input_string) + [END_MARKER]
    ip = 0

    while True:
        X = stack[-1]
        a = symbols[ip]

        if X == END_MARKER:
            return a == END_MARKER

        if X == a:
            stack.pop()
            ip += 1
        elif grammar.is_terminal(X) or X == END_MARKER:
            return False
        elif (X, a) not in table:
            return False
        else:
            _, production = table[(X, a)]
            stack.pop()
            if production != [EPSILON]:
                for sym in reversed(production):
                    stack.append(sym)
