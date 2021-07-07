import re

from typing import List

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
    
    if count <= 0:
      raise ValueError("count must be a positive integer, representing the output vector dimension")

    self.count = count


  
  def __repr__(self):
    return str({"name": self.name, "count": self.count})


  def __str__(self):
    return str(self)


class ModuleIntermediateRepr:
  """Contains information describing a module """
  def __init__(self, name, inbound: List[xBound], outbound: List[xBound], isNative: bool, isParametric: bool, hypers: dict, title: str = None):
    self.isNative = isNative
    self.isParametric = isParametric
    self.name = name
    self.title = (title if title else name)
    # these are mappings of {name:name, count:count}
    self.inbound = inbound
    self.outbound = outbound
    self.hyperparameters = hypers



  



