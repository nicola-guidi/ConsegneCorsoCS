# Splunk Log Analysis — tutorialdata.zip

## Introduzione

Questo report documenta l'analisi dei log di esempio `tutorialdata.zip` tramite Splunk Enterprise.  
Il dataset contiene tre tipologie di log:

| Sourcetype | Descrizione | Eventi |
|---|---|---|
| `secure-2` | Log SSH (autenticazione) | 40.088 |
| `access_combined_wcookie` | Log web Apache | 39.532 |
| `vendor_sales` | Dati di vendita | 30.244 |

---

## Query 1 — Tentativi di accesso falliti (Failed password)

**Obiettivo:** identificare tutti i tentativi di accesso falliti, mostrando timestamp, IP di origine, utente e motivo del fallimento.

```spl
index=main "Failed password"
| rex "Failed password for (?:invalid user )?(?P<user>[^\s]+) from (?P<src_ip>[^\s]+) port (?P<port>\d+)"
| where user!="abc"
| eval reason=if(match(_raw, "invalid user"), "Invalid user", "Valid user, wrong password")
| table _time, src_ip, user, reason
```

**Risultati:** 33.253 eventi

**Note:** il campo `reason` distingue tra tentativi su utenti inesistenti (`Invalid user`) e tentativi su utenti validi con password errata (`Valid user, wrong password`). La maggioranza degli eventi riguarda utenti inesistenti, tipico pattern di brute force con wordlist.

---

## Query 2 — Sessioni SSH aperte con successo per djohnson

**Obiettivo:** trovare tutte le sessioni SSH accettate per l'utente `djohnson`, mostrando timestamp e nome utente.

```spl
index=main "Accepted password" "djohnson"
| rex "Accepted password for (?P<user>[^\s]+) from (?P<src_ip>[^\s]+) port (?P<port>\d+)"
| search user=djohnson
| table _time, user
```

**Risultati:** 955 eventi

**Note:** l'elevato numero di sessioni accettate per un singolo utente da un unico IP (`10.3.10.46`) suggerisce attività automatizzata o uso continuativo di script di automazione.

---

## Query 3 — Tentativi falliti dall'IP 86.212.199.60

**Obiettivo:** trovare tutti i tentativi di accesso falliti provenienti dall'indirizzo IP `86.212.199.60`, mostrando timestamp, nome utente e porta.

```spl
index=main "Failed password" "86.212.199.60"
| rex "Failed password for (?:invalid user )?(?P<user>[^\s]+) from (?P<src_ip>[^\s]+) port (?P<port>\d+)"
| table _time, user, port
```

**Risultati:** 158 eventi

**Utenti tentati (campione):**

| Username | Tipo |
|---|---|
| administrator | Utente di sistema comune |
| root | Utente privilegiato |
| oracle | Utente di servizio database |
| nagios | Utente di monitoraggio |
| appserver | Utente di servizio applicativo |
| testuser | Utente di test |

**Note:** il pattern degli username tentati è caratteristico di un attacco brute force con dizionario. L'IP ha sistematicamente provato account di servizio e account privilegiati.

---

## Query 4 — IP con più di 5 tentativi falliti

**Obiettivo:** identificare gli indirizzi IP che hanno tentato di accedere con "Failed password" più di 5 volte, mostrando IP e numero di tentativi.

```spl
index=main "Failed password"
| rex "Failed password for (?:invalid user )?(?P<user>[^\s]+) from (?P<src_ip>[^\s]+) port (?P<port>\d+)"
| stats count by src_ip
| where count > 5
| sort -count
| table src_ip, count
```

**Risultati:** 182 IP distinti

**Top 5 IP per numero di tentativi:**

| IP | Tentativi |
|---|---|
| 87.194.216.51 | 948 |
| 211.166.11.101 | 743 |
| 128.241.220.82 | 622 |
| 109.169.32.135 | 515 |
| 194.215.205.19 | 514 |

**Note:** il volume di tentativi per singolo IP (fino a 948) indica campagne di brute force automatizzate. La distribuzione geografica degli IP suggerisce l'uso di botnet o proxy distribuiti.

---

## Query 5 — Internal Server Error (HTTP 500)

**Obiettivo:** trovare tutti gli Internal Server Error nei log web.

```spl
index=main sourcetype=access_combined_wcookie status=500
| table _time, host, clientip, uri, status
```

**Risultati:** 733 eventi

**URI più colpiti (campione):**

| URI | Pattern |
|---|---|
| `/category.screen?categoryId=NULL` | Parametro nullo |
| `/cart.do?action=view&itemId=...` | Errore carrello |
| `/product.screen?productId=...` | Errore pagina prodotto |
| `/oldlink?itemId=...` | Link obsoleto |

**Note:** la presenza di `categoryId=NULL` come causa ricorrente indica un bug applicativo nella gestione dei parametri mancanti. Gli errori su `/oldlink` suggeriscono la presenza di link non aggiornati che puntano a risorse inesistenti.

---

## Analisi AI — Conclusioni

### Minacce SSH identificate

L'analisi dei log `secure-2` rivela una superficie di attacco SSH significativamente esposta:

- **Brute force distribuito su larga scala:** 33.253 tentativi di accesso falliti provenienti da 182 IP distinti. Il volume e la distribuzione degli IP indicano l'utilizzo di botnet o tool automatizzati come Hydra o Medusa.

- **Attacco mirato da 86.212.199.60:** con 158 tentativi su account di servizio specifici (`oracle`, `nagios`, `appserver`), questo IP mostra una strategia più mirata rispetto al brute force generico — probabile ricognizione preliminare del target o uso di wordlist specializzate per ambienti server.

- **Attività anomala di djohnson:** 955 sessioni SSH accettate in un arco temporale ristretto da un singolo IP interno (`10.3.10.46`) è un volume inusualmente alto. Potrebbe indicare un processo automatizzato legittimo, ma merita verifica — in uno scenario reale sarebbe un candidato per un alert di behavioral analytics.

- **Utenti più attaccati:** la frequenza elevata di tentativi su `root`, `admin` e account di servizio indica che il sistema non ha restrizioni sull'accesso SSH per account privilegiati. Raccomandazione: disabilitare il login SSH diretto per `root` e applicare fail2ban o equivalente.

### Problemi applicativi web

I 733 errori HTTP 500 evidenziano instabilità nell'applicazione web:

- Il pattern `categoryId=NULL` indica mancata validazione dell'input lato server — l'applicazione non gestisce i parametri mancanti o nulli.
- La presenza di `/oldlink` tra gli URI che generano errori suggerisce mancanza di redirect management per URL deprecati.
- In un contesto di sicurezza, errori 500 ripetuti possono essere sintomo di tentativi di fuzzing o injection — da correlare con i `clientip` per verificare sovrapposizioni con gli IP già identificati nel brute force SSH.

### Raccomandazioni

1. Implementare fail2ban o simile per bloccare automaticamente gli IP dopo N tentativi falliti
2. Disabilitare il login SSH con password, migrare a chiavi SSH
3. Disabilitare il login diretto come `root` via SSH
4. Correggere la gestione dei parametri nulli nell'applicazione web
5. Implementare redirect 301 per gli URL obsoleti (`/oldlink`)
6. Investigare l'attività di `djohnson` per escludere uso improprio delle credenziali
