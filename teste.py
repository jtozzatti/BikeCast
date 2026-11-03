
# ==========================================
# BIKECAST — FEATURE ENGINEERING
# ==========================================

# Importa o Pandas para trabalhar com os dados
import pandas as pd


# ==========================================
# 1. CARREGAMENTO DOS DADOS
# ==========================================

# Lê o dataset de aluguel de bicicletas
df = pd.read_csv("data/hour.csv")

# Converte a coluna de data para datetime
df["dteday"] = pd.to_datetime(df["dteday"])


# ==========================================
# 2. VERIFICAÇÕES INICIAIS
# ==========================================

# Confere o tamanho do dataset
print("Dataset:", df.shape)

# Confere se existem valores ausentes
print("Valores ausentes:", df.isnull().sum().sum())

# Confere se existem registros duplicados
print("Duplicados:", df.duplicated().sum())

# Confere se o total de aluguéis está consistente
print(
    "Consistência do target:",
    (df["casual"] + df["registered"] == df["cnt"]).all()
)


# ==========================================
# 3. SEPARAÇÃO DAS FEATURES E TARGET
# ==========================================

# Define a variável que queremos prever
y = df["cnt"]

# Remove a variável alvo e colunas que não serão
# utilizadas como entradas nesta primeira versão
X = df.drop(columns=[
    "cnt",
    "casual",
    "registered",
    "instant",
    "dteday"
])

# Mostra o tamanho dos conjuntos
print("\nFeatures (X):", X.shape)
print("Target (y):", y.shape)

# Mostra as variáveis disponíveis para o modelo
print("\nVariáveis em X:")
print(X.columns.tolist())

# ==========================================
# 4. CLASSIFICAÇÃO DAS FEATURES
# ==========================================

# Variáveis que representam categorias
categoricas = ["season", "weathersit"]

# Variáveis que representam valores binários
binarias = ["yr", "holiday", "workingday"]

# Variáveis relacionadas ao tempo e calendário
temporais = ["mnth", "hr", "weekday"]

# Variáveis numéricas contínuas
numericas = ["temp", "atemp", "hum", "windspeed"]

# Mostra a quantidade de variáveis em cada grupo
print("\nCategóricas:", len(categoricas))
print("Binárias:", len(binarias))
print("Temporais:", len(temporais))
print("Numéricas:", len(numericas))

# ==========================================
# 5. ONE-HOT ENCODING
# ==========================================

# Transforma as categorias de season em colunas binárias
season_encoded = pd.get_dummies(
    X["season"],
    prefix="season",
    dtype=int
)

# Mostra as primeiras 5 linhas
print(season_encoded.head())

# Mostra o tamanho da nova tabela
print("Formato:", season_encoded.shape)

# Transforma as categorias climáticas em colunas binárias
weather_encoded = pd.get_dummies(
    X["weathersit"],
    prefix="weather",
    dtype=int
)

# Mostra as primeiras 5 linhas
print(weather_encoded.head())

# Mostra o tamanho da nova tabela
print("Formato:", weather_encoded.shape)

# Conta quantos registros pertencem a cada categoria
print("\nQuantidade por categoria:")
print(weather_encoded.sum())

# ==========================================
# 6. INTEGRAÇÃO DAS FEATURES
# ==========================================

# Remove as colunas categóricas originais
X_encoded = X.drop(columns=["season", "weathersit"])

# Adiciona as novas colunas binárias
X_encoded = pd.concat(
    [X_encoded, season_encoded, weather_encoded],
    axis=1
)

# Confere o resultado
print("\nNovo formato:", X_encoded.shape)
print("\nFeatures transformadas:")
print(X_encoded.columns.tolist())

# ==========================================
# 7. FEATURES CÍCLICAS
# ==========================================

# Importa funções matemáticas
import numpy as np

# Representa o horário em um ciclo de 24 horas
X_encoded["hr_sin"] = np.sin(
    2 * np.pi * X_encoded["hr"] / 24
)

X_encoded["hr_cos"] = np.cos(
    2 * np.pi * X_encoded["hr"] / 24
)

# Mostra as novas variáveis para cada horário
print(
    X_encoded[["hr", "hr_sin", "hr_cos"]]
    .drop_duplicates()
    .sort_values("hr")
    .round(3)
)

# ==========================================
# 8. TRANSFORMAÇÃO CÍCLICA DOS MESES
# ==========================================

# Representa os meses em um ciclo de 12 meses
X_encoded["mnth_sin"] = np.sin(
    2 * np.pi * (X_encoded["mnth"] - 1) / 12
)

X_encoded["mnth_cos"] = np.cos(
    2 * np.pi * (X_encoded["mnth"] - 1) / 12
)

# Mostra a representação dos 12 meses
print(
    X_encoded[["mnth", "mnth_sin", "mnth_cos"]]
    .drop_duplicates()
    .sort_values("mnth")
    .round(3)
)

# ==========================================
# 9. TRANSFORMAÇÃO CÍCLICA DA SEMANA
# ==========================================

# Representa os dias da semana em um ciclo de 7 dias
X_encoded["weekday_sin"] = np.sin(
    2 * np.pi * X_encoded["weekday"] / 7
)

X_encoded["weekday_cos"] = np.cos(
    2 * np.pi * X_encoded["weekday"] / 7
)

# Mostra a representação dos 7 dias da semana
print(
    X_encoded[["weekday", "weekday_sin", "weekday_cos"]]
    .drop_duplicates()
    .sort_values("weekday")
    .round(3)
)

# ==========================================
# 10. REVISÃO DAS FEATURES
# ==========================================

# Mostra a quantidade de registros e features
print("\nFormato atual:", X_encoded.shape)

# Verifica se existem valores ausentes
print("Valores ausentes:", X_encoded.isnull().sum().sum())

# Mostra todas as features disponíveis
print("\nFeatures atuais:")
print(X_encoded.columns.tolist())

# Confere se os índices de X e y continuam alinhados
print("\nÍndices alinhados:", X_encoded.index.equals(y.index))

# ==========================================
# 11. COMPARAÇÃO DE FEATURES CORRELACIONADAS
# ==========================================

# Versão A: mantém temperatura e sensação térmica
X_completo = X_encoded.copy()

# Versão B: remove apenas a sensação térmica
X_sem_atemp = X_encoded.drop(columns=["atemp"])

# Compara a quantidade de features
print("\nVersão completa:", X_completo.shape)
print("Versão sem atemp:", X_sem_atemp.shape)

# Confirma se atemp foi removida da versão B
print(
    "atemp na versão completa:",
    "atemp" in X_completo.columns
)

print(
    "atemp na versão reduzida:",
    "atemp" in X_sem_atemp.columns
)

# ==========================================
# 12. COMPARAÇÃO DAS FEATURES TEMPORAIS
# ==========================================

# Versão A: mantém as variáveis originais e cíclicas
X_temporal_completo = X_completo.copy()

# Versão B: mantém apenas as versões cíclicas
# de hr, mnth e weekday
X_temporal_ciclico = X_completo.drop(
    columns=["hr", "mnth", "weekday"]
)

# Compara os formatos
print("\nTemporal completo:", X_temporal_completo.shape)
print("Temporal cíclico:", X_temporal_ciclico.shape)

# Verifica quais colunas foram removidas
print(
    "\nColunas removidas:",
    set(X_temporal_completo.columns)
    - set(X_temporal_ciclico.columns)
)

# ==========================================
# 13. ORGANIZAÇÃO DOS EXPERIMENTOS
# ==========================================

# Organiza as versões para comparação futura
experimentos = {
    "completo": X_completo,
    "sem_atemp": X_sem_atemp,
    "temporal_ciclico": X_temporal_ciclico
}

# Mostra o tamanho de cada conjunto
for nome, dados in experimentos.items():
    print(
        f"{nome}: {dados.shape[0]} registros, "
        f"{dados.shape[1]} features"
    )

# ==========================================
# 14. VALIDAÇÃO FINAL DAS FEATURES
# ==========================================

# Verifica os tipos de dados das features
print("\nTipos de dados:")
print(X_completo.dtypes.value_counts())

# Verifica se todas as colunas são numéricas
print(
    "\nTodas as features são numéricas:",
    all(pd.api.types.is_numeric_dtype(tipo)
        for tipo in X_completo.dtypes)
)

# Confere se todos os experimentos preservaram
# a mesma quantidade de registros do target
for nome, dados in experimentos.items():
    print(
        f"{nome} alinhado:",
        dados.index.equals(y.index)
    )