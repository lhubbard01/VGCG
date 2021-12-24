class ApiSignalHandler:
  """This class exists to provide an interface between data packets (whose fields are required to contain "signal" keys)
  and the performance of the signals called. """

  def __init__(self, signals: dict):
    """It is the user's responsibility to ensure signals contains callbacks for all keys present at init time. otherwise,
    postpone and loop on add_signal"""
    self.signals = signals
    self.signal_list = list(signals.keys())

  def add_signal(self, signal, callback):
    if signal in self.signal_list:
      raise KeyError(f"Signal {signal} already registered! (try deleting the signal)")
    
    self.signals[signal] = callback
    self.signal_list.append(signal)
  

  def __str__(self):
    sb = "{\n"
    for key in self.signal_list:
      sb += "\t" + key + " : " + self.signals[key].__name__ + "\n"
    sb += "}"
    return sb



  def __repr__(self):
    return str(self.signal_list)
  
  def recv(self, signal, packet):
    """if isinstance(packet, dict):
      signal = packet["signal"]
    else:
      signal = packet.signal
    """


    if signal in self.signal_list:
      self.signals[signal](packet)

    else:
      raise KeyError("unexpected data dictionary!")

