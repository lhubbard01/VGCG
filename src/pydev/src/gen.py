from IR import *
from gen_fwd import *

def buildConnsDict(inbounds):
  ins = {}
  if not inbounds: return None
  for d in inbounds:
    ins[d.name] = d.count
  return ins

class ModelCache:
  def __init__(self):
    self.cache = {}

  def recv(self, msg, asdict: bool = False):
    message = msg#Msg(msg).proc()
    
    try:
      if not asdict:
        self.cache[message.Name]  = message# ModuleIntermediateRepr(**message)

    else:
      
      self.cache[message["Name"]]  = message# ModuleIntermediateRepr(**message)


    except KeyError as ke:
      print(message)


  def buildConns(self):
    dMod = {}
    for module, value in self.cache.items():
      dMod[value.Name] = conn(value.Name, buildConnsDict(value.inbound), buildConnsDict(value.outbound) )

    return dMod
  
  def __str__(self):
    return str(self.cache)




if __name__ == "__main__":
  #test
  iRepr = ModuleIntermediateRepr
  cache = ModelCache()
  cache.recv(iRepr(name = "A",
        inbound = None,
        outbound = [OutBound(x("B", 50)), OutBound(x("C",50)), OutBound(xBound("D",50))], 
        hypers = {"in_features":784, "out_features":50},
        isNative = True, 
        isParametric = True,
        mType = "Linear"))

  cache.recv(iRepr(name = "B",
        inbound = [InBound(x("A",50))], 
        outbound = [OutBound(x("C",50)),OutBound(xBound("D",50))], 
        hypers = {"in_features":50, "out_features": 50}, 
        isNative = True,
        isParametric = True,
        mType = "Linear"))

  cache.recv(iRepr(name = "C",
        inbound = [InBound(x("A",50)), InBound(x("B",50))], 
        outbound = [OutBound(xBound("D",50))],
        hypers = {"in_features": 100, "out_features":50},
        isNative = True,
        isParametric = True, 
        mType = "Linear"))

  cache.recv(iRepr(name = "D",
        inbound = [InBound(x("A",50)),InBound(x("B",50)), InBound(x("C",50))], 
        outbound = None, 
        hypers = {"in_features" : 150, "out_features" : 1},
        isNative = True, 
        isParametric = True,
        mType = "Linear"))
  builder = GraphBuild(cache.cache, indent = 4)
  dConns = builder.buildModuleGraph(dMod)
  print(dConns, builder.model_str, builder.fwd_str)
