# RugbyAnalytics PRO v1.0.0-Stable

[![Platform](https://img.shields.io/badge/Platform-Fedora%20Linux%20%7C%20Windows-blue?style=flat-square&logo=linux)](https://getfedora.org/)
[![Backend](https://img.shields.io/badge/Backend-C%23%20.NET%208-purple?style=flat-square&logo=dotnet)](https://dotnet.microsoft.com/)
[![Frontend](https://img.shields.io/badge/Frontend-Python%203-yellow?style=flat-square&logo=python)](https://www.python.org/)
[![Database](https://img.shields.io/badge/Database-SQLite%203-emerald?style=flat-square&logo=sqlite)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square)](LICENSE)

**RugbyAnalytics PRO** è un sistema enterprise distribuito eterogeneo (cross-language) progettato per la digitalizzazione, la raccolta e l'analisi in tempo reale dei KPI (Key Performance Indicators) prestazionali di una squadra di rugby direttamente a bordo campo.

Il progetto nasce come framework applicativo per l'Esame di Stato, integrando in un'unica architettura disaccoppiata i pilastri fondamentali dei programmi ministeriali dell'indirizzo Informatica e Telecomunicazioni (ITIS).

---

## 📐 Architettura del Sistema & Interoperabilità

Il software implementa una **Separation of Concerns (SoC)** totale attraverso due macro-componenti indipendenti che comunicano sulla scheda di rete:

```
┌─────────────────────────────────┐               ┌─────────────────────────────────┐
│     CLIENT GRAFICO (Python)     │               │     SERVER CENTRALE (C#)        │
│  ─────────────────────────────  │  TCP Socket   │  ─────────────────────────────  │
│  - Interfaccia CustomTkinter    ├──────────────►│  - Threading Asincrono (TAP)    │
│  - Architettura MVVM locale     │  Length-Pref  │  - Business Logic Polimorfica   │
│  - Framing Big-Endian (struct)  │  Payload JSON │  - Data Persistence (SQLite)    │
└─────────────────────────────────┘               └─────────────────────────────────┘

```
1. **Backend Server (C# .NET 8):** Agisce come engine headless centralizzato ad alte prestazioni. Gestisce il multithreading asincrono, la validazione crittografica degli accessi, l'elaborazione dei KPI e la persistenza atomica su database relazionale locale.
2. **Frontend Client (Python 3):** Applicazione desktop nativa utilizzata dallo staff tecnico a bordo campo per la rilevazione immediata degli eventi di gara. Garantisce un'interfaccia utente altamente reattiva basata sul pattern architetturale MVVM.

### Lo Strato "Shared" Eterogeneo
Essendo un sistema cross-language, l'interoperabilità è garantita da un **contratto logico sul protocollo applicativo**. Lo scambio dei dati avviene tramite uno stream TCP proprietario con codifica del testo in formato **JSON standard**. Il framing dei messaggi applica la tecnica **Length-Prefixed Framing**: il client Python serializza e calcola la dimensione del pacchetto inserendo un Header standard di 4 byte (Big-Endian tramite modulo `struct`), che il Server C# decodifica (tramite `BitConverter`) per allocare linearmente i buffer di lettura ed evitare fenomeni di frammentazione o overlap dei dati.

---

## 📂 Struttura del Workspace (Clean Architecture)

```text
RugbyAnalytics_Ibrido/
│
├── rugby_analytics_server/         # BACKEND ENGINE (C# .NET 8)
│   ├── RugbyAnalyticsServer.csproj # File di configurazione di progetto .NET
│   ├── Program.cs                  # Entry point del ciclo di vita del Server
│   ├── Core/                       # Strato di Rete (TcpListener Asincrono - TPSIT)
│   ├── Database/                   # Strato di Persistenza (SQLite SQL parametrico - Informatica)
│   ├── Security/                   # Autenticazione e Cifratura (SHA-256 + Salt - Sistemi)
│   ├── Models/                     # DTO di Protocollo e Classi Polimorfiche (OOP)
│   └── rugby_analytics.db          # File di database relazionale ad allocazione dinamica
│
└── rugby_analytics_client/         # FRONTEND APPLICATION (Python 3)
	├── app.py                      # Bootstrapper dell'interfaccia grafica
	├── network/                    # Client Socket e serializzazione JSON adattiva
	├── views/                      # Layout grafici (CustomTkinter / PySide6)
	└── viewmodels/                 # Logica dello stato della GUI e Data Binding
```

## 🛠️ Mappatura delle Materie d'Esame (Syllabus ITIS)

- **TPSIT (Tecnologie e Progettazione di Sistemi Informatici e di Telecomunicazioni):** Implementazione del Socket di rete non-blocking. Gestione della concorrenza multi-client sul server tramite il paradigma TAP (`async`/`await` su `ThreadPool`), gestione delle problematiche di trasporto (Framing TCP) e manipolazione dei buffer di byte (Big-Endian vs Little-Endian).
- **Informatica:** Progettazione del database relazionale normalizzato in Terza Forma Normale (3NF), isolamento della persistenza tramite query SQL strutturate parametriche contro attacchi SQL Injection. Utilizzo della programmazione orientata agli oggetti (OOP) avanzata con astrazione e polimorfismo dinamico in C# per il calcolo differenziato degli indici di efficacia prestazionale dei reparti tattici (*Avanti* e *Trequarti*).
- **Sistemi e Reti:** Protezione degli accessi e controllo delle sessioni. Implementazione di un sistema di hashing unidirezionale asimmetrico **SHA-256** integrato con stringhe casuali crittograficamente sicure (**Salt**), abbinato a un algoritmo di verifica delle credenziali a tempo costante (*Constant-Time Verification*) per mitigare i rischi latenti di *Timing Attacks*.

## 🚀 Requisiti e Modalità di Avvio
Il sistema è nativamente cross-platform ed è stato sviluppato e collaudato all'interno di una workstation **Fedora Linux** utilizzando **Visual Studio Code**.

### Prerequisiti di Sistema

- .NET SDK 8.0 o superiore
- Python 3.10 o superiore

### 1. Esecuzione del Server (C#)
Il server autogenererà il file di database e le tabelle relazionali se non presenti al primo avvio.

Bash

```
cd rugby_analytics_server
dotnet run
```

All'avvio corretto, il terminale confermerà lo stato: `[INFO] Server C# .NET 8 in ascolto sulla porta 5000...`

### 2. Esecuzione del Client (Python)
Posizionarsi nella cartella del client, inizializzare l'ambiente virtuale e lanciare l'applicazione:

Bash

```
cd rugby_analytics_client
python3 -m venv .venv
source .venv/bin/activate  # Su Windows: .venv\\Scripts\\activate
pip install -r requirements.txt  # Installa librerie grafiche (es. customtkinter)
python app.py
```

## 🧑‍💻 Autore e Contributors
Il presente progetto software è stato interamente ideato, architettato e sviluppato come opera individuale da:

- **Candidato:** Cipriano Salvatore
- **Specializzazione:** Informatica e Telecomunicazioni
- **Ambiente di sviluppo:** Visual Studio Code su Fedora Linux

## 📄 Licenza
Questo progetto è distribuito sotto Licenza MIT - consultare il file [LICENSE](https://www.google.com/search?q=LICENSE) per ulteriori dettagli.

```
Questo file fornisce una panoramica strutturata ed estremamente pulita del progetto. Dimostra a chiunque visiti il tuo repository GitHub che dietro il codice c'è un'analisi ingegneristica rigorosa.
```