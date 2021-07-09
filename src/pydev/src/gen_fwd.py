import torch
import torch.nn 
import torch.nn 
symtable = {}
fwd_str=""
model_str=None
def addToSym(symbol, out):
  global symtable
  symtable[symbol] = out
def getInSym(sym):
  global symtable
  return symtable[sym]

def getInSyms(module_ins):
  sb = ""
  for sym in module_ins.keys():
    sb += getInSym(sym)
  return sb

def moduleInput(module_ins):
    name="Cat"
    for mod in module_ins.keys():
      name+=mod
    
    return name, name+" = torch.cat(("+getInSyms(module_ins) + "), dim = 1)"

def addToConn(dConn, mod, indent: int = 4):
  global not_done, fwd_str
  dConn[mod.name] = {"ins": mod.ins, "outs": mod.outs, "done": False, "repr_fwd": None}

  if mod.ins:
    for in_name, in_card in mod.ins.items():
      if in_name in not_done:
        return False;
  else:
    mod.ins = {"X": 50}
    addToSym("X","X")
  if len(mod.ins ) > 1:
    name_ct, line = moduleInput(mod.ins) 
    

    sym =  mod.name+"Out"
    addToSym(mod.name,sym)#symtable[mod.name] = sym

    line +=  "\n"+ indent * " " + sym +" = " + mod.name + "(" + name_ct +")"
  else:
    print(f"mod {mod}")
    line = mod.name + "Out = " + mod.name + "(" + getInSym(list(mod.ins.keys())[0]) + ")"
    addToSym(mod.name,mod.name+"Out")#symtable[mod.name] = sym

  dConn[mod.name]["repr_fwd"] = line
  dConn[mod.name]["done"] = True

  not_done.pop(not_done.index(mod.name))
  
  fwd_str += indent * " " + dConn[mod.name]["repr_fwd"] + "\n"
  return True
dConn = {}

def build(dMod):
  global dConn, not_done
  print(dConn, dMod, not_done)  
  not_done = [name for name in dMod.keys()]
  print(not_done)
  curr = None
  for mod in dMod.keys():
    if dMod[mod].ins == None:
      print(dMod, dMod[mod])
      curr = dMod[mod]
      break
  addToConn(dConn, curr)
  while curr:
    print("Looping... ",curr)
    if dMod[curr.name].outs :
      for mod in dMod[curr.name].outs:
        print(f"mod {mod} from {curr.name} outs")
        addToConn(dConn, dMod[mod])
    print("exit on " + curr.name)
    if len(not_done) > 0 :
      print(not_done)
      curr = dMod[not_done[0]];
      print(83)
      addToConn(dConn, curr);

    else: break
  


not_done = []
class conn:
  def __init__(self, name, ins, outs):  self.name, self.ins, self.outs = name, ins, outs
  def __repr__(self): return str({"name":self.name, "ins": self.ins, "outs": self.outs})
  def __str__(self): return str(self.__repr__())
#def isModDone(mod):
#if dConn[mod.name].ins 
build({"A": conn("A",ins= None, outs = {"B":50, "C":50, "D":50}),
  "B" : conn("B", ins={"A":50}, outs={"C":50, "D":50}),
  "C":conn("C",ins= {"A":50, "B":50}, outs = {"D":50}),
  "D": conn("D", ins = {"A":50, "B":50, "C":50}, outs=None)})
print(dConn)
print(fwd_str)
