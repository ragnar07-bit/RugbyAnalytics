# Contributing

Grazie per l'interesse a contribuire a questo progetto. Di seguito trovi le linee guida pratiche per aprire issue, proporre funzionalità o inviare pull request.

## Prima di iniziare
- Leggi il `README.md` per comprendere l'architettura (C# backend, Python frontend, SQLite).
- Verifica che la tua proposta sia compatibile con la Licenza MIT.
- Controlla se è già aperta un'issue o una PR relativa alla tua idea.

## Segnalare bug o richiedere funzionalità
- Apri una nuova issue con:
	- Titolo chiaro e descrittivo.
	- Descrizione dettagliata del problema o della proposta.
	- Passi per riprodurre il bug (se applicabile), output atteso e output ottenuto.
	- Informazioni sull'ambiente (OS, versione .NET/Python, log rilevanti).
- Per nuove funzionalità, spiega il caso d'uso e i benefici attesi.

## Flusso consigliato per contribuire
1. Forka il repository.
2. Crea un branch nuovo e descrittivo:
	 - `feature/nome-funzionalita`
	 - `fix/descrizione-bug`
3. Implementa le modifiche con commit piccoli e leggibili.
4. Aggiorna la documentazione (`README.md`, eventuali guide).
5. Esegui test locali e verifica i comandi di avvio.
6. Apri una Pull Request verso il branch principale del repository originale, indicando issue correlate, descrizione delle modifiche e eventuali screenshot/log.

## Stile e formattazione del codice
- **C#**:
	- Segui le convenzioni .NET (PascalCase per classi e metodi pubblici).
	- Preferisci `async`/`await` per operazioni asincrone.
	- Usa `dotnet format` quando possibile.
- **Python**:
	- Mantieni compatibilità con Python 3.10+.
	- Usa `black` per il formato e `isort` per gli import.
- **SQL**:
	- Utilizza query parametrizzate per prevenire SQL injection.
- **Commit**:
	- Messaggi chiari e concisi (inglese o italiano accettati).

## Comandi utili per sviluppo locale
```bash
# Server C#
cd rugby_analytics_server
dotnet run

# Client Python
cd rugby_analytics_client
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

## Test e qualità
- Aggiungi test automatici quando possibile.
- **C#**: usa `dotnet test` se presenti progetti di test.
- **Python**: usa `pytest` per test unitari.
- Esegui linter/format prima di aprire la PR.

## Checklist per la Pull Request
- [ ] Il codice è stato testato localmente.
- [ ] Nessun errore di formattazione (rispettare `black`/`dotnet format`).
- [ ] Documentazione aggiornata se necessario.
- [ ] La PR include descrizione chiara e riferimenti a issue correlati.

## Comunicazione
- Usa le issue per discussioni tecniche e le PR per proposte di modifica.
- Se serve, indica contatti o canali (es. email istituzionali) nella repository.

## Codice di condotta
- Mantieni rispetto e comportamento collaborativo.
- Commenti offensivi, discriminatori o molesti non saranno tollerati.

Grazie per il tuo contributo — ogni miglioramento è apprezzato!