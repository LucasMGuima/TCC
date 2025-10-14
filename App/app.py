import streamlit as st
import pandas as pd
import src.call_model
import utils.widgets as widgets
import utils.database as database
import io
import os
from typing import List

# Configuração da página
st.set_page_config(
    page_title="Sistema de Comparação de Modelos",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Sistema de Comparação de Modelos de Distribuição de Espécies")
st.markdown("---")

# Inicia a conexão com o banco
try:
    db = database.Conection()
    if db.offline_mode:
        st.warning("⚠️  Executando em modo offline. Usando dados locais.")
    else:
        st.success("✅ Conectado ao Supabase")
except Exception as e:
    st.error(f"❌ Erro na conexão: {e}")
    st.stop()

# Seção de Seleção de Modelos
st.header("🤖 Seleção de Modelos")

# Lista os modelos disponíveis
available_models = widgets.contentIn_folder('models')
if not available_models:
    st.error("❌ Nenhum modelo encontrado na pasta 'models'")
    st.stop()

st.info(f"📁 Modelos disponíveis: {', '.join(available_models)}")

db_models = widgets.creat_multselect(
    available_models,
    '🔧 Selecione um ou mais modelo(s):'
)

if not db_models:
    st.warning("⚠️  Selecione pelo menos um modelo para continuar")

# Seção de Seleção de Dados
st.header("🗃️ Seleção de Dados")

try:
    data_list = database.contentIn_bucket(db, 'dados')
    data_disponivel = [x for x in data_list if '.csv' in x.lower()]
    
    if not data_disponivel:
        st.error("❌ Nenhum arquivo CSV encontrado")
        if db.offline_mode:
            st.info("📝 Adicione arquivos CSV na pasta 'data/dados' para usar em modo offline")
        st.stop()
        
    st.info(f"📁 Datasets disponíveis: {len(data_disponivel)} arquivos")
    
    db_data = widgets.creat_selectbox(
        data_disponivel,
        '📋 Selecione um dataset'
    )
except Exception as e:
    st.error(f"❌ Erro ao listar dados: {e}")
    st.stop()

if db_data:
    st.header("⚙️ Parâmetros do Modelo")
    
    # Carrega o dataset
    try:
        if db.offline_mode:
            # Modo offline: carrega do arquivo local
            file_path = os.path.join("data", "dados", db_data)
            if os.path.exists(file_path):
                data = pd.read_csv(file_path, encoding='utf-8')
            else:
                st.error(f"❌ Arquivo não encontrado: {file_path}")
                st.stop()
        else:
            # Modo online: baixa do Supabase
            response = db.supabase.storage.from_("data").download(f"dados/{db_data}")
            bytes_stream = io.BytesIO(response)
            data = pd.read_csv(bytes_stream, encoding='utf-8')
            
    except UnicodeDecodeError:
        # Tenta outros encodings se UTF-8 falhar
        try:
            if db.offline_mode:
                data = pd.read_csv(file_path, encoding='latin1')
            else:
                bytes_stream = io.BytesIO(response)
                data = pd.read_csv(bytes_stream, encoding='latin1')
            st.warning("⚠️  Usando encoding latin1 para o arquivo")
        except Exception as e:
            st.error(f"❌ Erro ao carregar arquivo com diferentes encodings: {e}")
            st.stop()
    except Exception as e:
        st.error(f"❌ Erro ao carregar o arquivo: {e}")
        st.stop()

    # Exibe informações do dataset
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📄 Linhas", len(data))
    with col2:
        st.metric("📊 Colunas", len(data.columns))
    with col3:
        st.metric("🔄 Valores NaN", data.isnull().sum().sum())
    
    # Mostra as primeiras linhas do dataset
    with st.expander("🔍 Visualizar Dataset"):
        st.dataframe(data.head())
    
    lst_param = data.columns.to_list()
    
    col1, col2 = st.columns(2)
    
    with col1:
        sb_response = widgets.creat_selectbox(
            lst_param,
            '🎯 Selecione o parâmetro de resposta (variável dependente)'
        )
        
    with col2:
        # Remove a variável de resposta da lista de preditores
        predictor_options = [col for col in lst_param if col != sb_response] if sb_response else lst_param
        sb_predictor = widgets.creat_multselect(
            predictor_options,
            '⚙️ Selecione um ou mais preditores (variáveis independentes)'
        )
    
    # Validações
    if sb_response and sb_predictor:
        missing_data_response = data[sb_response].isnull().sum()
        if missing_data_response > 0:
            st.warning(f"⚠️  A variável de resposta '{sb_response}' tem {missing_data_response} valores ausentes")
        
        missing_predictors = {col: data[col].isnull().sum() for col in sb_predictor if data[col].isnull().sum() > 0}
        if missing_predictors:
            st.warning(f"⚠️  Preditores com valores ausentes: {missing_predictors}")

# Execução dos Modelos
st.header("▶️ Execução dos Modelos")

# Verifica se todos os parâmetros necessários foram selecionados
can_run = bool(db_data and db_models and 'sb_response' in locals() and sb_response and 'sb_predictor' in locals() and sb_predictor)

if not can_run:
    st.info("📝 Para executar os modelos, certifique-se de que:")
    checks = [
        ("✓" if db_data else "❌", "Dataset selecionado"),
        ("✓" if db_models else "❌", "Modelo(s) selecionado(s)"),
        ("✓" if 'sb_response' in locals() and sb_response else "❌", "Variável de resposta selecionada"),
        ("✓" if 'sb_predictor' in locals() and sb_predictor else "❌", "Preditor(es) selecionado(s)")
    ]
    
    for check, desc in checks:
        st.write(f"{check} {desc}")
else:
    # Mostra resumo da configuração
    st.info(f"""
    📋 **Configuração:**
    - Dataset: {db_data}
    - Modelos: {', '.join(db_models)}
    - Resposta: {sb_response}
    - Preditores: {', '.join(sb_predictor)}
    """)
    
    if st.button("▶️ Executar Modelos", type="primary"):
        try:
            progress_bar = st.progress(0)
            status_text = st.empty()
            results = []
            
            for i, model in enumerate(db_models):
                status_text.text(f'🔄 Executando modelo: {model}...')
                progress_bar.progress((i) / len(db_models))
                
                try:
                    result = src.call_model.run_model(db_data, data, model, sb_response, sb_predictor)
                    results.append({
                        'modelo': model,
                        'status': '✅ Sucesso',
                        'resultado': result
                    })
                    st.success(f'✅ {model} executado com sucesso!')
                except Exception as e:
                    results.append({
                        'modelo': model,
                        'status': f'❌ Erro: {str(e)}',
                        'resultado': None
                    })
                    st.error(f'❌ Erro ao executar {model}: {str(e)}')
            
            progress_bar.progress(1.0)
            status_text.text('✅ Execução concluída!')
            
            # Exibe resultados
            st.header("📈 Resultados")
            
            for result in results:
                with st.expander(f"{result['modelo']} - {result['status']}"):
                    if result['resultado']:
                        st.code(result['resultado'], language='r')
                    else:
                        st.write("Nenhum resultado disponível devido a erro na execução.")
                        
        except Exception as e:
            st.error(f'❌ Erro geral durante a execução: {str(e)}')
