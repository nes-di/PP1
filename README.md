# 🎮 LE CLAVIER D'OR - PROJET QUIZ

Projet de quiz interactif en Python avec 2 versions différentes.

## 📂 Structure du projet

```
PP1 - Clavier d'Or/
├── Clavier d'or v1/     ← Version originale (complexe)
├── Clavier d'or v2/     ← Version simplifiée (recommandée)
└── README.md            ← Ce fichier
```

## 🎯 Comparaison des versions

### 🔵 Version 1 (Originale)
- **Stockage** : Fichiers JSON (200 questions/thème)
- **Questions** : Sélection aléatoire de 20 parmi 200
- **Structure** : Modulaire (Console, Logique, DataBase, Modèle)
- **Complexité** : ⭐⭐⭐⭐⭐ (Trop pour Bac+1)
- **Timer** : 10 secondes
- **Points** : 100 par question
- **Boss** : ❌ Non

### 🟢 Version 2 (Simplifiée) ⭐ RECOMMANDÉE
- **Stockage** : Base de données SQLite pure
- **Questions** : 20 questions fixes par thème (ordre)
- **Structure** : Simple (2 fichiers principaux)
- **Complexité** : ⭐⭐ (Adapté Bac+1)
- **Timer** : 10 secondes (questions) / 15 secondes (boss)
- **Points** : 100 par question / 300 pour le boss
- **Boss** : ✅ Oui (1 question difficile finale)

## 🚀 Démarrage rapide

### Version 2 (Recommandée)
```bash
cd "Clavier d'or v2"
python initialiser_questions.py   # Une seule fois
python main.py                     # Lancer le jeu
```

### Version 1
```bash
cd "Clavier d'or v1"
python main.py
```

## 📋 Fonctionnalités communes

✅ 5 thèmes : Culture Générale, Géographie, Maths, Science, Sports
✅ Sauvegarde et reprise de parties
✅ Suivi des questions déjà répondues
✅ Système de scoring
✅ Interface en console

## 🎓 Retour du professeur

**V1** : "Trop compliqué pour le niveau, trop de vérifications et contradictions"
**V2** : Structure simplifiée, logique plus claire, niveau adapté

## 💡 Pourquoi 2 versions ?

- **V1** : Démonstration de compétences avancées
- **V2** : Projet adapté au niveau et aux consignes
  - Boss de fin ajouté ✅
  - Commentaires détaillés ✅
  - Logique simplifiée ✅

## 📊 Base de données (V2)

3 tables principales :
- `questions` : 105 questions (20+1 boss par thème)
- `reponses_joueur` : Tracking des réponses
- `parties` : Sauvegarde des scores

## 👨‍💻 Auteur

Projet réalisé dans le cadre du cours PP1 - CESI

---

**🎯 Pour évaluation : Utiliser la Version 2**
