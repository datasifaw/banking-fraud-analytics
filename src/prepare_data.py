
# ============================================================
# BANKING FRAUD ANALYTICS
# Sprint 1 - Etape 1.5
# Data Preparation Pipeline
#
# Objectif :
# - Conserver toutes les transactions
# - Valider la qualite du dataset
# - Ajouter trois colonnes techniques
# - Generer un CSV pour BigQuery
# - Ne jamais modifier le CSV original
# ============================================================

from pathlib import Path
import os
import sys
import tempfile

import numpy as np
import pandas as pd


# ============================================================
# 1. CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = PROJECT_ROOT / "data" / "creditcard.csv"

OUTPUT_FILE = (
    PROJECT_ROOT / "data" / "creditcard_prepared.csv"
)

EXPECTED_COLUMNS = (
    ["Time"]
    + [f"V{i}" for i in range(1, 29)]
    + ["Amount", "Class"]
)

TECHNICAL_COLUMNS = [
    "source_row_id",
    "is_duplicate_extra",
    "is_in_duplicate_group",
]

EXPECTED_ROWS = 284807
EXPECTED_FRAUDS = 492
EXPECTED_EXTRA_DUPLICATES = 1081
EXPECTED_ROWS_IN_DUPLICATE_GROUPS = 1854


# ============================================================
# 2. FONCTION DE VALIDATION
# ============================================================

def validate(condition, message):
    if not condition:
        raise ValueError(message)


# ============================================================
# 3. CHARGEMENT DU DATASET
# ============================================================

def load_dataset():

    print("\n[1] Chargement du fichier source...")

    validate(
        INPUT_FILE.is_file(),
        f"CSV introuvable : {INPUT_FILE}"
    )

    df = pd.read_csv(
        INPUT_FILE,
        low_memory=False
    )

    print(f"Transactions chargees : {len(df)}")
    print(f"Colonnes chargees : {len(df.columns)}")

    return df


# ============================================================
# 4. VALIDATION DU DATASET
# ============================================================

def validate_dataset(df):

    print("\n[2] Validation du schema...")

    validate(
        list(df.columns) == EXPECTED_COLUMNS,
        "Le schema des 31 colonnes est incorrect."
    )

    validate(
        len(df) == EXPECTED_ROWS,
        "Le nombre de transactions est incorrect."
    )

    print("Schema et nombre de transactions : OK")

    # Convertir ou verifier les donnees numeriques.
    # Une conversion invalide provoque une erreur.
    print("\n[3] Verification des types numeriques...")

    for column in EXPECTED_COLUMNS:

        df[column] = pd.to_numeric(
            df[column],
            errors="raise"
        )

    # Verifier les valeurs manquantes.
    validate(
        not df[EXPECTED_COLUMNS].isna().any().any(),
        "Des valeurs manquantes sont presentes."
    )

    # Verifier les valeurs infinies.
    numeric_values = df[
        EXPECTED_COLUMNS
    ].to_numpy(dtype=np.float64)

    validate(
        bool(np.isfinite(numeric_values).all()),
        "Des valeurs numeriques non finies sont presentes."
    )

    # Verifier les montants.
    validate(
        bool((df["Amount"] >= 0).all()),
        "Des montants negatifs sont presents."
    )

    # Verifier le temps.
    validate(
        bool((df["Time"] >= 0).all()),
        "Des valeurs Time negatives sont presentes."
    )

    # Verifier les classes de fraude.
    validate(
        bool(df["Class"].isin([0, 1]).all()),
        "Class doit contenir uniquement 0 ou 1."
    )

    fraud_count = int(
        df["Class"].eq(1).sum()
    )

    validate(
        fraud_count == EXPECTED_FRAUDS,
        "Le nombre de fraudes ne correspond pas."
    )

    print("Types numeriques : OK")
    print("Valeurs manquantes : 0")
    print("Valeurs infinies : 0")
    print(f"Transactions frauduleuses : {fraud_count}")

    return df


# ============================================================
# 5. ANALYSE ET ENRICHISSEMENT
# ============================================================

def enrich_dataset(df):

    print("\n[4] Ajout des colonnes techniques...")

    # IMPORTANT :
    # La detection des doublons utilise exclusivement
    # les 31 colonnes originales.
    #
    # Elle doit etre effectuee AVANT l'ajout de
    # source_row_id.

    extra_duplicate_mask = df.duplicated(
        subset=EXPECTED_COLUMNS,
        keep="first"
    )

    duplicate_group_mask = df.duplicated(
        subset=EXPECTED_COLUMNS,
        keep=False
    )

    extra_duplicate_count = int(
        extra_duplicate_mask.sum()
    )

    duplicate_group_rows = int(
        duplicate_group_mask.sum()
    )

    validate(
        extra_duplicate_count == EXPECTED_EXTRA_DUPLICATES,
        "Le nombre de doublons supplementaires est incorrect."
    )

    validate(
        duplicate_group_rows
        == EXPECTED_ROWS_IN_DUPLICATE_GROUPS,
        "Le nombre de lignes dans les groupes repetes est incorrect."
    )

    # ID technique base sur l'ordre du CSV.
    # 1 = premiere transaction, hors ligne d'en-tete.
    # Ce n'est pas un identifiant bancaire.
    df["source_row_id"] = range(
        1,
        len(df) + 1
    )

    # True uniquement pour les occurrences
    # supplementaires d'une ligne deja presente.
    df["is_duplicate_extra"] = (
        extra_duplicate_mask
    )

    # True pour toutes les lignes d'un groupe repete,
    # y compris la premiere occurrence.
    df["is_in_duplicate_group"] = (
        duplicate_group_mask
    )

    # Reorganiser explicitement les colonnes.
    final_columns = (
        EXPECTED_COLUMNS + TECHNICAL_COLUMNS
    )

    df = df[final_columns]

    print("Colonnes techniques ajoutees : 3")
    print(f"Doublons supplementaires : {extra_duplicate_count}")
    print(f"Lignes en groupes repetes : {duplicate_group_rows}")

    return df


# ============================================================
# 6. CONTROLES FINAUX AVANT EXPORT
# ============================================================

def validate_prepared_dataset(df):

    print("\n[5] Validation finale...")

    validate(
        len(df) == EXPECTED_ROWS,
        "Des transactions ont ete perdues."
    )

    validate(
        len(df.columns) == 34,
        "Le nombre final de colonnes est incorrect."
    )

    validate(
        list(df.columns)
        == EXPECTED_COLUMNS + TECHNICAL_COLUMNS,
        "L'ordre final des colonnes est incorrect."
    )

    validate(
        int(df["Class"].eq(1).sum())
        == EXPECTED_FRAUDS,
        "Le nombre de fraudes a change."
    )

    validate(
        int(df["is_duplicate_extra"].sum())
        == EXPECTED_EXTRA_DUPLICATES,
        "Les indicateurs de doublons sont incorrects."
    )

    validate(
        int(df["is_in_duplicate_group"].sum())
        == EXPECTED_ROWS_IN_DUPLICATE_GROUPS,
        "Les indicateurs de groupes sont incorrects."
    )

    validate(
        bool(df["source_row_id"].is_unique),
        "Les identifiants techniques ne sont pas uniques."
    )

    validate(
        int(df["source_row_id"].iloc[0]) == 1
        and int(df["source_row_id"].iloc[-1])
        == EXPECTED_ROWS,
        "La numerotation technique est incorrecte."
    )

    print("Toutes les validations sont reussies.")

    return True


# ============================================================
# 7. EXPORT CSV SECURISE
# ============================================================

def export_dataset(df):

    print("\n[6] Export du dataset prepare...")

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    temporary_path = None

    try:

        # Fichier temporaire dans le meme dossier.
        # Il sera remplace atomiquement une fois
        # son ecriture terminee.

        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="",
            suffix=".csv",
            prefix="creditcard_prepared_temp_",
            dir=OUTPUT_FILE.parent,
            delete=False
        ) as temporary_file:

            temporary_path = Path(
                temporary_file.name
            )

            # 17 chiffres significatifs permettent
            # de representer les float64 sans perte
            # de precision binaire au format decimal.
            df.to_csv(
                temporary_file,
                index=False,
                float_format="%.17g"
            )

        validate(
            temporary_path.is_file()
            and temporary_path.stat().st_size > 0,
            "Le fichier temporaire est vide."
        )

        # Remplace uniquement le CSV prepare.
        # Le CSV original reste intact.
        os.replace(
            temporary_path,
            OUTPUT_FILE
        )

        temporary_path = None

    finally:

        # Nettoyage en cas d'echec.
        if (
            temporary_path is not None
            and temporary_path.exists()
        ):
            temporary_path.unlink()

    print("Export termine.")
    print(f"Fichier : {OUTPUT_FILE}")

    return OUTPUT_FILE


# ============================================================
# 8. PIPELINE PRINCIPAL
# ============================================================

def main():

    print("=" * 55)
    print("BANKING FRAUD ANALYTICS")
    print("DATA PREPARATION PIPELINE")
    print("=" * 55)

    try:

        # Chargement
        df = load_dataset()

        # Validation
        df = validate_dataset(df)

        # Enrichissement
        df = enrich_dataset(df)

        # Controle final
        validate_prepared_dataset(df)

        # Export
        output_path = export_dataset(df)

        # Resultats
        print("\n" + "=" * 55)
        print("RESULTATS DATA PREPARATION")
        print("=" * 55)

        print(f"Transactions : {len(df)}")
        print(f"Colonnes : {len(df.columns)}")

        print(
            "Transactions legitimes : "
            f"{int(df['Class'].eq(0).sum())}"
        )

        print(
            "Transactions frauduleuses : "
            f"{int(df['Class'].eq(1).sum())}"
        )

        print(
            "Doublons supplementaires conserves : "
            f"{int(df['is_duplicate_extra'].sum())}"
        )

        print(
            "Lignes dans les groupes repetes : "
            f"{int(df['is_in_duplicate_group'].sum())}"
        )

        size_mib = (
            output_path.stat().st_size / (1024 ** 2)
        )

        print(
            f"Taille CSV prepare : {size_mib:.2f} MiB"
        )

        print(f"Fichier prepare : {output_path}")
        print("CSV original : NON MODIFIE")
        print("Statut : SUCCESS")

        return 0

    except Exception as error:

        print("\nERREUR DATA PREPARATION")
        print(
            f"{type(error).__name__}: {error}"
        )

        return 1


# ============================================================
# 9. POINT D'ENTREE
# ============================================================

if __name__ == "__main__":
    sys.exit(main())
