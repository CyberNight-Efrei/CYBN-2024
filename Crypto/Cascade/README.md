# Cascade

| Catégorie  | Crypto |
|------------|-----------|
| Difficulté | Moyen 🙂  |
| État       | A tester 🎯    |
## Description

Un oracle de chiffrement est à votre disposition. Envoyez-lui des messages, et il vous retournera leur version chiffrée.
Mais attention, un secret est ajouté à la fin de votre message avant le chiffrement, à vous de le trouver !

FLAG_CHARSET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789#$-?!@_{}'

- Auteur : ThaySan

## Flag
||`CYBN{C45c4d3_R3v34l3d}`||

## Pistes
En envoyant des messages de différentes longueurs, on peut observer comment le chiffrement change. En ajustant progressivement la taille du message, on peut isoler la partie chiffrée correspondant au flag ajouté à la fin. Répéter ce processus permet de deviner le flag caractère par caractère en déduisant les changements.
