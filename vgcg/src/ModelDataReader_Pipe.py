import json
import os
import time
import select
import struct
from message import Msg
from gen import ModelCache
from loggingConf import CountLogger, init_logger

IPC_FIFO_MODEL = "model_pipe"





logger = init_logger(__file__)
def get_message(fifo, nbytes = 1024):
  return os.read(fifo, nbytes)





def prepend(*args):
  PREPEND = time.asctime() + " | PYTHON [MODEL]:"
  for arg in args:
    PREPEND += str(arg)

  print(PREPEND)



print("loading")
logger.info = prepend
class ModelIPC_Writer:

  def __init__(self,loc):
    os.mkfifo(IPC_FIFO_MODEL)
    
    self.loc   = loc
    self.cache = ModelCache()

    try:
      self.R=os.open(os.path.join(loc, IPC_FIFO_MODEL), os.O_RDONLY | os.O_NONBLOCK)
      
      logger.info("MODEL: model pipe is opened")

      try:
        poll = select.poll()
        poll.register(self.R, select.POLLIN)

        logger.info("registered to the poll, entering loop")

        try:
          while True:
            if (self.R, select.POLLIN) in poll.poll(1000):


              logger.info("PYTHON [MODEL]| ----MODEL MESSAGE RECV----")
              msg = get_message(self.R)
              pkt = self.proc_json(msg)
              pkt["pydict"] =  self.process_nested_dicts(pkt["data"])

              logger.info( pkt, "\n STARTING CACHE RECEIVE")
              assert isinstance(pkt, dict)
              self.cache.recv( pkt , asdict = True)
              #pImsg.decode("utf-8"))
              logger.info("logged message dict " + str(self.cache))
              #print("PYTHON [MODEL]: logged message dict " + str(self.cache))

        except Exception as e:
          raise e

      except Exception as e:
        raise e

      finally: 
        print("exitting, unregistering model pipe")
        poll.unregister(self.R)

    except Exception as e: 
      print(e)
      raise e

    finally:
      os.remove(os.path.join(self.loc, IPC_FIFO_MODEL))
      print("done model ipc")

  def proc_json(self, msg):
    #exists to process nested string versions of parameters from frontend packets
    try:
      out = json.loads(msg)
      logger.info(str(msg))
      return out

    except Exception as e: 
      print(e)
      return msg

  def process_nested_dicts(self, msg_dict):
    out = {}

    for k, v in msg_dict.items():
      if isinstance(v, str) and "{" in v and "}" in v:
        out[k] = self.process_nested_dicts(self.proc_json(v))
      else:
        out[k] = v
    return out

ModelIPC_Writer(loc = ".")
