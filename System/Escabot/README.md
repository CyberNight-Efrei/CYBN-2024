# Escabot

| Système     |
|-------------|
| Moyen 🙂    |
| Validé ✅  |
## Description

Bienvenue à cette introduction à l'escalade de privilèges sur système Linux !

Vous démarrez avec un compte symbolisé par une marche, et devez grimper les marches une par une jusqu'à arriver à la dernière disponible.

Chaque objet d'escalade possède un thème, qui vous sera utile à comprendre afin de grimper les marches !

------

L'escabot comporte quatre marches : de **marche3** à **marche6**
La dernière marche possède un flag dans ~/flag.txt

Le thème de l'escabot est : **Set User/Group ID**

|          |           |
|----------|-----------|
| User     | marche3   |
| Password | `marche3` |

------

- Auteur : NozZy

## Flag
||`CYBN{sU1d_i5_v3Ry_s3nSIT1ve_B3_c@reFUL}`||

## Pistes
SUID / GUID
find -perm /2000 (guid)
change env an copy fake ls to your env
command injection ;
