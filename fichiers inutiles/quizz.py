import os
import time
import threading
import asyncio

async def fake_download():
    for i in range(3):
        print(f"Chargement{'.' * (i + 1)}".center(80), end="\r")
        await asyncio.sleep(0.5)
    print(" " * 80, end="\r")  # Efface la ligne après le chargement

async def quiz_2_joueurs(pseudo1, pseudo2):
    questions = [
        {"question": "Quelle est la capitale de la France?", "options": ["A. Paris", "Z. Lyon", "E. Marseille", "R. Toulouse"], "answer": "A"},
        {"question": "Combien font 5 x 5?", "options": ["A. 10", "Z. 25", "E. 20", "R. 15"], "answer": "Z"},
        {"question": "Quelle est la couleur du ciel?", "options": ["A. Bleu", "Z. Vert", "E. Rouge", "R. Jaune"], "answer": "A"},
        {"question": "Qui a peint la Joconde?", "options": ["A. Léonard de Vinci", "Z. Picasso", "E. Van Gogh", "R. Monet"], "answer": "A"},
        {"question": "Quelle est la capitale de l'Italie?", "options": ["A. Rome", "Z. Milan", "E. Naples", "R. Florence"], "answer": "A"},
        {"question": "Combien y a-t-il de continents?", "options": ["A. 5", "Z. 6", "E. 7", "R. 8"], "answer": "E"},
        {"question": "Quelle est la planète la plus proche du Soleil?", "options": ["A. Mercure", "Z. Vénus", "E. Terre", "R. Mars"], "answer": "A"},
        {"question": "Quel est le plus grand océan?", "options": ["A. Atlantique", "Z. Pacifique", "E. Indien", "R. Arctique"], "answer": "Z"},
        {"question": "Qui a écrit 'Les Misérables'?", "options": ["A. Victor Hugo", "Z. Émile Zola", "E. Balzac", "R. Flaubert"], "answer": "A"},
        {"question": "Quelle est la langue la plus parlée au monde?", "options": ["A. Anglais", "Z. Espagnol", "E. Mandarin", "R. Hindi"], "answer": "E"},
        {"question": "Quel est le symbole chimique de l'eau?", "options": ["A. H2O", "Z. O2", "E. CO2", "R. H2"], "answer": "A"},
        {"question": "Combien y a-t-il d'heures dans une journée?", "options": ["A. 12", "Z. 24", "E. 36", "R. 48"], "answer": "Z"},
        {"question": "Quel est le plus grand désert du monde?", "options": ["A. Sahara", "Z. Gobi", "E. Antarctique", "R. Kalahari"], "answer": "E"},
        {"question": "Qui a découvert l'Amérique?", "options": ["A. Christophe Colomb", "Z. Vasco de Gama", "E. Magellan", "R. Amerigo Vespucci"], "answer": "A"},
        {"question": "Quelle est la capitale de l'Allemagne?", "options": ["A. Berlin", "Z. Munich", "E. Hambourg", "R. Francfort"], "answer": "A"},
        {"question": "Combien y a-t-il de jours dans une année bissextile?", "options": ["A. 364", "Z. 365", "E. 366", "R. 367"], "answer": "E"},
        {"question": "Quel est l'élément chimique le plus léger?", "options": ["A. Hydrogène", "Z. Hélium", "E. Lithium", "R. Carbone"], "answer": "A"},
        {"question": "Quel est le pays le plus peuplé du monde?", "options": ["A. Inde", "Z. Chine", "E. États-Unis", "R. Indonésie"], "answer": "Z"},
        {"question": "Quelle est la monnaie utilisée au Japon?", "options": ["A. Yen", "Z. Dollar", "E. Euro", "R. Won"], "answer": "A"},
        {"question": "Quel est le plus haut sommet du monde?", "options": ["A. Mont Everest", "Z. K2", "E. Kangchenjunga", "R. Lhotse"], "answer": "A"}
    ]

    scores = {pseudo1: 0, pseudo2: 0}

    for q in questions:
        await fake_download()
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n" + q["question"].center(80))

        await fake_download()
        for option, keys in zip(q["options"], ["A/U", "Z/I", "E/O", "R/P"]):
            print(option.replace(option[:1], keys).center(80))

        print(f"Score actuel : {pseudo1} - {scores[pseudo1]} points | {pseudo2} - {scores[pseudo2]} points".center(80))

        import threading
        import time

        def countdown(stop_event):
            for i in range(10, 0, -1):
                if stop_event.is_set():
                    break
                print(f"Temps restant : {i} secondes".center(80), end="\r")
                time.sleep(1)
            if not stop_event.is_set():
                print("Temps écoulé !".center(80))
            print(" " * 80, end="\r")  # Efface la ligne après le chrono

        stop_event = threading.Event()
        timer_thread = threading.Thread(target=countdown, args=(stop_event,))
        timer_thread.start()

        reponses = None
        try:
            reponses = input(f"Entrez vos réponses simultanément ({pseudo1}: A/Z/E/R, {pseudo2}: U/I/O/P) : ".center(80)).lower()
            stop_event.set()  # Arrête le chrono si une réponse est donnée
        except Exception:
            pass

        timer_thread.join()

        if not reponses:
            print("Temps écoulé, aucune réponse enregistrée.".center(80))
        else:
            reponse1 = reponses[0] if len(reponses) > 0 else None
            reponse2 = reponses[1] if len(reponses) > 1 else None

            if reponse1 and reponse1 in "azer" and reponse1.upper() == q["answer"]:
                scores[pseudo1] += 100
            if reponse2 and reponse2 in "uiop" and reponse2.upper() == q["answer"]:
                scores[pseudo2] += 100

        print(f"Score actuel : {pseudo1} - {scores[pseudo1]} points | {pseudo2} - {scores[pseudo2]} points".center(80))
        print("Appuyez sur une touche pour continuer...".center(80))
        input()

    print("\nRésultats finaux :")
    print(f"{pseudo1} : {scores[pseudo1]} points".center(80))
    print(f"{pseudo2} : {scores[pseudo2]} points".center(80))

def quiz_solo(pseudo):
    from quizz import quiz_2_joueurs
    questions = quiz_2_joueurs.__globals__["questions"]

    score = 0

    for q in questions:
        print("\n" + q["question"].center(80))
        for option in q["options"]:
            print(option.center(80))

        print(f"Score actuel : {pseudo} - {score} points".center(80))

        reponse = input(f"{pseudo}, entrez votre réponse (A/Z/E/R) : ".center(80)).upper()

        if reponse == q["answer"]:
            score += 100

    print("\nRésultat final :")
    print(f"{pseudo} : {score} points")

if __name__ == "__main__":
    quiz_2_joueurs("Joueur1", "Joueur2")