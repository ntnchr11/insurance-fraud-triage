"""
Fase 5 - Analisi delle soglie di decisione, confronto tra i due modelli.

Uso:
    python3 src/threshold_analysis.py
"""

import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

TARGET = "is_fraud"
NUMERIC_COLS = ["WeekOfMonth", "WeekOfMonthClaimed", "Age", "Deductible", "DriverRating"]
THRESHOLDS = [0.3, 0.4, 0.5, 0.6, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]


def threshold_table(y_test, y_proba, total_frauds, total_claims):
    rows = []
    for threshold in THRESHOLDS:
        flagged = y_proba >= threshold
        n_flagged = flagged.sum()
        frauds_caught = y_test[flagged].sum()
        rows.append({
            "soglia": threshold,
            "n_segnalati": n_flagged,
            "%_segnalati": round(n_flagged / total_claims * 100, 1),
            "frodi_trovate": frauds_caught,
            "%_frodi_su_totale": round(frauds_caught / total_frauds * 100, 1),
            "precision": round(frauds_caught / n_flagged, 3) if n_flagged > 0 else 0,
        })
    return pd.DataFrame(rows)


def main():
    train = pd.read_parquet("data/gold/claims_train.parquet")
    test = pd.read_parquet("data/gold/claims_test.parquet")

    X_train = train.drop(columns=[TARGET])
    y_train = train[TARGET]
    X_test = test.drop(columns=[TARGET])
    y_test = test[TARGET]

    total_claims = len(y_test)
    total_frauds = y_test.sum()
    print(f"Sinistri nel test set: {total_claims:,} | Frodi vere: {total_frauds}\n")

    # --- Logistic Regression ---
    scaler = StandardScaler()
    X_train_scaled = X_train.copy()
    X_test_scaled = X_test.copy()
    X_train_scaled[NUMERIC_COLS] = scaler.fit_transform(X_train[NUMERIC_COLS])
    X_test_scaled[NUMERIC_COLS] = scaler.transform(X_test[NUMERIC_COLS])

    log_reg = LogisticRegression(max_iter=2000, class_weight="balanced", random_state=42, C=0.1)
    log_reg.fit(X_train_scaled, y_train)
    proba_lr = log_reg.predict_proba(X_test_scaled)[:, 1]

    print("=== Logistic Regression ===")
    print(threshold_table(y_test, proba_lr, total_frauds, total_claims).to_string(index=False))

    # --- Random Forest ---
    rf = RandomForestClassifier(n_estimators=200, class_weight="balanced", random_state=42, max_depth=10)
    rf.fit(X_train, y_train)
    proba_rf = rf.predict_proba(X_test)[:, 1]

    print("\n=== Random Forest ===")
    print(threshold_table(y_test, proba_rf, total_frauds, total_claims).to_string(index=False))


if __name__ == "__main__":
    main()