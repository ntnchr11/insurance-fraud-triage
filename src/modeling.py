"""
Fase 4 - Modeling: confronto tra due approcci sul problema sbilanciato.

Uso:
    python3 src/modeling.py
"""
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    precision_score, recall_score, f1_score,
    average_precision_score, classification_report,
)

TARGET = "is_fraud"


def load_data():
    train = pd.read_parquet("data/gold/claims_train.parquet")
    test = pd.read_parquet("data/gold/claims_test.parquet")
    X_train = train.drop(columns=[TARGET])
    y_train = train[TARGET]
    X_test = test.drop(columns=[TARGET])
    y_test = test[TARGET]
    return X_train, y_train, X_test, y_test


def evaluate(name, model, X_test, y_test):
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    pr_auc = average_precision_score(y_test, y_proba)

    print(f"\n=== {name} ===")
    print(f"Precision: {precision:.3f}  (di quelli segnalati come frode, quanti lo erano davvero)")
    print(f"Recall:    {recall:.3f}  (delle frodi vere, quante ne ha trovate)")
    print(f"F1:        {f1:.3f}")
    print(f"PR-AUC:    {pr_auc:.3f}  (qualità complessiva su classi sbilanciate)")
    print("\nReport dettagliato:")
    print(classification_report(y_test, y_pred, target_names=["non frode", "frode"]))

    return {"model": name, "precision": precision, "recall": recall, "f1": f1, "pr_auc": pr_auc}


def main():
    X_train, y_train, X_test, y_test = load_data()

    # --- Modello 1: Logistic Regression ---
    numeric_cols = ["WeekOfMonth", "WeekOfMonthClaimed", "Age", "Deductible", "DriverRating"]
    scaler = StandardScaler()
    X_train_scaled = X_train.copy()
    X_test_scaled = X_test.copy()
    X_train_scaled[numeric_cols] = scaler.fit_transform(X_train[numeric_cols])
    X_test_scaled[numeric_cols] = scaler.transform(X_test[numeric_cols])

    log_reg = LogisticRegression(max_iter=2000, class_weight="balanced", random_state=42, C=0.1)
    log_reg.fit(X_train_scaled, y_train)
    results_lr = evaluate("Logistic Regression (class_weight=balanced)", log_reg, X_test_scaled, y_test)

    # --- Modello 2: Random Forest ---
    # Meno interpretabile direttamente, ma gestisce meglio interazioni
    # non lineari tra feature. Stesso class_weight per correttezza del confronto.
    rf = RandomForestClassifier(
        n_estimators=200, class_weight="balanced", random_state=42, max_depth=10
    )
    rf.fit(X_train, y_train)
    results_rf = evaluate("Random Forest (class_weight=balanced)", rf, X_test, y_test)

    # --- Feature importance (solo Random Forest, è nativo) ---
    importances = pd.Series(rf.feature_importances_, index=X_train.columns)
    top_features = importances.sort_values(ascending=False).head(10)
    print("\n=== Top 10 feature più importanti (Random Forest) ===")
    print(top_features.round(4))

    # --- Riepilogo comparativo ---
    summary = pd.DataFrame([results_lr, results_rf])
    print("\n=== Riepilogo comparativo ===")
    print(summary.round(3).to_string(index=False))
    summary.to_csv("data/gold/model_comparison.csv", index=False)


if __name__ == "__main__":
    main()