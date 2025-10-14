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
async def main():
    largeur = 120
    afficher_menu(largeur)
    from joueur import ajouter_ou_trouver_joueur, liste_joueur
    from quizz import quiz_2_joueurs, quiz_solo
    while True:
        choice = input("Choisissez une option (1-3 ou 'm' pour menu principal): ".center(largeur))
        if choice == 'm':
            return await main()
        elif choice == '1':
            print("\nMode de jeu :".center(largeur))
            print("1. Solo".center(largeur))
            print("2. 2 Joueurs".center(largeur))
            mode = input("Choisissez un mode (1-2 ou 'm' pour menu principal): ".center(largeur))
            if mode == 'm':
                return await main()
            elif mode == '1':
                res = ajouter_ou_trouver_joueur(largeur)
                if res == 'menu':
                    return await main()
                print()
                quiz_solo(res)
                break
            elif mode == '2':
                print("\nEntrez les pseudos des joueurs :".center(largeur))
                pseudo1 = input("Pseudo du Joueur 1 : ".center(largeur))
                pseudo2 = input("Pseudo du Joueur 2 : ".center(largeur))
                print(f"Bienvenue {pseudo1} et {pseudo2} ! Préparez-vous à jouer.".center(largeur))
                print()
                await quiz_2_joueurs(pseudo1, pseudo2)
                break
            else:
                print("Choix invalide. Réessayez.".center(largeur))
                print()
        elif choice == '2':
            if not liste_joueur:
                print("Aucune partie enregistrée.".center(largeur))
                return await main()
            for pseudo, score in liste_joueur:
                print(f"{pseudo}, Score: {score} points".center(largeur))
                print()
            while True:
                pseudo = input("Quelle partie voulez-vous charger? (entrez le pseudo ou 'm' pour menu principal): ".center(largeur))
                if pseudo == 'm':
                    return await main()
                for joueur in liste_joueur:
                    if joueur[0] == pseudo:
                        print(f"Partie chargée pour le joueur: {pseudo}. Score: {joueur[1]} points. Tapez sur Entrée pour continuer.".center(largeur))
                        input()
                        print()
                        return
                print("Aucun joueur trouvé avec ce pseudo. Réessayez.".center(largeur))
                print()
            return await main()
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
    import asyncio
    asyncio.run(main())