"""
Tests d'intégration pour le pipeline complet.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pandas as pd
import numpy as np
from fraudx.preprocessing import FeatureEngineer


def test_full_feature_pipeline():
    """Test que tout le feature engineering s'enchaîne sans erreur."""
    np.random.seed(42)
    n = 100

    df = pd.DataFrame({
        "TransactionAmt": np.random.exponential(1000, n),
        "TransactionDT": np.random.randint(0, 1000000, n),
        "card1": np.random.randint(1000, 9999, n),
        "ProductCD": np.random.choice(["W", "H", "C", "S", "R"], n),
        "card4": np.random.choice(["visa", "mastercard", "discover"], n)
    })

    df = FeatureEngineer.add_temporal_features(df)
    df = FeatureEngineer.add_amount_features(df)
    df = FeatureEngineer.add_behavioral_features(df)
    df = FeatureEngineer.add_velocity_features(df)
    df = FeatureEngineer.add_email_features(df)

    assert "hour" in df.columns
    assert "dayofweek" in df.columns
    assert "log_amount" in df.columns
    assert "tx_count_by_card1" in df.columns
    assert "time_since_last_tx_card1" in df.columns
    assert "amt_100_ratio" in df.columns
    assert "is_weekend" in df.columns
    assert "is_night" in df.columns
    assert len(df) == n


def test_pipeline_preserves_index():
    """Vérifie que l'index est préservé après le feature engineering."""
    df = pd.DataFrame({
        "TransactionAmt": [100, 200, 300],
        "TransactionDT": [0, 100, 200],
        "card1": [1, 1, 2]
    }, index=[10, 20, 30])

    df = FeatureEngineer.add_temporal_features(df)
    df = FeatureEngineer.add_amount_features(df)
    df = FeatureEngineer.add_behavioral_features(df)

    assert list(df.index) == [10, 20, 30]


def test_pipeline_handles_nulls():
    """Test la robustesse face aux valeurs manquantes."""
    df = pd.DataFrame({
        "TransactionAmt": [100, None, 300],
        "TransactionDT": [0, 100, None],
        "card1": [1, None, 2]
    })

    # Ne doit pas planter sur les NaN
    df = FeatureEngineer.add_temporal_features(df)
    df = FeatureEngineer.add_amount_features(df)
    df = FeatureEngineer.add_behavioral_features(df)

    assert len(df) == 3


def test_pipeline_no_crash_on_single_row():
    """Test avec une seule transaction."""
    df = pd.DataFrame({
        "TransactionAmt": [50000],
        "TransactionDT": [0],
        "card1": [12345]
    })

    df = FeatureEngineer.add_temporal_features(df)
    df = FeatureEngineer.add_amount_features(df)
    df = FeatureEngineer.add_behavioral_features(df)

    assert len(df) == 1
    assert df["tx_count_by_card1"].iloc[0] == 1
    assert df["time_since_last_tx_card1"].iloc[0] == 0
