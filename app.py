from flask import Flask, request, jsonify
from db.database import db
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from models.gifts import Gifts
from models.guest_id import Guest
from schemas.gift_schema import GiftSchema
from schemas.guests_schema import GuestSchema

app = Flask(__name__)

app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://marcos:3ut34m01010.@localhost:5432/ldw'

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/createUser', methods=['POST'])
def create_user():
   data = request.get_json()
   guest_data = GuestSchema(**data) 
   guest = Guest(**guest_data.to_dict())
   db.session.add(guest)
   db.session.commit()
   return jsonify(guest_data.to_dict()), 201

login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(guest_id):
   return Guest.query.get(int(guest_id))


@app.route('/login', methods=['POST'])
def login(): 
   data = request.get_json()

   identifier_number = int(data.get('guest_id'))

   if identifier_number:
      qguest = Guest.query.filter_by(guest_id=identifier_number).first()

      if qguest and qguest.guest_id == identifier_number: 
         login_user(qguest)
         return jsonify({'message': 'Login has succefully done'}), 200

   return jsonify({'message': "Convidado não existe"}), 401

@app.route('/logout', methods=['GET'])
@login_required
def logout():
   logout_user()
   return jsonify({"message": "Logout succefully done"})

@app.route("/gifts", methods=['POST'])
def create_git():
   data = request.get_json()
   gift_data = GiftSchema(**data)
   gift = Gifts(**gift_data.to_dict())
   db.session.add(gift)
   db.session.commit()
   return jsonify(gift_data.to_dict()) , 201


@app.route("/gifts", methods=["GET"])
def get_gifts():
   gifts = Gifts.query.filter(Gifts.catched.is_(False) | Gifts.catched.is_(None)).all()

   result = [
      {
         "gift_id": gift.gift_id,
         "description": gift.description,
         "source_img": gift.source_img,
         "url": gift.url,
         "catched": gift.catched
      }
      for gift in gifts
   ]
   
   return jsonify(result), 200

if __name__ == "__main__":
   app.run(debug=True)