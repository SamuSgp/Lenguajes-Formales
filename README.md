# LL(1) and SLR(1) Parser with SDD Evaluator

Final project for Formal Languages — Universidad EAFIT, 2026-2.
Professor: Oscar Rodríguez Cifuentes.

## Group Members

- Samuel González Pérez — sgonzalep3@eafit.edu.co
- Samuel López Bonilla — slopezb8q@eafit.edu.co

## Environment

  Component            Version          

 Operating System       windows 10/11    
 Programming Language   Python 3.10+   
 Additional tools        Standard library only (no external packages) |

The project uses only Python's standard library. No installation of third-party packages is required.

## Project Structure

```
├── grammar.py          # CFG representation and input parsing (Section 2.2)
├── first_follow.py     # FIRST and FOLLOW set computation (Section 4.4.2)
├── ll1_parser.py       # LL(1) table construction and predictive parser (Sections 4.4.3–4.4.4)
├── slr1_parser.py      # LR(0) items, canonical collection, SLR(1) tables and parser (Sections 4.6.2–4.6.4)
├── main.py             # Entry point for Items 1 and 2
├── sdd_definition.py   # SDD grammar and semantic rules as data (Sections 5.1–5.2)
├── sdd_evaluator.py    # Generic SDD evaluator: parse tree, dependency graph, topological sort
├── sdd_main.py         # Entry point for Item 3
├── report.pdf          # PDF report
└── README.md           # This file
```

## How to Run

### Items 1 and 2 — FIRST/FOLLOW and Parsers

```bash
python main.py
```

The program reads a context-free grammar from standard input in the format specified in Section 2.2 of the project document:

```
<number of nonterminals>
<nonterminal> -> <alt1> <alt2> ...
...
```

Symbols are single characters. Epsilon is represented as `e`. The start symbol is always `S`. Alternatives of a production are separated by spaces.

The program first prints the FIRST and FOLLOW sets (with the `--sets` flag), then classifies the grammar as `LL(1)`, `SLR(1)`, `both`, or `neither`. It then reads strings one per line (empty line to stop) and prints `yes` or `no` for each.

**Example** (grammar from Example 2 in the project document):

```
3
S -> AB
A -> aA d
B -> bBc e
```

To also display FIRST and FOLLOW sets:

```bash
python main.py --sets
```

### Item 3 — SDD Evaluator

```bash
python sdd_main.py
```

This evaluates a syntax-directed definition for a mini-calculator language with assignments and arithmetic expressions. The grammar is:

```
S -> x=E       E -> TA       A -> +TA | ε
T -> FM        M -> *FM | ε  F -> (E) | 1 | 2 | 3
```

Each input string is of the form `x=<expr>` where `<expr>` uses digits 1, 2, 3 with operators `+`, `*` and parentheses. For each valid string, the program prints:

1. The annotated parse tree with all attribute values
2. The evaluation order (topological sort of the dependency graph)
3. The computed value and the number of arithmetic operations

**Example input:**

```
x=2*3+1
x=(1+2)*3
1+2
```

**Circular SDD detection:**

```bash
python sdd_main.py --circular
```

This temporarily modifies one semantic rule to introduce a circular dependency and demonstrates the detection.

## Generative AI Disclosure

We used **Claude** (Anthropic) to help clarify textbook concepts, review code for bugs, and format parts of the LaTeX report. All algorithms were implemented following the book and we can explain every part of the code.

## References

Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D. (2007). *Compilers: Principles, Techniques, and Tools* (2nd ed.). Pearson.
