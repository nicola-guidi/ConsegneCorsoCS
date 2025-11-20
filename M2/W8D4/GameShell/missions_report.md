# GameShell - Guida Completa alle 44 Missioni

## Introduzione

GameShell è un gioco educativo per imparare i comandi Linux attraverso missioni interattive. Questo documento riporta le soluzioni e gli apprendimenti delle 44 missioni completate.

### Mission 1
Qui si tratta semplicemente di entrare nella cartella Castle/Main_tower fino a raggiungere l'ultima sottocartella Top_of_the_tower.

![mission1](./Media/mission1.png)

### Mission 2
Qui lo scopo della missione è quello di tornare indietro fino alla directory Castle ed entrare nella directory Cellar. L'utilizzo del comando `cd ..` è fondamentale.

![mission1](./Media/mission2.png)

### Mission 3
Qui si torna nella directory iniziale con il comando `cd`, dopo di che ci si sposta specificando il path assoluto con il comando `cd Castle/Main_building/Throne_room`.

![mission1](./Media/mission3.png)

### Mission 4
In questo task ci spostiamo nella cartella World/Forest e creiamo una cartella chiamata Hut. Dopodiché entriamo nella cartella creata e ne creiamo un'altra chiamata Chest.

![mission1](./Media/mission4.png)

### Mission 5
In questo task ci spostiamo nella cartella World/Castle/Cellar ed eliminiamo tutti i file che iniziano con la parola "spider".

![mission1](./Media/mission5.png)

### Mission 6
Ci spostiamo nella cartella Garden e muoviamo con il comando `mv` tutti i file coin_* nella cartella Forest/Hut/Chest.

![mission1](./Media/mission6.png)

### Mission 7
Stessa missione di prima ma in questo caso i file "coin" sono file nascosti. Per poterli listare si deve utilizzare il comando `ls -la` all'interno della cartella Garden.

![mission1](./Media/mission7.png)

### Mission 8
Qui possiamo rimuovere tutti i file richiesti dalla cartella Castle/Cellar utilizzando il comando `rm *spider*`. In questo modo elimineremo i file che avranno la parola "spider" al centro del nome del file.

![mission1](./Media/mission8.png)

### Mission 9
Questo è come l'esercizio precedente ma i file spider sono nascosti. Si deve dire a `rm` di rimuovere i file che sono nascosti e che hanno la parola spider nel nome del file utilizzando il comando `rm .*spider*`.

![mission1](./Media/mission9.png)

### Mission 10
In questo esercizio dobbiamo copiare i file standard_* dalla cartella Castle/Great_hall nella cartella Forest/Hut/Chest.

![mission1](./Media/mission10.png)

### Mission 11
Adesso il nostro obiettivo è quello di copiare tutti i file che hanno il pattern XXX_tapestry_XXX nel nostro forziere. Per fare questo possiamo utilizzare il comando `cp *tapestry* ../../Forest/Hut/Chest/`.

![mission1](./Media/mission11.png)

### Mission 12
In questo esercizio occorre listare i file con il comando `ls -l` per poter leggere la data di ultima modifica di ogni file. Poi si deve prendere il meno recente e spostarlo nel nostro forziere.

![mission1](./Media/mission12.png)

### Mission 13
Con il comando `cal 2020` possiamo stampare a video il calendario di quell'anno e vedere che il giorno richiesto (19 ottobre 2020) era un lunedì.

![mission1](./Media/mission13.png)

### Mission 14
In questo esercizio impareremo a creare un alias per il comando `ls -A`. Per poter creare un alias il comando è `alias la='ls -A'`.

![mission1](./Media/mission14.png)

### Mission 15
Nano è uno degli editor di testo presenti in molte delle distribuzioni Linux. Usando nano dovremo creare un file chiamato journal.txt all'interno della cartella Forest/Hut/Chest che contenga del testo.

![mission1](./Media/mission15.png)

### Mission 16
Gli alias sono un modo comodo per evitare di ridigitare comandi lunghi ogni volta. Utilizzando il comando `alias journal='nano ~/Forest/Hut/Chest/journal.txt'` potremo creare un alias per accedere in modo molto più comodo all'editor di testo per poter modificare il file journal.txt.

![mission1](./Media/mission16.png)

### Mission 17
Questa è una missione a tempo. Per poter risolvere l'esercizio è necessario utilizzare la Tab completion in modo da iniziare a scrivere soltanto la parte iniziale di una cartella o di un file e poi con il tasto tab fare in modo che il terminale finisca di scrivere in modo autonomo il nome del file o della cartella.

![mission1](./Media/mission17.png)

### Mission 18
Qui il gioco ci insegna come aprire un programma in background mettendo il carattere `&` in fondo al nome di un qualsiasi programma. Es: `mousepad&`.

![mission1](./Media/mission18.png)

### Mission 19
In questo esercizio vediamo come il comando `&` posto in mezzo a due o più comandi ci permetta di concatenare più comandi insieme.

![mission1](./Media/mission19.png)

### Missione 20
Qui ci si affida alla fortuna. La parola magica di 4 lettere da abbinare al comando charmiglio è `bash`.

![mission1](./Media/mission20.png)

### Missione 21
In questa missione ci muoviamo alla cieca nel labirinto, cartella per cartella per trovare il file OOOOO_copper_coin_OOOOO e spostarlo nella cartella Forest/Hut/Chest/.

![mission1](./Media/mission21.png)

### Missione 22
Il task è molto simile a quello precedente ma adesso abbiamo un'arma in più. Il comando `tree` ci mostra la struttura del file system dal punto in cui ci troviamo in basso. Questo ci semplifica la vita nel riuscire a trovare e spostare il file OOOOO_silver_coin_OOOOO nel nostro forziere.

![mission1](./Media/mission22_1.png)
![mission1](./Media/mission22_2.png)

### Missione 23
Qui possiamo utilizzare `find` per trovare i gold coins. Servirà utilizzare il comando `find -iname *coin*` per fare in modo che la ricerca non sia case-sensitive e trovare i due file.

![mission1](./Media/mission23.png)

### Mission 24
Per completare la missione dobbiamo per prima cosa trovare la pagina che contiene la ricetta dell'Herbal tea. Trovata la pagina dobbiamo tornare sopra di un livello nel file system nella cartella Cave (dove si trova Servillus). Per mostrare solo la parte del file che contiene la ricetta dell'Herbal tea dobbiamo utilizzare il comando `head -n 6 page_07`. Head mostra solo la parte iniziale di un file di testo (le prime 10 righe). Per specificare quante righe mostrare dobbiamo utilizzare il flag `-n` seguito dal numero di righe delle quali abbiamo bisogno.

![mission1](./Media/mission24.png)

### Mission 25
Missione simile alla precedente ma in questo caso si devono mostrare solo le ultime righe di un file. Nello specifico del file page_12. Possiamo eseguire il comando `tail -n 9 Book_of_potions/page_12` per completare la missione con successo.

![mission1](./Media/mission25.png)

### Mission 26
Per completare questa missione è necessario utilizzare il comando `cat` specificando i due file da leggere (page_01 e page_02) in modo che vengano stampati a schermo in un solo output. Il comando da utilizzare è `cat Book_of_potions/page_01 Book_of_potions/page_02`.

![mission1](./Media/mission26.png)

### Mission 27
Per riuscire a mostrare soltanto le 16 righe della ricetta richiesta dal task dobbiamo utilizzare una combinazione del comando `cat` e del comando `tail`. Utilizziamo il comando `cat` per mostrare l'intero contenuto della ricetta (page_03 e page_04). Reindirizzeremo quindi l'output di `cat` utilizzando la pipe (`|`) per fare in modo che venga preso in input dal comando `tail`, che con il flag `-n 16` restituirà solo ed esclusivamente le righe che ci servono.

![mission1](./Media/mission27.png)

### Mission 28
In questo esercizio dovremo stampare esclusivamente le tre righe della ricetta richiesta che si trovano al centro del file. Dovremo usare una combinazione di `head` (per settare il limite superiore delle righe che vogliamo mostrare) insieme a `tail` per eliminare dall'output le righe iniziali che non ci servono. Il comando sarà quindi `head -n 6 Book_of_potions/page_13 | tail -n 3`.

**Spiegazione**: `head -n 6` prende le prime 6 righe del file, poi `tail -n 3` estrae le ultime 3 di queste 6 righe, ottenendo così le righe 4, 5 e 6 del file originale.

![mission1](./Media/mission28.png)

### Mission 29
In questo task dobbiamo identificare e killare l'incantesimo (processo) che fa piovere carbone all'interno del castello. Possiamo fare ciò con il comando `ps` per elencare i processi, identificare il PID dell'incantesimo e killarlo con il comando `kill` seguito dal process identifier relativo.

![mission1](./Media/mission29.png)

### Mission 30
In questo task non basta il comando `kill` per interrompere l'incantesimo. Servirà anche specificare un tipo di segnale per fare in modo che il processo si fermi. Il comando `kill -1 195220` ha funzionato ed ha spezzato l'incantesimo.

![mission1](./Media/mission30.png)

### Mission 31
In questo task un processo padre ha generato diversi processi figlio che a loro volta creavano dei file *_coal. Per prima cosa si è reso necessario identificare il PID del processo padre con il comando `ps`. Poi con il comando `pstree 196558 -p` abbiamo ottenuto i PID di tutti i processi figlio. Li abbiamo killati con il comando `kill` e poi abbiamo rimosso i file *_coal con il comando `rm`.

![mission1](./Media/mission31_1.png)
![mission1](./Media/mission31_2.png)

### Mission 32
Addizioni matematiche di base.

![mission1](./Media/mission32.png)

### Mission 33
In questo esercizio dovremo fare in modo di fare eseguire i calcoli al file Mathematics_101. Per fare questo dobbiamo utilizzare il comando `gsh check < Mathematics_101`.

![mission1](./Media/mission33.png)

### Mission 34
In questo esercizio dobbiamo creare un file inventory.txt che contenga la lista di libri dell'ufficio di Merlino. Per fare questo possiamo listare tutti i file che inizino con la parola grimoire e reindirizzare questa lista nel file inventory.txt nella cartella Drawer.

![mission1](./Media/mission34.png)

### Mission 35
In questo task dobbiamo elencare i file che hanno al loro interno la parola 'ghs' indipendentemente dal fatto che sia maiuscola o minuscola. Possiamo fare questo utilizzando il comando `grep` con i flag `-i` per dire che vogliamo una ricerca non case-sensitive e `-l` per fare stampare a video solo i nomi dei file e non il loro contenuto.

![mission1](./Media/mission35.png)

### Mission 36
In questa missione abbiamo analizzato l'output del programma merlin, reindirizzando sia STDOUT che STDERR per identificare informazioni nascoste. Il messaggio d'errore conteneva la chiave segreta (THESECRETKEYISONDSTDER), necessaria per completare con successo la missione.

![mission1](./Media/mission36.png)

### Mission 37
In questa missione dobbiamo usare `chmod` per cambiare i permessi di accesso alla cartella Kings_quarter. Con il comando `chmod 777 Kings_quarter` faremo in modo che chiunque (noi compresi) possa accedere con pieni permessi alla cartella.

![mission1](./Media/mission37.png)

### Mission 38
Stesso goal della missione prima. Però invece di dover cambiare i permessi ad una cartella dobbiamo cambiarli ad un file nascosto. In questo caso è stato utilizzato il comando `chmod +r .secret_note`.

![mission1](./Media/mission38.png)

### Mission 39
Qui dobbiamo accedere alla cartella Safe nella sala del trono, per farlo dobbiamo cambiare i permessi in modo da poterci concedere l'accesso. Qui si trova la corona. Per poterla ispezionare e spostare nel nostro forziere dobbiamo anche qui modificarne i permessi. Fatto questo possiamo inserire i tre numeri presenti sulla corona e completare il task.

![mission1](./Media/mission39.png)

### Mission 40
In questo esercizio ci viene richiesto di trovare un file contenente un rubino. Possiamo utilizzare `find` per cercare soltanto i file (e non le cartelle) nel labirinto. Il comando `find -type f` elenca una serie di file da ispezionare. Trovato quello che contiene il rubino sarà necessario spostarlo nel nostro forziere.

![mission1](./Media/mission40.png)

### Mission 41
Nella missione 41 abbiamo utilizzato `find` insieme a `xargs` per individuare il file che conteneva la parola "diamond" all'interno della struttura di directory. Dopo aver identificato il file corretto, lo abbiamo spostato nel percorso richiesto, completando con successo la missione.

![mission1](./Media/mission41.png)

### Mission 42
In questa missione dobbiamo capire a quanto ammonta il debito del re. Per prima cosa dobbiamo escludere i file che non ci servono con il comando `grep -v` che fa una ricerca inversa, escludendo i file che contengono nel nome un pattern che non ci interessa. Dopo di che viene restituito un unico file dove se cerchiamo le righe al suo interno che contengono il pattern "the king" ed escludiamo, sempre con `grep -v` la parola "PAID" riusciamo a scoprire cosa ha comprato il re e cosa non è ancora stato pagato.

![mission1](./Media/mission42.png)

### Mission 43
Adesso dobbiamo fare la stessa cosa ma capire quanti oggetti non sono ancora stati pagati. Qui dobbiamo concatenare alcuni comandi. Inizialmente si escludono i file che contengono la parola boring nel titolo. Dopo di che, nel file che ci viene restituito, escludiamo le righe che hanno la parola "PAID". Fatto questo utilizziamo `wc` per contare le righe dell'output del comando precedente.

![mission1](./Media/mission43.png)

### Mission 44
In questa ultima missione dobbiamo decifrare il messaggio di Merlino. È criptato con un Caesar cipher e dobbiamo capire il numero di ROT. Siamo riusciti a decifrare il messaggio con il comando `cat ~/Castle/Main_building/Library/Merlin_s_office/Drawer/secret_message | tr "a-z" "o-za-n"`. Questo ci rivelerà la chiave per il forziere di Merlino e concluderà il gioco.

![mission1](./Media/mission44.png)

## Conclusioni

GameShell è uno strumento eccellente per apprendere i fondamenti della shell Linux in modo interattivo. Le 44 missioni coprono progressivamente i concetti essenziali dalla navigazione base fino alla gestione avanzata di processi, manipolazione di testi e crittografia.
