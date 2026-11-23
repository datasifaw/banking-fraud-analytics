
-- ============================================================
-- BANKING FRAUD ANALYTICS
-- Sprint 3 - Etape 3.3
--
-- Fichier : sql/fraud_time_analysis.sql
-- Objectif : analyser la fraude par heure relative
--
-- Projet  : banking-fraud-analytics-515016
-- Dataset : banking_fraud
-- Table   : transactions
-- Region  : EU
--
-- Requete en lecture seule.
-- Aucune transaction supprimee ou modifiee.
-- Les doublons sont conserves.
-- ============================================================


-- ============================================================
-- 1. REGROUPEMENT PAR HEURE RELATIVE
-- ============================================================

WITH hourly_summary AS (

    SELECT

        -- Time correspond au nombre de secondes
        -- ecoulees depuis la premiere transaction.
        --
        -- Heure 0 : de 0 a moins de 3600 secondes
        -- Heure 1 : de 3600 a moins de 7200 secondes
        -- Etc.

        CAST(
            FLOOR(Time / 3600.0)
            AS INT64
        ) AS relative_hour,

        -- Total des transactions
        COUNT(*) AS total_transactions,

        -- Transactions legitimes
        COUNTIF(
            Class = 0
        ) AS legitimate_transactions,

        -- Transactions frauduleuses
        COUNTIF(
            Class = 1
        ) AS fraudulent_transactions

    FROM
        `banking-fraud-analytics-515016.banking_fraud.transactions`

    GROUP BY
        relative_hour

)


-- ============================================================
-- 2. RESULTATS PAR INTERVALLE HORAIRE
-- ============================================================

SELECT

    -- Numero de l'heure relative
    relative_hour,

    -- Debut de l'intervalle en secondes
    relative_hour * 3600 AS start_second,

    -- Fin exclusive de l'intervalle
    (relative_hour + 1) * 3600 AS end_second_exclusive,

    -- Volume des transactions
    total_transactions,

    -- Transactions legitimes
    legitimate_transactions,

    -- Transactions frauduleuses
    fraudulent_transactions,

    -- Taux de fraude par heure relative
    ROUND(
        100.0 * SAFE_DIVIDE(
            fraudulent_transactions,
            total_transactions
        ),
        4
    ) AS fraud_rate_pct,

    -- Total de controle sur toutes les heures
    SUM(
        total_transactions
    ) OVER () AS overall_transactions,

    -- Total des fraudes sur toutes les heures
    SUM(
        fraudulent_transactions
    ) OVER () AS overall_frauds

FROM
    hourly_summary

ORDER BY
    relative_hour;


