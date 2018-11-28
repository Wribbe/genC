import re

def resolve_dirs_from_makefile():
  # Read correct lines from Makefile.
  lines_dirs = [l.strip() for l in open("Makefile").readlines() if
               l.startswith("DIR_")]

  # Split everything.
  lines_dirs = [([t.strip() for t in line.split(":=")]) for line in lines_dirs]
  dir_dict = {}

  # First pass, don't resolve variable-depending paths.
  for name, path in lines_dirs:
    if "$" not in path:
      dir_dict[name] = path

  def remove_found(lines):
    return [(name, path) for (name, path) in lines if not dir_dict.get(name)]

  # Remove all the found paths.
  lines_dirs = remove_found(lines_dirs)

  # Resolve variable-depending paths.
  max_pass = 100
  curr_pass = 1
  while lines_dirs and curr_pass < max_pass:
    modified_lines = []
    for name, path in list(lines_dirs):
      path_vars = re.findall(r'\$\(.*?\)', path)
      for var in path_vars:
        # Remove $().
        base = var[2:-1]
        # See if there is a match.
        resolved = dir_dict.get(base)
        # Replace if resolved.
        if resolved:
          path = path.replace(var, resolved)
      # Any variables left?
      if not "$" in path:
        dir_dict[name] = path
      else: # More variables to resolve.
        modified_lines.append((name, path))

    # Replace with new list.
    lines_dirs = modified_lines
    # Remove fully resolved.
    lines_dirs = remove_found(lines_dirs)
    # Keep track of number of passes.
    curr_pass += 1

  if curr_pass == max_pass:
    fmt_error = "Could not resolve all path dir-variables after {} passes!"
    print(fmt_error.format(curr_pass), file=sys.stderr)
  return dir_dict
