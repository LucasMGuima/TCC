# Sistema de Comparação e Avaliação de Modelos de Distribuição de Espécies

## 📋 Descrição

Este projeto implementa um sistema para comparação e avaliação das implementações em R dos algoritmos **GAM** (Generalized Additive Models), **GLM** (Generalized Linear Model) e **MARS** (Multivariate Adaptive Regression Spline) para modelagem de distribuição de espécies.

O sistema foi desenvolvido como parte de um Trabalho de Conclusão de Curso (TCC) do Bacharelado em Ciência da Computação do Centro Universitário Senac - Santo Amaro, com foco na análise de complexidade computacional e acurácia dos modelos.

### 🎯 Objetivos

- **Análise de complexidade e espaço** dos modelos GAM, GLM e MARS
- **Avaliação da acurácia** dos modelos com dados de ocorrência
- **Comparação dos modelos** baseada na relação custo x acurácia
- **Identificação do modelo** com melhor equilíbrio entre performance e custo computacional

## 🏗️ Arquitetura do Sistema

O sistema é composto por:

- **Interface Web (Streamlit)**: Interface amigável para upload de dados e execução de modelos
- **Modelos R**: Scripts R para implementação dos algoritmos GAM, GLM e MARS
- **Integração Python-R**: Sistema de comunicação entre Python e R via subprocess
- **Visualização**: Sistema de plotagem dos resultados dos modelos

## 📁 Estrutura do Projeto

```
TCC/
├── App/                          # Aplicação principal
│   ├── app.py                   # Interface principal do Streamlit
│   ├── requirements.txt         # Dependências Python
│   ├── data/                    # Datasets
│   │   └── pisasci2006.csv      # Dataset de exemplo (PISA 2006)
│   ├── models/                  # Scripts R dos modelos
│   │   ├── gam.r               # Implementação GAM
│   │   ├── glm.r               # Implementação GLM
│   │   └── mars.r              # Implementação MARS
│   ├── pages/                   # Páginas do Streamlit
│   │   ├── upload.py           # Página de upload de dados
│   │   └── testes.py           # Página de testes
│   ├── src/                     # Código fonte Python
│   │   ├── call_model.py       # Execução dos modelos R
│   │   ├── plot_model.py       # Visualização dos resultados
│   │   └── plot_model.r        # Script R para plotagem
│   └── utils/                   # Utilitários
│       └── widgets.py          # Widgets customizados
├── Texto/                       # Documentação do TCC
│   ├── main.tex                # Documento LaTeX principal
│   ├── bibliografia.bib        # Referências bibliográficas
│   └── main.pdf                # PDF do TCC
├── Refs/                       # Referências e literatura
├── Imgs/                       # Imagens e diagramas
└── Manual/                     # Manuais e documentação
```

## 🚀 Instalação

### Pré-requisitos

- **Python 3.8+**
- **R 4.0+**
- **RStudio** (recomendado)

### Dependências Python

```bash
pip install -r App/requirements.txt
```

### Dependências R

Execute no R ou RStudio:

```r
# Instalar pacotes necessários
install.packages(c("mgcv", "mda", "readr"))

# Carregar bibliotecas
library(mgcv)
library(mda)
library(readr)
```

## 🎮 Como Usar

### 1. Executar a Aplicação

```bash
cd App
streamlit run app.py
```

### 2. Interface Principal

A aplicação oferece uma interface web com as seguintes funcionalidades:

- **Seleção de Modelo**: Escolha entre GAM, GLM ou MARS
- **Upload de Dados**: Carregue arquivos CSV ou Excel
- **Configuração de Parâmetros**: 
  - Selecione a variável de resposta
  - Escolha os preditores
- **Execução**: Execute o modelo selecionado
- **Visualização**: Visualize os resultados

### 3. Upload de Dados

Acesse a página de upload para carregar seus próprios datasets:

- Formatos suportados: CSV, Excel
- Estrutura esperada: colunas com variáveis preditoras e uma variável de resposta

### 4. Exemplo de Uso

```python
# Exemplo de execução programática
from src.call_model import run_model

# Executar modelo GAM
resultado = run_model(
    file_name="pisasci2006.csv",
    model="gam.r", 
    response="Overall",
    predictors=["Income", "Health", "Edu"]
)
```

## 📊 Modelos Implementados

### GAM (Generalized Additive Model)
- **Biblioteca**: `mgcv`
- **Características**: Modelos semi-paramétricos com suavização
- **Uso**: Relações não-lineares entre variáveis

### GLM (Generalized Linear Model)
- **Biblioteca**: `stats` (base R)
- **Características**: Extensão dos modelos lineares
- **Uso**: Dados com distribuições não-gaussianas

### MARS (Multivariate Adaptive Regression Spline)
- **Biblioteca**: `mda`
- **Características**: Modelos adaptativos com splines
- **Uso**: Relações complexas e interações entre variáveis

## 🔬 Análise de Complexidade

O projeto inclui análise de complexidade computacional dos algoritmos:

- **Comparação**: Relação custo x avaliação entre os modelos

## 📈 Métricas de Avaliação

- **Acurácia**: Proporção de previsões corretas
- **Precisão**: Proporção de previsões positivas corretas
- **Recall**: Proporção de exemplos positivos identificados
- **F1-Score**: Média harmônica entre precisão e recall

## 🛠️ Desenvolvimento

### Estrutura de Desenvolvimento

1. **Análise Teórica**: Revisão bibliográfica dos modelos
2. **Implementação**: Desenvolvimento dos scripts R
3. **Integração**: Interface Python-R
4. **Testes**: Validação com dados reais
5. **Análise**: Comparação de performance

### Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📚 Referências

- **GAM**: Hastie, T. & Tibshirani, R. (1990). Generalized Additive Models
- **GLM**: Nelder, J. A. & Wedderburn, R. W. M. (1972). Generalized Linear Models
- **MARS**: Friedman, J. H. (1991). Multivariate Adaptive Regression Splines
- **R Language**: R Core Team (2021). R: A Language and Environment for Statistical Computing

## 📄 Licença

Este projeto foi desenvolvido como parte de um Trabalho de Conclusão de Curso (TCC) do Centro Universitário Senac - Santo Amaro.

## 👨‍💻 Autor

**Lucas da Mata Guimarães**
- Bacharelado em Ciência da Computação
- Centro Universitário Senac - Santo Amaro
- Orientador: Afonso Cesar Lelis Brandão

## 📞 Contato

Para dúvidas ou sugestões sobre o projeto, entre em contato através dos canais oficiais da instituição.

---

*Este README foi gerado automaticamente baseado na estrutura do projeto e documentação do TCC.*