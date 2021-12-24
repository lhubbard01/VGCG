import os
import string
import sys

import torch
import torch.nn as nn

from collections import OrderedDict

from IR import ModuleIntermediateRepr 




class FileTemplate:
  #used in buffering model file information until write. also where templates are loaded.
  def __init__(self, _file : str = None):
    self.file       = _file
    self.template   = None
    self.insert_loc = 0
    self.model = None

    if not _file: 
      self.template = "import torch\nimport torch.nn as nn\nimport torch.nn.functional as F"
      self.insert_loc = len(self.template) 
  

  def add_model(self, model_str):
    self.model = self.template + "\n\n" + model_str


  def write_to(self, loc):
    self.loc = loc
    with open(loc, "w") as f:
      print(self.model)
      f.write(self.model)
        

class GraphBuild:

  def __init__(self, reprs, indent: int = 4, model_str: str = None, fwd_str: str = None):
    self.symtable = {}
    
    self.indent = indent
    self.model_str = (model_str if model_str else
      "class LocalModel(nn.Module):\n" 
      + indent * 1 * " " + "def __init__(self):\n" 
      + indent * 2 * " " + "super(LocalModel, self).__init__()\n"
    )
    # repr is a dictionary of ModuleIntermediateRepr, used in init_call to construct "new" object and return string 
    self.fwd_str   = (fwd_str if fwd_str else indent * 1 * " " + "def forward(self, X):\n" )
    print("SELF FORWARD STRING", self.fwd_str)
    self.reprs = reprs
  
    self.dConn = {}
    
  def init_call(self, repr : ModuleIntermediateRepr):
      """function body is a wrapper to build method, a placeholder in case more work needs to be done on built string"""
      repr_str = repr.build() 
      return repr_str 

  def add_module_assignment(self, mod):
    return self.indent * 2 * " " + "self." + mod.name + " = " + self.init_call(self.reprs[mod.name]) + "\n"

  def addToSym(self, symbol, out):
    self.symtable[symbol] = out


  def getInSym(self, sym) :
    return self.symtable[sym]


  def getInSyms(self, module_ins):
    sb = ""
    for sym in module_ins.keys():
      sb += self.getInSym(sym) + ","
    return sb[:-1]



  def addToConn(self, mod, dMods):
    self.dConn[mod.name] = {
      "ins": mod.ins, 
      "outs": mod.outs, 
      "done": False, 
      "repr_fwd": None
    }

    print(mod)
    #for inputs to the current module
    if mod.ins:
      for in_name, in_card in mod.ins.items():
        if in_name in self.not_done:
          return False;
    #if none, give a default value
    else:
      mod.ins = {"X": 50}
      self.addToSym("X","X")


    if len(mod.ins ) > 1:
      s = 0
      #requires concat for the inputs
      #name of connecion, line being constructed
      name_ct, line = self.moduleInput(mod.ins) 
      sym =  mod.name+"Out"
      self.addToSym(mod.name,sym)
      line +=  "\n"+ self.indent * 2 * " " + sym +" = self." + mod.name + "(" + name_ct +")"
      for el in mod.ins:
        print("ELEMENT: " , el, " OUTPUTS: ", dMods[el].outs[mod.name])
        s += int ( dMods[el].outs[mod.name] ) #["outs"]
      self.reprs[mod.name].hypers["in_features"] = s
    else:
      #otherwise vanilla serial
      print("IS NORMAL VERSION, here is mod.ins, ", mod.ins)
      print(type(mod.ins))
      key = list(mod.ins.keys()) 
      print(key)
      if not "X" in key: 
        
        self.reprs[mod.name].hypers["in_features"] = int(dMods[key[0]].outs[mod.name])

      print("success!")
      line = mod.name + "Out = self." + mod.name + "(" + self.getInSym(list(mod.ins.keys())[0]) + ")"
      self.addToSym(mod.name,mod.name+"Out") #add to symbol table
    

    # line(s) representing requisite calls for forward pass
    self.dConn[mod.name]["repr_fwd"] = line 
    
    #status token, also remove from not done list
    self.dConn[mod.name]["done"] = True 
    self.not_done.pop(self.not_done.index(mod.name))
    
    # repr is a dictionary of ModuleIntermediateRepr, used in init_call to construct "new" object and return string 


    self.model_str += self.indent * 2 * " " + "self." + mod.name + " = " + self.init_call(self.reprs[mod.name], ) + "\n"
    
    #This is the forward pass string 
    self.fwd_str   += self.indent * 2 * " " + self.dConn[mod.name]["repr_fwd"] + "\n"

    return True
  

  def buildModuleGraph(self, dMod):
    self.not_done = [name for name in dMod.keys()]
    
    curr = None
    for mod in dMod.keys():
      if dMod[mod].ins == None:
        print(dMod, dMod[mod])
        curr = dMod[mod]
        break

    self.addToConn(curr, dMod)

    while curr:
      #print("Looping... ",curr)
      if dMod[curr.name].outs :
        for mod in dMod[curr.name].outs:
          print(f"mod {mod} from {curr.name} outs")
          self.addToConn( dMod[mod], dMod)
      print("exit on " + curr.name)
      

      if len(self.not_done) > 0 :
        print(self.not_done)
        curr = dMod[self.not_done[0]];
        self.addToConn(curr, dMod)

      else: 
        break
  

    # get last line of fwd, get first non whitespace nonempty substr
    outvar = list(filter(lambda x: x != "", 
        self.fwd_str.split("\n")[-2].split(" ")
        )
      )[0] 


    
    #complete forward string for model
    self.fwd_str += self.indent * 2 * " " + "return " + outvar + "\n"
    return self.dConn


  def moduleInput(self, module_ins):
    #construct names describing the variables relative to their input connections, where mod is module
    name = "Cat"
    for mod in module_ins.keys():
      name += mod
    
    return name, name+" = torch.cat((" + self.getInSyms(module_ins) + "), dim = 1)"



not_done = []
class conn:
  def __init__(self, name, ins, outs):  
    self.name = name
    self.ins  = ins
    self.outs = outs
    self.dr = {
      "Name"     :  self.name,
      "inbound"  : self.ins, 
      "outbound" : self.outs
    }
  


  def __repr__(self):
    return str(self.dr) #{"name" : self.name, "ins": self.ins, "outs": self.outs})
  
  def __str__(self):
    return str(self.__repr__())



"""
TESTING CODE FOR THIS FILE
buildModuleGraph({"A": conn("A",ins= None, outs = {"B":50, "C":50, "D":50}),
  "B" : conn("B", ins={"A":50}, outs={"C":50, "D":50}),
  "C":conn("C",ins= {"A":50, "B":50}, outs = {"D":50}),
  "D": conn("D", ins = {"A":50, "B":50, "C":50}, outs=None)})
print(dConn)
print(fwd_str)"""
