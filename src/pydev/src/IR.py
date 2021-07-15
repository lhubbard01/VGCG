import re

from typing import List, NewType

def isValid(name: str):
  """checks the validity of a name as a candidate for pythonic symbol table"""
  if not (name[0].isalpha() or name[0] == "_"):
    return False
  elif re.match(r"\s", name):
    return False

  elif re.match(r"\D\W", name):
    return False

  elif name in ["in", "return", "self", "for", "zip", "import"]:
    return False
  
  return True







class xBound:
  """renders readable the connection information, hopefully. 
  Ensures strictly positive integer params, python viable names."""
  

  def __init__(self, name: str, count: int):

    if not isValid(name):
      raise ValueError(f"name MUST be python-valid. received {name}")
    self.name = name
    if not isinstance(count, int):
      raise TypeError
    if count <= 0:
      raise ValueError("count must be a positive integer, representing the output vector dimension")

    self.count = count

  
  def __repr__(self):
    return str({"name": self.name, "count": self.count})


  def __str__(self):
    return str(self.__repr__())

def seek(target: str, mp: dict):
  for key in mp:
    if target in key:
      return key, mp[key]
#InBound  = xBound
#print(type(InBound))
#OutBound = xBound
InBound = NewType("InBound", xBound)
OutBound = NewType("OutBound", xBound)
#print(InBound == OutBound)
x = xBound
class ModuleIntermediateRepr:
  """Contains information describing a module """
  def __init__(self, name: str, inbound: List[InBound], outbound: List[OutBound], isNative: bool, isParametric: bool, hypers: dict, mType: str):
    if not isinstance(isNative, bool):
      raise TypeError
    self.isNative = isNative
    if not isinstance(isParametric, bool):
      raise TypeError
    self.isParametric = isParametric
    self.name = name
    self.mType = mType
    # these are mappings of {name:name, count:count}
    self.inbound = inbound
    self.outbound = outbound
    self.hypers = hypers
  

  def from_msg(self, msg): 
    self.msg = None
    exec("self.msg = " + msg)
    return self.msg

  def build(self):
    module_builder_string = ""

    if self.isNative:
      module_builder_string += "nn." + self.mType + "("
    
    if self.isParametric:
      in_kv_pair = seek("in_", self.hypers)
      module_builder_string += str(in_kv_pair[0]) + " = " + str(in_kv_pair[1]) + ", "
      print(module_builder_string)
      out_kv_pair = seek("out_", self.hypers)
      module_builder_string += str(out_kv_pair[0]) + " = " + str(out_kv_pair[1]) + ", "
      print(module_builder_string)

    for hparam in self.hypers.keys():
      if "out_" not in hparam and "in_" not in hparam:
        module_builder_string += hparam + " = " + str(self.hypers[hparam]) + ", "

    module_builder_string = module_builder_string[:-2] + ")"

    return module_builder_string
    #exec("obj = " + module_builder_string, globals(), locals())
    #return obj

  



