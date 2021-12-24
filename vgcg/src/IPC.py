import os
import time
import json
import logging
import select
import signal
import re


#designators for the interprocess communication via pipes with node server (bidirectional)
IPC_FIFO_NAME_A = "pipe_a"
IPC_FIFO_NAME_B = "pipe_b"
import datetime as dt








IPC_FIFO_MODEL = "model_pipe"

from loggingConf import CountLogger, init_logger, VERBOSE

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
    global VERBOSE
    if VERBOSE :
      logger.info("MESSAGE: ", type(msg), msg, "\nPIPE: ", type(self.pipe))
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
symtable = {}
VERBOSE = False
def log_input(msg, *args):
  
  
  


  global VERBOSE
  if VERBOSE:
    print(msg, args)
  #global logger
  preface_str = ""
  for arg in args:
    preface_str += str(arg) + " "
  
  if VERBOSE: logger.info(preface_str, "LOGGING: ", msg, " type: ", type(msg))
  return msg

def handle_message_runtime( msg_dict):
  global exec_history, symtable #, logger
  msg, outbound = msg_dict["data"], None
  l_r = msg.split("=")
  

  l_r[0] = l_r[0].replace(" ","")
  try:
    exec(msg, globals(), locals())
    if len(l_r) > 1:
      exec("symtable[l_r[0]] = " + l_r[1], globals(), locals());
      outbound = symtable[l_r[0]]
  except NameError as ne:
    try:
      print(symtable); print(msg.replace(" ",""))
      outbound = symtable[msg]
    except KeyError as ke:    outbound = str(ke)
    except SyntaxError as se: outbound = str(se) 
  except SyntaxError as se:
    outbound = str(se) 

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
    

    out1 = log_input(msgdict, "INBOUND")
    if msgdict["route"] == "model":
      out1 = moveToModel(msg)
      logging.info("moved to model")

    elif msgdict["route"] == "pyexec":
      out1  = handle_message_runtime(msgdict)
      logging.info("handle interpreter state pyexec") 

    log_input(out1, "OUTBOUND")
   
    return str(out1)


  except Exception as e:
    raise e
    logging.critical(e)
    raise e



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
    global VERBOSE
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
              if VERBOSE:
                logger.info("--------received from JS--------");logger.info("    " + msg.decode("utf-8"))
                logger.info("\n\n\n\n");
              outbound = process_message(msg)
  
              if VERBOSE: logger.info("-------writing------", outbound)
              os.write(fifo_b, bytes(str(outbound),"utf-8"))
              

        


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
