import json
import os
import threading
import time
from progression import enregistrer_partie, recuperer_historique

# Fonction pour charger les questions depuis le fichier JSON
def charger_questions():
    with open("data/quizz.json", "r", encoding="utf-8") as f:
        return json.load(f)

# Fonction principale pour jouer une partie
# - pseudo1 : nom du joueur 1
# - pseudo2 : nom du joueur 2 (optionnel, pour le mode 2 joueurs)
def jouer_partie(pseudo1, pseudo2=None):
    questions = charger_questions()
    scores = {pseudo1: 0}  # Initialisation des scores
    if pseudo2:
        scores[pseudo2] = 0

    for q in questions:
        os.system('cls' if os.name == 'nt' else 'clear')  # Efface l'écran pour chaque nouvelle question
        print("\n" + q["question"].center(120))  # Affiche la question
        for option in q["options"]:
            print(option.center(120))  # Affiche les options de réponse

        # Fonction pour gérer le compte à rebours
        def countdown(stop_event):
            for i in range(10, 0, -1):
                if stop_event.is_set():
                    break
                print(f"Temps restant : {i} secondes".center(120), end="\r")
                time.sleep(1)
            if not stop_event.is_set():
                print("Temps écoulé ! Vous gagnez 0 points.".center(120))
                stop_event.set()  # Signale que le chrono est terminé

        stop_event = threading.Event()
        timer_thread = threading.Thread(target=countdown, args=(stop_event,))
        timer_thread.start()

        reponses = None
        try:
            reponses = input("Entrez vos réponses : ".center(120)).lower()
            stop_event.set()  # Arrête le chrono si une réponse est donnée
        except Exception:
            pass

        timer_thread.join()

        if not reponses and not stop_event.is_set():
            print("Temps écoulé, aucune réponse enregistrée. Vous gagnez 0 points.".center(120))
        else:
            reponse1 = reponses[0] if len(reponses) > 0 else None
            reponse2 = reponses[1] if len(reponses) > 1 else None

            # Vérification des réponses pour le joueur 1
            if reponse1 and reponse1.upper() == q["answer"]:
                scores[pseudo1] += 100
                print(f"Bonne réponse, {pseudo1}! Vous gagnez 100 points.".center(120))
            else:
                print(f"Mauvaise réponse, {pseudo1}. La bonne réponse était {q['answer']}!".center(120))

            # Vérification des réponses pour le joueur 2 (si présent)
            if pseudo2 and reponse2 and reponse2.upper() == q["answer"]:
                scores[pseudo2] += 100
                print(f"Bonne réponse, {pseudo2}! Vous gagnez 100 points.".center(120))
            elif pseudo2:
                print(f"Mauvaise réponse, {pseudo2}. La bonne réponse était {q['answer']}!".center(120))

        # Affichage des scores actuels
        print(f"Score actuel : {pseudo1} - {scores[pseudo1]} points".center(120))
        if pseudo2:
            print(f"Score actuel : {pseudo2} - {scores[pseudo2]} points".center(120))
        print("Appuyez sur une touche pour continuer...".center(120))
        input()

        # Enregistrement des scores dans la base de données après chaque question
        enregistrer_partie(pseudo1, scores[pseudo1])
        if pseudo2:
            enregistrer_partie(pseudo2, scores[pseudo2])

    return scores