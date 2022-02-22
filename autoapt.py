#!/usr/bin/python
# -*- coding: utf-8 -*-

import __builtin__, subprocess, sys
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
  #print "name", repr(name)
  proc = subprocess.Popen(["apt-file", "search", name.replace(".", "/")],
                          stdout = subprocess.PIPE,
                          stderr = subprocess.PIPE)
  out, err = proc.communicate()
  if err.strip() != "":
    print >>sys.stderr, "auto-apt error:", err
  results = set([])
  for line in out.split("\n"):
    #print repr(line)
    if (".py" not in line) and ("python3" not in line): # false positive?
      continue
    if "\t" not in line: # error in output format?
      continue # may be changed to raise exception WHEN debugging
    results.add(line[line.index("\t"):].split("/")[-1])
  return results

original_excepthook = sys.excepthook
def excepthook(exctype, exc, trace):
  if exctype == ImportError:
    missing_module_string = "No module named "
    if exc.args[0].startswith(missing_module_string):
      name = exc.args[0][len(missing_module_string):]
      packages = " ".join(auto_apt(name))
    exc.args = ("%s you may try packages: %s" % (exc.args[0], packages),)
  original_excepthook(exctype, exc, trace)

def install_hook():
  global original_excepthook
  original_excepthook = sys.excepthook
  sys.excepthook = excepthook

if __name__=="__main__":
  import optparse
  # Options
  optparser = optparse.OptionParser(usage="%prog [<options>] <module> - finds packages responsible for named modules")
  
  opts, args = optparser.parse_args() # Parse arguments
  
  # Verify arguments
  if len(args)<1:
    print >> sys.stderr, optparser.format_help()
    sys.exit(1)
 
  install_hook() 
  for name in args:
    print name, ":", ' '.join(auto_apt(name))

    cmd = "import %s" % name
    #print "cmd", repr(cmd)
    exec cmd


     
