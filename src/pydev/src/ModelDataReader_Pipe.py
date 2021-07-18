import os
from message import Msg
import json
import select
import struct
from gen import *
IPC_FIFO_MODEL = "model_pipe"
def get_message(fifo, nbytes = 1024):
  return os.read(fifo, nbytes)
class ModelIPC_Writer:
  def __init__(self,loc):
    os.mkfifo(IPC_FIFO_MODEL)
    self.loc=loc
    self.cache = ModelCache()


    try:
      self.R=os.open(os.path.join(loc, IPC_FIFO_MODEL), os.O_RDONLY | os.O_NONBLOCK)
      
      print("model pipe is opened")
      try:
        poll = select.poll()
        poll.register(self.R, select.POLLIN)
        




        print("registered to the poll, entering loop")
        try:
          while True:
            if (self.R, select.POLLIN) in poll.poll(1000):


              print("----MODEL MESSAGE RECV----")
              msg = get_message(self.R)
              pkt = self.proc_json(msg)
              data_dict = self.process_nested_dicts(pkt["data"])

              self.cache.recv( data_dict , asdict = True)
              #pImsg.decode("utf-8"))
              print("logged message dict " + str(self.cache))

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
    try:
      return json.loads(msg)

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
