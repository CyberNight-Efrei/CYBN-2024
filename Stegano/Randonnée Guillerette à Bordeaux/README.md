# Randonnée Guillerette à Bordeaux

| Catégorie  | Stegano      |
|------------|--------------|
| Difficulté | Difficile 😠 |
| État       | A tester 🎯  |
## Description

Ceci est une photo de lapin un peu spéciale.

![daisy.png](daisy.png)

- Auteur : NozZy

## Fichiers (si besoin)
[daisy.png](daisy.png)

## Flag
||`CYBN{LSB_RGB_1s_fUck1NG_diSgu5T1Ng}`||

## Pistes
LSB diagonal, R then G then B
``bash
python3 LSB.py daisy.png -o flag.txt -d diagonal
``