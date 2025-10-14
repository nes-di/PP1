import sqlite3

def creer_base():
    conn = sqlite3.connect("data/progression.db")
    cursor = conn.cursor()

    # Table pour les joueurs
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS joueurs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pseudo TEXT UNIQUE NOT NULL
    )
    ''')

    # Table pour les parties
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS parties (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        joueur_id INTEGER,
        score INTEGER,
        date_partie TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(joueur_id) REFERENCES joueurs(id)
    )
    ''')

    conn.commit()
    conn.close()

def enregistrer_partie(pseudo, score):
    conn = sqlite3.connect("data/progression.db")
    cursor = conn.cursor()

    # Insérer le joueur s'il n'existe pas
    cursor.execute("INSERT OR IGNORE INTO joueurs (pseudo) VALUES (?)", (pseudo,))

    # Récupérer l'ID du joueur
    cursor.execute("SELECT id FROM joueurs WHERE pseudo = ?", (pseudo,))
    joueur_id = cursor.fetchone()[0]

    # Enregistrer la partie
    cursor.execute("INSERT INTO parties (joueur_id, score) VALUES (?, ?)", (joueur_id, score))

    conn.commit()
    conn.close()

def recuperer_historique():
    conn = sqlite3.connect("data/progression.db")
    cursor = conn.cursor()

    cursor.execute('''
    SELECT joueurs.pseudo, parties.score, parties.date_partie
    FROM parties
    JOIN joueurs ON parties.joueur_id = joueurs.id
    ORDER BY parties.date_partie DESC
    ''')

    historique = cursor.fetchall()
    conn.close()
    return historique
