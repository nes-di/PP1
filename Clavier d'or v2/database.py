# Importe le module sqlite3 pour gérer la base de données SQLite
import sqlite3
# Importe le module os pour les opérations système (fichiers, chemins, etc.)
import os

# Fonction qui crée et retourne une connexion à la base de données
def get_connection():
    # sqlite3.connect() ouvre une connexion à quiz.db
    # Si le fichier n'existe pas, il sera créé automatiquement
    # Retourne un objet "connection" qui permet d'interagir avec la base
    return sqlite3.connect("quiz.db")

# Fonction qui crée la structure complète de la base de données
# Crée 3 tables: questions, reponses_joueur, parties
# Initialise aussi les 105 questions si la base est vide
def creer_base():
    # Obtient une connexion à la base de données
    conn = get_connection()
    # Crée un curseur (objet qui permet d'exécuter des requêtes SQL)
    cursor = conn.cursor()
    
    # ===== TABLE 1: QUESTIONS =====
    # Stocke toutes les questions du quiz (105 questions: 5 thèmes × 21 questions)
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
    # Explication des colonnes:
    # - id: identifiant unique de la question
    # - theme: le thème (Culture, Géo, Maths, Science, Sports)
    # - question: texte de la question
    # - option_a/z/e/r: les 4 choix de réponse (touches clavier AZER)
    # - reponse: la bonne réponse (A, Z, E ou R)
    # - est_boss: 0 si question normale, 1 si question boss (vaut 300 points)
    
    # ===== TABLE 2: RÉPONSES DU JOUEUR =====
    # Enregistre chaque question répondue par chaque joueur
    # Permet de savoir quelles questions ont déjà été faites (pour ne pas les reposer)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reponses_joueur (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pseudo TEXT NOT NULL,
        theme TEXT NOT NULL,
        question_id INTEGER NOT NULL,
        date_reponse TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    # Explication des colonnes:
    # - id: identifiant unique de l'enregistrement
    # - pseudo: nom du joueur qui a répondu
    # - theme: le thème de la question
    # - question_id: l'ID de la question répondue (référence à la table questions)
    # - date_reponse: date/heure de la réponse (automatique)
    
    # ===== TABLE 3: PARTIES SAUVEGARDÉES =====
    # Stocke le score actuel de chaque partie en cours
    # Une ligne par combinaison (joueur, thème)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS parties (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pseudo TEXT NOT NULL,
        theme TEXT NOT NULL,
        score INTEGER DEFAULT 0,
        date_sauvegarde TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    # Explication des colonnes:
    # - id: identifiant unique de la partie
    # - pseudo: nom du joueur
    # - theme: thème de la partie
    # - score: score actuel (100 points par bonne réponse, 300 pour le boss)
    # - date_sauvegarde: date/heure de la dernière sauvegarde (automatique)
    
    # ===== ENREGISTREMENT DES TABLES =====
    # conn.commit() valide et enregistre toutes les modifications dans la base
    # Sans commit(), les tables ne seraient pas vraiment créées
    conn.commit()
    
    # ===== INITIALISATION DES QUESTIONS =====
    # Vérifie si la table questions est vide
    # SELECT COUNT(*) compte le nombre de lignes dans la table
    cursor.execute('SELECT COUNT(*) FROM questions')
    # fetchone() récupère le résultat (un tuple avec 1 valeur)
    # [0] prend la première (et seule) valeur du tuple
    # Si le résultat est 0, la table est vide
    if cursor.fetchone()[0] == 0:
        # Appelle la fonction privée qui insère les 105 questions
        _initialiser_questions(cursor)
        # Enregistre les questions dans la base
        conn.commit()
    
    # Ferme la connexion à la base de données
    # Libère les ressources et s'assure que tout est bien enregistré
    conn.close()

# Fonction pour ajouter une nouvelle question dans la base de données
# Paramètres: theme, question, les 4 options (opt_a/z/e/r), reponse, est_boss
# est_boss=0 par défaut (question normale)
def ajouter_question(theme, question, opt_a, opt_z, opt_e, opt_r, reponse, est_boss=0):
    # Ouvre une connexion à la base
    conn = get_connection()
    # Crée un curseur pour exécuter des requêtes
    cursor = conn.cursor()
    # Exécute une requête INSERT pour ajouter une ligne dans la table questions
    # Les ? sont des paramètres qui seront remplacés par les valeurs du tuple
    # Cela évite les injections SQL (sécurité)
    cursor.execute('''
    INSERT INTO questions (theme, question, option_a, option_z, option_e, option_r, reponse, est_boss)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (theme, question, opt_a, opt_z, opt_e, opt_r, reponse, est_boss))
    # Enregistre la modification dans la base
    conn.commit()
    # Ferme la connexion
    conn.close()

# Fonction qui récupère toutes les questions normales d'un thème (SANS le boss)
# Paramètre: theme = le nom du thème (Culture, Géo, Maths, Science, Sports)
# Retourne: une liste de tuples (chaque tuple = une question avec toutes ses données)
def get_questions_par_theme(theme):
    # Ouvre une connexion à la base
    conn = get_connection()
    # Crée un curseur
    cursor = conn.cursor()
    # Exécute une requête SELECT pour récupérer les questions
    # WHERE theme = ? filtre par thème
    # AND est_boss = 0 exclut la question boss (on ne veut que les 19 normales)
    # ORDER BY id trie par ID croissant (ordre d'insertion)
    cursor.execute('''
    SELECT id, question, option_a, option_z, option_e, option_r, reponse, est_boss
    FROM questions
    WHERE theme = ? AND est_boss = 0
    ORDER BY id
    ''', (theme,))
    # fetchall() récupère TOUTES les lignes du résultat
    # Retourne une liste de tuples: [(id1, q1, a1, z1...), (id2, q2, a2...)]
    questions = cursor.fetchall()
    # Ferme la connexion
    conn.close()
    # Retourne la liste des questions
    return questions

# Fonction qui récupère LA question boss d'un thème spécifique
# Paramètre: theme = le nom du thème
# Retourne: un tuple avec les données de la question boss (ou None si pas trouvée)
def get_question_boss(theme):
    # Ouvre une connexion
    conn = get_connection()
    # Crée un curseur
    cursor = conn.cursor()
    # Exécute une requête SELECT pour trouver le boss
    # WHERE theme = ? filtre par thème
    # AND est_boss = 1 ne prend QUE la question boss (exclut les 19 normales)
    cursor.execute('''
    SELECT id, question, option_a, option_z, option_e, option_r, reponse, est_boss
    FROM questions
    WHERE theme = ? AND est_boss = 1
    ''', (theme,))
    # fetchone() récupère UNE SEULE ligne (la première)
    # Retourne un tuple ou None si aucun résultat
    question = cursor.fetchone()
    # Ferme la connexion
    conn.close()
    # Retourne la question boss
    return question

# Fonction qui récupère la liste des IDs des questions déjà répondues par un joueur
# Paramètres: pseudo = nom du joueur, theme = thème concerné
# Retourne: une liste d'IDs [5, 12, 18, 23...]
def get_questions_repondues(pseudo, theme):
    # Ouvre une connexion
    conn = get_connection()
    # Crée un curseur
    cursor = conn.cursor()
    # Exécute une requête SELECT pour récupérer les question_id
    # WHERE filtre par pseudo ET theme
    cursor.execute('''
    SELECT question_id FROM reponses_joueur
    WHERE pseudo = ? AND theme = ?
    ''', (pseudo, theme))
    # fetchall() retourne [(5,), (12,), (18,)...] (liste de tuples)
    # La compréhension de liste [row[0] for row in ...] extrait juste les IDs
    # Résultat final: [5, 12, 18...]
    ids = [row[0] for row in cursor.fetchall()]
    # Ferme la connexion
    conn.close()
    # Retourne la liste des IDs
    return ids

# Fonction qui enregistre qu'un joueur a répondu à une question spécifique
# Cela permet de ne pas reposer la même question si la partie est rechargée
# Paramètres: pseudo, theme, question_id (l'ID de la question répondue)
def enregistrer_reponse(pseudo, theme, question_id):
    # Ouvre une connexion
    conn = get_connection()
    # Crée un curseur
    cursor = conn.cursor()
    # Exécute une requête INSERT pour ajouter une ligne dans reponses_joueur
    # Enregistre: quel joueur, quel thème, quelle question, à quelle date (auto)
    cursor.execute('''
    INSERT INTO reponses_joueur (pseudo, theme, question_id)
    VALUES (?, ?, ?)
    ''', (pseudo, theme, question_id))
    # Enregistre la modification
    conn.commit()
    # Ferme la connexion
    conn.close()

# Fonction qui sauvegarde ou met à jour le score d'une partie en cours
# Si une partie existe déjà pour ce (joueur, thème), met à jour le score
# Sinon, crée une nouvelle entrée
# Paramètres: pseudo, theme, score (le score actuel à sauvegarder)
def sauvegarder_partie(pseudo, theme, score):
    # Ouvre une connexion
    conn = get_connection()
    # Crée un curseur
    cursor = conn.cursor()
    
    # ===== VÉRIFICATION SI LA PARTIE EXISTE DÉJÀ =====
    # Cherche si une ligne existe avec ce pseudo ET ce thème
    cursor.execute('''
    SELECT id FROM parties WHERE pseudo = ? AND theme = ?
    ''', (pseudo, theme))
    
    # fetchone() retourne un tuple si une ligne existe, ou None si rien trouvé
    if cursor.fetchone():
        # ===== CAS 1: LA PARTIE EXISTE DÉJÀ - MISE À JOUR =====
        # Exécute une requête UPDATE pour modifier le score existant
        # Met aussi à jour date_sauvegarde avec l'heure actuelle (CURRENT_TIMESTAMP)
        cursor.execute('''
        UPDATE parties 
        SET score = ?, date_sauvegarde = CURRENT_TIMESTAMP 
        WHERE pseudo = ? AND theme = ?
        ''', (score, pseudo, theme))
    else:
        # ===== CAS 2: PREMIÈRE SAUVEGARDE - INSERTION =====
        # Exécute une requête INSERT pour créer une nouvelle ligne
        cursor.execute('''
        INSERT INTO parties (pseudo, theme, score)
        VALUES (?, ?, ?)
        ''', (pseudo, theme, score))
    
    # Enregistre la modification (UPDATE ou INSERT)
    conn.commit()
    # Ferme la connexion
    conn.close()

# Fonction qui charge le score sauvegardé d'une partie existante
# Paramètres: pseudo, theme
# Retourne: le score (nombre entier) ou 0 si aucune partie n'existe
def charger_partie(pseudo, theme):
    # Ouvre une connexion
    conn = get_connection()
    # Crée un curseur
    cursor = conn.cursor()
    # Exécute une requête SELECT pour récupérer le score
    # WHERE filtre par pseudo ET theme
    cursor.execute('''
    SELECT score FROM parties
    WHERE pseudo = ? AND theme = ?
    ''', (pseudo, theme))
    # fetchone() retourne un tuple (score,) ou None si rien trouvé
    result = cursor.fetchone()
    # Ferme la connexion
    conn.close()
    # Si result existe, retourne result[0] (le score)
    # Sinon, retourne 0 (pas de partie sauvegardée)
    return result[0] if result else 0

# Fonction qui efface complètement la progression d'un joueur sur un thème
# Supprime l'historique des réponses ET le score sauvegardé
# Utilisé quand on commence une NOUVELLE partie (pas une continuation)
# Paramètres: pseudo, theme
def effacer_progression(pseudo, theme):
    # Ouvre une connexion
    conn = get_connection()
    # Crée un curseur
    cursor = conn.cursor()
    
    # ===== SUPPRESSION 1: HISTORIQUE DES RÉPONSES =====
    # Exécute une requête DELETE pour supprimer toutes les réponses enregistrées
    # WHERE filtre par pseudo ET theme pour ne supprimer que ce joueur/thème
    cursor.execute('''
    DELETE FROM reponses_joueur 
    WHERE pseudo = ? AND theme = ?
    ''', (pseudo, theme))
    
    # ===== SUPPRESSION 2: SCORE SAUVEGARDÉ =====
    # Exécute une requête DELETE pour supprimer le score sauvegardé
    cursor.execute('''
    DELETE FROM parties 
    WHERE pseudo = ? AND theme = ?
    ''', (pseudo, theme))
    
    # Enregistre les suppressions dans la base
    conn.commit()
    # Ferme la connexion
    conn.close()

# Fonction qui récupère les 5 dernières parties sauvegardées
# Calcule aussi le nombre de questions restantes pour chaque partie
# Retourne: liste de tuples (pseudo, theme, score, date, questions_restantes)
def get_dernieres_parties():
    # Ouvre une connexion
    conn = get_connection()
    # Crée un curseur
    cursor = conn.cursor()
    # Exécute une requête SQL complexe avec jointure et calcul
    cursor.execute('''
    SELECT 
        p.pseudo, 
        p.theme, 
        p.score, 
        p.date_sauvegarde,
        (20 - COUNT(r.question_id)) as questions_restantes
    FROM parties p
    LEFT JOIN reponses_joueur r ON p.pseudo = r.pseudo AND p.theme = r.theme
    GROUP BY p.pseudo, p.theme, p.score, p.date_sauvegarde
    ORDER BY p.date_sauvegarde DESC
    LIMIT 5
    ''')
    # Explication de la requête:
    # - SELECT sélectionne les colonnes à retourner
    # - FROM parties p : table principale (alias "p")
    # - LEFT JOIN reponses_joueur r : joint avec les réponses (alias "r")
    # - ON ... : condition de jointure (même pseudo ET même thème)
    # - COUNT(r.question_id) : compte le nombre de réponses
    # - (20 - COUNT(...)) : calcule questions restantes (20 total - déjà faites)
    # - GROUP BY : regroupe par partie (pour avoir un COUNT par partie)
    # - ORDER BY ... DESC : trie par date décroissante (plus récent d'abord)
    # - LIMIT 5 : prend seulement les 5 premières lignes
    
    # fetchall() récupère tous les résultats
    parties = cursor.fetchall()
    # Ferme la connexion
    conn.close()
    # Retourne la liste des parties
    return parties

# Fonction PRIVÉE (commence par _) qui initialise toutes les questions dans la base
# Appelée automatiquement par creer_base() si la table questions est vide
# Insère 105 questions: 5 thèmes × 21 questions (20 normales + 1 boss)
# Paramètre: cursor = le curseur de la base (pas besoin de créer une nouvelle connexion)
def _initialiser_questions(cursor):
    # Liste de toutes les questions sous forme de tuples
    # Chaque tuple = (theme, question, opt_a, opt_z, opt_e, opt_r, reponse, est_boss)
    # Les 19 premières de chaque thème ont est_boss=0 (normales)
    # La 20ème a est_boss=1 (boss, vaut 300 points)
    questions_data = [
        # ===== CULTURE GÉNÉRALE (20 questions normales + 1 boss) =====
        ("Culture Générale", "Qui a peint la Joconde ?", "De Vinci", "Picasso", "Van Gogh", "Monet", "A", 0),
        ("Culture Générale", "En quelle année l'homme a-t-il marché sur la Lune ?", "1965", "1969", "1972", "1975", "Z", 0),
        ("Culture Générale", "Quelle est la capitale de l'Espagne ?", "Séville", "Barcelone", "Madrid", "Valence", "E", 0),
        ("Culture Générale", "Qui a écrit Les Misérables ?", "Zola", "Hugo", "Balzac", "Dumas", "Z", 0),
        ("Culture Générale", "Combien de continents existe-t-il ?", "5", "6", "7", "8", "E", 0),
        ("Culture Générale", "Quelle est la planète la plus proche du Soleil ?", "Mars", "Vénus", "Terre", "Mercure", "R", 0),
        ("Culture Générale", "Quel est le plus grand océan ?", "Pacifique", "Atlantique", "Indien", "Arctique", "A", 0),
        ("Culture Générale", "Qui a découvert l'Amérique en 1492 ?", "Magellan", "Colomb", "Vespucci", "Cook", "Z", 0),
        ("Culture Générale", "Combien font 7 x 8 ?", "54", "56", "58", "60", "Z", 0),
        ("Culture Générale", "Quelle est la langue la plus parlée au monde ?", "Espagnol", "Anglais", "Mandarin", "Hindi", "E", 0),
        ("Culture Générale", "Dans quel pays se trouve la tour Eiffel ?", "Belgique", "France", "Suisse", "Italie", "Z", 0),
        ("Culture Générale", "Quel animal est le roi de la jungle ?", "Tigre", "Lion", "Éléphant", "Gorille", "Z", 0),
        ("Culture Générale", "Combien de joueurs dans une équipe de foot ?", "9", "10", "12", "11", "R", 0),
        ("Culture Générale", "Quelle est la capitale de l'Italie ?", "Rome", "Milan", "Naples", "Venise", "A", 0),
        ("Culture Générale", "Quel est le symbole chimique de l'or ?", "Or", "Au", "Ag", "Go", "Z", 0),
        ("Culture Générale", "Qui a inventé l'ampoule électrique ?", "Bell", "Tesla", "Edison", "Marconi", "E", 0),
        ("Culture Générale", "Combien de côtés a un hexagone ?", "8", "5", "7", "6", "R", 0),
        ("Culture Générale", "Quel est le plus grand pays du monde ?", "Russie", "Canada", "Chine", "USA", "A", 0),
        ("Culture Générale", "Quelle est la monnaie du Japon ?", "Won", "Yuan", "Yen", "Dong", "E", 0),
        ("Culture Générale", "En quelle année la Révolution française a-t-elle commencé ?", "1789", "1799", "1804", "1815", "A", 1),
        
        # Géographie (20 + boss)
        ("Géographie", "Quelle est la capitale de la France ?", "Paris", "Lyon", "Marseille", "Nice", "A", 0),
        ("Géographie", "Quel est le plus long fleuve du monde ?", "Amazone", "Nil", "Yangtsé", "Mississippi", "Z", 0),
        ("Géographie", "Combien y a-t-il de pays en Europe ?", "50", "44", "47", "52", "E", 0),
        ("Géographie", "Quel désert est le plus grand du monde ?", "Gobi", "Sahara", "Arabie", "Kalahari", "Z", 0),
        ("Géographie", "Dans quel pays se trouve le Mont Everest ?", "Chine", "Inde", "Tibet", "Népal", "R", 0),
        ("Géographie", "Quelle est la capitale du Canada ?", "Ottawa", "Toronto", "Montréal", "Vancouver", "A", 0),
        ("Géographie", "Quel océan borde l'Afrique à l'ouest ?", "Indien", "Atlantique", "Pacifique", "Arctique", "Z", 0),
        ("Géographie", "Combien d'États composent les USA ?", "49", "48", "50", "52", "E", 0),
        ("Géographie", "Quelle est la capitale de l'Allemagne ?", "Francfort", "Munich", "Hambourg", "Berlin", "R", 0),
        ("Géographie", "Dans quel continent se trouve l'Égypte ?", "Afrique", "Asie", "Europe", "Moyen-Orient", "A", 0),
        ("Géographie", "Quel est le plus petit pays du monde ?", "Monaco", "Vatican", "Nauru", "Liechtenstein", "Z", 0),
        ("Géographie", "Quelle chaîne de montagnes sépare l'Europe de l'Asie ?", "Alpes", "Himalaya", "Oural", "Caucase", "E", 0),
        ("Géographie", "Quelle est la capitale de l'Australie ?", "Brisbane", "Sydney", "Melbourne", "Canberra", "R", 0),
        ("Géographie", "Dans quel pays se trouve la ville de Moscou ?", "Russie", "Ukraine", "Pologne", "Biélorussie", "A", 0),
        ("Géographie", "Quel est le plus grand lac d'Afrique ?", "Tanganyika", "Victoria", "Malawi", "Tchad", "Z", 0),
        ("Géographie", "Combien de fuseaux horaires en Russie ?", "7", "9", "11", "13", "E", 0),
        ("Géographie", "Quelle est la capitale du Brésil ?", "Salvador", "Rio", "São Paulo", "Brasilia", "R", 0),
        ("Géographie", "Dans quel océan se trouvent les Maldives ?", "Indien", "Atlantique", "Pacifique", "Arctique", "A", 0),
        ("Géographie", "Quel pays a la plus grande population ?", "Inde", "Chine", "USA", "Indonésie", "Z", 0),
        ("Géographie", "Quelle est la capitale de la Mongolie ?", "Oulan-Bator", "Astana", "Bichkek", "Tachkent", "A", 1),
        
        # Maths (20 + boss)
        ("Maths", "Combien font 12 + 8 ?", "20", "18", "22", "24", "A", 0),
        ("Maths", "Combien font 15 - 7 ?", "6", "8", "9", "10", "Z", 0),
        ("Maths", "Combien font 6 x 7 ?", "48", "40", "42", "44", "E", 0),
        ("Maths", "Combien font 36 / 6 ?", "5", "6", "7", "8", "Z", 0),
        ("Maths", "Combien font 5² (5 au carré) ?", "20", "10", "15", "25", "R", 0),
        ("Maths", "Quelle est la racine carrée de 64 ?", "8", "6", "10", "12", "A", 0),
        ("Maths", "Combien font 100 - 37 ?", "63", "73", "53", "67", "A", 0),
        ("Maths", "Combien font 9 x 9 ?", "72", "81", "90", "99", "Z", 0),
        ("Maths", "Combien de degrés dans un triangle ?", "90", "180", "360", "270", "Z", 0),
        ("Maths", "Combien font 144 / 12 ?", "16", "10", "12", "14", "E", 0),
        ("Maths", "Quel est le double de 45 ?", "80", "90", "100", "110", "Z", 0),
        ("Maths", "Combien font 3 x 13 ?", "45", "36", "42", "39", "R", 0),
        ("Maths", "Combien de faces a un cube ?", "6", "4", "8", "12", "A", 0),
        ("Maths", "Combien font 50% de 200 ?", "100", "150", "50", "75", "A", 0),
        ("Maths", "Combien font 1000 / 10 ?", "10", "100", "1000", "10000", "Z", 0),
        ("Maths", "Quel est le triple de 15 ?", "60", "30", "45", "75", "E", 0),
        ("Maths", "Combien font 8 + 9 + 3 ?", "18", "19", "21", "20", "R", 0),
        ("Maths", "Combien de millimètres dans 1 mètre ?", "1000", "100", "10", "10000", "A", 0),
        ("Maths", "Combien font 7 x 6 ?", "36", "42", "48", "54", "Z", 0),
        ("Maths", "Combien font 13² + 17² ?", "458", "338", "628", "538", "A", 1),
        
        # Science (20 + boss)
        ("Science", "Quelle planète est surnommée la planète rouge ?", "Mars", "Vénus", "Jupiter", "Saturne", "A", 0),
        ("Science", "Combien d'os dans le corps humain adulte ?", "196", "206", "216", "226", "Z", 0),
        ("Science", "Quel gaz respirons-nous ?", "Azote", "CO2", "Oxygène", "Hydrogène", "E", 0),
        ("Science", "Quelle est la vitesse de la lumière (km/s) ?", "200000", "300000", "400000", "500000", "Z", 0),
        ("Science", "Combien de chromosomes chez l'humain ?", "50", "44", "48", "46", "R", 0),
        ("Science", "Quel est le symbole de l'eau ?", "H2O", "HO", "O2H", "HOH", "A", 0),
        ("Science", "Quelle force nous maintient au sol ?", "Magnétisme", "Gravité", "Inertie", "Friction", "Z", 0),
        ("Science", "Combien de planètes dans le système solaire ?", "9", "7", "8", "10", "E", 0),
        ("Science", "Quel animal pond des œufs et allaite ?", "Cygne", "Ornithorynque", "Kangourou", "Dauphin", "Z", 0),
        ("Science", "Quelle est l'unité de mesure de la force ?", "Pascal", "Joule", "Watt", "Newton", "R", 0),
        ("Science", "Quel organe pompe le sang ?", "Cœur", "Poumon", "Foie", "Rein", "A", 0),
        ("Science", "Combien de dents chez un adulte ?", "28", "32", "36", "30", "Z", 0),
        ("Science", "Quelle partie de la plante fait la photosynthèse ?", "Tige", "Racine", "Feuille", "Fleur", "E", 0),
        ("Science", "Quel est le plus gros mammifère ?", "Hippopotame", "Éléphant", "Girafe", "Baleine bleue", "R", 0),
        ("Science", "À quelle température l'eau bout-elle (°C) ?", "100", "90", "110", "120", "A", 0),
        ("Science", "Quel est le gaz le plus abondant dans l'air ?", "Oxygène", "Azote", "CO2", "Hydrogène", "Z", 0),
        ("Science", "Combien de sens chez l'humain ?", "7", "4", "5", "6", "E", 0),
        ("Science", "Quel est l'animal le plus rapide ?", "Faucon", "Lion", "Antilope", "Guépard", "R", 0),
        ("Science", "Quelle planète a des anneaux ?", "Saturne", "Jupiter", "Uranus", "Neptune", "A", 0),
        ("Science", "Quel scientifique a développé la théorie de la relativité générale ?", "Einstein", "Newton", "Hawking", "Bohr", "A", 1),
        
        # Sports (20 + boss)
        ("Sports", "Combien de joueurs dans une équipe de basket ?", "5", "4", "6", "7", "A", 0),
        ("Sports", "Quelle est la durée d'un match de foot ?", "80 min", "90 min", "100 min", "120 min", "Z", 0),
        ("Sports", "Combien de sets gagnants au tennis (Grand Chelem) ?", "4", "2", "3", "5", "E", 0),
        ("Sports", "Dans quel sport utilise-t-on une raquette ?", "Golf", "Tennis", "Hockey", "Baseball", "Z", 0),
        ("Sports", "Combien de points vaut un essai au rugby ?", "10", "3", "7", "5", "R", 0),
        ("Sports", "Quel pays a gagné le plus de Coupes du Monde de foot ?", "Brésil", "Argentine", "Allemagne", "Italie", "A", 0),
        ("Sports", "Combien de manches dans un match de boxe pro ?", "10", "12", "15", "8", "Z", 0),
        ("Sports", "Quelle distance pour un marathon (km) ?", "45", "40", "42.195", "50", "E", 0),
        ("Sports", "Combien de joueurs sur un terrain de volley ?", "8", "5", "7", "6", "R", 0),
        ("Sports", "Dans quel sport y a-t-il un smash ?", "Tous", "Tennis", "Badminton", "Volley", "A", 0),
        ("Sports", "Quelle est la couleur du maillot jaune au Tour de France ?", "Vert", "Jaune", "Rouge", "Blanc", "Z", 0),
        ("Sports", "Combien de trous sur un parcours de golf ?", "20", "16", "18", "22", "E", 0),
        ("Sports", "Quel sport pratique-t-on sur une piste de 400m ?", "Natation", "Cyclisme", "Patinage", "Athlétisme", "R", 0),
        ("Sports", "Combien de périodes dans un match de hockey sur glace ?", "3", "2", "4", "5", "A", 0),
        ("Sports", "Dans quel sport y a-t-il un wicket ?", "Baseball", "Cricket", "Golf", "Rugby", "Z", 0),
        ("Sports", "Quelle est la hauteur d'un panier de basket (m) ?", "3.15", "2.95", "3.05", "3.25", "E", 0),
        ("Sports", "Combien de grand chelems en tennis par an ?", "6", "3", "5", "4", "R", 0),
        ("Sports", "Dans quel sport dit-on 'strike' ?", "Bowling", "Golf", "Baseball", "Tennis", "A", 0),
        ("Sports", "Combien pèse un ballon de foot (grammes) ?", "400", "430", "450", "500", "Z", 0),
        # Question boss Sports (la 21ème, est_boss=1)
        ("Sports", "En quelle année la France a-t-elle gagné sa première Coupe du Monde de football ?", "1998", "2000", "1996", "2002", "A", 1)
    ]
    
    # ===== INSERTION MASSIVE DES QUESTIONS =====
    # cursor.executemany() exécute la même requête INSERT pour chaque tuple de la liste
    # Beaucoup plus rapide que faire 105 INSERT séparés
    # Les ? sont remplacés par les valeurs de chaque tuple
    cursor.executemany('''
    INSERT INTO questions (theme, question, option_a, option_z, option_e, option_r, reponse, est_boss)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', questions_data)
    # Note: le commit() est fait dans creer_base(), pas ici
