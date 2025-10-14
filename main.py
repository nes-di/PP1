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
            mode = input("Mode de jeu : 1. Solo 2. 2 Joueurs : ".center(largeur))
            if mode == '1':
                pseudo = input("Entrez votre pseudo : ".center(largeur))
                scores = jouer_partie(pseudo)  # Lance une partie solo
                enregistrer_partie(pseudo, scores[pseudo])  # Enregistre le score
            elif mode == '2':
                pseudo1 = input("Pseudo du Joueur 1 : ".center(largeur))
                pseudo2 = input("Pseudo du Joueur 2 : ".center(largeur))
                scores = jouer_partie(pseudo1, pseudo2)  # Lance une partie à deux joueurs
                enregistrer_partie(pseudo1, scores[pseudo1])  # Enregistre le score du joueur 1
                enregistrer_partie(pseudo2, scores[pseudo2])  # Enregistre le score du joueur 2
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