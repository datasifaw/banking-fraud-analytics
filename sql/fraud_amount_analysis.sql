
-- ============================================================
-- BANKING FRAUD ANALYTICS
-- Sprint 3 - Etape 3.2
--
-- Fichier : sql/fraud_amount_analysis.sql
-- Objectif : analyser les montants des transactions
--
-- Projet  : banking-fraud-analytics-515016
-- Dataset : banking_fraud
-- Table   : transactions
-- Region  : EU
--
-- Requete en lecture seule : SELECT uniquement.
-- Aucune transaction supprimee.
-- Les doublons sont conserves.
-- ============================================================


-- ============================================================
-- 1. PREPARATION DES MONTANTS ET CALCUL DES MEDIANES
-- ============================================================

WITH transactions_with_median AS (

    SELECT
        Class,
        Amount,

        -- Mediane exacte calculee separement
        -- pour chaque classe de transaction.
        PERCENTILE_CONT(
            Amount,
            0.5
        ) OVER (
            PARTITION BY Class
        ) AS median_amount

    FROM
        `banking-fraud-analytics-515016.banking_fraud.transactions`

    WHERE
        Class IN (0, 1)

),


-- ============================================================
-- 2. CALCUL DES INDICATEURS PAR CLASSE
-- ============================================================

amount_by_class AS (

    SELECT
        Class,

        COUNT(*) AS transaction_count,

        SUM(Amount) AS total_amount,

        AVG(Amount) AS average_amount,

        MAX(median_amount) AS median_amount,

        MIN(Amount) AS minimum_amount,

        MAX(Amount) AS maximum_amount

    FROM
        transactions_with_median

    GROUP BY
        Class

)


-- ============================================================
-- 3. RESULTATS DE L'ANALYSE
-- ============================================================

SELECT

    CASE
        WHEN Class = 0 THEN 'legitimate'
        WHEN Class = 1 THEN 'fraudulent'
    END AS transaction_class,

    -- Nombre de transactions
    transaction_count,

    -- Montant total
    ROUND(
        total_amount,
        2
    ) AS total_amount,

    -- Montant moyen
    ROUND(
        average_amount,
        2
    ) AS average_amount,

    -- Montant median
    ROUND(
        median_amount,
        2
    ) AS median_amount,

    -- Montant minimum
    ROUND(
        minimum_amount,
        2
    ) AS minimum_amount,

    -- Montant maximum
    ROUND(
        maximum_amount,
        2
    ) AS maximum_amount,

    -- Pourcentage du montant total
    -- represente par cette classe
    ROUND(
        100.0 * SAFE_DIVIDE(
            total_amount,
            SUM(total_amount) OVER ()
        ),
        4
    ) AS amount_share_pct

FROM
    amount_by_class

ORDER BY
    Class;



