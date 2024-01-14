# Queens College
# Dicrete Structures CSCI 220
# Winter 2024
# Assignment 1 Logic and Truth Tables
# Mikdad Abdullah
# Collaborated With Class


import inspect
import pandas as pd
from itertools import product


# [2] Define functions for these logical operators:

# xor

def xor(p, q):
    return p != q


# impl
def impl(p, q):
    return not p or q


# bi_impl
def bi_impl(p, q):
    return impl(p, q) and impl(q, p)


# rev_impl
def rev_impl(p, q):
    return impl(q, p)


# [3]Define a function for each expression that needs to be evaluated.For example, for the Boolean expression "(p ∨ q) ∧ r", you might write:
def f0(p, q, r):
    return (p or q) and r


# [4] Define a function func_body(f) that returns the content of the function. This will be used later in the truth table.
def func_body(f):
    body = inspect.getsource(f)  # gets the code
    idx = body.index("return")  # get the part after return
    return '"' + body[7 + idx:].strip() + '"'


# [5] Define a function truth_table(f) that creates a truth table for a logical function f. Add a comment acknowledging this source: https://stackoverflow.com/questions/29548744/creating-a-truth-table-for-any-expression-in-python :

def truth_table(f):
    values = [list(x) + [f(*x)] for x in product([False, True], repeat=f.__code__.co_argcount)]
    return pd.DataFrame(values, columns=(list(f.__code__.co_varnames) + [f.__name__]))


# [6] Define a function analyze_truth_table(f) that calls the previous function to generate the truth table, including the evaluated expression, followed by your categorization of the expression as a tautology, contingency, or contradiction.

def analyze_truth_table(f, verbose=False):
    tt = truth_table(f)
    tt_rows = tt.shape[0]
    tt_cols = tt.shape[1]
    tt_vars = tt_cols - 1
    tt_type = None
    last_col = tt.iloc[:, tt_vars]
    if last_col.all():
        tt_type = "Tautology"
    elif last_col.any():
        tt_type = "Contingency"
    else:
        tt_type = "Contradiction"
    binary = "".join(["1" if last_col[i] else "0" for i in range(len(last_col))])[::-1]
    if verbose:
        print("Name:", f.__name__, func_body(f))
        print(tt)
        print("Rows:", tt_rows, "Cols:", tt_cols, "Vars:", tt_vars, "Type:", tt_type)
    return tt_rows, tt_cols, tt_vars, tt_type, last_col, binary, int(binary, 2)


# [7] Apply the analyze function to the sixteen possible functions listed at
# https://en.wikipedia.org/wiki/Truth_table#Truth_table_for_all_binary_logical_operators.
# Label them f0 thru f15, to match the order in Wikipedia.
# All sixteen should have two propositional variables p and q, even if the function uses only one or the other.
# Verify that the output matches what is expected.
def f0_false(p, q):
    return False


def f1_NOR(p, q):
    return not (p or q)


def f2_converse_nonimpl(p, q):
    return not p and q


def f3_neg_p(p, q):
    return not p


def f4_nimply(p, q):
    return p and not q


def f5_neg_q(p, q):
    return not q


def f6_xor(p, q):
    return xor(p, q)


def f7_nand(p, q):
    return not (p and q)


def f8_and(p, q):
    return p and q


def f9_xnor(p, q):
    return (p and q) or (not p and not q)


def f10_q(p, q):
    return q


def f11_imply(p, q):
    return impl(p, q)


def f12_p(p, q):
    return p


def f13_converse(p, q):
    return impl(q, p)


def f14_or(p, q):
    return p or q


def f15_T(p, q):
    return True


# [10] Define a function is_equivalent(f1, f2) that determines if two functions are logically equivalent by building the truth tables for both and comparing outputs, or by evaluating f1 ↔ f2 to be a tautology. Test that it works as expected.

def is_equivalent(f1, f2):
    # tt1 = truth_table(f1)
    # r1, c1 = tt1.shape[0], tt1.shape[1]
    # out1 = tt1.iloc[:, c1 - 1]
    # tt2 = truth_table(f2)
    # r2, c2 = tt2.shape[0], tt2.shape[1]
    # out2 = tt2.iloc[:, c2 - 1]
    result1 = analyze_truth_table(f1)
    result2 = analyze_truth_table(f2)
    return result1[0] == result2[0] and result1[1] == result2[1] and all(([result1[4][i] == result2[4][i] for i in range(result1[0])]))


def f1_test(p, q):
    return not (p and q)


def f2_test(p, q):
    return not p or not q


def f3_test(p, q):
    return not p and not q


# [8] Apply the analyze function to some logical equivalences, the two parts of De Morgan's Laws.
# Law #1: ~(p | q) ↔ (~p & ~q)
# Law #2: ~(p & q) ↔ (~p | ~q)
def dm1l(p, q):
    return not (p or q)


def dm1r(p, q):
    return not p and not q


def dm2l(p, q):
    return not (p and q)


def dm2r(p, q):
    return not p or not q


# [11] Modify the analyze_truth_table() function as follows:

# Computes the binary equivalent of the last column: e.g. TTFT → 1101
# Computes the decimal equivalent of that binary number: e.g. 1101 → 13
# Returns not only the type (tautology / contingency / contradiction) but also any other data of interest: rows, columns, variables, output column, binary equivalent, and decimal equivalent
# Define a function is_equivalent(f1, f2) that determines if two functions are logically equivalent by building the truth tables for both and comparing outputs, or by evaluating f1 ↔ f2 to be a tautology. Test that it works as expected.

# Then modify the is_equivalent() function to use the reworked code.

def main():
    results = analyze_truth_table(f0, True)
    print(results)
    print(func_body(f1_test), func_body(f2_test), is_equivalent(f1_test, f2_test))  # True
    print(func_body(f1_test), func_body(f3_test), is_equivalent(f1_test, f3_test))  # False
    print(func_body(dm1l), func_body(dm1r), is_equivalent(dm1l, dm1r))  # True
    print(func_body(dm2l), func_body(dm2r), is_equivalent(dm2l, dm2r))  # False

    functions = (f0_false, f1_NOR, f2_converse_nonimpl, f3_neg_p, f4_nimply,
                 f5_neg_q, f6_xor, f7_nand, f8_and,
                 f9_xnor, f10_q, f11_imply, f12_p, f13_converse, f14_or, f15_T)
    for func in functions:
        result = analyze_truth_table(func)
        print(func.__name__, result[5], result[6])


if __name__ == '__main__':
    main()
