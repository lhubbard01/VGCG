import atexit

import os
import subprocess as sp

runtime_registry = []
def launch(cmd):
  return sp.Popen(cmd, cwd=".")

def r_append(X):
  global runtime_registry
  runtime_registry.append(X)


def clean_procs():
  global runtime_registry
  for pid in runtime_registry:
    print(signal.pidfd_send_signal(pid, signal.SIGTERM))
  
atexit.register(clean_procs)  



print("launching IPC...")
r_append( launch("python3 ../../pydev/src/IPC.py"))

print("launching IPC...")
r_append( launch("node jsipc.js"))

print("IPC protocol up between node and python3!")


