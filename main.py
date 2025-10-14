from modules.menu import afficher_menu
from modules.partie import jouer_partie
from progression import creer_base, enregistrer_partie, recuperer_historique

# Fonction principale pour gérer le menu et les interactions utilisateur
async def main():
    largeur = 120  # Largeur pour centrer les affichages
    creer_base()  # Création de la base de données si elle n'existe pas
    afficher_menu(largeur)  # Affiche le menu principal

    while True:
        choice = input("Choisissez une option (1-3 ou 'm' pour menu principal): ".center(largeur))
        if choice == 'm':
            afficher_menu(largeur)  # Réaffiche le menu principal
        elif choice == '1':
            # Démarrage d'une nouvelle partie
            pseudo = input("Entrez votre pseudo : ".center(largeur))
            scores = jouer_partie(pseudo)  # Lance une partie solo
            enregistrer_partie(pseudo, scores[pseudo])  # Enregistre le score
        elif choice == '2':
            # Affichage de l'historique des parties
            historique = recuperer_historique()
            for pseudo, score, date in historique:
                print(f"{pseudo} - {score} points - {date}".center(largeur))
        elif choice == '3':
            # Quitte le programme
            print("Au revoir !".center(largeur))
            break
        else:
            print("Choix invalide. Réessayez.".center(largeur))

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())