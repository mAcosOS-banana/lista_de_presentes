from typing import *
from flask import jsonify
from dataclasses import dataclass, asdict

@dataclass
class GiftSchema:
   description : str
   source_img : str
   url : str

   def to_dict(self):
      return asdict(self)
