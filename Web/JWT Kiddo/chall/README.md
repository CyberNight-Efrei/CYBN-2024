# FlagForum

| Catégorie  | Programmation |
|------------|---------------|
| Difficulté | Moyen 🙂      |
| État       | Validé ✅      |
## Description

J'ai découvert un forum assez étrange, apparement ça se refile des solutions sous le manteau pour la CyberNight... Il faudra pouvoir accèder au compte de l'administrateur du site pour révéler ses plus sombres secrets ! 

- Auteur : ThaySan

## Flag
||`CYBN{h4ck3r_2_h4ck3r5}`||

# Pistes

L'objectif de ce challenge est d'identifier une LFI dans le kid de l'access_token puis de l'exploiter en générant une paire de clé RSA dont la privée sert à signer un access_token forgé et la publique à être inclue pour vérifier celui-ci.

## Skills Required

- Savoir analyser le traffic HTTP
- Avoir connaissances basiques concernant les JWT
- Avoir connaissances basiques concernant les LFI
- Etre capable de générer des clés RSA
