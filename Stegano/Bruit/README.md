# Bruit

| Catégorie  | Stegano  |
| ---------- |----------|
| Difficulté | Moyen 🙂 |
| Etat       | Validé ✅ |

## Description

Moins fort !!! Tu fais trop de bruit !!!

- Auteur : NozZy

## Fichier
![noise.png](noise.png)

## Flag
||`CYBN{N01s3_I5_No7_OnLy_1N_50UnD}`||


## Pistes
decode.py

get all Red bytes (left to right, top to bottom)
remove text, keep PNG bytes and save image
image is corrupted, look at hex in middle => remove noisy text : image is fixed