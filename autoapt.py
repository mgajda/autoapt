#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess, sys
"""This module allows to run auto-apt to find missing python modules.
   It is most convenient when chained as a part of sys.excepthook.
   Try putting the following into your .pythonrc:

   >> import autoapt, sys
   >> autoapt.install_hook()
   >> del autoapt

   Then whenever you try to import a missing module, you will see something like:

   >> import pstats
Traceback (most recent call last):
  File "autoapt_import.py", line 56, in <module>
    exec cmd
  File "<string>", line 1, in <module>
ImportError: No module named pstats you may try packages: python-profiler python3-profiler
"""

__all__ = ["auto_apt", "excepthook", "install_hook"]

def auto_apt(name):
  """
  For a given import name, find a file that may provide it with `apt-file`.
  """
  proc = subprocess.Popen(["apt-file", "search", name.replace(".", "/")],
                          stdout   = subprocess.PIPE,
                          stderr   = subprocess.PIPE,
                          encoding = "ascii")
  out, err = proc.communicate()
  if err.strip() != "":
    print("auto-apt error: %s" % err, file=sys.stderr)
  results = set([])
  for line in out.split("\n"):
    if (".py" not in line) and ("python3" not in line): # false positive?
      continue
    if ":" not in line: # error in output format?
      print("Error in apt-file output: expected \\t", file=sys.stderr)
      continue # may be changed to raise exception WHEN debugging
    results.add(line.split(":")[0])
  return results

def excepthook(exctype, exc, trace):
  """
  Unhandled exception hook:
  If exception is ImportError,
  then call `auto_apt` function to discover the Apt package to install.
  """
  if exctype == ImportError:
    missing_module_string = "No module named "
    if exc.args[0].startswith(missing_module_string):
      name = exc.args[0][len(missing_module_string):]
      packages = " ".join(auto_apt(name))
    exc.args = ("For %s you may try one of the packages: %s"
                   % (exc.args[0], packages),)
  original_excepthook(exctype, exc, trace)

def install_hook():
  "Install a global hook of unhandled exceptions."
  global original_excepthook
  original_excepthook = sys.excepthook
  sys.excepthook = excepthook

install_hook()

# Debugging as a module
if __name__=="__main__":
  import optparse
  # Options
  optparser = optparse.OptionParser(usage="%prog [<options>] <module> - finds packages responsible for named modules")

  opts, args = optparser.parse_args() # Parse arguments

  # Verify arguments
  if len(args)<1:
    print(optparser.format_help(), file=sys.stderr)
    sys.exit(1)

  for name in args:
    result = auto_apt(name)
    print("%s: %s" % (name, ' '.join(auto_apt(name))))

    cmd = "import " + name
    exec(cmd)


     
