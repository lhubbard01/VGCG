import os
def seek_mods(candidates):
  to_find = {k: v for zip(candidates, [False for i in range(len(candidates))])}

  for pth in sys.path:
    for walkable in os.walk(pth):
      located_modules = [candidate for candidate in candidates if candidate in walkable[1]]
      for located in located_modules:
        to_find[located] = {"path" : os.path.abspath("."), "modules": {}} 
        
        to_find[located]
        candidates.pop(located)
import sys
sys.path.

class ModuleCallbackGen:
  def __init__(self, name: str, module_path : str = None):
    self.name = name
    self.path = (module_path if module_path else "")
  def write_cb(self, indent: int = 4):
  signature = "function " + self.name + "(ev) " 
  body_datadef = "{\n" \
  " " * indent + "let data = {\n"\
  + 2 * indent *" " + "isParametric: " + moduleX._params.weight + "\n" + indent * " " * 2 + "mType: " + str(self.mType) + ", Name:  " + self.Name + "};\n"
  body_senddef  = "send(data, \"add\"); \n}"
  CB = signature + body_datadef + body_senddef
  return CB # used for sending callback as string for file generation

