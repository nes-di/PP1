from database import *

# Test avec Culture Générale
theme = "Culture Générale"
pseudo = "nes"

print("=== TEST NOUVELLE PARTIE ===")
# Simule une nouvelle partie
effacer_progression(pseudo, theme)

questions = get_questions_par_theme(theme)
questions_repondues = get_questions_repondues(pseudo, theme)
questions_a_faire = [q for q in questions if q[0] not in questions_repondues]

print(f"Questions chargées: {len(questions)}")
print(f"IDs des questions: {[q[0] for q in questions]}")
print(f"Questions répondues: {questions_repondues}")
print(f"Questions à faire: {len(questions_a_faire)}")
print(f"IDs à faire: {[q[0] for q in questions_a_faire]}")
