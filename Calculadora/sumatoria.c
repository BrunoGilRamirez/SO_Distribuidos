#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <unistd.h>
int main (int argc, char *argv[]) {
    printf("pid: %d\n", getpid());
    if(argc<2) {
    exit(1);
    }
    int sum;
    for (int i=1; i<argc; i++) {
        sum += atoi(argv[i]);
    }
    printf("Sumatoria: %d\n",sum);
    return 0;
}