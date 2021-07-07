from IR import *

import torch
import torch.nn as nn

from unittest import TestCase
from unittest.suite import TestSuite
"""
def before
def after"""





class Test_xBound(TestCase):
  def test__xBound_success(self):
    x = xBound("S", 50)
    self.assertEqual(x.name, "S")
    self.assertEqual(x.count, 50)
  
  def test__xBound_NameField_ValueError(self):
    with self.assertRaises(ValueError) as cm:
      x = xBound("3_py", 50)

  def test__xBound_CountField_ValueError(self):
    with self.assertRaises(ValueError) as cm:
      x = xBound("py_3", 0)
    with self.assertRaises(ValueError) as cm:
      x = xBound("py_3", -65)
  
  def test__xBound_CountField_TypeError(self):
    with self.assertRaises(TypeError) as cm:
      x = xBound("py_3", "6")
    with self.assertRaises(TypeError) as cm:
      x = xBound("py_3", -65.5)
  
  def test_xBound_StrRepr(self):
    x = xBound("S", 50)
    self.assertEqual(str(x), "{\'name\': \'S\', \'count\': 50}")
"""class LinearLayer_Success(TestCase):
class LinearLayer_isNative_ValueError(TestCase)
with self.assertRaises(ValueError) as ve:
  x
self.assertEqual( cm.exception, 
class LinearLayer_isParametric_ValueError(TestCase)
with self.assertRaises(ValueError) as ve:
  x
self.assertEqual( cm.exception, 
class LinearLayer_xBound_FailGracefully(TestCase)
with self.assertRaises(ValueError) as ve:
  x
self.assertEqual( cm.exception, 
class IntermediateRepresentation__TestSuite(TestSuite)
"""


"""if __name__ == "__main__":
  unittest.main()"""

