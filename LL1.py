import argparse
import re

# Get expression from user via CLI
parser = argparse.ArgumentParser(description='Arguments for the program')
parser.add_argument('-e', required=True, help='The expression to parse')
args = parser.parse_args()

expression = args.e

# Rules
def E():
  return ('E', [[T, Ep]])

def Ep():
  return ('Ep', [['+', T, Ep], ['-', T, Ep], ['lambda']])

def T():
  return ('T', [[F, Tp]])

def Tp():
  return ('Tp', [['*', F, Tp], ['/', F, Tp], ['lambda']])

def F():
  return ('F', [['(', E, ')'], ['n']])

def first_set(rule):
  if not callable(rule):
    return [rule]

  first_items = []
  for r in rule()[1]:
    first_items.extend(first_set(r[0]))
  return first_items

def generate_follow_sets(rules):
  follow_sets = {}
  # Initialize the first rule with '$'
  for rule in rules:
    if rules[rule]['num'] == 1:
      follow_sets[rule] = ['$']
    else:
      follow_sets[rule] = []

  # Add all items caused by first sets
  for rule in rules:
    for rule_def in rules[rule]['rule']()[1]:
      i = 1
      while i < len(rule_def):
        # Search all rules for items that follow non-terminal symbols
        if callable(rule_def[i-1]):
          if not callable(rule_def[i]):
            # Terminal symbol follows non-terminal symbol
            follow_sets[rule_def[i-1]()[0]].append(rule_def[i])
          else:
            # Non-terminal symbol follows non-terminal symbol
            follow_sets[rule_def[i-1]()[0]].extend(first_set(rule_def[i]))
        i += 1
  # Remove duplicates
  for item in follow_sets:
    follow_sets[item] = [ele for ele in list(set(follow_sets[item])) if ele != 'lambda']

  changing = True
  sorted_keys = sorted(rules.keys(), key=lambda x: (rules[x]['num']))
  while changing:
    changing = False
    # Cascade the rules downwards as long as they continue to change
    for i in range(len(sorted_keys) - 1):
      r = sorted_keys[i]
      # Cascade with every other odd rule
      if rules[r]['num'] % 2 == 1:
        for ind in [i+1, i+2]:
          # Copy follow set items to next nodes
          if ind < len(sorted_keys):
            prev = len(follow_sets[sorted_keys[ind]])
            follow_sets[sorted_keys[ind]].extend(follow_sets[r])
            follow_sets[sorted_keys[ind]] = list(set(follow_sets[sorted_keys[ind]]))
            if prev < len(follow_sets[sorted_keys[ind]]):
              changing = True

  return follow_sets

def find_first(rule_items, target):
  print rule_items
  rule_forms = rule_items[0]()[1]

  for item in rule_forms:
    if item[0] == target:
      return item + rule_items[1:]
  for item in rule_forms:
    if callable(item[0]) and target in first_set(item[0]):
      found = find_first(item, target)
      if found:
        return found + rule_items[1:]

  return found

def print_stack(stack):
  items = []
  for item in reversed(stack):
    if callable(item):
      items.append(item()[0])
    else:
      items.append(item)
  print ', '.join(items)

def valid_expression(tokens):
  rules = {
    'E': {'rule': E, 'num': 1},
    'Ep': {'rule': Ep, 'num': 2},
    'T': {'rule': T, 'num': 3},
    'Tp': {'rule': Tp, 'num': 4},
    'F': {'rule': F, 'num': 5}
  }
  sorted_keys = sorted(rules.keys(), key=lambda x: (rules[x]['num']))

  follow_sets = generate_follow_sets(rules)
  for s in follow_sets:
    print s
    print follow_sets[s]

  input_stack = tokens
  stack = list(reversed(rules[sorted_keys[0]]['rule']()[1][0]))
  done = ''
  
  while len(stack) > 0:
    curr = stack.pop()
    print curr
    print input_stack[0]
    # Check for terminal symbol
    if not callable(curr):
      if curr == input_stack[0]:
        # Found terminal symbol match
        done += str(input_stack.pop(0))
      else:
        # Invalid expression (+ != *)
        print 'FAILED'
        print 'Current:'
        print curr
        print 'Target:'
        print input_stack[0]
        return False
    else:
      # Dealing with a non-terminal symbol
      if input_stack[0] in first_set(curr):
        found_items = input_stack[0]
        if not curr()[1][0][0] == input_stack[0]:
          found_items = find_first(curr()[1][0], input_stack[0])
        for item in reversed(found_items):
          stack.append(item)
      # elif input_stack[0] in follow_sets[curr()[0]]:
      #   stack.pop()

    print 'COMPLETED: {}'.format(done)
    print 'Stack:'
    print_stack(stack)
    raw_input()



# Separate user input into numbers and symbols
match = re.findall('\d+|\D+', expression)
tokens = []
# Convert all numbers to an 'n' string
for item in match:
  if item.isdigit():
    tokens.append('n')
  else:
    tokens.extend(list(item))

print tokens
print '\n'
valid_expression(tokens)
