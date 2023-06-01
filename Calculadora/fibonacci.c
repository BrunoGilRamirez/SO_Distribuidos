#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
int main(int argc, char *argv[]){
  printf("pid: %d\n", getpid());
  int t1 = 0, t2 = 1;
  int sigTerm = t1 + t2;
  if(argc<2) {
    exit(1);
  }
  int n=atoi(argv[1]);
  printf("El número de términos: %i \n",n);
  printf("Serie Fibonacci: %d, %d ", t1, t2);
  for (int i = 3; i <= n; ++i) {
      sleep(1);
      printf(" ,%d", sigTerm);
      t1 = t2;
      t2 = sigTerm;
      sigTerm = t1 + t2;
    }
  printf (".\n");
  return 0;
}
