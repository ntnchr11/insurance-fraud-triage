# PRD — Coda di triage per sinistri a rischio frode

## Problema

Oggi i sinistri vengono revisionati senza una priorità guidata dai dati. Con un tasso di frode storico del 6% (923 casi su 15.420 nel dataset di riferimento), un investigatore che lavora senza segnale rischia di distribuire tempo uniformemente su tutti i sinistri, invece di concentrarsi su quelli a rischio più alto.

## Proposta

Un modello di classificazione (Random Forest) assegna a ogni sinistro appena aperto un punteggio di probabilità di frode. I sinistri con punteggio sopra una soglia configurabile entrano in una coda di revisione prioritaria.

## Utenti

Investigatori antifrode e team claims che gestiscono la revisione dei sinistri.

## Come funziona la soglia di decisione

Il modello è stato validato su un test set di 3.084 sinistri (185 frodi reali). Due configurazioni possibili:

| Strategia | Soglia | Sinistri segnalati | Frodi catturate | Precision |
|---|---|---|---|---|
| **Rete larga** (consigliata in fase di lancio) | 0.50 | 33.5% del totale | 78.9% delle frodi vere | 0.141 |
| **Rete focalizzata** (se il team ha capacità limitata) | 0.60 | 11.7% del totale | 35.7% delle frodi vere | 0.183 |

Con la strategia "rete larga", su un volume di 1.000 sinistri mensili, il team riceverebbe circa 335 segnalazioni, di cui circa 47 sarebbero frodi reali (basato sulla precision osservata). È un carico di lavoro sostanzialmente più gestibile rispetto a una revisione non prioritizzata su tutti i 1.000 casi.

## Metriche di successo

- % di frodi confermate intercettate dalla coda nei primi 90 giorni (target: mantenere il recall osservato in validazione, ~79%)
- Precision realizzata sul campo (quante segnalazioni si confermano frodi dopo investigazione)
- Ore investigative dedicate alla coda prioritaria vs. revisione non guidata, a parità di frodi intercettate

## Rischi e trade-off

- **Falsi positivi**: anche nella configurazione più conservativa, circa 1 segnalazione su 5-7 è un falso positivo. Serve comunicare chiaramente al team che il punteggio è un supporto alla priorità, non una sentenza.
- **Instabilità del modello a soglie estratte**: in fase di sviluppo si è osservato che un modello alternativo (Logistic Regression) produceva stime di probabilità non affidabili a soglie molto alte (sopra 0.85), per un fenomeno di quasi-separazione statistica legato a variabili categoriche rare. Il Random Forest, scelto per la produzione, non presenta questo problema, ma è un promemoria che ogni soglia scelta va validata, non solo ereditata dal training.
- **Drift nel tempo**: comportamenti fraudolenti ed economia del settore cambiano; serve un piano di retraining periodico e monitoraggio delle metriche su dati nuovi.

## Roadmap minima

1. **MVP**: punteggio di rischio + coda ordinata con soglia "rete larga" (0.50)
2. **Iterazione 1**: soglia regolabile dal team in base alla capacità operativa reale; spiegazione del punteggio per singolo sinistro (quali fattori hanno pesato di più)
3. **Iterazione 2**: monitoraggio del drift (il tasso di frode osservato si allontana da quello storico?) e retraining periodico