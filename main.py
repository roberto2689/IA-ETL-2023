from selenium import webdriver

from time import sleep

import pyautogui

import pandas as pd

import requests

import json

import openai

from selenium.webdriver.common.by import By

opts = ChromeOptions()

opts.add_experimental_option("detach", False)

options = webdriver.ChromeOptions()

options.add_experimental_option("useAutomationExtension", False)

options.add_experimental_option("excludeSwitches", ["enable-automation"])

driver = webdriver.Edge()

#ETAPA DE EXTRAÇÃO

df = pd.read_csv("C:\Users\Roberto Barros Filho\Área de Trabalho\Bootcamp_Santander\Projeto ETL\santander-dev-week-2023.csv")

user_ids = df['UserID'].tolist()

print(user_ids)

url = 'https://sdw-2023-prd.up.railway.app/users/1'

def get_user(id):

response = requests.get(f'{url}/users/{id}')

return response.json() if response.status_code == 200 else None
users = [user for id in user_ids if (user := get_user(id)) is not None]

print(json.dumps(users, indent=2))

#ETAPA DE TRANSFORMAÇÃO

INSTAALAR UM BIBLIOTECA
pip install openai
openai_api_key = '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'

openai_api_key = openai_api_key

def generate_ai_news(user):

completion = openai.ChatCompletion.create(

model="gpt-3.5-turbo",

messages=[

{"role": "system", "content": "Você trabalha com markting bancário."},

{"role": "user", "content": f"Crei uma mensagem para {user['name']} sobre a importância dos investimentos (máximo de 100 caracteres)"}

]
)

return completion.choices[0].message.content

for user in users:

news = generate_ai_news(user)

print(news)

user['news'].append({

"icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg",

"description": news
})

ETAPA DE LOAD
def update_user(user):

response = requests.put(f'{url}/users{user[id]}', json=user)

return True if response.status_code == 200 else False
for user in users:

success = update_user(user)

print(f"User {user['name']} update? {success}!")