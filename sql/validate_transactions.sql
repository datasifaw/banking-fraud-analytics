
-- ============================================================
-- BANKING FRAUD ANALYTICS
-- Sprint 2 - Etape 2.3.7
--
-- Fichier : sql/validate_transactions.sql
--
-- Objectif :
-- Valider les transactions importees dans Google BigQuery.
--
-- Projet  : banking-fraud-analytics-515016
-- Dataset : banking_fraud
-- Table   : transactions
-- Region  : EU
--
-- Cette requete est en lecture seule.
-- Elle ne modifie aucune donnee ni aucune table.
-- ============================================================


-- ============================================================
-- 1. VERIFICATION DU VOLUME DES TRANSACTIONS
-- ============================================================

-- Total attendu : 284807 transactions


-- ============================================================
-- 2. VERIFICATION DES CLASSES DE FRAUDE
-- ============================================================

-- Transactions legitimes attendues : 284315
-- Transactions frauduleuses attendues : 492


-- ============================================================
-- 3. VERIFICATION DES DOUBLONS
-- ============================================================

-- Doublons supplementaires attendus : 1081
-- Lignes dans les groupes repetes attendues : 1854


-- ============================================================
-- 4. VERIFICATION DES IDENTIFIANTS TECHNIQUES
-- ============================================================

-- Identifiants uniques attendus : 284807
-- Premier identifiant attendu : 1
-- Dernier identifiant attendu : 284807


-- ============================================================
-- 5. VERIFICATION DU TAUX DE FRAUDE
-- ============================================================

-- Taux de fraude attendu : 0.1727 %


-- ============================================================
-- 6. VERIFICATION DE COHERENCE DES INDICATEURS
-- ============================================================

-- Incoherences attendues : 0
--
-- Une ligne marquee comme doublon supplementaire
-- doit obligatoirement appartenir a un groupe repete.


-- ============================================================
-- REQUETE PRINCIPALE DE VALIDATION
-- ============================================================

SELECT

    -- Nombre total de transactions
    COUNT(*) AS total_transactions,

    -- Repartition par classe
    COUNTIF(Class = 0) AS legitimate_transactions,

    COUNTIF(Class = 1) AS fraudulent_transactions,

    -- Doublons supplementaires conserves
    COUNTIF(
        is_duplicate_extra
    ) AS extra_duplicate_rows,

    -- Ensemble des lignes appartenant
    -- a des groupes repetes
    COUNTIF(
        is_in_duplicate_group
    ) AS rows_in_duplicate_groups,

    -- Verification des identifiants techniques
    COUNT(
        DISTINCT source_row_id
    ) AS unique_source_row_ids,

    MIN(
        source_row_id
    ) AS min_source_row_id,

    MAX(
        source_row_id
    ) AS max_source_row_id,

    -- Pourcentage des transactions frauduleuses
    ROUND(
        SAFE_DIVIDE(
            COUNTIF(Class = 1) * 100,
            COUNT(*)
        ),
        4
    ) AS fraud_rate_pct,

    -- Controle de coherence des indicateurs
    COUNTIF(
        is_duplicate_extra
        AND NOT is_in_duplicate_group
    ) AS inconsistent_duplicate_flags

FROM
    `banking-fraud-analytics-515016.banking_fraud.transactions`;


