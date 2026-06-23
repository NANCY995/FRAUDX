import sqlite3
import pandas as pd
import datetime
from pathlib import Path
from typing import Optional, List, Dict


DB_PATH = Path("data/fraudx.db")


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id TEXT UNIQUE,
            timestamp TEXT,
            fraud_score REAL,
            prediction TEXT,
            risk_level TEXT,
            raw_input TEXT,
            created_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id TEXT,
            is_fraud INTEGER,
            analyst TEXT,
            comment TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (transaction_id) REFERENCES predictions(transaction_id)
        );

        CREATE TABLE IF NOT EXISTS models (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_name TEXT,
            model_path TEXT,
            f1_score REAL,
            recall REAL,
            precision REAL,
            auc_pr REAL,
            params TEXT,
            created_at TEXT DEFAULT (datetime('now'))
        );

        CREATE INDEX IF NOT EXISTS idx_prediction_tx_id ON predictions(transaction_id);
        CREATE INDEX IF NOT EXISTS idx_feedback_tx_id ON feedback(transaction_id);
    """)

    conn.commit()
    conn.close()


def save_prediction(tx_id: str, timestamp: str, fraud_score: float,
                    prediction: str, risk_level: str, raw_input: dict):
    conn = get_connection()
    conn.execute("""
        INSERT OR REPLACE INTO predictions
        (transaction_id, timestamp, fraud_score, prediction, risk_level, raw_input)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (tx_id, timestamp, fraud_score, prediction, risk_level, str(raw_input)))
    conn.commit()
    conn.close()


def save_feedback(tx_id: str, is_fraud: bool, analyst: str, comment: str = ""):
    conn = get_connection()
    conn.execute("""
        INSERT INTO feedback (transaction_id, is_fraud, analyst, comment)
        VALUES (?, ?, ?, ?)
    """, (tx_id, int(is_fraud), analyst, comment))
    conn.commit()
    conn.close()


def get_recent_predictions(limit: int = 100) -> List[Dict]:
    conn = get_connection()
    rows = conn.execute("""
        SELECT p.*, f.is_fraud as feedback_fraud, f.analyst
        FROM predictions p
        LEFT JOIN feedback f ON p.transaction_id = f.transaction_id
        ORDER BY p.created_at DESC
        LIMIT ?
    """, (limit,)).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_fraud_rate() -> float:
    conn = get_connection()
    row = conn.execute("""
        SELECT
            COUNT(*) as total,
            SUM(CASE WHEN prediction = 'FRAUDE' THEN 1 ELSE 0 END) as frauds
        FROM predictions
    """).fetchone()
    conn.close()
    if row and row["total"] > 0:
        return row["frauds"] / row["total"] * 100
    return 0.0


def get_labeled_data() -> Optional[pd.DataFrame]:
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT p.*, f.is_fraud as label
        FROM predictions p
        INNER JOIN feedback f ON p.transaction_id = f.transaction_id
        WHERE f.is_fraud IS NOT NULL
    """, conn)
    conn.close()
    return df if len(df) > 0 else None


def save_model_metrics(model_name: str, model_path: str,
                       f1: float, recall: float, precision: float,
                       auc_pr: float, params: dict):
    conn = get_connection()
    conn.execute("""
        INSERT INTO models (model_name, model_path, f1_score, recall, precision, auc_pr, params)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (model_name, model_path, f1, recall, precision, auc_pr, str(params)))
    conn.commit()
    conn.close()


def get_best_model() -> Optional[Dict]:
    conn = get_connection()
    row = conn.execute("""
        SELECT * FROM models ORDER BY f1_score DESC LIMIT 1
    """).fetchone()
    conn.close()
    return dict(row) if row else None


if __name__ == "__main__":
    init_db()
    print(f"✅ Base de données initialisée : {DB_PATH}")
