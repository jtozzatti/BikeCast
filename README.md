# 🚲 BikeCast

### Bike Sharing Demand Analysis & Forecasting

> Projeto de **Data Science e Machine Learning** focado na análise, previsão e visualização da demanda por bicicletas compartilhadas.

O **BikeCast** nasceu como um projeto prático para aplicar, de ponta a ponta, conceitos de **Python, análise de dados, exploração de dados e Machine Learning** em um problema realista.

A ideia é utilizar dados históricos de aluguel de bicicletas para entender **quais fatores estão associados à demanda**, desenvolver um modelo capaz de **estimar a quantidade de bicicletas que poderão ser utilizadas em determinado período** e, ao final, transformar o projeto em uma **aplicação web interativa** para visualização das análises e utilização do modelo.

Além de construir o projeto, um dos objetivos é documentar o processo de desenvolvimento, registrando decisões, hipóteses, erros e aprendizados encontrados em cada etapa.

---

## 🎯 Objetivo

O projeto busca responder perguntas como:

* Em quais horários existe maior demanda?
* Como a demanda muda ao longo dos dias da semana?
* Existe diferença de utilização entre estações do ano?
* Como as condições climáticas estão relacionadas ao uso das bicicletas?
* A demanda é diferente entre dias úteis e dias não úteis?
* Existe diferença entre feriados e dias normais?
* A demanda mudou entre os anos presentes no dataset?
* Quais variáveis apresentam maior relação com o número de aluguéis?
* Existem variáveis que carregam informações muito semelhantes?
* É possível utilizar os dados históricos para prever a demanda?

Além da análise e modelagem, o objetivo final é disponibilizar os resultados através de uma **aplicação web**, permitindo explorar os principais insights do projeto e realizar previsões de demanda utilizando o modelo treinado.

O projeto está sendo desenvolvido de forma incremental, desde a **compreensão e preparação dos dados** até a construção, avaliação e disponibilização do modelo.

---

## 🧠 Processo do projeto

O desenvolvimento segue um fluxo inspirado no processo utilizado em projetos de Data Science:

```text
1. Entender o problema                  ✅
        ↓
2. Entender os dados                    ✅
        ↓
3. Limpar / preparar                    ✅
        ↓
4. Explorar e encontrar padrões (EDA)   ✅
        ↓
5. Criar features                       ⏭️
        ↓
6. Modelar
        ↓
7. Avaliar
        ↓
8. Entregar / comunicar
        ↓
9. Aplicação + Deploy
```

A ideia não é tratar essas etapas como caixas completamente isoladas.

Conforme novas descobertas forem feitas, algumas decisões poderão ser revisitadas.

A aplicação será desenvolvida somente após a conclusão da parte principal de Data Science e Machine Learning, utilizando os resultados construídos durante as etapas anteriores.

---

## 📊 Dataset

O projeto utiliza o **Bike Sharing Dataset**, disponibilizado pelo **UCI Machine Learning Repository**.

O dataset utilizado contém **17.379 registros e 17 variáveis**, com informações relacionadas ao uso de um sistema de bicicletas compartilhadas, incluindo:

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

* [x] Conversão da variável de data para `datetime`
* [x] Verificação de valores ausentes
* [x] Verificação de linhas duplicadas
* [x] Verificação de registros duplicados por data + hora
* [x] Verificação dos valores das variáveis categóricas
* [x] Verificação das faixas das variáveis climáticas
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
* [x] Comparação da demanda entre os dois anos
* [x] Comparação da demanda mensal entre os anos
* [x] Análise da sensação térmica (`atemp`)
* [x] Análise da relação entre `temp` e `atemp`
* [x] Análise das principais correlações
* [x] Análise da demanda em feriados
* [x] Verificação da quantidade de registros de feriados
* [x] Revisão dos principais insights
* [x] Conclusão da EDA

### Feature Engineering

* [ ] Definição das features utilizadas pelo modelo
* [ ] Tratamento das variáveis categóricas
* [ ] Avaliação da redundância entre `temp` e `atemp`
* [ ] Avaliação de possíveis novas features
* [ ] Preparação do conjunto final para modelagem

---

# 📈 Principais insights da EDA

A Análise Exploratória dos Dados revelou diferentes padrões temporais, sazonais e climáticos associados à demanda por bicicletas.

---

## ⏰ Horário

A demanda varia bastante ao longo do dia.

Nos dias úteis, foram identificados dois períodos de maior utilização:

* Por volta das **8h**
* Entre **17h e 18h**

Já nos dias não úteis, a demanda apresenta um comportamento mais distribuído, crescendo durante a manhã e permanecendo elevada principalmente entre o final da manhã e a tarde.

Esse comportamento sugere que `hr` e `workingday` carregam informações importantes para explicar a demanda.

Os picos encontrados nos dias úteis são compatíveis com horários típicos de deslocamento, embora essa interpretação não represente uma relação causal comprovada.

---

## 💼 Dias úteis x dias não úteis

A interação entre horário e tipo de dia revelou dois comportamentos bastante diferentes.

Nos dias úteis, os principais valores médios observados foram:

```text
8h  → ~477 aluguéis
17h → ~525 aluguéis
18h → ~492 aluguéis
```

Nos dias não úteis, a demanda fica mais distribuída durante o dia, com valores elevados principalmente entre **12h e 16h**.

Isso indica que analisar apenas a hora sem considerar o tipo de dia poderia esconder parte importante do comportamento da demanda.

---

## 📅 Dia da semana

Quando analisada isoladamente, a variável `weekday` apresentou médias relativamente próximas entre suas categorias.

O menor valor médio observado ficou próximo de **177 aluguéis**, enquanto o maior ficou próximo de **196**.

Isso sugere que, isoladamente, o dia da semana separa menos a demanda do que variáveis como `hr` e `workingday`.

---

## 📆 Sazonalidade

A demanda apresenta um padrão sazonal claro ao longo dos meses.

De forma geral:

```text
Jan → Jun: crescimento da demanda
Jun → Set: demanda em patamar elevado
Out → Dez: queda da demanda
```

As categorias de estação do ano também apresentaram diferenças relevantes.

```text
season 1 → ~111
season 2 → ~208
season 3 → ~236
season 4 → ~199
```

A categoria `season = 3` apresentou a maior demanda média, enquanto `season = 1` apresentou a menor.

---

## 🌦️ Condições climáticas

As condições climáticas apresentaram diferenças relevantes na demanda média.

```text
weathersit 1 → ~205
weathersit 2 → ~175
weathersit 3 → ~112
weathersit 4 → ~74
```

Entretanto, a distribuição dos registros mostrou:

```text
weathersit 1 → 11.413 registros
weathersit 2 →  4.544 registros
weathersit 3 →  1.419 registros
weathersit 4 →      3 registros
```

A categoria `weathersit = 4` possui apenas **3 registros**.

Por isso, apesar de apresentar a menor média, esse resultado deve ser interpretado com bastante cautela.

Essa análise reforçou uma lição importante durante a EDA: **não basta analisar uma média sem observar a quantidade de dados que a produziu**.

---

## 🌡️ Temperatura

A temperatura apresentou correlação de aproximadamente:

```text
temp × cnt ≈ +0.405
```

Isso indica uma **associação linear positiva moderada** com a quantidade de aluguéis.

Valores maiores de temperatura tendem a aparecer associados a demandas maiores, embora exista bastante dispersão e a temperatura sozinha não explique o comportamento da demanda.

---

## 💧 Umidade

A umidade apresentou correlação de aproximadamente:

```text
hum × cnt ≈ -0.323
```

Isso representa uma **associação linear negativa**.

Nos dados analisados, valores maiores de umidade tendem a aparecer associados a valores menores de demanda.

---

## 💨 Velocidade do vento

A velocidade do vento apresentou:

```text
windspeed × cnt ≈ +0.093
```

O resultado indica uma **associação linear muito fraca** com a quantidade de aluguéis.

Isso não significa automaticamente que a variável seja inútil para Machine Learning, já que podem existir relações não lineares ou interações com outras features que uma correlação simples não consegue capturar.

---

## 📈 Diferença entre os anos

A demanda apresentou uma diferença considerável entre os dois anos presentes no dataset.

```text
Ano 0 → média ≈ 143,8
Ano 1 → média ≈ 234,7
```

A média do segundo ano foi aproximadamente **63,2% maior** que a do primeiro.

Para verificar se essa diferença estava concentrada apenas em alguns períodos, também foi feita uma comparação entre mês e ano.

O resultado mostrou que o **Ano 1 apresentou demanda média superior ao Ano 0 em todos os 12 meses**.

Ao mesmo tempo, ambos mantiveram um padrão sazonal semelhante ao longo do ano.

Isso indica que `yr` carrega informação relevante sobre a demanda.

---

## 🌡️ Temperatura x sensação térmica

Durante a análise também foi identificada uma correlação extremamente alta entre `temp` e `atemp`:

```text
temp × atemp ≈ +0.988
```

Além disso, as duas possuem praticamente a mesma correlação com a variável alvo:

```text
temp  × cnt ≈ +0.405
atemp × cnt ≈ +0.401
```

Isso sugere que `temp` e `atemp` podem carregar informações bastante semelhantes.

Nenhuma variável será removida apenas com base nessa análise.

A possível redundância será avaliada nas próximas etapas do projeto.

---

## 🗓️ Feriados

A demanda média também foi comparada entre feriados e dias não classificados como feriado.

```text
Não feriado → média ≈ 190,43
Feriado     → média ≈ 156,87
```

A demanda média nos registros de feriado foi aproximadamente **17,6% menor**.

A quantidade de registros em cada categoria foi:

```text
Não feriado → 16.879 registros
Feriado     →    500 registros
```

Os feriados representam uma parcela menor do dataset, mas possuem uma quantidade de observações consideravelmente maior do que situações extremas encontradas em outras variáveis, como `weathersit = 4`.

O resultado representa uma associação observada nos dados e não significa necessariamente que o feriado, isoladamente, seja responsável pela redução da demanda.

---

## 🔗 Principais correlações

Para obter uma visão geral das principais variáveis numéricas contínuas, foi construída uma matriz de correlação utilizando:

```text
temp
atemp
hum
windspeed
cnt
```

Os principais resultados foram:

```text
temp       × cnt ≈ +0.405
atemp      × cnt ≈ +0.401
hum        × cnt ≈ -0.323
windspeed  × cnt ≈ +0.093

temp × atemp ≈ +0.988
```

Variáveis categóricas representadas numericamente, como `season`, `weekday` e `weathersit`, não foram incluídas nessa interpretação da correlação de Pearson para evitar conclusões inadequadas baseadas apenas nos códigos numéricos das categorias.

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

## 🧠 Principais aprendizados da EDA

Além dos insights sobre o dataset, a etapa de EDA também trouxe aprendizados importantes sobre o processo de análise de dados.

Entre eles:

* Correlação não significa causalidade.
* Uma média deve ser interpretada considerando também a quantidade de observações.
* Correlação linear baixa não significa automaticamente que uma variável seja inútil.
* Variáveis diferentes podem carregar informações muito semelhantes.
* Médias gerais podem esconder padrões importantes presentes em subgrupos.
* Cruzar variáveis pode revelar comportamentos que não aparecem quando elas são analisadas isoladamente.
* A EDA deve ser guiada por perguntas, e não apenas pela geração de gráficos.

Durante essa etapa, a análise seguiu principalmente a lógica:

```text
Pergunta
   ↓
Análise
   ↓
Resultado
   ↓
Visualização
   ↓
Interpretação
   ↓
Nova pergunta
```

---

## ✅ Conclusão da EDA

A Análise Exploratória dos Dados permitiu identificar padrões temporais, sazonais e climáticos associados à demanda por bicicletas.

Variáveis como `hr`, `workingday`, `mnth`, `yr`, condições climáticas, temperatura e umidade apresentaram comportamentos relevantes durante a exploração.

Também foram identificados pontos que exigirão atenção nas próximas etapas:

* possível redundância entre `temp` e `atemp`;
* baixa quantidade de registros em `weathersit = 4`;
* Data Leakage em `casual` e `registered`;
* possíveis interações entre variáveis, principalmente `hr` e `workingday`.

Nenhuma variável isolada foi capaz de explicar completamente a demanda.

Os resultados indicam que o comportamento de `cnt` está associado a uma combinação de informações temporais, climáticas e de calendário.

Com isso, a etapa de **Análise Exploratória dos Dados está concluída**.

---

# 🧩 Próxima etapa — Feature Engineering

Com a EDA finalizada, o próximo passo do BikeCast será a etapa de **Feature Engineering**.

Nessa fase, os insights encontrados durante a exploração serão utilizados para decidir como representar e preparar melhor as variáveis antes do treinamento dos modelos.

Algumas questões que serão investigadas:

* Quais variáveis devem entrar no modelo?
* Como tratar variáveis categóricas?
* `temp` e `atemp` devem permanecer juntas?
* Faz sentido criar novas features a partir das informações temporais?
* Existem interações entre variáveis que podem ser representadas?
* Como preparar os dados para treinamento e avaliação?

As decisões serão tomadas durante a própria etapa, evitando remover ou transformar variáveis apenas com base em uma única análise da EDA.

---

## 🌐 Aplicação Web

Após a conclusão das etapas de análise e Machine Learning, o BikeCast será transformado em uma **aplicação web interativa**.

A ideia é criar uma interface que permita apresentar o projeto de forma mais visual e acessível, sem remover a documentação técnica e o código disponíveis neste repositório.

A aplicação deverá possuir duas áreas principais:

### 📊 Dashboard

Uma visualização dos principais resultados encontrados durante a análise exploratória, incluindo padrões relacionados a:

* Horários
* Dias úteis e não úteis
* Meses e sazonalidade
* Condições climáticas
* Temperatura
* Umidade
* Diferenças entre os anos
* Outros fatores relevantes identificados durante a EDA

### 🤖 Previsão de demanda

Uma interface onde será possível informar características como horário, condições climáticas e outras variáveis utilizadas pelo modelo para obter uma **estimativa da demanda por bicicletas**.

Exemplo conceitual:

```text
Horário:            18:00
Temperatura:        ...
Umidade:            ...
Condição climática: ...
Dia útil:           Sim

        [ Prever demanda ]

Demanda estimada: ...
```

A aplicação será desenvolvida somente depois que o modelo estiver treinado e avaliado, garantindo que a interface seja uma camada de apresentação de um projeto de Machine Learning já estruturado.

---

## 🛠️ Tecnologias utilizadas

Atualmente, o projeto utiliza:

* Python
* Pandas
* Matplotlib
* VS Code
* Git
* GitHub

### Tecnologias previstas

Conforme o projeto avançar, novas ferramentas serão adicionadas para as etapas de Machine Learning, aplicação e deploy.

A aplicação web está planejada para ser desenvolvida utilizando **Streamlit**, mantendo grande parte do projeto dentro do ecossistema Python.

---

## 🚧 Status do projeto

### Etapa atual

**EDA concluída ✅**

### Próxima etapa

**Feature Engineering 🧩**

O fluxo seguirá para:

```text
Feature Engineering     ⏭️
        ↓
Machine Learning
        ↓
Avaliação dos modelos
        ↓
Conclusões
        ↓
Aplicação Web
        ↓
Deploy
```

---

## 🎯 Objetivo final

Ao final do projeto, o BikeCast deverá possuir três componentes principais:

### 1. Análise de dados

Exploração e documentação dos principais padrões encontrados no histórico de utilização das bicicletas.

### 2. Modelo de Machine Learning

Modelo capaz de utilizar informações temporais e climáticas para estimar a demanda por bicicletas compartilhadas.

### 3. Aplicação Web

Interface visual para apresentar os principais insights da análise e permitir a utilização do modelo para realizar previsões.

Dessa forma, o projeto busca percorrer um fluxo completo, partindo dos dados brutos até uma solução de Machine Learning que possa ser acessada através de uma aplicação online.

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
