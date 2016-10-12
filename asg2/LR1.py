#####
###
# Author: Matt Price
# Ilstu ID: 830083370
# Copyright: Matt Price
#
# HOWTO: 
# You can run the program using the command line by typing `python /path/to/LL2.py -e "100-((2*(5-3))-2)+3"`.
###
#####

import argparse
import csv
import re

# Load a parsing table from a .csv file. Defaults to "table.csv"
def load_parsing_table(table_file='table.csv'):
  table = {}
  with open(table_file, 'rU') as csvfile:
    reader = csv.reader(csvfile, delimiter = ',')
    for row in reader:
      n = row[0]
      if n not in table:
        # initialize new state
        table[n] = {}

      for symbol in row[1].split():
        if symbol not in table[n]:
          # new action
          table[n][symbol] = {}

        if row[2] == 's':
          # Shift
          table[n][symbol]['shift'] = row[3]
        elif row[2] == 'a':
          # Accept
          table[n][symbol]['accept'] = True
        else:
          # Reduce
          if 'reduce' not in table[n][symbol]:
            # "reduce" data structure is a list of possible reductions
            table[n][symbol]['reduce'] = []

          items = row[3].split(':')
          reduction = { items[0]: items[1].split() }
          table[n][symbol]['reduce'].append(reduction)

  return table

# Print the current stack along with the remaining tokens
def print_status(stack, tokens):
  s = ''
  for item in stack:
    s += '[{}:{}] '.format(item[0], item[1])
  s += '     '
  for item in tokens:
    s += '{} '.format(item)
  print s

# The main logic
def valid_expression(tokens, table):

  stack = []
  stack.append(('-', '0'))
  while stack and tokens:
    print_status(stack, tokens)
    top_i = len(stack) - 1
    curr_state = stack[top_i][1]
    curr_token = tokens.pop(0)

    if curr_token not in table[curr_state]:
      # Rule for token doesn't exist at current state
      return False

    # Shift
    if 'shift' in table[curr_state][curr_token]:
      
      stack.append((curr_token, table[curr_state][curr_token]['shift']))
      continue

    # Reduce
    elif 'reduce' in table[curr_state][curr_token]:

      # push token back into tokens queue since we're reducing
      tokens = [curr_token] + tokens

      valid_red = False
      # Can be multiple reduction rules
      for red_rule in table[curr_state][curr_token]['reduce']:
        rule_items = red_rule.values()[0]

        if len(stack) >= len(rule_items) and rule_items == [st[0] for st in stack[len(stack)-len(rule_items):]]:
          # Reduction rule matched 
          valid_red = True
          for i in range(len(rule_items)):
            stack.pop()
          # Pop all reduction rule items and push new rule to tokens queue since it's logically processed the same as other actions
          tokens = [red_rule.keys()[0]] + tokens
          break

      if not valid_red:
        # Invalid reduction attempt
        return False

    # Accept 
    else:
      return True
  
  # Make sure there isn't extra stuff remaining
  if len(stack) == 2 and stack[1] == ('E', 1):
    return True
  else:
    return False

# Main function
if __name__ == '__main__':

  # Get expression from user via CLI
  parser = argparse.ArgumentParser(description='Arguments for the program')
  parser.add_argument('-e', required=True, help='The expression to parse')
  parser.add_argument('-f', help='Optional - the file to load a parsing table from.')
  args = parser.parse_args()

  expression = args.e

  # Separate user input into numbers and symbols
  match = re.findall('\d+|\D+', expression)
  tokens = []
  # Convert all numbers to string 'n'
  for item in match:
    if item.isdigit():
      tokens.append('n')
    else:
      tokens.extend(list(item))

  # Load the parsing table
  if args.f:
    # user specified a specific file for a table
    table = load_parsing_table(args.f)
  else:
    table = load_parsing_table()

  if tokens and tokens[len(tokens)-1] != '$':
    tokens.append('$')

  if valid_expression(tokens, table):
    print 'Yes'
  else:
    print 'No'
