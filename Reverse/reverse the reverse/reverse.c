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

	char str1[] = "{NBYC";
	char str2[] = "_W0nK_u0Y";
	char str3[] = "_o7_W0h";
	char str4[] = "}35Rev3R";
	char input[30];

	int size = strlen(str1) + strlen(str2) + strlen(str3) + strlen(str4);

	char *result = malloc(size + 1);

	r(str1);
	r(str2);
	r(str3);
	r(str4);

	strcpy(result, str1);
	strcat(result, str2);
	strcat(result, str3);
	strcat(result, str4);

	printf("Only true reverser know the password!\nWhats the password: ");
	gets(input);
	if (!strcmp(input, result)) {
		printf("You are a true reverser! Use this password as the flag.");
	} else {
		printf("No, you are not a true reverser. Try again.");
	}
}
