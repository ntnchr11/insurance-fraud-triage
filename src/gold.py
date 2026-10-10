"""
Fase 2 (continua) - Modeling table e KPI aggregates (gold layer).

Uso:
    python3 src/gold.py
"""

import pandas as pd
from sklearn.model_selection import train_test_split

TARGET = "is_fraud"


def main():
    df = pd.read_parquet("data/silver/claims_silver.parquet")

    # --- KPI aggregates per il layer di prodotto ---
    # Calcolati PRIMA dell'encoding, quando le categorie sono ancora leggibili
    kpi_cols = ["VehicleCategory", "BasePolicy", "AccidentArea"]
    kpi_rows = []
    for col in kpi_cols:
        rates = df.groupby(col)[TARGET].agg(["mean", "count"]).reset_index()
        rates.columns = ["categoria_valore", "tasso_frode", "n_sinistri"]
        rates.insert(0, "dimensione", col)
        kpi_rows.append(rates)
    kpi_table = pd.concat(kpi_rows, ignore_index=True)
    kpi_table["tasso_frode"] = (kpi_table["tasso_frode"] * 100).round(1)
    kpi_table.to_csv("data/gold/kpi_fraud_rate.csv", index=False)
    print(f"Salvato data/gold/kpi_fraud_rate.csv ({len(kpi_table)} righe)")

    # --- Modeling table ---
    categorical_cols = [c for c in df.columns if df[c].dtype == "object"]

    # drop_first=True evita la "trappola delle variabili dummy": se una categoria
    # ha N valori possibili, bastano N-1 colonne per rappresentarla senza
    # ridondanza (l'ultima è implicita quando tutte le altre sono 0).
    df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

    X = df_encoded.drop(columns=[TARGET])
    y = df_encoded[TARGET]

    # stratify=y: con solo il 6% di frodi, uno split casuale "normale" rischia
    # di lasciare pochissimi casi di frode nel test set, rendendo la valutazione
    # inaffidabile. stratify mantiene la stessa proporzione di frodi in
    # train e test.
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    train_df = X_train.copy()
    train_df[TARGET] = y_train
    test_df = X_test.copy()
    test_df[TARGET] = y_test

    train_df.to_parquet("data/gold/claims_train.parquet", index=False)
    test_df.to_parquet("data/gold/claims_test.parquet", index=False)

    print(f"\nTrain set: {len(train_df):,} righe, tasso frode {y_train.mean():.1%}")
    print(f"Test set:  {len(test_df):,} righe, tasso frode {y_test.mean():.1%}")
    print(f"Feature totali dopo l'encoding: {X.shape[1]}")


if __name__ == "__main__":
    main()