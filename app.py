import streamlit as st
import pickle
import pandas as pd

with open('model_gr.pickle', 'rb') as handle:
    model = pickle.load(handle)

st.title('Предсказание цены подержанного автомобиля')

year = int(st.text_input("Год выпуска машины", "1234"))
km_driven = st.number_input('Пробег машины (км)')
fuel = st.select_slider('Тип топлива', ['Дизель', 'Бензин', 'Другое'])
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
seller_type = st.selectbox("Тип продавца", ("Индивидуальный", "Дилер"))
if seller_type == "Индивидуальный":
    seller_type_Individual = 1
else:
    seller_type_Individual = 0
transmission = st.selectbox("Коробка передач", ("Механическая", "Автоматическая"))
if transmission == "Механическая":
    transmission_Manual = 1
else:
    transmission_Manual = 0
owner = st.selectbox("Первый владелец", ("Да", "Нет"))
if owner == "Нет":
    owner_Second = 1
else:
    owner_Second = 0

def predict():
    row = np.array([year, km_driven, engine, max_power, seats, mileage_kmpl, \
                   fuel_Others, fuel_Petrol, seller_type_Individual, transmission_Manual, owner_Second])
    X = pd.DataFrame([row], columns = columns)
    prediction = model.predict(X)
    st.write(prediction)

st.button('Рассчитать стоимость', on_click = predict)
