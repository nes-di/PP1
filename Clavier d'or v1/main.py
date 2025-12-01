from Console.menu import afficher_menu
from Logique.partie import jouer_partie
from DataBaseLink.database import creer_base, charger_partie

def main():
    largeur = 120
    creer_base()
    afficher_menu(largeur)

    while True:
        choice = input("Choisissez une option (1-3 ou 'm' pour menu principal): ".center(largeur))
        if choice == 'm':
            afficher_menu(largeur)
        elif choice == '1':
            pseudo = input("Entrez votre pseudo : ".center(largeur))
            scores = jouer_partie(pseudo)
        elif choice == '2':
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
            print("Au revoir !".center(largeur))
            break
        else:
            print("Choix invalide. Réessayez.".center(largeur))
main()
#enlevé if __name__ == "__main__"