#!/usr/bin/env python3

import os
import re
import sys

def indent(text):
  lines = [line for line in text.splitlines() if line.strip()]
  whitespace = []

  def num_whitespaces(line):
    return len(re.findall(r'^\s+', line)[0])

  for line in lines:
    whitespace.append(num_whitespaces(line))

  n_min = min(whitespace)
  whitespace = [n-n_min for n in whitespace]

  lines = ["{}{}".format(' '*n,line.strip()) for (n,line) in zip(whitespace, lines)]
  print(whitespace)
  return '\n'.join(lines)


def main(args):
  fname = args[-1]

  src = """\
  #!/usr/bin/env python3

  def main():

    def print_me(sender):
      print("HELLO from {}".format(sender))

    print_me(__file__)

  if __name__ == "__main__":
    main()
  """

  with open(fname, 'w') as handle_f:
    handle_f.write(indent(src))
    handle_f.write(os.linesep)

if __name__ == "__main__":
  main(sys.argv[1:])
