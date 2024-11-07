# Grenier 3/3

| Catégorie  | Forensics   |
|------------|-------------|
| Difficulté | Medium 🙂   | 
| État       | A tester 🎯 |
## Description

Haha quelle bouille j'avais !

Bon, et si on s'attaquait au virus qu'a téléchargé papa ?

-----

- Quel est le hash md5 du virus ?
- Quelle est sa date d'exécution ?
- Quelle est la seed cryptographique Windows générée à son exécution ? (32 premiers caractères hexadécimaux)

Flag format : `CYBN{5f10dc15a21f11866d71692607042420_jj-mm-aaaa_hh:mm:ss_6e766572676f6e6167697665796f7570}`

- Auteur : NozZy

## Fichier
[grenier.7z](https://files.cybernight-c.tf/grenier.7z)

## Flag
||`CYBN{4ed4e1009dc7e7b67600731b98b534b2_08-06-2017_21:15:26_0f39e4ee5a25dd5888c53499203bf48f}`||

## Pistes
About malware
	- Hash, setup.exe in suspicious location (4ed4e1009dc7e7b67600731b98b534b2)
	- Date and time of execution (C:\Windows\Prefetch\SETUP.EXE-345388FD.pf -> 2017-06-08 21:15:26)
	- Registry key changes (%WINDIR%\config\software\Microsoft\Cryptography\RNG\Seed -> 0F39E4EE5A25DD5888C53499203BF48F)
