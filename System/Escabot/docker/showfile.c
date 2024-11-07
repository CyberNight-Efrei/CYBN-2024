#include <unistd.h>
#include <stdio.h>

int main(int argc, char** argv, char** envp) {
  char *args[] = {"ls", "-l", "-a", argv[1], NULL};
  execvpe(args[0], args, envp);
  return 0;
}
