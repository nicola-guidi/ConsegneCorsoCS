# QUESTO PROGRAMMA GENERA DUE TIPI DI PASSWORD, UNA SEMPLICE (8 CARATTERI) ED UNA COMPLESSA (20 CARATTERI) IN BASE ALLA SCELTA DELL'UTENTE
# IMPORT DEI MODULI
import random
import string

# FUNZIONE PER LA GENERAZIONE DI UNA PASSWORD SEMPLICE
def password_semplice(lunghezza):
    set_caratteri = string.ascii_letters + string.digits # SET DI CARATTERI USATO
    stringa_casuale_semplice = ''.join(random.choice(set_caratteri) for i in range (lunghezza)) # CREAZIONE DELLA STRINGA CASUALE
    print("Ecco la tua password semplice: " + stringa_casuale_semplice) # OUTPUT DELLA PASSWORD

# FUNZIONE PER LA GENERAZIONE DI UNA PASSWORD COMPLESSA
def password_complessa(lunghezza):
    set_caratteri = string.ascii_letters + string.digits # SET DI CARATTERI USATO
    stringa_casuale_complessa = ''.join(random.choice(set_caratteri) for i in range (lunghezza)) # CREAZIONE DELLA STRINGA CASUALE 
    print("Ecco la tua password complessa: " + stringa_casuale_complessa) # OUTPUT DELLA PASSWORD

# INIZIO PROGRAMMA
print("Benvenuto nel tuo fantastico generatore di password!")
scelta = input("Seleziona [1] se vuoi una password semplice, oppure seleziona [2] se vuoi generare una password complessa.\n>>> ")

# SELEZIONE DELL'UTENTE
if scelta == "1":
    password_semplice(8)
elif scelta == "2":
    password_complessa(20)
else:
    print("Scelta non valida!") # ERROR HANDLING
