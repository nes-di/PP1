import json
import os
import threading
import time
from DataBaseLink.progression import enregistrer_partie
from Console.menu import afficher_menu

# Fonction pour charger les questions depuis le fichier JSON
# Retourne une liste de dictionnaires contenant les questions et réponses
def charger_questions():
    with open("Projet/Modèle/quizz.json", "r", encoding="utf-8") as f:
        return json.load(f)

# Fonction principale pour jouer une partie
# - pseudo : nom du joueur
def jouer_partie(pseudo):
    questions = charger_questions()  # Charge les questions depuis le fichier JSON
    scores = {pseudo: 0}  # Initialisation des scores pour le joueur

    for index, q in enumerate(questions, start=1):
        os.system('cls' if os.name == 'nt' else 'clear')  # Efface l'écran pour chaque nouvelle question

        # Affiche le numéro de la question et le nombre total de questions
        print(f"Question {index}/{len(questions)}".center(120))
        print("\n" + q["question"].center(120))  # Affiche la question
        for option in q["options"]:
            print(option.center(120))  # Affiche les options de réponse

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
            reponses = input("Entrez votre réponse : ".center(120)).lower()
            stop_event.set()  # Arrête le chrono si une réponse est donnée
        except Exception:
            pass

        timer_thread.join()  # Attend la fin du chrono

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

        # Affichage des scores actuels après chaque question
        print(f"Score actuel : {pseudo} - {scores[pseudo]} points".center(120))
        print("Appuyez sur une touche pour continuer...".center(120))
        input()

        # Enregistrement des scores dans la base de données après chaque question
        enregistrer_partie(pseudo, scores[pseudo])

    # Affichage du score final
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Félicitations ! Vous avez terminé le quiz.".center(120))
    print(f"Score final de {pseudo} : {scores[pseudo]} points".center(120))

    # Retour au menu principal
    print("Appuyez sur une touche pour retourner au menu principal...".center(120))
    input()
    afficher_menu(120)  # Relance le menu principal

    return scores