import pandas as pd
import jsonify
from schemas.gift_schema import GiftSchema
import requests
import json


df = pd.read_excel('Lista de Presentes.xlsx')

df = df.drop(columns=['id'])
df = df.rename(columns= {
   'Descricao': 'description', 'link do anuncio': 'url', 'link da imagem': 'source_img'
})

for idx, i in enumerate(df['description']):
   some = df.iloc[idx].to_dict()

   resquester = requests.post(url="http://127.0.0.1:5000/gifts", json=some)

   print(resquester.status_code)