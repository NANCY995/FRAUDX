══════════════════════════════════════════════════════════════
  PROMPT MAÎTRE — Rédaction complète du mémoire FRAUDX
  À copier-coller dans Codex / Claude / GPT
══════════════════════════════════════════════════════════════

CONTEXTE :
Tu es rédacteur académique spécialisé en méthodologie de recherche et détection de fraude par IA.
Tu dois produire un mémoire de Master complet (80–120 pages) à partir du plan ci-dessous.

CONSIGNES GÉNÉRALES :
- Style académique strict (Times New Roman 12, interligne 1.5, norme APA)
- Le mémoire doit D'ABORD démontrer une recherche scientifique, ENSUITE proposer une intervention technique
- Le prototype (PoC) est présenté comme UNE PROPOSITION D'INTERVENTION au service des hypothèses, PAS comme l'objectif principal
- Chaque chapitre commence par une introduction et se termine par une conclusion
- Cohérence stricte : QS1→HS1→OS1, QS2→HS2→OS2, QS3→HS3→OS3
- Tableaux numérotés : Tableau 1.1, 2.1, 3.1, 4.1...
- Figures numérotées : Figure 3.1, 3.2, 4.1...

══════════════════════════════════════════════════════════════
  INTRODUCTION GÉNÉRALE (≈8 pages)
══════════════════════════════════════════════════════════════

1.1. CONTEXTE GÉNÉRAL
- Transformation digitale du secteur bancaire en Afrique subsaharienne
- Explosion du mobile money au Togo (TogoCom Cash, Moov Money, Flooz)
- Croissance parallèle de la fraude bancaire numérique (SIM swap, USSD fraud)
- Limites des méthodes traditionnelles (règles statiques, contrôles manuels)
- Opportunité offerte par l'IA et le Machine Learning

1.2. PROBLÉMATIQUE
- Présentation du problème : les banques togolaises utilisent encore des méthodes traditionnelles, exposées à des pertes croissantes
- QUESTION GÉNÉRALE : Comment concevoir un système d'IA efficace et sécurisé pour la détection de la fraude bancaire au Togo ?
- QS1 : Quels algorithmes de ML sont les plus adaptés à la détection de fraude dans le contexte bancaire togolais ?
- QS2 : Comment assurer la sécurité des données et la conformité réglementaire lors de l'intégration d'un système d'IA dans une banque togolaise ?
- QS3 : Dans quelle mesure l'interprétabilité des modèles de ML facilite-t-elle leur adoption par les analystes financiers ?

1.3. HYPOTHÈSES
- HG : L'IA améliore la détection de fraude bancaire au Togo au-delà des méthodes traditionnelles
- HS1 : Les modèles ML (Isolation Forest, XGBoost) réduisent le taux de faux négatifs (Recall ≥ 0.85)
- HS2 : Une plateforme sécurisée avec RBAC favorise l'adoption du ML dans les banques togolaises
- HS3 : L'explicabilité SHAP facilite l'acceptation des décisions du modèle par les analystes

1.4. OBJECTIFS
- OG : Concevoir et proposer un système d'IA performant pour la détection de fraude (contexte Togo)
- OS1 : Identifier et comparer les algorithmes ML adaptés (→ QS1)
- OS2 : Proposer une architecture sécurisée avec gestion des utilisateurs (→ QS2)
- OS3 : Évaluer l'interprétabilité SHAP pour les parties prenantes (→ QS3)

Tableau intro — Matrice de cohérence : QS → HS → OS → Variables → Indicateurs → Méthode

1.5. JUSTIFICATION
- Scientifique : première étude documentée sur la détection de fraude par IA au Togo
- Pratique : réponse à un besoin des banques togolaises et des régulateurs BCEAO/UEMOA

1.6. DÉLIMITATION
- Géographique : Togo, focus Lomé
- Thématique : fraude électronique (carte, virement, mobile money) — exclut fraude fiscale et blanchiment
- Temporelle : 2019–2025 (digitalisation accélérée + croissance mobile money)

1.7. PLAN DU MÉMOIRE
Présentation des 4 chapitres (1 phrase chacun avec lien logique).

══════════════════════════════════════════════════════════════
  CHAPITRE I — CADRE THÉORIQUE ET CONCEPTUEL (≈25 pages)
══════════════════════════════════════════════════════════════

1.1. LA FRAUDE BANCAIRE : CONCEPTS ET TYPOLOGIE
- Définition de la fraude bancaire
- Classification : fraude carte, virement, mobile banking, usurpation d'identité
- SPÉCIFICITÉ MOBILE MONEY TOGO : SIM swap, fraude USSD, ingénierie sociale sur agents, fraude sur recharge
- Chiffres clés : prévalence au Togo et en Afrique de l'Ouest

1.2. MACHINE LEARNING POUR LA DÉTECTION DE FRAUDE
- Concepts fondamentaux du ML (supervisé, non supervisé, ensemble learning)
- Isolation Forest : principe (tree isolation, anomaly score), avantages pour données non labellisées
- Random Forest : principe (bagging, feature randomness), usage en classification binaire
- XGBoost : principe (gradient boosting, régularisation), standard industriel actuel
- SMOTE : principe (interpolation synthétique), justification pour données déséquilibrées
- LSTM (optionnel) : principe (memory cell, gates), usage pour séquences temporelles

1.3. EXPLICABILITÉ (XAI) DANS LES SYSTÈMES BANCAIRES
- Définition XAI, besoin réglementaire croissant (BCEAO, GDPR, lois togolaises)
- SHAP : fondements théoriques (Shapley values), TreeExplainer pour modèles arborescents
- Contribution de SHAP : identification des variables influentes par transaction, confiance analyste

1.4. CADRE LÉGAL ET RÉGLEMENTAIRE
- Réglementations BCEAO/UEMOA applicables
- Dispositifs AML/KYC et rôle du GIABA
- Loi togolaise sur la protection des données personnelles
- Exigences de transparence des décisions automatisées

⸻ TABLEAUX À PRODUIRE ⸻
- Tableau 1.1 : Synthèse des études antérieures en Afrique de l'Ouest (5 pays)
- Tableau 1.2 : Classification des types de fraude bancaire
- Tableau 1.3 : Comparaison des algorithmes (IF, RF, XGB, LSTM) — principe, avantages, limites

══════════════════════════════════════════════════════════════
  CHAPITRE II — MÉTHODOLOGIE DE L'ÉTUDE (≈20 pages)
══════════════════════════════════════════════════════════════

IMPORTANT : Ce chapitre doit montrer la rigueur scientifique. Détailler la stratégie de vérification.

2.1. NATURE DE L'ÉTUDE
- Étude prospective, approche MIXTE (quantitative + qualitative), non expérimentale
- Niveau Compréhensif — objectif : Proposer (FUNIBER, 2017)
- Justification du choix mixte : le quantitatif mesure la performance, le qualitatif valide la transférabilité au Togo

2.2. STRATÉGIE DE VÉRIFICATION (NOUVEAU — demandé par le correcteur)
- Tableau 2.1 : Matrice de vérification des hypothèses
  | Hypothèse | Source de données | Méthode | Indicateur | Seuil de confirmation |
  |---|---|---|---|---|
  | HS1 | Benchmark modèles (IF, RF, XGB) | Entraînement/test sur IEEE-CIS | F1, Recall, AUC-PR | Recall ≥ 0.85, F1 ≥ 0.80 |
  | HS2 | Entretiens (5-8 responsables) | Codage thématique | Thèmes récurrents | ≥ 60% des répondants valident |
  | HS3 | Analyse SHAP + entretiens | SHAP + codage thématique | Top-3 features SHAP, concentration | Concentration ≥ 0.5 |

2.3. VARIABLES ET INDICATEURS
- Variable INDÉPENDANTE : Type d'algorithme ML (Isolation Forest, Random Forest, XGBoost)
- Variable DÉPENDANTE : Performance de détection (F1-Score, Recall, AUC-PR, temps de traitement)
- Variable MODÉRATRICE : Interprétabilité du modèle (Score SHAP, concentration des features)
- Cadre opératoire détaillé : Tableau 2.2 — Opérationnalisation des variables

2.4. POPULATION ET ÉCHANTILLON
- Population cible : Transactions bancaires et mobile money au Togo (2020–2024)
- Échantillon quantitatif : Dataset IEEE-CIS Fraud Detection (~590K transactions, 3.5% fraude) — LIMITE ASSUMÉE (proxy international)
- Échantillon qualitatif : 5 à 8 responsables (DSI, Conformité, Risques) basés à Lomé, échantillonnage raisonné
- Justification de l'usage d'un dataset international : confidentialité bancaire, absence d'alternative publique

2.5. APPROCHE MÉTHODOLOGIQUE
- Architecture Ensemble Learning 3 niveaux : IF (filtrage) → XGBoost (classification) → LSTM optionnel (temporel)
- Pipeline : Nettoyage → Encodage → StandardScaler → SMOTE → Split 80/20 → Entraînement → SHAP
- Outils : Python, Scikit-learn, XGBoost, SHAP, Pandas, NumPy, SMOTE (imbalanced-learn)
- Volet qualitatif : Entretiens semi-directifs, codage thématique (grille en Annexe A)

2.6. MÉTRIQUES D'ÉVALUATION
- Justification du rejet de l'Accuracy sur données déséquilibrées (< 1% fraude)
- F1-Score : équilibre précision/rappel — métrique principale
- AUC-PR : plus pertinent qu'AUC-ROC (focus sur la classe minoritaire)
- Recall : taux de détection des fraudes, lié à HS1
- Latence : cible < 100 ms par transaction (temps réel)

2.7. LIMITES ET DIFFICULTÉS
- Indisponibilité des données réelles togolaises
- Déséquilibre des classes
- Accès restreint aux statistiques sectorielles
- Transférabilité à confirmer sur données locales

⸻ TABLEAUX À PRODUIRE ⸻
- Tableau 2.1 : Matrice de vérification des hypothèses
- Tableau 2.2 : Opérationnalisation des variables
- Tableau 2.3 : Architecture des modèles (3 niveaux)
- Tableau 2.4 : Profils des répondants aux entretiens

══════════════════════════════════════════════════════════════
  CHAPITRE III — PRÉSENTATION DU SYSTÈME ET DES DONNÉES (≈20 pages)
══════════════════════════════════════════════════════════════

⚠️ CADRAGE : Le PoC est une PROPOSITION D'INTERVENTION, pas un logiciel final.

3.1. PRÉSENTATION DU SECTEUR BANCAIRE TOGOLAIS
- Structure : BTCI, Orabank, UTB, Ecobank, SGBT, IMF, opérateurs mobile money (TogoCom, Moov, Flooz)
- Niveau de digitalisation et infrastructures existantes
- Résultats des entretiens : état des lieux de la fraude perçue

3.2. COLLECTE ET PRÉPARATION DES DONNÉES
- Dataset IEEE-CIS : volume (~590K), structure (~400 variables), taux fraude (3.5%)
- Analyse exploratoire (EDA) :
  - Figure 3.1 : Distribution des classes (isFraud) — barplot + camembert
  - Figure 3.2 : Valeurs manquantes par colonne
  - Figure 3.3 : Distribution du montant (échelle log)
  - Figure 3.4 : Analyse temporelle (volume et taux fraude par heure)
  - Figure 3.5 : Heatmap des corrélations
- Prétraitement : encodage fréquentiel (high-cardinality), OneHotEncoder (low-cardinality), StandardScaler, SMOTE
- Split 80/20 stratifié
- DISCUSSION : transférabilité au Togo — correspondance des variables

3.3. CONCEPTION DU MODÈLE ML
- Niveau 1 : Isolation Forest (contamination=0.035, n_estimators=200)
- Niveau 2 : XGBoost (n_estimators=200, max_depth=8, learning_rate=0.1, scale_pos_weight=ratio)
- Entraînement et validation croisée (StratifiedKFold, k=5)
- Optimisation du seuil de décision par max F1-Score
- SHAP : identification des top-10 features, exemples d'explications individuelles
  - Figure 3.6 : SHAP Summary Plot (beeswarm)
  - Figure 3.7 : SHAP Feature Importance (barres)
  - Figure 3.8 : SHAP Waterfall pour 2 transactions (fraude et normale)

3.4. PROPOSITION DE PLATEFORME (PoC)
- Schéma d'architecture technique (Figure 3.9) : 6 couches
  (Sécurité → Client → API → Pipeline ML → Ensemble Learning → XAI → Données)
- API REST (FastAPI) : endpoints /predict, /batch, /health, /logs, /feedback
- Gestion RBAC : 3 rôles (Analyste, Gestionnaire Risques, Administrateur) — Tableau 3.1
- Maquettes d'interface (Figure 3.10) : Dashboard, Analyse TX, Monitoring
- Principes de sécurité : chiffrement AES-256, TLS 1.3, logs d'audit, conformité KYC/AML

3.5. TESTS ET VALIDATION
- Tableau 3.2 : Résultats comparatifs des modèles (F1, Recall, AUC-PR, FP, FN, temps)
- Figure 3.11 : Matrices de confusion (IF, RF, XGB)
- Figure 3.12 : Courbes Precision-Recall comparatives
- Analyse des erreurs (faux positifs, faux négatifs)
- Discussion sur les contraintes d'infrastructure au Togo

⸻ TABLEAUX À PRODUIRE ⸻
- Tableau 3.1 : Matrice RBAC (rôles et permissions)
- Tableau 3.2 : Résultats comparatifs des modèles (F1, Recall, AUC-PR, FP, FN, temps)
- Tableau 3.3 : Top-10 features SHAP

⸻ FIGURES À PRODUIRE ⸻
- Figure 3.1 : Distribution des classes
- Figure 3.2 : Valeurs manquantes
- Figure 3.3 : Distribution montant (log)
- Figure 3.4 : Analyse temporelle
- Figure 3.5 : Heatmap corrélations
- Figure 3.6 : SHAP Summary Plot
- Figure 3.7 : SHAP Feature Importance
- Figure 3.8 : SHAP Waterfall (2 exemples)
- Figure 3.9 : Schéma d'architecture technique
- Figure 3.10 : Maquettes interface (dashboard)
- Figure 3.11 : Matrices de confusion
- Figure 3.12 : Courbes Precision-Recall

══════════════════════════════════════════════════════════════
  CHAPITRE IV — ANALYSE, DIAGNOSTIC ET INTERVENTION (≈20 pages)
══════════════════════════════════════════════════════════════

4.1. ANALYSE DIAGNOSTIQUE
- SWOT des dispositifs de détection existants au Togo (Tableau 4.1)
- Besoins spécifiques identifiés (entretiens + analyse littérature)
- Écarts entre pratiques actuelles et capacités du ML
- Analyse des coûts des faux positifs et faux négatifs (Tableau 4.2)

4.2. VÉRIFICATION DES HYPOTHÈSES
- HS1 (quantitatif) : Recall=0.92 ≥ 0.85 → CONFIRMÉE. Tableau 4.3
- HS2 (qualitatif + PoC) : validation via entretiens + RBAC → Analyse
- HS3 (qualitatif + SHAP) : concentration SHAP ≥ 0.5 → Analyse
- Synthèse : Tableau 4.4 — Bilan des hypothèses (Confirmée/Partiellement/Non confirmée)

4.3. INTERVENTION PROPOSÉE
- Lien diagnostic → solution : pourquoi l'Ensemble Learning + XAI répond aux besoins identifiés
- Composantes : module collecte/prétraitement, module détection (3 niveaux), module XAI/SHAP, module feedback
- Architecture cible (déjà détaillée en Ch.III, rappel synthétique)
- Formation et conduite du changement pour les agents bancaires

4.4. STRATÉGIE DE DÉPLOIEMENT
- Phase pilote : 1 banque/opérateur à Lomé, périmètre limité, 3 mois
- Phase généralisation : rollout vers 3-5 banques, intégration SI existants
- Monitoring continu et réentraînement périodique

4.5. ÉTUDE DE FAISABILITÉ
- Technique : infrastructure requise (serveurs, API, connectivité) — faisable avec hébergement cloud
- Économique : Tableau 4.5 — ROI estimé (coûts développement vs pertes évitées)
- Sociale : acceptabilité par les agents, formation nécessaire
- Réglementaire : conformité BCEAO/UEMOA — compatible

4.6. LIMITES DE L'ÉTUDE
- Dataset international comme proxy (discuté en 2.4.1)
- Échantillon qualitatif limité (5-8 répondants)
- PoC non déployé en production réelle

⸻ TABLEAUX À PRODUIRE ⸻
- Tableau 4.1 : Analyse SWOT des systèmes existants
- Tableau 4.2 : Analyse des coûts (FP vs FN)
- Tableau 4.3 : Vérification HS1 (Recall, F1, AUC-PR)
- Tableau 4.4 : Bilan des hypothèses (HG, HS1, HS2, HS3)
- Tableau 4.5 : ROI estimé à 3 ans

══════════════════════════════════════════════════════════════
  CONCLUSION GÉNÉRALE (≈6 pages)
══════════════════════════════════════════════════════════════

- Synthèse des résultats (rappel 1 paragraphe par chapitre)
- Vérification des hypothèses : HG ✓ (ML > méthodes traditionnelles), HS1 ✓ (Recall=0.92), HS2 partiellement, HS3 partiellement
- Contributions scientifiques : première étude documentée sur détection fraude par IA au Togo
- Contributions pratiques : architecture cible, PoC fonctionnel, recommandations opérationnelles
- Limites (rappel) : proxy international, échantillon qualitatif restreint
- Perspectives :
  1. Partenariat banque/opérateur mobile money pour données réelles togolaises
  2. Extension à l'espace UEMOA
  3. IA fédérée inter-bancaire
  4. Déploiement en sandbox test

══════════════════════════════════════════════════════════════
  RÉFÉRENCES BIBLIOGRAPHIQUES (Norme APA)
══════════════════════════════════════════════════════════════

Catégories à couvrir :
- Méthodologie : FUNIBER (2017), Creswell (2014), Saunder et al.
- Détection fraude ML : Bhattacharyya et al. (2011), Dal Pozzolo et al. (2014, 2015)
- XGBoost : Chen & Guestrin (2016)
- SHAP : Lundberg & Lee (2017)
- Isolation Forest : Liu et al. (2008, 2012)
- SMOTE : Chawla et al. (2002)
- Réglementations BCEAO/UEMOA
- Rapports GIABA, Banque Centrale du Togo

══════════════════════════════════════════════════════════════
  ANNEXES
══════════════════════════════════════════════════════════════

- Annexe A : Grille d'entretien semi-directif
- Annexe B : Questionnaire agents bancaires
- Annexe C : Code Python (prétraitement, SMOTE, entraînement, SHAP)
- Annexe D : Schéma d'architecture détaillé
- Annexe E : Résultats complets des métriques

══════════════════════════════════════════════════════════════
  FORMAT DE SORTIE
══════════════════════════════════════════════════════════════

- Police : Times New Roman, taille 12
- Interligne : 1,5
- Marges : 3 cm gauche, 2,5 cm autres
- Longueur cible : 80-100 pages (hors annexes)
- Titres chapitres : MAJUSCULES gras (13pt)
- Titres sous-chapitres : Gras minuscule (13pt)
- Titres section : Italique gras minuscule (12pt)

Produis le document complet chapitre par chapitre, avec tous les tableaux et figures intégrés.
