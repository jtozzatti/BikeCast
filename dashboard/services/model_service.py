import joblib
import sklearn
import numpy as np
import streamlit as st
from dashboard.services.data_service import BASE_DIR
from preprocessamento import preparar_features
@st.cache_resource
def _load(path, modified):
    artifact=joblib.load(path)
    if artifact['versao_sklearn'] != sklearn.__version__:
        raise RuntimeError('Scikit-learn version mismatch / versão incompatível')
    return artifact
def load_model():
    path=BASE_DIR/'models/bikecast_model.joblib'
    return _load(str(path),path.stat().st_mtime_ns)
def predict(rows):
    artifact=load_model()
    X=preparar_features(rows)
    expected=artifact['features']
    if set(X.columns)!=set(expected): raise ValueError('Feature schema mismatch')
    X=X[expected]
    if not np.isfinite(X.to_numpy(dtype=float)).all(): raise ValueError('Invalid features')
    return np.maximum(artifact['modelo'].predict(X),0)
