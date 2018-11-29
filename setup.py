from distutils.core import setup
name = "genC"
setup(
  name=name,
  version=open("__VERSION__").read(),
  packages=[name, "{}.utils".format(name)],
)
