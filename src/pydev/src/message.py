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

  def proc(self):
    """The payload comes in as a string of some mapping, following some
    specification of data organization. 
    This is used to write a dictionary from this string through concatenating 
    assignment statement with the string dict, and using that dictionary as python native
    after the execution of that statement. The object is then constructed from
    these parameters NOTE not safe for production environments!! think sql injections.
    """
    
    exec("self.as_dict = " + self.payload, globals(), locals())
    return self.as_dict

