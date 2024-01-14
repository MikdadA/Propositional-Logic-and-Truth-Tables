Introduction:

In this assignment, we will write a Python program that
generates the "truth table" for a set of Boolean variables (i.e. all possible assignments of T/F to those variables)
for each row of the truth table, evaluates the same Boolean expression implemented as a function
determines whether the expression is a tautology (always true), contradiction (always false), or contingency (truth depends on the assignment of TRUE/FALSE to the variables)
determines whether two expressions E1 E2 are logically equivalent by checking whether E1 ↔ E2 is a tautology.    

Submissions:

In the Google form, please submit:

Assignment1.py (your program)
Assignment1.txt (console output showing the truth-tables and summary information for functions f0 - f18)

Standard Preliminary Tasks:

[1] Install the Python language and interpreter and the PyCharm integrated development environment (IDE) and get the sample "Hello User" program running  as  outlined in "Assignment #0: Installing Python and PyCharm".  

[2] Add a comment at the top. (This will also be a template for commenting future assignments) 

[3] Define a function main() which will be the springboard for the execution of all other code in this assignment. 

def main():
    pass # placeholder until actual function content is provided

[4] Add these lines just below the main() function to ensure that importing of this module into another program will not automatically run it. 

if __name__ == "__main__": 
    main()

[5] Create a program configuration. Note: one will automatically be created if you run via the Run menu item.


Assignment-Specific Tasks:

[1] Near the beginning of the program, write the following line to give us access to some important Python packages

import inspect
import pandas as pd
from itertools import product

[2] Define functions for these logical operators:

xor 
impl
bi_impl
rev_impl
  
[3] Define a function for each expression that needs to be evaluated. For example, for the Boolean expression "(p ∨ q) ∧ r", you might write:

def f(p, q, r):
    return (p or q) and r

[4] Define a function func_body(f) that returns the content of the function. This will be used later in the truth table. 

def func_body(f):
    body = inspect.getsource(f)  # gets the code
    idx = body.index("return")  # get the part after return
    return '"' + body[7+idx:].strip() + '"'

[5] Define a function truth_table(f) that creates a truth table for a logical function f. Add a comment acknowledging this source: https://stackoverflow.com/questions/29548744/creating-a-truth-table-for-any-expression-in-python :

def truth_table(f):
    values = [list(x) + [f(*x)] for x in product([False,True], repeat=f.__code__.co_argcount)]
    return pd.DataFrame(values,columns=(list(f.__code__.co_varnames) + [f.__name__]))

Note: the method for accessing function attributes such as its name, code, parameter count, and parameter names, has changed from Python 2 to Python 3. We have modified the Stackoverflow code  accordingly.

[6] Define a function analyze_truth_table(f) that calls the previous function to generate the truth table, including the evaluated expression, followed by your categorization of the expression as a tautology, contingency, or contradiction.

def analyze_truth_table(f):
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
   print("Name:", f.__name__, func_body(f))
   print(tt)
   print("Rows:", tt_rows, "Cols:", tt_cols, "Vars:", tt_vars, "Type:", tt_type)

[7] Apply the analyze function to the sixteen possible functions listed at
https://en.wikipedia.org/wiki/Truth_table#Truth_table_for_all_binary_logical_operators. Label them f0 thru f15, to match the order in Wikipedia. All sixteen should have two propositional variables p and q, even if the function uses only one or the other. Verify that the output matches what is expected.

[8] Apply the analyze function to some logical equivalences, the two parts of De Morgan's Laws.  
Law #1: ~(p | q) ↔ (~p & ~q) 
Law #2: ~(p & q) ↔ (~p | ~q) 

[9] Create functions and truth tables for three rules of inference: Modus Ponens, Modus Tollen, Hypothetical Syllogism.  

Modus Ponens: ((p → q) & p) → q 
Modus Tollens: ((p → q) & ~q) → ~p 
Hypothetical Syllogism:  ((p → q) & (q → r)) → (p → r)

[10] Define a function is_equivalent(f1, f2) that determines if two functions are logically equivalent by building the truth tables for both and comparing outputs, or by evaluating f1 ↔ f2 to be a tautology. Test that it works as expected.  

def is_equivalent(f1, f2):
    tt1 = truth_table(f1)
    r1, c1 = tt1.shape[0], tt1.shape[1]
    out1 = tt1.iloc[:, c1 - 1]
    tt2 = truth_table(f2)
    r2, c2 = tt2.shape[0], tt2.shape[1]
    out2 = tt2.iloc[:, c2 - 1]
    return r1 == r2 and c1 == c2 and all([out1[i] == out2[i] for i in range(r1)])


def f1_test(p, q): return not(p and q)


def f2_test(p, q): return not p or not q


def f3_test(p, q): return not p and not q


# place inside your main()
print(func_body(f1_test), func_body(f2_test), is_equivalent(f1_test, f2_test)) # True
print(func_body(f1_test), func_body(f3_test), is_equivalent(f1_test, f3_test)) # False

[11] Modify the analyze_truth_table() function as follows:

Computes the binary equivalent of the last column: e.g. TTFT → 1101
Computes the decimal equivalent of that binary number: e.g. 1101 → 13
Returns not only the type (tautology / contingency / contradiction) but also any other data of interest: rows, columns, variables, output column, binary equivalent, and decimal equivalent
Define a function is_equivalent(f1, f2) that determines if two functions are logically equivalent by building the truth tables for both and comparing outputs, or by evaluating f1 ↔ f2 to be a tautology. Test that it works as expected.  

Then modify the is_equivalent() function to use the reworked code. 


References:

https://www.geeksforgeeks.org/python-logical-operators-with-examples-improvement-needed/ 
https://docs.python.org/3/library/stdtypes.html#index-16 
https://docs.sympy.org/latest/modules/logic.html 
https://stackoverflow.com/questions/432842/how-do-you-get-the-logical-xor-of-two-variables-in-python 
https://stackoverflow.com/questions/16405892/is-there-an-implication-logical-operator-in-python 

You should always acknowledge, in a comment either at the top of your code or just before the borrowed function, any websites that you used, both as a form of attribution and also to build an inventory of helpful resources for implementing Discrete Structures in Python.  

Optional Examples for Additional Testing:

p & ~p
p | ~p
~p & (p → q)
(p → q) | (q → p)
(p | q) | (~p & ~q)
(p | q) & (~p & ~q)
(p → q) & (q → r)

More testing examples at the bottom of https://sites.millersville.edu/bikenaga/math-proof/truth-tables/truth-tables.html 


