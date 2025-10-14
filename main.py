from modules.menu import afficher_menu
from modules.partie import jouer_partie
from progression import creer_base, enregistrer_partie, recuperer_historique

async def main():
    largeur = 120
    creer_base()
    afficher_menu(largeur)

    while True:
        choice = input("Choisissez une option (1-3 ou 'm' pour menu principal): ".center(largeur))
        if choice == 'm':
            afficher_menu(largeur)
        elif choice == '1':
            mode = input("Mode de jeu : 1. Solo 2. 2 Joueurs : ".center(largeur))
            if mode == '1':
                pseudo = input("Entrez votre pseudo : ".center(largeur))
                scores = jouer_partie(pseudo)
                enregistrer_partie(pseudo, scores[pseudo])
            elif mode == '2':
                pseudo1 = input("Pseudo du Joueur 1 : ".center(largeur))
                pseudo2 = input("Pseudo du Joueur 2 : ".center(largeur))
                scores = jouer_partie(pseudo1, pseudo2)
                enregistrer_partie(pseudo1, scores[pseudo1])
                enregistrer_partie(pseudo2, scores[pseudo2])
        elif choice == '2':
            historique = recuperer_historique()
            for pseudo, score, date in historique:
                print(f"{pseudo} - {score} points - {date}".center(largeur))
        elif choice == '3':
            print("Au revoir !".center(largeur))
            break
        else:
            print("Choix invalide. Réessayez.".center(largeur))

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())