import streamlit as st
import pandas as pd
from PIL import Image
import numpy as np
import joblib
from bokeh.models.widgets import Div
import streamlit.components.v1 as components
import webbrowser

#image = Image.open("copadosdados-main/logo.png")
#st.image(image)

#with open("style.css") as f:
#  st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

url = 'https://copadomundofifa.herokuapp.com'

if st.button('Página Inicial'):
    webbrowser.open_new_tab(url)

def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://static.vecteezy.com/ti/vetor-gratis/p3/3207377-futebol-padrao-para-banner-campeonato-de-futebol-2022-no-qatar-gratis-vetor.jpg");
             background-attachment: fixed;
             background-size: cover;
             opacity: 0.8;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url()


st.markdown("<h1 style='color:#fff;'> Copa do Mundo da FIFA 2022 </h1>", unsafe_allow_html=True)

st.markdown("<p style='color:#fff;'>Algoritmo de Machine Learning capaz de predizer confrontos da Copa do Mundo no Qatar</p>", unsafe_allow_html=True)

df_selecoes = pd.read_csv("Selecoes2022.csv")

todas_selecoes = sorted(df_selecoes['Selecoes'].unique())

selecionar_primeira_selecao = st.selectbox('Primeira Seleção (home)', todas_selecoes)

selecao_b = df_selecoes[df_selecoes['Selecoes'] != selecionar_primeira_selecao]
selecionar_segunda_selecao = st.selectbox('Segunda Seleção (away)', selecao_b)

model = joblib.load('model.pkl')


nome_time = { 'France': 0, 'Mexico': 1, 'USA': 2, 'Belgium': 3, 'Yugoslavia': 4, 'Brazil': 5, 'Romania': 6, 'Peru': 7, 'Argentina': 8,
            'Chile': 9, 'Bolivia': 10, 'Paraguay': 11, 'Uruguay': 12, 'Austria': 13,'Hungary': 14, 'Egypt': 15, 'Switzerland': 16, 'Netherlands': 17,
            'Sweden': 18, 'Germany': 19, 'Spain': 20, 'Italy': 21, 'Czechoslovakia': 22, 'Dutch East Indies': 23, 'Cuba': 24, 'Norway': 25,
            'Poland': 26, 'England': 27, 'Scotland': 28, 'Turkey': 29, 'South Korea': 30, 'Soviet Union': 31, 'Wales': 32, 'Northern Ireland': 33,
            'Colombia': 34, 'Bulgaria': 35, 'North Korea': 36, 'Portugal': 37, 'Israel': 38, 'Morocco': 39, 'El Salvador': 40, 'German DR': 41,
            'Australia': 42, 'Zaire': 43, 'Haiti': 44, 'Tunisia': 45, 'IR Iran': 46, 'Iran': 47, 'Cameroon': 48, 'New Zealand': 49, 'Algeria': 50,
            'Honduras': 51, 'Kuwait': 52, 'Canada': 53, 'Iraq': 54, 'Denmark': 55, 'United Arab Emirates': 56, 'Costa Rica': 57, 'Republic of Ireland': 58,
            'Saudi Arabia': 59, 'Russia': 60,   'Greece': 61,   'Nigeria': 62,  'South Africa': 63, 'Japan': 64,    'Jamaica': 65,  'Croatia': 66,
            'Senegal': 67, 'Slovenia': 68, 'Ecuador': 69, 'China': 70, 'Trinidad and Tobago': 71, "Côte d'Ivoire": 72, 'Serbia and Montenegro': 73,
            'Angola': 74,  'Czech Republic': 75, 'Ghana': 76, 'Togo': 77, 'Ukraine': 78, 'Serbia': 79, 'Slovakia': 80, 'rBosnia and Herzegovina': 81,
            'Iceland': 82,'Panama': 83, 'Qatar': 84 } 

df_campeoes = pd.read_csv("Campeoes.csv")
campeoes = df_campeoes['Vencedor'].value_counts()

def predicao(timeA, timeB):
  idA = nome_time[timeA]
  idB = nome_time[timeB]
  campeaoA = campeoes.get(timeA) if campeoes.get(timeA) != None else 0
  campeaoB = campeoes.get(timeB) if campeoes.get(timeB) != None else 0

  x = np.array([idA, idB, campeaoA, campeaoB]).astype('float64')
  x = np.reshape(x, (1,-1))
  _y = model.predict_proba(x)[0]

  text = ('Chance de ' +timeA+' vencer '+timeB+' é {}\nChance de '+timeB+' vencer '+timeA+' é {}\nChance de '+timeA+' e '+timeB+' empatar é {}').format(_y[1]*100,_y[2]*100,_y[0]*100)
  return _y[0], text

prob1, text1 = predicao(selecionar_primeira_selecao, selecionar_segunda_selecao)

if st.button('Realizar predição do jogo'):
    st.text(text1)