"""Section 4.4.2 — FIRST and FOLLOW sets."""

from grammar import EPSILON, END_MARKER


def compute_first(grammar):
    first = {}
    for t in grammar.terminals:
        first[t] = {t}
    for nt in grammar.nonterminals:
        first[nt] = set()

    changed = True
    while changed:
        changed = False
        for head, alt in grammar.all_productions():
            if alt == [EPSILON]:
                if EPSILON not in first[head]:
                    first[head].add(EPSILON)
                    changed = True
            else:
                if _add_first_of_string(first, head, alt):
                    changed = True
    return first


def _add_first_of_string(first, target, symbols):
    changed = False
    all_eps = True
    for sym in symbols:
        sym_first = first.get(sym, set())
        for t in sym_first:
            if t != EPSILON and t not in first[target]:
                first[target].add(t)
                changed = True
        if EPSILON not in sym_first:
            all_eps = False
            break
    if all_eps and EPSILON not in first[target]:
        first[target].add(EPSILON)
        changed = True
    return changed


def first_of_string(first, symbols):
    result = set()
    if not symbols or symbols == [EPSILON]:
        return {EPSILON}
    all_eps = True
    for sym in symbols:
        sym_first = first.get(sym, set())
        result |= (sym_first - {EPSILON})
        if EPSILON not in sym_first:
            all_eps = False
            break
    if all_eps:
        result.add(EPSILON)
    return result


def compute_follow(grammar, first):
    follow = {nt: set() for nt in grammar.nonterminals}
    follow[grammar.start].add(END_MARKER)

    changed = True
    while changed:
        changed = False
        for head, alt in grammar.all_productions():
            if alt == [EPSILON]:
                continue
            for i, sym in enumerate(alt):
                if not grammar.is_nonterminal(sym):
                    continue
                beta = alt[i + 1:]
                if beta:
                    fb = first_of_string(first, beta)
                    for t in fb - {EPSILON}:
                        if t not in follow[sym]:
                            follow[sym].add(t)
                            changed = True
                    if EPSILON in fb:
                        for t in follow[head]:
                            if t not in follow[sym]:
                                follow[sym].add(t)
                                changed = True
                else:
                    for t in follow[head]:
                        if t not in follow[sym]:
                            follow[sym].add(t)
                            changed = True
    return follow


def print_sets(grammar, first, follow):
    sorted_nts = sorted(grammar.nonterminals)
    for nt in sorted_nts:
        print(f"First({nt}) = {{{_fmt(first[nt], False)}}}")
    for nt in sorted_nts:
        print(f"Follow({nt}) = {{{_fmt(follow[nt], True)}}}")


def _fmt(s, with_dollar):
    regular = sorted(t for t in s if t != EPSILON and t != END_MARKER)
    parts = regular[:]
    if EPSILON in s:
        parts.append(EPSILON)
    if with_dollar and END_MARKER in s:
        parts.append(END_MARKER)
    return ', '.join(parts)
