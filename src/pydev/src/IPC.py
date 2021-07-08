#Adapted from
#https://levelup.gitconnected.com/inter-process-communication-between-node-js-and-python-2e9c4fda928d
import os
import select
import signal
import re
#designators for the interprocess communication via pipes with node server (bidirectional)
IPC_FIFO_NAME_A = "pipe_a"
IPC_FIFO_NAME_B = "pipe_b"










exec_history = []
def log_input(msg, *args):
  preface_str = ""
  for arg in args:
    preface_str += arg + " "
  print(preface_str, "LOGGING: ", msg, " type: ", type(msg))
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
    print(te)
    return str(te) 




def process_message(msg):
  try:
    msg = bytes_to_str(msg)
    msg = log_input(msg, "INBOUND")
    msg = handle_message_runtime(msg) 
    log_input(msg, "OUTBOUND")
    return str(msg)
  except Exception as e:
    return str(type(e))+ "\n" + str(e)


#def kb_int():

#signal
class IPC_Handler:
  def __init__(self, loc):
    os.mkfifo(IPC_FIFO_NAME_A)
    try:
      fifo_a = os.open(os.path.join(loc, IPC_FIFO_NAME_A), os.O_RDONLY | os.O_NONBLOCK)
      print("pipe a is opened")
      while True:
        try:
          fifo_b = os.open(os.path.join(loc, IPC_FIFO_NAME_B), os.O_WRONLY)
          print("Pipe B is opened")
          break
        except:
          pass
      #Polling A
      try:
        print("initiating pipe polling")
        poll = select.poll()
        poll.register(fifo_a, select.POLLIN)
        try:
          while True:
            if (fifo_a, select.POLLIN) in poll.poll(1000):
              msg = get_message(fifo_a)
              outbound = process_message(msg)
              os.write(fifo_b, bytes(outbound,"utf-8"))
              print("--------received from JS--------")
              print("    " + msg.decode("utf-8"))
        except KeyboardInterrupt:
          pass
        finally:
          print("slect poll unregistering pipe a")
          poll.unregister(fifo_a)
      finally:
        print("os closing fifo a pipe") 
        os.close(fifo_a)
    finally:
      print("OS removing IPC FIFO PIPES")
      os.remove(os.path.join(loc, IPC_FIFO_NAME_A))
      os.remove(os.path.join(loc,IPC_FIFO_NAME_B))

  print("exiting runtime")
if __name__ == "__main__":
  IPC_Handler(loc = input("enter target location"))
