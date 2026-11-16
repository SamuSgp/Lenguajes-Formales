"""Generic SDD evaluator — dependency graph method (Sections 5.1–5.2)."""

from grammar import EPSILON, END_MARKER


class TreeNode:
    __slots__ = ('symbol', 'children', 'prod_index', 'attrs', 'node_id')

    def __init__(self, symbol):
        self.symbol = symbol
        self.children = []
        self.prod_index = None
        self.attrs = {}
        self.node_id = -1


def build_prod_index(grammar):
    prod_list = list(grammar.all_productions())
    mapping = {}
    for i, (head, alt) in enumerate(prod_list):
        mapping[(head, tuple(alt))] = i
    return mapping, prod_list


def parse_to_tree(grammar, table, prod_map, input_string):
    root = TreeNode(grammar.start)
    stack = [(END_MARKER, None), (grammar.start, root)]
    symbols = list(input_string) + [END_MARKER] if input_string else [END_MARKER]
    ip = 0

    while True:
        top_sym, top_node = stack[-1]
        a = symbols[ip]

        if top_sym == END_MARKER:
            return root if a == END_MARKER else None

        if top_sym == a:
            stack.pop()
            top_node.attrs['lexval'] = a
            ip += 1
        elif grammar.is_terminal(top_sym) or top_sym == END_MARKER:
            return None
        elif (top_sym, a) not in table:
            return None
        else:
            head, alt = table[(top_sym, a)]
            stack.pop()
            top_node.prod_index = prod_map[(head, tuple(alt))]

            if alt == [EPSILON]:
                top_node.children = [TreeNode(EPSILON)]
            else:
                children = [TreeNode(s) for s in alt]
                top_node.children = children
                for c in reversed(children):
                    stack.append((c.symbol, c))


def _assign_ids(root):
    counter = [0]
    def walk(node):
        node.node_id = counter[0]
        counter[0] += 1
        for c in node.children:
            walk(c)
    walk(root)


def _collect_nodes(root):
    nodes = {}
    def walk(n):
        nodes[n.node_id] = n
        for c in n.children:
            walk(c)
    walk(root)
    return nodes


def build_dependency_graph(root, rules, attr_decls):
    _assign_ids(root)
    vertices = set()
    edges = []
    rule_info = {}

    def resolve(node, pos):
        return node if pos == 0 else node.children[pos - 1]

    def process(node):
        if node.symbol == EPSILON:
            return

        if node.prod_index is None:
            vertices.add((node.node_id, 'lexval'))
        else:
            for attr_name, _ in attr_decls.get(node.symbol, []):
                vertices.add((node.node_id, attr_name))

            for rule in rules.get(node.prod_index, []):
                def_pos, def_attr = rule['defines']
                def_node = resolve(node, def_pos)
                target = (def_node.node_id, def_attr)
                vertices.add(target)
                rule_info[target] = (rule, node)

                for use_pos, use_attr in rule['uses']:
                    use_node = resolve(node, use_pos)
                    source = (use_node.node_id, use_attr)
                    vertices.add(source)
                    edges.append((source, target))

        for c in node.children:
            process(c)

    process(root)
    return vertices, edges, rule_info


def topological_sort(vertices, edges):
    adj = {v: [] for v in vertices}
    in_deg = {v: 0 for v in vertices}

    for u, v in edges:
        adj[u].append(v)
        in_deg[v] += 1

    queue = sorted(v for v in vertices if in_deg[v] == 0)
    order = []

    while queue:
        v = queue.pop(0)
        order.append(v)
        for w in adj[v]:
            in_deg[w] -= 1
            if in_deg[w] == 0:
                queue.append(w)
        queue.sort()

    return order, len(order) < len(vertices)


def evaluate_attrs(root, order, rule_info):
    nodes = _collect_nodes(root)

    for nid, attr in order:
        node = nodes[nid]
        if attr == 'lexval':
            continue
        if (nid, attr) not in rule_info:
            continue

        rule, parent = rule_info[(nid, attr)]
        vals = []
        for p, a in rule['uses']:
            src = parent if p == 0 else parent.children[p - 1]
            vals.append(src.attrs[a])
        node.attrs[attr] = rule['fn'](vals)

    return nodes


def print_tree(root, attr_decls, depth=0):
    indent = "  " * depth
    if root.symbol == EPSILON:
        print(f"{indent}e")
        return
    if root.prod_index is None:
        print(f"{indent}{root.symbol} [lexval='{root.attrs.get('lexval', '')}']")
    else:
        parts = []
        for a, _ in attr_decls.get(root.symbol, []):
            if a in root.attrs:
                parts.append(f"{a}={root.attrs[a]}")
        print(f"{indent}{root.symbol} [{', '.join(parts)}]")
    for c in root.children:
        print_tree(c, attr_decls, depth + 1)


def print_eval_order(order, nodes):
    print("Evaluation order:")
    for i, (nid, attr) in enumerate(order):
        node = nodes[nid]
        val = node.attrs.get(attr, '?')
        if attr == 'lexval':
            print(f"  {i+1}. {node.symbol}#{nid}.lexval = '{val}'")
        else:
            print(f"  {i+1}. {node.symbol}#{nid}.{attr} = {val}")
