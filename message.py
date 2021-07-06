import json

import torch
import torch.nn as nn

#potenital message structures between js and python for module descriptions
"""hypers: {
}
{
  isNative : bool
  isWeighted : bool
}
{
  in_X  : int
  out_X : int
}"""






def seek(target: str, mp: dict):
  for key in mp:
    if target in key:
      return key, mp[key]
class Msg:
  """contains data payloads describing single primitive blocks, very open to change"""
  def __init__(self, msg):
    self.payload = msg
    self.obj = self.proc()

  def proc(self):
    """The payload comes in as a string of some mapping, following some
    specification of data organization. 
    This is used to write a dictionary from this string through concatenating 
    assignment statement with the string dict, and using that dictionary as python native
    after the execution of that statement. The object is then constructed from
    these parameters NOTE not safe for production environments!! think sql injections.
    """
    exec("msg = " + self.payload, globals(), locals()) 
    
    module_builder_string = ""
    
    if msg["isNative"]:
      module_builder_string += "nn." + msg.name + "("
    
    if msg["isParameter"]:
      in_kv_pair = seek("in_", msg.hyper)
      module_builder_string += in_kv_pair[0] + " = " + in_kv_pair[1] + ", "

      out_kv_pair = seek("out_", msg.hyper)
      module_builder_string += out_kv_pair[0] + " = " + out_kv_pair[1] + ", "

    for hparam in msg.hyper.keys():
      module_builder_string += hparam + " = " + msg.hyper[hparam] + ", "

    module_builder_string = module_builder_string[:-2] + ")"


    exec("obj = " + module_builder_string, globals(), locals())
    return obj
