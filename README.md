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

O dataset contém **17.379 registros e 17 variáveis**, com informações sobre o uso de um sistema de bicicletas compartilhadas, incluindo:

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
* [x] Verificação da consistência `casual + registered = cnt`
* [x] Identificação de Data Leakage nas variáveis `casual` e `registered`

### Análise Exploratória dos Dados (EDA)

* [x] Análise estatística da variável alvo `cnt`
* [x] Análise da demanda média por hora
* [x] Comparação da demanda por hora entre dias úteis e dias não úteis
* [x] Análise da demanda média por dia da semana
* [x] Análise da demanda média por mês
* [x] Análise da demanda por estação do ano
* [x] Análise da demanda por condição climática
* [x] Verificação da quantidade de registros por condição climática
* [x] Análise da relação entre temperatura e demanda
* [x] Análise da relação entre umidade e demanda
* [x] Análise da relação entre velocidade do vento e demanda
* [ ] Análise da demanda entre os anos
* [ ] Conclusão da EDA

---

## 📈 Primeiros insights da EDA

A análise exploratória começou a revelar alguns padrões importantes no comportamento da demanda.

### Horário

A demanda varia bastante ao longo do dia.

Nos dias úteis, foram identificados dois períodos de maior utilização:

* Por volta das **8h**
* Entre **17h e 18h**

Já nos dias não úteis, a demanda apresenta um comportamento mais distribuído ao longo do dia, principalmente entre o final da manhã e a tarde.

### Sazonalidade

A demanda também apresenta variações ao longo dos meses.

Os primeiros meses do ano possuem uma demanda média menor, seguida por um crescimento ao longo dos meses e valores mais elevados entre o meio e o segundo semestre do ano.

As estações do ano também apresentam diferenças relevantes na média de aluguéis.

### Condições climáticas

As condições climáticas demonstraram relação com a utilização das bicicletas.

Condições menos favoráveis apresentaram médias menores de aluguel.

A categoria `weathersit = 4`, entretanto, possui apenas **3 registros**, portanto sua média deve ser interpretada com cautela.

### Temperatura

A temperatura apresentou uma correlação de aproximadamente:

```text
0.405
```

Isso indica uma **relação positiva moderada** com a quantidade de aluguéis.

### Umidade

A umidade apresentou uma correlação de aproximadamente:

```text
-0.323
```

Isso indica uma **relação negativa** com a demanda.

### Velocidade do vento

A velocidade do vento apresentou uma correlação de aproximadamente:

```text
0.093
```

O resultado indica uma **relação linear muito fraca** com a quantidade de aluguéis.

Essas relações representam associações encontradas durante a exploração dos dados e **não significam necessariamente causalidade**.

---

## ⚠️ Data Leakage

Durante a análise dos dados foi identificada a seguinte relação:

```text
casual + registered = cnt
```

As variáveis `casual` e `registered` representam diretamente partes da variável alvo.

Utilizá-las como entradas para prever `cnt` faria com que o modelo tivesse acesso indireto à própria resposta, caracterizando **Data Leakage**.

Por esse motivo, essas variáveis não serão utilizadas como preditoras do modelo.

---

## 🛠️ Tecnologias utilizadas

* Python
* Pandas
* Matplotlib
* VS Code
* Git
* GitHub

Novas ferramentas e bibliotecas serão adicionadas conforme o projeto avançar.

---

## 🚧 Status do projeto

O projeto está atualmente na etapa de:

**Análise Exploratória dos Dados (EDA)** 📊

A próxima análise será investigar a diferença de demanda entre os dois anos presentes no dataset.

Após a conclusão da EDA, o projeto seguirá para:

```text
Feature Engineering
        ↓
Machine Learning
        ↓
Avaliação dos modelos
        ↓
Conclusões
```

---

## 🎯 Objetivo final

Ao final do projeto, será desenvolvido um modelo de Machine Learning capaz de utilizar informações temporais e climáticas para **estimar a demanda por bicicletas compartilhadas**.

Além do modelo, o projeto busca documentar todo o processo de análise, desde a compreensão dos dados até a interpretação dos resultados.

---

## 👨‍💻 Autor

**João Victor**

Estudante de Inteligência Artificial e Machine Learning na FIAP, desenvolvendo projetos práticos para aprofundar conhecimentos em:

* Python
* Data Science
* Machine Learning
* Inteligência Artificial

---

> 🚧 **Projeto em desenvolvimento**
