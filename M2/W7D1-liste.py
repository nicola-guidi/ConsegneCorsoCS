# QUESTO PROGRAMMA PRENDE IN INGRESSO UNA LISTA DI PAROLE E RESTITUISCE IN OUTPUT UNA NUOVA LISTA DI INTERI CHE RAPPRESENTA LE LUNGHEZZE DELLE PAROLE INSERITE
# INIZIALIZZAZIONE DELLE LISTE VUOTE
lista_a = []
lista_b = []

lista_a = input("[+] Inserisci una serie di parole a tua scelta separate da una virgola:\n>>> ") # PRENDE IN INPUT UNA SERIE DI PAROLE
lista_a = lista_a.split(",") # TOGLIE LA VIRGOLA E AGGIUNGE OGNI PAROLA INSERITA NELLA LISTA A

# FUNZIONE PER IL CONTEGGIO DELLA LUNGHEZZA DELLE PAROLE
def conversione_lista(lista_a):
    for i in lista_a: # PER OGNI ELEMENTO DELLA LISTA MISURA LA SUA LUNGHEZZA E AGGIUNTE IL NUMERO DI CARATTERI A LISTA B
        lunghezza = len(i)
        lista_b.append(lunghezza)
        
conversione_lista(lista_a) # CHIAMATA DELLA FUNZIONE
print("[+] Il numero di caratteri di ogni parola fornita è: " + str(lista_b)) # OUTPUT FINALE
