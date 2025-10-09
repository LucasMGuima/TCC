import utils.widgets as wdg
import src.call_model
import streamlit as st
import re
import pandas as pd
import json

modelos_disponiveis = filter(lambda x: ".json" in x,  wdg.contentIn_folder('modelos'))


db_avaliableModels = wdg.creat_multselect(
    modelos_disponiveis,
    'Selecione um ou mais modelo(s) disponivel(is)'
)

if st.button("Cacular Metricas"):
    for avaliableModel in db_avaliableModels:
        model = f"modelos/{avaliableModel}"

        src.call_model.run_teste(model)

    path = "modelos/resp"
    jsons = wdg.contentIn_folder(path)

    st.write("Avaliações")
    for file in jsons:
        if file in db_avaliableModels:
            with open(f"{path}/{file}", 'r') as f:
                data = json.load(f)
                chaves = data[0].keys()

                st.write(file)
                for chave in chaves:
                    st.write(f"{chave}: {data[0][chave]}")
        