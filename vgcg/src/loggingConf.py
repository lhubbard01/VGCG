import logging
from logging import Logger, FileHandler, StreamHandler, Formatter

class CountLogger(Logger):
  def __init__(self, threshold: int, *args, **kwargs):
    super(CountLogger, self).__init__(*args, **kwargs)
    self.thresh = threshold
    self.count = 0

  def info (self, *args, **kwargs):
    super().info(*args, **kwargs)
    self.count+=1
    self.check() 
  
  def debug(self, *args, **kwargs):
    super().info(*args, **kwargs)
    self.count+=1
  
    self.check() 

  def critical(self, *args, **kwargs):
    super().info(*args, **kwargs)
    self.count+=1
    self.check() 

  def check(self):
    if self.count % self.thresh == 0 and self.count != 0 and len(self.handlers) > 0 :
      for handler in self.handlers: 
        if isinstance(handler, FileHandler) :
          handler.emit()


def init_logger(name, count : int = 10):
    
  #useful for a default logging setup 
  #logger                 = CountLogger(threshold = count, name = name)
  logger = logging.getLogger()
  stdout_logging_handler = StreamHandler()
  #stdout_logging_handler = FileHandler("runtime.log", delay = True)
  stdout_logging_fmt     = Formatter(f"{logger.name} %(levelname)s %(asctime)s %(message)s", datefmt="%Y-%m-%dT%H:%M:%sZ")
  stdout_logging_handler.setLevel(logging.INFO)
  stdout_logging_handler.setFormatter(stdout_logging_fmt)
  
  logger.addHandler(stdout_logging_handler)
  return logger
class Prepend:
  def __init__(self, pr):
    self.prepend = pr
  def __call__(self, *args):
    sb = self.pr
    for arg in args:
      sb += str(arg)
    print(sb)

