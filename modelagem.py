
# ==========================================
# BIKECAST — ETAPA 6: MODELAGEM
# ==========================================

import pandas as pd
import time

from sklearn.base import clone
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import HistGradientBoostingRegressor

from sklearn.metrics import (
    mean_absolute_error,
    root_mean_squared_error,
    r2_score
)

from preprocessamento import (
    preparar_features,
    criar_experimentos
)


# ==========================================
# 6.1 VERIFICAÇÃO CRONOLÓGICA
# ==========================================

df = pd.read_csv("data/hour.csv")

df["dteday"] = pd.to_datetime(df["dteday"])

# Combina data e hora
df["datetime"] = (
    df["dteday"] +
    pd.to_timedelta(df["hr"], unit="h")
)

# Verifica a organização temporal
print("\n--- VERIFICAÇÃO CRONOLÓGICA ---")

print(
    "Ordem cronológica:",
    df["datetime"].is_monotonic_increasing
)

print("Primeiro registro:", df["datetime"].min())
print("Último registro:", df["datetime"].max())
print("Horários duplicados:", df["datetime"].duplicated().sum())

assert df["datetime"].is_monotonic_increasing
assert not df["datetime"].duplicated().any()


# ==========================================
# 6.2 DIVISÃO TEMPORAL DOS DADOS
# ==========================================

n = len(df)

fim_treino = int(n * 0.70)
fim_validacao = int(n * 0.85)

# Treino: 70%
treino = df.iloc[:fim_treino].copy()

# Validação: 15%
validacao = df.iloc[
    fim_treino:fim_validacao
].copy()

# Teste: 15%
teste = df.iloc[fim_validacao:].copy()

# Mostra os períodos
for nome, conjunto in [
    ("Treino", treino),
    ("Validação", validacao),
    ("Teste", teste)
]:
    print(f"\n--- {nome.upper()} ---")
    print("Registros:", len(conjunto))
    print("Início:", conjunto["datetime"].min())
    print("Fim:", conjunto["datetime"].max())

# Separa os targets
y_treino = treino["cnt"]
y_validacao = validacao["cnt"]

# O teste permanece reservado para a Etapa 7


# ==========================================
# FUNÇÃO DE AVALIAÇÃO
# ==========================================

def avaliar_modelo(y_real, y_previsto):

    return {
        "MAE": mean_absolute_error(
            y_real, y_previsto
        ),

        "RMSE": root_mean_squared_error(
            y_real, y_previsto
        ),

        "R2": r2_score(
            y_real, y_previsto
        )
    }


# Armazena os resultados dos experimentos
resultados = []


# ==========================================
# 6.3 MODELO BASELINE
# ==========================================

baseline = DummyRegressor(strategy="mean")

# Treina utilizando a média da demanda
baseline.fit(treino[["hr"]], y_treino)

# Realiza previsões
previsoes_baseline = baseline.predict(
    validacao[["hr"]]
)

# Calcula as métricas
metricas_baseline = avaliar_modelo(
    y_validacao,
    previsoes_baseline
)

resultados.append({
    "Modelo": "Baseline",
    "Features": "media",
    **metricas_baseline,
    "Tempo_treino": 0.0
})

print("\n--- BASELINE ---")

print(
    "Previsão constante:",
    round(baseline.constant_[0][0], 2)
)

for metrica, valor in metricas_baseline.items():
    print(f"{metrica}: {valor:.4f}")


# ==========================================
# PREPARAÇÃO DAS FEATURES
# ==========================================

X_treino = preparar_features(treino)
X_validacao = preparar_features(validacao)

# Verifica a integridade dos conjuntos
assert X_treino.columns.equals(
    X_validacao.columns
)

assert X_treino.index.equals(y_treino.index)
assert X_validacao.index.equals(y_validacao.index)

assert not X_treino.isnull().any().any()
assert not X_validacao.isnull().any().any()

print("\n--- FEATURES PREPARADAS ---")
print("X treino:", X_treino.shape)
print("X validação:", X_validacao.shape)

# Cria os conjuntos de experimentos
experimentos_treino = criar_experimentos(
    X_treino
)

experimentos_validacao = criar_experimentos(
    X_validacao
)


# ==========================================
# 6.4 REGRESSÃO LINEAR
# ==========================================

regressao_linear = LinearRegression()


# ==========================================
# 6.5 RANDOM FOREST
# ==========================================

random_forest = RandomForestRegressor(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)


# ==========================================
# 6.6 GRADIENT BOOSTING
# ==========================================

gradient_boosting = HistGradientBoostingRegressor(
    max_iter=200,
    learning_rate=0.1,
    random_state=42
)


# ==========================================
# ORGANIZAÇÃO DOS MODELOS
# ==========================================

modelos = {
    "Regressão Linear": regressao_linear,
    "Random Forest": random_forest,
    "Gradient Boosting": gradient_boosting
}


# ==========================================
# 6.7 TREINAMENTO E COMPARAÇÃO
# ==========================================

print("\n--- INICIANDO EXPERIMENTOS ---")

for nome_modelo, modelo_base in modelos.items():

    for nome_features, X_train in experimentos_treino.items():

        # Seleciona o conjunto de validação correspondente
        X_val = experimentos_validacao[nome_features]

        assert X_train.columns.equals(X_val.columns)

        print("\n" + "=" * 50)
        print("Modelo:", nome_modelo)
        print("Features:", nome_features)
        print("Quantidade de features:", X_train.shape[1])

        # Cria uma nova instância do modelo
        modelo = clone(modelo_base)

        # Inicia a contagem do tempo
        inicio = time.perf_counter()

        # Treina o modelo
        modelo.fit(X_train, y_treino)

        # Calcula o tempo de treinamento
        tempo_treino = time.perf_counter() - inicio

        # Realiza previsões na validação
        previsoes = modelo.predict(X_val)

        # Evita previsões negativas de demanda
        previsoes = previsoes.clip(min=0)

        # Calcula as métricas
        metricas = avaliar_modelo(
            y_validacao,
            previsoes
        )

        # Armazena os resultados
        resultados.append({
            "Modelo": nome_modelo,
            "Features": nome_features,
            **metricas,
            "Tempo_treino": tempo_treino
        })

        # Mostra o desempenho
        for metrica, valor in metricas.items():
            print(f"{metrica}: {valor:.4f}")

        print(
            f"Tempo de treinamento: "
            f"{tempo_treino:.2f}s"
        )


# ==========================================
# 6.8 COMPARAÇÃO FINAL DOS RESULTADOS
# ==========================================

# Transforma os resultados em um DataFrame
df_resultados = pd.DataFrame(resultados)

# Ordena pelo menor erro absoluto médio
df_resultados = df_resultados.sort_values(
    "MAE"
).reset_index(drop=True)

# Calcula a melhoria em relação ao baseline
df_resultados["Melhoria_MAE_pct"] = (
    (
        metricas_baseline["MAE"]
        - df_resultados["MAE"]
    )
    / metricas_baseline["MAE"]
) * 100

print("\n" + "=" * 80)
print("RANKING DOS MODELOS — VALIDAÇÃO")
print("=" * 80)

print(
    df_resultados.round(4).to_string(
        index=False
    )
)

# Seleciona o melhor candidato
melhor = df_resultados.iloc[0]

print("\n--- MELHOR CANDIDATO ---")

print("Modelo:", melhor["Modelo"])
print("Features:", melhor["Features"])
print("MAE:", round(melhor["MAE"], 2))
print("RMSE:", round(melhor["RMSE"], 2))
print("R²:", round(melhor["R2"], 4))

print(
    "Melhoria sobre o baseline:",
    f'{melhor["Melhoria_MAE_pct"]:.2f}%'
)


# ==========================================
# EXPORTAÇÃO DOS RESULTADOS
# ==========================================

df_resultados.to_csv(
    "resultados_modelagem.csv",
    index=False
)

print("\nResultados exportados com sucesso!")
print("Arquivo: resultados_modelagem.csv")

print("\nETAPA 6 — EXPERIMENTOS FINALIZADOS")
