# Dataset e data dictionary

## Dataset consigliato

**Vehicle Claim Fraud Detection** (Kaggle, utente shivamb)
https://www.kaggle.com/datasets/shivamb/vehicle-claim-fraud-detection

È la versione più diffusa del dataset storico del settore (deriva dal "carclaims.csv" di Angoss Knowledge Seeker), citato in più lavori accademici, compreso uno studio del 2025 sul *Journal of Risk and Insurance* che confronta modelli ML e DL proprio su questo tipo di dato. Circa 15-16mila sinistri, con la colonna target che indica se il sinistro è stato segnalato come fraudolento (nel dataset storico si chiama `FraudFound_P`).

**Nota onesta**: non ho un accesso diretto a Kaggle da questo ambiente per scaricare il file e confermarti lo schema esatto delle colonne. Le fonti che ho trovato concordano su circa 32 colonne, con informazioni su assicurato, veicolo, tipo di incidente e importo del sinistro, ma i nomi precisi delle colonne vanno verificati sul file che scarichi tu. È il primo vero compito della Fase 1: apri il CSV, guarda le colonne, e aggiornale in `src/config_columns.yaml`.

## Alternativa più "pulita"

Se preferisci uno schema più leggibile da subito (nomi di colonna espliciti tipo `policy_id`, `incident_type`, `claim_amount`, `fraud_reported`), c'è anche:
https://www.kaggle.com/datasets/ahluwaliasaksham/car-insurance-fraud-detection-dataset

È un dataset più recente, meno citato in letteratura accademica ma più comodo per un primo giro. Puoi anche usarlo come confronto nella sezione "Limiti e sviluppi futuri" del paper.

## Come scaricarlo

Serve un account Kaggle gratuito.

1. Vai sulla pagina del dataset scelto, premi "Download"
2. Estrai il CSV e rinominalo in modo chiaro, per esempio `claims_raw.csv`
3. Mettilo in `data/raw/claims_raw.csv`

In alternativa, se nel tuo ambiente locale di Claude Code hai configurato le credenziali Kaggle (`~/.kaggle/kaggle.json`), puoi automatizzare il download con:

```bash
pip install kaggle
kaggle datasets download -d shivamb/vehicle-claim-fraud-detection -p data/raw --unzip
```

## Dopo il download

Apri `src/config_columns.yaml` e compila la mappatura tra i nomi di colonna reali del file e i nomi standardizzati che la pipeline userà da qui in poi. Questo passaggio tiene la pipeline indipendente da quale dei due dataset sceglierai.
