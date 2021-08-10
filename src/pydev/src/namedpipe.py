import os
import re
import select


class NamedPipe:
  def __init__(self, name: str, loc: str = "."):
    self.name = name
    self.O=[]
    if name in os.listdir(loc):
      print("NOTE: target direcrory contains extant pipe of same name!")
    
    self.path = os.path.join(loc, name)
  
  def __call__(self):
    #TODO can receive bytes or be opened, or accept bytes to send.
    pass
  


  def __str__(self): 
    s = str(self) + ": " + "NAME: " + self.name + "\nLOC: " + str(self.path) + "\nOPTS: " + str(self.opts)

  def __del__(self):
    try:
      if os.path.exists(self.path):
        os.remove(self.path)
        LOG("EXITTING W SUCCESSFUL DELETION OF ", self.path)
      else:
        LOG("EXXITTING W O DESTROYING PIPE BC NOT FOUND")
    except FileNotFoundError as FNFE: 
      LOG("FAILURE | ", FNFE)


  def open(self, flag, *args):
    """works with os.O_* enum as well as integers, for bitwise OR= op, 
    opening and maintaining only 1 pipe per object
    accepts at least one argument, as many as user wants though.

    args are the required bitfields being set.

    returns nothing
    """
    opts = 0
    
    ENUMS = [f for f in os.__all__ if re.match(r"^O_[A-Z]+]", f)]
    for arg in args:
      if isinstance(arg, int):
        opts |= arg
        self.O += retrieve_enum(arg, ENUMS)
    LOG(opts)
    self.opts = opts 
    
    try:
      self.pipe = os.mkfifo(self.path, mode = opts)
    except FileExistsError as FEE:
      LOG("FAILURE | " , FEE)
      raise FEE

    LOG("Created pipe " + self.path + " successfully!")


def loglocal(*args):
  prepend = "[PYTHON NAMED_P] | " 
  for arg in args:
    prepend += str(arg) + ", "

  prepend = prepend[:-2]
  print(prepend)
  return prepend

LOG = loglocal


def retrieve_enum(enum_x: int, enum_list: list) -> list:
  """performs a per enumerated option check on x to determine corresponding option"""
  for enum_el in enum_list: 
    #LOG(enum_el, type(enum_el), enum_x)
    if eval("os." + enum_el + "== enum_x"):
      #LOG("SUCCESS", enum_el, enum_x)
      return enum_el

if __name__ == "__main__":
  retrieve_enum(2, [f for f in os.__all__ if re.match(r"^O_[A-Z]+", f)])
  b=NamedPipe(name="A", loc = ".")
  b.open(os.O_WRONLY)
  
