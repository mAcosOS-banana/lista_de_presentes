from db.database import db


class Gifts(db.Model):
   gift_id = db.Column(db.Integer, primary_key=True)
   description = db.Column(db.String(300))
   source_img = db.Column(db.Text)
   url = db.Column(db.String(400), nullable= False)
   catched = db.Column(db.Boolean, default = False)

