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
print(df[["season", "yr", "mnth", "hr", "holiday", "weekday", "workingday", "weathersit"]].nunique())