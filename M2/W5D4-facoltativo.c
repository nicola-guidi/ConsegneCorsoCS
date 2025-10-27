//Import delle librerie necessarie

#include <stdio.h>
#include <math.h>

// Funzione main()

int main(){ 

// Inizializzazione delle variabili

float first_num;
float second_num;
float third_num;

// Banner
    
printf("****************************\n");
printf("* Ciao, facciamo un gioco! *\n");
printf("****************************\n");
printf("\n");
printf("Inserisci un numero:\n");
scanf("%f", &first_num);     // Input utente e assegnazione valore a variabile

printf("Grazie, adesso inserisci un secondo numero:\n");
scanf("%f", &second_num);     // Input utente e assegnazione valore a variabile

printf("Ottimo! Infine inserisci un terzo ed ultimo numero:\n");
scanf("%f", &third_num);     // Input utente e assegnazione valore a variabile

// Calcolo della media

printf("\n");
printf("*** CALCOLO DELLA MEDIA ***\n");
float media_dec = (first_num + second_num + third_num) / 3;     // Calcolo della media
printf("La media, con due numeri decimali, dei tre numeri: %.2f\n", media_dec);     // %.2f tronca il float a due numeri decimali
int media_int = (int) roundf(media_dec);     // Arrotondamento della media a numero intero
printf("La media arrotondata dei tre numeri: %d\n\n", media_int);

 // Calcolo dell'area del quadrato

float area_quad_dec = media_dec * media_dec;     // Formula area del quadrato che prende come input la media con due decimali
float area_quad_int = media_int * media_int;     // Formula area del quadrato che prende come input la media intera

printf("*** AREA DEL QUADRATO ***\n");
printf("Se la media, con due decimali, dei numeri inseriti fosse il lato di un quadrato la sua area sarebbe: %.2f\n", area_quad_dec);
printf("Se la media, senza decimali, dei numeri inseriti fosse il lato di un quadrato la sua area intera sarebbe: %.2f\n\n", area_quad_int);

// Calcolo dell'area del cerchio

float raggio_dec = media_dec / 2;     // Calcolo del raggio dalla media con decimali
float area_cerch_dec = (raggio_dec * raggio_dec) * 3.141592653589793;     // Formula area del cerchio che prende come input la media con due decimali
float raggio_int = (float)media_int / 2;     // Calcolo del raggio dalla media intera. Necessario casting a float altrimenti media_int, essendo intero, verrebbe trocato/arrotondato
float area_cerch_int = (raggio_int * raggio_int) * 3.141592653589793;     // Formula area del cerchio che prende come input la media intera

printf("*** AREA DEL CERCHIO ***\n");
printf("Se la media, con due decimali, dei numeri inseriti fosse il lato di un cerchio la sua area sarebbe: %.2f\n", area_cerch_dec); 
printf("Se la media, senza decimali, dei numeri inseriti fosse il lato di un cerchio la sua area intera sarebbe: %.2f\n\n", area_cerch_int); 

// Calcolo dell'area del triangolo equilatero
    
float area_tri_dec = ((media_dec * media_dec) * sqrt(3)) / 4;     // Formula area del triangolo equilatero che prende come input la media con due decimali
float area_tri_int = ((media_int * media_int) * sqrt(3)) / 4;     // Formula area del trinagolo equilatero che prende come input la media intera

printf("*** AREA DEL TRIANGOLO EQUILATERO ***\n");
printf("Se la media, con due decimali, dei numeri inseriti fosse il lato di un triangolo equilatero la sua area sarebbe: %.2f\n", area_tri_dec);
printf("Se la media, senza decimali, dei numeri inseriti fosse il lato di un triangolo equilatero la sua area intera sarebbe: %.2f\n", area_tri_int);

return 0;     // Ritorno funzione main
}
