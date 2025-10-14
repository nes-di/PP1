import json
import os
import threading
import time
from progression import enregistrer_partie, recuperer_historique

def charger_questions():
    with open("data/quizz.json", "r", encoding="utf-8") as f:
        return json.load(f)

def jouer_partie(pseudo1, pseudo2=None):
    questions = charger_questions()
    scores = {pseudo1: 0}
    if pseudo2:
        scores[pseudo2] = 0

    for q in questions:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n" + q["question"].center(80))
        for option in q["options"]:
            print(option.center(80))

        def countdown(stop_event):
            for i in range(10, 0, -1):
                if stop_event.is_set():
                    break
                print(f"Temps restant : {i} secondes".center(80), end="\r")
                time.sleep(1)
            if not stop_event.is_set():
                print("Temps écoulé ! Vous gagnez 0 points.".center(80))
                stop_event.set()  # Signale que le chrono est terminé

        stop_event = threading.Event()
        timer_thread = threading.Thread(target=countdown, args=(stop_event,))
        timer_thread.start()

        reponses = None
        try:
            reponses = input("Entrez vos réponses : ").lower()
            stop_event.set()  # Arrête le chrono si une réponse est donnée
        except Exception:
            pass

        timer_thread.join()

        if not reponses and not stop_event.is_set():
            print("Temps écoulé, aucune réponse enregistrée. Vous gagnez 0 points.".center(80))
        else:
            reponse1 = reponses[0] if len(reponses) > 0 else None
            reponse2 = reponses[1] if len(reponses) > 1 else None

            if reponse1 and reponse1.upper() == q["answer"]:
                scores[pseudo1] += 100
                print(f"Bonne réponse, {pseudo1}! Vous gagnez 100 points.".center(80))
            else:
                print(f"Mauvaise réponse, {pseudo1}. La bonne réponse était {q['answer']}!".center(80))

            if pseudo2 and reponse2 and reponse2.upper() == q["answer"]:
                scores[pseudo2] += 100
                print(f"Bonne réponse, {pseudo2}! Vous gagnez 100 points.".center(80))
            elif pseudo2:
                print(f"Mauvaise réponse, {pseudo2}. La bonne réponse était {q['answer']}!".center(80))

        print(f"Score actuel : {pseudo1} - {scores[pseudo1]} points".center(80))
        if pseudo2:
            print(f"Score actuel : {pseudo2} - {scores[pseudo2]} points".center(80))
        print("Appuyez sur une touche pour continuer...".center(80))
        input()

        # Enregistrer les scores dans la base de données après chaque question
        enregistrer_partie(pseudo1, scores[pseudo1])
        if pseudo2:
            enregistrer_partie(pseudo2, scores[pseudo2])

    return scores