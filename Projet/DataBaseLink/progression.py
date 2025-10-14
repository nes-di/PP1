import sqlite3
import datetime

# Fonction pour créer la base de données et les tables nécessaires
# - joueurs : stocke les pseudos des joueurs
# - parties : enregistre les scores des parties jouées
def creer_base():
    conn = sqlite3.connect("Projet/data/progression.db")
    cursor = conn.cursor()

    # Création de la table des joueurs
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS joueurs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pseudo TEXT UNIQUE NOT NULL
    )
    ''')

    # Supprimer la table des parties si elle existe
    cursor.execute('DROP TABLE IF EXISTS parties')

    # Création de la table des parties avec des colonnes supplémentaires
    cursor.execute('''
    CREATE TABLE parties (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        joueur_id INTEGER UNIQUE,
        score INTEGER,
        questions_repondues INTEGER DEFAULT 0,
        ids_questions_repondues TEXT DEFAULT '',
        date_partie TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(joueur_id) REFERENCES joueurs(id)
    )
    ''')

    conn.commit()
    conn.close()

# Fonction pour enregistrer une partie dans la base de données
# - pseudo : le pseudo du joueur
# - score : le score obtenu par le joueur
def enregistrer_partie(pseudo, score, questions_repondues=0, ids_questions_repondues=""):
    conn = sqlite3.connect("Projet/data/progression.db")
    cursor = conn.cursor()

    # Insérer le joueur s'il n'existe pas déjà
    cursor.execute("INSERT OR IGNORE INTO joueurs (pseudo) VALUES (?)", (pseudo,))

    # Récupérer l'ID du joueur
    cursor.execute("SELECT id FROM joueurs WHERE pseudo = ?", (pseudo,))
    joueur_id = cursor.fetchone()[0]

    # Mettre à jour ou insérer la dernière étape du joueur
    cursor.execute("""
    INSERT INTO parties (joueur_id, score, questions_repondues, ids_questions_repondues)
    VALUES (?, ?, ?, ?)
    ON CONFLICT(joueur_id) DO UPDATE SET 
        score=excluded.score, 
        questions_repondues=excluded.questions_repondues, 
        ids_questions_repondues=excluded.ids_questions_repondues, 
        date_partie=CURRENT_TIMESTAMP
    """, (joueur_id, score, questions_repondues, ids_questions_repondues))

    conn.commit()
    conn.close()

def recuperer_historique():
    conn = sqlite3.connect("Projet/data/progression.db")
    cursor = conn.cursor()

    # Récupérer uniquement la dernière étape de chaque joueur
    cursor.execute('''
    SELECT joueurs.pseudo, parties.score, parties.date_partie
    FROM parties
    JOIN joueurs ON parties.joueur_id = joueurs.id
    WHERE parties.date_partie = (
        SELECT MAX(date_partie)
        FROM parties p2
        WHERE p2.joueur_id = parties.joueur_id
    )
    ORDER BY parties.date_partie DESC
    ''')

    historique = cursor.fetchall()
    conn.close()

    # Ajuster les heures pour le fuseau horaire (+2 heures)
    historique_ajuste = []
    for pseudo, score, date_partie in historique:
        date_ajustee = datetime.datetime.strptime(date_partie, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(hours=2)
        historique_ajuste.append((pseudo, score, date_ajustee.strftime("%Y-%m-%d %H:%M:%S")))

    return historique_ajuste