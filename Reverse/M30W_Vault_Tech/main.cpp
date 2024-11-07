#include <iostream>
#include <fstream>
#include <vector>
#include <openssl/sha.h>

#define NDIGEST 20
#define NKEY 16

long strlen(char* str)
{
    long acc = 0;
    while (*str)
    {
        acc++;
        str++;
    }
    return acc;
}

bool strcmp(char* a, char* b)
{
    if (strlen(a) != strlen(b))
        return false;

    while(*a)
    {
        if (*a != *b)
            return false;
        a++;
        b++;
    }
    return true;
}

unsigned char*
weird_rc4(unsigned char *plaintext, unsigned long nplaintext, unsigned char *key)
{ 
    unsigned char state[256] = {0};
    for (unsigned int i = 0; i < 256; i++)
    {
        state[i] = i;
    }

    unsigned int seed = 0x574f454d;
    srand(seed);
    unsigned int j = 0;
    for (unsigned int i = 0; i < 256; i++)
    {
        j = (j + state[i] + key[i % NKEY] + (rand() & 0xf)) & 0xFF;
        int tmp = state[j];
        state[j] = state[i];
        state[i] = tmp;
    }

    unsigned char* cipher = (unsigned char*)malloc(nplaintext);
    unsigned int i = 0;
    j = 0;
    for (unsigned int k = 0; k < nplaintext; k++)
    {
        int tmp = state[j];
        state[j] = state[i];
        state[i] = tmp;
        cipher[i] = state[(state[i] + state[j]) & 0xFF] ^ plaintext[i];
        i = (i+1) & 0xFF;
        j = (j+1) & 0xFF;
    }

    return cipher;
}

unsigned char* get_digest(char* password, long size)
{
    unsigned char* digest = (unsigned char*)malloc(NDIGEST);
    SHA_CTX sha;
    SHA1_Init(&sha);
    SHA1_Update(&sha, password, 2);
    SHA1_Final(digest, &sha);
    return digest;
}

unsigned char* make_key(char* password, long npassword)
{
    unsigned char* digest = get_digest(password, npassword);
    char* tmp_key = (char*)"M30W";
    unsigned char* key = (unsigned char*)calloc(16, 1);
    for (unsigned int i = 0; i < 8; i++)
        key[i]=digest[i];
    for (unsigned int i = 0; i < 8; i++)
        key[i+8]= ((unsigned char*)password)[i % npassword] ^ tmp_key[i % 4];
    return key;
}

int main(int argc, char *argv[])
{
    std::cout << "-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=--" << std::endl;
    std::cout << "     SECURE M30W VAULT TECH      " << std::endl;
    std::cout << "              Unique,            " << std::endl;
    std::cout << "             Premium ,           " << std::endl;
    std::cout << "         State of the art,       " << std::endl;
    std::cout << "           CRYPTAGE :3           " << std::endl;
    std::cout << "-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=--" << std::endl;

    if (argc < 3)
    {
        std::cerr << "usage: meow_vault <file> <password> [--decrypt]" 
                    << std::endl;
        return EXIT_FAILURE;
    }

    bool decrypt = false;
    if (argc > 3 && strcmp(argv[3], (char*)"--decrypt"))
    {
        std::cout << "Decrypting service selectionned" << std::endl;
        decrypt = true;
    }
        

    FILE *fin = fopen(argv[1], "r");
    if (!fin)
    {
        std::cerr << "Could not open file " << argv[1] << std::endl;
        return EXIT_FAILURE;
    }

    fseek(fin, 0, SEEK_END);
    long size = ftell(fin);
    fseek(fin, 0, 0);

    char* content = (char *)malloc(size);
    fread(content, 1, size, fin);
    fclose(fin);

    if (decrypt)
    {
        content+=NKEY;
        size-=NKEY;
        if (size < 0)
        {
            std::cerr << "Invalid file" << std::endl;
            return EXIT_FAILURE;
        }
    }

    unsigned char* key = make_key(argv[2], strlen(argv[2]));
    char* cipher = (char*)weird_rc4((unsigned char*)content, size, key);

    std::string path(argv[1]);
    if (decrypt)
    {
        path.append(".out");
        std::cout << "Writting plaintext to : " << path << std::endl;
    }
    else
    {
        path.append(".inc");
        std::cout << "Writting secret secured content to : " << path << std::endl;
    }
    FILE* fout = fopen(path.c_str(), "w");
    
    long written = 0;
    if (!decrypt)
        written += fwrite(key, 1, NKEY, fout);
    written += fwrite(cipher, 1, size, fout);
    std::cout << written << " bytes written, enjoy" << std::endl;
    fclose(fout);

    return EXIT_SUCCESS;
}