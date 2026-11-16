"""SDD definition — grammar, attributes and semantic rules stored as data."""

from grammar import EPSILON

GRAMMAR_LINES = [
    "6",
    "S -> x=E",
    "E -> TA",
    "A -> +TA e",
    "T -> FM",
    "M -> *FM e",
    "F -> (E) 1 2 3",
]

ATTR_DECLS = {
    'S': [('val', 'syn'), ('ops', 'syn')],
    'E': [('val', 'syn'), ('ops', 'syn')],
    'A': [('inh', 'inh'), ('val', 'syn'), ('ops', 'syn')],
    'T': [('val', 'syn'), ('ops', 'syn')],
    'M': [('inh', 'inh'), ('val', 'syn'), ('ops', 'syn')],
    'F': [('val', 'syn'), ('ops', 'syn')],
}

#   Position convention:  0 = head,  1..n = body symbols (1-indexed)
#   Each rule:  defines (pos, attr),  uses [(pos, attr), ...],  fn(args_list) -> value

RULES = {
    0: [  # S -> x = E          body: x[1] =[2] E[3]
        {'defines': (0, 'val'), 'uses': [(3, 'val')], 'fn': lambda a: a[0]},
        {'defines': (0, 'ops'), 'uses': [(3, 'ops')], 'fn': lambda a: a[0]},
    ],
    1: [  # E -> T A             body: T[1] A[2]
        {'defines': (2, 'inh'), 'uses': [(1, 'val')], 'fn': lambda a: a[0]},
        {'defines': (0, 'val'), 'uses': [(2, 'val')], 'fn': lambda a: a[0]},
        {'defines': (0, 'ops'), 'uses': [(1, 'ops'), (2, 'ops')],
         'fn': lambda a: a[0] + a[1]},
    ],
    2: [  # A -> + T A1          body: +[1] T[2] A1[3]
        {'defines': (3, 'inh'), 'uses': [(0, 'inh'), (2, 'val')],
         'fn': lambda a: a[0] + a[1]},
        {'defines': (0, 'val'), 'uses': [(3, 'val')], 'fn': lambda a: a[0]},
        {'defines': (0, 'ops'), 'uses': [(2, 'ops'), (3, 'ops')],
         'fn': lambda a: 1 + a[0] + a[1]},
    ],
    3: [  # A -> e
        {'defines': (0, 'val'), 'uses': [(0, 'inh')], 'fn': lambda a: a[0]},
        {'defines': (0, 'ops'), 'uses': [], 'fn': lambda a: 0},
    ],
    4: [  # T -> F M             body: F[1] M[2]
        {'defines': (2, 'inh'), 'uses': [(1, 'val')], 'fn': lambda a: a[0]},
        {'defines': (0, 'val'), 'uses': [(2, 'val')], 'fn': lambda a: a[0]},
        {'defines': (0, 'ops'), 'uses': [(1, 'ops'), (2, 'ops')],
         'fn': lambda a: a[0] + a[1]},
    ],
    5: [  # M -> * F M1          body: *[1] F[2] M1[3]
        {'defines': (3, 'inh'), 'uses': [(0, 'inh'), (2, 'val')],
         'fn': lambda a: a[0] * a[1]},
        {'defines': (0, 'val'), 'uses': [(3, 'val')], 'fn': lambda a: a[0]},
        {'defines': (0, 'ops'), 'uses': [(2, 'ops'), (3, 'ops')],
         'fn': lambda a: 1 + a[0] + a[1]},
    ],
    6: [  # M -> e
        {'defines': (0, 'val'), 'uses': [(0, 'inh')], 'fn': lambda a: a[0]},
        {'defines': (0, 'ops'), 'uses': [], 'fn': lambda a: 0},
    ],
    7: [  # F -> ( E )           body: ([1] E[2] )[3]
        {'defines': (0, 'val'), 'uses': [(2, 'val')], 'fn': lambda a: a[0]},
        {'defines': (0, 'ops'), 'uses': [(2, 'ops')], 'fn': lambda a: a[0]},
    ],
    8: [  # F -> 1               body: 1[1]
        {'defines': (0, 'val'), 'uses': [(1, 'lexval')],
         'fn': lambda a: int(a[0])},
        {'defines': (0, 'ops'), 'uses': [], 'fn': lambda a: 0},
    ],
    9: [  # F -> 2
        {'defines': (0, 'val'), 'uses': [(1, 'lexval')],
         'fn': lambda a: int(a[0])},
        {'defines': (0, 'ops'), 'uses': [], 'fn': lambda a: 0},
    ],
    10: [ # F -> 3
        {'defines': (0, 'val'), 'uses': [(1, 'lexval')],
         'fn': lambda a: int(a[0])},
        {'defines': (0, 'ops'), 'uses': [], 'fn': lambda a: 0},
    ],
}

RULES_CIRCULAR = dict(RULES)
RULES_CIRCULAR[3] = [  # A -> e   (modified: A.val depends on itself → cycle)
    {'defines': (0, 'val'), 'uses': [(0, 'val')], 'fn': lambda a: a[0]},
    {'defines': (0, 'ops'), 'uses': [], 'fn': lambda a: 0},
]
