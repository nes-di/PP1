def afficher_menu(largeur=120):
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


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