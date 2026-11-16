"""Item 3 — SDD evaluator entry point."""

import sys
from grammar import Grammar
from first_follow import compute_first, compute_follow, print_sets
from ll1_parser import build_ll1_table
from sdd_definition import GRAMMAR_LINES, RULES, RULES_CIRCULAR, ATTR_DECLS
from sdd_evaluator import (
    build_prod_index, parse_to_tree, build_dependency_graph,
    topological_sort, evaluate_attrs, print_tree, print_eval_order,
)


def main():
    grammar = Grammar.read_from_lines(GRAMMAR_LINES)
    first = compute_first(grammar)
    follow = compute_follow(grammar, first)

    if '--sets' in sys.argv:
        print_sets(grammar, first, follow)
        print()

    table, is_ll1 = build_ll1_table(grammar, first, follow)
    if not is_ll1:
        print("Error: SDD grammar is not LL(1).")
        return

    prod_map, _ = build_prod_index(grammar)

    use_circular = '--circular' in sys.argv
    rules = RULES_CIRCULAR if use_circular else RULES

    if use_circular:
        print("(Using circular SDD for testing)\n")

    print("SDD Evaluator")
    print("Grammar: x = expr  (with +, *, parentheses, digits 1-3)")
    print("Enter strings to evaluate (empty line to stop):\n")

    while True:
        try:
            line = input()
        except EOFError:
            break
        if line == '':
            break

        s = '' if line == 'e' else line
        root = parse_to_tree(grammar, table, prod_map, s)
        if root is None:
            print("no\n")
            continue

        verts, edges, rule_info = build_dependency_graph(root, rules, ATTR_DECLS)
        order, circular = topological_sort(verts, edges)

        if circular:
            print("The SDD is circular for this input.\n")
            continue

        nodes = evaluate_attrs(root, order, rule_info)

        print("Annotated parse tree:")
        print_tree(root, ATTR_DECLS)
        print()
        print_eval_order(order, nodes)
        print()
        print(f"Result: x = {root.attrs.get('val', '?')}")
        print(f"Operations: {root.attrs.get('ops', '?')}")
        print()


if __name__ == '__main__':
    main()
