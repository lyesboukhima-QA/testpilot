"""
TestPilot - Script principal
==============================
Lance les tests ET génère le rapport en une seule commande.

Usage:
    python testpilot.py                    # utilise tests.yaml par défaut
    python testpilot.py mon_fichier.yaml   # fichier custom
"""

import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

from runner import run as run_tests
from reporter import run as run_report


def main():
    fichier_yaml = sys.argv[1] if len(sys.argv) > 1 else "tests.yaml"

    print()
    print("=" * 50)
    print("  ✈  TestPilot - Automatisation de tests API")
    print("=" * 50)

    # Étape 1 : Exécuter les tests
    code_sortie = run_tests(fichier_yaml=fichier_yaml)

    # Étape 2 : Générer le rapport HTML
    run_report()

    if code_sortie == 0:
        print("🎉 Tout est vert ! Ouvre dashboard.html pour voir les résultats.")
    else:
        print("⚠️  Certains tests ont échoué. Consulte le dashboard pour les détails.")

    return code_sortie


if __name__ == "__main__":
    sys.exit(main())
