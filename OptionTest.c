#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define DIVIDE printf("================================================================\n")

void set_IP();

int main(void) {
    char op[10];
    while (1) {
        DIVIDE;
        printf("(1) Show ipmiitool IP\n");
        printf("(2) IP setting\n");
        printf("(3) FAN setting\n");
        printf("(4) Remote\n");
        printf("(q) Leave\n");
        printf("Option:");
        fgets(op, sizeof(op), stdin);
        op[strlen(op)-1] = '\0';
        DIVIDE;

        if (strcmp(op, "1") == 0) {
            printf("What are you looking for!\n");
        } else if (strcmp(op, "2") == 0) {
            set_IP();
        } else if (strcmp(op, "q") == 0) {
            break;
        } else {
            printf("Wrong!\n");
        }
    }

    printf("Press Enter to exit...");
    while (getchar() != '\n');
    return 0;
}

void set_IP() {
    char op_IP[10];
    while(1){
        DIVIDE;
        printf("(1) Static\n");
        printf("(2) DHCP\n");
        printf("(q) Go back\n");
        printf("Option:");
        fgets(op_IP, sizeof(op_IP), stdin);
        op_IP[strlen(op_IP)-1] = '\0';
        DIVIDE;
        if (strcmp(op_IP, "1") == 0) {
            printf("Static!\n");
        } else if (strcmp(op_IP, "2") == 0) {
            printf("DHCP!\n");
        } else if (strcmp(op_IP, "q") == 0) {
            break;
        } else {
            printf("Wrong!\n");
        }
    }
}
