# Brutus.py

Brutus.py è uno strumento progettato per testare la sicurezza dei servizi SSH attraverso diverse modalità di attacco basate su combinazioni di username e password.  
Il programma permette sia l’utilizzo diretto di credenziali singole, sia l’impiego di wordlist per generare automaticamente tutte le combinazioni possibili.  
L’obiettivo è fornire un metodo semplice e controllato per verificare la robustezza di un servizio SSH in un contesto autorizzato.

> ⚠️ **Attenzione**  
> L’utilizzo di questo tool è consentito esclusivamente su sistemi per cui si dispone di esplicita autorizzazione.  
> L’autore non è responsabile per eventuali usi impropri o illegali.

---

## Funzionamento generale

Brutus.py utilizza `asyncio` e `asyncssh` per gestire i tentativi di autenticazione in modalità asincrona, rendendo l’esecuzione fluida anche quando vengono testate molte credenziali.  
In base agli input forniti, il programma può eseguire attacchi mirati, attacchi basati su wordlist o tentativi distribuiti su più utenti.

---

## Modalità di attacco supportate

Brutus.py riconosce automaticamente la modalità di attacco in base ai parametri forniti. Le modalità implementate sono le seguenti:

---

### 🔹 1. Credenziali singole  
*(Single Username + Single Password)*

La modalità più semplice: viene effettuato un solo tentativo.

Viene attivata quando vengono specificati:

- `-u <username>`
- `-p <password>`

**Esempio:**

```bash
python3 brutus.py -i 192.168.1.10 -u admin -p admin123
```

### 🔹 2. Attacco Dictionary / Cluster Bomb  
*(Username list × Password list)*

Questa modalità esegue un attacco completo combinando **ogni username** con **ogni password**.  
È la modalità più efficace quando si vogliono testare molte credenziali.

Si attiva quando vengono fornite wordlist tramite:

- `-U <file>` — lista username  
- `-P <file>` — lista password  

In questo caso Brutus.py costruisce automaticamente tutte le combinazioni possibili.

**Esempio:**

```bash
python3 brutus.py -i 10.0.0.5 -U users.txt -P passwords.txt
```
### 🔹 3. Password Spraying Attack  
*(Una password testata su molti utenti)*

In questa modalità viene utilizzata **una singola password** per tutti gli username presenti nella wordlist.  
È utile quando si vogliono evitare lock-out dovuti a troppi tentativi falliti sullo stesso utente.

La modalità si attiva quando vengono specificati:

- `-U <file>` — lista di username  
- `-p <password>` — password singola

**Esempio:**

```bash
python3 brutus.py -i 192.168.1.20 -U users.txt -p Winter2024!
```
## 🛡️ Gestione degli errori e validazione degli input

Il programma include un sistema di validazione progettato per intercettare errori prima dell’esecuzione.  
In particolare vengono gestiti:

- **Validità dell’indirizzo IP**, tramite il modulo `ipaddress`
- **Validità della porta**, che deve essere numerica e compresa tra **1 e 65535**
- **Esistenza dei file** (per userlist e passlist)
- **Prevenzione della confusione tra file e stringhe**, evitando interpretazioni errate
- **Gestione delle eccezioni di rete e autenticazione**
  - timeout  
  - permission denied  
  - errori `asyncssh`  
  - problemi di connessione  

Gli errori vengono comunicati in modo chiaro e senza interrompere bruscamente l’esecuzione.

---

## 📦 Requisiti

- Python **3.8+**
- Modulo necessario:

```bash
pip install asyncssh
```
## 🧪 Esempi di utilizzo

### 🔹 Username singolo + passlist

```bash
python3 brutus.py -i 192.168.1.10 -u root -P rockyou.txt
```
### 🔹 Wordlist utenti + password singola (password spraying)
```bash
python3 brutus.py -i 192.168.1.50 -U users.txt -p qwerty!
```
### 🔹 Attacco cluster-bomb
```bash
python3 brutus.py -i 10.0.0.5 -U users.txt -P passwords.txt
```
### 🔹 Continuare anche dopo credenziali valide
```bash
python3 brutus.py -i 192.168.1.10 -U u.txt -P p.txt --dont-stop
```
## ⚙️ Opzioni disponibili
```bash
- `-i, --ip` → Indirizzo IP target  
- `-s, --service` → Porta SSH (default: 22)  
- `-u, --username` → Username singolo  
- `-p, --password` → Password singola  
- `-U, --userlist` → File contenente lista di username  
- `-P, --passlist` → File contenente lista di password  
- `--dont-stop` → Non interrompe l’attacco se vengono trovate credenziali valide
```
