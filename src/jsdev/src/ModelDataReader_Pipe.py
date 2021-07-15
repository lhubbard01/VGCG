import os
import select
import struct

IPC_FIFO_MODEL = "model_pipe"
def get_message(fifo, nbytes = 1024):
  return os.read(fifo, nbytes)
class ModelIPC_Writer:
  def __init__(self,loc):
    os.mkfifo(IPC_FIFO_MODEL)
    self.loc=loc
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
              print("    " + msg.decode("utf-8"))
        except:
          pass
      except:
        pass
      finally: 
        print("exitting, unregistering model pipe")
        poll.unregister(self.R)
    except Exception as e: 
      print(e)
    finally:
      os.remove(os.path.join(self.loc, IPC_FIFO_MODEL))
      print("done model ipc")

ModelIPC_Writer(loc = ".")
