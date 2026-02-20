# Security Assessment Report
## Applicazione E-Commerce — Analisi delle Minacce e Piano di Risposta

---

| Campo | Dettaglio |
|---|---|
| **Documento** | Security Assessment Report |
| **Oggetto** | Applicazione Web E-Commerce |
| **Classificazione** | Riservato |
| **Data** | Febbraio 2026 |
| **Versione** | 1.0 |

---

## Sommario Esecutivo

Il presente documento riporta i risultati dell'assessment di sicurezza condotto sull'infrastruttura dell'applicazione web di e-commerce. L'analisi ha preso in esame l'architettura di rete esistente, con particolare attenzione alla DMZ esposta su Internet, e ha identificato tre scenari di rischio principali: attacchi applicativi di tipo SQLi e XSS, attacchi volumetrici DDoS con impatto sulla disponibilità del servizio, e infezione da malware con rischio di propagazione laterale alla rete interna.

Per ciascuno scenario vengono proposte misure preventive, una quantificazione dell'impatto economico ove applicabile, e un piano di risposta agli incidenti. Il documento si conclude con una soluzione architetturale integrata che unifica le contromisure identificate.

---

## 1. Architettura di Riferimento

### 1.1 Descrizione dell'infrastruttura

L'architettura analizzata è composta dai seguenti elementi:

- **Internet / utenti esterni**: accesso pubblico all'applicazione tramite browser
- **Firewall perimetrale**: unico punto di controllo tra la zona pubblica, la DMZ e la rete interna
- **DMZ**: ospita il server dell'applicazione e-commerce, accessibile sia dall'esterno (utenti e attaccanti) che dall'interno
- **Rete interna**: contiene i sistemi degli sviluppatori e i server di backend; raggiungibile dalla DMZ per policy firewall

### 1.2 Vulnerabilità architetturale identificata

La criticità principale risiede nel fatto che la rete interna è raggiungibile direttamente dalla DMZ tramite policy sul firewall. Di conseguenza, qualsiasi compromissione del server in DMZ potrebbe consentire a un attaccante di effettuare movimenti laterali verso i sistemi interni, amplificando significativamente l'impatto di un eventuale incidente.

---

## 2. Azioni Preventive — Attacchi SQLi e XSS

### 2.1 Descrizione delle minacce

**SQL Injection (SQLi)** è una tecnica di attacco che consente a un attore malevolo di manipolare le query SQL eseguite dal backend dell'applicazione inserendo codice SQL arbitrario nei campi di input. Un attacco SQLi riuscito può portare a esfiltrazione di dati, bypass dell'autenticazione o distruzione del database.

**Cross-Site Scripting (XSS)** consente all'attaccante di iniettare codice JavaScript malevolo nelle pagine web visualizzate dagli utenti. Può essere utilizzato per furto di sessioni, reindirizzamento a siti fraudolenti o distribuzione di malware agli utenti della piattaforma.

### 2.2 Misure preventive raccomandate

#### Web Application Firewall (WAF)

Il WAF deve essere posizionato tra il firewall perimetrale e il server applicativo in DMZ, operando al livello 7 del modello OSI. Il WAF analizza il traffico HTTP/HTTPS in ingresso e blocca le richieste contenenti pattern malevoli tipici di SQLi (es. `' OR 1=1 --`) e XSS (es. `<script>alert()</script>`), prima che queste raggiungano l'applicazione.

**Posizionamento**: DMZ, inline tra firewall e server e-commerce.

#### Input Validation e Output Encoding

A livello applicativo, è fondamentale implementare una validazione rigorosa di tutti i dati in ingresso. Per SQLi, l'adozione di **Prepared Statements** (query parametrizzate) elimina la possibilità di iniezione SQL, disaccoppiando il codice SQL dai dati forniti dall'utente. Per XSS, l'**output encoding** contestuale (HTML encoding, JavaScript encoding) garantisce che il contenuto dinamico non venga interpretato come codice eseguibile dal browser.

#### Content Security Policy (CSP)

L'implementazione di header HTTP **Content-Security-Policy** consente di definire una whitelist di sorgenti da cui il browser è autorizzato a caricare script, stili e risorse. Questo riduce drasticamente la superficie di attacco per XSS di tipo DOM-based e reflected, impedendo l'esecuzione di script non autorizzati anche in caso di iniezione riuscita.

### 2.3 Sintesi delle contromisure

| Contromisura | Tipo di attacco mitigato | Livello di applicazione |
|---|---|---|
| WAF | SQLi, XSS | Rete / Infrastruttura |
| Prepared Statements | SQLi | Applicazione / Codice |
| Output Encoding | XSS | Applicazione / Codice |
| Content Security Policy | XSS | Browser / HTTP Header |

---

## 3. Impatto sul Business — Attacco DDoS

### 3.1 Descrizione della minaccia

Un attacco **Distributed Denial of Service (DDoS)** mira a rendere un servizio irraggiungibile saturando le risorse della rete o del server con un volume di traffico abnorme, generato da una rete distribuita di macchine compromesse (botnet). In questo scenario, l'applicazione e-commerce risulta non disponibile per una durata di 10 minuti.

### 3.2 Calcolo dell'impatto economico

Dati forniti:
- Spesa media per minuto sulla piattaforma: **€ 1.500**
- Durata del disservizio: **10 minuti**

**Impatto economico diretto:**

```
Impatto = Durata (min) × Perdita per minuto (€)
Impatto = 10 × 1.500 €
Impatto = 15.000 €
```

Il valore di **€ 15.000** rappresenta il mancato ricavo diretto imputabile alla non disponibilità del servizio. A questa cifra vanno aggiunti i costi indiretti, tipicamente non quantificabili in modo immediato:

- **Danno reputazionale**: perdita di fiducia da parte degli utenti che hanno tentato di accedere al servizio senza successo
- **Abbandono del carrello**: utenti che non completano l'acquisto anche dopo il ripristino del servizio
- **Costi di risposta all'incidente**: ore uomo del team tecnico impegnate nel mitigare l'attacco
- **Potenziali penali contrattuali**: in caso di SLA con partner o marketplace

### 3.3 Azioni preventive contro DDoS

**CDN con protezione DDoS integrata** (es. Cloudflare, AWS Shield, Akamai): posizionata a monte del firewall, la CDN assorbe il traffico volumetrico distribuendo le richieste su una rete globale di PoP (Point of Presence). Questa soluzione è in grado di mitigare attacchi da centinaia di Gbps senza impattare il traffico legittimo.

**Rate limiting**: implementazione di regole sul firewall e a livello applicativo che limitano il numero di richieste accettate per IP in un determinato intervallo di tempo, riducendo l'efficacia degli attacchi a bassa intensità.

**Auto-scaling delle risorse**: architetture cloud-native con scalabilità automatica permettono di assorbire picchi di traffico anomali, aumentando temporaneamente la capacità computazionale del servizio.

**Anycast routing**: distribuzione del traffico su più data center geograficamente distribuiti, riducendo l'impatto di attacchi localizzati.

---

## 4. Incident Response — Infezione da Malware

### 4.1 Scenario

Il server dell'applicazione e-commerce in DMZ viene infettato da un malware. L'obiettivo prioritario è **impedire la propagazione del malware alla rete interna**, mantenendo al contempo attivo l'accesso dell'attaccante alla macchina infetta (es. per attività di forensics o per non allertare l'attaccante prima di aver raccolto le evidenze necessarie).

### 4.2 Piano di risposta

#### Fase 1 — Rilevamento e Classificazione

Identificazione dell'infezione tramite gli strumenti di monitoraggio (SIEM, IDS/IPS, log del firewall). Classificazione dell'incidente in base alla natura del malware e alla sua potenziale capacità di movimento laterale.

#### Fase 2 — Contenimento (priorità massima)

L'azione immediata consiste nell'**isolare il server infetto** modificando le policy del firewall in modo da bloccare completamente il traffico tra la DMZ e la rete interna. Nello specifico:

- Rimozione o disabilitazione di tutte le regole firewall che consentono la comunicazione DMZ → Rete Interna
- Mantenimento attivo del traffico Internet → DMZ per non allertare l'attaccante
- Il server entra in uno stato di **quarantena di rete**: isolato lateralmente ma ancora raggiungibile dall'esterno

Questa procedura implementa di fatto una **rete di quarantena**, che consente di contenere l'incidente senza spegnere il sistema, preservando le evidenze forensi.

#### Fase 3 — Analisi (in parallelo al contenimento)

Con il server in quarantena, il team di sicurezza procede all'analisi del malware: tipologia, vettore di infezione, attività svolta, dati potenzialmente esfiltrati. Questa fase può avvalersi di tecniche di **threat hunting** e analisi dei log per ricostruire la timeline dell'attacco.

#### Fase 4 — Eradicazione e Ripristino (fuori scope di questo scenario)

Una volta conclusa l'analisi forense e raccolte le evidenze, si procede alla bonifica del sistema, al ripristino da backup e al rafforzamento delle difese per prevenire recidive.

### 4.3 Modifica all'architettura di rete

| Elemento | Stato prima | Stato dopo |
|---|---|---|
| Regola firewall DMZ → Rete Interna | Attiva | **Disabilitata** |
| Traffico Internet → DMZ | Attivo | Attivo (invariato) |
| Server e-commerce | Operativo | **In quarantena di rete** |
| Accesso attaccante al server | — | **Mantenuto** (by design) |

---

## 5. Soluzione Completa — Architettura Integrata

### 5.1 Descrizione

La soluzione completa unisce le misure preventive contro SQLi/XSS (punto 2) con il piano di contenimento del malware (punto 4), producendo un'architettura di sicurezza difensiva a più livelli, coerente con il principio di **Defense in Depth**.

### 5.2 Componenti della soluzione integrata

**Livello 1 — Perimetro Internet (CDN/DDoS Protection)**
Una CDN con protezione DDoS integrata viene posizionata a monte del firewall. Tutto il traffico proveniente da Internet, sia quello degli utenti legittimi che quello degli attaccanti, transita obbligatoriamente per questo layer, che filtra il traffico volumetrico anomalo prima che raggiunga l'infrastruttura.

**Livello 2 — Firewall Perimetrale con Policy Rafforzate**
Il firewall mantiene il suo ruolo centrale, con policy aggiornate che includono il blocco esplicito di qualsiasi comunicazione dalla DMZ verso la rete interna. Questa regola, introdotta nella fase di risposta all'incidente, diventa una policy permanente dell'architettura.

**Livello 3 — WAF in DMZ**
Il Web Application Firewall viene inserito inline tra il firewall e il server applicativo. Analizza il traffico HTTP/HTTPS e blocca i payload malevoli tipici di SQLi e XSS prima che raggiungano l'applicazione.

**Livello 4 — Applicazione E-Commerce (hardening)**
A livello di codice applicativo vengono implementati Prepared Statements, output encoding e header CSP, garantendo una protezione residua anche qualora un payload riuscisse a superare i layer infrastrutturali.

### 5.3 Schema dei flussi nell'architettura integrata

```
[Attaccante / Utenti]
        |
        ▼
[CDN + DDoS Protection]   ← Mitiga attacchi volumetrici
        |
        ▼
[Firewall]                ← Policy: BLOCCO DMZ → Rete Interna
     |       |
     |       ▼
     |   [Rete Interna]   ← Isolata dalla DMZ
     |
     ▼
[WAF]                     ← Blocca SQLi e XSS
     |
     ▼
[App E-Commerce / DMZ]    ← Input Validation + CSP
```

### 5.4 Riepilogo delle contromisure per scenario

| Scenario | Contromisura | Livello |
|---|---|---|
| SQLi | WAF + Prepared Statements | Infrastruttura + Applicazione |
| XSS | WAF + Output Encoding + CSP | Infrastruttura + Applicazione |
| DDoS | CDN + Rate Limiting + Auto-scaling | Perimetro |
| Malware / Propagazione | Blocco firewall DMZ→Interno + Quarantena | Rete |

---

## 6. Conclusioni e Raccomandazioni

L'analisi ha evidenziato come l'architettura iniziale presenti un rischio significativo legato alla comunicazione diretta tra DMZ e rete interna, che in caso di compromissione del server esporrebbe l'intera infrastruttura a movimenti laterali dell'attaccante. L'impatto economico di un singolo evento DDoS di soli 10 minuti è quantificabile in **€ 15.000 di mancato ricavo diretto**, a cui si aggiungono costi indiretti difficilmente quantificabili.

Le principali raccomandazioni in ordine di priorità sono le seguenti. In prima istanza, si raccomanda di rivedere immediatamente le policy firewall per eliminare le regole che consentono comunicazioni dirette dalla DMZ verso la rete interna. In seconda istanza, si suggerisce di implementare un WAF davanti all'applicazione per mitigare attacchi applicativi di tipo SQLi e XSS. In terza istanza, si consiglia di valutare l'adozione di una CDN con protezione DDoS per ridurre l'esposizione ad attacchi volumetrici e il relativo impatto economico. Infine, si raccomanda di avviare un processo di code review dell'applicazione e-commerce per garantire l'adozione di Prepared Statements e pratiche di output encoding in tutto il codebase.

L'implementazione di queste misure in modo coordinato consente di costruire un'architettura di sicurezza stratificata, in cui la compromissione di un singolo livello non è sufficiente a compromettersi l'intera infrastruttura.

---

*Documento prodotto a fini di assessment della sicurezza. Classificazione: Riservato.*
