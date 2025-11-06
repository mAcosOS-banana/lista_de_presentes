from dataclasses import dataclass, asdict

@dataclass
class GuestSchema:
   guest_name : str
   

   def to_dict(self):
      return asdict(self)
