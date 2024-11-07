# Laverie sans contact

| Catégorie  | Hardware     |
|------------|--------------|
| Difficulté | Difficile 😠 |
| État       | A tester 🎯  |
## Description

Lors d'un voyage au Canada, je suis allé dans un laverie où l'on devait payer avec des cartes à puce.

En lisant une de ces cartes à puce avec mon Flipper Zero, je me suis rendu compte qu'il s'agissait d'une carte "CSC Service Works" et qu'il ne restait que **0$** sur ma carte...

Sauf qu'une machine à laver coûte **4$**... Aidez-moi à faire ma machine à laver pour obtenir le flag de challenge !

- Auteur : DocSystem

## Indices
1. Recherchez des modifications du firmware du Flipper Zero avec le support de plus de cartes NFC

## Flag
||`CYBN{W4sh1ng_f0r_r33F}`||

## Pistes
Trouver le code du lecteur de carte dans un firmware de Flipper Zero (exemple : [csc.c](https://github.com/RogueMaster/flipperzero-firmware-wPlugins/blob/420/applications/main/nfc/plugins/supported_cards/csc.c))

Créer un algorithme "inverse" pour modifier le contenu de la carte et modifier le solde, le dernier refill et son checksum.
