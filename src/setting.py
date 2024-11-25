

# This is the basic data model for keeping track of users and their assigned nicknames
class setting:
  def __init__(self, administrative_features:bool = False, rude_features:bool = False) -> None:
    self.administrative_features = administrative_features
    self.rude_features = rude_features
