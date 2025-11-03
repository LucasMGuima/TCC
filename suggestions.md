# Revisão – Semana 45 (para o Lucas)

> Revisor sugerido: @LucasMGuima

Olá Lucas, segue o consolidado da revisão desta semana. A ideia é usá-lo como texto do PR.

## 1. Lacunas de conteúdo que impedem a entrega
- `Texto/main.tex:205-220`: **Resumo** e **Abstract** ainda estão com texto fictício; é necessário inserir síntese (problema, objetivo, dados, método, principais resultados) e palavras‑chave/keywords formatadas segundo ABNT.
- `Texto/main.tex:332-350`: Objetivo geral não menciona dataset, ambiente experimental nem critérios de comparação; completar com recorte, hipóteses e métricas utilizadas.
- `Texto/main.tex:1164-1219`: Capítulo **Desenvolvimento** inteiro está como esqueleto. Detalhar arquitetura (diagrama), fluxo da aplicação, integração Python↔R, preparação de dados, lógica de treinamento, persistência e tratamento de falhas de rede.
- `Texto/main.tex:1224`: Capítulo **Resultados** vazio; incluir tabelas/gráficos com métricas (acurácia/precisão ou regressão), tempos de treino, uso de memória/CPU, interpretação do custo × qualidade.
- `Texto/main.tex:1229-1231`: **Conclusão** e **Trabalhos Futuros** ausentes; consolidar achados, limitações, próximos passos (ex.: incluir métricas adicionais, novos datasets, otimização de hardware).

## 2. Erros conceituais e técnicos
- `Texto/main.tex:556-558`: Definições da matriz de confusão estão invertidas (falsos positivos/negativos). Corrigir para “negativos classificados como positivos” e “positivos classificados como negativos”.
- `Texto/main.tex:594`: Fórmula de total de previsões usa “Falsos Verdadeiros”; substituir por “Falsos Positivos”.
- `Texto/main.tex:333-335` e `Texto/main.tex:627-628`: Bibliotecas citadas estão trocadas — `mgcv` implementa GAM, `mda` fornece MARS e FDA, e `GLM` está no pacote base `stats`.
- `Texto/main.tex:575-578`: Argumento de que se “aceita o erro de falso negativo” conflita com a priorização de precisão; revisar justificativa e alinhar com a métrica escolhida.
- `Texto/main.tex:1101-1106`: Descrição dos packages repete equívoco sobre quais modelos cada biblioteca oferece; reforçar citações oficiais (`?mgcv`, Wood 2017) e explicar por que escolher duas bibliotecas em vez de usar apenas `mgcv`.

## 3. Ajustes de escrita e estilo
- Revisar ortografia recorrente: `cápitulo`, `sera`, `preocesso`, `possiveis`, `utilzadas`, `perca`, `oque`, `pos`, `occorrencia`, `éspecia`, `exempols`, `quantos`, etc. (ex.: `Texto/main.tex:1166`, `Texto/main.tex:1202`, `Texto/main.tex:576-578`, `Texto/main.tex:597-599`).
- Padronizar acentuação e cedilha nas seções e legendas (ex.: `\section{Recursos tecnologicos}` → `Recursos tecnológicos`).
- Completar legendas de figuras/tabelas com fonte e descrição interpretativa; checar se `\legend{}` atende ao formato exigido pela banca.
- Inserir período final em frases quebradas por linhas (ex.: `Texto/main.tex:335-336`).
- Verificar consistência de termos e siglas (SDM plural, ML grafado por extenso antes da sigla, etc.).

## 4. Metodologia e reprodutibilidade
- Documentar dataset utilizado: origem (fonte oficial/DOI), número de ocorrências/ausências, variáveis ambientais, recorte temporal, tratamentos aplicados. Se dados forem próprios, disponibilizar anexo ou repositório.
- Registrar configuração de experimentos: hardware (CPU/GPU, RAM), versões de Python/R e pacotes (`requirements.txt`/`renv.lock`), semente aleatória e protocolo de validação (k-fold, holdout).
- Evidenciar passo a passo de geração dos resultados (scripts executados, comandos, parâmetros da interface Streamlit). Ideal registrar no capítulo Desenvolvimento e/ou apêndice.

## 5. Bibliografia
- Revisar entradas `bibliografia.bib` (ex.: `tiposDados_sdm` está com `tite=`; chaves com hífen como `quase-likehood`; URLs de redirecionamento). Use tipos de entrada adequados (`@article`, `@book`, `@manual`).
- Substituir referências frágeis (blogs, sites sem curadoria acadêmica) por livros/artigos canônicos: Cormen para análise de algoritmos, Wood para GAM, Hastie & Tibshirani para GLM/GAM, Friedman para MARS.
- Garantir correspondência 1:1 entre citações no texto e entradas no `.bib`; remover chaves não utilizadas.
