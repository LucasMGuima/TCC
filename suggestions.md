# Sugestões de correções na parte escrita (TCC)

Este arquivo replica, em Markdown, a descrição do PR aberto para documentar as melhorias sugeridas na parte escrita (LaTeX + bibliografia) do TCC. Serve como checklist local, caso o PR não seja utilizado.

Link do PR (já aberto): https://github.com/LucasMGuima/TCC/pull/4

## Contexto
- Estrutura abnTeX2 está configurada e compila (`Texto/main.pdf`). Introdução e Revisão bem encaminhadas; Desenvolvimento/Resultados/Conclusão ainda carecem de conteúdo substantivo.
- Objetivo: consolidar uma lista clara e acionável de ajustes e melhorias, sem modificar arquivos neste momento.

## 1) Conteúdo obrigatório a completar
- Resumo (PT-BR): incluir problema, objetivo, método, dados, principais resultados (métricas/custo) e conclusão (150–500 palavras). Palavras‑chave separadas por ponto.
- Abstract (EN): espelhar o resumo em inglês com keywords padronizadas.
- Desenvolvimento/Metodologia: datasets (fonte, variáveis, pré-processamento), ambiente/hardware, protocolo de avaliação (holdout/k-fold), métricas usadas (regressão e/ou classificação), hiperparâmetros/versões, como mediram custo computacional (tempo/memória).
- Resultados: tabelas e gráficos com tempos, consumo (se medido), métricas (RMSE/MAE, AUC/Accuracy/F1 etc.), visualizações; análise crítica custo × acurácia.
- Conclusão e Trabalhos Futuros: síntese do melhor equilíbrio custo × acurácia, limitações, próximos passos (ex.: presença‑only, novas famílias/modelos, variáveis ambientais adicionais).

## 2) Correções técnicas no LaTeX
- Trocar “GML” por “GLM” no Objetivo.
- Tabela de complexidade: corrigir “Linearítimica” → “quase linear (n log n)” (ou “Linearítmica” sem acento incorreto).
- Ortografia e digitação ao longo do texto: “senário” → “cenário”, “vairaveis” → “variáveis”, “splien” → “spline”, “proxima” → “próxima”, “dodos” → “dados”, etc.
- Notação matemática:
  - Regressão simples geral: ajustar para `Y_i = \beta_0 + \beta_1 X_i + \epsilon_i` (corrigir `_beta_i`).
  - Revisar definições com índices e vizinhança `N_i` (uso de chaves/colchetes, `max/min`, `{\cdot}_+^q` bem formatado).
  - Padronizar símbolos (x vs x_i; ε_i; β_0/β_1) e negrito para vetores apenas quando necessário.
- Labels e legendas:
  - Evitar acentos/espaços em `\label{}` (ex.: `\label{fig:reg_linear_simples}`) e usar nomes consistentes.
  - Conferir `\legend` e `\caption` conforme ABNT (fonte/autoria indicada onde necessário).
- Preambulo e pacotes:
  - Remover duplicidade de `\usepackage{indentfirst}`.
  - Validar necessidade de `geometry` custom; o abnTeX2 já atende margens ABNT. Se a banca exigir margens específicas, documentar.
- Siglas: revisar/expandir lista (SDM, R, RMSE, AUC, etc.) para todos os termos usados.

## 3) Bibliografia (`Texto/bibliografia.bib`)
- Corrigir campos e chaves:
  - `tite=` → `title=` (tiposDados_sdm).
  - Evitar chaves com hífen em nomes (ex.: `quase-likehood`) e padronizar nomes das entradas.
  - Remover URLs de redirecionamento/trechos “#:~:text”.
- Substituir/fortalecer referências fracas:
  - Big‑O: manter Cormen et al. (já presente) e remover link para imagem/“ml-science.com”.
  - Regressão linear: preferir livros ou artigos acadêmicos (ISLR, Montgomery & Runger, notas universitárias com DOI) no lugar de blogs.
  - “R é mais robusta para dados”: reformular com base em R Core Team ou obras técnicas (ex.: Wood para GAM) sem tom opinativo.
- Tipos de entrada adequados:
  - Usar `@article`, `@book`, `@manual` quando couber, evitando `@misc` para materiais com DOI/ISSN.
- Consistência de citações: revisar que todas as chaves citadas no texto existem e vice‑versa.

## 4) Integração com o sistema (descrever no texto)
- Incluir uma subseção descrevendo a arquitetura implementada: integração Python↔R, cálculo/retorno de métricas, visualizações geradas.
- Capturas de tela essenciais (upload, seleção de modelos, resultados) como figuras no apêndice.
- Procedimento de reprodutibilidade: versões (Python/R/pacotes), comando de execução, parametrizações usadas nos experimentos.

## 5) Formatação e exigências ABNT
- Resumo/Abstract conforme norma; palavras‑chave/keywords separadas por ponto.
- Verificar se é exigida folha de aprovação e ficha catalográfica no curso; se sim, incluir conforme template abnTeX2.
- Conferir resolução das figuras e padronizar legendas (Fonte: ...).

## Observações adicionais
- O PDF `Texto/main.pdf` compila e as imagens citadas existem em `Imgs/`.
- Este documento funciona como checklist local; aplicar as mudanças em PRs separados é recomendado para facilitar a revisão.

## Próximos passos sugeridos (em PRs separados)
1. Correções LaTeX (typos, labels, notação, pacotes) — sem mudanças de conteúdo.
2. Higienização do `.bib` (campos, tipos, fontes) e alinhamento das citações no texto.
3. Preenchimento de Resumo/Abstract com base nos resultados atuais do sistema.
4. Redação da Metodologia/Resultados/Conclusão com tabelas e gráficos padronizados.

