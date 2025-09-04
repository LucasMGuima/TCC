import utils.widgets as wdg
import src.plot_model
import streamlit as st

db_avaliableModels = wdg.creat_selectbox(
    wdg.contentIn_folder('modelos'),
    'Selecione um modelo disponivel'
)

if st.button("Plot"):
   resp = src.plot_model.plot(db_avaliableModels)
   st.write(resp)