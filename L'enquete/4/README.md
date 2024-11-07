# Saisie - L'enquête 4/6

| Enquête (Forensics / Web) |
|---------------------------|
| Moyen 🙂                  | 
| A tester 🎯               |

## Description

- 25 Octobre 2024

Ca c'est mon Michel ! La perquisition a fait son affaire, on a désormais une liste de contacts avec qui il échange.

On a bien la preuve qu'il semble échanger régulièrement avec notre **Somier**, et même qu'ils se rencontrent...

Si on pouvait chopper leur prochain rendez-vous, ce serait parfait !

Ah d'ailleurs, il y avait un autre ordi sur place, une tour cette fois. Le disque est chiffré, on pourra rien en faire. Par contre, on a pu récupérer **sa mémoire vive** ! 

Il devait se connecter à son site web depuis ce poste, essaie de retrouver des traces de leurs échanges.

- Auteur : NozZy

## Files

https://files.cybernight-c.tf/DESKTOP-5U82BDL.7z

## Indices
1. Il doit bien y avoir une trâce permettant de se connecter sur son compte quelque part.
2. Il ne semblait rien stocker sur cet ordi, mais les applications elles doivent stocker tout plein de choses.

## Flag
||`CYBN{La_TR0nch3_Du_C0oKie}`||

## Pistes
Forensics => Trouver cookie session
analyser cookie => construire vrai cookie qui marche => admin => flag

COOKIE : chifre d'un timestamp d'expiration du cookie + chiffres ASCII du nom de compte en MAJ (ADMIN => 6568777378)
