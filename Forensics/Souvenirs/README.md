# Mémoire de poisson 🐟

| Forensics    |
|--------------|
| Nightmare  |
| A tester 🎯  | 
## Description

J'ai encore perdu la mémoire... La seule chose dont je me souvienne à peu près, c'est Nemo.. Mais je ne sais même plus qui c'est..

Heuresement cette fois, j'ai pensé à enregistrer mes souvenirs proprement !

Tu peux m'aider à retrouver la mémoire ?

- Auteur : NozZy

## Fichiers (si besoin)
[souvenirs.7z](https://files.cybernight-c.tf/souvenirs.7z)

## Indices
1. J'ai essayé de sauvegarder mes mots de passe et code, mais impossible de me souvenir où...


## Flag
||`CYBN{J'a1_r3Tr0uV3_m@_Mem01Re}`||

## Pistes
 - AES key in memory => mount fs
 - memory => clipboard password (bash history hint) on fish.7z
 - jwt => hash => google => password : yep59f$4txwrr => stegseek
 - mysql history => password : n3m03@tsy0urf@ce => flag chiffré => flag

LUKS key in mem  -> clipboard   -> password SHA in cookie -> mysql_history -> AES-CBC-128
Disk chiffré     -> zip chiffré -> image steghide         -> flag chiffré  -> flag
