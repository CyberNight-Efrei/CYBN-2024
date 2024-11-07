#include <stdio.h>
#include <time.h>
#include <stdlib.h>

void get_random()
{
    srand(time(NULL));
    int r = rand();
    printf("%d\n", &r);
}
