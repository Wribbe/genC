#!/usr/bin/env python3

import sys
import re

import sqlite3

str_indent=2*' '

alph = list("abcdefghijklmnopqrstuvwxyz")

type_int = "int"
type_float = "float"
type_double = "double"
type_char = "char"

def flatten(text):
  return '\n'.join([l.strip() for l in text.splitlines()])

def pointer(t):
  if t == type_char:
    t = "const {}".format(t)
  return "{} * ".format(t)

indent_level = 0
def indent(text):
  global indent_level
  lines = text.splitlines()
  out = []
  for line in lines:
    if line.endswith('}'):
      indent_level -= 1
    out.append("{}{}".format(indent_level*str_indent, line))
    if line.endswith('{'):
      indent_level += 1

  return '\n'.join(out)

functions = [
("func_a", "",                  [type_int]*3),
("func_change_me", "",          []),
("func_c", "",                  []),
("func_d", type_double,         [type_float]*2),
("func_e", "",                  []),
("func_f", "",                  [type_double, type_int, pointer(type_int)]),
("func_g", "",                  [type_double]*4),
("func_h", "",                  []),
("func_i", type_int,            []),
("func_j", "",                  []),
("func_k", pointer(type_char),  []),
("func_l", type_char,           [type_int]*4),
]

def gen_functions(functions):
  out = []
  for name, type_return, attributes in functions:
    if not attributes:
      attributes = "void"
    else:
      attributes = ', '.join(["{} {}".format(atype, char) for atype, char in
                             zip(attributes, alph)])
      attributes = re.sub(r'\s+', ' ', attributes)
    if not type_return:
      type_return = "void"

    out.append("""\
      {type_return}
      {name}({attributes})
      {{
      }}
    """.format(
      name=name,
      type_return=type_return,
      attributes=attributes,
    ))
    out.append('\n')
  if out:
    return ''.join(out)

def main(args):
  fmt_printf = 'printf("HELLO WORLD %d.\\n", {});'
  prints = '\n'.join([fmt_printf.format(i) for i in range(20)])
  code = """\
    #include <stdlib.h>
    #include <stdio.h>

    {functions}

    int
    main(void)
    {{
      {main_code}
    }}
  """.format(
    main_code=prints,
    functions=gen_functions(functions),
  )

  print(indent(flatten(code)))

if __name__ == "__main__":
  main(sys.argv[1:])
