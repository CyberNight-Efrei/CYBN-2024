# Bienvenue chez les Pabètes !

| Catégorie  | Misc      |
|------------|-----------|
| Difficulté | Facile 😊 |
| État       | Validé ✅ |
## Description

Bienvenue au pays des pabetes. Les pabetes sont des êtres simplets, mais malgré cela, ils réussissent à bien survivre dans la forêt des sirzewltb en utilisant un langage très simple qui est censé pouvoir tout dire. 

Le chef de pabetes est Caesar, voici ce qu'il vous dit:

>La forêt regorge bien de secrets.
>Son nom en premier,
>Mon nom en second,
>17 est le chiffre sacré

Une fois son poème récité, il vous en explique comment les pabetes parlent :

> Quand on veut avancer, on dit ba, pour reculer, on dit bu, quand on veut augmenter, on dit boo, on dit bee quand on veut descendre, on commence souvent les boucl..choses par po et on les finit par pa, et enfin quand on veut dire ce qu'on a sur le cœur, on dit bilibili

Puis il finit par vous donner un parchemin qui contient ceci :

>boo boo boo boo boo boo boo boo po ba boo boo boo boo boo boo boo boo bu bee pa ba boo boo boo bilibili 
>bu boo boo boo boo boo po ba boo boo boo boo bu bee pa ba boo boo bilibili
>bu boo boo boo boo boo po ba bee bee bee bee bee bu bee pa ba boo boo bilibili
>bu boo boo boo boo po ba boo boo boo bu bee pa ba bilibili
>bu boo boo boo boo boo boo boo boo boo boo boo po ba ba boo boo boo boo boo boo boo boo boo boo boo bu bu bee pa ba ba boo boo bilibili
>bu bu boo boo boo po ba ba bee bee bee bu bu bee pa ba ba bee bilibili
>boo boo boo boo bilibili
>bu bu boo boo boo boo boo boo boo boo po ba ba ba ba boo boo boo boo boo boo bu bu bu bu bee pa ba ba ba ba bilibili
>bu bu bu bu boo boo boo boo po ba ba bee bee bee bu bu bee pa ba ba bilibili
>bee bee bee bee bee bee bilibili
>ba ba bilibili
>bu bu bu bu boo boo boo boo po ba ba boo boo boo boo bu bu bee pa ba ba boo boo bilibili
>bu bu boo boo boo boo boo po ba ba bee bee bee bee bu bu bee pa ba ba boo bilibili
>ba ba boo boo boo bilibili
>bu bu boo boo boo boo boo boo bilibili
>bu bu boo boo boo boo boo boo boo po ba ba boo boo boo bu bu bee pa ba ba bilibili

Alors pourriez trouvez le secret du village des pabetes ? 


- Auteur : OnePanthéon (L4kk4s)

## Flag
||`CYBN{qu0ic0ub3h}`||

## Pistes
Brainfuck :

+ + + + + + + + [ > + + + + + + + + < - ] > + + + . 
< + + + + + [ > + + + + < - ] > + + .
< + + + + + [ > - - - - - < - ] > + + .
< + + + + [ > + + + < - ] > .
< + + + + + + + + + + + [ > > + + + + + + + + + + + < < - ] > > + + .
< < + + + [ > > - - - < < - ] > > - .
+ + + + .
< < + + + + + + + + [ > > > > + + + + + + < < < < - ] > > > > .
< < < < + + + + [ > > - - - < < - ] > > .
- - - - - - .
> > .
< < < < + + + + [ > > + + + + < < - ] > > + + .
< < + + + + + [ > > - - - - < < - ] > > + .
> > + + + .
< < + + + + + + .
< < + + + + + + + [ > > + + + < < - ] > > .

boo			+	incrémenter le pointeur
bee			-	décrémenter le pointeur
ba			>	déplacer le pointeur à droite
bu			<	déplacer le pointeur à gauche
po			[	boucle jusque s tant que pointeur non nul
pa			]	fin de boucle
bilibili	.	affiche la valeur ascii du pointeur