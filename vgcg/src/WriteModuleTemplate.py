import torch
import torch.nn as nn
import os
import sys

def touch(fl):
  with open(fl, "w") as f:
    f.write("")


class LinearWrite(nn.Linear):
  def __init__(self, in_features, out_features, write_loc: str = "local.txt", mode: str = "APPEND", **kwargs):
    super().__init__(in_features, out_features, **kwargs)
    if not os.path.isfile(write_loc): 
      touch(write_loc) 
      print(f"added {write_loc} to current dir")
    self.file_w = write_loc
    self.mode = mode 
  
  


  def write(self, X): 
    if self.mode == "APPEND" :
      with open(self.file_w, "a") as f:
        f.write(str(X)) 
    
    elif self.mode == "WRITE":
      with open(self.file_w, "w") as f:
        f.write(str(X))
  
  def forward(self, X):
    out = super().forward(X)
    self.write(out)
    return out


def generate_writeable(X, ins, write_loc, mode, include_imports: bool = False, is_in_torch: bool = True):
  
  #module definition 
  X_super = ("nn." + X if is_in_torch else "nn.Module")
  start = "class " + X + "Write(" + X_super + "):\n"


  
  #useful in case we are constructing a large file, dont want redundant import calls
  if include_imports: 
    imports = "import torch\nimport torch.nn as nn\nimport torch.nn.functional as F\n\nimport os\n\n\n"
    start = imports + start


  #module inputs specific string
  init_ins = (str(ins)+", " if ins is not None else "")

  #actual init string
  init = "  def __init__(self," + init_ins + write_loc + ": str = \"local.txt\", " + mode + ": str = \"APPEND\", **kwargs):\n"

  #super line to hook to pytorch
  _super = "    super().__init__(" + init_ins + "**kwargs)\n"

  #rest of file
  template_writeable = """
    self.file_w = write_loc
    self.mode = mode
  

  def write(self, X): 
    if self.mode == "APPEND" :
      with open(self.file_w, "a") as f:
        f.write(str(X)) 
    
    elif self.mode == "WRITE":
      with open(self.file_w, "w") as f:
        f.write(str(X))
  
  def forward(self, X):
    out = super().forward(X)
    self.write(out)
    return out

  """
  return start + init + _super + template_writeable #constructs a module that writes its output upon activation









if __name__ == "__main__":
  print("testing " + __file__ + "...\n")
  local = nn.Sequential(LinearWrite(100, 50), nn.ReLU(), LinearWrite(50, 10), nn.Softmax())
  D = torch.randn(1,1,100)

  print(D)
  local(D)


  write_model = generate_writeable("ReLU", None, "local.txt", "APPEND", include_imports = True)
  with open("other.txt", "w") as f:
    f.write(write_model)
print(write_model)
