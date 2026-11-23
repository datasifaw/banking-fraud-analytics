
-- ============================================================
-- BANKING FRAUD ANALYTICS
-- Sprint 3 - Etape 3.5
--
-- Fichier : sql/dashboard_kpis.sql
--
-- Objectif :
-- Preparer les KPI globaux pour Looker Studio.
--
-- Projet  : banking-fraud-analytics-515016
-- Dataset : banking_fraud
-- Table   : transactions
-- Region  : EU
--
-- Requete en lecture seule.
-- Les doublons sont conserves.
-- ============================================================

SELECT

    -- 1. Volume global
    COUNT(*) AS total_transactions,

    -- 2. Transactions legitimes
    COUNTIF(
        Class = 0
    ) AS legitimate_transactions,

    -- 3. Transactions frauduleuses
    COUNTIF(
        Class = 1
    ) AS fraudulent_transactions,

    -- 4. Taux de fraude
    ROUND(
        100.0 * SAFE_DIVIDE(
            COUNTIF(Class = 1),
            COUNT(*)
        ),
        4
    ) AS fraud_rate_pct,

    -- 5. Montant total des transactions
    ROUND(
        SUM(Amount),
        2
    ) AS total_amount,

    -- 6. Montant total des fraudes
    ROUND(
        SUM(
            IF(Class = 1, Amount, 0)
        ),
        2
    ) AS fraud_amount,

    -- 7. Part des montants frauduleux
    ROUND(
        100.0 * SAFE_DIVIDE(
            SUM(IF(Class = 1, Amount, 0)),
            SUM(Amount)
        ),
        4
    ) AS fraud_amount_share_pct,

    -- 8. Montant moyen des fraudes
    ROUND(
        AVG(
            IF(Class = 1, Amount, NULL)
        ),
        2
    ) AS average_fraud_amount,

    -- 9. Doublons supplementaires
    COUNTIF(
        is_duplicate_extra
    ) AS extra_duplicate_rows,

    -- 10. Lignes dans les groupes repetes
    COUNTIF(
        is_in_duplicate_group
    ) AS rows_in_duplicate_groups

FROM
    `banking-fraud-analytics-515016.banking_fraud.transactions`;


