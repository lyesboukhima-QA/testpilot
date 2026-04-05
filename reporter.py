"""
TestPilot - Générateur de rapport HTML
========================================
Ce module lit les résultats JSON produits par le runner
et génère un beau dashboard HTML interactif.
"""

import json
import sys
from pathlib import Path
from datetime import datetime


def charger_resultats(fichier_json: str) -> dict:
    """Charge les résultats depuis le fichier JSON."""
    chemin = Path(fichier_json)
    if not chemin.exists():
        print(f"❌ Fichier introuvable : {fichier_json}")
        print("💡 Lance d'abord : python runner.py")
        sys.exit(1)

    with open(chemin, "r", encoding="utf-8") as f:
        return json.load(f)


def charger_historique(dossier: str) -> list:
    """Charge l'historique des runs précédents."""
    chemin = Path(dossier) / "historique.json"
    if chemin.exists():
        with open(chemin, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def generer_html(donnees: dict, historique: list) -> str:
    """Génère le code HTML du dashboard."""
    resume = donnees["resume"]
    resultats = donnees["resultats"]

    # Préparer les données pour les graphiques
    tests_html = ""
    for r in resultats:
        statut_class = "pass" if r["statut"] == "PASS" else "fail"
        statut_icon = "✅" if r["statut"] == "PASS" else "❌"
        erreurs_html = ""
        if r["erreurs"]:
            erreurs_list = "".join(f"<li>{e}</li>" for e in r["erreurs"])
            erreurs_html = f'<ul class="erreurs">{erreurs_list}</ul>'

        tests_html += f"""
        <div class="test-card {statut_class}">
            <div class="test-header">
                <span class="test-icon">{statut_icon}</span>
                <span class="test-nom">{r['nom']}</span>
                <span class="test-badge {statut_class}">{r['statut']}</span>
            </div>
            <div class="test-details">
                <span class="method-badge">{r['methode']}</span>
                <span class="test-url">{r['url']}</span>
            </div>
            <div class="test-metrics">
                <span>Status: <strong>{r['status_code']}</strong></span>
                <span>Temps: <strong>{r['temps_reponse']}s</strong></span>
            </div>
            {erreurs_html}
        </div>
        """

    # Données historique pour le graphique
    hist_labels = []
    hist_taux = []
    hist_temps = []
    for h in historique[-10:]:
        date_str = h.get("date", "")
        try:
            dt = datetime.fromisoformat(date_str)
            hist_labels.append(dt.strftime("%d/%m %H:%M"))
        except (ValueError, TypeError):
            hist_labels.append("?")
        hist_taux.append(h.get("taux_reussite", 0))
        hist_temps.append(h.get("temps_moyen", 0))

    taux = resume["taux_reussite"]
    if taux >= 80:
        taux_color = "#22c55e"
    elif taux >= 50:
        taux_color = "#f59e0b"
    else:
        taux_color = "#ef4444"

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TestPilot - Rapport de tests</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

        :root {{
            --bg-primary: #0a0e1a;
            --bg-card: #111827;
            --bg-card-hover: #1a2234;
            --border: #1e293b;
            --text-primary: #f1f5f9;
            --text-secondary: #94a3b8;
            --accent-green: #22c55e;
            --accent-red: #ef4444;
            --accent-amber: #f59e0b;
            --accent-blue: #3b82f6;
            --accent-purple: #8b5cf6;
            --glow-green: rgba(34, 197, 94, 0.15);
            --glow-red: rgba(239, 68, 68, 0.15);
        }}

        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        body {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
            padding: 2rem;
        }}

        .container {{
            max-width: 1100px;
            margin: 0 auto;
        }}

        /* Header */
        .header {{
            text-align: center;
            margin-bottom: 3rem;
            padding: 2rem 0;
        }}

        .header h1 {{
            font-size: 2.5rem;
            font-weight: 800;
            background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
            letter-spacing: -0.02em;
        }}

        .header .subtitle {{
            color: var(--text-secondary);
            font-size: 0.95rem;
            font-family: 'JetBrains Mono', monospace;
        }}

        /* Stats Cards */
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1rem;
            margin-bottom: 2.5rem;
        }}

        .stat-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
            transition: transform 0.2s, border-color 0.2s;
        }}

        .stat-card:hover {{
            transform: translateY(-2px);
            border-color: var(--accent-blue);
        }}

        .stat-value {{
            font-size: 2rem;
            font-weight: 800;
            font-family: 'JetBrains Mono', monospace;
        }}

        .stat-label {{
            color: var(--text-secondary);
            font-size: 0.8rem;
            margin-top: 0.3rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        /* Gauge */
        .gauge-section {{
            display: flex;
            justify-content: center;
            margin-bottom: 2.5rem;
        }}

        .gauge-container {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 2rem 4rem;
            text-align: center;
        }}

        .gauge {{
            position: relative;
            width: 180px;
            height: 180px;
            margin: 0 auto 1rem;
        }}

        .gauge svg {{
            transform: rotate(-90deg);
        }}

        .gauge-text {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 2.2rem;
            font-weight: 800;
            font-family: 'JetBrains Mono', monospace;
            color: {taux_color};
        }}

        .gauge-label {{
            color: var(--text-secondary);
            font-size: 0.85rem;
        }}

        /* Historique */
        .section-title {{
            font-size: 1.3rem;
            font-weight: 700;
            margin-bottom: 1.2rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .historique-section {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 2.5rem;
        }}

        .chart-container {{
            height: 200px;
            display: flex;
            align-items: flex-end;
            gap: 4px;
            padding: 1rem 0;
        }}

        .chart-bar-wrapper {{
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 0.4rem;
        }}

        .chart-bar {{
            width: 100%;
            max-width: 50px;
            border-radius: 6px 6px 2px 2px;
            transition: opacity 0.2s;
            position: relative;
            min-height: 8px;
        }}

        .chart-bar:hover {{
            opacity: 0.8;
        }}

        .chart-label {{
            font-size: 0.65rem;
            color: var(--text-secondary);
            font-family: 'JetBrains Mono', monospace;
            writing-mode: vertical-lr;
            transform: rotate(180deg);
            max-height: 60px;
            overflow: hidden;
        }}

        .chart-value {{
            font-size: 0.7rem;
            color: var(--text-secondary);
            font-family: 'JetBrains Mono', monospace;
        }}

        /* Tests List */
        .tests-section {{
            margin-bottom: 2rem;
        }}

        .test-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 1.2rem 1.5rem;
            margin-bottom: 0.75rem;
            transition: border-color 0.2s, background 0.2s;
        }}

        .test-card:hover {{
            background: var(--bg-card-hover);
        }}

        .test-card.pass {{
            border-left: 3px solid var(--accent-green);
        }}

        .test-card.fail {{
            border-left: 3px solid var(--accent-red);
            background: rgba(239, 68, 68, 0.03);
        }}

        .test-header {{
            display: flex;
            align-items: center;
            gap: 0.7rem;
            margin-bottom: 0.5rem;
        }}

        .test-icon {{
            font-size: 1.1rem;
        }}

        .test-nom {{
            font-weight: 600;
            flex: 1;
        }}

        .test-badge {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.7rem;
            font-weight: 700;
            padding: 0.2rem 0.6rem;
            border-radius: 20px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        .test-badge.pass {{
            background: var(--glow-green);
            color: var(--accent-green);
        }}

        .test-badge.fail {{
            background: var(--glow-red);
            color: var(--accent-red);
        }}

        .test-details {{
            display: flex;
            align-items: center;
            gap: 0.6rem;
            margin-bottom: 0.4rem;
        }}

        .method-badge {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.7rem;
            font-weight: 700;
            padding: 0.15rem 0.5rem;
            border-radius: 4px;
            background: rgba(59, 130, 246, 0.15);
            color: var(--accent-blue);
        }}

        .test-url {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
            color: var(--text-secondary);
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }}

        .test-metrics {{
            display: flex;
            gap: 1.5rem;
            font-size: 0.85rem;
            color: var(--text-secondary);
        }}

        .test-metrics strong {{
            color: var(--text-primary);
        }}

        .erreurs {{
            margin-top: 0.7rem;
            padding: 0.7rem 1rem;
            background: rgba(239, 68, 68, 0.08);
            border-radius: 6px;
            list-style: none;
        }}

        .erreurs li {{
            font-size: 0.8rem;
            color: var(--accent-red);
            padding: 0.15rem 0;
            font-family: 'JetBrains Mono', monospace;
        }}

        .erreurs li::before {{
            content: "⚠ ";
        }}

        /* Footer */
        .footer {{
            text-align: center;
            padding: 2rem 0;
            color: var(--text-secondary);
            font-size: 0.8rem;
            font-family: 'JetBrains Mono', monospace;
        }}

        @media (max-width: 768px) {{
            .stats-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
            body {{
                padding: 1rem;
            }}
            .header h1 {{
                font-size: 1.8rem;
            }}
            .gauge-container {{
                padding: 1.5rem 2rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">

        <div class="header">
            <h1>✈ TestPilot</h1>
            <div class="subtitle">Rapport généré le {datetime.now().strftime("%d/%m/%Y à %H:%M:%S")}</div>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value" style="color: var(--accent-blue)">{resume['total']}</div>
                <div class="stat-label">Tests total</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" style="color: var(--accent-green)">{resume['passes']}</div>
                <div class="stat-label">Réussis</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" style="color: var(--accent-red)">{resume['echecs']}</div>
                <div class="stat-label">Échoués</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" style="color: var(--accent-amber)">{resume['temps_moyen']}s</div>
                <div class="stat-label">Temps moyen</div>
            </div>
        </div>

        <div class="gauge-section">
            <div class="gauge-container">
                <div class="gauge">
                    <svg width="180" height="180" viewBox="0 0 180 180">
                        <circle cx="90" cy="90" r="75" fill="none" stroke="#1e293b" stroke-width="12"/>
                        <circle cx="90" cy="90" r="75" fill="none" stroke="{taux_color}"
                                stroke-width="12" stroke-linecap="round"
                                stroke-dasharray="{taux * 4.71} 471"/>
                    </svg>
                    <div class="gauge-text">{taux}%</div>
                </div>
                <div class="gauge-label">Taux de réussite</div>
            </div>
        </div>

        {"" if not historique else f'''
        <div class="historique-section">
            <div class="section-title">📈 Historique des runs</div>
            <div class="chart-container">
                {"".join(f"""
                <div class="chart-bar-wrapper">
                    <div class="chart-value">{t}%</div>
                    <div class="chart-bar" style="height: {max(t * 1.6, 8)}px; background: {'var(--accent-green)' if t >= 80 else 'var(--accent-amber)' if t >= 50 else 'var(--accent-red)'}"></div>
                    <div class="chart-label">{l}</div>
                </div>
                """ for l, t in zip(hist_labels, hist_taux))}
            </div>
        </div>
        '''}

        <div class="tests-section">
            <div class="section-title">🧪 Détail des tests</div>
            {tests_html}
        </div>

        <div class="footer">
            TestPilot v1.0 — Automatisation de tests API
        </div>
    </div>
</body>
</html>"""

    return html


def run(fichier_json: str = "results.json", fichier_html: str = "dashboard.html"):
    """Point d'entrée : charge les résultats et génère le rapport."""
    print()
    print("📊 TestPilot - Génération du rapport")
    print("=" * 50)

    donnees = charger_resultats(fichier_json)
    historique = charger_historique(str(Path(fichier_json).parent))
    html = generer_html(donnees, historique)

    with open(fichier_html, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ Rapport généré : {fichier_html}")
    print(f"💡 Ouvre ce fichier dans ton navigateur pour voir le dashboard !")
    print()


if __name__ == "__main__":
    run()
