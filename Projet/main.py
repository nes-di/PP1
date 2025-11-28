from Console.menu import afficher_menu
from Logique.partie import jouer_partie
from DataBaseLink.database import creer_base, charger_partie

# Cette fonction de chargement est maintenant dans database.py

# Fonction principale pour gérer le menu et les interactions utilisateur
def main():
    largeur = 120
    creer_base()  # Création de la base SQLite
    afficher_menu(largeur)

    while True:
        choice = input("Choisissez une option (1-3 ou 'm' pour menu principal): ".center(largeur))
        if choice == 'm':
            afficher_menu(largeur)  # Réaffiche le menu principal
        elif choice == '1':
            # Démarrage d'une nouvelle partie
            pseudo = input("Entrez votre pseudo : ".center(largeur))
            scores = jouer_partie(pseudo)  # Lance une partie solo
            # L'enregistrement est maintenant géré automatiquement par le PartieManager
        elif choice == '2':
            # Charger une partie inachevée
            pseudo = input("Entrez votre pseudo pour charger une partie : ".center(largeur))
            partie = charger_partie(pseudo)
            if partie:
                theme, score, questions_repondues, ids_questions = partie
                print(f"Reprise de la partie pour {pseudo}. Score actuel : {score}, Questions répondues : {questions_repondues}/20".center(largeur))
                print(f"Thème : {theme}".center(largeur))
                input("Appuyez sur une touche pour continuer...".center(largeur))
                scores = jouer_partie(pseudo, score, ids_questions, theme)
            else:
                print("Aucune partie inachevée trouvée pour ce pseudo.".center(largeur))
                input("Appuyez sur une touche pour continuer...".center(largeur))
        elif choice == '3':
            # Quitte le programme
            print("Au revoir !".center(largeur))
            break
        else:
            print("Choix invalide. Réessayez.".center(largeur))

if __name__ == "__main__":
    main()