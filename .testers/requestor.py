import pandas as pd
import jsonify
from schemas.gift_schema import GiftSchema
from schemas.guests_schema import GuestSchema
import requests
import json


df = pd.read_excel('Lista de Presentes.xlsx', sheet_name="Convidados")

df = df.rename(columns= {
   'Convidados': 'guest_name'
})

for idx, i in enumerate(df['guest_name']):
   some = df.iloc[idx].to_dict()

   resquester = requests.post(url="http://127.0.0.1:5000/createUser", json=some)

   print(resquester.status_code)