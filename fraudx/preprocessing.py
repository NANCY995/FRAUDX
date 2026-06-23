import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler
from typing import List, Optional, Dict
from pathlib import Path


class FraudPreprocessor:
    def __init__(self, models_path: str = "models_optuna/"):
        self.models_path = Path(models_path)
        self.freq_maps: Optional[Dict] = None
        self.ohe = None
        self.scaler: Optional[StandardScaler] = None
        self.low_card_cols: List[str] = []
        self.high_card_cols: List[str] = []
        self.num_cols: List[str] = []
        self.best_threshold: float = 0.5
        self._loaded = False

    def load_artifacts(self):
        self.freq_maps = joblib.load(self.models_path / "freq_maps.pkl")
        self.best_threshold = float(np.load(self.models_path / "best_threshold.npy"))
        self.scaler = joblib.load(self.models_path / "scaler.pkl")

        try:
            self.ohe = joblib.load(self.models_path / "ohe_encoder.pkl")
        except Exception:
            self.ohe = None

        if self.freq_maps:
            self.high_card_cols = list(self.freq_maps.keys())

        if self.ohe:
            self.low_card_cols = list(self.ohe.feature_names_in_)

        self._loaded = True

    def _ensure_loaded(self):
        if not self._loaded:
            self.load_artifacts()

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        self._ensure_loaded()
        df = df.copy()

        # Frequency encoding (haute cardinalité)
        for col in self.high_card_cols:
            if col in df.columns:
                freq_map = self.freq_maps.get(col, {})
                df[col] = df[col].map(freq_map).fillna(0)

        # One-hot encoding (faible cardinalité) — ajouter les colonnes manquantes
        if self.ohe and self.low_card_cols:
            for col in self.low_card_cols:
                if col not in df.columns:
                    df[col] = ""
            ohe_data = self.ohe.transform(df[self.low_card_cols])
            ohe_cols = self.ohe.get_feature_names_out(self.low_card_cols)
            ohe_df = pd.DataFrame(ohe_data, columns=ohe_cols, index=df.index)
            df = df.drop(columns=self.low_card_cols)
            df = pd.concat([df, ohe_df], axis=1)

        # Ajouter les colonnes manquantes AVANT standardisation
        for col in self.scaler.feature_names_in_:
            if col not in df.columns:
                df[col] = 0.0

        # Forcer les types numériques (évite les colonnes object de Pydantic)
        for col in df.columns:
            if col in self.scaler.feature_names_in_:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

        # Standardisation (toutes les colonnes du scaler sont maintenant présentes)
        scalable = [c for c in self.scaler.feature_names_in_
                    if c in df.select_dtypes(include=np.number).columns]
        if scalable:
            df[scalable] = self.scaler.transform(df[scalable])

        return df

    def transform_single(self, transaction: dict) -> pd.DataFrame:
        df = pd.DataFrame([transaction])
        return self.transform(df)


class FeatureEngineer:
    @staticmethod
    def add_temporal_features(df: pd.DataFrame) -> pd.DataFrame:
        if 'TransactionDT' in df.columns:
            start = pd.Timestamp("2017-12-01")
            dt = start + pd.to_timedelta(df['TransactionDT'], unit='s')
            df['hour'] = dt.dt.hour
            df['dayofweek'] = dt.dt.dayofweek
            df['is_weekend'] = dt.dt.dayofweek.isin([5, 6]).astype(int)
            df['is_night'] = ((dt.dt.hour >= 22) | (dt.dt.hour <= 5)).astype(int)
            df['day_of_month'] = dt.dt.day
        return df

    @staticmethod
    def add_amount_features(df: pd.DataFrame) -> pd.DataFrame:
        if 'TransactionAmt' in df.columns:
            df['log_amount'] = np.log1p(df['TransactionAmt'])
            df['amt_100_ratio'] = df['TransactionAmt'] / 100
        return df

    @staticmethod
    def add_behavioral_features(df: pd.DataFrame) -> pd.DataFrame:
        if 'card1' in df.columns and 'TransactionAmt' in df.columns:
            df['tx_count_by_card1'] = df.groupby('card1')['TransactionAmt'].transform('count')
        if 'card1' in df.columns and 'TransactionDT' in df.columns:
            df_sorted = df.sort_values(['card1', 'TransactionDT'])
            df['time_since_last_tx_card1'] = df_sorted.groupby('card1')['TransactionDT'].diff().fillna(0)
        return df

    @staticmethod
    def add_velocity_features(df: pd.DataFrame) -> pd.DataFrame:
        for group_col in ['card1', 'card2', 'addr1', 'addr2']:
            if group_col in df.columns and 'TransactionAmt' in df.columns:
                key_count = f'tx_count_by_{group_col}'
                key_avg = f'avg_amt_by_{group_col}'
                key_ratio = f'amt_ratio_{group_col}'
                df[key_count] = df.groupby(group_col)['TransactionAmt'].transform('count')
                df[key_avg] = df.groupby(group_col)['TransactionAmt'].transform('mean')
                df[key_ratio] = df['TransactionAmt'] / (df[key_avg] + 1)
        if all(c in df.columns for c in ['card1', 'card2', 'TransactionAmt']):
            df['card1_card2_amt'] = df.groupby(['card1', 'card2'])['TransactionAmt'].transform('mean').fillna(0)
        if 'dist1' in df.columns and 'dist2' in df.columns:
            d1 = pd.to_numeric(df['dist1'], errors='coerce').fillna(0)
            d2 = pd.to_numeric(df['dist2'], errors='coerce').fillna(0)
            df['dist_diff'] = abs(d1 - d2)
        if 'dist1' in df.columns:
            df['dist1_log'] = np.log1p(pd.to_numeric(df['dist1'], errors='coerce').fillna(0))
        return df

    @staticmethod
    def add_email_features(df: pd.DataFrame) -> pd.DataFrame:
        for col in ['P_emaildomain', 'R_emaildomain']:
            if col in df.columns:
                df[f'{col}_cat'] = df[col].fillna('unknown').map(
                    lambda x: 'premium' if any(d in str(x) for d in ['gmail', 'yahoo', 'outlook', 'hotmail'])
                    else ('pro' if any(d in str(x) for d in ['company', 'corp', 'bank'])
                    else 'other')
                )
        return df
