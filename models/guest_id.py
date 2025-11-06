from db.database import db
from flask_login import UserMixin
class Guest(UserMixin, db.Model):
   guest_id = db.Column(db.Integer(), primary_key=True)
   guest_name = db.Column(db.String(150))

   def get_id(self):
      # o Flask-Login precisa que isso retorne uma string
      return str(self.guest_id)