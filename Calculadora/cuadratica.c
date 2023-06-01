#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <unistd.h>
int main(int argc, char *argv[]) {
    printf("pid: %d\n", getpid());
    if(argc<4) {
        exit(1);
    }
    int a= atoi(argv[1]), b=atoi(argv[2]), c=atoi(argv[3]);
    int aux= pow(b,2.0)-((4*a)*c);
    float raiz= sqrt(aux);
    if(a==0){
        exit(2);
    }
    if (aux>0.0){
        printf("\t\t\tLas dos raices son reales");
        float posx= (-b+raiz)/(2*a);
        float negx= (-b-raiz)/(2*a);
        printf("valor de x1= %6f\nvalor de x2= %6f\n",posx,negx);
    }
    if (aux==0.0){
        float x1=(-b)/(2.0*a);
        printf("La ecuacion solo tiene una raiz %.2f\n", x1);
        exit(3);
    }else{
        float xr=(-b/(2.0*a));
        float xi=(sqrt(-aux)/(2.0*a));
        printf("xreal es %.2f\nximg es %.2f\n", xr, xi);
        exit(4);
    }

return 0;
}
