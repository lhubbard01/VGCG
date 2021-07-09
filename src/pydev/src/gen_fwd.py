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

def addToConn(dConn, mod):
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

    line += "\n"+ sym +" = " + mod.name + "(" + name_ct +")"
  else:
    line = mod.name + "Out = " + mod.name + "(" + getInSym(list(mod.ins.keys())[0]) + ")"
    addToSym(mod.name,mod.name+"Out")#symtable[mod.name] = sym

  dConn[mod.name]["repr_fwd"] = line
  dConn[mod.name]["done"] = True

  not_done.pop(not_done.index(mod.name))
  fwd_str+=dConn[mod.name]["repr_fwd"] + "\n"
  return True




#dMod = {}
dConn = {}

def build(dMod):
  
  global dConn, not_done
  not_done = [name for name in dMod.keys()]
  curr = None
  for mod in dMod.keys():
    if dMod[mod].ins == None:
      print(dMod, dMod[mod])
      curr = dMod[mod]
      break
  addToConn(dConn, curr)
  for mod in dMod[curr.name].outs:
    addToConn(dConn, dMod[mod])


  


not_done = []
class conn:
  def __init__(self, name, ins, outs):  self.name, self.ins, self.outs = name, ins, outs
#def isModDone(mod):
#if dConn[mod.name].ins 
build({"A": conn("A",ins= None, outs = {"B":50, "C":50}),
  "B" : conn("B", ins={"A":50}, outs={"C":50}),
  "C":conn("C",ins= {"A":50, "B":50}, outs = None)
  })
print(dConn)
print(fwd_str)
