import json
import os
import threading
import time
import random
from DataBaseLink.database import enregistrer_partie
from Console.menu import afficher_menu

# Charge toutes les questions du fichier JSON principal
def charger_questions():
    with open("Projet/Modèle/quizz.json", "r", encoding="utf-8") as f:
        return json.load(f)

# Charge les questions en fonction du thème choisi
def charger_questions_par_theme(theme):
    theme_files = {
        "Culture Générale": "Modèle/quizz_culture_générale.json",
        "Géographie": "Modèle/quizz_géographie.json",
        "Maths": "Modèle/quizz_maths.json",
        "Science": "Modèle/quizz_science.json",
        "Sports": "Modèle/quizz_sports.json"
    }

    if theme in theme_files:
        with open(theme_files[theme], "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict) and "quizz" in data:
                for item in data["quizz"]:
                    if "questions" in item:
                        return item["questions"]  # Retourne la liste des questions
                raise ValueError("Aucune clé 'questions' trouvée dans 'quizz'.")
            else:
                raise ValueError("Le fichier JSON ne contient pas de clé 'quizz' valide.")
    else:
        raise ValueError("Thème non valide")

# Fonction principale du jeu
def jouer_partie(pseudo, score_initial=0, ids_questions_repondues_initial=[], theme_sauvegarde=None):
    themes = ["Culture Générale", "Géographie", "Maths", "Science", "Sports"]
    theme_choisi = None
    
    # Vérifie si on reprend une partie existante
    if theme_sauvegarde:
        if theme_sauvegarde in themes:
            theme_choisi = theme_sauvegarde
            print(f"Reprise de la partie avec le thème : {theme_choisi}".center(120))
        else:
            print(f"Thème sauvegardé invalide ({theme_sauvegarde}). Veuillez choisir un nouveau thème :".center(120))
    
    # Demande le thème si pas de sauvegarde
    if not theme_choisi:
        print("Choisissez un thème :".center(120))
        for i, theme in enumerate(themes, start=1):
            print(f"{i}. {theme}".center(120))
        
        try:
            choix_str = input("Entrez le numéro de votre choix (1-5) : ".center(120)).strip()
            choix = int(choix_str)
            if 1 <= choix <= len(themes):
                theme_choisi = themes[choix - 1]
                print(f"Thème choisi : {theme_choisi}".center(120))
            else:
                print(f"Choix invalide ({choix}). Doit être entre 1 et {len(themes)}.".center(120))
                input("Appuyez sur une touche pour retourner au menu principal...".center(120))
                afficher_menu(120)
                return {pseudo: score_initial}
        except ValueError:
            print(f"Entrée invalide. Veuillez entrer un nombre entre 1 et {len(themes)}.".center(120))
            input("Appuyez sur une touche pour retourner au menu principal...".center(120))
            afficher_menu(120)
            return {pseudo: score_initial}
        
    # Charge les questions et retire celles déjà répondues
    questions = charger_questions_par_theme(theme_choisi)
    questions = [q for q in questions if q['id'] not in ids_questions_repondues_initial]
    
    questions_restantes = 20 - len(ids_questions_repondues_initial)
    
    if questions_restantes <= 0:
        print("Cette partie est déjà terminée !".center(120))
        input("Appuyez sur une touche pour retourner au menu principal...".center(120))
        afficher_menu(120)
        return {pseudo: score_initial}
    
    if len(questions) == 0:
        print("Aucune nouvelle question disponible pour ce thème.".center(120))
        input("Appuyez sur une touche pour retourner au menu principal...".center(120))
        afficher_menu(120)
        return {pseudo: score_initial}
        
    questions = random.sample(questions, min(questions_restantes, len(questions)))

    # Init des variables de jeu
    scores = {pseudo: score_initial}
    ids_questions_repondues = ids_questions_repondues_initial.copy()

    # Petit décompte avant de commencer
    print("Préparez-vous, le quiz commence dans :".center(120))
    for i in range(3, 0, -1):
        print(f"{i}...".center(120))
        time.sleep(1)

    # Boucle principale du quiz
    for index, q in enumerate(questions, start=len(ids_questions_repondues_initial) + 1):
        os.system('cls' if os.name == 'nt' else 'clear')

        # Affiche la question et les options
        print(f"Question {index}/20".center(120))
        print("\n" + q["question"].center(120))
        for key, value in q["options"].items():
            print(f"{key}: {value}".center(120))

        # Timer de 10 secondes pour répondre
        def countdown(stop_event):
            for i in range(10, 0, -1):
                if stop_event.is_set():
                    break
                print(f"Temps restant : {i} secondes".center(120), end="\r")
                time.sleep(1)
            if not stop_event.is_set():
                print("Temps écoulé ! Vous gagnez 0 points.".center(120))
                stop_event.set()

        stop_event = threading.Event()
        timer_thread = threading.Thread(target=countdown, args=(stop_event,))
        timer_thread.start()

        reponses = None
        try:
            reponses = input("Entrez votre réponse (ou 's' pour sauvegarder et quitter) : ".center(120)).lower()
            stop_event.set()
        except Exception:
            pass

        timer_thread.join()

        # Gestion de la sauvegarde
        if reponses == 's':
            enregistrer_partie(pseudo, theme_choisi, scores[pseudo], len(ids_questions_repondues), ids_questions_repondues)
            print("Partie sauvegardée. Vous pouvez la reprendre plus tard.".center(120))
            print("Retour au menu principal...".center(120))
            input("Appuyez sur une touche pour continuer...".center(120))
            afficher_menu(120)
            return scores

        # Vérifie si la réponse est correcte
        if not reponses and not stop_event.is_set():
            print("Temps écoulé, aucune réponse enregistrée. Vous gagnez 0 points.".center(120))
        else:
            reponse = reponses[0] if len(reponses) > 0 else None

            if reponse and reponse.upper() == q["answer"]:
                scores[pseudo] += 100
                print(f"Bonne réponse, {pseudo}! Vous gagnez 100 points.".center(120))
            else:
                print(f"Mauvaise réponse, {pseudo}. La bonne réponse était {q['answer']}!".center(120))
        
        ids_questions_repondues.append(q['id'])


        print(f"Score actuel : {pseudo} - {scores[pseudo]} points".center(120))
        print("Appuyez sur une touche pour continuer...".center(120))
        input()

    # Fin du quiz - affiche le score final
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Félicitations ! Vous avez terminé le quiz.".center(120))
    print(f"Score final de {pseudo} : {scores[pseudo]} points".center(120))
    
    # Sauvegarde automatique en fin de partie
    enregistrer_partie(pseudo, theme_choisi, scores[pseudo], len(ids_questions_repondues), ids_questions_repondues)

    print("Appuyez sur une touche pour retourner au menu principal...".center(120))
    input()
    afficher_menu(120)

    return scores