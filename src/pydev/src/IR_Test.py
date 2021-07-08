from IR import *

import torch
import torch.nn as nn

from unittest import TestCase
from unittest.suite import TestSuite






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
  
  def test__xBound_StrRepr(self):
    x = xBound("S", 50)
    self.assertEqual(str(x), "{\'name\': \'S\', \'count\': 50}")


xb = xBound 
class Test_IR_CreateLinear(TestCase):
  def test__LinearLayer_Success(TestCase):
    name  = "Linear"
    title = "Linear1" #name is module name, title is name in ModuleDict

    isNative     = True #contained within pytorch?
    isParametric = True #gradient info maintained for backprop?
    hypers = {"bias": True} #other hyper parameters

    
    conn1 = InBound(xBound("S", 50)) #receives concat of two layers, S and Y
    conn2 = InBound(xBound("Y", 50))
    
    conn3 = OutBound(xb("Z", 50)) #outputs to Z 
    #Note, is useful for inbound and outbout as offers guarantee 
    #it is connected to intended target

    ModuleIntermediateRepr(name = name,
          inbound = [conn1, conn2],
          outbound = [conn3],
          isNative = isNative,
          isParametric = isParametric, 
          hypers = hypers,
          title = title)
  def test__LinearLayer_isNative_TypeError(self):
    name  = "Linear"
    title = "Linear1" #name is module name, title is name in ModuleDict

    isNative     = True #contained within pytorch?
    isParametric = True #gradient info maintained for backprop?
    hypers = {"bias": True} #other hyper parameters

    conn1 = InBound(xb("S", 50)) #receives concat of two layers, S and Y
    conn2 = InBound(xb("Y", 50))
    
    conn3 = OutBound(xb("Z", 50)) #outputs to Z 
    with self.assertRaises(TypeError) as cm:
      ModuleIntermediateRepr(name = name,
          inbound = [conn1, conn2],
          outbound = [conn3],
          isNative = 0,
          isParametric = isParametric, 
          hypers = hypers,
          title = title)
  
  def test__LinearLayer_isParametric_TypeError(self):
    name  = "Linear"
    title = "Linear1" #name is module name, title is name in ModuleDict

    isNative     = True #contained within pytorch?
    isParametric = True #gradient info maintained for backprop?
    hypers = {"bias": True} #other hyper parameters

    conn1 = InBound(xb("S", 50)) #receives concat of two layers, S and Y
    conn2 = InBound(xb("Y", 50))
    
    conn3 = OutBound(xb("Z", 50)) #outputs to Z 
    with self.assertRaises(TypeError) as cm:
      ModuleIntermediateRepr(name = name,
          inbound = [conn1, conn2],
          outbound = [conn3],
          isNative = isNative,
          isParametric = 1,
          hypers = hypers,
          title = title)
  

