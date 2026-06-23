"""
Configuration centralisée pour FRAUDX.
Charge les variables depuis .env ou utilise les valeurs par défaut.
"""
import os
from pathlib import Path
from typing import Optional


class Config:
    def __init__(self, env_file: Optional[str] = None):
        self._load_dotenv(env_file)

    def _load_dotenv(self, env_file: Optional[str] = None):
        if env_file is None:
            env_file = self._find_env_file()
        if env_file and Path(env_file).exists():
            with open(env_file) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, val = line.split("=", 1)
                        os.environ.setdefault(key.strip(), val.strip())

    def _find_env_file(self) -> Optional[str]:
        for p in [".env", "../.env", os.path.expanduser("~/.fraudx/.env")]:
            if Path(p).exists():
                return p
        return None

    @property
    def API_HOST(self) -> str:
        return os.getenv("API_HOST", "0.0.0.0")

    @property
    def API_PORT(self) -> int:
        return int(os.getenv("API_PORT", "8000"))

    @property
    def API_WORKERS(self) -> int:
        return int(os.getenv("API_WORKERS", "1"))

    @property
    def DASHBOARD_PORT(self) -> int:
        return int(os.getenv("DASHBOARD_PORT", "8501"))

    @property
    def DB_PATH(self) -> str:
        return os.getenv("DB_PATH", "data/fraudx.db")

    @property
    def MODELS_PATH(self) -> str:
        return os.getenv("MODELS_PATH", "models_optuna/")

    @property
    def MODEL_NAME(self) -> str:
        return os.getenv("MODEL_NAME", "xgb_model.pkl")

    @property
    def THRESHOLD_PATH(self) -> str:
        return os.getenv("THRESHOLD_PATH", "models_optuna/best_threshold.npy")

    @property
    def TRAIN_DATASET(self) -> str:
        return os.getenv("TRAIN_DATASET", "ieee")

    @property
    def TRAIN_FAST(self) -> bool:
        return os.getenv("TRAIN_FAST", "false").lower() == "true"

    @property
    def TRAIN_OPTUNA_TRIALS(self) -> int:
        return int(os.getenv("TRAIN_OPTUNA_TRIALS", "30"))

    @property
    def TRAIN_SEED(self) -> int:
        return int(os.getenv("TRAIN_SEED", "42"))

    @property
    def RETRAIN_MIN_SAMPLES(self) -> int:
        return int(os.getenv("RETRAIN_MIN_SAMPLES", "500"))

    @property
    def RETRAIN_SCHEDULE_HOURS(self) -> int:
        return int(os.getenv("RETRAIN_SCHEDULE_HOURS", "24"))

    @property
    def LOG_LEVEL(self) -> str:
        return os.getenv("LOG_LEVEL", "INFO")

    def __repr__(self) -> str:
        items = [f"{k}={v}" for k, v in self.__dict__.items() if not k.startswith("_")]
        return f"Config({', '.join(items)})"


config = Config()
