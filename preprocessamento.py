
# ==========================================
# BIKECAST — PRÉ-PROCESSAMENTO
# ==========================================

import pandas as pd
import numpy as np


def preparar_features(dados):

    # Seleciona apenas as variáveis preditoras
    X = dados[[
        "season", "yr", "mnth", "hr",
        "holiday", "weekday", "workingday",
        "weathersit", "temp", "atemp",
        "hum", "windspeed"
    ]].copy()

    # Define as categorias conhecidas
    X["season"] = pd.Categorical(
        X["season"], categories=[1, 2, 3, 4]
    )

    X["weathersit"] = pd.Categorical(
        X["weathersit"], categories=[1, 2, 3, 4]
    )

    # One-Hot Encoding
    X = pd.get_dummies(
        X,
        columns=["season", "weathersit"],
        prefix=["season", "weather"],
        dtype=int
    )

    # Transformação cíclica das horas
    X["hr_sin"] = np.sin(2 * np.pi * X["hr"] / 24)
    X["hr_cos"] = np.cos(2 * np.pi * X["hr"] / 24)

    # Transformação cíclica dos meses
    X["mnth_sin"] = np.sin(
        2 * np.pi * (X["mnth"] - 1) / 12
    )

    X["mnth_cos"] = np.cos(
        2 * np.pi * (X["mnth"] - 1) / 12
    )

    # Transformação cíclica dos dias da semana
    X["weekday_sin"] = np.sin(
        2 * np.pi * X["weekday"] / 7
    )

    X["weekday_cos"] = np.cos(
        2 * np.pi * X["weekday"] / 7
    )

    return X


def criar_experimentos(X):

    # Organiza os três conjuntos de features
    return {
        "completo": X.copy(),

        "sem_atemp": X.drop(
            columns=["atemp"]
        ),

        "temporal_ciclico": X.drop(
            columns=["hr", "mnth", "weekday"]
        )
    }
