# IMPORT DELLE LIBRERIE
import math

# FUNZIONI DEI VARI CALCOLI
def calcolo_per_quad(lato_quad):
    return lato_quad * 4

def calcolo_area_quad(lato_quad):
    return lato_quad ** 2

def calcolo_circ_cerchio(raggio):
    return (2 * (math.pi)) * raggio

def calcolo_area_cerchio(raggio):
    return math.pi * (raggio ** 2)

def calcolo_perimetro_triangolo(lato_tri):
    return lato_tri * 3

def calcolo_area_triangolo(lato_tri):
    return ((lato_tri ** 2) * math.sqrt(3)) / 4

# FUNZIONI RELATIVE ALLA SCELTA DELLE FIGURE
def scelta_quadrato():
    perimetro_quad_2 = round(calcolo_per_quad(area), 2)
    area_quad_2 = round(calcolo_area_quad(area), 2)
    print("Se l'area calcolata prima fosse uguale al lato di un quadrato, il suo perimetro sarebbe " + str(perimetro_quad_2) + " e la sua area " + str(area_quad_2))
        
def scelta_triangolo():
    perimetro_tri_2 = round(calcolo_perimetro_triangolo(area), 2)
    area_tri_2 = round(calcolo_area_triangolo(area), 2)
    print("Se l'area calcolata prima fosse uguale al lato di un triangolo equilatero, il suo perimetro sarebbe " + str(perimetro_tri_2) + " e la sua area " + str(area_tri_2))

def scelta_cerchio():
    circonferenza_2 = round(calcolo_circ_cerchio(area), 2)
    area_cer_2 = round(calcolo_area_cerchio(area), 2)
    print("Se l'area calcolata prima fosse uguale al raggio del cerchio, la sua circonferenza sarebbe " + str(circonferenza_2) + " e la sua area " + str(area_cer_2))

# INIZIO DEL PROGRAMMA CON SCELTA DELLA FIGURA INIZIALE
print("Scegli una figura:\n")
print(" 1. Quadrato")
print(" 2. Cerchio")
print(" 3. Triangolo (equilatero)\n")

figura_1 = int(input(">>> "))

# PRIMO BLOCCO IF/ELSE
if figura_1 == 1:
    lato_quad = int(input("Bene, iniziamo dal quadrato. Inserisci un numero: "))
    perimetro_quad = calcolo_per_quad(lato_quad)
    area_quad = calcolo_area_quad(lato_quad)
    area = area_quad

    print("Se il numero che mi hai dato fosse il lato di un quadrato, il suo perimetro sarebbe " + str(perimetro_quad) + " e la sua area " + str(area_quad))
    print("Scegli una nuova figura:\n")
    print(" 1. Cerchio")
    print(" 2. Triangolo (equilatero)\n")

    figura_2 = int(input(">>> "))

    # SECONDO BLOCCO (NETSTED) IF/ELSE
    if figura_2 == 1:
        print("Bene, proseguiamo con il cerchio")   
        scelta_cerchio()
        scelta_triangolo()
    elif figura_2 == 2:
        print("Bene, proseguiamo con il triangolo equilatero")
        scelta_triangolo()
        scelta_cerchio()
    else:
        print("Selezione non valida!") # ERROR HANDLING

elif figura_1 == 2:
    raggio = int(input("Bene, iniziamo dal cerchio. Inserisci un numero: "))
    circonferenza = calcolo_circ_cerchio(raggio)
    area_cer = calcolo_area_cerchio(raggio)
    area = area_cer

    print("Se il numero che mi hai dato fosse il raggio di un cerchio, la sua circonferenza sarebbe " + str(round(circonferenza, 2)) + " e la sua area " + str(round(area, 2))) # FUNZIONE ROUND PER ARROTONDARE A 2 DECIMALI
    print("Scegli una nuova figura:\n")
    print(" 1. Quadrato")
    print(" 2. Triangolo (equilatero)\n")
    
    figura_2 = int(input(">>> "))  

    # TERZO BLOCCO (NETSTED) IF/ELSE
    if figura_2 == 1:   
       print("Bene, proseguiamo con il quadrato")
       scelta_quadrato()
       scelta_triangolo()
    elif figura_2 == 2:
       print("Bene, proseguiamo con il triangolo equilatero")
       scelta_triangolo()
       scelta_quadrato()
    else:
        print("Selezione non valida!") # ERROR HANDLING     
      
elif figura_1 == 3:
    lato_tri = int(input("Bene, iniziamo dal triangolo equilatero. Inserisci un numero: "))
    perimetro_tri = calcolo_perimetro_triangolo(lato_tri)
    area_tri = calcolo_area_triangolo(lato_tri)
    area = area_tri

    print("Se il numero che mi hai dato fosse il lato di un triangolo equilatero, il suo perimetro sarebbe " + str(perimetro_tri) + " e la sua area " + str(round(area_tri, 2))) # FUNZIONE ROUND PER ARROTONDARE A 2 DECIMALI
    print("Scegli una nuova figura:\n")
    print(" 1. Quadrato")
    print(" 2. Cerchio\n")

    figura_2 = int(input(">>> "))  

    # QUARTO BLOCCO (NETSTED) IF/ELSE
    if figura_2 == 1:   
       print("Bene, proseguiamo con il quadrato")
       scelta_quadrato()
       scelta_cerchio()
    elif figura_2 == 2:
       print("Bene, proseguiamo con il cerchio") 
       scelta_cerchio()
       scelta_quadrato()
    else:
        print("Selezione non valida!") # ERROR HANDLING   
else:
    print("Selezione non valida!") # ERROR HANDLING
