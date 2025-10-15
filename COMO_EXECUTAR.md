# 🚀 Como Executar o Sistema

## 📋 Pré-requisitos

Antes de executar o sistema, certifique-se de ter:

- **Python 3.8+** instalado
- **R 4.0+** instalado 
- **Rscript** disponível no PATH
- Dependências Python instaladas

## ⚡ Execução Rápida

### 1. Navegue para o diretório do App
```bash
cd /home/afonsolelis/Repositórios/senac/20252_bcc_tcc_lucas/TCC/App
```

### 2. Execute o Streamlit
```bash
streamlit run app.py
```

### 3. Acesse no navegador
O sistema abrirá automaticamente em: `http://localhost:8501`

## 🎯 Como Usar

### Passo 1: Verificar Status
- ✅ Se aparecer "Conectado ao Supabase" → Modo online ativo
- ⚠️ Se aparecer "Executando em modo offline" → Usando dados locais

### Passo 2: Selecionar Modelos
- 🔧 Escolha um ou mais modelos:
  - `gam.r` - Generalized Additive Model
  - `glm.r` - Generalized Linear Model  
  - `mars.r` - Multivariate Adaptive Regression Spline

### Passo 3: Selecionar Dataset
- 📋 Escolha um arquivo CSV da lista
- O sistema mostra automaticamente:
  - 📄 Número de linhas
  - 📊 Número de colunas
  - 🔄 Valores ausentes (NaN)

### Passo 4: Configurar Variáveis
- 🎯 **Variável de Resposta**: A variável que você quer predizer
- ⚙️ **Preditores**: As variáveis que serão usadas para fazer a predição

### Passo 5: Executar
- ▶️ Clique em "Executar Modelos"
- Acompanhe o progresso na barra de status
- Veja os resultados expandindo cada modelo

## 📁 Estrutura de Dados

### Modo Offline (Recomendado para desenvolvimento)
Coloque seus arquivos CSV em:
```
TCC/App/data/dados/arquivo.csv
```

### Dados de Exemplo
O sistema já inclui:
- `pisasci2006.csv` - Dataset de exemplo do PISA 2006

## 🔍 Solução de Problemas

### Erro: "Nenhum modelo encontrado"
**Causa**: Scripts R não estão na pasta `models/`
**Solução**: Verifique se existem os arquivos:
- `models/gam.r`
- `models/glm.r`
- `models/mars.r`
- `models/model_utils.r`

### Erro: "Rscript não encontrado"
**Causa**: R não está instalado ou não está no PATH
**Solução**:
```bash
# Verificar se R está instalado
R --version

# Verificar se Rscript está disponível
which Rscript
```

### Erro: Biblioteca R não encontrada
**Causa**: Pacotes R necessários não estão instalados
**Solução**: Execute no R:
```r
install.packages(c("mgcv", "mda", "readr", "jsonlite"))
```

### Erro de encoding em CSV
**Causa**: Arquivo CSV com caracteres especiais
**Solução**: O sistema tenta automaticamente UTF-8 e Latin1

### Erro: "Coluna não encontrada"
**Causa**: Nome da coluna digitado incorretamente ou coluna não existe
**Solução**: Use exatamente os nomes que aparecem na lista

## 📊 Interpretando os Resultados

### Saída dos Modelos R
Cada modelo retorna:
- **Summary**: Resumo estatístico do modelo
- **Coeficientes**: Valores dos parâmetros estimados  
- **Métricas**: R², p-values, etc.

### Arquivos Gerados
O sistema cria automaticamente:
- `data/train_*.csv` - Dataset de treinamento (80%)
- `data/test_*.csv` - Dataset de teste (20%)
- `modelos/*.rds` - Modelos treinados salvos
- `data/*.json` - Metadados dos modelos

## 🔧 Configurações Avançadas

### Usar com Supabase (Opcional)
1. Edite `.env`:
```env
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_ANON_KEY=sua-chave-anon
```

2. Reinicie a aplicação

### Modificar Proporção de Teste
Edite `src/call_model.py`, linha com `split_data(20, ...)`:
- `20` = 20% para teste, 80% para treino
- Modifique conforme necessário

### Adicionar Novos Modelos
1. Crie novo script R em `models/`
2. Use `models/model_utils.r` para funções auxiliares
3. Siga o padrão dos modelos existentes

## 📈 Exemplo de Uso Completo

1. **Iniciar**: `streamlit run app.py`
2. **Selecionar**: `gam.r` e `glm.r`
3. **Dataset**: `pisasci2006.csv`
4. **Resposta**: `Overall` (pontuação geral)
5. **Preditores**: `Income`, `Health`, `Edu`
6. **Executar**: Clique no botão
7. **Resultados**: Veja outputs do R

## 🆘 Suporte

Se encontrar problemas:
1. Verifique as mensagens de erro na interface
2. Consulte `CORREÇÕES_REALIZADAS.md` para problemas conhecidos
3. Verifique logs no terminal onde executou o Streamlit

---

*Sistema corrigido e funcional em modo offline! 🎉*