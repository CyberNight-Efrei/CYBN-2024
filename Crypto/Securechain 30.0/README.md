# Securechain 30.0

| Catégorie  | Forensics |
|------------|-----------|
| Difficulté | Facile 😊  |
| État       | A tester 🎯    |
## Description

Un service de gestion de comptes vous permet d'en créer ou de vous y connecter. Cependant, il semble qu'un des comptes existants cache un secret !
Connectez-vous à ce compte pour leur démontrer que la clé n'est pas si sécurisée...

- Auteur : ThaySan

## Flag
||`CYBN{br34k_th3_md5_l00p}`||

## Pistes
Remarquer que la clé générée à la création d'un compte est du MD5. S'aider du titre du challenge pour comprendre que la clé est un MD5 chainé 30 fois de l'ID. Se connecter au compte admin, son ID est dans les crédits.