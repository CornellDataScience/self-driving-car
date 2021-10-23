class StateFieldRegistry():
  def __init__(self):
    self.fields = {}

  """ Set a single value in the SFR. """
  def set(self, key: str, value):
    self.fields[key] = value

  """ Returns None if [key] is not in SFR """
  def get(self, key: str):
    return self.fields.get(key)

  """ SFR as a dictionary, with keys and values """
  def as_dict(self):
    # a deep copy, use copy() if the dict will never contain compound objects
    return self.fields.deepcopy()
