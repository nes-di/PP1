# Importe le module os pour gérer les commandes système (comme nettoyer l'écran)
import os
# Importe le module time pour gérer les pauses et les délais
import time
# Importe toutes les fonctions du fichier database.py (connexion base de données, requêtes, etc.)
from database import *

# Liste des thèmes disponibles pour le quiz (5 thèmes au total)
THEMES = ["Culture Générale", "Géographie", "Maths", "Science", "Sports"]

# Fonction pour effacer l'écran du terminal/console
def clear_screen():
    # os.system() exécute une commande système
    # 'cls' est la commande Windows pour nettoyer l'écran
    # 'clear' est la commande Linux/Mac pour nettoyer l'écran
    # os.name == 'nt' vérifie si on est sur Windows (nt = Windows NT)
    # Si Windows : exécute 'cls', sinon : exécute 'clear'
    os.system('cls' if os.name == 'nt' else 'clear')

# Fonction qui affiche le menu principal du jeu avec le logo ASCII
def afficher_menu():
    # Nettoie l'écran avant d'afficher le menu
    clear_screen()
    # Affiche le logo "LE CLAVIER D'OR" en ASCII art (8 lignes de caractères spéciaux)
    print(" /$$       /$$$$$$$$        /$$$$$$  /$$        /$$$$$$  /$$    /$$ /$$$$$$ /$$$$$$$$ /$$$$$$$        /$$$$$$$  /$$ /$$$$$$  /$$$$$$$ ")
    print("| $$      | $$_____/       /$$__  $$| $$       /$$__  $$| $$   | $$|_  $$_/| $$_____/| $$__  $$      | $$__  $$| $//$$__  $$| $$__  $$")
    print("| $$      | $$            | $$  \\__/| $$      | $$  \\ $$| $$   | $$  | $$  | $$      | $$  \\ $$      | $$  \\ $$|_/| $$  \\ $$| $$  \\ $$")
    print("| $$      | $$$$$         | $$      | $$      | $$$$$$$$|  $$ / $$/  | $$  | $$$$$   | $$$$$$$/      | $$  | $$   | $$  | $$| $$$$$$$/")
    print("| $$      | $$__/         | $$      | $$      | $$__  $$ \\  $$ $$/   | $$  | $$__/   | $$__  $$      | $$  | $$   | $$  | $$| $$__  $$")
    print("| $$      | $$            | $$    $$| $$      | $$  | $$  \\  $$$/    | $$  | $$      | $$  \\ $$      | $$  | $$   | $$  | $$| $$  \\ $$")
    print("| $$$$$$$$| $$$$$$$$      |  $$$$$$/| $$$$$$$$| $$  | $$   \\  $/    /$$$$$$| $$$$$$$$| $$  | $$      | $$$$$$$/   |  $$$$$$/| $$  | $$")
    print("|________/|________/       \\______/ |________/|__/  |__/    \\_/    |______/|________/|__/  |__/      |_______/     \\______/ |__/  |__/")
    # Affiche une ligne de séparation faite de 120 symboles "="
    print("=" * 120)
    # Affiche une ligne vide pour l'espacement
    print()
    # Affiche l'option 1 : commencer une nouvelle partie
    print("1. Nouvelle partie")
    # Affiche l'option 2 : reprendre une partie sauvegardée
    print("2. Continuer une partie")
    # Affiche l'option 3 : quitter le jeu
    print("3. Quitter")
    # Affiche une ligne vide pour l'espacement
    print()

# Fonction qui demande au joueur de choisir un thème parmi les 5 disponibles
def choisir_theme():
    # Affiche le titre de sélection
    print("\nChoisissez un thème :")
    # Parcourt la liste THEMES avec enumerate() qui donne (index, valeur)
    # enumerate(THEMES, 1) commence la numérotation à 1 au lieu de 0
    # i = numéro (1,2,3,4,5), theme = nom du thème
    for i, theme in enumerate(THEMES, 1):
        # Affiche chaque thème avec son numéro (ex: "1. Culture Générale")
        print(f"{i}. {theme}")
    
    # Boucle infinie qui tourne jusqu'à ce qu'on obtienne un choix valide
    while True:
        # try/except permet de gérer les erreurs (si l'utilisateur tape une lettre par exemple)
        try:
            # Demande à l'utilisateur de taper un nombre et le convertit en entier (int)
            choix = int(input("\nVotre choix (1-5) : "))
            # Vérifie si le choix est entre 1 et 5 (inclus)
            if 1 <= choix <= 5:
                # Retourne le thème correspondant (choix-1 car les listes commencent à 0)
                # Ex: choix=1 → THEMES[0] → "Culture Générale"
                return THEMES[choix - 1]
            # Si le nombre n'est pas entre 1 et 5, affiche un message d'erreur
            print("Choix invalide !")
        # Si int() échoue (l'utilisateur a tapé du texte), on arrive ici
        except:
            # Affiche un message demandant un nombre
            print("Entrez un nombre !")

# Fonction qui affiche une question normale et récupère la réponse du joueur
# Paramètres: numero = numéro de la question actuelle, total = nombre total de questions (20)
#             question_data = tuple contenant toutes les infos de la question
def poser_question(numero, total, question_data):
    # Nettoie l'écran pour afficher uniquement cette question
    clear_screen()
    
    # Décompose le tuple question_data en 8 variables distinctes
    # q_id = identifiant unique de la question dans la base
    # question = texte de la question
    # opt_a, opt_z, opt_e, opt_r = les 4 options de réponse (touches AZER du clavier)
    # reponse = la bonne réponse (A, Z, E ou R)
    # est_boss = 0 si question normale, 1 si question boss
    q_id, question, opt_a, opt_z, opt_e, opt_r, reponse, est_boss = question_data
    
    # ===== AFFICHAGE DE LA QUESTION =====
    # Affiche une ligne de 60 symboles "=" (ligne de séparation du haut)
    print(f"\n{'=' * 60}")
    # Affiche "Question X/20" centré sur 60 caractères
    # .center(60) ajoute des espaces pour centrer le texte
    print(f"Question {numero}/{total}".center(60))
    # Affiche une ligne de 60 symboles "=" (ligne de séparation du bas)
    print(f"{'=' * 60}\n")
    # Affiche le texte de la question
    print(question)
    # Affiche une ligne vide pour l'espacement
    print()
    # Affiche l'option A avec son texte
    print(f"A) {opt_a}")
    # Affiche l'option Z avec son texte
    print(f"Z) {opt_z}")
    # Affiche l'option E avec son texte
    print(f"E) {opt_e}")
    # Affiche l'option R avec son texte
    print(f"R) {opt_r}")
    # Affiche une ligne vide pour l'espacement
    print()
    
    # Demande la réponse au joueur
    # .upper() convertit en majuscules (a → A)
    # .strip() enlève les espaces au début et à la fin
    reponse_joueur = input("Votre réponse (A/Z/E/R ou S pour sauvegarder) : ").upper().strip()
    
    # Retourne 2 valeurs: la réponse du joueur ET la bonne réponse
    return reponse_joueur, reponse

# Fonction qui affiche la question BOSS (question 20, plus difficile, vaut 300 points)
# Paramètre: question_data = tuple contenant toutes les infos de la question boss
def poser_question_boss(question_data):
    # Nettoie l'écran pour afficher uniquement la question boss
    clear_screen()
    
    # Décompose le tuple question_data (même structure que les questions normales)
    q_id, question, opt_a, opt_z, opt_e, opt_r, reponse, est_boss = question_data
    
    # ===== AFFICHAGE SPÉCIAL POUR LE BOSS =====
    # Affiche une ligne vide puis 30 émojis de feu 🔥
    print("\n" + "🔥" * 30)
    # Affiche "QUESTION BOSS !!!" centré sur 60 caractères
    print("QUESTION BOSS !!!".center(60))
    # Affiche une ligne de 30 émojis de feu suivie d'une ligne vide
    print("🔥" * 30 + "\n")
    # Affiche un avertissement que cette question vaut 300 points (au lieu de 100)
    print("⚠️  Cette question vaut 300 points ! ⚠️\n")
    # Affiche le texte de la question boss
    print(question)
    # Affiche une ligne vide
    print()
    # Affiche les 4 options de réponse (touches AZER)
    print(f"A) {opt_a}")
    print(f"Z) {opt_z}")
    print(f"E) {opt_e}")
    print(f"R) {opt_r}")
    # Affiche une ligne vide
    print()
    
    # Demande la réponse au joueur (pas d'option sauvegarde pour le boss)
    # .upper() convertit en majuscules, .strip() enlève les espaces
    reponse_joueur = input("\nVotre réponse (A/Z/E/R) : ").upper().strip()
    
    # Retourne la réponse du joueur ET la bonne réponse
    return reponse_joueur, reponse

# Fonction principale qui gère une partie complète de quiz (19 questions + 1 boss)
# Paramètres: pseudo = nom du joueur, theme = thème choisi
#             continuer = True si on reprend une partie, False si nouvelle partie
def jouer_partie(pseudo, theme, continuer=False):
    # ===== CHARGEMENT DES DONNÉES =====
    # Récupère toutes les questions du thème choisi depuis la base de données
    # Cette fonction vient de database.py et retourne une liste de questions
    questions = get_questions_par_theme(theme)
    
    # Vérifie si c'est une partie qui continue ou une nouvelle partie
    if continuer:
        # PARTIE EXISTANTE: charge les questions déjà répondues par ce joueur
        # questions_repondues = liste des IDs de questions déjà faites
        questions_repondues = get_questions_repondues(pseudo, theme)
        # Charge le score sauvegardé de ce joueur pour ce thème
        score = charger_partie(pseudo, theme)
    else:
        # NOUVELLE PARTIE: efface toute l'ancienne progression de ce joueur sur ce thème
        # Supprime l'historique des réponses ET le score sauvegardé
        effacer_progression(pseudo, theme)
        # Initialise une liste vide (aucune question répondue)
        questions_repondues = []
        # Démarre avec un score de 0
        score = 0
    
    # ===== FILTRAGE DES QUESTIONS =====
    # Crée une nouvelle liste contenant SEULEMENT les questions non encore répondues
    # q[0] = l'ID de la question
    # "if q[0] not in questions_repondues" = garde la question si son ID n'est pas dans la liste des réponses
    questions_a_faire = [q for q in questions if q[0] not in questions_repondues]
    
    # Vérifie s'il reste des questions à faire
    if not questions_a_faire:
        # Si la liste est vide, toutes les questions ont été répondues
        print("\n✅ Vous avez déjà répondu à toutes les questions de ce thème !")
        # Attend que le joueur appuie sur Entrée
        input("\nAppuyez sur Entrée...")
        # Quitte la fonction (retour au menu)
        return
    
    # ===== AFFICHAGE INFORMATIONS DE DÉBUT =====
    # Affiche le thème choisi
    print(f"\n🎮 Début de la partie sur le thème : {theme}")
    # Affiche combien de questions restent (+1 pour compter le boss)
    # len(questions_a_faire) = nombre de questions dans la liste
    print(f"📊 Questions restantes : {len(questions_a_faire)+1}")
    # Affiche le score actuel (0 si nouvelle partie, score sauvegardé si partie continue)
    print(f"💰 Score actuel : {score} points\n")
    # Attend que le joueur appuie sur Entrée pour commencer
    input("Appuyez sur Entrée pour commencer...")
    
    # ===== COMPTE À REBOURS 3, 2, 1 =====
    # Boucle qui compte de 3 à 1 (range(3, 0, -1) = [3, 2, 1])
    for i in range(3, 0, -1):
        # Nettoie l'écran
        clear_screen()
        # Affiche le chiffre centré (ex: "3...")
        print(f"\n\n{i}...".center(60))
        # Pause de 1 seconde avant d'afficher le chiffre suivant
        time.sleep(1)
    
    # ===== BOUCLE DES QUESTIONS NORMALES (1 à 19) =====
    # Calcule le numéro de la question actuelle
    # Si 5 questions déjà répondues → commence à la question 6
    numero_question = len(questions_repondues) + 1
    
    # Parcourt chaque question de la liste des questions à faire
    # question_data = tuple avec toutes les infos d'une question
    for question_data in questions_a_faire:
        # Récupère l'ID de la question (premier élément du tuple, index 0)
        q_id = question_data[0]
        # Récupère la bonne réponse (7ème élément du tuple, index 6)
        reponse_correcte = question_data[6]
        
        # ===== AFFICHAGE DE LA QUESTION =====
        # Appelle la fonction qui affiche la question et attend la réponse
        # Retourne 2 valeurs: ce que le joueur a tapé, et la bonne réponse
        reponse_joueur, reponse = poser_question(numero_question, 20, question_data)
        
        # ===== GESTION DE LA SAUVEGARDE =====
        # Vérifie si le joueur a tapé 'S' pour sauvegarder
        if reponse_joueur == 'S':
            # Sauvegarde le score actuel dans la base de données
            sauvegarder_partie(pseudo, theme, score)
            # Affiche un message de confirmation
            print("\n💾 Partie sauvegardée !")
            # Attend que le joueur appuie sur Entrée
            input("Appuyez sur Entrée...")
            # Quitte la fonction (retour au menu)
            return
        
        # ===== VÉRIFICATION DE LA RÉPONSE =====
        # Compare la réponse du joueur avec la bonne réponse
        if reponse_joueur == reponse_correcte:
            # BONNE RÉPONSE: ajoute 100 points au score
            score += 100
            # Affiche un message de succès
            print("\n✅ Bonne réponse ! +100 points")
        else:
            # MAUVAISE RÉPONSE: n'ajoute rien au score
            # Affiche la bonne réponse pour que le joueur apprenne
            print(f"\n❌ Mauvaise réponse ! La bonne réponse était : {reponse_correcte}")
        
        # Affiche le score mis à jour
        print(f"💰 Score actuel : {score} points")
        
        # ===== ENREGISTREMENT DE LA PROGRESSION =====
        # Enregistre dans la base que le joueur a répondu à cette question
        # Permet de ne pas la reposer si la partie est rechargée
        enregistrer_reponse(pseudo, theme, q_id)
        
        # Attend que le joueur appuie sur Entrée pour continuer
        input("\nAppuyez sur Entrée...")
        # Incrémente le numéro de question pour la prochaine (1→2, 2→3, etc.)
        numero_question += 1
    
    # ===== QUESTION BOSS (QUESTION 20) =====
    # Récupère la question boss du thème depuis la base de données
    # get_question_boss() retourne la question avec est_boss=1
    question_boss = get_question_boss(theme)
    
    # Vérifie que la question boss existe ET qu'elle n'a pas déjà été répondue
    # question_boss = None si pas de boss trouvé, sinon = tuple avec les données
    # question_boss[0] = ID de la question boss
    if question_boss and question_boss[0] not in questions_repondues:
        # Affiche un message d'annonce du boss
        print("\n🎉 Dernière question ! Place au BOSS final ! 🎉")
        # Attend que le joueur appuie sur Entrée
        input("Appuyez sur Entrée pour affronter le boss...")
        
        # ===== AFFICHAGE DE LA QUESTION BOSS =====
        # Appelle la fonction spéciale pour afficher le boss
        reponse_joueur, reponse = poser_question_boss(question_boss)
        
        # ===== GESTION SAUVEGARDE (optionnelle, peu probable à ce stade) =====
        # Vérifie si le joueur veut sauvegarder avant de répondre au boss
        if reponse_joueur == 'S':
            # Sauvegarde le score dans la base
            sauvegarder_partie(pseudo, theme, score)
            print("\n💾 Partie sauvegardée !")
            input("Appuyez sur Entrée...")
            # Quitte la fonction
            return
        
        # ===== VÉRIFICATION RÉPONSE BOSS =====
        # Récupère la bonne réponse du boss (index 6)
        reponse_correcte_boss = question_boss[6]
        # Compare la réponse du joueur avec la bonne réponse
        if reponse_joueur == reponse_correcte_boss:
            # BONNE RÉPONSE: ajoute 300 points (au lieu de 100)
            score += 300
            # Affiche un message de victoire épique
            print("\n🏆 VICTOIRE CONTRE LE BOSS ! +300 points !! 🏆")
        else:
            # MAUVAISE RÉPONSE: affiche la bonne réponse
            print(f"\n💀 Défaite... La bonne réponse était : {reponse_correcte_boss}")
        
        # Affiche le score mis à jour après le boss
        print(f"💰 Score actuel : {score} points")
        
        # ===== ENREGISTREMENT DU BOSS =====
        # Enregistre dans la base que le boss a été répondu
        enregistrer_reponse(pseudo, theme, question_boss[0])
        
        # Attend que le joueur appuie sur Entrée
        input("\nAppuyez sur Entrée...")
    
    # ===== FIN DE PARTIE =====
    # Nettoie l'écran pour afficher l'écran de fin
    clear_screen()
    # Affiche une ligne vide puis une ligne de séparation
    print("\n" + "=" * 60)
    # Affiche "FIN DE LA PARTIE" centré
    print("FIN DE LA PARTIE".center(60))
    # Affiche une ligne de séparation
    print("=" * 60)
    # Affiche le nom du joueur
    print(f"\n🎮 Joueur : {pseudo}")
    # Affiche le thème joué
    print(f"📚 Thème : {theme}")
    # Affiche le score final
    print(f"💰 Score final : {score} points")
    # Affiche une ligne de séparation
    print("\n" + "=" * 60)
    
    # ===== SAUVEGARDE FINALE =====
    # Sauvegarde le score final dans la base de données
    sauvegarder_partie(pseudo, theme, score)
    
    # Attend que le joueur appuie sur Entrée pour retourner au menu
    input("\nAppuyez sur Entrée pour retourner au menu...")

# Fonction principale du programme - point d'entrée de l'application
def main():
    # ===== INITIALISATION =====
    # Crée la base de données et les tables si elles n'existent pas
    # Initialise aussi les 105 questions (5 thèmes × 21 questions) si la base est vide
    creer_base()
    
    # ===== BOUCLE PRINCIPALE DU MENU =====
    # Boucle infinie qui affiche le menu tant que le joueur ne quitte pas
    while True:
        # Affiche le menu avec le logo et les 3 options
        afficher_menu()
        # Demande au joueur de choisir une option (1, 2 ou 3)
        choix = input("Votre choix : ")
        
        # ===== OPTION 1: NOUVELLE PARTIE =====
        if choix == "1":
            # Nettoie l'écran
            clear_screen()
            # Demande le pseudo du joueur
            pseudo = input("\nEntrez votre pseudo : ")
            # Demande au joueur de choisir un thème (affiche la liste des 5 thèmes)
            theme = choisir_theme()
            # Lance une partie complète avec continuer=False (nouvelle partie)
            jouer_partie(pseudo, theme, continuer=False)
        
        # ===== OPTION 2: CONTINUER UNE PARTIE =====
        elif choix == "2":
            # Nettoie l'écran
            clear_screen()
            # Affiche le titre de l'historique
            print("\n📜 Historique des 5 dernières parties sauvegardées :")
            # Affiche une ligne de séparation de 80 caractères
            print("=" * 80)
            
            # ===== RÉCUPÉRATION DES PARTIES SAUVEGARDÉES =====
            # Récupère les 5 dernières parties depuis la base de données
            # parties = liste de tuples (pseudo, theme, score, date, questions_restantes)
            parties = get_dernieres_parties()
            
            # Vérifie si la liste est vide (aucune partie sauvegardée)
            if not parties:
                # Affiche un message
                print("\nAucune partie sauvegardée.")
                # Attend que le joueur appuie sur Entrée
                input("\nAppuyez sur Entrée...")
                # Continue la boucle (retourne au menu)
                continue
            
            # ===== AFFICHAGE DE L'HISTORIQUE =====
            # Parcourt chaque partie avec enumerate pour avoir un numéro (1, 2, 3, 4, 5)
            # enumerate(parties, 1) commence à 1 au lieu de 0
            for i, partie in enumerate(parties, 1):
                # Décompose le tuple partie en 5 variables
                pseudo_p, theme_p, score_p, date_p, questions_restantes = partie
                
                # Affiche le numéro de la partie
                print(f"\n{i}. Pseudo: {pseudo_p}")
                # Affiche le thème de cette partie (indenté avec 3 espaces)
                print(f"   Thème: {theme_p}")
                # Affiche le score de cette partie
                print(f"   Score: {score_p} points")
                # Affiche combien de questions restent sur 20
                print(f"   Questions restantes: {questions_restantes}/20")
                # Affiche la date de sauvegarde
                print(f"   Sauvegardé le: {date_p}")
            
            # Affiche une ligne de séparation
            print("\n" + "=" * 80)
            
            # ===== SÉLECTION DU JOUEUR =====
            # Demande au joueur quel pseudo il veut charger
            # .strip() enlève les espaces au début et à la fin
            pseudo = input("\nEntrez le pseudo à charger : ").strip()
            
            # ===== VÉRIFICATION DU PSEUDO =====
            # Crée une liste contenant uniquement les pseudos des parties sauvegardées
            # p[0] = premier élément du tuple = le pseudo
            pseudos_disponibles = [p[0] for p in parties]
            # Vérifie si le pseudo entré n'est pas dans la liste
            if pseudo not in pseudos_disponibles:
                # Affiche un message d'erreur
                print("\n❌ Ce pseudo n'a pas de partie sauvegardée dans l'historique.")
                # Attend que le joueur appuie sur Entrée
                input("Appuyez sur Entrée...")
                # Continue la boucle (retourne au menu)
                continue
            
            # ===== LANCEMENT DE LA PARTIE =====
            # Demande au joueur de choisir le thème
            theme = choisir_theme()
            # Lance la partie avec continuer=True (charge la progression sauvegardée)
            jouer_partie(pseudo, theme, continuer=True)
        
        # ===== OPTION 3: QUITTER =====
        elif choix == "3":
            # Nettoie l'écran
            clear_screen()
            # Affiche un message d'au revoir
            print("\n👋 Au revoir !\n")
            # Sort de la boucle while (arrête le programme)
            break
        
        # ===== CHOIX INVALIDE =====
        else:
            # Si le joueur tape autre chose que 1, 2 ou 3
            print("\nChoix invalide !")
            # Pause de 1 seconde pour que le joueur voie le message
            time.sleep(1)

# Point d'entrée du programme Python
# Ce bloc s'exécute UNIQUEMENT si on lance ce fichier directement
# (pas si on l'importe comme module dans un autre fichier)
if __name__ == "__main__":
    # Appelle la fonction main() pour démarrer le programme
    main()
