//Import delle librerie necessarie

#include <stdio.h>
#include <math.h>

// Funzione main()

int main() {

// Inizializzazione delle variabili

float num;
float pi = 3.1415926535897932384626433; // Costante PI

printf("Inserisci un numero reale: \n");
scanf("%f", &num); // Input dell'utente

float quad = num * num; // Calcolo dell'area del quadrato
float circ = ((num / 2) * (num / 2)) * pi; // Caloclo dell'area del cerchio
float tri = (pow(num, 2) * sqrt(3)) / 4; // Calcolo dell'area del triangolo equilatero

printf("L'area del quadrato: %f\n", quad);
printf("L'area del cerchio: %f\n", circ);
printf("L'area del triangolo equilatero: %f\n", tri);
printf("Goodbye");

return 0; // Ritorno funzione main
}
