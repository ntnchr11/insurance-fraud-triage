import pandas as pd

df = pd.read_parquet("data/bronze/claims_bronze.parquet")

categorical_cols = [
    "Fault", "VehicleCategory", "BasePolicy", "AccidentArea",
    "PolicyType", "PoliceReportFiled", "WitnessPresent", "AgentType",
]

print("Tasso di frode per categoria (attenzione a valori vicini a 0% o 100%: possibile leakage):\n")
for col in categorical_cols:
    print(f"--- {col} ---")
    rates = df.groupby(col)["FraudFound_P"].agg(["mean", "count"])
    rates["mean"] = (rates["mean"] * 100).round(1)
    print(rates.rename(columns={"mean": "tasso_frode_%", "count": "n_sinistri"}))
    print()