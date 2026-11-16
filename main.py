#!/usr/bin/env python3
"""Entry point — reads grammar, computes sets, determines parser type, parses strings."""

import sys
from grammar import Grammar, EPSILON
from first_follow import compute_first, compute_follow, print_sets
from ll1_parser import build_ll1_table, parse_ll1
from slr1_parser import build_slr1_tables, parse_slr1


def read_and_parse_strings(parse_fn):
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line == '':
            break
        s = '' if line == EPSILON else line
        print('yes' if parse_fn(s) else 'no')


def main():
    show_sets = '--sets' in sys.argv
    grammar = Grammar.read_from_stdin()
    first = compute_first(grammar)
    follow = compute_follow(grammar, first)

    if show_sets:
        print_sets(grammar, first, follow)

    ll1_table, is_ll1 = build_ll1_table(grammar, first, follow)
    action, goto_table, is_slr1, productions = build_slr1_tables(grammar, follow)

    if is_ll1 and is_slr1:
        while True:
            print('Select a parser (T: for LL(1), B: for SLR(1), Q: quit):')
            choice = input().strip()
            if choice == 'Q':
                break
            elif choice == 'T':
                read_and_parse_strings(lambda s: parse_ll1(grammar, ll1_table, s))
            elif choice == 'B':
                read_and_parse_strings(lambda s: parse_slr1(action, goto_table, productions, s))
    elif is_ll1:
        print('Grammar is LL(1).')
        read_and_parse_strings(lambda s: parse_ll1(grammar, ll1_table, s))
    elif is_slr1:
        print('Grammar is SLR(1).')
        read_and_parse_strings(lambda s: parse_slr1(action, goto_table, productions, s))
    else:
        print('Grammar is neither LL(1) nor SLR(1).')


if __name__ == '__main__':
    main()
