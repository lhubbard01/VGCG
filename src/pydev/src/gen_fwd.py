import os
import string
import sys

import torch
import torch.nn as nn

from collections import OrderedDict

from IR import ModuleIntermediateRepr 





class GraphBuild:

  def __init__(self, reprs, indent: int = 4, model_str: str = None, fwd_str: str = None):
    self.symtable = {}
    
    self.indent = indent
    self.model_str = (model_str if model_str else "")
    # repr is a dictionary of ModuleIntermediateRepr, used in init_call to construct "new" object and return string 
    self.fwd_str   = (fwd_str if fwd_str else indent * 1 * " " + "def forward(self, X):\n" )
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



  def addToConn(self, mod):
    #global not_done, fwd_str
    self.dConn[mod.name] = {"ins": mod.ins, "outs": mod.outs, "done": False, "repr_fwd": None}
    print(mod)
    if mod.ins:
      for in_name, in_card in mod.ins.items():
        if in_name in self.not_done:
          return False;
    else:
      mod.ins = {"X": 50}
      self.addToSym("X","X")
    if len(mod.ins ) > 1:
      #requires concat for the inputs
      name_ct, line = self.moduleInput(mod.ins) 
    

      sym =  mod.name+"Out"
      self.addToSym(mod.name,sym)

      line +=  "\n"+ self.indent * 2 * " " + sym +" = self." + mod.name + "(" + name_ct +")"
    else:
      #otherwise vanilla serial
      line = mod.name + "Out = self." + mod.name + "(" + self.getInSym(list(mod.ins.keys())[0]) + ")"
      self.addToSym(mod.name,mod.name+"Out")
  
    self.dConn[mod.name]["repr_fwd"] = line # line(s) representing requisite calls for forward pass
    self.dConn[mod.name]["done"] = True #status token, also remove from not done list

    self.not_done.pop(self.not_done.index(mod.name))
  
    self.model_str += self.indent * 2 * " " + "self." + mod.name + " = " + self.init_call(self.reprs[mod.name]) + "\n"# repr is a dictionary of ModuleIntermediateRepr, used in init_call to construct "new" object and return string 
    #This is the forward pass string 
    self.fwd_str   += self.indent * 2 * " " + self.dConn[mod.name]["repr_fwd"] + "\n"

    return True
  

  def buildModuleGraph(self, dMod):
    self.not_done = [name for name in dMod.keys()]
    #print(dConn, dMod, not_done)  
    curr = None
    for mod in dMod.keys():
      if dMod[mod].ins == None:
        print(dMod, dMod[mod])
        curr = dMod[mod]
        break

    self.addToConn( curr)

    while curr:
      print("Looping... ",curr)
      if dMod[curr.name].outs :
        for mod in dMod[curr.name].outs:
          print(f"mod {mod} from {curr.name} outs")
          self.addToConn( dMod[mod])
      print("exit on " + curr.name)
      

      if len(self.not_done) > 0 :
        print(self.not_done)
        curr = dMod[self.not_done[0]];
        print(83)
        self.addToConn( curr);

      else: 
        break
  
  
    return self.dConn






  def moduleInput(self, module_ins):
    name="Cat"
    for mod in module_ins.keys():
      name+=mod
    
    return name, name+" = torch.cat((" + self.getInSyms(module_ins) + "), dim = 1)"



not_done = []
class conn:
  def __init__(self, name, ins, outs):  
    self.name = name
    self.ins  = ins
    self.outs = outs
    self.dr = {"Name":self.name, "inbound":self.ins, "outbound":self.outs}
  def __repr__(self):
    return str({"name":self.name, "ins": self.ins, "outs": self.outs})
  def __str__(self):
    return str(self.__repr__())

"""

buildModuleGraph({"A": conn("A",ins= None, outs = {"B":50, "C":50, "D":50}),
  "B" : conn("B", ins={"A":50}, outs={"C":50, "D":50}),
  "C":conn("C",ins= {"A":50, "B":50}, outs = {"D":50}),
  "D": conn("D", ins = {"A":50, "B":50, "C":50}, outs=None)})
print(dConn)
print(fwd_str)"""
