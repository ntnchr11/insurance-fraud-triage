"""
Fase 2 - Pulizia e arricchimento (silver layer).

Uso:
    python3 src/silver.py
"""

import pandas as pd

TARGET_RAW = "FraudFound_P"
TARGET_STD = "is_fraud"

# Colonne che sono identificativi o rumore, non segnale predittivo:
# - PolicyNumber: identificativo univoco, nessun valore informativo per il modello
# - RepNumber: identificativo dell'incaricato che gestisce il sinistro
# - Year: il dataset copre solo 3 anni, tenerlo rischia di far "memorizzare"
#   al modello un pattern legato a quegli anni specifici invece di un pattern
#   generalizzabile
DROP_COLS = ["PolicyNumber", "RepNumber", "Year"]


def main():
    df = pd.read_parquet("data/bronze/claims_bronze.parquet")
    print(f"Righe in ingresso: {len(df):,}")

    # 1. Standardizza il nome della colonna target
    df = df.rename(columns={TARGET_RAW: TARGET_STD})

    # 2. Rimuove le colonne non informative
    df = df.drop(columns=[c for c in DROP_COLS if c in df.columns])

    # 3. Gestione esplicita dei valori mancanti (se ce ne sono)
    #    Non si eliminano righe in silenzio: si marca esplicitamente cosa manca.
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    categorical_cols = [c for c in df.columns if c not in numeric_cols and c != TARGET_STD]

    for col in numeric_cols:
        n_missing = df[col].isna().sum()
        if n_missing > 0:
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val)
            print(f"  {col}: {n_missing} valori mancanti riempiti con la mediana ({median_val})")

    for col in categorical_cols:
        n_missing = df[col].isna().sum()
        if n_missing > 0:
            df[col] = df[col].fillna("Sconosciuto")
            print(f"  {col}: {n_missing} valori mancanti marcati come 'Sconosciuto'")

    print(f"\nColonne numeriche: {numeric_cols}")
    print(f"Colonne categoriche: {categorical_cols}")

    output_path = "data/silver/claims_silver.parquet"
    df.to_parquet(output_path, index=False)
    print(f"\nSalvato livello silver in: {output_path} ({len(df):,} righe, {df.shape[1]} colonne)")


if __name__ == "__main__":
    main()