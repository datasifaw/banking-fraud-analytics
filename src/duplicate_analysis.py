
from pathlib import Path
import json
import sys

try:
    import pandas as pd
except ImportError:
    print("ERREUR : pandas n'est pas installe.")
    sys.exit(1)


# =====================================================
# BANKING FRAUD ANALYTICS
# SPRINT 1 - ETAPE 1.4
# ANALYSE DETAILLEE DES DOUBLONS
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CSV_PATH = PROJECT_ROOT / "data" / "creditcard.csv"

REPORT_PATH = (
    PROJECT_ROOT / "data" / "duplicate_analysis_report.json"
)

EXPECTED_COLUMNS = (
    ["Time"]
    + [f"V{i}" for i in range(1, 29)]
    + ["Amount", "Class"]
)


def percentage(numerator, denominator):
    if denominator == 0:
        return 0.0

    return round(100 * numerator / denominator, 4)


def main():

    print("=" * 55)
    print("BANKING FRAUD ANALYTICS")
    print("ANALYSE DETAILLEE DES DOUBLONS")
    print("=" * 55)

    # -------------------------------------------------
    # 1. Verification du fichier
    # -------------------------------------------------

    if not CSV_PATH.is_file():
        print("ERREUR : creditcard.csv introuvable.")
        return 1

    print("\n[1] Chargement du dataset...")

    try:
        df = pd.read_csv(
            CSV_PATH,
            low_memory=False
        )
    except Exception as error:
        print(f"ERREUR de lecture : {error}")
        return 1

    # -------------------------------------------------
    # 2. Verification du schema
    # -------------------------------------------------

    if list(df.columns) != EXPECTED_COLUMNS:
        print("ERREUR : structure des colonnes incorrecte.")
        return 1

    if not df["Class"].isin([0, 1]).all():
        print("ERREUR : valeurs de Class invalides.")
        return 1

    print("Dataset charge et schema valide.")

    total = len(df)

    fraud_count = int((df["Class"] == 1).sum())
    legitimate_count = int((df["Class"] == 0).sum())

    original_fraud_rate = percentage(
        fraud_count,
        total
    )

    # -------------------------------------------------
    # 3. Detecter les lignes supplementaires dupliquees
    # -------------------------------------------------

    print("\n[2] Detection des doublons...")

    # Conserve implicitement la premiere occurrence.
    # Les autres occurrences sont marquees True.
    extra_duplicate_mask = df.duplicated(
        keep="first"
    )

    extra_duplicates = int(
        extra_duplicate_mask.sum()
    )

    # Cette mesure inclut toutes les lignes appartenant
    # aux groupes repetes, premiere occurrence comprise.
    all_duplicate_mask = df.duplicated(
        keep=False
    )

    rows_in_duplicate_groups = int(
        all_duplicate_mask.sum()
    )

    duplicate_percentage = percentage(
        extra_duplicates,
        total
    )

    # -------------------------------------------------
    # 4. Doublons par classe
    # -------------------------------------------------

    print("\n[3] Repartition par classe de fraude...")

    legitimate_duplicates = int(
        (
            extra_duplicate_mask
            & df["Class"].eq(0)
        ).sum()
    )

    fraud_duplicates = int(
        (
            extra_duplicate_mask
            & df["Class"].eq(1)
        ).sum()
    )

    legitimate_rows_in_groups = int(
        (
            all_duplicate_mask
            & df["Class"].eq(0)
        ).sum()
    )

    fraud_rows_in_groups = int(
        (
            all_duplicate_mask
            & df["Class"].eq(1)
        ).sum()
    )

    # -------------------------------------------------
    # 5. Identifier les groupes de doublons
    # -------------------------------------------------

    print("\n[4] Analyse des groupes repetes...")

    # On groupe uniquement les lignes deja detectees
    # comme appartenant a un groupe de doublons.
    repeated_rows = df.loc[all_duplicate_mask]

    if repeated_rows.empty:
        duplicate_groups = pd.DataFrame(
            columns=EXPECTED_COLUMNS + ["occurrences"]
        )
    else:
        duplicate_groups = (
            repeated_rows
            .groupby(
                EXPECTED_COLUMNS,
                dropna=False,
                sort=False
            )
            .size()
            .reset_index(name="occurrences")
        )

    group_count = len(duplicate_groups)

    max_occurrences = (
        int(duplicate_groups["occurrences"].max())
        if group_count > 0
        else 0
    )

    legitimate_groups = int(
        (duplicate_groups["Class"] == 0).sum()
    )

    fraud_groups = int(
        (duplicate_groups["Class"] == 1).sum()
    )

    # Nombre de groupes pour chaque multiplicite.
    multiplicity_counts = (
        duplicate_groups["occurrences"]
        .value_counts()
        .sort_index()
    )

    repetitions = {
        str(int(count)): int(groups)
        for count, groups in multiplicity_counts.items()
    }

    # -------------------------------------------------
    # 6. Simulation theorique de suppression
    # -------------------------------------------------

    print("\n[5] Simulation sans suppression reelle...")

    hypothetical_total = total - extra_duplicates

    hypothetical_legitimate = (
        legitimate_count - legitimate_duplicates
    )

    hypothetical_fraud = (
        fraud_count - fraud_duplicates
    )

    hypothetical_fraud_rate = percentage(
        hypothetical_fraud,
        hypothetical_total
    )

    fraud_rate_difference = round(
        hypothetical_fraud_rate - original_fraud_rate,
        4
    )

    # -------------------------------------------------
    # 7. Rapport JSON agrege
    # -------------------------------------------------

    report = {
        "project": "Banking Fraud Analytics",
        "analysis": "Duplicate Analysis",
        "source": "data/creditcard.csv",

        "original_dataset": {
            "total_transactions": total,
            "legitimate_transactions": legitimate_count,
            "fraudulent_transactions": fraud_count,
            "fraud_rate_pct": original_fraud_rate
        },

        "duplicate_analysis": {
            "extra_duplicate_rows": extra_duplicates,
            "duplicate_percentage": duplicate_percentage,
            "rows_in_duplicate_groups": rows_in_duplicate_groups,
            "duplicate_group_count": group_count,
            "maximum_group_occurrences": max_occurrences,
            "group_multiplicity_distribution": repetitions
        },

        "duplicates_by_class": {
            "legitimate_extra_duplicates":
                legitimate_duplicates,

            "fraudulent_extra_duplicates":
                fraud_duplicates,

            "legitimate_rows_in_duplicate_groups":
                legitimate_rows_in_groups,

            "fraudulent_rows_in_duplicate_groups":
                fraud_rows_in_groups,

            "legitimate_duplicate_groups":
                legitimate_groups,

            "fraudulent_duplicate_groups":
                fraud_groups
        },

        "hypothetical_deduplication": {
            "transactions_after_dedup":
                hypothetical_total,

            "legitimate_after_dedup":
                hypothetical_legitimate,

            "fraudulent_after_dedup":
                hypothetical_fraud,

            "fraud_rate_after_dedup_pct":
                hypothetical_fraud_rate,

            "fraud_rate_difference_percentage_points":
                fraud_rate_difference
        },

        "source_csv_modified": False,

        "note": (
            "Simulation only. Duplicate rows were not "
            "removed. Identical anonymized records "
            "are not necessarily duplicate transactions."
        )
    }

    # Verification de coherence
    assert (
        legitimate_duplicates + fraud_duplicates
        == extra_duplicates
    )

    assert (
        hypothetical_legitimate + hypothetical_fraud
        == hypothetical_total
    )

    assert (
        int(
            (
                duplicate_groups["occurrences"] - 1
            ).sum()
        )
        == extra_duplicates
    )

    # Enregistre uniquement des statistiques agregees.
    # Aucune transaction individuelle n'est exportee.
    REPORT_PATH.write_text(
        json.dumps(
            report,
            indent=2,
            ensure_ascii=True
        ),
        encoding="utf-8"
    )

    # -------------------------------------------------
    # 8. Resultats dans le terminal
    # -------------------------------------------------

    print("\n" + "=" * 55)
    print("RESULTATS DUPLICATE ANALYSIS")
    print("=" * 55)

    print(f"Total transactions : {total}")
    print(f"Fraudes originales : {fraud_count}")

    print(f"\nDoublons supplementaires : {extra_duplicates}")
    print(f"Taux de doublons (%) : {duplicate_percentage}")

    print(
        "Lignes dans des groupes dupliques : "
        f"{rows_in_duplicate_groups}"
    )

    print(f"Nombre de groupes dupliques : {group_count}")

    print(
        "Nombre maximal d'occurrences d'un groupe : "
        f"{max_occurrences}"
    )

    print("\n--- DOUBLONS PAR CLASSE ---")

    print(
        f"Doublons legitimes : {legitimate_duplicates}"
    )

    print(
        f"Doublons frauduleux : {fraud_duplicates}"
    )

    print(
        f"Groupes legitimes dupliques : {legitimate_groups}"
    )

    print(
        f"Groupes frauduleux dupliques : {fraud_groups}"
    )

    print("\n--- FREQUENCES DES REPETITIONS ---")

    for occurrences, groups in repetitions.items():
        print(
            f"{occurrences} occurrences : {groups} groupes"
        )

    print("\n--- IMPACT HYPOTHETIQUE ---")

    print(
        f"Taux de fraude original (%) : "
        f"{original_fraud_rate}"
    )

    print(
        f"Taux de fraude apres deduplication (%) : "
        f"{hypothetical_fraud_rate}"
    )

    print(
        "Variation en points de pourcentage : "
        f"{fraud_rate_difference}"
    )

    print("\nAUCUNE LIGNE DU CSV N'A ETE SUPPRIMEE.")
    print(f"Rapport local : {REPORT_PATH}")

    print("\nANALYSE TERMINEE")

    return 0


if __name__ == "__main__":
    sys.exit(main())
