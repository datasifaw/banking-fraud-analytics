
from pathlib import Path
import json
import sys

try:
    import pandas as pd
except ImportError:
    print("ERREUR : pandas n'est pas installé dans cet environnement Python.")
    sys.exit(1)


# =====================================================
# BANKING FRAUD ANALYTICS
# SPRINT 1 - DATA QUALITY
# =====================================================

EXPECTED_COLUMNS = (
    ["Time"]
    + [f"V{i}" for i in range(1, 29)]
    + ["Amount", "Class"]
)


def main():

    # -------------------------------------------------
    # 1. Chemins du projet
    # -------------------------------------------------

    project_root = Path(__file__).resolve().parent.parent

    csv_path = project_root / "data" / "creditcard.csv"

    report_path = (
        project_root / "data" / "data_quality_report.json"
    )

    print("\n========================================")
    print("BANKING FRAUD ANALYTICS")
    print("DATA QUALITY CHECK")
    print("========================================")

    # -------------------------------------------------
    # 2. Vérifier le fichier source
    # -------------------------------------------------

    if not csv_path.is_file():
        print(f"ERREUR : fichier introuvable : {csv_path}")
        return 1

    print("\n[1] Lecture du dataset...")

    try:
        df = pd.read_csv(csv_path, low_memory=False)

    except (
        OSError,
        UnicodeError,
        pd.errors.ParserError,
    ) as error:

        print(f"ERREUR : lecture CSV impossible : {error}")
        return 1

    print("Dataset chargé.")

    # -------------------------------------------------
    # 3. Vérifier la structure
    # -------------------------------------------------

    print("\n[2] Vérification du schéma...")

    actual_columns = list(df.columns)

    if actual_columns != EXPECTED_COLUMNS:

        print("ERREUR : structure CSV incorrecte.")
        print("Colonnes trouvées :", actual_columns)
        print("Colonnes attendues :", EXPECTED_COLUMNS)

        return 1

    print("Structure des 31 colonnes : OK")

    total_rows = len(df)
    total_columns = len(df.columns)

    # -------------------------------------------------
    # 4. Conversion numérique pour les contrôles
    # -------------------------------------------------

    numeric_data = df.apply(
        pd.to_numeric,
        errors="coerce"
    )

    # -------------------------------------------------
    # 5. Valeurs manquantes
    # -------------------------------------------------

    print("\n[3] Vérification des valeurs manquantes...")

    missing_mask = df.isna()

    missing_by_column = {
        column: int(count)
        for column, count in missing_mask.sum().items()
    }

    total_missing = int(
        missing_mask.to_numpy().sum()
    )

    # -------------------------------------------------
    # 6. Valeurs numériques invalides
    # -------------------------------------------------

    print("\n[4] Vérification des valeurs numériques...")

    non_numeric_values = int(
        (
            numeric_data.isna() & ~missing_mask
        ).to_numpy().sum()
    )

    infinite_values = int(
        numeric_data.isin(
            [float("inf"), float("-inf")]
        ).to_numpy().sum()
    )

    # -------------------------------------------------
    # 7. Transactions dupliquées
    # -------------------------------------------------

    print("\n[5] Recherche des doublons...")

    duplicate_rows = int(
        df.duplicated().sum()
    )

    # -------------------------------------------------
    # 8. Montants et temps négatifs
    # -------------------------------------------------

    print("\n[6] Vérification des montants...")

    negative_amounts = int(
        (numeric_data["Amount"] < 0).sum()
    )

    negative_times = int(
        (numeric_data["Time"] < 0).sum()
    )

    # -------------------------------------------------
    # 9. Vérifier la classification des fraudes
    # -------------------------------------------------

    print("\n[7] Analyse des classes de fraude...")

    class_values = numeric_data["Class"]

    valid_class_mask = class_values.isin([0, 1])

    invalid_classes = int(
        (~valid_class_mask).sum()
    )

    legitimate_count = int(
        (class_values == 0).sum()
    )

    fraud_count = int(
        (class_values == 1).sum()
    )

    classified_count = legitimate_count + fraud_count

    if classified_count > 0:

        fraud_rate = round(
            fraud_count / classified_count * 100,
            4
        )

    else:
        fraud_rate = None

    # -------------------------------------------------
    # 10. Identifier les anomalies
    # -------------------------------------------------

    errors = []
    warnings = []

    if total_missing > 0:
        errors.append("Valeurs manquantes détectées")

    if non_numeric_values > 0:
        errors.append("Valeurs non numériques détectées")

    if infinite_values > 0:
        errors.append("Valeurs infinies détectées")

    if invalid_classes > 0:
        errors.append("Classes de fraude invalides")

    if negative_amounts > 0:
        errors.append("Montants négatifs détectés")

    if negative_times > 0:
        errors.append("Temps négatifs détectés")

    if duplicate_rows > 0:
        warnings.append(
            "Doublons à analyser avant toute suppression"
        )

    if errors:
        quality_status = "ERROR"

    elif warnings:
        quality_status = "WARNING"

    else:
        quality_status = "OK"

    # -------------------------------------------------
    # 11. Construire le rapport qualité
    # -------------------------------------------------

    report = {

        "dataset": "data/creditcard.csv",

        "transactions": total_rows,

        "columns": total_columns,

        "missing_values": total_missing,

        "missing_by_column": missing_by_column,

        "non_numeric_values": non_numeric_values,

        "infinite_values": infinite_values,

        "duplicate_rows": duplicate_rows,

        "negative_amounts": negative_amounts,

        "negative_times": negative_times,

        "invalid_class_values": invalid_classes,

        "legitimate_transactions": legitimate_count,

        "fraudulent_transactions": fraud_count,

        "fraud_rate_pct_among_valid_classes": fraud_rate,

        "errors": errors,

        "warnings": warnings,

        "status": quality_status

    }

    # -------------------------------------------------
    # 12. Enregistrer le rapport JSON
    # -------------------------------------------------

    report_path.write_text(
        json.dumps(
            report,
            indent=2,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )

    # -------------------------------------------------
    # 13. Afficher les résultats
    # -------------------------------------------------

    print("\n========================================")
    print("RESULTATS DATA QUALITY")
    print("========================================")

    print(f"Transactions : {total_rows}")
    print(f"Colonnes : {total_columns}")

    print(f"Valeurs manquantes : {total_missing}")

    print(f"Valeurs non numériques : {non_numeric_values}")

    print(f"Valeurs infinies : {infinite_values}")

    print(f"Doublons : {duplicate_rows}")

    print(f"Montants négatifs : {negative_amounts}")

    print(f"Temps négatifs : {negative_times}")

    print(f"Classes invalides : {invalid_classes}")

    print(f"Transactions légitimes : {legitimate_count}")

    print(f"Transactions frauduleuses : {fraud_count}")

    print(f"Taux de fraude (%) : {fraud_rate}")

    print(f"Statut qualité : {quality_status}")

    print("\nRapport enregistré :")
    print(report_path)

    for message in errors:
        print(f"ERREUR : {message}")

    for message in warnings:
        print(f"ATTENTION : {message}")

    print("\nAnalyse terminée.")

    return 1 if errors else 0


# =====================================================
# POINT D'ENTREE
# =====================================================

if __name__ == "__main__":
    sys.exit(main())
