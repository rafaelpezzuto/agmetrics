# AGMetrics
AGMetrics é um script para calcular 13 métricas topológicas associadas aos vértices de grafos de genealogia acadêmica. 
A **entrada** é um arquivo CSV que contém as arestas do grafo (o seu formato está indicado no arquivo `example/edges.csv`. 
A **saída** é uma tabela de métricas computadas para cada vértice do grafo (o seu formato está indicado no arquivo `example/metrics.csv`.
Segue um exemplo de arquivo de arestas a ser utilizado como entrada:

```
source,target
1,3
2,3
3,4
4,5
4,6
7,8
7,10
```


## Como usar

Para calcular as métricas para todos os vértices de um grafo basta executar: `python3 calculate.py -e <arquivo de arestas>`.
Por exemplo, para o arquivo de arestas `example/edges.csv`, basta executar `python3 calculate.py -e example.edges.csv`; será gerada a saída:

```
node,d+,d-,fc+,fc-,ft+,ft-,c+,c-,g+,g-,r+,r-,g
1,4,0,1,0,1,0,0,1,3,0,4,0,1
2,4,0,1,0,1,0,0,1,3,0,4,0,1
3,3,2,1,2,1,0,0,0,2,1,3,2,1
4,2,3,2,1,0,1,0,0,1,2,2,3,0
5,0,4,0,1,0,1,1,0,0,3,0,4,0
6,0,4,0,1,0,1,1,0,0,3,0,4,0
7,5,0,2,0,2,0,0,0,3,0,6,0,1
8,2,1,1,1,1,0,0,1,2,1,2,1,1
9,1,2,1,1,0,1,1,0,1,2,1,2,0
10,2,1,1,1,1,0,0,1,2,1,2,1,1
11,1,2,1,1,0,1,1,0,1,2,1,2,0
12,0,5,0,2,0,2,0,0,0,3,0,6,0
13,4,0,1,0,1,0,0,2,2,0,4,0,1
14,4,0,1,0,1,0,0,2,2,0,4,0,1
15,4,0,1,0,1,0,0,2,2,0,4,0,1
16,3,3,3,3,0,0,0,0,1,1,3,3,0
17,0,4,0,1,0,1,2,0,0,2,0,4,0
18,0,4,0,1,0,1,2,0,0,2,0,4,0
19,0,4,0,1,0,1,2,0,0,2,0,4,0
20,4,0,3,0,3,0,0,0,2,0,6,0,1
21,1,1,1,1,0,0,0,0,1,1,1,1,0
22,1,1,1,1,0,0,0,0,1,1,1,1,0
23,1,1,1,1,0,0,0,0,1,1,1,1,0
24,0,4,0,3,0,3,0,0,0,2,0,6,0
25,11,0,1,0,1,0,0,3,3,0,17,0,1
26,10,1,4,1,4,0,0,4,2,1,16,1,3
27,9,2,3,1,3,1,3,4,2,2,12,2,3
28,8,3,3,2,2,2,9,4,2,3,9,4,2
29,6,4,3,3,1,3,9,3,2,4,6,7,1
30,3,5,3,4,0,4,9,0,1,5,3,11,0
31,0,4,0,1,0,1,8,0,0,4,0,5,0
32,0,5,0,1,0,1,8,0,0,5,0,8,0
33,0,5,0,1,0,1,8,0,0,5,0,8,0
34,0,6,0,1,0,1,8,0,0,6,0,12,0
35,0,6,0,1,0,1,8,0,0,6,0,12,0
36,0,6,0,1,0,1,8,0,0,6,0,12,0
```


## Métricas genealógicas

As seguintes medidas topológicas de cada vértice são calculadas no sentido ascendente (**-**) e descendente (**+**):

- Descendência (**d+** e **d-**)
- Fecundidade (**fc+** e **fc-**)
- Fertilidade (**ft+** e **ft-**)
- Gerações (**g+**- e **g-**)
- Índice genealógico (**gi**)
- Primos (**c+** e **c-**)
- Relações (**r+** e **r-**)


## Autores

- [Rafael J. P. Damaceno](https://rafaelpezzuto.github.io/)
- [Luciano Rossi](https://rossi-luciano.github.io/homepage/)
- [Jesús Pascual Mecha-Chalco](http://professor.ufabc.edu.br/~jesus.mena/)

