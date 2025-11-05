from flask import Flask, request, jsonify
from db.database import db
from models.gifts import Gifts
from models.guest_id import Guest
from schemas.gift_schema import GiftSchema
import pandas as pd


app = Flask(__name__)

app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://marcos:3ut34m01010.@localhost:5432/ldw'

db.init_app(app)
@app.route('/login', methods=['POST'])
def login(): 
   data = request.get_json()

   identifier_number = data.get('number')

   if identifier_number:
      pass

   return jsonify({'message': "Número Invalido"})

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