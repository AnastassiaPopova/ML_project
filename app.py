import sklearn
import streamlit as st
import pickle
import pandas as pd
import numpy as np
import requests
from streamlit_lottie import st_lottie
from PIL import Image

st.set_page_config(page_title="My Webpage", page_icon=":tada:", layout="wide")

with open('model_gr.pickle', 'rb') as handle:
    model = pickle.load(handle)

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_coding = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json")

with st.container():
    left_column, right_column = st.columns(2)
    with left_column:
        st.write("##")
        st.write("[YouTube Channel >]")
    with right_column:
        st_lottie(lottie_coding, height=300, key="coding")

st.title('Рассчитайте стоимость Вашего подержанного автомобиля')
st.write('Для более точного расчета, пожалуйста, введите все характеристики')

year = int(st.text_input("Год выпуска машины", "2015"))
km_driven = st.number_input('Пробег машины (км)')
fuel = st.sidebar.selectbox('Тип топлива', ['Дизель', 'Бензин', 'Другое'])
if fuel == "Бензин":
    fuel_Petrol = 1
    fuel_Others = 0
elif fuel == "Другое":
    fuel_Others = 1
    fuel_Petrol = 0
else:
    fuel_Others = 0
    fuel_Petrol = 0
seats = st.slider("Количество мест", 2, 14)
engine = st.number_input('Объем двигателя (куб.см)')
max_power = st.number_input('Пиковая мощность (л.с.)')
mileage = st.number_input('Расход двигателя (км/л)')
seller_type = st.sidebar.selectbox("Тип продавца", ("Индивидуальный", "Дилер"))
if seller_type == "Индивидуальный":
    seller_type_Individual = 1
else:
    seller_type_Individual = 0
transmission = st.sidebar.selectbox("Коробка передач", ("Механическая", "Автоматическая"))
if transmission == "Механическая":
    transmission_Manual = 1
else:
    transmission_Manual = 0
owner = st.sidebar.selectbox("Первый владелец", ("Да", "Нет"))
if owner == "Нет":
    owner_Second = 1
else:
    owner_Second = 0

def predict():
    row = np.array([year, km_driven, engine, max_power, seats, mileage, \
                   fuel_Others, fuel_Petrol, seller_type_Individual, transmission_Manual, owner_Second])
    prediction = model.predict(row.reshape(1, -1))
    st.write(prediction[0])
    return row

st.button('Рассчитать стоимость', on_click = predict)
