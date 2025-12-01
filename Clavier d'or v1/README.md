# CLAVIER D'OR V1 - VERSION ORIGINALE

## 📁 Structure du projet

- `main.py` : Point d'entrée du programme
- `Console/menu.py` : Affichage du menu
- `Logique/partie.py` : Logique principale du jeu
- `DataBaseLink/database.py` : Gestion base de données SQLite
- `Modèle/` : Fichiers JSON avec les questions (200 par thème)
- `game.db` : Base de données

## 🚀 Lancement

```bash
python main.py
```

## 📊 Caractéristiques V1

- **5 thèmes** : Culture Générale, Géographie, Maths, Science, Sports
- **200 questions** par thème (stockées en JSON)
- **20 questions aléatoires** par partie
- **Timer de 10 secondes** par question
- **100 points** par bonne réponse
- **Sauvegarde** avec touche 's'

## ⚙️ Fonctionnalités

- Sélection aléatoire de 20 questions parmi 200
- Système de timer avec threading
- Sauvegarde/Chargement de parties
- Tracking des questions déjà répondues
- Interface avec ASCII art

## 🎓 Note

Cette version est **plus complexe** avec :
- Gestion JSON
- Sélection aléatoire
- Plus de vérifications
- Structure modulaire avancée

**⚠️ Trop compliqué pour un projet Bac+1 selon le prof**
