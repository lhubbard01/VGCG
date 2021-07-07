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

InBound  = xBound
OutBound = xBound

class ModuleIntermediateRepr:
  """Contains information describing a module """
  def __init__(self, name: str, inbound: List[InBound], outbound: List[OutBound], isNative: bool, isParametric: bool, hypers: dict, title: str = None):
    if not isinstance(isNative, bool):
      raise TypeError
    self.isNative = isNative
    if not isinstance(isParametric, bool):
      raise TypeError
    self.isParametric = isParametric
    self.name = name
    self.title = (title if title else name)
    # these are mappings of {name:name, count:count}
    self.inbound = inbound
    self.outbound = outbound
    self.hyperparameters = hypers



  



