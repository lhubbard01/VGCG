from IR import *

import torch
import torch.nn as nn

import unittest

#from unittest import TestCase
#from unittest.suite import TestSuite
"""
def before
def after"""





















class Test_xBound(unittest.TestCase):
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
  
  #self.assertEqual( cm.exception, 
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


if __name__ == "__main__":
  unittest.main()

