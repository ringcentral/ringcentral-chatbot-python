"""
common props, function
"""

import sys, os

isProduction = False
try:
  isProduction = os.environ['ENV'] == 'production'
except:
  isProduction = False

tables = ('bot', 'user')

def debug(*argv):
  if isProduction:
    return
  print(argv)