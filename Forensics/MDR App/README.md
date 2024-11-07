# MDR App

| Forensics   |
|-------------|
| Easy 😊   |
| A tester 🎯 |
## Description

Mon frère s'est connecté à mon ordi, et il me dit s'être amusé un peu avec.
Depuis, il y a un nouveau compte de créé, donc je l'ai supprimé... Mais il a tendance à revenir
J'ai peur qu'il ait fait plus de trucs que je ne vois pas.

Tu peux m'aider à comprendre ce qu'il a fait ?

Le flag est composé de :
- Mot de passe du compte créé
- Technique Mitre utilisée par son frère pour que le compte continue d'apparaître
- Le mot de passe qui a été volé

Exemple : `CYBN{Password_T1234_XXXXXXXXXXXX}`

- Auteur : NozZy

## Fichiers (si besoin)
[MDR App.7z](https://files.cybernight-c.tf/MDR%20App.7z)

## Indices
1. Le compte semble apparaître à nouveau quand je fais des screenshots...

## Flag
||`CYBN{MyDearBrother_T1546_!!foto**12345}`||

## Pistes
Fichier de conf/historique ShareX
net user brother MyDearBrother /add && net localgroup administrateurs brother /add
Persistence par trigger => T1546
URL de screenshot sharex, mdp jaune
