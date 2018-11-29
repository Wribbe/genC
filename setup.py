from distutils.core import setup
name = "genC"
setup(
  name=name,
  version=open("__VERSION__").read(),
  py_modules=[name],
)
