import streamlit as st
import pandas as pd
import src.call_model
import utils.widgets as widgets
import utils.database as database
import io

def contentIn_bucket(folder: str) -> list:
    db = database.Conection()
    print(f"ID da conexão: {id(db)}")

    response = db.supabase.storage.from_("data").list(folder,{
        "limiti": 100,
        "offset": 0,
        "sortBy": {"column": "name", "order": "desc"},
    })

    content = []
    for item in response:
        name = item["name"]
        content.append(name)
    return content

# Inicia a conexão com o banco
db = database.Conection()
print(f"ID da conexão: {id(db)}")

st.title("App")

db_models = widgets.creat_selectbox(
    widgets.contentIn_folder('models'),
    'Selecione um modelo:'
)
db_data = widgets.creat_selectbox(
    contentIn_bucket('dados'),
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
    resp = src.call_model.run_model(db_data, data, db_models, sb_response, sb_predictor)
    st.write(resp)