import streamlit as st
import pandas as pd
import src.call_model
import utils.widgets as widgets
import utils.database as database
from supabase import Client

# -- TODO --
# Supabase: bucket para salvar os datasets
db_keys = pd.read_csv("keys.csv")
url: str = db_keys['NEXT_PUBLIC_SUPABASE_URL'][0]
key: str = db_keys['NEXT_PUBLIC_SUPABASE_ANON_KEY'][0]

cliente: Client = database.start_conection(url, key)

st.title("App")

db_models = widgets.creat_selectbox(
    widgets.contentIn_folder('models'),
    'Selecione um modelo:'
)
db_data = widgets.creat_selectbox(
    widgets.contentIn_folder('data'),
    'Selecione um dataset'
)

if db_data:
    path = f"data/{db_data}"
    try:
        lst_param = pd.read_csv(path, encoding='latin1').columns.to_list()
    except UnicodeDecodeError:
        # Se falhar, tente uma codificação alternativa
        lst_param = pd.read_csv(path, encoding='ISO-8859-1').columns.to_list()
    except Exception as e:
        # Caso haja outro erro
        st.error(f"Erro ao ler o arquivo CSV: {e}")

    sb_response = widgets.creat_selectbox(
        lst_param,
        'Selecione o parametro de resposta'
    )
    sb_predictor = widgets.creat_multselect(
        lst_param,
        'Selecione um ou mais preditores'
    )

if st.button("Rodar"): 
    resp = src.call_model.run_model(db_data, db_models, sb_response, sb_predictor)
    st.write(resp)