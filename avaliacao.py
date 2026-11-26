
# ==========================================
# BIKECAST — ETAPA 7: AVALIAÇÃO
# ==========================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib
import time
import sklearn

from pathlib import Path

from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.dummy import DummyRegressor
from sklearn.inspection import permutation_importance

from sklearn.metrics import (
    mean_absolute_error,
    root_mean_squared_error,
    r2_score
)

from preprocessamento import preparar_features


# ==========================================
# ORGANIZAÇÃO DAS PASTAS
# ==========================================

# Cria pastas para armazenar os resultados
Path("models").mkdir(exist_ok=True)
Path("reports").mkdir(exist_ok=True)
Path("reports/figures").mkdir(exist_ok=True)


# ==========================================
# CARREGAMENTO DOS DADOS
# ==========================================

df = pd.read_csv("data/hour.csv")

df["dteday"] = pd.to_datetime(df["dteday"])

df["datetime"] = (
    df["dteday"] +
    pd.to_timedelta(df["hr"], unit="h")
)

# Confere a organização temporal
assert df["datetime"].is_monotonic_increasing
assert not df["datetime"].duplicated().any()


# ==========================================
# 7.1 RETREINAMENTO DO MODELO
# ==========================================

# Preserva o corte temporal da Etapa 6
n = len(df)

fim_validacao = int(n * 0.85)

# Combina treino e validação
treino_final = df.iloc[:fim_validacao].copy()

# Mantém o conjunto de teste original
teste = df.iloc[fim_validacao:].copy()

# Prepara as 24 features
X_treino_final = preparar_features(treino_final)
X_teste = preparar_features(teste)

# Separa os targets
y_treino_final = treino_final["cnt"]
y_teste = teste["cnt"]

# Valida os conjuntos
assert X_treino_final.columns.equals(X_teste.columns)
assert X_treino_final.index.equals(y_treino_final.index)
assert X_teste.index.equals(y_teste.index)

assert not X_treino_final.isnull().any().any()
assert not X_teste.isnull().any().any()

assert (
    treino_final["datetime"].max()
    < teste["datetime"].min()
)

print("\n--- CONJUNTOS FINAIS ---")

print("Treino final:", X_treino_final.shape)
print("Teste:", X_teste.shape)

print("\nPeríodo de treinamento:")
print(treino_final["datetime"].min())
print(treino_final["datetime"].max())

print("\nPeríodo de teste:")
print(teste["datetime"].min())
print(teste["datetime"].max())

# Mantém a configuração selecionada na Etapa 6
modelo_final = HistGradientBoostingRegressor(
    max_iter=200,
    learning_rate=0.1,
    random_state=42
)

# Mede o tempo de treinamento
inicio = time.perf_counter()

# Treina utilizando treino + validação
modelo_final.fit(
    X_treino_final,
    y_treino_final
)

tempo_treino = time.perf_counter() - inicio

print("\n--- MODELO RETREINADO ---")
print(f"Tempo de treinamento: {tempo_treino:.2f}s")


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


# ==========================================
# 7.2 AVALIAÇÃO NO CONJUNTO DE TESTE
# ==========================================

# Realiza previsões em dados reservados
inicio = time.perf_counter()

previsoes = modelo_final.predict(X_teste)

# Impede previsões negativas
previsoes = previsoes.clip(min=0)

tempo_previsao = time.perf_counter() - inicio

# Calcula as métricas finais
metricas_teste = avaliar_modelo(
    y_teste,
    previsoes
)

print("\n--- RESULTADOS NO TESTE ---")

for metrica, valor in metricas_teste.items():
    print(f"{metrica}: {valor:.4f}")

print(f"Tempo de previsão: {tempo_previsao:.4f}s")


# ==========================================
# 7.3 COMPARAÇÃO COM O BASELINE
# ==========================================

# Retreina o baseline com os mesmos dados
baseline = DummyRegressor(strategy="mean")

baseline.fit(
    X_treino_final,
    y_treino_final
)

# Realiza previsões no mesmo conjunto de teste
previsoes_baseline = baseline.predict(X_teste)

metricas_baseline = avaliar_modelo(
    y_teste,
    previsoes_baseline
)

# Calcula a redução percentual do MAE
melhoria_mae = (
    (
        metricas_baseline["MAE"]
        - metricas_teste["MAE"]
    )
    / metricas_baseline["MAE"]
) * 100

print("\n--- BASELINE NO TESTE ---")

for metrica, valor in metricas_baseline.items():
    print(f"{metrica}: {valor:.4f}")

print(
    "\nRedução do MAE sobre o baseline:",
    f"{melhoria_mae:.2f}%"
)


# ==========================================
# 7.4 VALIDAÇÃO X TESTE
# ==========================================

# Carrega os resultados reais da Etapa 6
resultados_modelagem = pd.read_csv(
    "resultados_modelagem.csv"
)

# Seleciona a configuração vencedora
resultado_validacao = resultados_modelagem.loc[
    (resultados_modelagem["Modelo"] == "Gradient Boosting")
    & (resultados_modelagem["Features"] == "completo")
].iloc[0]

# Organiza os resultados
comparacao = pd.DataFrame([
    {
        "Conjunto": "Validação",
        "Modelo": "Gradient Boosting",
        "MAE": resultado_validacao["MAE"],
        "RMSE": resultado_validacao["RMSE"],
        "R2": resultado_validacao["R2"]
    },
    {
        "Conjunto": "Teste",
        "Modelo": "Gradient Boosting",
        **metricas_teste
    },
    {
        "Conjunto": "Teste",
        "Modelo": "Baseline",
        **metricas_baseline
    }
])

print("\n--- COMPARAÇÃO FINAL ---")

print(
    comparacao.round(4).to_string(index=False)
)

# Calcula a variação do MAE
variacao_mae = (
    (
        metricas_teste["MAE"]
        - resultado_validacao["MAE"]
    )
    / resultado_validacao["MAE"]
) * 100

print(
    "\nVariação do MAE entre validação e teste:",
    f"{variacao_mae:+.2f}%"
)


# ==========================================
# 7.5 VALORES REAIS X PREVISTOS
# ==========================================

# Organiza as previsões em um DataFrame
df_previsoes = pd.DataFrame({
    "datetime": teste["datetime"].to_numpy(),
    "hr": teste["hr"].to_numpy(),
    "workingday": teste["workingday"].to_numpy(),
    "weathersit": teste["weathersit"].to_numpy(),
    "real": y_teste.to_numpy(),
    "previsto": previsoes
})

# Calcula os erros individuais
df_previsoes["residuo"] = (
    df_previsoes["real"]
    - df_previsoes["previsto"]
)

df_previsoes["erro_absoluto"] = (
    df_previsoes["residuo"].abs()
)

# Define apenas as colunas que serão arredondadas
colunas_arredondamento = {
    "previsto": 2,
    "residuo": 2,
    "erro_absoluto": 2
}

print("\n--- PRIMEIRAS PREVISÕES ---")

# Arredonda somente as colunas numéricas
print(
    df_previsoes.head(10)
    .round(colunas_arredondamento)
    .to_string(index=False)
)

# Seleciona os primeiros sete dias do teste
inicio_periodo = df_previsoes["datetime"].min()

fim_periodo = (
    inicio_periodo + pd.Timedelta(days=7)
)

amostra = df_previsoes[
    df_previsoes["datetime"] < fim_periodo
]

# Gráfico temporal
plt.figure(figsize=(14, 5))

plt.plot(
    amostra["datetime"],
    amostra["real"],
    label="Demanda real"
)

plt.plot(
    amostra["datetime"],
    amostra["previsto"],
    label="Demanda prevista",
    linestyle="--"
)

plt.title("BikeCast — Demanda real x prevista")
plt.xlabel("Data")
plt.ylabel("Quantidade de aluguéis")
plt.legend()
plt.xticks(rotation=30)
plt.tight_layout()

plt.savefig(
    "reports/figures/01_real_vs_previsto.png",
    dpi=150
)

plt.close()


# ==========================================
# GRÁFICO DE DISPERSÃO
# ==========================================

plt.figure(figsize=(7, 7))

plt.scatter(
    df_previsoes["real"],
    df_previsoes["previsto"],
    alpha=0.3
)

# Define a linha de previsão perfeita
limite = max(
    df_previsoes["real"].max(),
    df_previsoes["previsto"].max()
)

plt.plot(
    [0, limite],
    [0, limite],
    linestyle="--",
    label="Previsão perfeita"
)

plt.title("Valores reais x valores previstos")
plt.xlabel("Demanda real")
plt.ylabel("Demanda prevista")
plt.legend()
plt.tight_layout()

plt.savefig(
    "reports/figures/02_dispersao_previsoes.png",
    dpi=150
)

plt.close()


# ==========================================
# 7.6 ANÁLISE DOS RESÍDUOS
# ==========================================

# Resíduo positivo: modelo subestimou
# Resíduo negativo: modelo superestimou

print("\n--- ESTATÍSTICAS DOS RESÍDUOS ---")

print(
    df_previsoes["residuo"].describe().round(2)
)

print(
    "\nResíduo médio:",
    round(df_previsoes["residuo"].mean(), 2)
)

print(
    "Mediana do erro absoluto:",
    round(df_previsoes["erro_absoluto"].median(), 2)
)

print(
    "Percentil 90 do erro absoluto:",
    round(df_previsoes["erro_absoluto"].quantile(0.90), 2)
)

# Distribuição dos resíduos
plt.figure(figsize=(10, 5))

plt.hist(
    df_previsoes["residuo"],
    bins=50,
    edgecolor="black"
)

plt.axvline(
    0,
    linestyle="--",
    label="Erro zero"
)

plt.title("Distribuição dos resíduos")
plt.xlabel("Valor real - valor previsto")
plt.ylabel("Frequência")
plt.legend()
plt.tight_layout()

plt.savefig(
    "reports/figures/03_distribuicao_residuos.png",
    dpi=150
)

plt.close()


# ==========================================
# RESÍDUOS X PREVISÕES
# ==========================================

plt.figure(figsize=(10, 5))

plt.scatter(
    df_previsoes["previsto"],
    df_previsoes["residuo"],
    alpha=0.3
)

plt.axhline(
    0,
    linestyle="--"
)

plt.title("Resíduos x valores previstos")
plt.xlabel("Demanda prevista")
plt.ylabel("Resíduo")
plt.tight_layout()

plt.savefig(
    "reports/figures/04_residuos_vs_previsoes.png",
    dpi=150
)

plt.close()


# ==========================================
# 7.7 ANÁLISE DOS ERROS POR HORÁRIO
# ==========================================

# Calcula o erro médio em cada hora
erro_por_hora = (
    df_previsoes.groupby("hr")
    .agg(
        MAE=("erro_absoluto", "mean"),
        demanda_media=("real", "mean"),
        previsao_media=("previsto", "mean"),
        registros=("real", "size")
    )
)

print("\n--- ERRO POR HORÁRIO ---")

print(erro_por_hora.round(2))

print("\n--- HORÁRIOS COM MAIORES ERROS ---")

print(
    erro_por_hora
    .sort_values("MAE", ascending=False)
    .head(5)
    .round(2)
)

# Gráfico de erros por horário
plt.figure(figsize=(12, 5))

plt.bar(
    erro_por_hora.index,
    erro_por_hora["MAE"]
)

plt.title("Erro absoluto médio por horário")
plt.xlabel("Hora")
plt.ylabel("MAE")
plt.xticks(range(24))
plt.tight_layout()

plt.savefig(
    "reports/figures/05_erro_por_hora.png",
    dpi=150
)

plt.close()


# ==========================================
# ERROS POR TIPO DE DIA
# ==========================================

erro_por_dia = (
    df_previsoes.groupby("workingday")
    .agg(
        MAE=("erro_absoluto", "mean"),
        demanda_media=("real", "mean"),
        registros=("real", "size")
    )
)

print("\n--- ERRO POR TIPO DE DIA ---")

print(erro_por_dia.round(2))


# ==========================================
# ERROS POR CONDIÇÃO CLIMÁTICA
# ==========================================

erro_por_clima = (
    df_previsoes.groupby("weathersit")
    .agg(
        MAE=("erro_absoluto", "mean"),
        demanda_media=("real", "mean"),
        registros=("real", "size")
    )
)

print("\n--- ERRO POR CONDIÇÃO CLIMÁTICA ---")

print(erro_por_clima.round(2))


# ==========================================
# MAIORES ERROS INDIVIDUAIS
# ==========================================

maiores_erros = df_previsoes.nlargest(
    10,
    "erro_absoluto"
)

print("\n--- 10 MAIORES ERROS ---")

# Arredonda somente as colunas numéricas
print(
    maiores_erros
    .round(colunas_arredondamento)
    .to_string(index=False)
)


# ==========================================
# 7.8 IMPORTÂNCIA DAS FEATURES
# ==========================================

# Utiliza o MAE com a mesma regra de clipping
# aplicada durante a avaliação do modelo
def pontuacao_mae(modelo, X, y):

    previsto = modelo.predict(X).clip(min=0)

    return -mean_absolute_error(y, previsto)


# Mede a perda de desempenho ao embaralhar
# individualmente cada feature
importancia = permutation_importance(
    modelo_final,
    X_teste,
    y_teste,
    scoring=pontuacao_mae,
    n_repeats=10,
    random_state=42,
    n_jobs=-1
)

# Organiza os resultados
df_importancia = pd.DataFrame({
    "Feature": X_teste.columns,
    "Importancia": importancia.importances_mean,
    "Desvio_padrao": importancia.importances_std
})

df_importancia = df_importancia.sort_values(
    "Importancia",
    ascending=False
)

print("\n--- IMPORTÂNCIA DAS FEATURES ---")

print(
    df_importancia.round(4).to_string(index=False)
)

# Seleciona as 15 primeiras features
top_features = (
    df_importancia.head(15)
    .sort_values("Importancia")
)

plt.figure(figsize=(10, 7))

plt.barh(
    top_features["Feature"],
    top_features["Importancia"],
    xerr=top_features["Desvio_padrao"]
)

plt.axvline(0, linestyle="--")

plt.title("Importância das features — Permutation Importance")
plt.xlabel("Aumento do MAE após embaralhamento")
plt.tight_layout()

plt.savefig(
    "reports/figures/06_importancia_features.png",
    dpi=150
)

plt.close()


# ==========================================
# GRÁFICO DE COMPARAÇÃO DOS MODELOS
# ==========================================

plt.figure(figsize=(9, 5))

nomes = [
    "Baseline\nTeste",
    "Gradient Boosting\nValidação",
    "Gradient Boosting\nTeste"
]

valores = [
    metricas_baseline["MAE"],
    resultado_validacao["MAE"],
    metricas_teste["MAE"]
]

barras = plt.bar(nomes, valores)

plt.bar_label(
    barras,
    fmt="%.2f",
    padding=3
)

plt.title("Comparação do erro absoluto médio")
plt.ylabel("MAE")
plt.ylim(0, max(valores) * 1.15)
plt.tight_layout()

plt.savefig(
    "reports/figures/07_comparacao_mae.png",
    dpi=150
)

plt.close()


# ==========================================
# 7.9 EXPORTAÇÃO DOS RESULTADOS
# ==========================================

# Salva o modelo e suas informações
artefato = {
    "modelo": modelo_final,
    "features": X_treino_final.columns.tolist(),
    "nome_modelo": "HistGradientBoostingRegressor",
    "conjunto_features": "completo",
    "metricas_teste": metricas_teste,
    "registros_treino": len(treino_final),
    "registros_teste": len(teste),
    "inicio_treino": str(treino_final["datetime"].min()),
    "fim_treino": str(treino_final["datetime"].max()),
    "inicio_teste": str(teste["datetime"].min()),
    "fim_teste": str(teste["datetime"].max()),
    "versao_sklearn": sklearn.__version__
}

joblib.dump(
    artefato,
    "models/bikecast_model.joblib"
)

# Confere se o modelo salvo funciona
artefato_carregado = joblib.load(
    "models/bikecast_model.joblib"
)

previsoes_carregadas = (
    artefato_carregado["modelo"]
    .predict(X_teste.head(5))
    .clip(min=0)
)

assert np.allclose(
    previsoes_carregadas,
    previsoes[:5]
)

# Exporta as métricas
comparacao.to_csv(
    "reports/metricas_avaliacao.csv",
    index=False
)

# Exporta as previsões
df_previsoes.to_csv(
    "reports/previsoes_teste.csv",
    index=False
)

# Exporta a importância das features
df_importancia.to_csv(
    "reports/importancia_features.csv",
    index=False
)

# Exporta os erros por horário
erro_por_hora.to_csv(
    "reports/erros_por_hora.csv"
)

# Exporta os erros por tipo de dia
erro_por_dia.to_csv(
    "reports/erros_por_dia.csv"
)

# Exporta os erros por clima
erro_por_clima.to_csv(
    "reports/erros_por_clima.csv"
)

# Exporta os maiores erros
maiores_erros.to_csv(
    "reports/maiores_erros.csv",
    index=False
)


# ==========================================
# RESUMO FINAL
# ==========================================

print("\n" + "=" * 60)
print("BIKECAST — RESULTADO FINAL")
print("=" * 60)

print("Modelo: HistGradientBoostingRegressor")
print("Features:", X_treino_final.shape[1])
print("Registros de treinamento:", len(treino_final))
print("Registros de teste:", len(teste))

print(f"\nMAE: {metricas_teste['MAE']:.4f}")
print(f"RMSE: {metricas_teste['RMSE']:.4f}")
print(f"R²: {metricas_teste['R2']:.4f}")

print(f"Redução do MAE sobre baseline: {melhoria_mae:.2f}%")

print("\nModelo salvo em:")
print("models/bikecast_model.joblib")

print("\nRelatórios salvos em:")
print("reports/")

print("\nGráficos salvos em:")
print("reports/figures/")

print("\nModelo exportado e verificado com sucesso!")

print("\nETAPA 7 — EXPERIMENTOS FINALIZADOS")
