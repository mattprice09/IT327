#####
###
# Author: Matt Price
# Ilstu ID: 830083370
# Copyright: Matt Price
#
# HOWTO: 
# You can run the program using the command line by typing `python /path/to/LL1.py -e "100-((2*(5-3))-2)+3"`.
###
#####

import argparse
import re

# Get expression from user via CLI
parser = argparse.ArgumentParser(description='Arguments for the program')
parser.add_argument('-e', required=True, help='The expression to parse')
args = parser.parse_args()

expression = args.e

# Hard-coded functions that return all rule options for a non-terminal symbol.
def E():
  return [ [T, Ep] ]

def Ep():
  return [ ['+', T, Ep],
           ['-', T, Ep],
           ['lambda'] ]

def T():
  return [ [F, Tp] ]

def Tp():
  return [ ['*', F, Tp],
           ['/', F, Tp],
           ['lambda'] ]

def F():
  return [ ['(', E, ')'],
           ['n'] ]

# Recursively find first sets for rules
def first_set(rule):
  # Base case
  if not callable(rule):
    return [rule]

  first_items = []
  for r in rule():
    first_items.extend(first_set(r[0]))
  return first_items

# Replace rule with its definition (e.g. "E -> (E)")
def get_rule_replacement(rule_class, target):
  for rule in rule_class():
    if (not callable(rule[0]) and target == rule[0]) or target in first_set(rule[0]):
      return rule

# The main logic
def valid_expression(tokens):
  # Dictionary to help keep track of rule ordering
  rules = {
    'E': {'rule': E, 'num': 1},
    'Ep': {'rule': Ep, 'num': 2},
    'T': {'rule': T, 'num': 3},
    'Tp': {'rule': Tp, 'num': 4},
    'F': {'rule': F, 'num': 5}
  }
  sorted_keys = sorted(rules.keys(), key=lambda x: (rules[x]['num']))

  # Keep track of remaining expression tokens
  input_stack = tokens

  # Use a stack with top of stack as last list element
  stack = list(reversed(rules[sorted_keys[0]]['rule']()[0]))
  done = ''
  while len(stack) > 0 and len(input_stack) > 0:
    curr = stack.pop()

    if not callable(curr):
      if curr == input_stack[0]:
        # Found terminal symbol match
        input_stack.pop(0)
      else:
        # Invalid expression (unexpected terminal symbol)
        return False
    else:
      # Replace/remove non-terminal symbol
      replacement = get_rule_replacement(curr, input_stack[0])
      if replacement:
        stack.extend(reversed(replacement))

  # Unparsed terminal symbols remaining
  if len(input_stack) > 0:
    return False

  # Check for unexpected non-terminal symbols remaining
  if len(stack) > 0:
    for rule in stack:
      if 'lambda' not in first_set(rule):
        return False
  return True

# Separate user input into numbers and symbols
match = re.findall('\d+|\D+', expression)
tokens = []
# Convert all numbers to string 'n'
for item in match:
  if item.isdigit():
    tokens.append('n')
  else:
    tokens.extend(list(item))

# Main function
if __name__ == '__main__':

  if valid_expression(tokens):
    print 'Yes'
  else:
    print 'No'
