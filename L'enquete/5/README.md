# Message codé - L'enquête 5/6

| Enquête (Stegano / Forensics) |
|-------------------------------|
| Moyen 🙂                     | 
| En cours ⏳                   | 
## Description

Michel, j'te paie un coup ce soir.

Un autre si t'arrives à comprendre le message, et dix autres si le message indique le prochain lieu de rendez-vous !

Probablement qu'il notait ses rendez-vous quelque part, il devait pas décoder ça à chaque fois pour s'en rappeler.

Format : `CYBN{jj-mm_hh:mm}`

- Auteur : NozZy

## Indices
1. Les messages ressemblent à des rendez-vous. Peut-être les notait-il quelque part ?

## Flag
||`CYBN{30-10_14:15}`||

## Pistes
Messages codé pour décrire date de RDV :

Message :
A=2
B=22
C=222
D=3
E=33
F=333
G=4
H=44
I=444
J=5
K=55
L=555
M=6
N=66
O=666
P=7
Q=77
R=777
S=7777
T=8
U=88
V=888
W=9
X=99
Y=999
Z=9999

Ciné = allégorie "lieu de RDV"
Séance = semaine
Prix = touches clavier
Salle = heure
Rang = minutes

---

Exemple :

J 19h = 5 / 19 -> jeudi 11/07 19h
---------------
> S. - Envoyé le 07 juillet 2024
Il faudrait d'ailleurs que tu passes au ciné, celui dont je t'ai parlé. Une place à 5€, pour la séance prochaine, salle 19.


S 17h = 7777 / 17 / Séance+1 -> Samedi 03/08 17h 16h30
---------------------
> S. - Envoyé le 21 juillet 2024
On se refait un ciné. Pas la séance prochaine, la suivante, salle 17. Tu pourras prendre 4 popcorn à 7€.


V 17h30 = 888 / 11 -> Vendredi 13/09 11h 17h30
--------------
> S. - Envoyé le 09 septembre 2024
On doit voir le nouveau film. Les prix ont augmenté, 3 popcorn à 8€, salle 11. Prochaine séance.


D 18h30 = 3 / 18 -> Mardi 13/10 18h30
--------------- 
> S. - Envoyé le 10 octobre 2024
Nouvelle séance de film, la suivante. Même ciné, salle 18, rang 30. Prends moi la bouteille à 3€.


Me 14h15 = 6 33 -> Mercredi 30/10 14h15
---------------
> S. - 25 octobre 2024
On a un nouveau film à se voir. La bouteille à 6€33 sera parfait pour nous. C'est salle 14, range 15. Prochaine séance.
