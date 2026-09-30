# Importamos o pandas para trabalhar com os dados
import pandas as pd

# Lemos o arquivo CSV
df = pd.read_csv("data/hour.csv")

# Mostramos as primeiras 5 linhas
print(df.head())

# Mostra a quantidade de linhas e colunas
print(df.shape)

# Mostra o nome das colunas
print(df.columns)

# Mostra o tipo de dado de cada coluna
print(df.dtypes)

# Conta quantos valores vazios existem em cada coluna
print(df.isnull().sum())

# Converte a coluna dteday para o tipo datetime e logo em seguida mostra o tipo de dado de cada coluna
df["dteday"] = pd.to_datetime(df["dteday"])
print(df.dtypes)

# Mostra os valores únicos de algumas colunas
print(df["season"].unique())
print(df["weathersit"].unique())
print(df["hr"].unique())

# Mostra a contagem de valores únicos de algumas colunas
print(df.describe())

# Mostra a quantidade de valores duplicados
print(df.duplicated().sum())

# Mostra todos os valores diferentes que aparecem na coluna "holiday"
print(df["holiday"].unique())

# Mostra todos os valores diferentes que aparecem na coluna "weekday"
print(df["weekday"].unique())

# Mostra todos os valores diferentes que aparecem na coluna "workingday"
print(df["workingday"].unique())

# Mostra todos os valores diferentes que aparecem na coluna "temp"
print(df["temp"].unique())

# Verifica se existem registros repetidos considerando apenas a data e a hora
print(df.duplicated(subset=["dteday", "hr"]).sum())

# Verifica se a soma de usuários casuais e registrados é igual ao total de usuários
print((df["casual"] + df["registered"] == df["cnt"]).all())

# Mostra o menor e o maior valor das variáveis climáticas
print(df[["temp", "atemp", "hum", "windspeed"]].agg(["min", "max"]))

# Mostra o menor e o maior número de bicicletas alugadas em um registro
print(df["cnt"].agg(["min", "max"]))

# Mostra quantos valores diferentes existem em cada variável categórica
print(
    df[
        ["season", "yr", "mnth", "hr", "holiday",
         "weekday", "workingday", "weathersit"]
    ].nunique()
)

# Mostra algumas estatísticas da variável que queremos prever
print(df["cnt"].describe())


# ==========================================
# ANÁLISE EXPLORATÓRIA DOS DADOS (EDA)
# ==========================================

# Calcula a média de aluguéis para cada hora do dia
media_por_hora = df.groupby("hr")["cnt"].mean()

# Mostra a média de cada hora
print(media_por_hora)

# Importa a biblioteca matplotlib para criar gráficos
import matplotlib.pyplot as plt

# Cria um gráfico com a média de aluguéis para cada hora
plt.plot(media_por_hora)

# Define o título do gráfico
plt.title("Média de aluguéis por hora")

# Define os nomes dos eixos
plt.xlabel("Hora")
plt.ylabel("Média de aluguéis")

# Mostra o gráfico
plt.show()


# Calcula a média de aluguéis por hora separando
# dias úteis (1) e dias não úteis (0)
media_hora_trabalho = df.groupby(
    ["hr", "workingday"]
)["cnt"].mean()

print(media_hora_trabalho)


# Organiza os dados para deixar dias úteis e não úteis em colunas separadas
media_hora_trabalho = df.groupby(
    ["hr", "workingday"]
)["cnt"].mean().unstack()

print(media_hora_trabalho)

# Cria uma linha para os dias não úteis
plt.plot(
    media_hora_trabalho.index,
    media_hora_trabalho[0],
    label="Dia não útil"
)

# Cria uma linha para os dias úteis
plt.plot(
    media_hora_trabalho.index,
    media_hora_trabalho[1],
    label="Dia útil"
)

# Adiciona informações ao gráfico
plt.title("Média de aluguéis por hora")
plt.xlabel("Hora")
plt.ylabel("Média de aluguéis")

# Mostra qual linha representa cada tipo de dia
plt.legend()

# Exibe o gráfico
plt.show()


# Calcula a média de aluguéis para cada dia da semana
media_por_dia = df.groupby("weekday")["cnt"].mean()

# Mostra o resultado
print(media_por_dia)


# Calcula a média de aluguéis em cada mês
media_por_mes = df.groupby("mnth")["cnt"].mean()

# Mostra o resultado
print(media_por_mes)

# Cria um gráfico mostrando a média de aluguéis em cada mês
plt.plot(media_por_mes.index, media_por_mes.values, marker="o")

# Adiciona informações ao gráfico
plt.title("Média de aluguéis por mês")
plt.xlabel("Mês")
plt.ylabel("Média de aluguéis")

# Mostra todos os meses no eixo X
plt.xticks(range(1, 13))

# Exibe o gráfico
plt.show()


# Calcula a média de aluguéis para cada estação do ano
media_por_estacao = df.groupby("season")["cnt"].mean()

# Mostra o resultado
print(media_por_estacao)


# Calcula a média de aluguéis para cada condição climática
media_por_clima = df.groupby("weathersit")["cnt"].mean()

# Mostra o resultado
print(media_por_clima)


# Conta quantos registros existem em cada condição climática
quantidade_por_clima = df["weathersit"].value_counts().sort_index()

# Mostra o resultado
print(quantidade_por_clima)


# Mostra temperatura e quantidade de aluguéis
print(df[["temp", "cnt"]].head(10))


# Calcula a correlação entre temperatura e quantidade de aluguéis
correlacao_temp = df["temp"].corr(df["cnt"])

# Mostra o resultado
print(correlacao_temp)


# Cria um gráfico de dispersão entre temperatura e aluguéis
plt.scatter(df["temp"], df["cnt"], alpha=0.2)

# Adiciona informações ao gráfico
plt.title("Temperatura x quantidade de aluguéis")
plt.xlabel("Temperatura normalizada")
plt.ylabel("Quantidade de aluguéis")

# Exibe o gráfico
plt.show()

# Calcula a correlação entre umidade e quantidade de aluguéis
correlacao_umidade = df["hum"].corr(df["cnt"])

# Mostra o resultado
print(correlacao_umidade)

# Cria um gráfico de dispersão entre umidade e aluguéis
plt.scatter(df["hum"], df["cnt"], alpha=0.2)

# Adiciona informações ao gráfico
plt.title("Umidade x quantidade de aluguéis")
plt.xlabel("Umidade normalizada")
plt.ylabel("Quantidade de aluguéis")

# Exibe o gráfico
plt.show()

# Calcula a correlação entre velocidade do vento e quantidade de aluguéis
correlacao_vento = df["windspeed"].corr(df["cnt"])

# Mostra o resultado
print(correlacao_vento)

# Cria um gráfico de dispersão entre velocidade do vento e aluguéis
plt.scatter(df["windspeed"], df["cnt"], alpha=0.2)

# Adiciona informações ao gráfico
plt.title("Velocidade do vento x quantidade de aluguéis")
plt.xlabel("Velocidade do vento normalizada")
plt.ylabel("Quantidade de aluguéis")

# Exibe o gráfico
plt.show()

# Calcula a média de aluguéis em cada ano
media_por_ano = df.groupby("yr")["cnt"].mean()

# Mostra o resultado
print(media_por_ano)

# Cria um gráfico comparando a demanda média entre os dois anos
plt.bar(media_por_ano.index, media_por_ano.values)

# Adiciona título e nomes dos eixos
plt.title("Média de aluguéis por ano")
plt.xlabel("Ano")
plt.ylabel("Média de aluguéis")

# Mostra apenas os códigos dos dois anos
plt.xticks([0, 1])

plt.show()

# Calcula a média de aluguéis para cada mês de cada ano
media_mes_ano = df.groupby(["mnth", "yr"])["cnt"].mean().unstack()

# Mostra o resultado
print(media_mes_ano)

# Plota a demanda mensal do primeiro ano
plt.plot(
    media_mes_ano.index,
    media_mes_ano[0],
    marker="o",
    label="Ano 0"
)

# Plota a demanda mensal do segundo ano
plt.plot(
    media_mes_ano.index,
    media_mes_ano[1],
    marker="o",
    label="Ano 1"
)

# Configura o gráfico
plt.title("Demanda média mensal por ano")
plt.xlabel("Mês")
plt.ylabel("Média de aluguéis")
plt.xticks(range(1, 13))
plt.legend()

plt.show()

# Calcula a correlação entre temperatura e sensação térmica
correlacao_temp_atemp = df["temp"].corr(df["atemp"])

# Mostra o resultado
print(correlacao_temp_atemp)

# Calcula a correlação entre sensação térmica e demanda
correlacao_atemp = df["atemp"].corr(df["cnt"])

# Mostra o resultado
print(correlacao_atemp)

# Seleciona as principais variáveis numéricas contínuas
variaveis_numericas = [
    "temp",
    "atemp",
    "hum",
    "windspeed",
    "cnt"
]

# Calcula a correlação entre elas
matriz_correlacao = df[variaveis_numericas].corr()

# Mostra a matriz
print(matriz_correlacao)

# Calcula a média de aluguéis em dias normais e feriados
media_feriado = df.groupby("holiday")["cnt"].mean()

# Mostra o resultado
print(media_feriado)

# Conta quantos registros existem em cada categoria
quantidade_feriado = df["holiday"].value_counts().sort_index()

# Mostra o resultado
print(quantidade_feriado)