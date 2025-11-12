from flask import Flask, request, jsonify, render_template
from db.database import db
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from flask_cors import CORS
from models.gifts import Gifts
from models.guest_id import Guest
from models.gifts_guest import GiftsGuest
from schemas.gift_schema import GiftSchema
from schemas.guests_schema import GuestSchema
import os
#from dotenv import load_dotenv


#load_dotenv()


app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")

    
db.init_app(app)




login_manager = LoginManager()
login_manager.init_app(app)


CORS(app,
     supports_credentials=True,
     resources={
         r"/*": {
             "origins": [
                "https://hortinbox.com.br",
                "https://www.hortinbox.com.br",
                "https://gift.hortinbox.com.br",
                "http://127.0.0.1:8080"
             ]
         }
     })


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

   return jsonify({'message': "Convidado não existe"}), 404

@app.route('/logout', methods=['GET'])
@login_required
def logout():
   logout_user()
   return jsonify({"message": "Logout succefully done"})

@app.route("/gifts", methods=['POST'])
@login_required
def create_git():
   data = request.get_json()
   gift_data = GiftSchema(**data)
   gift = Gifts(**gift_data.to_dict())
   db.session.add(gift)
   db.session.commit()
   return jsonify(gift_data.to_dict()) , 201


@app.route("/gifts", methods=["GET"])
@login_required
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

@app.route('/getGift/<int:gift_id>', methods=['PUT'])
@login_required
def catch_gift(gift_id):
   data = request.get_json()
   gift = Gifts.query.get(gift_id)

   if not gift:
      return jsonify({'message': 'Presente não existe'}), 404

   # Obtém o guest_id do JSON ou da sessão (melhor via current_user)
   guest_id = current_user.guest_id

   if not guest_id:
      return jsonify({'message': 'Campo "guest_id" é obrigatório.'}), 400

   # Verifica se já está pego
   existing_claim = GiftsGuest.query.filter_by(gift_id=gift_id).first()
   if existing_claim:
      return jsonify({'message': 'Presente já foi pego.'}), 409

   # Cria o relacionamento (claim)
   claim = GiftsGuest(gift_id=gift_id, guest_id=guest_id)
   db.session.add(claim)

   # Atualiza o estado do presente
   gift.catched = True

   db.session.commit()

   return jsonify({
      'message': 'Presente pego com sucesso!',
      'gift_id': gift_id,
      'guest_id': guest_id
   }), 200



@login_required
@app.route('/getGift/<int:gift_id>', methods=['GET'])
def get_gift(gift_id):
    gift = Gifts.query.get(gift_id)
    if not gift:
        return jsonify({'message': 'Presente não existe'}), 404

    return jsonify({
        'id': gift.gift_id,
        'description': gift.description,
        'url': gift.url,
        'source_img': gift.source_img,
        'catched': gift.catched
    }), 200

@app.route('/getGift/<int:gift_id>', methods=['DELETE'])
@login_required
def uncatch_gift(gift_id):
    # verifica se o presente existe
    gift = Gifts.query.get(gift_id)
    if not gift:
        return jsonify({'message': 'Presente não existe'}), 404

    # procura o relacionamento (claim) com o usuário logado
    claim = GiftsGuest.query.filter_by(
        gift_id=gift_id,
        guest_id=current_user.guest_id
    ).first()

    if not claim:
        return jsonify({'message': 'Você não possui este presente'}), 403

    # remove o claim e atualiza o presente
    db.session.delete(claim)
    gift.catched = False
    db.session.commit()

    return jsonify({
        'message': 'Presente liberado com sucesso!',
        'gift_id': gift_id,
        'guest_id': current_user.guest_id
    }), 200

@app.route('/me/gifts', methods=['GET'])
@login_required
def get_my_gifts():
    """Retorna todos os presentes que o current_user pegou"""
    gifts = (
        db.session.query(Gifts)
        .join(GiftsGuest, Gifts.gift_id == GiftsGuest.gift_id)
        .filter(GiftsGuest.guest_id == current_user.guest_id)
        .all()
    )

    result = [
        {
            'gift_id': gift.gift_id,
            'description': gift.description,
            'url': gift.url,
            'source_img': gift.source_img,
            'catched': True,
            'claimed_by': current_user.guest_id
        }
        for gift in gifts
    ]

    return jsonify(result), 200


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/meus-presentes')
@login_required
def my_gifts_page():
    return render_template('mygifts.html')



@app.route('/health')
def health():
    return {"status": "ok"}, 200



if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

