"""
Tests unitaires pour le module de preprocessing.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pandas as pd
import numpy as np
from fraudx.preprocessing import FraudPreprocessor, FeatureEngineer


def test_preprocessor_instantiation():
    p = FraudPreprocessor(models_path="models_optuna/")
    assert p is not None
    assert p._loaded is False


def test_feature_engineering_temporal():
    df = pd.DataFrame({"TransactionDT": [0, 3600, 86400]})
    df = FeatureEngineer.add_temporal_features(df)
    assert "hour" in df.columns
    assert "dayofweek" in df.columns
    assert df["hour"].iloc[0] == 0


def test_feature_engineering_amount():
    df = pd.DataFrame({"TransactionAmt": [0, 100, 1000]})
    df = FeatureEngineer.add_amount_features(df)
    assert "log_amount" in df.columns
    assert df["log_amount"].iloc[2] > df["log_amount"].iloc[1]


def test_feature_engineering_behavioral():
    df = pd.DataFrame({
        "card1": [1, 1, 2, 2, 2],
        "TransactionAmt": [100, 200, 300, 400, 500],
        "TransactionDT": [0, 100, 0, 200, 400]
    })
    df = FeatureEngineer.add_behavioral_features(df)
    assert "tx_count_by_card1" in df.columns
    assert "time_since_last_tx_card1" in df.columns
    assert df["tx_count_by_card1"].iloc[0] == 2
    assert df["tx_count_by_card1"].iloc[2] == 3


def test_preprocessor_transform_raises_without_load():
    p = FraudPreprocessor(models_path="models_optuna/")
    try:
        p.transform(pd.DataFrame())
        assert False, "Devrait lever une erreur (artefacts non chargés)"
    except Exception:
        pass


def test_feature_engineer_empty_df():
    df = pd.DataFrame()
    df = FeatureEngineer.add_temporal_features(df)
    df = FeatureEngineer.add_amount_features(df)
    df = FeatureEngineer.add_behavioral_features(df)
    assert len(df.columns) == 0


def test_feature_engineer_missing_columns():
    df = pd.DataFrame({"dummy": [1, 2, 3]})
    df = FeatureEngineer.add_temporal_features(df)
    df = FeatureEngineer.add_amount_features(df)
    df = FeatureEngineer.add_behavioral_features(df)
    assert "dummy" in df.columns
    assert "hour" not in df.columns
    assert "log_amount" not in df.columns


def test_preprocessor_repr():
    p = FraudPreprocessor(models_path="models_optuna/")
    assert "FraudPreprocessor" in repr(p)


def test_get_risk_level_import():
    from fraudx.preprocessing import FraudPreprocessor
    p = FraudPreprocessor()
    assert hasattr(p, "load_artifacts")
    assert hasattr(p, "transform")
    assert hasattr(p, "transform_single")
