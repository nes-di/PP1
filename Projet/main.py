from Console.menu import afficher_menu
from Logique.partie import jouer_partie
from DataBaseLink.progression import creer_base, enregistrer_partie, recuperer_historique
import sqlite3

# Fonction pour charger une partie inachevée
def charger_partie(pseudo):
    conn = sqlite3.connect("Projet/data/progression.db")
    cursor = conn.cursor()

    # Récupérer les informations de la dernière partie inachevée
    cursor.execute('''
    SELECT score, questions_repondues, ids_questions_repondues
    FROM parties
    JOIN joueurs ON parties.joueur_id = joueurs.id
    WHERE joueurs.pseudo = ?
    ''', (pseudo,))

    partie = cursor.fetchone()
    conn.close()

    if partie:
        score, questions_repondues, ids_questions_repondues = partie
        ids_questions_repondues = ids_questions_repondues.split(",") if ids_questions_repondues else []
        return score, int(questions_repondues), ids_questions_repondues
    else:
        return None

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
            # Charger une partie inachevée
            pseudo = input("Entrez votre pseudo pour charger une partie : ".center(largeur))
            partie = charger_partie(pseudo)
            if partie:
                score, questions_repondues, ids_questions_repondues = partie
                print(f"Reprise de la partie pour {pseudo}. Score actuel : {score}, Questions répondues : {questions_repondues}".center(largeur))
                scores = jouer_partie(pseudo, score, ids_questions_repondues)  # Reprendre la partie
                enregistrer_partie(pseudo, scores[pseudo])  # Mettre à jour le score
            else:
                print("Aucune partie inachevée trouvée pour ce pseudo.".center(largeur))
        elif choice == '3':
            # Quitte le programme
            print("Au revoir !".center(largeur))
            break
        else:
            print("Choix invalide. Réessayez.".center(largeur))

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())