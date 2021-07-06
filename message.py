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
      module_builder_string += "nn." + name + "("

    if msg["isParameter"]:
      
      in_key = str(list(msg.hyper.keys()))
      module_builder_string += in_key + " = " + msg.hyper[in_key] + ", "
      out_key = str(list(msg.hyper.keys()))
      module_builder_string += out_key + " = " + msg.hyper[out_key] + ", "

    for hparam in msg.hyper:
      module_builder_string += hparam + " = " + msg.hyper[hparam] + ", "

    module_builder_string = module_builder_string[:-2] + ")"
    exec("obj = " + module_builder_string, globals(), locals())

    return obj
