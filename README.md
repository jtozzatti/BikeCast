# 🚲 BikeCast

### Bike Sharing Demand Analysis & Forecasting

> Projeto de **Data Science e Machine Learning** focado na análise e previsão da demanda por bicicletas compartilhadas.

O **BikeCast** nasceu como um projeto prático para aplicar, de ponta a ponta, conceitos de **Python, análise de dados, exploração de dados e Machine Learning** em um problema realista.

A ideia é utilizar dados históricos de aluguel de bicicletas para entender **quais fatores influenciam a demanda** e, posteriormente, desenvolver um modelo capaz de **prever a quantidade de bicicletas que poderão ser utilizadas em determinado período**.

---

## 🎯 Objetivo

O projeto busca responder perguntas como:

* Em quais horários existe maior demanda?
* Como a demanda muda ao longo dos dias da semana?
* Existe diferença de utilização entre estações do ano?
* Como condições climáticas influenciam o uso das bicicletas?
* A demanda é diferente entre dias úteis e finais de semana?
* Quais variáveis possuem maior relação com o número de aluguéis?
* É possível utilizar os dados históricos para prever a demanda futura?

O projeto será desenvolvido de forma incremental, passando desde a **compreensão e preparação dos dados** até a construção e avaliação de modelos de Machine Learning.

---

## 🧠 Processo do projeto

O desenvolvimento segue um fluxo inspirado no processo utilizado em projetos reais de Data Science:

```text
1. Entender o problema
        ↓
2. Entender os dados
        ↓
3. Limpar / preparar
        ↓
4. Explorar e encontrar padrões (EDA)
        ↓
5. Criar features
        ↓
6. Modelar
        ↓
7. Avaliar
        ↓
8. Entregar / comunicar
```

A ideia não é tratar essas etapas como caixas isoladas.

Conforme novas descobertas forem feitas, algumas decisões poderão ser revisitadas.

---

## 📊 Dataset

O projeto utiliza o **Bike Sharing Dataset**, disponibilizado pelo **UCI Machine Learning Repository**.

O dataset contém informações sobre o uso de um sistema de bicicletas compartilhadas, incluindo:

* Data
* Hora
* Estação do ano
* Mês
* Dia da semana
* Feriado
* Dia útil
* Condições climáticas
* Temperatura
* Sensação térmica
* Umidade
* Velocidade do vento
* Usuários casuais
* Usuários registrados
* Total de bicicletas alugadas

### Variável alvo

A principal variável que queremos prever é:

```text
cnt
```

Ela representa o **número total de bicicletas alugadas em determinado período**.

---

## 🔍 O que já foi feito

### Entendimento dos dados

* [x] Dataset carregado com Pandas
* [x] Estrutura do DataFrame analisada
* [x] Número de linhas e colunas identificado
* [x] Tipos das variáveis analisados
* [x] Variáveis e seus significados estudados
* [x] Variável alvo definida

### Limpeza e preparação inicial

* [x] Verificação de valores ausentes
* [x] Verificação de linhas duplicadas
* [x] Verificação de registros duplicados por data + hora
* [x] Verificação de valores categóricos
* [x] Verificação de faixas das variáveis climáticas
* [x] Verificação da faixa da variável `cnt`
* [x] Verificação da consistência `cnt = casua
