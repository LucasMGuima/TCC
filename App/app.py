import streamlit as st
import pandas as pd
import src.call_model
import utils.widgets as widgets
import utils.database as database
import io

# Inicia a conexão com o banco
db = database.Conection()
print(f"ID da conexão: {id(db)}")

st.title("App")

db_models = widgets.creat_multselect(
    widgets.contentIn_folder('models'),
    'Selecione um ou mais modelo(s):'
)
db_data = widgets.creat_selectbox(
    database.contentIn_bucket(db, 'dados'),
    'Selecione um dataset'
)

if db_data:
    # Faz o dowload do arquivo
    try:
        response = db.supabase.storage.from_("data").download(f"dados/{db_data}")
    except Exception as e:
        st.error(f"Erro ao baixar o arquivo: {e}")
        st.stop()

    # Convert o objeto de byres 'response' em um fluxo de dados na memória
    bytes_stream = io.BytesIO(response)

    # Passa o fluxo de dados para o pandas
    data = pd.read_csv(bytes_stream, encoding='latin1')
    lst_param = data.columns.to_list()

    sb_response = widgets.creat_selectbox(
        lst_param,
        'Selecione o parametro de resposta'
    )
    sb_predictor = widgets.creat_multselect(
        lst_param,
        'Selecione um ou mais preditores'
    )

if st.button("Rodar"):
    resp = []
    for model in db_models:
        resp.append(src.call_model.run_model(db_data, data, model, sb_response, sb_predictor))
    st.write(resp)