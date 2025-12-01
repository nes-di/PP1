import sqlite3

# Connexion à la base de données
def get_connection():
    return sqlite3.connect("quiz.db")

# Création de toutes les tables nécessaires
def creer_base():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Table des questions avec leur thème
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        theme TEXT NOT NULL,
        question TEXT NOT NULL,
        option_a TEXT NOT NULL,
        option_z TEXT NOT NULL,
        option_e TEXT NOT NULL,
        option_r TEXT NOT NULL,
        reponse TEXT NOT NULL,
        est_boss INTEGER DEFAULT 0
    )
    ''')
    
    # Table pour suivre les réponses du joueur
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reponses_joueur (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pseudo TEXT NOT NULL,
        theme TEXT NOT NULL,
        question_id INTEGER NOT NULL,
        date_reponse TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Table pour sauvegarder les parties en cours
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS parties (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pseudo TEXT NOT NULL,
        theme TEXT NOT NULL,
        score INTEGER DEFAULT 0,
        date_partie TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    conn.close()

# Ajoute une question dans la base
def ajouter_question(theme, question, opt_a, opt_z, opt_e, opt_r, reponse, est_boss=0):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO questions (theme, question, option_a, option_z, option_e, option_r, reponse, est_boss)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (theme, question, opt_a, opt_z, opt_e, opt_r, reponse, est_boss))
    conn.commit()
    conn.close()

# Récupère toutes les questions d'un thème (boss compris)
def get_questions_par_theme(theme):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT id, question, option_a, option_z, option_e, option_r, reponse, est_boss
    FROM questions
    WHERE theme = ? AND est_boss = 0
    ORDER BY id
    ''', (theme,))
    questions = cursor.fetchall()
    conn.close()
    return questions

# Charge la question boss pour un thème
def get_question_boss(theme):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT id, question, option_a, option_z, option_e, option_r, reponse, est_boss
    FROM questions
    WHERE theme = ? AND est_boss = 1
    ''', (theme,))
    question = cursor.fetchone()
    conn.close()
    return question

# Vérifie quelles questions le joueur a déjà répondu
def get_questions_repondues(pseudo, theme):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT question_id FROM reponses_joueur
    WHERE pseudo = ? AND theme = ?
    ''', (pseudo, theme))
    ids = [row[0] for row in cursor.fetchall()]
    conn.close()
    return ids

# Enregistre qu'un joueur a répondu à une question
def enregistrer_reponse(pseudo, theme, question_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO reponses_joueur (pseudo, theme, question_id)
    VALUES (?, ?, ?)
    ''', (pseudo, theme, question_id))
    conn.commit()
    conn.close()

# Sauvegarde ou met à jour le score d'une partie
def sauvegarder_partie(pseudo, theme, score):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Vérifie si une partie existe déjà
    cursor.execute('''
    SELECT id FROM parties WHERE pseudo = ? AND theme = ?
    ''', (pseudo, theme))
    
    if cursor.fetchone():
        # Met à jour le score
        cursor.execute('''
        UPDATE parties SET score = ? WHERE pseudo = ? AND theme = ?
        ''', (score, pseudo, theme))
    else:
        # Crée une nouvelle partie
        cursor.execute('''
        INSERT INTO parties (pseudo, theme, score)
        VALUES (?, ?, ?)
        ''', (pseudo, theme, score))
    
    conn.commit()
    conn.close()

# Charge le score d'une partie sauvegardée
def charger_partie(pseudo, theme):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT score FROM parties
    WHERE pseudo = ? AND theme = ?
    ''', (pseudo, theme))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0

# Supprime l'historique et le score d'un joueur pour un thème donné
def effacer_progression(pseudo, theme):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Supprime les réponses enregistrées
    cursor.execute('''
    DELETE FROM reponses_joueur 
    WHERE pseudo = ? AND theme = ?
    ''', (pseudo, theme))
    
    # Supprime la partie sauvegardée (score)
    cursor.execute('''
    DELETE FROM parties 
    WHERE pseudo = ? AND theme = ?
    ''', (pseudo, theme))
    
    conn.commit()
    conn.close()
