import pkgutil
import unittest
from FGABrejaAPI import tests

for importer, modname, ispkg in pkgutil.iter_modules(tests.__path__):
    exec('from FGABrejaAPI.tests.{} import *'.format(modname))

unittest.main()
