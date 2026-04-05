"""
TestPilot - Runner de tests API
================================
Ce module lit les scénarios de test depuis un fichier YAML,
exécute chaque test, et sauvegarde les résultats en JSON.
"""

import yaml
import requests
import json
import time
import sys
from datetime import datetime
from pathlib import Path


def charger_tests(fichier_yaml: str) -> list:
    """Lit le fichier YAML et retourne la liste des tests."""
    chemin = Path(fichier_yaml)
    if not chemin.exists():
        print(f"❌ Fichier introuvable : {fichier_yaml}")
        sys.exit(1)

    with open(chemin, "r", encoding="utf-8") as f:
        tests = yaml.safe_load(f)

    print(f"📋 {len(tests)} test(s) chargé(s) depuis {fichier_yaml}")
    return tests


def executer_test(test: dict) -> dict:
    """
    Exécute un seul test et retourne le résultat.

    Chaque test produit un dictionnaire avec :
    - nom : le nom du test
    - statut : "PASS" ou "FAIL"
    - temps_reponse : en secondes
    - status_code : le code HTTP reçu
    - erreurs : liste des problèmes trouvés
    """
    nom = test.get("nom", "Test sans nom")
    url = test.get("url")
    methode = test.get("methode", "GET").upper()
    headers = test.get("headers", {})
    body = test.get("body", None)
    attendu = test.get("attendu", {})

    resultat = {
        "nom": nom,
        "url": url,
        "methode": methode,
        "statut": "PASS",
        "temps_reponse": 0,
        "status_code": 0,
        "erreurs": [],
        "timestamp": datetime.now().isoformat(),
    }

    try:
        # Envoyer la requête HTTP
        debut = time.time()

        if methode == "GET":
            reponse = requests.get(url, headers=headers, timeout=10)
        elif methode == "POST":
            reponse = requests.post(url, headers=headers, json=body, timeout=10)
        elif methode == "PUT":
            reponse = requests.put(url, headers=headers, json=body, timeout=10)
        elif methode == "DELETE":
            reponse = requests.delete(url, headers=headers, timeout=10)
        elif methode == "PATCH":
            reponse = requests.patch(url, headers=headers, json=body, timeout=10)
        else:
            resultat["statut"] = "FAIL"
            resultat["erreurs"].append(f"Méthode HTTP inconnue : {methode}")
            return resultat

        temps_reponse = round(time.time() - debut, 3)
        resultat["temps_reponse"] = temps_reponse
        resultat["status_code"] = reponse.status_code

        # --- ASSERTIONS ---

        # 1. Vérifier le status code
        if "status" in attendu:
            if reponse.status_code != attendu["status"]:
                resultat["erreurs"].append(
                    f"Status attendu {attendu['status']}, reçu {reponse.status_code}"
                )

        # 2. Vérifier le temps de réponse
        if "temps_max" in attendu:
            if temps_reponse > attendu["temps_max"]:
                resultat["erreurs"].append(
                    f"Trop lent : {temps_reponse}s (max {attendu['temps_max']}s)"
                )

        # 3. Vérifier le contenu de la réponse
        if "contient" in attendu:
            try:
                data = reponse.json()
                for cle, valeur in attendu["contient"].items():
                    if cle not in data:
                        resultat["erreurs"].append(
                            f"Clé '{cle}' absente de la réponse"
                        )
                    elif data[cle] != valeur:
                        resultat["erreurs"].append(
                            f"'{cle}' attendu {valeur}, reçu {data[cle]}"
                        )
            except json.JSONDecodeError:
                resultat["erreurs"].append("La réponse n'est pas du JSON valide")

        # Si des erreurs ont été trouvées, le test échoue
        if resultat["erreurs"]:
            resultat["statut"] = "FAIL"

    except requests.exceptions.Timeout:
        resultat["statut"] = "FAIL"
        resultat["erreurs"].append("Timeout : le serveur n'a pas répondu à temps")
    except requests.exceptions.ConnectionError:
        resultat["statut"] = "FAIL"
        resultat["erreurs"].append("Impossible de se connecter au serveur")
    except Exception as e:
        resultat["statut"] = "FAIL"
        resultat["erreurs"].append(f"Erreur inattendue : {str(e)}")

    return resultat


def afficher_resultat(resultat: dict):
    """Affiche le résultat d'un test dans le terminal."""
    if resultat["statut"] == "PASS":
        icone = "✅"
    else:
        icone = "❌"

    print(f"  {icone} {resultat['nom']}")
    print(f"     → {resultat['methode']} {resultat['url']}")
    print(f"     → Status: {resultat['status_code']} | Temps: {resultat['temps_reponse']}s")

    for erreur in resultat["erreurs"]:
        print(f"     ⚠️  {erreur}")
    print()


def generer_resume(resultats: list) -> dict:
    """Génère un résumé global des résultats."""
    total = len(resultats)
    passes = sum(1 for r in resultats if r["statut"] == "PASS")
    echecs = total - passes
    temps_moyen = round(
        sum(r["temps_reponse"] for r in resultats) / total, 3
    ) if total > 0 else 0
    taux_reussite = round((passes / total) * 100, 1) if total > 0 else 0

    return {
        "total": total,
        "passes": passes,
        "echecs": echecs,
        "temps_moyen": temps_moyen,
        "taux_reussite": taux_reussite,
        "date": datetime.now().isoformat(),
    }


def sauvegarder_resultats(resultats: list, resume: dict, fichier_sortie: str):
    """Sauvegarde les résultats en JSON."""
    donnees = {
        "resume": resume,
        "resultats": resultats,
    }

    # Charger l'historique existant s'il y en a
    chemin_historique = Path(fichier_sortie).parent / "historique.json"
    historique = []
    if chemin_historique.exists():
        with open(chemin_historique, "r", encoding="utf-8") as f:
            historique = json.load(f)

    # Ajouter ce run à l'historique (garder les 20 derniers)
    historique.append(resume)
    historique = historique[-20:]

    with open(fichier_sortie, "w", encoding="utf-8") as f:
        json.dump(donnees, f, indent=2, ensure_ascii=False)

    with open(chemin_historique, "w", encoding="utf-8") as f:
        json.dump(historique, f, indent=2, ensure_ascii=False)

    print(f"💾 Résultats sauvegardés dans {fichier_sortie}")


def run(fichier_yaml: str = "tests.yaml", fichier_sortie: str = "results.json"):
    """Point d'entrée principal : charge, exécute, affiche, sauvegarde."""
    print()
    print("🚀 TestPilot - Lancement des tests")
    print("=" * 50)
    print()

    # 1. Charger les tests
    tests = charger_tests(fichier_yaml)
    print()

    # 2. Exécuter chaque test
    resultats = []
    for test in tests:
        resultat = executer_test(test)
        afficher_resultat(resultat)
        resultats.append(resultat)

    # 3. Générer et afficher le résumé
    resume = generer_resume(resultats)

    print("=" * 50)
    print(f"📊 Résumé : {resume['passes']}/{resume['total']} tests passés "
          f"({resume['taux_reussite']}%)")
    print(f"⏱️  Temps moyen : {resume['temps_moyen']}s")

    if resume["echecs"] > 0:
        print(f"⚠️  {resume['echecs']} test(s) en échec")
    else:
        print("🎉 Tous les tests sont passés !")

    print()

    # 4. Sauvegarder
    sauvegarder_resultats(resultats, resume, fichier_sortie)

    # Retourner le code de sortie (utile pour CI/CD)
    return 0 if resume["echecs"] == 0 else 1


if __name__ == "__main__":
    fichier = sys.argv[1] if len(sys.argv) > 1 else "tests.yaml"
    code = run(fichier_yaml=fichier)
    sys.exit(code)
