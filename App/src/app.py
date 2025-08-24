import streamlit as st
import pandas as pd

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
file = st.file_uploader("Carregar Arquivo CSV.", type=["csv", "xlsx"])
data = load_data(file)
if data is not None: 
    st.write(data)