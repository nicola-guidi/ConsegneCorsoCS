# Brutus.py

Brutus.py è uno strumento pensato per il testing di sicurezza di servizi SSH.  
Il suo scopo è permettere di verificare in modo rapido e controllato la robustezza delle credenziali di accesso, attraverso tentativi mirati o combinazioni generate automaticamente da apposite liste. L’idea alla base del progetto è fornire uno strumento sia semplice da usare sia sufficientemente flessibile per scenari più ampi di audit e penetration testing autorizzato.

> ⚠️ **Attenzione**  
> Questo script deve essere utilizzato esclusivamente in contesti autorizzati.  
> Qualsiasi tentativo di accesso non autorizzato a sistemi remoti è illegale.  
> L’autore declina ogni responsabilità per usi impropri dello strumento.

---

## Funzionamento generale

Brutus.py permette di tentare l’accesso SSH combinando username e password forniti manualmente o tramite wordlist.  
Il programma supporta sia l’utilizzo singolo (un solo utente e una sola password), sia modalità più estese in cui ogni username viene testato contro ogni password, generando automaticamente tutte le combinazioni possibili.

L’esecuzione sfrutta `asyncio` e `asyncssh`, permettendo un flusso di tentativi fluido, reattivo e privo di blocchi.  
Se viene individuata una combinazione valida, questa viene evidenziata immediatamente, con la possibilità di proseguire o interrompere l’esecuzione in base ai parametri scelti dall’utente.

---

## Gestione degli errori e validazione degli input

Uno degli aspetti su cui è stata posta particolare attenzione durante lo sviluppo è la **corretta validazione degli input** e la gestione degli errori generati da formati non corretti.

Brutus.py effettua infatti controlli preventivi su:

- **Formato dell’indirizzo IP**  
  Utilizza il modulo `ipaddress` per verificare che l’IP fornito sia valido.

- **Porta del servizio SSH**  
  Controlla che il valore sia numerico e compreso tra 1 e 65535.

- **Esistenza effettiva dei file**  
  I percorsi forniti come userlist e passlist vengono verificati prima dell’avvio, e in caso di file inesistenti il programma interrompe l’esecuzione mostrando un messaggio chiaro.

- **Distinzione tra stringhe e file**  
  Lo script impedisce che valori destinati a username/password vengano scambiati per un percorso di file e viceversa.

- **Gestione delle eccezioni di rete e autenticazione**  
  Qualunque errore di connessione, timeout, permesso negato o problema interno di `asyncssh` viene catturato e gestito in modo sicuro, evitando crash dello script.

Questi controlli garantiscono un’esecuzione stabile e riducono sensibilmente la possibilità di input errati o comportamenti inattesi.

---

## Requisiti e installazione

Lo script necessita di:

- Python 3.8 o versioni successive
- La libreria `asyncssh`, installabile tramite:

```bash
pip install asyncssh
