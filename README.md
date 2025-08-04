# Tech Challenge Fase 2

**IA para Devs — Pos Tech**  
Instituição: FIAP
Ano: 2025

**Integrantes do Grupo:**  
Erick Bognar, Alexsander Maia Simas, Leonardo Guedes, Ruâni Filipe, Talita Hipolito

---

## Descrição

Este projeto tem como objetivo projetar e implementar um sistema baseado em **Algoritmos Genéticos** capaz de **otimizar a escalação de jogadores de futebol** para formar um time ideal, com base em parâmetros definidos pelo usuário.

O sistema simula a evolução de formações, utilizando operadores genéticos (seleção, crossover e mutação) para encontrar a combinação mais eficiente de jogadores.

---

## Índice

- [📚 Descrição](#-descrição)
- [❓ Problema de Pesquisa](#-problema-de-pesquisa)
- [🧠 Abordagem e Metodologia](#-abordagem-e-metodologia)
- [🛠 Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [📊 Resultados](#-resultados)
- [📌 Conclusões](#-conclusões)

---

## Problema de Pesquisa

Selecionar jogadores para compor uma equipe envolve restrições de posição, desempenho, e equilíbrio entre setores (defesa, meio e ataque). O problema é tratar essa escolha como um processo de **otimização**.

> Como formar automaticamente uma equipe com 11 jogadores, respeitando a estrutura tática 4-4-2 e maximizando o desempenho total da equipe?

---

## Abordagem e Metodologia

A metodologia aplicada envolve:

- Uso de um **dataset de jogadores de futebol da plataforma Kaggle** (disponível em: https://www.kaggle.com/code/rahulanand18bce0953/dv-project)
- Pré-processamento dos dados com `pandas`
- Representação de cada time como um **indivíduo** com 11 jogadores únicos
- **Função de avaliação (fitness)** que soma os ratings e penaliza formações que não respeitam a estrutura 4-4-2
- **Algoritmo Genético com:**
  - Seleção por torneio
  - Cruzamento com ponto de corte aleatório
  - Mutação com taxa de 5%
  - Substituição elitista para próxima geração

---

## Tecnologias Utilizadas

- Python 3.11+
- pandas
- numpy
- seaborn / matplotlib
- Jupyter Notebook

---

## Resultados

O algoritmo foi executado por **100 gerações**, com uma população de **100 equipes**. A cada geração, a melhor pontuação de fitness foi registrada. O sistema retorna ao final:

- A formação ideal com 11 jogadores
- Suas respectivas posições, clubes, nacionalidade e rating
- O somatório total do rating da equipe
- Logs da evolução por geração

---

## Conclusões

O algoritmo genético demonstrou eficiência na busca de soluções viáveis dentro do espaço de combinações possíveis, e o uso de penalidades ajudou a garantir que as formações respeitassem a tática desejada.
