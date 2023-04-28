#include <stdio.h>
#include <stdlib.h>

#define DIVIDE printf("================================================================\n")

void set_IP();

int main(void) {
    while (1) {
        char op;
        DIVIDE;
        printf("(1) Show ipmiitool IP\n");
        printf("(2) IP setting\n");
        printf("(3) FAN setting\n");
        printf("(4) Remote\n");
        printf("(q) Leave\n");
        printf("Option:");
        scanf("%s", &op);  // 修正 %s 為 %c
        DIVIDE;

        if(op == '1'){
            printf("What are you looking for!\n");
        }
        else if(op == '2'){
        	//printf("What are you looking for!\n");
            set_IP();
        }
        else if(op == 'q'){
            break;
        }
        else{
            printf("Wrong!\n");
        }
    }

    system("pause");
    return 0;
}

void set_IP() {
    
    while(1){
    	char op_IP;
    	DIVIDE;
	    printf("(1) Static\n");
	    printf("(2) DHCP\n");
	    printf("(q) Go back\n");
	    printf("Option:");
	    scanf("%s", &op_IP);  // 修正 %s 為 %c
	    DIVIDE;
	    if(op_IP == '1'){
	        printf("Static!\n");
	        continue;
	    }
	    else if(op_IP == '2'){
	        printf("DHCP!\n");
			continue; 
	    }
	    else if(op_IP == 'q'){
	        break;
	    }
	    else{
	        printf("Wrong!\n");
	        continue;
	    }
	}
    
}

