#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
struct calculadora
{
    char input[30]
};
void errorcatcher(char args[],int status){
    if(strcmp(args,"./fibo")==0){
        switch (status) {
        case 0:
            printf("\ncalculadora$ %s termino con exito\nestado: %i\n",args,status);
        break;
        case 1:
            printf("\ncalculadora$ %s\nestado: %i\n Faltaron argumentos de ejecucion\n",args,status);
        break;
        }
    }
    if(strcmp(args,"./cuad")==0){
        switch (status) {
        case 0:
            printf("\ncalculadora$ %s termino con exito\nestado: %i\n",args,status);
        break;
        case 1:
            printf("\ncalculadora$ %s \nestado: %i\n Faltaron argumentos de ejecucion\n",args,status);
        break;
        case 2:
            printf("\ncalculadora$ %s\nestado: %i\n No se puede dividir entre 0\n",args,status); 
        break;
        case 3: 
            printf("\ncalculadora$ %s\nestado: %i\n Solo tiene una raiz\n",args,status); 
        break;
        case 4: 
            printf("calculadora$ %s\nestado: %i\nSon raices complejas\n",args,status);
        break;
        }
    }
    if(strcmp(args,"./sum")==0){
        switch (status) {
        case 0:
            printf("\ncalculadora$ %s termino con exito\nestado: %i\n",args,status);
        break;
        case 1:
            printf("\ncalculadora$ %s\nestado: %i\n Faltaron argumentos de ejecucion\n",args,status);
        break;
        }
    }
    if(strcmp(args,"./sumc")==0){
        switch (status) {
        case 0:
            printf("\ncalculadora$ %s termino con exito\nestado: %i\n",args,status);
        break;
        case 1:
            printf("\ncalculadora$ %s\nestado: %i\n Faltaron argumentos de ejecucion\n",args,status);
        break;
        }
    }
    
}

int main(){
    char buff[100];
    printf("pid: %d\n", getpid());
    while (strcasecmp(buff,"fin")){
        struct calculadora calculadora[100];
        char aux[40];
        int x,y=0,i=0;
        printf("\ncalculadora$ ");
        scanf("%[^\n]%*c", &buff);
        int z=strlen(buff);
        for(x=0;x<=z;x++){
            if (buff[x] == ' '||x==z){
                strcpy(calculadora[y].input,aux);
                y++;
                for(int c=0;c<i;c++){
                aux[c]=NULL;
                }
                i=0;
            }
            if(buff[x] != ' '){
                aux[i] = buff[x];
                i++;
            }
            
        }
        char *args[100];
        for ( i=0;i<y;i++){
            args[i] = calculadora[i].input;
            args[i+1] = NULL;
        }
        if((strcmp(args[0],"./fibo")==0)||(strcmp(args[0],"./cuad")==0)||(strcmp(args[0],"./sum")==0)||(strcmp(args[0],"./sumc")==0)){
            int wstatus;
            pid_t _child= fork(), a;
            if(_child==-1){
                printf("fork error\n");
                exit(1);
            }
            if(_child==0){
                execv(args[0],args);
            }else{
                a = waitpid(_child, &wstatus, WUNTRACED | WCONTINUED);

                if(WIFSIGNALED(wstatus)==1){
                    printf("Al prceso %s lo han exterminado\n",args[0]);
                    printf("WIFEXITED %i\n",WIFEXITED(wstatus));
                }else{
                    errorcatcher(args[0],WEXITSTATUS(wstatus));
                    printf("WIFEXITED %i\n",WIFEXITED(wstatus));
                }
                
            }
        }
        

    }
    return 0;

}