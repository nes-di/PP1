import json
import os

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

        reponses = input("Entrez vos réponses : ").lower()

        if len(reponses) > 0 and reponses[0].upper() == q["answer"]:
            scores[pseudo1] += 100
        if pseudo2 and len(reponses) > 1 and reponses[1].upper() == q["answer"]:
            scores[pseudo2] += 100

    return scores