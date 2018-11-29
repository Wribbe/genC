#!/usr/bin/env python3

import click

@click.command()
@click.argument("file")
@click.argument("shebang")
def cli_main(file, shebang):
  lines = open(file).readlines()
  lines[0] = shebang
  print('\n'.join(lines))

if __name__ == "__main__":
  cli_main()
