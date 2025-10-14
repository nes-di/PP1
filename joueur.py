liste_joueur = [("nes", 6)] 

# Fonction pour ajouter un nouveau joueur ou charger une partie existante
def ajouter_ou_trouver_joueur(largeur=120):
    while True:
        pseudo = input("Entrez votre pseudo (ou 'm' pour menu principal): ".center(largeur))
        if pseudo == 'm':
            # Retourne au menu principal
            import os; os.system('cls' if os.name == 'nt' else 'clear')
            return 'menu'
        for joueur in liste_joueur:
            if joueur[0] == pseudo:
                # Si le pseudo existe déjà, propose de charger la partie
                print(f"Ce pseudo a déjà une partie existante ({joueur[1]} points.), voulez-vous charger cette partie? (o/n)".center(largeur))
                choix = input().lower()
                if choix == 'o':
                    print(f"Partie chargée pour le joueur: {pseudo}. Score: {joueur[1]} points. Tapez sur Entrée pour continuer.".center(largeur))
                    input()
                    return
                else:
                    print("Veuillez choisir un autre pseudo.".center(largeur))
                    print()
                    break
        else:
            # Ajoute un nouveau joueur si le pseudo n'existe pas
            liste_joueur.append((pseudo, 0))
            print(f"Nouveau joueur ajouté: {pseudo}. Score: 0 points.".center(largeur))
            print()
            return
