# Piano del progetto — guida fase per fase

Questo file è la mappa. Ogni fase spiega cosa fare, perché conta per il ruolo di **Junior Product Manager** e perché conta per il ruolo di **Data Scientist Fraud Detection**, così il lavoro serve a entrambi i colloqui con lo stesso sforzo.

## Fase 0 — Setup ambiente (fatta)

Struttura cartelle, README, requirements. Non c'è niente da imparare qui, solo da avere pronto.

## Fase 1 — Procurarsi e capire il dato (il tuo prossimo passo)

Cosa fare: scaricare il dataset indicato in `docs/data_dictionary.md`, aprirlo e guardare davvero le colonne, i tipi, quanti valori mancanti, quanti casi di frode rispetto al totale.

- **Lato Data Scientist**: prima di scrivere una riga di codice di modeling, un data scientist serio passa del tempo a capire cosa c'è davvero nel dato. Qui scoprirai lo sbilanciamento di classe (pochissime frodi rispetto ai casi regolari), che è il problema centrale di tutto il progetto.
- **Lato Product Manager**: questa è la stessa disciplina che serve quando raccogli requisiti: non fidarti della descrizione, guarda i dati reali prima di decidere cosa costruire.

## Fase 2 — Pipeline bronze → silver → gold

Cosa fare: scrivere gli script che portano il dato grezzo (bronze) a un dato pulito e arricchito (silver) e poi a tabelle pronte per l'analisi (gold).

- **Lato Data Scientist**: qui si fa feature engineering vero (per esempio: età della polizza al momento del sinistro, numero di sinistri precedenti, rapporto tra importo richiesto e premio annuo). Le feature buone contano più del modello scelto.
- **Lato Product Manager**: un'architettura a livelli è esattamente il tipo di decisione tecnica che un PM deve saper leggere e discutere con il team dati, anche senza scriverla lui stesso.

## Fase 3 — Analisi esplorativa (EDA)

Cosa fare: grafici e statistiche descrittive. Come si distribuisce l'importo dei sinistri? Ci sono pattern temporali (giorno della settimana, mese)? Quali variabili sembrano separare meglio i casi di frode?

- **Lato Data Scientist**: qui la tua laurea in fisica è un vantaggio diretto: distribuzioni, test di significatività, correlazioni vanno lette con occhio critico, non solo prodotte.
- **Lato Product Manager**: l'EDA è la stessa logica di un'analisi di mercato o di utilizzo prodotto, saper leggere un grafico e trarne una decisione.

## Fase 4 — Modeling

Cosa fare: almeno due modelli a confronto (per esempio un albero decisionale/logistic regression interpretabile e un ensemble come Random Forest), con class weighting o SMOTE per gestire lo sbilanciamento.

- **Lato Data Scientist**: qui dimostri di saper scegliere il modello giusto per il problema, non il più sofisticato in assoluto, e di saperlo giustificare.
- **Lato Product Manager**: il trade-off tra un modello interpretabile e uno più preciso ma opaco è una decisione di prodotto, non solo tecnica (un investigatore si fida di più di un modello che spiega perché).

## Fase 5 — Valutazione

Cosa fare: precision, recall, F1, curva PR-AUC. Capire quanti falsi positivi genera il modello a diverse soglie di decisione.

- **Lato Data Scientist**: su classi sbilanciate l'accuratezza mente, qui mostri di saperlo e di usare le metriche giuste.
- **Lato Product Manager**: la scelta della soglia è una decisione di business pura: più soglia bassa, più frodi catturate ma più lavoro manuale sprecato dagli investigatori su falsi positivi. Questo è il cuore della Fase 6.

## Fase 6 — Layer di prodotto

Cosa fare: scrivere `product/PRD_fraud_triage.md`, una specifica prodotto per uno strumento di triage che usa il punteggio del modello. Soglia scelta, stima di impatto (sinistri intercettati, ore di lavoro investigative stimate), metriche di successo, roadmap minima.

- **Lato Product Manager**: questo è il pezzo che la maggior parte dei portfolio tecnici non ha. Dimostra che sai tradurre un output di machine learning in una decisione di prodotto con numeri a supporto.
- **Lato Data Scientist**: dimostra che non ti fermi al modello, capisci l'impatto operativo di quello che costruisci, qualità rara e molto apprezzata.

## Fase 7 — Completare il "paper" (README)

Cosa fare: riempire le sezioni lasciate in sospeso nel README con risultati reali e la discussione.

## Fase 8 — Pubblicazione

Repo GitHub pubblico, eventualmente un post LinkedIn che segue lo stile che usi già per collegare fisica e lavoro, e un riferimento nel CV e nelle risposte di colloquio.

---

**Prossimo passo concreto**: apri `docs/data_dictionary.md`, segui le istruzioni per scaricare il dataset, e torna qui quando hai il file in `data/raw/`.
