#Adapted from
#https://levelup.gitconnected.com/inter-process-communication-between-node-js-and-python-2e9c4fda928d
import os
import json
import logging
import select
import signal
import re
#designators for the interprocess communication via pipes with node server (bidirectional)
IPC_FIFO_NAME_A = "pipe_a"
IPC_FIFO_NAME_B = "pipe_b"














import struct
#<I
IPC_FIFO_MODEL = "model_pipe"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class FifoModel:
  def __init__(self, loc):
    self.loc = loc
    try:
      self.pipe =  os.open(os.path.join(self.loc, IPC_FIFO_MODEL), os.O_WRONLY)
    except Exception as e:
      raise e
  
  def __call__(self, msg):
    logging.info(type(msg))
    self.write(msg)

  def write(self, msg):
    if not isinstance(msg, bytes):
      if not isinstance(msg, str):
        os.write(self.pipe, bytes(str(msg),"utf-8"))
      else:
        os.write(self.pipe, bytes(msg,"utf-8"))
    else:
      os.write(self.pipe, msg)

  def exit(self):
    try:
      os.remove(os.path.join(self.loc,IPC_FIFO_MODEL))
    except FileNotFoundError as fnfe:
      logger.critical(fnfe)

    
def moveToModel(msg):
  global fifo_model
  fifo_model(msg)

exec_history = []
def log_input(msg, *args):
  preface_str = ""
  for arg in args:
    preface_str += arg + " "


  logging.info(preface_str, "LOGGING: ", msg, " type: ", type(msg))
  return msg

def handle_message_runtime( msg):
  global exec_history
  try:
    outbound = eval(msg)
    if not outbound:
      outbound = True
  except SyntaxError as se:
    try:
      exec(msg, locals(), globals())
      if "plt" in msg:


        outbound = plt.__dir__()
      else:
        outbound = True
    except SyntaxError as sse:
      logging.critical(sse)
      raise sse

  exec_history.append(msg)
  return outbound


def get_message(fifo, nbytes = 1024):
  return os.read(fifo, nbytes)

def bytes_to_str(msg):
  try:
    outmsg = bytes.decode(msg)
    return outmsg
  except Exception as e:
    return "re_match" + str(e)
   
def re_match(msg):
  try: 
    if re.match(r"(dddd-dd-ddTdd:dd:dd).*", msg):
      return "TIME: " + msg
    elif "2021" in msg:
      return "TIME2: " + msg
  except TypeError as te:
    logging.critical(te)
    return str(te) 


def process_message(msg):
  try:
    msgdict = None
    try: 
      msgdict = json.loads(msg)

      logging.debug(msgdict)
    except Exception as e:
      raise e
    msgstr = bytes_to_str(msg)
    logging.debug(msgstr)
    

    #exec("msgdict= "+msg.replace("\\",""), globals(),locals())
    #print(msgdict)
    out1 = log_input(msgdict, "INBOUND")
    if msgdict["route"] == "model":
      msgstro=moveToModel(msg)#msgdict["data"])
      logging.info("moved to model")

    elif msgdict["route"] == "update":
      msg = handle_message_runtime(msg) 
      logging.info("handle interpreter state update") 

    log_input(msg, "OUTBOUND")

    return str(msg)


  except Exception as e:
    
    logging.critical(e)
    raise e
    #return str(type(e))+ "\n" + str(e)


#def kb_int():

#signal

def pend_on_pipe(loc, name, F_flags):
  while True:
    try:
      fifo = os.open(os.path.join(loc, name), F_flags) 
      logging.info("pipe ", name, " is opened")
      return fifo
    except: 
      pass


class IPC_Handler:
  def __init__(self, loc):
    global fifo_model
    os.mkfifo(IPC_FIFO_NAME_A)


    try:
      fifo_a = os.open(os.path.join(loc, IPC_FIFO_NAME_A), os.O_RDONLY | os.O_NONBLOCK)
      logging.info("pipe a is opened")

      fifo_b     = pend_on_pipe(loc, IPC_FIFO_NAME_B, os.O_WRONLY)
      logging.info("pipe b is opened")

      pipe_model = FifoModel(loc)
      logging.info("model pipe is opened")


      """
      while True:
        try:
          fifo_b = os.open(os.path.join(loc, IPC_FIFO_NAME_B), os.O_WRONLY)
          logging.info("Pipe B is opened")
          break
        except:
          pass
      while True:
        try:
          fifo_model = FifoModel(loc)
          print("model fifo is opened")
          break
        except:
          pass
      #Polling A"""
      try:
        logging.info("initiating pipe polling")
        poll = select.poll()
        poll.register(fifo_a, select.POLLIN)
        try:
          while True:
            if (fifo_a, select.POLLIN) in poll.poll(1000):
              logging.info("--------received from JS--------")
              logging.info("    " + msg.decode("utf-8"))

              msg      = get_message(fifo_a)
              outbound = process_message(msg)
  
              logging.info("-------writing------", outbound)
              os.write(fifo_b, bytes(outbound,"utf-8"))
              

        except KeyboardInterrupt:
          pass

        finally:
          logging.info("select poll unregistering pipe a")
          poll.unregister(fifo_a)
      finally:
        logger.info("os closing fifo a pipe") 
        os.close(fifo_a)
    finally:
      logger.info("OS removing IPC FIFO PIPES")
      os.remove(os.path.join(loc, IPC_FIFO_NAME_A))
      logger.info("removed pipe a")
      os.remove(os.path.join(loc,IPC_FIFO_NAME_B))
      logger.info("removed pipe b")
      fifo_model.exit()
      logger.info("removed model pipe")

  print("exiting runtime")

fifo_model = None
if __name__ == "__main__":
    IPC_Handler(".")
