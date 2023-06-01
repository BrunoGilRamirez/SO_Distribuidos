#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
int main(){
    printf("pid: %d\n", getpid());
    printf("Bienvenido a la calculadora\ndigita la operacion y los parametros");
    char data[1024];
    while (strcasecmp(data,"fin")){
        printf("\ncalculadora$");
        scanf("%[^\n]%*c", &data);
        int i;
        if (strcasecmp(data,"fin")) {i= system(data);}
    }
    
    return 0;

}