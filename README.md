# Projet IFT-7020

Lors de ce projet, nous souhaitons générer des horaires sportifs sous contraintes. Une première version des contraintes à respecter se trouvent [au lien suivant](https://support.exposureevents.com/hc/en-us/articles/115002080888-Import-restrictions-Director-).

Toutefois, ces contraintes ne définissent pas de façon exhaustive les éléments nécessaires à la planification d'un tournoi sportif. Les éléments importants à définir qu'il faut passer au modèle sont les suivants:

+ Équipes
    + Division correspondante
    + Coach (plusieurs équipes ayant le même coach ne peuvent pas jouer en même temps)
+ Emplacements/Lieux des parties (multi-niveaux)
    + Venue (lieu 1)
    + Court (terrain A, B, C)
+ Plages de disponibilité de chacun des lieux
+ Durée d'une partie
    + Durée entre deux parties (s'il y a lieu)

Pour ce projet, nous souhaitons traiter une seule structure de tournoi, soit la planification d'un _single round robin_ pour chaque division. Autrement dit, on souhaite que chaque équipe joue contre toutes les équipes de sa division exactement une fois.

Les contraintes obligatoires que nos horaires générés doivent respecter sont les suivantes:

+ Chaque équipe joue contre chaque équipe de sa division exactement une fois.
+ Deux parties ne sont jamais jouées en même temps à un même emplacement.
+ Toutes les parties sont jouées dans les plages de disponibilité des emplacements.
+ Chaque partie a la durée définie.
+ Temps minimal entre deux parties est respecté.

Également, notre modèle doit s'efforcer de respecter les préférences suivantes (du mieux possible):

+ Préférences de date/heures de chaque équipe (équipe 1 préfère jouer après 16h, pas le 24, etc...).
+ Restrictions de lieux (maximum x parties pour y date à z venue/l court).
+ Tables de contraintes avec poids.
+ Les équipes ayant le même coach ne jouent pas en même temps (aucun coach ne doit être découpé).
+ Une équipe ne joue pas deux parties de suite.
+ Toutes les équipes de chaque division ont le même nombre maximal de parties par jour.
+ Le nombre de parties par jour est bien balancé pour toutes les équipes (idéalement une par jour).
+ Groupes de force* (séparer les divisions en n groupes et alterner les parties entre les groupes de force).
+ Pas de déplacement entre différentes venues dans une même journée

Les modèles seront comparés selon deux bases:

+ Nombre de contraintes brisées par l'horaire généré (à minimiser).
+ Temps de calcul pour obtenir l'horaire.
