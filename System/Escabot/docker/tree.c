#include <unistd.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char** argv, char** envp) {
  setreuid(geteuid(), geteuid());
  char command[32] = "/bin/tree ";
  strcat(command, argv[1]);
  system(command);
  return 0;
}
