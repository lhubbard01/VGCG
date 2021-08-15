from gen_fwd import GraphBuild, conn
from IR      import ModuleIntermediateRepr, OutBound, x, xBound, InBound

from loggingConf import init_logger, Prepend

logger = init_logger(__file__, count = 1)
#logger.info = Prepend("PYTHON    [GEN]:")


def buildConnsDict(inbounds):

  print("BUILD CONNS:", inbounds)
  #construct a dictionary that organizes data as gen_fwd expects
  ins = {}
  if not inbounds:
    return None
  for el in inbounds:
    for k, v in el.items():
      ins[k] = v
  return ins

class ModelCache:
  def __init__(self):
    self.cache = {}
    self.conns = {}

  def recv(self, msg,    asdict: bool = False):

    message = msg
    data_type, message = msg["signal_type"], msg["pydict"]
    
    if data_type == "add":
      try:
        if not asdict:
          self.cache[message.name]  = message# ModuleIntermediateRepr(**message)

        else:
          self.cache[message["Name"]]  = message# ModuleIntermediateRepr(**message)
        logger.info(self.cache)


      except KeyError as ke:
        print(message)
    
    elif data_type =="conn-remove":
      print(self.conns)
      self.conns[message["from"]["Name"]] ["outs"] = [
        el for el in self.conns[message["from"]["Name"]] ["outs"] if not message["to"]["Name"] in el.keys()]

      self.conns[message["to"]["Name"]] ["ins"]    = [
        el for el in self.conns[message["to"]["Name"]]   ["ins"] if not message["from"]["Name"] in el.keys()]


    elif data_type =="conn":
      if not asdict: 
        pass          
      else: 
          print("PYTHON [CACHE]:from", self.conns, "\nPYTHON [CACHE]: message ", message)
          if "from" in message.keys():
            if not message["from"]["Name"] in self.conns.keys():
              self.conns[message["from"]["Name"]] = {"ins":[], "outs":[]}
            self.conns[message["from"]["Name"]] ["outs"].append({
              message["to"]["Name"] : message["to"]["count"]
            })  #if defined through a connection instead of features in and out 

          else:
            if not message["in"]["Name"] in self.conns.keys():
              self.conns[message["in"]["Name"]] = {"ins":[], "outs":[]}

            self.conns[message["in"]["Name"]]  ["outs"].append({
              message["in"]["Name"] : message["in"]["count"],
              })


          if "to" in message.keys():
            if not message["to"]["Name"] in self.conns.keys():
              self.conns[message["to"]["Name"]] = {"ins":[], "outs":[]}
            self.conns[message["to"]["Name"]] ["ins"].append({
              message["from"]["Name"] : message["from"]["count"],
            })


          else:
            if not message["out"]["Name"] in self.conns.keys():
              self.conns[message["out"]["Name"]] = {"ins":[], "outs":[]}

            self.conns[message["out"]["Name"]] ["outs"].append({
              message["out"]["Name"]: message["out"]["count"],
            })
      print("PYTHON [CACHE]:from", self.conns, "\nPYTHON [CACHE]: message ", message)
    elif data_type == "remove":
      #TODO handle deletion of different modules or connections
      pass
    elif data_type == "signal": 
      
      if message["signal"] == "verbose":
        print("PYTHON [CACHE]:Conn", self.conns, "\nPYTHON [CACHE]: Cache", self.cache)
      
      elif message["signal"] == "register":
        self.builder = GraphBuild(self.cache, indent = 4)

      
      elif message["signal"] == "reset": 
        self.cache = {}
        self.conns = {}
        print(self.__dict__)
        print("reset successfully executed")
      elif message["signal"] == "build":
        dict_modules=self.buildConns() 
        self.builder = GraphBuild(self.cache, indent = 4)
        dconns = self.builder.buildModuleGraph(dict_modules)
        print(dconns)




        with open("local.py", "w") as f:
          model = self.builder.model_str + "\n" + self.builder.fwd_str
          print(model)
          f.write(model)
        
      #TODO handle processing of 1) build signal 2) launch signal
    else:
      raise ValueError("unexpected data dictionary!")


  def buildConns(self):
    """dMod is a dictionary of modules containing connections between
    others. inbounds and outbounds represent the information flow relative to 
    the module. This information is used by the gen_fwd module"""
    dMod = {}

    for name, value in self.conns.items():
      
      print("NAME", name,"\n", self.cache[name], "*"*80)
      dMod[name] = conn(
                          name,
                          buildConnsDict(value["ins"]), 
                          buildConnsDict(value["outs"]))

      self.cache[name] = {**self.cache[name],  ** dMod[name].dr}
      self.cache[name] = ModuleIntermediateRepr(**self.cache[name])

    print(dMod)
    return dMod
  
  def __str__(self):
    return str(self.cache)






  def run(self):
    subprocess.call("",shell = True)

if __name__ == "__main__":
  #test ## construct densenet (as only a composition of linear transformations) 
  # this demonstrates the mvp 
  iRepr = ModuleIntermediateRepr
  cache = ModelCache()
  cache.recv(iRepr(name = "A",
        inbound = None,
        outbound = [OutBound(x("B", 50)), OutBound(x("C",50)), OutBound(xBound("D",50))], 
        hypers = {"in_features":784, "out_features":50},
        isNative = True, 
        isParametric = True,
        mType = "Linear"), data_type = "model_cache")

  cache.recv(iRepr(name = "B",
        inbound = [InBound(x("A",50))], 
        outbound = [OutBound(x("C",50)),OutBound(xBound("D",50))], 
        hypers = {"in_features":50, "out_features": 50}, 
        isNative = True,
        isParametric = True,
        mType = "Linear"), data_type = "model_cache")

  cache.recv(iRepr(name = "C",
        inbound = [InBound(x("A",50)), InBound(x("B",50))], 
        outbound = [OutBound(xBound("D",50))],
        hypers = {"in_features": 100, "out_features":50},
        isNative = True,
        isParametric = True, 
        mType = "Linear"), data_type="model_cache")

  cache.recv(iRepr(name = "D",
        inbound = [InBound(x("A",50)),InBound(x("B",50)), InBound(x("C",50))], 
        outbound = None, 
        hypers = {"in_features" : 150, "out_features" : 1},
        isNative = True, 
        isParametric = True,
        mType = "Linear"), data_type = "model_cache")
  builder = GraphBuild(cache.cache, indent = 4)

  dConns = builder.buildModuleGraph(cache.buildConns())
  print("connection dictionary: ", dConns)
  print("MODEL: ",builder.model_str, "\nforward: ",builder.fwd_str)
