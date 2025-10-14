import json
import os
import threading
import time
import random
from DataBaseLink.progression import enregistrer_partie
from Console.menu import afficher_menu

# Fonction pour charger les questions depuis le fichier JSON
# Retourne une liste de dictionnaires contenant les questions et réponses
def charger_questions():
    with open("Projet/Modèle/quizz.json", "r", encoding="utf-8") as f:
        return json.load(f)

def charger_questions_par_theme(theme):
    theme_files = {
        "Culture Générale": "Projet/Modèle/quizz_culture_générale.json",
        "Géographie": "Projet/Modèle/quizz_géographie.json",
        "Maths": "Projet/Modèle/quizz_maths.json",
        "Science": "Projet/Modèle/quizz_science.json",
        "Sports": "Projet/Modèle/quizz_sports.json"
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

# Fonction principale pour jouer une partie
# - pseudo : nom du joueur
def jouer_partie(pseudo, score_initial=0, ids_questions_repondues_initial=[]):
    print("Choisissez un thème :".center(120))
    themes = ["Culture Générale", "Géographie", "Maths", "Science", "Sports"]
    for i, theme in enumerate(themes, start=1):
        print(f"{i}. {theme}".center(120))

    choix = int(input("Entrez le numéro de votre choix : ".center(120)))
    if 1 <= choix <= len(themes):
        theme_choisi = themes[choix - 1]
        questions = charger_questions_par_theme(theme_choisi)  # Charge les questions du thème choisi
        questions = [q for q in questions if str(q['id']) not in ids_questions_repondues_initial]  # Filtrer les questions déjà répondues
        questions = random.sample(questions, min(20 - len(ids_questions_repondues_initial), len(questions)))  # Sélectionner les questions restantes
    else:
        print("Choix invalide. Retour au menu principal.".center(120))
        afficher_menu(120)
        return

    scores = {pseudo: score_initial}  # Initialisation des scores pour le joueur
    ids_questions_repondues = ids_questions_repondues_initial.copy()

    # Décompte avant de commencer la première question
    print("Préparez-vous, le quiz commence dans :".center(120))
    for i in range(3, 0, -1):
        print(f"{i}...".center(120))
        time.sleep(1)

    for index, q in enumerate(questions, start=len(ids_questions_repondues) + 1):
        os.system('cls' if os.name == 'nt' else 'clear')  # Efface l'écran pour chaque nouvelle question

        # Affiche le numéro de la question et le nombre total de questions
        print(f"Question {index}/20".center(120))
        print("\n" + q["question"].center(120))  # Affiche la question
        for key, value in q["options"].items():
            print(f"{key}: {value}".center(120))  # Affiche les options de réponse avec les lettres et les réponses

        # Fonction pour gérer le compte à rebours
        def countdown(stop_event):
            for i in range(10, 0, -1):
                if stop_event.is_set():
                    break  # Arrête le chrono si une réponse est donnée
                print(f"Temps restant : {i} secondes".center(120), end="\r")
                time.sleep(1)
            if not stop_event.is_set():
                print("Temps écoulé ! Vous gagnez 0 points.".center(120))
                stop_event.set()  # Signale que le chrono est terminé

        stop_event = threading.Event()  # Événement pour arrêter le chrono
        timer_thread = threading.Thread(target=countdown, args=(stop_event,))
        timer_thread.start()  # Démarre le chrono

        reponses = None
        try:
            reponses = input("Entrez votre réponse (ou 's' pour sauvegarder et quitter) : ".center(120)).lower()
            stop_event.set()  # Arrête le chrono si une réponse est donnée
        except Exception:
            pass

        timer_thread.join()  # Attend la fin du chrono

        if reponses == 's':
            # Sauvegarder la partie
            ids_questions_repondues.append(str(q['id']))
            enregistrer_partie(pseudo, scores[pseudo], len(ids_questions_repondues), ",".join(ids_questions_repondues))
            print("Partie sauvegardée. Vous pouvez la reprendre plus tard.".center(120))
            print("Retour au menu principal...".center(120))
            input("Appuyez sur une touche pour continuer...".center(120))
            afficher_menu(120)  # Retour au menu principal
            return scores  # Return scores when exiting early after saving the game

        if not reponses and not stop_event.is_set():
            # Si aucune réponse n'est donnée et que le chrono est écoulé
            print("Temps écoulé, aucune réponse enregistrée. Vous gagnez 0 points.".center(120))
        else:
            reponse = reponses[0] if len(reponses) > 0 else None  # Réponse du joueur

            # Vérification des réponses pour le joueur
            if reponse and reponse.upper() == q["answer"]:
                scores[pseudo] += 100  # Ajoute des points pour une bonne réponse
                print(f"Bonne réponse, {pseudo}! Vous gagnez 100 points.".center(120))
            else:
                print(f"Mauvaise réponse, {pseudo}. La bonne réponse était {q['answer']}!".center(120))

        # Ajouter l'ID de la question répondue
        ids_questions_repondues.append(str(q['id']))

        # Affichage des scores actuels après chaque question
        print(f"Score actuel : {pseudo} - {scores[pseudo]} points".center(120))
        print("Appuyez sur une touche pour continuer...".center(120))
        input()

        # Enregistrement des scores dans la base de données après chaque question
        enregistrer_partie(pseudo, scores[pseudo], len(ids_questions_repondues), ",".join(ids_questions_repondues))

    # Affichage du score final
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Félicitations ! Vous avez terminé le quiz.".center(120))
    print(f"Score final de {pseudo} : {scores[pseudo]} points".center(120))

    # Retour au menu principal
    print("Appuyez sur une touche pour retourner au menu principal...".center(120))
    input()
    afficher_menu(120)  # Relance le menu principal

    return scores