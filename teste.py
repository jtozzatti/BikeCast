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