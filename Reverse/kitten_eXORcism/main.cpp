#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

const char KEY[] = "\xde\xad\xbe\xeflikes\xc0\xff\xea";
const char CIPHER[] = "\x9d\xf4\xfc\xa1\x17\x10X\x16,\xb7\xcc\xb5\xa6\x9d\xcc\xb0]\x07Z\x11,\xad\xc7\xd5\xe1\xd0";

std::size_t strlen(const char* str)
{
	std::size_t acc = 0;
	while (*str)
	{
		acc++;
		str++;
	}
	return acc;
}

int main(int argc, char* argv[])
{
	if (argc < 2)
	{
		fprintf(stderr, "usage: ./chall <password>\n");
		return EXIT_FAILURE;
	}

	printf("lemme think about it ...");
	sleep(1);
	bool has_failed = false;
	std::size_t length = strlen(CIPHER);
	std::size_t i = 0;
	while (i < strlen(CIPHER) && i < strlen(argv[1])) {
		char cflag = CIPHER[i] ^ KEY[i % strlen(KEY)];
		if ( cflag != argv[1][i])
			has_failed = true;
		i++;
	}
	if (i != length || has_failed) goto failure;

	printf("Yay :)\n");
	return EXIT_SUCCESS;

	failure:
		printf("0x90");
		return EXIT_FAILURE;
}
