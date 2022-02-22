DESCRIPTION:
============

This module allows to run auto-apt to find missing python modules.
It is most convenient when chained as a part of `sys.excepthook`.

It requires that you install `apt-file`:

```
apt-get install -y apt-file
```

USAGE:
======

Try putting the following into your .pythonrc:

```
import autoapt, sys
autoapt.install_hook()
del autoapt
```
Then whenever you try to import a missing module, you will see something like:

```
   >> import shortuuidfield

      Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
      ModuleNotFoundError: To get missing module 'shortuuidfield' you may try among packages: python3-django-shortuuidfield
```

LICENSE:
========
BSD3

AUTHOR:
=======
Michał J. Gajda
