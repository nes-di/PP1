import sqlite3

def creer_base():
    conn = sqlite3.connect("game.db")
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS parties (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pseudo TEXT,
        theme TEXT,
        score INTEGER DEFAULT 0,
        questions_repondues INTEGER DEFAULT 0,
        ids_questions TEXT DEFAULT '',
        statut TEXT DEFAULT 'en_cours',
        date_partie TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    conn.close()

def enregistrer_partie(pseudo, theme, score, questions_repondues, ids_questions):
    conn = sqlite3.connect("game.db")
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM parties WHERE pseudo = ? AND statut = 'en_cours'", (pseudo,))
    

    if isinstance(ids_questions, list):
        ids_str = ','.join(map(str, ids_questions))
    else:
        ids_str = str(ids_questions) if ids_questions else ''
    
    statut = 'terminee' if questions_repondues >= 20 else 'en_cours'
    cursor.execute("""
    INSERT INTO parties (pseudo, theme, score, questions_repondues, ids_questions, statut)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (pseudo, theme, score, questions_repondues, ids_str, statut))
    
    conn.commit()
    conn.close()
    print(f"✅ Partie sauvegardée: {pseudo}, Score: {score}, Questions: {questions_repondues}/20")

def charger_partie(pseudo):
    conn = sqlite3.connect("game.db")
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT theme, score, questions_repondues, ids_questions
    FROM parties
    WHERE pseudo = ? AND statut = 'en_cours'
    ORDER BY date_partie DESC LIMIT 1
    """, (pseudo,))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        theme, score, questions_repondues, ids_questions = result

        if ids_questions and ids_questions.strip():
            ids_list = [int(x.strip()) for x in ids_questions.split(',') if x.strip()]
        else:
            ids_list = []
        print(f"📂 Partie chargée: {pseudo}, Score: {score}, Questions: {questions_repondues}/20")
        return theme, score, questions_repondues, ids_list
    return None