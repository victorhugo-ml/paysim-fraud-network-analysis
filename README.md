# PaySim — análise de fraude com grafos

[![CI](https://github.com/victorhugo-ml/paysim-fraud-network-analysis/actions/workflows/ci.yml/badge.svg)](https://github.com/victorhugo-ml/paysim-fraud-network-analysis/actions/workflows/ci.yml)

Projeto exploratório de estudo com transações financeiras sintéticas, desenvolvido para praticar **DuckDB/SQL**, **Pandas**, **NumPy**, visualizações em **Matplotlib** e grafos direcionados com **NetworkX**.

Desenvolvido como projeto da disciplina **Comunicação e Redes**
(BCM0506-15) do Bacharelado em Ciência e Tecnologia da UFABC, em 2026, e
apresentado ao professor em vídeo. A ementa da disciplina cobre redes
complexas, teoria dos grafos e propriedades estruturais de redes — o que
explica por que a análise é conduzida como um problema de grafo e não como
um problema tabular.

Este repositório registra meu processo de aprendizado. Ele não apresenta um sistema antifraude pronto: o objetivo é formular uma pergunta, construir uma amostra que permita estudar a rede e interpretar os resultados sem esconder as limitações.

O projeto investiga a seguinte pergunta:

> A estrutura de uma rede de transações financeiras permite identificar padrões associados às fraudes selecionadas?

[Abrir o notebook executado](notebooks/paysim_fraud_network_analysis.ipynb)

O notebook foi organizado para ser lido de cima para baixo. Os laços, filtros e etapas da amostragem foram mantidos visíveis, com comentários em linguagem direta, para que cada decisão possa ser acompanhada e explicada.

## Visão geral

O dataset PaySim possui milhões de transações. Para manter a análise leve e visualmente explorável, o notebook constrói uma amostra de exatamente **1.000 transações**.

Uma amostra aleatória pequena poderia eliminar recorrências, caminhos e hubs relevantes. Por isso, a seleção é orientada à estrutura da rede e combina:

- 25 fraudes distribuídas no tempo;
- contas que aparecem como origem e destino;
- hubs de recebimento;
- vizinhanças das contas selecionadas;
- transações normais para completar a amostra.

O **DuckDB** consulta o CSV completo com SQL sem carregá-lo integralmente em um DataFrame. Depois da amostragem, **Pandas** organiza os dados, **NumPy** apoia os cálculos numéricos, **NetworkX** modela a rede e **Matplotlib** produz as visualizações da análise.

```text
PaySim completo
      |
      v
DuckDB + SQL
      |
      v
Amostragem estrutural (1.000 transações)
      |
      +--> Pandas + NumPy / análise exploratória
      |
      +--> NetworkX / métricas e subgrafos
      |
      +--> Matplotlib / visualizações
      |
      v
Resultados e exportação para Gephi
```

## Principais resultados

| Indicador | Resultado |
| --- | ---: |
| Transações analisadas | 1.000 |
| Períodos (`steps`) representados | 318 |
| Fraudes selecionadas | 25 |
| Nós | 1.780 |
| Arestas agregadas | 1.000 |
| Densidade | 0,000316 |
| Maior componente fracamente conexa | 19 nós |
| Reciprocidade | 0 |
| Clustering médio | 0 |
| Maior k-core | 1 |

Na amostra executada:

- os 50 nós associados às fraudes selecionadas tiveram **in-degree médio de 1,88**, ante **0,52** nos demais nós;
- o PageRank médio desses nós foi **0,000985**, ante **0,000550** nos demais;
- o valor mediano das transações fraudulentas foi **722.832,95**, ante **101.598,47** nas transações normais;
- a conta de origem terminou com saldo zero em **100%** das fraudes selecionadas, contra **24,00%** das demais transações.

Essas diferenças são **exploratórias**. Elas não representam a população do PaySim e não demonstram capacidade preditiva.

O diagnóstico registrou **2 origens recorrentes**, **3 contas com entrada e saída** e **25 sequências direcionadas potenciais de duas arestas**. A seleção preservou algumas conexões, mas a rede permaneceu muito esparsa. Esses números não comprovam superioridade em relação a uma amostra aleatória nem garantem caminhos temporalmente válidos.

O indicador de saldo considera uma origem com saldo inicial positivo que terminou em zero. Ele usa informação posterior à transação: em um modelo destinado a decidir antes de sua conclusão, seu uso representaria risco de vazamento temporal. Aqui, ele é usado apenas na análise retrospectiva da amostra.

## Visualizações

<table>
  <tr>
    <td align="center">
      <img src="docs/images/fraudes-por-tipo.png" alt="Participação de fraudes por tipo de transação"><br>
      <sub>Fraudes selecionadas por tipo de transação</sub>
    </td>
    <td align="center">
      <img src="docs/images/subgrafo-fraudes.png" alt="Subgrafo das fraudes selecionadas"><br>
      <sub>Subgrafo das fraudes e suas vizinhanças</sub>
    </td>
  </tr>
  <tr>
    <td align="center">
      <img src="docs/images/maior-componente.png" alt="Maior componente da rede"><br>
      <sub>Maior componente fracamente conexa</sub>
    </td>
    <td align="center">
      <img src="docs/images/correlacao-metricas.png" alt="Correlação de Spearman entre métricas"><br>
      <sub>Correlação de Spearman entre métricas</sub>
    </td>
  </tr>
</table>

## Métricas estudadas

- in-degree e out-degree;
- PageRank topológico e ponderado por valor;
- betweenness centrality;
- densidade, grau médio e reciprocidade;
- componentes fracas e fortes;
- clustering e k-core;
- assortatividade;
- correlação de Spearman entre centralidades e fluxos financeiros.

O notebook usa um `MultiDiGraph` para preservar transações individuais e um `DiGraph` agregado para analisar relações entre contas.

## Limitações metodológicas

A amostra foi construída deliberadamente para preservar fraudes e estruturas interessantes. Portanto:

- a proporção de fraude não estima a prevalência real;
- diferenças entre grupos não sustentam inferência causal;
- a estratégia de amostragem influencia as propriedades do grafo;
- o projeto não treina nem avalia um classificador de fraude;
- centralidade não deve ser interpretada como evidência de comportamento fraudulento.

A principal conclusão metodológica é que, em redes grandes, **a estratégia de amostragem faz parte do problema analítico**.

## Como executar

Requisitos: Python 3.11 ou superior e Jupyter.

```bash
python -m venv .venv
```

Ative o ambiente virtual e instale as dependências:

```bash
pip install -r requirements.txt
jupyter lab
```

Abra `notebooks/paysim_fraud_network_analysis.ipynb` e execute as células em ordem. O notebook baixa o PaySim por meio do `kagglehub`; o CSV não é versionado neste repositório.

### Alcance da validação

Execute `python scripts/validate_notebook.py` para verificar estrutura, sintaxe, ausência de erros salvos e arquivos de visualização. Essa é a mesma validação estática executada pela CI; ela **não baixa o dataset nem executa as células**, e não garante os resultados analíticos.

O `requirements.txt` documenta faixas de versões compatíveis, não um ambiente com todas as versões fixadas. O notebook registra parte das versões da execução salva. Para confirmar a reprodução dos resultados, é necessário executar a análise completa no ambiente escolhido.

## Estrutura

```text
.
├── notebooks/
│   └── paysim_fraud_network_analysis.ipynb
├── docs/
│   └── images/
├── scripts/
│   └── validate_notebook.py
├── DATASET.md
├── requirements.txt
└── README.md
```

## Dataset e atribuição

O PaySim é um dataset sintético gerado por um simulador de transações de mobile money. O dataset não está incluído no repositório.

- [Dataset no Kaggle](https://www.kaggle.com/datasets/ealaxi/paysim1)
- [Projeto original PaySim](https://github.com/EdgarLopezPhD/PaySim)
- E. A. Lopez-Rojas, A. Elmir e S. Axelsson. *PaySim: A financial mobile money simulator for fraud detection*. EMSS, 2016.

Consulte [`DATASET.md`](DATASET.md) para detalhes de uso e atribuição.
