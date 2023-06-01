#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <unistd.h>
int main (int argc, char *argv[]) {
    printf("pid: %d\n", getpid());
    if(argc<2) {
    exit(1);
    }
    float sum;
    for (int i=1; i<=atoi(argv[1]); i++) {
        sum += pow(i,2.0);
    }
    printf("Sumatoria de 1 hasta %s es igual: %2f\n", argv[1],sum);
    return 0;
}
