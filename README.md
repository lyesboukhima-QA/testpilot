# ✈ TestPilot

**Framework léger d'automatisation de tests API avec dashboard de reporting.**

TestPilot permet de définir des scénarios de test d'API en YAML, de les exécuter automatiquement, et de visualiser les résultats dans un dashboard HTML interactif.

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![CI](https://img.shields.io/badge/CI-GitHub%20Actions-blue?logo=githubactions&logoColor=white)

---

## Fonctionnalités

- **Configuration en YAML** : Définir des tests lisibles, même pour les non-développeurs
- **Support multi-méthodes** : GET, POST, PUT, PATCH, DELETE
- **Assertions flexibles** : Status code, temps de réponse, contenu JSON
- **Dashboard HTML** : Rapport visuel avec jauge, métriques et historique
- **CI/CD intégré** : Pipeline GitHub Actions prêt à l'emploi
- **Historique** : Suivi de l'évolution des résultats sur les 20 derniers runs

---

## Installation

```bash
git clone https://github.com/ton-username/testpilot.git
cd testpilot
pip install -r requirements.txt
```

## Utilisation rapide

```bash
# Lancer les tests + générer le rapport
python testpilot.py

# Utiliser un fichier de tests spécifique
python testpilot.py mes_tests.yaml

# Lancer seulement les tests (sans rapport)
python runner.py

# Générer le rapport à partir de résultats existants
python reporter.py
```

## Écrire des tests

Les tests sont définis dans un fichier YAML. Voici un exemple :

```yaml
- nom: "Vérifier que l'API répond"
  url: "https://api.exemple.com/health"
  methode: GET
  attendu:
    status: 200
    temps_max: 2

- nom: "Créer un utilisateur"
  url: "https://api.exemple.com/users"
  methode: POST
  headers:
    Content-Type: "application/json"
    Authorization: "Bearer mon-token"
  body:
    nom: "Jean Dupont"
    email: "jean@exemple.com"
  attendu:
    status: 201
    temps_max: 3
    contient:
      nom: "Jean Dupont"
```

### Options disponibles

| Champ | Description | Requis |
|-------|-------------|--------|
| `nom` | Nom descriptif du test | Oui |
| `url` | URL de l'API à tester | Oui |
| `methode` | GET, POST, PUT, PATCH, DELETE | Non (défaut: GET) |
| `headers` | En-têtes HTTP | Non |
| `body` | Corps de la requête (JSON) | Non |
| `attendu.status` | Code HTTP attendu | Non |
| `attendu.temps_max` | Temps max en secondes | Non |
| `attendu.contient` | Vérifier des champs dans la réponse JSON | Non |

## Dashboard

Le rapport est généré dans `dashboard.html`. Il contient :

- **Métriques globales** : total, réussis, échoués, temps moyen
- **Jauge visuelle** : taux de réussite en pourcentage
- **Historique** : graphique des runs précédents
- **Détail des tests** : chaque test avec son statut, URL, et erreurs

## CI/CD avec GitHub Actions

Le pipeline `.github/workflows/tests.yml` est déjà configuré pour :

1. Lancer les tests à chaque push sur `main`
2. Exécuter quotidiennement à 8h UTC
3. Sauvegarder le rapport en artifact téléchargeable

---

## Structure du projet

```
testpilot/
├── testpilot.py          # Script principal (tout-en-un)
├── runner.py             # Moteur d'exécution des tests
├── reporter.py           # Générateur de rapport HTML
├── tests.yaml            # Scénarios de test
├── requirements.txt      # Dépendances Python
├── README.md             # Ce fichier
└── .github/
    └── workflows/
        └── tests.yml     # Pipeline CI/CD
```

## Contribuer

Les contributions sont les bienvenues ! N'hésite pas à ouvrir une issue ou un pull request.

## Licence

MIT License — libre d'utilisation et de modification.
