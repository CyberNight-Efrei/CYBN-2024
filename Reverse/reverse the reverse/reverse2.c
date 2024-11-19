#include <stdlib.h>
#include <stdio.h>
#include <string.h>

void r(char* str) {
	int first = 0;
	int last = strlen(str) - 1;
	char temp;

	while (first < last) {
		temp = str[first];
		str[first] = str[last];
		str[last] = temp;

		first++;
		last--;
	}
}

void main() {

	char str1[] = "}35Rev3R_o7_W0h_W0nK_u0Y{NBYC";
	char input[30];

	r(str1);

	printf("Only true reverser know the password!\nWhats the password: ");
	gets(input);
	if (!strcmp(input, str1)) {
		printf("You are a true reverser! Use this password as the flag.");
	} else {
		printf("No, you are not a true reverser. Try again.");
	}
}
