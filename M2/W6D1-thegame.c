// Importazione librerie

#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

// ASCII Banner

void ascii_banner() {

printf("'########:'##::::'##:'########::'######::::::'###::::'##::::'##:'########:\n");
printf("... ##..:: ##:::: ##: ##.....::'##... ##::::'## ##::: ###::'###: ##.....::\n");
printf("::: ##:::: ##:::: ##: ##::::::: ##:::..::::'##:. ##:: ####'####: ##:::::::\n");
printf("::: ##:::: #########: ######::: ##::'####:'##:::. ##: ## ### ##: ######:::\n");
printf("::: ##:::: ##.... ##: ##...:::: ##::: ##:: #########: ##. #: ##: ##...::::\n");
printf("::: ##:::: ##:::: ##: ##::::::: ##::: ##:: ##.... ##: ##:.:: ##: ##:::::::\n");
printf("::: ##:::: ##:::: ##: ########:. ######::: ##:::: ##: ##:::: ##: ########:\n");
printf(":::..:::::..:::::..::........:::......::::..:::::..::..:::::..::........::\n");
printf("\n");

}

// Funzione menu principale. Chiede all'utente se si vuole giocare una partita o uscire dal programma

char game_start() { 
    char start;

    printf("Premi A per iniziare una nuova partita o premi B per uscire dal gioco:\n\n>>> ");
    scanf(" %c", &start);
    return start;
} 

// Funzione del gioco. Vengono fatte alcune domande e se la risposta è esatta si aggiungono 10 punti al contatore

int questions() { 

    char player[15];
    int counter = 0; // Contatore punti

    printf("\nInserisci il tuo nome:\n\n>>> "); // Nome giocatore
    scanf(" %s", &player);
    printf("\nBenvenuto %s!\n", player);

    // Domanda 1

    printf("Domanda 1 - Quale fu il linguaggio di programmazione da cui nacque il linguaggio C?\n\n");
    printf("A) Assembly\nB) B\nC) Pascal\n\n>>> ");
    char q1;
    scanf(" %c", &q1);

    if (q1 == 'B' || q1 == 'b') {
        printf("\nRisposta esatta!!\n");
        counter = counter + 10;
        printf("Il tuo punteggio è: %d\n\n", counter);
    } else {
        printf("\nPeccato! Risposta errata!\n");
        printf("Il tuo punteggio è: %d\n\n", counter);
    }

    // Domanda 2

    printf("Domanda 2 - Cosa accade se non si include <stdio.h> ma si usa printf() in un programma C moderno?\n\n");
    printf("A) Il programma non compila\nB) Il programma stampa comunque ma con warning\nC) Il programma gira solo su Windows\n\n>>> ");
    char q2;
    scanf(" %c", &q2);

    if (q2 == 'A' || q2 == 'a') {
        printf("\nRisposta esatta!!\n");
        counter = counter + 10;
        printf("Il tuo punteggio è: %d\n\n", counter);
    } else {
        printf("\nPeccato! Risposta errata!\n");
        printf("Il tuo punteggio è: %d\n\n", counter);
    }

    // Domanda 3

    printf("Domanda 3 - Quale tra questi non è un tipo di dato standard del C?\n\n");
    printf("A) int\nB) bool\nC) double\n\n>>> ");
    char q3;
    scanf(" %c", &q3);

    if (q3 == 'B' || q3 == 'b') {
        printf("\nRisposta esatta!!\n");
        counter = counter + 10;
        printf("\n----------------------------------------------------\n");
        printf("\nIl tuo punteggio finale è: %d\n\n", counter);
        printf("----------------------------------------------------\n\n");
        printf("Le domande sono terminate!\n");
    } else {
        printf("\nPeccato! Risposta errata!\n");
        printf("\n----------------------------------------------------\n");
        printf("\nIl tuo punteggio finale è: %d\n\n", counter);
        printf("----------------------------------------------------\n\n");
        printf("Le domande sono terminate!\n");
    }
}

// Funzione main

int main() { 
    char start;
    ascii_banner();
    
    do { // Viene valutato l'input iniziale dell'utente sulla funzione game_start. Se A si gioca una partita, se B si chiude il programma

        start = game_start();
        switch (toupper(start)){
            case 'A':
                questions();
                break;
            case 'B':
                printf("\nAlla prossima!\n");
                exit(1);
                break;
            default:
            printf("\nOpzione non valida.\n"); // Gestisce l'errore in caso venga selezionata un'opzione diversa da A e B
        }

    } while (toupper(start) != 'B'); // Qualora l'input dell'utente sia diverso da B il programma riparte da capo
    return 0;
}
