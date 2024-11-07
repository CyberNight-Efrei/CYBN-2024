# Co(mpressed)okies

| Catégorie  | Web |
|------------|-----------|
| Difficulté | Facile 😊  |
| État       | A tester 🎯 |

## Description

J'ai entendu dire que sérialiser ses objets et les renvoyer au client pouvait être dangereux. Du coup, je suis en train d'expérimenter une nouvelle façon de stocker des données ! J'ai tellement confiance en ce système que je me suis permis de cacher une partie du flag directement sur la machine 😎

- Auteur : Romain

## Flag
||`CYBN{Wh4t_4_w31rd_w4y_t0_st0r3_d4t4}`||

## Pistes
Récupérer le .zip dans les cookies, éditer user en admin dans le fichier pour avoir la première partie du flag, rajouter `; import os; os.system('sh ...')` à la fin d'une des lignes éditables pour récupérer la seconde partie
