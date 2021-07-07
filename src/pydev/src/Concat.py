import torch
import torch.nn as nn
class Intermediate(nn.Module):
  """concatenate many input tensors from different computational paths to single tensor"""
  def __init__(self, from_size, target_size):
    super(Intermediate, self).__init__()
    assert sum(from_size) == target_size

  def forward(self, *args):
    cat_tensor = torch.cat(*args, dim = 1)
    return cat_tensor
  
