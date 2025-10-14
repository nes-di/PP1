liste_joueur = [("nes", 6)] 

# Fonction pour ajouter un nouveau joueur ou charger une partie existante
def ajouter_ou_trouver_joueur(largeur=120):
    while True:
        # Demande à l'utilisateur d'entrer un pseudo ou de retourner au menu principal
        pseudo = input("Entrez votre pseudo (ou 'm' pour menu principal): ".center(largeur))
        if pseudo == 'm':
            # Si l'utilisateur choisit de retourner au menu, on nettoie l'écran et on retourne 'menu'
            import os; os.system('cls' if os.name == 'nt' else 'clear')
            return 'menu'
        for joueur in liste_joueur:
            if joueur[0] == pseudo:
                # Si le pseudo existe déjà dans la liste des joueurs
                # On informe l'utilisateur et on lui demande s'il souhaite charger la partie existante
                print(f"Ce pseudo a déjà une partie existante ({joueur[1]} points.), voulez-vous charger cette partie? (o/n)".center(largeur))
                choix = input().lower()
                if choix == 'o':
                    # Si l'utilisateur choisit de charger la partie, on affiche un message de confirmation
                    print(f"Partie chargée pour le joueur: {pseudo}. Score: {joueur[1]} points. Tapez sur Entrée pour continuer.".center(largeur))
                    input()
                    return
                else:
                    # Si l'utilisateur ne souhaite pas charger la partie, on lui demande de choisir un autre pseudo
                    print("Veuillez choisir un autre pseudo.".center(largeur))
                    print()
                    break
        else:
            # Si le pseudo n'existe pas dans la liste, on ajoute le nouveau joueur avec un score de 0
            liste_joueur.append((pseudo, 0))
            print(f"Nouveau joueur ajouté: {pseudo}. Score: 0 points.".center(largeur))
            print()
            return
