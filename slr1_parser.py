"""Sections 4.5–4.6 — LR(0) items, canonical collection, SLR(1) tables, and LR parser."""

from grammar import EPSILON, END_MARKER

AUGMENTED_START = "S'"


class Item:
    __slots__ = ('head', 'body', 'dot')

    def __init__(self, head, body, dot):
        self.head = head
        self.body = body
        self.dot = dot

    def __eq__(self, other):
        return (self.head, self.body, self.dot) == (other.head, other.body, other.dot)

    def __hash__(self):
        return hash((self.head, self.body, self.dot))

    def after_dot(self):
        return self.body[self.dot] if self.dot < len(self.body) else None

    def advance(self):
        return Item(self.head, self.body, self.dot + 1)

    def is_reduce(self):
        return self.dot >= len(self.body)


def _slr_body(alt):
    return () if alt == [EPSILON] else tuple(alt)


def _build_production_list(grammar):
    prods = [(AUGMENTED_START, (grammar.start,))]
    for head, alt in grammar.all_productions():
        prods.append((head, _slr_body(alt)))
    return prods


def closure(items, productions, nonterminals):
    result = set(items)
    changed = True
    while changed:
        changed = False
        add = set()
        for item in result:
            B = item.after_dot()
            if B in nonterminals:
                for h, b in productions:
                    if h == B:
                        ni = Item(B, b, 0)
                        if ni not in result:
                            add.add(ni)
        if add:
            result |= add
            changed = True
    return frozenset(result)


def goto(items, symbol, productions, nonterminals):
    moved = frozenset(it.advance() for it in items if it.after_dot() == symbol)
    return closure(moved, productions, nonterminals) if moved else frozenset()


def build_slr1_tables(grammar, follow):
    """Algorithm 4.46 — SLR parsing table construction."""
    productions = _build_production_list(grammar)
    nonterminals = grammar.nonterminals | {AUGMENTED_START}
    all_symbols = grammar.terminals | grammar.nonterminals

    I0 = closure({Item(AUGMENTED_START, (grammar.start,), 0)}, productions, nonterminals)
    states = [I0]
    state_map = {I0: 0}
    transitions = {}

    i = 0
    while i < len(states):
        syms = {it.after_dot() for it in states[i]} - {None}
        for sym in syms:
            target = goto(states[i], sym, productions, nonterminals)
            if not target:
                continue
            if target not in state_map:
                state_map[target] = len(states)
                states.append(target)
            transitions[(i, sym)] = state_map[target]
        i += 1

    action = {}
    goto_table = {}
    is_slr1 = True

    for i, state in enumerate(states):
        for item in state:
            sym = item.after_dot()

            if sym is not None and grammar.is_terminal(sym) and (i, sym) in transitions:
                key = (i, sym)
                entry = ('s', transitions[key])
                if key in action and action[key] != entry:
                    is_slr1 = False
                action[key] = entry

            elif item.is_reduce():
                if item.head == AUGMENTED_START:
                    key = (i, END_MARKER)
                    entry = ('acc',)
                    if key in action and action[key] != entry:
                        is_slr1 = False
                    action[key] = entry
                else:
                    pi = None
                    for idx, (h, b) in enumerate(productions):
                        if h == item.head and b == item.body:
                            pi = idx
                            break
                    for a in follow[item.head]:
                        key = (i, a)
                        entry = ('r', pi)
                        if key in action and action[key] != entry:
                            is_slr1 = False
                        action[key] = entry

        for nt in grammar.nonterminals:
            if (i, nt) in transitions:
                goto_table[(i, nt)] = transitions[(i, nt)]

    return action, goto_table, is_slr1, productions


def parse_slr1(action, goto_table, productions, input_string):
    """Algorithm 4.44 — LR parsing algorithm."""
    stack = [0]
    symbols = list(input_string) + [END_MARKER]
    ip = 0

    while True:
        s = stack[-1]
        a = symbols[ip]
        entry = action.get((s, a))

        if entry is None:
            return False
        if entry[0] == 's':
            stack.append(entry[1])
            ip += 1
        elif entry[0] == 'r':
            head, body = productions[entry[1]]
            for _ in range(len(body)):
                stack.pop()
            t = stack[-1]
            if (t, head) not in goto_table:
                return False
            stack.append(goto_table[(t, head)])
        elif entry[0] == 'acc':
            return True
        else:
            return False
