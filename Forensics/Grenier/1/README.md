# Grenier 1/3

| Catégorie  | Forensics   |
|------------|-------------|
| Difficulté | Easy 😊   | 
| État       | A tester 🎯 |
## Description

J'ai retrouvé un vieil ordi qui trainait dans le grenier de mes parents, on avait arrêté de l'utiliser après que mon père ait lancé un virus bien violent !

Je n'ai plus le mot de passe, mais on va utiliser nos compétences forensiques pour voir ce qu'on peut retrouver comme info dessus.

-----

- Quel est le prénom de mon père ?
- Que représente la photo de profil de son compte ?
- Quel est le SID de son compte ?

Flag format : `CYBN{Marcel_ballon_S-1-5-21-xxxxx-xxxxx-xxxxx-xxxxx}`

- Auteur : NozZy

## Fichier
[grenier.7z](https://files.cybernight-c.tf/grenier.7z)

## Flag
||`CYBN{grenouille_Franck_S-1-5-21-725345543-1390067357-1417001333-1003}`||

## Pistes
autopsy advised
account info
	- photo du compte, seule image .bmp en double avec nom du compte (grenouille)
	- nom du compte (Franck)
	- SID du compte (S-1-5-21-725345543-1390067357-1417001333-1003)
