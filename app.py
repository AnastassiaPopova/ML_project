import sklearn
import streamlit as st
import pickle
import pandas as pd
import numpy as np
import requests
from streamlit_lottie import st_lottie
from PIL import Image

st.set_page_config(page_title="Car's Price Prediction", page_icon=":tada:", layout="wide")
#загружаем модель 
with open('model_gr.pickle', 'rb') as handle:
    model = pickle.load(handle)
#цвета элементов
st.markdown(
    """
<style>
div[data-baseweb="select"]>div {
  background-color: #fff;
  border-color:rgb(244, 108, 11);
}
</style>
""",
    unsafe_allow_html=True,
)
#функция для анимации 
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_coding = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_wkaoqtgc.json")
#Заголовок
with st.container():
    left_column, right_column = st.columns(2)
    with left_column:
        st.write("##")
        st.write("##")
        st.write("##")
        st.title('Рассчитайте стоимость подержанного автомобиля')
        st.write("##")
    with right_column:
        st_lottie(lottie_coding, height=300, key="coding")

#Ввод данных
with st.container():
    st.write("---")
    st.header("Для более точного расчета, пожалуйста, введите все характеристики")
    left_column, right_column = st.columns(2)
    with left_column:
        year = int(st.text_input("Год выпуска машины", "2015"))
        km_driven = st.number_input('Пробег машины (км)')
        engine = st.number_input('Объем двигателя (куб.см)')
        st.write("######")
        max_power = st.number_input('Пиковая мощность (л.с.)')
        mileage = st.number_input('Расход двигателя (км/л)')
    with right_column:
        fuel = st.selectbox('Тип топлива', ['Дизель', 'Бензин', 'Другое'])
        if fuel == "Бензин":
            fuel_Petrol = 1
            fuel_Others = 0
        elif fuel == "Другое":
            fuel_Others = 1
            fuel_Petrol = 0
        else:
            fuel_Others = 0
            fuel_Petrol = 0
        transmission = st.selectbox("Коробка передач", ("Механическая", "Автоматическая"))
        if transmission == "Механическая":
            transmission_Manual = 1
        else:
            transmission_Manual = 0
        seats = st.slider("Количество мест", 2, 14)
        owner = st.selectbox("Первый владелец", ("Да", "Нет"))
        if owner == "Нет":
            owner_Second = 1
        else:
           owner_Second = 0
        seller_type = st.selectbox("Тип продавца", ("Индивидуальный", "Дилер"))
        if seller_type == "Индивидуальный":
            seller_type_Individual = 1
        else:
            seller_type_Individual = 0

#Функция для предсказания
def predict():
    row = np.array([year, km_driven, engine, max_power, seats, mileage, \
                   fuel_Others, fuel_Petrol, seller_type_Individual, transmission_Manual, owner_Second])
    prediction = model.predict(row.reshape(1, -1))
    #st.write(np.exp(prediction)[0])
    st.write(np.exp(prediction)[0])

st.markdown(""" 
<style>
div.stButton > button:first-child {
      background-color: rgb(244, 108, 11); color:white; font-size:20px;height:3em;width:30em;border-radius:10px 10px 10px 10px;
}
<style>""", unsafe_allow_html=True)

#if st.button('Рассчитать стоимость', on_click = predict):
#    st.success('Welcome', np.exp(prediction)[0])
st.button('Рассчитать стоимость', on_click = predict)
 #   st.success('Welcome', predict)
