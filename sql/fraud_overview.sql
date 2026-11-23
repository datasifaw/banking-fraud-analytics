
-- ============================================================
-- BANKING FRAUD ANALYTICS
-- Sprint 3 - Etape 3.1
--
-- Fichier : sql/fraud_overview.sql
-- Objectif : Analyse globale de la fraude bancaire
--
-- Projet  : banking-fraud-analytics-515016
-- Dataset : banking_fraud
-- Table   : transactions
-- Region  : EU
--
-- Requete en lecture seule
-- ============================================================

SELECT

    -- 1. Nombre total de transactions
    COUNT(*) AS total_transactions,

    -- 2. Nombre de transactions legitimes
    COUNTIF(Class = 0) AS legitimate_transactions,

    -- 3. Nombre de transactions frauduleuses
    COUNTIF(Class = 1) AS fraudulent_transactions,

    -- 4. Taux de fraude en pourcentage
    ROUND(
        SAFE_DIVIDE(
            100.0 * COUNTIF(Class = 1),
            COUNT(*)
        ),
        4
    ) AS fraud_rate_pct,

    -- 5. Taux de transactions legitimes
    ROUND(
        SAFE_DIVIDE(
            100.0 * COUNTIF(Class = 0),
            COUNT(*)
        ),
        4
    ) AS legitimate_rate_pct,

    -- 6. Verification des classes invalides
    COUNTIF(
        Class IS NULL
        OR Class NOT IN (0, 1)
    ) AS invalid_class_values

FROM
    `banking-fraud-analytics-515016.banking_fraud.transactions`;


