import logging

from loggingConf import CountLogger

def init_logger():
  logger                 = CountLogger(threshold = 100, name = __name__)

  stdout_logging_handler = logging.StreamHandler()
  stdout_logging_handler = logging.FileHandler("runtime.log", delay = True)
  stdout_logging_fmt     = logging.Formatter("%(levelname)s %(asctime)s %(message)s", datefmt="%Y-%m-%dT%H:%M:%sZ")
  stdout_logging_handler.setLevel(logging.INFO)
  stdout_logging_handler.setFormatter(stdout_logging_fmt)
  
  logger.addHandler(stdout_logging_handler)

  logger.setLevel(logging.INFO)

  return logger

#logger.(format="%(levelname) %(asctime)s %(message)", datefmt="%Y-%m-%dT%H:%M:%sZ")


import atexit
import os
import signal
import subprocess as sp


runtime_registry = []

    
def launch(cmd):
  logger.info("launching " + str(cmd))
  if not isinstance(cmd, list) and isinstance(cmd, str): 
    cmd = cmd.split()
  logger.info("opening process")  
  return sp.Popen(cmd, cwd=".")

def r_append(X):
  global runtime_registry
  logger.info(f"registering {X} to exit registry")
  runtime_registry.append(X)
  logger.info(X)

def clean_procs():
  global runtime_registry
  for pid in runtime_registry:
      logging.info("exitting " + str(pid) + str(signal.pthread_kill(pid.pid, signal.SIGTERM)))
  
  logger.info("success cleaning processes")

def clean_pipes():
  pipes = [maybe_pipe for maybe_pipe in os.listdir(".") if "pipe" in maybe_pipe]
  logger.info("cleaning up pipes, " +str(pipes))
  [os.remove(pipe) for pipe in pipes]
  
  logger.info("success cleaning pipes")
logger = init_logger()
logger.info("registering all atexit calls")
#atexit.register(clean_procs)  
#atexit.register(clean_pipes)
#atexit.register(lambda : sp.call("pkill node", shell = True))

logger.info("successful registration of exit calls")


logging.info("launching IPC Python Main...")
PATH_IPC = "./IPC.py"
r_append( launch("python3 " + PATH_IPC))
logging.info("success on Python Main Launch!")

logging.info("launching IPC node...")
PATH_NODE = "./jsipc.js"
r_append( launch("node " + PATH_NODE))
logging.info("success on Node IPC Launch!")
logging.info("IPC protocol up between node and python3!")

logging.info("IPC protocol pending on ModelReader...")
print("launching IPC model reader...")
print(r_append)
PATH_MODEL_IPC = "./ModelDataReader_Pipe.py"
r_append( launch("python3 " + PATH_MODEL_IPC))
print("ALL PIPES LAUNCHED")
while True:
  1;
logger.critical("we shouldnt be here: exitting runtime loop")
