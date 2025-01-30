# DEC_POMDP
Contrôle continue dans le cadre du cour : (SMINF3D2) Processus décisionnels avancés

## Partie 1

- **BFS.txt** : Commande et trace d'exécution de l'algorithme BFS sur le problème GridSmall.
- **JESP.txt** : Commande et trace d'exécution de l'algorithme JESP sur le problème GridSmall.

## Partie 2

### 1.

- **src** : Dossier contenant les fichiers sources de l'algorithme Best Response avec comme base l'algorithme JESP version dynamique de MADP.
- **bin** : Dossier contenant le fichier binaire de l'algorithme Best Response.
- **Makefile** : Fichier pour générer le binaire avec la commande `make`
- **grid_small.dpomdp** : Fichier du problème GridSmall

### 2.

    Politique BEST_RESPONSE : Cette politique cherche à maximiser les gains de l'agent 0 en considérant la politique fixée de l'agent 1. Si l'agent 1 reste toujours immobile, l'agent 0 optimise son déplacement pour atteindre un état optimal (ici, se déplace en down ou left selon la configuration).

    Politique MDP : Si un MDP est utilisé pour permettre à l'agent 0 d'aller explicitement vers la position de l'agent 1, la politique calculée pourrait consister à réduire la distance entre les deux agents jusqu’à convergence.

Comparaison :

    Dans un MDP, l'objectif explicite peut être d'amener l'agent 0 à atteindre la position de l'agent 1, ce qui peut inclure une logique de minimisation de distance. En revanche, avec BEST_RESPONSE, l'agent 0 agit uniquement en fonction de la politique de l'agent 1 et son propre gain, ce qui peut produire des comportements différents si les récompenses sont définies différemment.

### 3. Conditions pour lesquelles les deux politiques (MDP et BEST_RESPONSE) sont identiques :

Les deux politiques seront identiques si :

    Récompense alignée : Les fonctions de récompense dans le MDP et dans BEST_RESPONSE sont équivalentes et favorisent les mêmes actions.
    Objectif aligné : L'agent 0 a pour unique objectif d'atteindre la position de l'agent 1 dans les deux approches.
    Pas de contraintes conflictuelles : Aucune contrainte supplémentaire (par exemple, éviter certaines positions) ne limite le comportement dans l'une ou l'autre approche.

### 4. Modification du modèle pour empêcher les rencontres entre agents :

Pour garantir que les deux agents ne se rencontrent pas, on peut modifier le modèle de la manière suivante :

    Ajout d'une contrainte explicite dans les états : Un état où les deux agents occupent la même position est invalide ou associé à une récompense très négative.

    Récompense pénalisant la proximité : Ajouter une pénalité dans la fonction de récompense pour les états où la distance entre les agents est inférieure à une certaine valeur (par exemple, une distance Manhattan de 1).

    Ajout de contraintes dans l'espace d'action : Restreindre les actions possibles de chaque agent pour empêcher un mouvement conduisant à une rencontre.

    Nouveau benchmark : Relancer les algorithmes exhaustifs et JESP avec ce modèle modifié.

## Partie 3

- **src** : Dossier contenant les fichiers sources de l'algorithme Best Response avec comme base l'algorithme JESP version dynamique de MADP.
- **bin** : Dossier contenant le fichier binaire de l'algorithme Best Response.
- **Makefile** : Fichier pour générer le binaire avec la commande `make`
- **grid_large.dpomdp** : Fichier du problème GridSmall

### 1.

Lancer le script python pour générer le fichier `grid_large.dpomdp` : `python3 generate_grid_large.py`

### 2.
**JESP.txt** : Commande et trace d'exécution de l'algorithme JESP sur le problème précédemment généré.