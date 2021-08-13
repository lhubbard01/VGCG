import os
import time
from IPython import embed
import json
import logging
import select
import signal
import re
#designators for the interprocess communication via pipes with node server (bidirectional)
IPC_FIFO_NAME_A = "pipe_a"
IPC_FIFO_NAME_B = "pipe_b"
import datetime as dt








VERBOSE = False
IPC_FIFO_MODEL = "model_pipe"

from loggingConf import CountLogger, init_logger

logger = init_logger(__file__, count = 1)
def prepend(*args):


  PREPEND = time.asctime() + " | PYTHON  [MAIN]:"
  for arg in args:
    PREPEND += str(arg)
  print(PREPEND)


logger.info = prepend

"""
class FifoModel:
  def __init__(self, loc):
    self.loc = loc
    try:
      self.pipe =  os.open(os.path.join(self.loc, IPC_FIFO_MODEL), os.O_WRONLY)
    except Exception as e:
      raise e
  
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

  """  
class FifoModel:
  def __init__(self, PIPE):
    self.pipe = PIPE

  def __call__(self, msg):
    self.write(msg)


  def write(self, msg : (bytes, str)):
    
    #logger.info("MESSAGE: ", type(msg), msg, "\nPIPE: ", type(self.pipe))
    if not isinstance(msg, bytes):
      if not isinstance(msg,str):
        os.write(self.pipe, bytes(str(msg), "utf-8"))

      else:
        os.write(self.pipe, bytes(msg), "utf-8")

    else:
      logging.info(msg, type(msg), self.pipe, type(self.pipe))

      os.write(self.pipe, msg)


def moveToModel(msg):
  global fifo_model
  fifo_model(msg)

exec_history = []
def log_input(msg, *args):
  print(msg, args)
  #global logger
  preface_str = ""
  

  for arg in args:
    preface_str += str(arg) + " "


  logger.info(preface_str, "LOGGING: ", msg, " type: ", type(msg))
  return msg

def handle_message_runtime( msg_dict):
  print("hmr")
  msg = msg_dict["data"]
  outbound = None
  global exec_history #, logger
  try:
    outbound = eval(msg)
    print("try eval succeeded")
    print(outbound, "outbound eval")
    if not outbound:
      outbound = True
  except Exception as se:
    
    embed()
    try:
      exec(msg, locals(), globals())
      if "plt" in msg:
        outbound = plt.__dir__()
      else:
        print("try succeeded")
        outbound = True
    except SyntaxError as sse:
      logging.critical(sse)
      raise sse

  exec_history.append(msg)
  print("exitting handle message runtime, outbound is ", outbound)
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
  print(msg)
  try:
    msgdict = None
    try: 
      msgdict = json.loads(msg)

      logging.debug(msgdict)
      print("this is the message dict", msgdict    ,"\nthis is the original message", msg)


    except Exception as e:
      raise e
    msgstr = bytes_to_str(msg)
    logging.debug(msgstr)
    

    #exec("msgdict= "+msg.replace("\\",""), globals(),locals())
    #print(msgdict)
    out1 = log_input(msgdict, "INBOUND")
    if msgdict["route"] == "model":
      print("moving to model, message is as ", msg)
      out1 = moveToModel(msg)#msgdict["data"])
      print("moved to model")
      logging.info("moved to model")

    elif msgdict["route"] == "pyexec":
      print("message rout is pyexec")
      out1  = handle_message_runtime(msgstr)
      logging.info("handle interpreter state pyexec") 

    log_input(out1, "OUTBOUND")
   
    return str(out1)


  except Exception as e:
    print("getting called at 170") 
    raise e
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
    global fifo_model, logger
    if not logger: 
      logger = init_logger()
    os.mkfifo(IPC_FIFO_NAME_A)
    try:
      fifo_a = os.open(os.path.join(loc, IPC_FIFO_NAME_A), os.O_RDONLY | os.O_NONBLOCK)
      logger.info("pipe a is opened")



      fifo_b     = pend_on_pipe(loc, IPC_FIFO_NAME_B, os.O_WRONLY)
      logger.info("pipe b is opened")

      fifo_model = FifoModel(pend_on_pipe(loc, IPC_FIFO_MODEL, os.O_WRONLY))
      logger.info("model pipe is opened")


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
        logger.info("initiating pipe polling")
        poll = select.poll()
        poll.register(fifo_a, select.POLLIN)
        try:
          while True:
            if (fifo_a, select.POLLIN) in poll.poll(1000):
              msg      = get_message(fifo_a)
              logger.info("--------received from JS--------");logger.info("    " + msg.decode("utf-8"))
              logger.info("\n\n\n\n");
              outbound = process_message(msg)
  
              logger.info("-------writing------", outbound)
              os.write(fifo_b, bytes(outbound,"utf-8"))
              

        


        except KeyboardInterrupt:
          pass

        finally:
          logger.info("select poll unregistering pipe a")
          #handles condition where a launching script calls this instead
          try:
            poll.unregister(fifo_a)

          except FileNotFoundError as fnfe :
            logger.info("cannot unregister selecting of pipe a due to pipe already being freed");



      finally:
        logger.info("os closing fifo a pipe") 
        #handles condition where a launching script calls this instead
        try:
          os.close(fifo_a)
        except FileNotFoundError as fnfe :
          logger.info("cannot close pipe a due to pipe already being freed");
    finally:
        
      #handles condition where a launching script calls this instead
      try:
        logger.info("OS removing IPC FIFO PIPES")
        os.remove(os.path.join(loc, IPC_FIFO_NAME_A))
        logger.info("removed pipe a")
        os.remove(os.path.join(loc,IPC_FIFO_NAME_B))
        logger.info("removed pipe b")
        #fifo_model.exit()
        logger.info("removed model pipe")
      except FileNotFoundError as fnfe :
        logger.info("did not find a pipe, assuming cleaned from caller.")

    print("exiting runtime")

fifo_model = None
if __name__ == "__main__":
    IPC_Handler(".")
