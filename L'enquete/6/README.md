# RDV - L'enquête 6/6

| Enquête (Forensics / OSINT) |
|-----------------------------|
| Difficile 😠               | 
| A tester 🎯                | 

## Description

On y est presque ! On sait enfin quand ils étaient censés se revoir !!

Ouais bon, vu qu'on sait pas où, les dix coups tiennent plus...

Par contre on n'a pas de nouveaux éléments, et l'autre Patrick refuse toujours de dire quoi que ce soit.

Doit bien y avoir des traces de leurs dernières rencontres, et de leur lieu de rencontre habituel...

*Le flag est les coordonnées du lieu de rencontre, à deux unités après la virgule*

Format : `CYBN{12.34,56.78}`

- Auteur : NozZy

## Indices
1. Je suis persuadé qu'il emmenait son ordi portable avec lui pendant les rendez-vous.

## Flag
||`CYBN{47.32,5.0[34]}`||

## Pistes
Forensics 	: dates de RDV (Agenda) => Logs du PC (part 3)
OSINT 		: Logs WiFi à chaque RDV (hint WiFi dans document) => https://wigle.net/ for location
47.323093525196775, 5.0349948096162995
