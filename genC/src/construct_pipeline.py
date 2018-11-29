#!/usr/bin/env python3

import os
import re
import sys

import click
import utils

def num_whitespaces(line):
  num = 0
  for c in line:
    if re.match(r'\s', c):
      num += 1
    else:
      break
  return num


def baseline_indent(text, strip_blank=False):

  # Remove inline comments.
  lines = [line.split('#',1)[0] if '#' in line else line for line in
           text.splitlines()]

  if strip_blank:
    lines = [line for line in lines if line.strip()]
  else:
    lines = [line for line in lines]

  whitespace = []

  for line in lines:
    whitespace.append(num_whitespaces(line))

  n_min = min(whitespace)
  whitespace = [n-n_min for n in whitespace]

  lines = ["{}{}".format(' '*n,line.strip()) for (n,line) in zip(whitespace, lines)]
  return os.linesep.join(lines)


def parse_defines(list_defines):
  list_defines = [(toks) for toks in [l.split(':',1) for l in list_defines]]
  out = ["", ""]
  fmt = """\
    class {class_name}():
      args = types.SimpleNamespace()
      def __init__(self, {argument_names}):
        {{argument_assignments}}
  """
  fmt = baseline_indent(fmt, strip_blank=True)
  for name_def, args in list_defines:

    # Get argument names.
    argnames = [v.split('=')[0] for v in args.split(',')]
    # Flatten any nestings.
    argnames = utils.flatten_nesting(','.join(argnames))

    # Construct argument assignments.
    argument_assignments = []
    for arg_name in argnames.split(','):
      argument_assignments.append("self.args.{} = {}".format(arg_name, 0))

    # Fill in class format and append to output.
    out.append(fmt.format(
      class_name = name_def,
      argument_names = argnames,
    ))
    # Figure out correct indentation and add to the arguments.
    indent = num_whitespaces(out[-1].splitlines()[-1])
    first_assignment = argument_assignments.pop(0)
    argument_assignments = ["{}{}".format(' '*indent,arg) for arg
                            in argument_assignments]
    argument_assignments.insert(0,first_assignment)
    # Add arguments to template.
    out[-1] = out[-1].format(
      argument_assignments = os.linesep.join(argument_assignments)
    )
    # Separate each class with 2*linesep.
    out.append("")
    out.append("")

  out.append("")

  return baseline_indent(os.linesep.join(out))


def parse_pipefile(pipefile):
  lines = [l for l in open(pipefile).readlines() if not l.strip() or
           not l.startswith("#")]

  lines = baseline_indent('\n'.join(lines), strip_blank=True).splitlines()

  pipelines = []
  defines = []

  indent_current = 0
  indent_current_define = 0
  define_stack = []

  def flush_define_stack():
    definition = re.sub(r'\s+', ' ', ''.join(define_stack))
    if definition.endswith(','):
      definition = definition[:-1]
    defines.append(definition)
    return (0, [])

  for line in lines:
    indent_current = num_whitespaces(line)

    # Handle continuation of indented define statements.
    if indent_current_define > 0:
      if indent_current < indent_current_define:
        indent_current_define, define_stack = flush_define_stack()
      else:
        define_stack.append(line)

    # Handle non-indented lines.
    if line.startswith("define"):
      indent_current_define = num_whitespaces(line)+2
      define_stack.append(line)
    elif '->' in line:
      pipelines.append(line)

  if define_stack:
    flush_define_stack()

  # Remove any spaces in defines after ':'.
  defines = ["{}:{}".format(d.replace("define",'').strip(),args.replace(' ',''))
             for (d,args) in [definition.split(':',1) for definition in defines]]

  # Parse defines into classes.
  defines = parse_defines(defines)

  src = """\
    {definitions}

    #{pipelines}
  """
  src = baseline_indent(src, strip_blank=True)

  return baseline_indent(src.format(definitions=defines, pipelines=pipelines))

def main(pipefile, out):


  src = """\
  #!/usr/bin/env python3

  import types

  {data_section}

  def main():

    def print_me(sender):
      print("HELLO from {{}}".format(sender))

    print_me(__file__)
    print("pipesource: \\n{{}}".format(open("{}").read()))

  if __name__ == "__main__":
    main()
  """

  data_section = parse_pipefile(pipefile)
  src = baseline_indent(src, strip_blank=True)
  src = src.format(pipefile, data_section=data_section)

  with open(out, 'w') as handle_f:
    handle_f.write(baseline_indent(src))
    handle_f.write(os.linesep)

@click.command()
@click.argument("pipefile")
@click.option('-out', '-o', help='Set output path of pipeline executable.')
def cli_main(pipefile, out):
  main(pipefile, out)

if __name__ == "__main__":
  cli_main()
