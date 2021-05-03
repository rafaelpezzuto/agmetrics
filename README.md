# AGMetrics
Calcula métricas topológicas em grafos de genealogia acadêmica.


## Descrição

O AGMetrics calcula 13 métricas topológicas para os vértices de grafos de genealogia acadêmica. A **entrada de dados** é uma lista vértices e arestas de um grafo de genealogia acadêmica. A **saída** é uma lista de métricas para cada vértice do grafo.


## Como usar

Para calcular as métricas para todos os vértices do grafo basta executar:

    python3 calculate_metrics.py

Para calcular as métricas para os vértices avós e seus netos, basta executar:

    python3 grandfather_vs_grandchildren.py

Para calcular a linhagem acadêmica de um vértice, indique seu código (id) no arquivo `config.py` e após, execute:

    python3 lineage.py


## Opções

É preciso indicar no arquivo `config.py` o local do arquivo de vértices, arestas bem como dos arquivos resultantes a serem gerados por este script. Lá também se deve indicar o código ou id do pesquisador que o qual se deseja obter a linhagem acadêmica.


## Métricas genealógicas

As seguintes medidas topológicas de cada vértice são calculadas no sentido ascendente (**-**) e descendente (**+**):

- Descendência (**d-** e **d+**)
- Fecundidade (**fc-** e **fc+**)
- Fertilidade (**ct-** e **ft+**)
- Gerações (**ge**- e **ge+**)
- Índice genealógico (**g**)
- Primos (**c-** e **c+**)
- Relações (**r-** e **r+**)


## Autor

[Rafael J. P. Damaceno](https://rafaelpezzuto.github.io/)
