import sqlite3
import os

# Fonction qui crée et retourne une connexion à la base de données
def get_connection():
    return sqlite3.connect("quiz.db")

# Fonction qui crée la structure complète de la base de données
def creer_base():
    conn = get_connection()
    cursor = conn.cursor()
    
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
    
    # Stocke le score actuel de chaque partie en cours
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS parties (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pseudo TEXT NOT NULL,
        theme TEXT NOT NULL,
        score INTEGER DEFAULT 0,
        date_sauvegarde TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    cursor.execute('SELECT COUNT(*) FROM questions')
    if cursor.fetchone()[0] == 0:
        _initialiser_questions(cursor)
        conn.commit()
    conn.close()

# Fonction pour ajouter une nouvelle question dans la base de données
def ajouter_question(theme, question, opt_a, opt_z, opt_e, opt_r, reponse, est_boss=0):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO questions (theme, question, option_a, option_z, option_e, option_r, reponse, est_boss)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (theme, question, opt_a, opt_z, opt_e, opt_r, reponse, est_boss))
    conn.commit()
    conn.close()

# Fonction qui récupère toutes les questions normales d'un thème (SANS le boss)
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

# Fonction qui récupère la question boss d'un thème spécifique
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

# Fonction qui récupère la liste des IDs des questions déjà répondues par un joueur
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

# Fonction qui enregistre qu'un joueur a répondu à une question spécifique
def enregistrer_reponse(pseudo, theme, question_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO reponses_joueur (pseudo, theme, question_id)
    VALUES (?, ?, ?)
    ''', (pseudo, theme, question_id))
    conn.commit()
    conn.close()

# Fonction qui sauvegarde ou met à jour le score d'une partie en cours
def sauvegarder_partie(pseudo, theme, score):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT id FROM parties WHERE pseudo = ? AND theme = ?
    ''', (pseudo, theme))
    if cursor.fetchone():
        cursor.execute('''
        UPDATE parties 
        SET score = ?, date_sauvegarde = CURRENT_TIMESTAMP 
        WHERE pseudo = ? AND theme = ?
        ''', (score, pseudo, theme))
    else:
        cursor.execute('''
        INSERT INTO parties (pseudo, theme, score)
        VALUES (?, ?, ?)
        ''', (pseudo, theme, score))
    conn.commit()
    conn.close()

# Fonction qui charge le score sauvegardé d'une partie existante
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

# Fonction qui efface complètement la progression d'un joueur sur un thème
def effacer_progression(pseudo, theme):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    DELETE FROM reponses_joueur 
    WHERE pseudo = ? AND theme = ?
    ''', (pseudo, theme))
    cursor.execute('''
    DELETE FROM parties 
    WHERE pseudo = ? AND theme = ?
    ''', (pseudo, theme))
    conn.commit()
    conn.close()

# Fonction qui récupère les 5 dernières parties sauvegardées
# Calcule aussi le nombre de questions restantes pour chaque partie
def get_dernieres_parties():
    conn = get_connection()
    cursor = conn.cursor()
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
    parties = cursor.fetchall()
    conn.close()
    return parties

# Appelée automatiquement par creer_base() si la table questions est vide
def _initialiser_questions(cursor):
    questions_data = [
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
        ("Sports", "En quelle année la France a-t-elle gagné sa première Coupe du Monde de football ?", "1998", "2000", "1996", "2002", "A", 1)
    ]
    
    # Exécution la même requête INSERT pour chaque tuple de la liste
    cursor.executemany('''
    INSERT INTO questions (theme, question, option_a, option_z, option_e, option_r, reponse, est_boss)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', questions_data)
