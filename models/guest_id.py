from db.database import db

class Guest(db.Model):
   guest_id = db.Column(db.Integer(), primary_key=True)
   guest_name = db.Column(db.String(150))