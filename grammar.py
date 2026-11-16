EPSILON = 'e'
END_MARKER = '$'
START_SYMBOL = 'S'


class Grammar:
    def __init__(self):
        self.nonterminals = set()
        self.terminals = set()
        self.productions = {}
        self.start = START_SYMBOL

    @staticmethod
    def read_from_stdin():
        g = Grammar()
        n = int(input())
        for _ in range(n):
            line = input().strip()
            head, rest = line.split('->')
            head = head.strip()
            g.nonterminals.add(head)
            alternatives = rest.strip().split()
            prod_list = []
            for alt in alternatives:
                if alt == EPSILON:
                    prod_list.append([EPSILON])
                else:
                    prod_list.append(list(alt))
            g.productions[head] = prod_list

        for nt in g.nonterminals:
            for alt in g.productions[nt]:
                for sym in alt:
                    if sym != EPSILON and sym not in g.nonterminals:
                        g.terminals.add(sym)

        return g

    @staticmethod
    def read_from_lines(lines):
        g = Grammar()
        idx = 0
        n = int(lines[idx].strip())
        idx += 1
        for _ in range(n):
            line = lines[idx].strip()
            idx += 1
            head, rest = line.split('->')
            head = head.strip()
            g.nonterminals.add(head)
            alternatives = rest.strip().split()
            prod_list = []
            for alt in alternatives:
                if alt == EPSILON:
                    prod_list.append([EPSILON])
                else:
                    prod_list.append(list(alt))
            g.productions[head] = prod_list

        for nt in g.nonterminals:
            for alt in g.productions[nt]:
                for sym in alt:
                    if sym != EPSILON and sym not in g.nonterminals:
                        g.terminals.add(sym)

        return g

    def is_nonterminal(self, sym):
        return sym in self.nonterminals

    def is_terminal(self, sym):
        return sym in self.terminals

    def all_productions(self):
        for head, alts in self.productions.items():
            for alt in alts:
                yield head, alt
