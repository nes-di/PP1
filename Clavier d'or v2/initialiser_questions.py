from database import *

def init_questions():
    print("Création de la base de données...")
    creer_base()
    
    # ========== CULTURE GÉNÉRALE (20 questions + 1 boss) ==========
    theme = "Culture Générale"
    
    questions_culture = [
        ("Qui a peint la Joconde ?", "De Vinci", "Picasso", "Van Gogh", "Monet", "A"),
        ("En quelle année l'homme a-t-il marché sur la Lune ?", "1965", "1969", "1972", "1975", "Z"),
        ("Quelle est la capitale de l'Espagne ?", "Séville", "Barcelone", "Madrid", "Valence", "E"),
        ("Qui a écrit Les Misérables ?", "Zola", "Hugo", "Balzac", "Dumas", "Z"),
        ("Combien de continents existe-t-il ?", "5", "6", "7", "8", "E"),
        ("Quelle est la planète la plus proche du Soleil ?", "Mars", "Vénus", "Terre", "Mercure", "R"),
        ("Quel est le plus grand océan ?", "Pacifique", "Atlantique", "Indien", "Arctique", "A"),
        ("Qui a découvert l'Amérique en 1492 ?", "Magellan", "Colomb", "Vespucci", "Cook", "Z"),
        ("Combien font 7 x 8 ?", "54", "56", "58", "60", "Z"),
        ("Quelle est la langue la plus parlée au monde ?", "Espagnol", "Anglais", "Mandarin", "Hindi", "E"),
        ("Dans quel pays se trouve la tour Eiffel ?", "Belgique", "France", "Suisse", "Italie", "Z"),
        ("Quel animal est le roi de la jungle ?", "Tigre", "Lion", "Éléphant", "Gorille", "Z"),
        ("Combien de joueurs dans une équipe de foot ?", "9", "10", "12", "11", "R"),
        ("Quelle est la capitale de l'Italie ?", "Rome", "Milan", "Naples", "Venise", "A"),
        ("Quel est le symbole chimique de l'or ?", "Or", "Au", "Ag", "Go", "Z"),
        ("Qui a inventé l'ampoule électrique ?", "Bell", "Tesla", "Edison", "Marconi", "E"),
        ("Combien de côtés a un hexagone ?", "8", "5", "7", "6", "R"),
        ("Quel est le plus grand pays du monde ?", "Russie", "Canada", "Chine", "USA", "A"),
        ("Quelle est la monnaie du Japon ?", "Won", "Yuan", "Yen", "Dong", "E"),
        ("En quelle année la Révolution française a-t-elle commencé ?", "1789", "1799", "1804", "1815", "A")
    ]
    
    for i, q in enumerate(questions_culture):
        est_boss = 1 if i == 19 else 0
        ajouter_question(theme, q[0], q[1], q[2], q[3], q[4], q[5], est_boss)
    
    # ========== GÉOGRAPHIE (20 questions + 1 boss) ==========
    theme = "Géographie"
    
    questions_geo = [
        ("Quelle est la capitale de la France ?", "Paris", "Lyon", "Marseille", "Nice", "A"),
        ("Quel est le plus long fleuve du monde ?", "Amazone", "Nil", "Yangtsé", "Mississippi", "Z"),
        ("Combien y a-t-il de pays en Europe ?", "50", "44", "47", "52", "E"),
        ("Quel désert est le plus grand du monde ?", "Gobi", "Sahara", "Arabie", "Kalahari", "Z"),
        ("Dans quel pays se trouve le Mont Everest ?", "Chine", "Inde", "Tibet", "Népal", "R"),
        ("Quelle est la capitale du Canada ?", "Ottawa", "Toronto", "Montréal", "Vancouver", "A"),
        ("Quel océan borde l'Afrique à l'ouest ?", "Indien", "Atlantique", "Pacifique", "Arctique", "Z"),
        ("Combien d'États composent les USA ?", "49", "48", "50", "52", "E"),
        ("Quelle est la capitale de l'Allemagne ?", "Francfort", "Munich", "Hambourg", "Berlin", "R"),
        ("Dans quel continent se trouve l'Égypte ?", "Afrique", "Asie", "Europe", "Moyen-Orient", "A"),
        ("Quel est le plus petit pays du monde ?", "Monaco", "Vatican", "Nauru", "Liechtenstein", "Z"),
        ("Quelle chaîne de montagnes sépare l'Europe de l'Asie ?", "Alpes", "Himalaya", "Oural", "Caucase", "E"),
        ("Quelle est la capitale de l'Australie ?", "Brisbane", "Sydney", "Melbourne", "Canberra", "R"),
        ("Dans quel pays se trouve la ville de Moscou ?", "Russie", "Ukraine", "Pologne", "Biélorussie", "A"),
        ("Quel est le plus grand lac d'Afrique ?", "Tanganyika", "Victoria", "Malawi", "Tchad", "Z"),
        ("Combien de fuseaux horaires en Russie ?", "7", "9", "11", "13", "E"),
        ("Quelle est la capitale du Brésil ?", "Salvador", "Rio", "São Paulo", "Brasilia", "R"),
        ("Dans quel océan se trouvent les Maldives ?", "Indien", "Atlantique", "Pacifique", "Arctique", "A"),
        ("Quel pays a la plus grande population ?", "Inde", "Chine", "USA", "Indonésie", "Z"),
        ("Quelle est la capitale de la Mongolie ?", "Oulan-Bator", "Astana", "Bichkek", "Tachkent", "A")
    ]
    
    for i, q in enumerate(questions_geo):
        est_boss = 1 if i == 19 else 0
        ajouter_question(theme, q[0], q[1], q[2], q[3], q[4], q[5], est_boss)
    
    # ========== MATHS (20 questions + 1 boss) ==========
    theme = "Maths"
    
    questions_maths = [
        ("Combien font 12 + 8 ?", "20", "18", "22", "24", "A"),
        ("Combien font 15 - 7 ?", "6", "8", "9", "10", "Z"),
        ("Combien font 6 x 7 ?", "48", "40", "42", "44", "E"),
        ("Combien font 36 / 6 ?", "5", "6", "7", "8", "Z"),
        ("Combien font 5² (5 au carré) ?", "20", "10", "15", "25", "R"),
        ("Quelle est la racine carrée de 64 ?", "8", "6", "10", "12", "A"),
        ("Combien font 100 - 37 ?", "63", "73", "53", "67", "A"),
        ("Combien font 9 x 9 ?", "72", "81", "90", "99", "Z"),
        ("Combien de degrés dans un triangle ?", "90", "180", "360", "270", "Z"),
        ("Combien font 144 / 12 ?", "16", "10", "12", "14", "E"),
        ("Quel est le double de 45 ?", "80", "90", "100", "110", "Z"),
        ("Combien font 3 x 13 ?", "45", "36", "42", "39", "R"),
        ("Combien de faces a un cube ?", "6", "4", "8", "12", "A"),
        ("Combien font 50% de 200 ?", "100", "150", "50", "75", "A"),
        ("Combien font 1000 / 10 ?", "10", "100", "1000", "10000", "Z"),
        ("Quel est le triple de 15 ?", "60", "30", "45", "75", "E"),
        ("Combien font 8 + 9 + 3 ?", "18", "19", "21", "20", "R"),
        ("Combien de millimètres dans 1 mètre ?", "1000", "100", "10", "10000", "A"),
        ("Combien font 7 x 6 ?", "36", "42", "48", "54", "Z"),
        ("Combien font 13² + 17² ?", "458", "338", "628", "538", "A")
    ]
    
    for i, q in enumerate(questions_maths):
        est_boss = 1 if i == 19 else 0
        ajouter_question(theme, q[0], q[1], q[2], q[3], q[4], q[5], est_boss)
    
    # ========== SCIENCE (20 questions + 1 boss) ==========
    theme = "Science"
    
    questions_science = [
        ("Quelle planète est surnommée la planète rouge ?", "Mars", "Vénus", "Jupiter", "Saturne", "A"),
        ("Combien d'os dans le corps humain adulte ?", "196", "206", "216", "226", "Z"),
        ("Quel gaz respirons-nous ?", "Azote", "CO2", "Oxygène", "Hydrogène", "E"),
        ("Quelle est la vitesse de la lumière (km/s) ?", "200000", "300000", "400000", "500000", "Z"),
        ("Combien de chromosomes chez l'humain ?", "50", "44", "48", "46", "R"),
        ("Quel est le symbole de l'eau ?", "H2O", "HO", "O2H", "HOH", "A"),
        ("Quelle force nous maintient au sol ?", "Magnétisme", "Gravité", "Inertie", "Friction", "Z"),
        ("Combien de planètes dans le système solaire ?", "9", "7", "8", "10", "E"),
        ("Quel animal pond des œufs et allaite ?", "Cygne", "Ornithorynque", "Kangourou", "Dauphin", "Z"),
        ("Quelle est l'unité de mesure de la force ?", "Pascal", "Joule", "Watt", "Newton", "R"),
        ("Quel organe pompe le sang ?", "Cœur", "Poumon", "Foie", "Rein", "A"),
        ("Combien de dents chez un adulte ?", "28", "32", "36", "30", "Z"),
        ("Quelle partie de la plante fait la photosynthèse ?", "Tige", "Racine", "Feuille", "Fleur", "E"),
        ("Quel est le plus gros mammifère ?", "Hippopotame", "Éléphant", "Girafe", "Baleine bleue", "R"),
        ("À quelle température l'eau bout-elle (°C) ?", "100", "90", "110", "120", "A"),
        ("Quel est le gaz le plus abondant dans l'air ?", "Oxygène", "Azote", "CO2", "Hydrogène", "Z"),
        ("Combien de sens chez l'humain ?", "7", "4", "5", "6", "E"),
        ("Quel est l'animal le plus rapide ?", "Faucon", "Lion", "Antilope", "Guépard", "R"),
        ("Quelle planète a des anneaux ?", "Saturne", "Jupiter", "Uranus", "Neptune", "A"),
        ("Quel scientifique a développé la théorie de la relativité générale ?", "Einstein", "Newton", "Hawking", "Bohr", "A")
    ]
    
    for i, q in enumerate(questions_science):
        est_boss = 1 if i == 19 else 0
        ajouter_question(theme, q[0], q[1], q[2], q[3], q[4], q[5], est_boss)
    
    # ========== SPORTS (20 questions + 1 boss) ==========
    theme = "Sports"
    
    questions_sports = [
        ("Combien de joueurs dans une équipe de basket ?", "5", "4", "6", "7", "A"),
        ("Quelle est la durée d'un match de foot ?", "80 min", "90 min", "100 min", "120 min", "Z"),
        ("Combien de sets gagnants au tennis (Grand Chelem) ?", "4", "2", "3", "5", "E"),
        ("Dans quel sport utilise-t-on une raquette ?", "Golf", "Tennis", "Hockey", "Baseball", "Z"),
        ("Combien de points vaut un essai au rugby ?", "10", "3", "7", "5", "R"),
        ("Quel pays a gagné le plus de Coupes du Monde de foot ?", "Brésil", "Argentine", "Allemagne", "Italie", "A"),
        ("Combien de manches dans un match de boxe pro ?", "10", "12", "15", "8", "Z"),
        ("Quelle distance pour un marathon (km) ?", "45", "40", "42.195", "50", "E"),
        ("Combien de joueurs sur un terrain de volley ?", "8", "5", "7", "6", "R"),
        ("Dans quel sport y a-t-il un smash ?", "Tous", "Tennis", "Badminton", "Volley", "A"),
        ("Quelle est la couleur du maillot jaune au Tour de France ?", "Vert", "Jaune", "Rouge", "Blanc", "Z"),
        ("Combien de trous sur un parcours de golf ?", "20", "16", "18", "22", "E"),
        ("Quel sport pratique-t-on sur une piste de 400m ?", "Natation", "Cyclisme", "Patinage", "Athlétisme", "R"),
        ("Combien de périodes dans un match de hockey sur glace ?", "3", "2", "4", "5", "A"),
        ("Dans quel sport y a-t-il un wicket ?", "Baseball", "Cricket", "Golf", "Rugby", "Z"),
        ("Quelle est la hauteur d'un panier de basket (m) ?", "3.15", "2.95", "3.05", "3.25", "E"),
        ("Combien de grand chelems en tennis par an ?", "6", "3", "5", "4", "R"),
        ("Dans quel sport dit-on 'strike' ?", "Bowling", "Golf", "Baseball", "Tennis", "A"),
        ("Combien pèse un ballon de foot (grammes) ?", "400", "430", "450", "500", "Z"),
        ("En quelle année la France a-t-elle gagné sa première Coupe du Monde de football ?", "1998", "2000", "1996", "2002", "A")
    ]
    
    for i, q in enumerate(questions_sports):
        est_boss = 1 if i == 19 else 0
        ajouter_question(theme, q[0], q[1], q[2], q[3], q[4], q[5], est_boss)

if __name__ == "__main__":
    init_questions()
