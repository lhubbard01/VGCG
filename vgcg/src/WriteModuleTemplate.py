import json

import torch
import torch.nn as nn

import numpy as np

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
    X_np = X.clone().detach().numpy()
    X_colorspace_255 = ((X_np + np.abs(X_np.min()))/X_np.max()) * 255
    X_colorspace_255.astype(np.uint8)
    if self.mode == "APPEND" :
      with open(self.file_w, "a") as f:
        f.write(str(X_colorspace_255)) 
    
    elif self.mode == "WRITE":
      with open(self.file_w, "w") as f:
        f.write(str(X))
  
  def forward(self, X):
    out = super().forward(X)
    self.write(out)
    return out


def generate_writeable(name: str, ins: str, write_loc: str, mode: str, include_imports: bool = False, is_in_torch: bool = True):
  
  #module definition 
  name_super = ("nn." + name if is_in_torch else "nn.Module")
  start = "class " + name + "Write(" + name_super + "):\n"


  id_check = "    if id is None:  raise ValueError(\"each writing module requires a unique id for payloading.  '" + name + "Write'  aborting...\")\n"
  #useful in case we are constructing a large file, dont want redundant import calls
  if include_imports: 
    imports = "import torch\nimport torch.nn as nn\nimport torch.nn.functional as F\n\nimport numpy as np\nimport os\nimport json\n\n"
    start = imports + start


  #module inputs specific string
  init_ins = (str(ins)+", " if ins is not None else "")

  #actual init string
  init = "  def __init__(self," + init_ins + "write_loc: str = \"" + write_loc + "\", mode: str = \"" + mode +"\", id  = None, **kwargs):\n"

  #super line to hook to pytorch
  _super = "    super().__init__(" + init_ins + "**kwargs)\n"

  #rest of file
  template_writeable = """
    self.file_w = write_loc
    self.mode = mode
    self.id = id

  def write(self, X): 
    X_np = X.clone().detach().numpy()
    X_min, X_max = np.abs(X_np[0].min()), np.abs(X_np[0].max())
    X_colorspace_255 = (X_np[0] + X_min)/(X_max + X_min) * 255
    X_colorspace_255 = X_colorspace_255.astype(np.uint8)
    if self.mode == "APPEND" :

      with open(self.file_w, "a") as f:
        json.dump({"data": str(X_colorspace_255), "id": self.id}, f) #originally was f.write
        f.write(\"\\n\") 
    elif self.mode == "WRITE":
      with open(self.file_w, "w") as f:
        f.write(str(X_colorspace_255))
  
  def forward(self, X):
    out = super().forward(X)
    self.write(out)
    return out

  """
  return start + init + _super + id_check + template_writeable #constructs a module that writes its output upon activation





def write_generate_writeable(name, ins, write_loc, mode : str= "APPEND", include_imports: bool = False, is_in_torch: bool = True):
  write_model = generate_writeable(name = name, ins = ins, write_loc = write_loc, mode = mode, include_imports = include_imports, is_in_torch = is_in_torch)
  with open(name + "Write.py", "w") as f:
    f.write(write_model)
  print("wrote ", write_model)

if __name__ == "__main__":
  print("testing " + __file__ + "...\n")
  write_generate_writeable("Linear", ins = "in_features, out_features", write_loc = "local.txt", include_imports = True)
  write_generate_writeable("ReLU", ins = None, write_loc = "local.txt", include_imports = True)
  from LinearWrite import LinearWrite
  from ReLUWrite import ReLUWrite
  local = nn.Sequential(LinearWrite(100, 50, id="L1"), ReLUWrite(id = "R1"), LinearWrite(50, 10, id="L2"), nn.Softmax())
  D = torch.randn(1,1,100)
  print(D)
  local(D)
  

