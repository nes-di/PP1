import time

def quiz_2_joueurs(pseudo1, pseudo2):
    questions = [
        {"question": "Quelle est la capitale de la France?", "options": ["A. Paris", "Z. Lyon", "E. Marseille", "R. Toulouse"], "answer": "A"},
        {"question": "Combien font 5 x 5?", "options": ["A. 10", "Z. 25", "E. 20", "R. 15"], "answer": "Z"},
        {"question": "Quelle est la couleur du ciel?", "options": ["A. Bleu", "Z. Vert", "E. Rouge", "R. Jaune"], "answer": "A"}
    ]

    scores = {pseudo1: 0, pseudo2: 0}

    for q in questions:
        print("\n" + q["question"])
        for option in q["options"]:
            print(option)

        start_time = time.time()
        reponse1 = input(f"{pseudo1}, entrez votre réponse (A/Z/E/R) : ").upper()
        time1 = time.time() - start_time

        start_time = time.time()
        reponse2 = input(f"{pseudo2}, entrez votre réponse (U/I/O/P) : ").upper()
        time2 = time.time() - start_time

        if reponse1 == q["answer"]:
            scores[pseudo1] += 100
        if reponse2 == q["answer"]:
            scores[pseudo2] += 100

        if reponse1 == q["answer"] and reponse2 == q["answer"]:
            if time1 < time2:
                scores[pseudo1] += 10
            elif time2 < time1:
                scores[pseudo2] += 10

    print("\nRésultats finaux :")
    print(f"{pseudo1} : {scores[pseudo1]} points")
    print(f"{pseudo2} : {scores[pseudo2]} points")

if __name__ == "__main__":
    quiz_2_joueurs("Joueur1", "Joueur2")