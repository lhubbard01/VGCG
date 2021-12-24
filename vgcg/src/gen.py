from gen_fwd import GraphBuild, FileTemplate, conn
from IR      import ModuleIntermediateRepr, OutBound, x, xBound, InBound

from loggingConf import init_logger, Prepend, VERBOSE
VERBOSE = True
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
from api import ApiSignalHandler










class ModelCache:

  def __init__(self):
    self.cache = {}
    self.built_cache = {} 
    self.conns = {}
    self.built_cache_as_IR = {}

    self.API = ApiSignalHandler( {
      "add":self.add,
      "delete": self.remove,
      "conn_remove": self.conn_remove,
      "conn": self.conn,
      "update": self.update,
      "signal" : self.signal
      }
    )

  def recv(self, msg, asdict: bool = False):
    print("message: ", msg)
    #msg is a packet from the IPC
    data_type, message = msg["signal_type"], msg["pydict"]
    self.API.recv(data_type, message) 

  def add_new_node(self, name):

    self.conns[name] = {
      "ins" : [], 
      "outs": []
    }

  def add(self, message):
    self.cache[message["Name"]]  = message# ModuleIntermediateRepr(**message)
    logger.info(self.cache)

  def conn_remove(self, message):
      print(self.conns)
      sender = message["from"]
      recvr  = message["to"]
      if sender["Name"] == recvr["Name"]:
        print("sending to self! treated as a user error, continuing...")
        return
      #There might be a better way to represent the data packets. Maybe just make a class?
      #updates the outut list to disinclude the receiver of this connection 
      self.conns[sender["Name"]] ["outs"] = [
        el for el in self.conns[sender["Name"]]["outs"] if not recvr["Name"] in el.keys()]
      #updates the input list for the receiver to disinclude the sender of this connection
      self.conns[recvr["Name"]] ["ins"]    = [
        el for el in self.conns[recvr["Name"]]["ins"] if not sender["Name"] in el.keys()]

      print(self.conns[recvr["Name"]]["ins"])

  def conn(self, message):
    print("PYTHON [CACHE]: connections: ", self.conns, "\nPYTHON [CACHE]: message ", message)
    
    connections = list(self.conns.keys())

    if "from" in message.keys():
      sender = message["from"]
      recvr  = message["to"]

      if not sender["Name"] in connections:
        self.add_new_node(sender["Name"])
      
      self.conns[ sender["Name"] ] ["outs"].append({
              recvr["Name"] : recvr["count"]
            })  #if defined through a connection instead of features in and out 

      if not recvr["Name"] in connections:
        self.add_new_node(recvr["Name"])
      
      self.conns[recvr["Name"]] ["ins"].append({
              sender["Name"] : sender["count"],
            })
    

  def remove(self, message):
    to_remove = message["Name"]
    for key in self.conns.keys(): 
      
      #remove for inputs
      for i, connect in enumerate(self.conns[key]["ins"]):
        if to_remove in list(connect.keys()):
          self.conns[key]["ins"].pop(i)
          if VERBOSE: 
            print("removed " + to_remove + " from " + key + " ins, which is now " + str(self.conns[key]["ins"]) )
      

      #remove for outputs too

      for i, connect in enumerate(self.conns[key]["outs"]):
        if to_remove in list(connect.keys()):
          self.conns[key]["outs"].pop(i)
          if VERBOSE: 
            print("removed " + to_remove + " from " + key + " outs, which is now " + str(self.conns[key]["outs"]) )
    self.conns.pop(to_remove)


    if to_remove in list(self.cache.keys()): 
      self.cache.pop(to_remove) 
      print("remove " + to_remove + " from model cache, which is now " + str(self.cache))
    
  def update(self, message):
      self.cache[message["Name"]] = message
    
      
  def signal(self, message):
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
        #creates connections -> self.built_cache, and then corresponding intermediate representation -> self.built_cache_as_IR
        dict_modules = self.buildConns() 
        self.builder = GraphBuild(self.built_cache_as_IR, indent = 4)

        dconns = self.builder.buildModuleGraph(dict_modules)

        print(dconns)

        ft = FileTemplate()
        ft.add_model(self.builder.model_str + "\n" + self.builder.fwd_str)
        ft.write_to("local.py")
      #TODO handle processing of 1) build signal 2) launch signal


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
      self.built_cache[name] = {
          **self.cache[name],  
          **dMod[name].dr
        }

      

      self.built_cache_as_IR[name] = ModuleIntermediateRepr(**self.built_cache[name])

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

  cache.recv(
    iRepr(name = "C",
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
