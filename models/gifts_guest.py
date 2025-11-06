from db.database import db 


class GiftsGuest(db.Model):
   claim_id = db.Column(db.Integer, primary_key= True)
   guest_id = db.Column(db.Integer, db.ForeignKey('guest.guest_id', ondelete="CASCADE"), nullable= False)
   gift_id = db.Column(db.Integer, db.ForeignKey('gifts.gift_id', ondelete= "CASCADE"), unique=True, nullable= False)