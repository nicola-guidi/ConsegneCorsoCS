# IMPORT DELLE LIBRERIE
import math
import sys
import time

# ASCII BANNER
print("                          d8b")                      
print("                          Y8P")                         
print("                                                    ")   
print("88888b.   .d88b.  888d888 888     88888b.  888  888")    
print('888 "88b d8P  Y8b 888P"   888     888 "88b 888  888')    
print("888  888 88888888 888     888     888  888 888  888")    
print("888 d88P Y8b.     888     888 d8b 888 d88P Y88b 888")    
print('88888P"   "Y8888  888     888 Y8P 88888P"   "Y88888')    
print("888                               888           888")    
print("888                               888      Y8b d88P")    
print('888                               888       "Y88P"')     
print("                                                    ")   
print("                                                    ")   

print("Benvenuto nel programma che ti aiuta a calcolare facilmente") 
print("perimetri e circonferenze di varie figure geometriche!")
print("Isn't it lovely?\n")  

# SUPER-COOL PROGRESS BAR - RUBATA DA LIBRERIE ESTERNE
def progress_bar():
    for i in range(51):  
        percent = i * 2  
        bar = "#" * i + "-" * (50 - i)
        sys.stdout.write(f"\r[{bar}] {percent:3d}%")
        sys.stdout.flush()
        time.sleep(0.05)  

print("                    PLEASE WAIT...")
progress_bar()
print("")

# FUNZIONE PRINCIPALE
def calcolo():
    while True: # MENU A SCELTA MULTIPLA
        print("\n[+] Scegli una figura:\n")
        print(" 1. Quadrato")
        print(" 2. Cerchio")
        print(" 3. Rettangolo")
        print("")   

        figura = input(">>> ")

        if figura == "1":
            print("\n[+] Hai scelto di calcolare il perimetro di un quadrato")
            numero = int(input("[+] Dammi un numero >>> "))
            print("\n                 MAN, this is HARD...")
            progress_bar()
            print("")
            per_quadrato = numero * 4 # CALCOLO PERIMETRO DEL QUADRATO
            print("\n[+] Se il numero che mi hai dato fosse la lunghezza del lato di un quadrato, il quadrato avrebbe un perimetro di " + str(per_quadrato))
            break
        elif figura == "2":
            print("\n[+] Hai scelto di calcolare la circonferenza di un cerchio")
            numero = int(input("[+] Dammi un numero >>> "))
            print("\n          Getting results from the NASA...")
            progress_bar()
            print("")
            circ_cerchio = (2 * (math.pi)) * numero # CALCOLO CIRCONFERENZA DEL CERCHIO
            circ_cerchio = round(circ_cerchio, 2)
            print("\n[+] Se il numero che mi hai dato fosse il raggio di un cerchio, il cerchio avrebbe una circonferenza di " + str(circ_cerchio))
            break
        elif figura == "3":
            print("\n[+] Hai scelto di calcolare il perimetro di un quadrato")
            numero = int(input("[+] Dammi un numero >>> "))
            numero_2 = int(input("[+] Per questo calcolo ho bisogno di un altro numero >>> ")) # PER IL RETTANGOLO SERVE UN DATO IN PIU
            print("\n     Performing some SUPER-DUPER calculations...")
            progress_bar()
            print("")
            per_rettangolo = ((numero * 2) + (numero_2 * 2)) # CALOCLO DEL PERIMETRO DEL RETTANGOLO
            print("\n[+] Se i numeri che mi hai dato fossero la base e l'altezza di un rettangolo, il rettangolo avrebbe un perimetro di " + str(per_rettangolo))
            break
        else:
            print("\n[!] NON FARE IL FURBO con i tuoi sporchi payload! This is REAL INPUT VALIDATION!")
            print("[!] Riproviamo...")
            continue

# CHIAMATA DELLA FUNZIONE
calcolo()
