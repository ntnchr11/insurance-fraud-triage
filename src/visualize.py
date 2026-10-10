"""
Fase 7 (parte grafica) - Figure per il paper e per il colloquio.

Uso:
    python3 src/visualize.py

Salva 3 immagini in docs/figures/:
    - fraud_rate_by_category.png
    - threshold_tradeoff.png
    - feature_importance.png
"""

import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_recall_curve

TARGET = "is_fraud"
FIGDIR = Path("docs/figures")
FIGDIR.mkdir(parents=True, exist_ok=True)

BLUE = "#2E6F95"
ORANGE = "#D97A28"
GREY = "#8A8F98"

plt.rcParams.update({
    "font.size": 11,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.edgecolor": GREY,
})


def fig_fraud_rate_by_category():
    silver = pd.read_parquet("data/silver/claims_silver.parquet")
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    for ax, col, title in zip(
        axes,
        ["BasePolicy", "Fault"],
        ["Tasso di frode per tipo di polizza", "Tasso di frode per responsabilità"],
    ):
        rates = (silver.groupby(col)[TARGET].mean() * 100).sort_values(ascending=True)
        bars = ax.barh(rates.index, rates.values, color=BLUE, height=0.6)
        ax.set_title(title, fontsize=11, loc="left")
        ax.set_xlabel("% sinistri fraudolenti")
        ax.grid(axis="x", color="#E3E5E8", linewidth=0.8, zorder=0)
        ax.set_axisbelow(True)
        for bar, value in zip(bars, rates.values):
            ax.text(value + 0.2, bar.get_y() + bar.get_height() / 2,
                    f"{value:.1f}%", va="center", fontsize=9)
        ax.set_xlim(0, rates.values.max() * 1.25)

    fig.suptitle("Quali categorie concentrano il rischio di frode", fontsize=13, y=1.03)
    fig.tight_layout()
    fig.savefig(FIGDIR / "fraud_rate_by_category.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Salvato {FIGDIR / 'fraud_rate_by_category.png'}")


def fig_threshold_tradeoff():
    train = pd.read_parquet("data/gold/claims_train.parquet")
    test = pd.read_parquet("data/gold/claims_test.parquet")
    X_train, y_train = train.drop(columns=[TARGET]), train[TARGET]
    X_test, y_test = test.drop(columns=[TARGET]), test[TARGET]

    rf = RandomForestClassifier(n_estimators=200, class_weight="balanced", random_state=42, max_depth=10)
    rf.fit(X_train, y_train)
    proba = rf.predict_proba(X_test)[:, 1]

    precision, recall, thresholds = precision_recall_curve(y_test, proba)
    precision, recall = precision[:-1], recall[:-1]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(thresholds, recall, color=BLUE, linewidth=2, label="% frodi catturate (recall)")
    ax.plot(thresholds, precision, color=ORANGE, linewidth=2, label="Precision")

    for t, label in [(0.50, "rete larga"), (0.60, "rete focalizzata")]:
        ax.axvline(t, color=GREY, linestyle="--", linewidth=1)
        ax.text(t + 0.01, 0.95, label, fontsize=9, color=GREY, rotation=90, va="top")

    ax.set_xlabel("Soglia di decisione")
    ax.set_ylabel("Valore (0-1)")
    ax.set_title("Il trade-off tra frodi catturate e precisione, al variare della soglia", loc="left")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.grid(color="#E3E5E8", linewidth=0.8)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, loc="upper right")

    fig.tight_layout()
    fig.savefig(FIGDIR / "threshold_tradeoff.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Salvato {FIGDIR / 'threshold_tradeoff.png'}")

    return rf, X_train.columns


def fig_feature_importance(rf, feature_names):
    importances = pd.Series(rf.feature_importances_, index=feature_names)
    top = importances.sort_values(ascending=True).tail(10)

    fig, ax = plt.subplots(figsize=(7, 5))
    bars = ax.barh(top.index, top.values, color=BLUE, height=0.6)
    ax.set_title("Le 10 feature più predittive (Random Forest)", loc="left")
    ax.set_xlabel("Importanza relativa")
    ax.grid(axis="x", color="#E3E5E8", linewidth=0.8)
    ax.set_axisbelow(True)
    for bar, value in zip(bars, top.values):
        ax.text(value + 0.002, bar.get_y() + bar.get_height() / 2,
                f"{value:.3f}", va="center", fontsize=9)

    fig.tight_layout()
    fig.savefig(FIGDIR / "feature_importance.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Salvato {FIGDIR / 'feature_importance.png'}")


def main():
    fig_fraud_rate_by_category()
    rf, feature_names = fig_threshold_tradeoff()
    fig_feature_importance(rf, feature_names)


if __name__ == "__main__":
    main()