import unittest
import numpy as np
from dashboard.services.data_service import load_dataset,load_evaluation_metrics,load_test_predictions
from dashboard.services.model_service import load_model,predict
class Integration(unittest.TestCase):
    def test_data(self):
        df=load_dataset(); self.assertEqual(len(df),17379); self.assertFalse(df.datetime.duplicated().any())
    def test_model(self):
        df=load_dataset(); artifact=load_model(); self.assertEqual(len(artifact['features']),24)
        pred=predict(df.tail(5)); self.assertEqual(len(pred),5); self.assertTrue(np.isfinite(pred).all()); self.assertTrue((pred>=0).all())
        saved=load_test_predictions().tail(5).previsto.to_numpy(); np.testing.assert_allclose(pred,saved,rtol=1e-6,atol=1e-6)
    def test_metrics(self):
        df=load_test_predictions(); m=load_evaluation_metrics(); row=m[(m.Conjunto=='Teste')&(m.Modelo=='Gradient Boosting')].iloc[0]
        self.assertAlmostEqual(float(np.abs(df.real-df.previsto).mean()),row.MAE,places=6)
if __name__=='__main__': unittest.main()
