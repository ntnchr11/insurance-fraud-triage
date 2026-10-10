"""
Fase 1 - Ingestion e validazione del dato grezzo (bronze layer).

Uso:
    python src/ingest.py --input data/raw/claims_raw.csv

Cosa fa:
    1. Carica il CSV grezzo
    2. Controlla dimensioni, duplicati, valori mancanti per colonna
    3. Se src/config_columns.yaml è compilato, verifica che la colonna
       target esista e stampa il bilanciamento delle classi (frode vs non frode)
    4. Rimuove i duplicati esatti e salva il risultato in data/bronze/

Questo script non fa feature engineering: quello è compito dello
script di silver (fase successiva, da scrivere dopo aver esplorato il dato).
"""

import argparse
from pathlib import Path

import pandas as pd
import yaml


def load_column_config(config_path: Path) -> dict:
    if not config_path.exists():
        return {}
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def profile_raw_data(df: pd.DataFrame) -> None:
    print(f"\nRighe: {len(df):,} | Colonne: {df.shape[1]}")
    print(f"Righe duplicate esatte: {df.duplicated().sum():,}")

    missing = df.isna().sum()
    missing = missing[missing > 0].sort_values(ascending=False)
    if len(missing) > 0:
        print("\nValori mancanti per colonna:")
        for col, n in missing.items():
            print(f"  {col}: {n:,} ({n / len(df):.1%})")
    else:
        print("\nNessun valore mancante rilevato.")

    print("\nColonne disponibili nel file:")
    for col in df.columns:
        print(f"  - {col}")


def check_target_balance(df: pd.DataFrame, config: dict) -> None:
    target_cfg = config.get("target", {})
    raw_col = target_cfg.get("raw", "")

    if not raw_col:
        print(
            "\nAttenzione: src/config_columns.yaml non ha ancora il campo "
            "'target.raw' compilato. Apri il CSV, trova la colonna che indica "
            "la frode, e completala per vedere qui il bilanciamento delle classi."
        )
        return

    if raw_col not in df.columns:
        print(
            f"\nAttenzione: la colonna '{raw_col}' indicata in config_columns.yaml "
            f"non è presente nel file. Colonne disponibili sopra: controlla il nome esatto."
        )
        return

    counts = df[raw_col].value_counts(dropna=False)
    total = len(df)
    print(f"\nBilanciamento della colonna target '{raw_col}':")
    for value, n in counts.items():
        print(f"  {value}: {n:,} ({n / total:.1%})")


def main():
    parser = argparse.ArgumentParser(description="Ingestion e validazione dato grezzo")
    parser.add_argument(
        "--input", default="data/raw/claims_raw.csv", help="Percorso del CSV grezzo"
    )
    parser.add_argument(
        "--output", default="data/bronze/claims_bronze.parquet",
        help="Percorso di output per il livello bronze"
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(
            f"Non trovo il file '{input_path}'.\n"
            "Scarica il dataset seguendo docs/data_dictionary.md e mettilo in data/raw/."
        )
        return

    df = pd.read_csv(input_path)
    profile_raw_data(df)

    config = load_column_config(Path("src/config_columns.yaml"))
    check_target_balance(df, config)

    before = len(df)
    df_clean = df.drop_duplicates()
    removed = before - len(df_clean)
    if removed > 0:
        print(f"\nRimosse {removed:,} righe duplicate esatte.")

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df_clean.to_parquet(output_path, index=False)
    print(f"\nSalvato livello bronze in: {output_path}")


if __name__ == "__main__":
    main()
