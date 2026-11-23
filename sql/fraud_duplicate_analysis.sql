
-- ============================================================
-- BANKING FRAUD ANALYTICS
-- Sprint 3 - Etape 3.4
--
-- Fichier : sql/fraud_duplicate_analysis.sql
-- Objectif : analyser les doublons et leur impact
--
-- Projet  : banking-fraud-analytics-515016
-- Dataset : banking_fraud
-- Table   : transactions
-- Region  : EU
--
-- Requete SELECT en lecture seule.
-- Aucune suppression ni modification de transactions.
--
-- Les calculs utilisent les indicateurs de doublons
-- crees et valides pendant le Sprint 1.
-- ============================================================


-- ============================================================
-- 1. INDICATEURS DE BASE
-- ============================================================

WITH duplicate_summary AS (

    SELECT

        COUNT(*) AS total_transactions,

        COUNTIF(
            Class = 0
        ) AS legitimate_transactions,

        COUNTIF(
            Class = 1
        ) AS fraudulent_transactions,

        COUNTIF(
            is_duplicate_extra
        ) AS extra_duplicate_rows,

        COUNTIF(
            is_in_duplicate_group
        ) AS rows_in_duplicate_groups,

        COUNTIF(
            Class = 0
            AND is_duplicate_extra
        ) AS legitimate_extra_duplicates,

        COUNTIF(
            Class = 1
            AND is_duplicate_extra
        ) AS fraudulent_extra_duplicates,

        COUNTIF(
            Class = 0
            AND is_in_duplicate_group
        ) AS legitimate_rows_in_duplicate_groups,

        COUNTIF(
            Class = 1
            AND is_in_duplicate_group
        ) AS fraudulent_rows_in_duplicate_groups,

        COUNTIF(
            is_duplicate_extra
            AND NOT is_in_duplicate_group
        ) AS inconsistent_duplicate_flags

    FROM
        `banking-fraud-analytics-515016.banking_fraud.transactions`

)


-- ============================================================
-- 2. ANALYSE DES DOUBLONS ET SIMULATION
-- ============================================================

SELECT

    total_transactions,

    -- Doublons supplementaires
    extra_duplicate_rows,

    ROUND(
        100.0 * SAFE_DIVIDE(
            extra_duplicate_rows,
            total_transactions
        ),
        4
    ) AS duplicate_rate_pct,

    -- Lignes appartenant a des groupes repetes
    rows_in_duplicate_groups,

    -- Un groupe de m lignes contient m - 1
    -- doublons supplementaires.
    rows_in_duplicate_groups
        - extra_duplicate_rows
        AS duplicate_group_count,

    -- Repartition des doublons par classe
    legitimate_extra_duplicates,

    fraudulent_extra_duplicates,

    -- Groupes repetes par classe
    legitimate_rows_in_duplicate_groups
        - legitimate_extra_duplicates
        AS legitimate_duplicate_groups,

    fraudulent_rows_in_duplicate_groups
        - fraudulent_extra_duplicates
        AS fraudulent_duplicate_groups,

    -- Nombre de lignes hypothetique
    -- apres suppression des occurrences supplementaires
    total_transactions
        - extra_duplicate_rows
        AS hypothetical_transactions_after_dedup,

    -- Nombre de fraudes hypothetique
    fraudulent_transactions
        - fraudulent_extra_duplicates
        AS hypothetical_frauds_after_dedup,

    -- Taux de fraude original
    ROUND(
        100.0 * SAFE_DIVIDE(
            fraudulent_transactions,
            total_transactions
        ),
        4
    ) AS original_fraud_rate_pct,

    -- Taux de fraude hypothetique apres deduplication
    ROUND(
        100.0 * SAFE_DIVIDE(
            fraudulent_transactions
                - fraudulent_extra_duplicates,
            total_transactions
                - extra_duplicate_rows
        ),
        4
    ) AS hypothetical_fraud_rate_pct,

    -- Variation en points de pourcentage
    ROUND(
        100.0 * SAFE_DIVIDE(
            fraudulent_transactions
                - fraudulent_extra_duplicates,
            total_transactions
                - extra_duplicate_rows
        )
        - 100.0 * SAFE_DIVIDE(
            fraudulent_transactions,
            total_transactions
        ),
        4
    ) AS fraud_rate_difference_pp,

    -- Verification de coherence des indicateurs
    inconsistent_duplicate_flags

FROM
    duplicate_summary;



