def afficher_menu(largeur=120):
    import os; os.system('cls' if os.name == 'nt' else 'clear')
    print(" /$$       /$$$$$$$$        /$$$$$$  /$$        /$$$$$$  /$$    /$$ /$$$$$$ /$$$$$$$$ /$$$$$$$        /$$$$$$$  /$$ /$$$$$$  /$$$$$$$ ".center(largeur))
    print("| $$      | $$_____/       /$$__  $$| $$       /$$__  $$| $$   | $$|_  $$_/| $$_____/| $$__  $$      | $$__  $$| $//$$__  $$| $$__  $$".center(largeur))
    print("| $$      | $$            | $$  \\__/| $$      | $$  \\ $$| $$   | $$  | $$  | $$      | $$  \\ $$      | $$  \\ $$|_/| $$  \\ $$| $$  \\ $$".center(largeur))
    print("| $$      | $$$$$         | $$      | $$      | $$$$$$$$|  $$ / $$/  | $$  | $$$$$   | $$$$$$$/      | $$  | $$   | $$  | $$| $$$$$$$/".center(largeur))
    print("| $$      | $$__/         | $$      | $$      | $$__  $$ \\  $$ $$/   | $$  | $$__/   | $$__  $$      | $$  | $$   | $$  | $$| $$__  $$".center(largeur))
    print("| $$      | $$            | $$    $$| $$      | $$  | $$  \\  $$$/    | $$  | $$      | $$  \\ $$      | $$  | $$   | $$  | $$| $$  \\ $$".center(largeur))
    print("| $$$$$$$$| $$$$$$$$      |  $$$$$$/| $$$$$$$$| $$  | $$   \\  $/    /$$$$$$| $$$$$$$$| $$  | $$      | $$$$$$$/   |  $$$$$$/| $$  | $$".center(largeur))
    print("|________/|________/       \\______/ |________/|__/  |__/    \\_/    |______/|________/|__/  |__/      |_______/     \\______/ |__/  |__/".center(largeur))
    print("="*largeur)
    print("1. Nouvelle partie".center(largeur))
    print("2. Historique des parties ou charger une partie".center(largeur))
    print("3. Quitter".center(largeur))
def main():
    largeur = 120
    afficher_menu(largeur)
    from joueur import ajouter_ou_trouver_joueur, liste_joueur
    while True:
        choice = input("Choisissez une option (1-3 ou 'm' pour menu principal): ".center(largeur))
        if choice == 'm':
            return main()
        elif choice == '1':
            print()
            res = ajouter_ou_trouver_joueur(largeur)
            if res == 'menu':
                return main()
            print()
            # importer quizz ici
            break
        elif choice == '2':
            if not liste_joueur:
                print("Aucune partie enregistrée.".center(largeur))
                return main()
            for pseudo, score in liste_joueur:
                print(f"{pseudo}, Score: {score} points".center(largeur))
                print()
            while True:
                pseudo = input("Quelle partie voulez-vous charger? (entrez le pseudo ou 'm' pour menu principal): ".center(largeur))
                if pseudo == 'm':
                    return main()
                for joueur in liste_joueur:
                    if joueur[0] == pseudo:
                        print(f"Partie chargée pour le joueur: {pseudo}. Score: {joueur[1]} points. Tapez sur Entrée pour continuer.".center(largeur))
                        input()
                        print()
                        # importer quizz ici
                        return
                print("Aucun joueur trouvé avec ce pseudo. Réessayez.".center(largeur))
                print()
            return main()
        elif choice == '3':
            print()
            print("Au revoir !".center(largeur))
            print()
            return
        else:
            print()
            print("Choix invalide. Réessayez.".center(largeur))
            print()
if __name__ == "__main__":
    main()