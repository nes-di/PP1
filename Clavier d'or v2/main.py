import os
import time
from database import *

THEMES = ["Culture Générale", "Géographie", "Maths", "Science", "Sports"]

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Fonction qui affiche le menu principal du jeu avec le logo ASCII
def afficher_menu():
    clear_screen()
    print(" /$$       /$$$$$$$$        /$$$$$$  /$$        /$$$$$$  /$$    /$$ /$$$$$$ /$$$$$$$$ /$$$$$$$        /$$$$$$$  /$$ /$$$$$$  /$$$$$$$ ")
    print("| $$      | $$_____/       /$$__  $$| $$       /$$__  $$| $$   | $$|_  $$_/| $$_____/| $$__  $$      | $$__  $$| $//$$__  $$| $$__  $$")
    print("| $$      | $$            | $$  \\__/| $$      | $$  \\ $$| $$   | $$  | $$  | $$      | $$  \\ $$      | $$  \\ $$|_/| $$  \\ $$| $$  \\ $$")
    print("| $$      | $$$$$         | $$      | $$      | $$$$$$$$|  $$ / $$/  | $$  | $$$$$   | $$$$$$$/      | $$  | $$   | $$  | $$| $$$$$$$/")
    print("| $$      | $$__/         | $$      | $$      | $$__  $$ \\  $$ $$/   | $$  | $$__/   | $$__  $$      | $$  | $$   | $$  | $$| $$__  $$")
    print("| $$      | $$            | $$    $$| $$      | $$  | $$  \\  $$$/    | $$  | $$      | $$  \\ $$      | $$  | $$   | $$  | $$| $$  \\ $$")
    print("| $$$$$$$$| $$$$$$$$      |  $$$$$$/| $$$$$$$$| $$  | $$   \\  $/    /$$$$$$| $$$$$$$$| $$  | $$      | $$$$$$$/   |  $$$$$$/| $$  | $$")
    print("|________/|________/       \\______/ |________/|__/  |__/    \\_/    |______/|________/|__/  |__/      |_______/     \\______/ |__/  |__/")
    print("=" * 120)
    print()
    print("1. Nouvelle partie")
    print("2. Continuer une partie")
    print("3. Quitter")
    print()

# Fonction qui demande au joueur de choisir un thème parmi les 5 disponibles
def choisir_theme():
    print("\nChoisissez un thème :")
    for i, theme in enumerate(THEMES, 1):
        print(f"{i}. {theme}")

    while True:
        try:
            choix = int(input("\nVotre choix (1-5) : "))
            if 1 <= choix <= 5:
                return THEMES[choix - 1]
            print("Choix invalide !")
        except:
            print("Entrez un nombre !")

def poser_question(numero, total, question_data):
    clear_screen()   
    q_id, question, opt_a, opt_z, opt_e, opt_r, reponse, est_boss = question_data
    print(f"\n{'=' * 60}")
    print(f"Question {numero}/{total}".center(60))
    print(f"{'=' * 60}\n")
    print(question)
    print()
    print(f"A) {opt_a}")
    print(f"Z) {opt_z}")
    print(f"E) {opt_e}")
    print(f"R) {opt_r}")
    print()
    reponse_joueur = input("Votre réponse (A/Z/E/R ou S pour sauvegarder) : ").upper().strip()
    return reponse_joueur, reponse

def poser_question_boss(question_data):
    clear_screen()
    q_id, question, opt_a, opt_z, opt_e, opt_r, reponse, est_boss = question_data
    print("\n" + "🔥" * 30)
    print("QUESTION BOSS !!!".center(60))
    print("🔥" * 30 + "\n")
    print("⚠️  Cette question vaut 300 points ! ⚠️\n")
    print(question)
    print()
    print(f"A) {opt_a}")
    print(f"Z) {opt_z}")
    print(f"E) {opt_e}")
    print(f"R) {opt_r}")
    print()
    reponse_joueur = input("\nVotre réponse (A/Z/E/R) : ").upper().strip()
    return reponse_joueur, reponse

# Fonction principale qui gère une partie complète de quiz
def jouer_partie(pseudo, theme, continuer=False):
    questions = get_questions_par_theme(theme)
    if continuer:
        questions_repondues = get_questions_repondues(pseudo, theme)
        score = charger_partie(pseudo, theme)
    else:
        effacer_progression(pseudo, theme)
        questions_repondues = []
        score = 0
    questions_a_faire = [q for q in questions if q[0] not in questions_repondues]
    if not questions_a_faire:
        print("\n✅ Vous avez déjà répondu à toutes les questions de ce thème !")
        input("\nAppuyez sur Entrée...")
        return
    print(f"\n🎮 Début de la partie sur le thème : {theme}")
    print(f"📊 Questions restantes : {len(questions_a_faire)+1}")
    print(f"💰 Score actuel : {score} points\n")
    input("Appuyez sur Entrée pour commencer...")
    
    #Compte à rebours avant le début de la partie
    for i in range(3, 0, -1):
        clear_screen()
        print(f"\n\n{i}...".center(60))
        time.sleep(1)
    
    numero_question = len(questions_repondues) + 1
    for question_data in questions_a_faire:
        q_id = question_data[0]
        reponse_correcte = question_data[6]
        reponse_joueur, reponse = poser_question(numero_question, 20, question_data)
        
        # Sauvegarde de la partie
        if reponse_joueur == 'S':
            sauvegarder_partie(pseudo, theme, score)
            print("\n💾 Partie sauvegardée !")
            input("Appuyez sur Entrée...")
            return
        
        if reponse_joueur == reponse_correcte:
            score += 100
            print("\n✅ Bonne réponse ! +100 points")
        else:
            print(f"\n❌ Mauvaise réponse ! La bonne réponse était : {reponse_correcte}")
        print(f"💰 Score actuel : {score} points")
        enregistrer_reponse(pseudo, theme, q_id)
        input("\nAppuyez sur Entrée...")
        numero_question += 1
    
    question_boss = get_question_boss(theme)
    if question_boss and question_boss[0] not in questions_repondues:
        print("\n🎉 Dernière question ! Place au BOSS final ! 🎉")
        input("Appuyez sur Entrée pour affronter le boss...")
        reponse_joueur, reponse = poser_question_boss(question_boss)
        if reponse_joueur == 'S':
            sauvegarder_partie(pseudo, theme, score)
            print("\n💾 Partie sauvegardée !")
            input("Appuyez sur Entrée...")
            return
        reponse_correcte_boss = question_boss[6]
        if reponse_joueur == reponse_correcte_boss:
            score += 300
            print("\n🏆 VICTOIRE CONTRE LE BOSS ! +300 points !! 🏆")
        else:
            print(f"\n💀 Défaite... La bonne réponse était : {reponse_correcte_boss}")
        print(f"💰 Score actuel : {score} points")
        enregistrer_reponse(pseudo, theme, question_boss[0])
        input("\nAppuyez sur Entrée...")
    
    # Fin de la partie
    clear_screen()
    print("\n" + "=" * 60)
    print("FIN DE LA PARTIE".center(60))
    print("=" * 60)
    print(f"\n🎮 Joueur : {pseudo}")
    print(f"📚 Thème : {theme}")
    print(f"💰 Score final : {score} points")
    print("\n" + "=" * 60)
    sauvegarder_partie(pseudo, theme, score)
    input("\nAppuyez sur Entrée pour retourner au menu...")


def main():
    creer_base()
    
    # Boucle infinie qui affiche le menu tant que le joueur ne quitte pas
    while True:
        afficher_menu()
        choix = input("Votre choix : ")
        if choix == "1":
            clear_screen()
            pseudo = input("\nEntrez votre pseudo : ")
            theme = choisir_theme()
            jouer_partie(pseudo, theme, continuer=False)

        elif choix == "2":
            clear_screen()
            print("\n📜 Historique des 5 dernières parties sauvegardées :")
            print("=" * 80)
            
            # Récupère les 5 dernières parties depuis la base de données
            parties = get_dernieres_parties()
            if not parties:
                print("\nAucune partie sauvegardée.")
                input("\nAppuyez sur Entrée...")
                continue
            
            # Affiche chaque partie avec ses détails
            for i, partie in enumerate(parties, 1):
                pseudo_p, theme_p, score_p, date_p, questions_restantes = partie
                
                print(f"\n{i}. Pseudo: {pseudo_p}")
                print(f"   Thème: {theme_p}")
                print(f"   Score: {score_p} points")
                print(f"   Questions restantes: {questions_restantes}/20")
                print(f"   Sauvegardé le: {date_p}")
            print("\n" + "=" * 80)
            
            # Demande au joueur quel pseudo il veut charger
            pseudo = input("\nEntrez le pseudo à charger : ").strip()
            pseudos_disponibles = [p[0] for p in parties]
            if pseudo not in pseudos_disponibles:
                print("\n❌ Ce pseudo n'a pas de partie sauvegardée dans l'historique.")
                input("Appuyez sur Entrée...")
                continue
            
            theme = choisir_theme()
            jouer_partie(pseudo, theme, continuer=True)
        
        elif choix == "3":
            clear_screen()
            print("\n👋 Au revoir !\n")
            break
        
        else:
            print("\nChoix invalide !")
            time.sleep(1)

main()
