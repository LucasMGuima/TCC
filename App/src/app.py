import streamlit as st
import pandas as pd
import os, io
import call_model
import requests

def contentIn_folder(folder: str) -> list|None:
    if os.path.exists(folder) and os.path.isdir(folder):
        return os.listdir(folder)
    else:
        return None

def creat_selectbox(list: list, label: str|None):
    return st.selectbox(label, list)

def creat_multselect(list: list, label: str|None):
    return st.multiselect(label, list)

@st.cache_data
def load_data(file, nrows=100):
    if file is not None:
        if '.csv' in file.name:
            return pd.read_csv(file, nrows=nrows)
        elif '.xlsx' in file.name:
            return pd.read_excel(file, nrows=nrows)
        else:
            return None
    return None

st.title("App")

file = st.file_uploader("Carregar arquivo: ", type=["csv", "xlsx"])

if st.button("Carregar"):
    data = load_data(file)

    if data is not None:
        path = os.path.join("data", file.name)
        with open(path, 'w') as f:
            f.write(data.to_csv())

db_models = creat_selectbox(
    contentIn_folder('models'),
    'Selecione um modelo:'
)
db_data = creat_selectbox(
    contentIn_folder('data'),
    'Selecione um dataset'
)

if db_data:
    path = f"data/{db_data}"
    lst_param = pd.read_csv(path).columns.to_list()
    sb_response = creat_selectbox(
        lst_param,
        'Selecione o parametro de resposta'
    )
    sb_predictor = creat_multselect(
        lst_param,
        'Selecione um ou mais preditores'
    )

if st.button("Rodar"): 
    call_model.run_model(db_data, db_models, sb_response, sb_predictor)
   