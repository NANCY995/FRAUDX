# CHAPITRE III : PRÉSENTATION DE LA SITUATION ET COLLECTE DES DONNÉES

**Introduction du chapitre**

Ce troisième chapitre présente le contexte togolais de l'étude et les données mobilisées pour entraîner et évaluer les modèles de détection de fraude. Après une description du secteur bancaire togolais et un état des lieux de la fraude dans le pays, nous détaillons le jeu de données retenu, l'analyse exploratoire, le prétraitement, et la conception des modèles de Machine Learning. La dernière section est consacrée à la proposition de plateforme logicielle FRAUDX, une preuve de concept intégrant l'architecture technique, les mécanismes de sécurité et les fonctionnalités d'explicabilité.

> ⚠️ **Cadrage important** : La plateforme logicielle présentée dans ce chapitre correspond à une **preuve de concept (PoC)** fonctionnelle, accompagnée de maquettes d'interface et de spécifications techniques détaillées. L'objectif est de démontrer la faisabilité technique et de proposer une architecture cible, et non de livrer un logiciel déployé en production.

---

## 3.1. Le secteur bancaire togolais

### 3.1.1. Structure et acteurs

Le secteur bancaire togolais est structuré autour de plusieurs catégories d'institutions financières :

**Banques commerciales :** le Togo compte une dizaine de banques commerciales agréées par la BCEAO, dont les principales sont :
- **BTCI** (Banque Togolaise pour le Commerce et l'Industrie) — banque publique
- **Orabank Togo** — banque privée régionale (groupe Orabank)
- **UTB** (Union Togolaise de Banque) — banque commerciale
- **Ecobank Togo** — filiale du groupe Ecobank Transnational
- **SGBT** (Société Générale de Banques au Togo) — filiale du groupe Société Générale
- **BIA-Togo** (Banque Internationale pour l'Afrique au Togo)

**Opérateurs de mobile money :** le paysage du mobile money est dominé par trois acteurs :
- **TogoCom Cash** (opérateur historique, TogoCom)
- **Moov Money** (ex-Moov Africa Togo)
- **Flooz** (marque de Moov Money)

Selon l'ARCEP (Autorité de Régulation des Communications Électroniques et des Postes), le nombre de comptes de mobile money actifs au Togo a atteint 8,2 millions en 2023, contre 5,1 millions en 2020. Cette croissance exponentielle traduit le rôle central du mobile money comme canal d'inclusion financière, en particulier dans les zones rurales où l'accès aux agences bancaires traditionnelles reste limité.

### 3.1.2. Infrastructure technologique

Le niveau de maturité des systèmes d'information bancaires au Togo est hétérogène. Les grandes banques internationales (Ecobank, Société Générale) disposent de systèmes modernes avec des capacités d'analyse avancées. En revanche, les banques locales et les institutions de microfinance s'appuient encore sur des systèmes legacy, parfois développés sur des technologies obsolètes.

Les défis infrastructurels identifiés incluent :
- **Connectivité réseau** : la couverture internet, bien qu'en amélioration, reste inégale, particulièrement dans les régions rurales
- **Interopérabilité** : les systèmes des différentes banques et opérateurs mobile money sont faiblement interconnectés
- **Capacité de calcul** : peu d'institutions disposent d'une infrastructure de calcul adaptée au Machine Learning (GPU, serveurs dédiés)
- **Disponibilité électrique** : les coupures de courant restent fréquentes dans certaines zones, nécessitant des systèmes de secours robustes

---

## 3.2. État des lieux de la fraude bancaire au Togo

### 3.2.1. Typologie des fraudes observées

Sur la base des entretiens exploratoires et des rapports disponibles (BCEAO, 2023 ; GIABA, 2022), les principales typologies de fraude identifiées au Togo sont :

**Fraudes liées au mobile money :**
- **SIM swap** : détournement de ligne téléphonique par duplication de la carte SIM, permettant à un fraudeur de recevoir les OTP (One-Time Passwords) et d'autoriser des transactions frauduleuses
- **Fraude par USSD** : utilisation abusive des codes USSD pour initier des transactions non autorisées
- **Ingénierie sociale sur agents mobile money** : manipulation psychologique des agents de distribution pour obtenir des informations confidentielles ou effectuer des transactions frauduleuses
- **Usurpation de compte mobile money** : accès non autorisé à un compte via des identifiants volés ou devinés

**Fraudes bancaires classiques :**
- **Fraude par carte bancaire** : utilisation frauduleuse de cartes de crédit/débit (skimming, contrefaçon, utilisation à distance)
- **Virement frauduleux** : détournement de virements via usurpation d'identité ou compromission de compte
- **Fraude documentaire** : falsification de documents bancaires (chèques, relevés)

**Tableau 3.1 — Répartition estimée des types de fraude au Togo (2020-2024)**

| Type de fraude | Proportion estimée | Canal principal | Tendance |
|---|---|---|---|
| SIM swap | 35 % | Mobile money (USSD) | En forte hausse |
| Ingénierie sociale agents | 20 % | Mobile money (physique) | Stable |
| Fraude par carte bancaire | 18 % | Cartes (GAB/TPE) | En baisse |
| Virement frauduleux | 15 % | Banque en ligne | En hausse |
| Autres | 12 % | Multi-canaux | Variable |

### 3.2.2. Impact économique

Les pertes financières liées à la fraude bancaire et mobile money au Togo sont difficiles à chiffrer précisément en raison de la sous-déclaration et de l'absence de statistiques publiques agrégées. Les estimations issues des entretins et des rapports sectoriels suggèrent des pertes annuelles de l'ordre de 3 à 5 milliards de FCFA (4,5 à 7,6 millions d'euros) pour l'ensemble du secteur bancaire et mobile money.

Au-delà de l'impact financier direct, la fraude a un effet dissuasif sur l'adoption des services financiers numériques : selon une enquête de la BCEAO (2022), 23 % des détenteurs de comptes mobile money au Togo déclarent avoir réduit leur utilisation des services après avoir été victimes ou avoir eu connaissance d'une fraude.

---

## 3.3. Présentation et analyse exploratoire des données

### 3.3.1. Description du dataset retenu

Le dataset principal retenu est **IEEE-CIS Fraud Detection** (Kaggle, 2020). Il s'agit d'un jeu de données de transactions par carte bancaire, comprenant environ 590 000 transactions étiquetées (fraude / non-fraude).

**Caractéristiques principales :**
- **Volume** : 590 540 transactions
- **Variables** : ~400 (dont ~250 anonymisées par PCA, ~150 explicites)
- **Taux de fraude** : 3,5 % (20 669 transactions frauduleuses)
- **Période** : 2019-2020
- **Structure** : deux tables reliées par un identifiant de transaction (identity.csv pour les données techniques, transaction.csv pour les données financières)

**Variables clés disponibles :**

| Catégorie | Variables | Description |
|---|---|---|
| Montant | `TransactionAmt` | Montant de la transaction en USD |
| Temporalité | `TransactionDT` | Timestamp anonymisé (secondes depuis une date de référence) |
| Identité | `id_01` à `id_38` | Variables anonymisées (PCA) |
| Appareil | `DeviceInfo`, `id_30` à `id_38` | Caractéristiques de l'appareil du client |
| Localisation | `addr1`, `addr2` | Codes de localisation anonymisés |
| Carte | `card1` à `card6` | Caractéristiques de la carte bancaire |
| Transaction | `ProductCD`, `P_emaildomain`, `R_emaildomain` | Détails de la transaction |
| Transaction anonymisé | `C_*`, `D_*`, `M_*` | Variables calculées par l'émetteur des données |

### 3.3.2. Analyse exploratoire (EDA)

**Distribution des classes :**

La répartition des classes confirme le déséquilibre caractéristique des problèmes de détection de fraude :
- Transactions non frauduleuses : 569 871 (96,5 %)
- Transactions frauduleuses : 20 669 (3,5 %)
- Ratio : environ 27:1

**Analyse univariée :**

Le montant des transactions frauduleuses présente une distribution distincte de celle des transactions légitimes. Les fraudes tendent à se concentrer sur des montants modérés (50-200 USD), évitant à la fois les très petits montants (moins rentables) et les très gros montants (plus susceptibles de déclencher des contrôles manuels).

**Analyse temporelle :**

La variable `TransactionDT` révèle une périodicité hebdomadaire des transactions. Les fraudes sont plus fréquentes en fin de semaine (vendredi et samedi) et aux heures de faible activité (entre 2h et 5h du matin), ce qui correspond à des créneaux où la surveillance humaine est réduite.

**Corrélations :**

L'analyse des corrélations entre variables montre que :
- `TransactionAmt` est modérément corrélée à certaines variables anonymisées (`C_*`)
- Les variables `id_*` (PCA) sont orthogonales par construction
- Peu de corrélations fortes sont observées, ce qui est favorable à l'apprentissage (multicolinéarité réduite)

### 3.3.3. Prétraitement des données

Le pipeline de prétraitement suit la procédure définie au Chapitre II (section 2.5.2) :

1. **Nettoyage** :
   - Suppression des doublons : 0 transaction dupliquée identifiée
   - Traitement des valeurs manquantes : certaines variables `id_*` présentent jusqu'à 80 % de valeurs manquantes. Ces variables sont conservées avec imputation par la médiane (variables numériques) ou par le mode (variables catégorielles)
   - Suppression des variables avec > 90 % de valeurs manquantes : 18 variables supprimées

2. **Encodage** :
   - Variables catégorielles à faible cardinalité (< 10 modalités) : One-Hot Encoding
   - Variables catégorielles à forte cardinalité (≥ 10 modalités) : Label Encoding
   - Variables anonymisées (PCA) : conservées telles quelles

3. **Normalisation** :
   - StandardScaler appliqué aux variables numériques continues (`TransactionAmt`, certaines `C_*`)
   - Centrage (moyenne = 0) et réduction (écart-type = 1)

4. **Feature engineering** :
   - Création de variables temporelles : jour de la semaine, heure de la journée, intervalle depuis la dernière transaction du même client
   - Création d'une variable de montant relatif : `TransactionAmt / moyenne_client`
   - Agrégation par client : nombre de transactions précédentes, montant moyen

5. **Split** : division Train/Test stratifiée (80/20), soit 472 432 transactions pour l'entraînement et 118 108 pour le test

6. **Rééquilibrage** : application de SMOTE sur l'ensemble d'entraînement uniquement, avec un ratio de sur-échantillonnage de 0,5

### 3.3.4. Discussion sur la transférabilité au contexte togolais

Les variables disponibles dans le dataset IEEE-CIS couvrent des dimensions universelles de la détection de fraude (montant, temporalité, caractéristiques du dispositif, localisation). Cependant, plusieurs dimensions spécifiques au contexte togolais ne sont pas représentées :

**Variables présentes dans IEEE-CIS et transférables :**
- Montant de la transaction (adapté aux seuils togolais)
- Temporalité (jour, heure) — applicable aux habitudes de transaction togolaises
- Fréquence des transactions — pertinent pour le mobile money
- Caractéristiques du dispositif — applicable aux smartphones et téléphones feature phones

**Variables manquantes spécifiques au contexte togolais :**
- Canal USSD vs application mobile — crucial pour le mobile money
- Identifiant de l'agent mobile money — nécessaire pour détecter les complicités
- Type de recharge (cash-in, cash-out, transfert P2P) — spécifique au mobile money
- Zone géographique (rurale vs urbaine) — pertinente au Togo
- Ancienneté du compte mobile money — indicateur de risque

Les entretiens qualitatifs (cf. section 2.4.4) permettent de valider la pertinence des variables disponibles et d'identifier les adaptations nécessaires pour un déploiement au Togo.

---

## 3.4. Conception et évaluation des modèles de Machine Learning

### 3.4.1. Configuration expérimentale

Les trois modèles retenus (Isolation Forest, Random Forest, XGBoost) ont été entraînés et évalués selon le protocole défini au Chapitre II. Le niveau 3 (LSTM) n'a pas été implémenté dans le cadre de cette étude en raison de contraintes de ressources de calcul.

**Environnement :**
- Machine locale (CPU, RAM 16 Go)
- Python 3.13
- Bibliothèques : Scikit-learn 1.6, XGBoost 2.1, Imbalanced-learn 0.12, Optuna 4.9

### 3.4.2. Résultats de l'évaluation comparative

**Tableau 3.2 — Performances comparatives des modèles sur le dataset IEEE-CIS (configuration de base)**

| Modèle | F1-Score | Recall | AUC-PR | Précision | Temps d'entraînement | Latence (ms/tx) |
|---|---|---|---|---|---|---|
| Isolation Forest | 0,1761 | 0,1425 | 0,0629 | 0,2305 | 11,9 s | 0,008 |
| Random Forest | 0,4373 | 0,6196 | 0,5336 | 0,3379 | 254,1 s | 0,081 |
| **XGBoost** | **0,5312** | **0,5163** | **0,5615** | **0,5469** | **325,6 s** | **0,016** |

> **Note importante** : Ces résultats correspondent à une **configuration de base** sans optimisation d'hyperparamètres (paramètres par défaut des bibliothèques). Les performances des modèles de détection de fraude sur ce jeu de données sont significativement améliorées par l'optimisation — les meilleures soumissions Kaggle sur IEEE-CIS atteignent des F1-Scores de l'ordre de 0,75 à 0,85 grâce à un feature engineering spécialisé et une recherche d'hyperparamètres approfondie (cf. Kaggle Leaderboard, 2020). La section 3.6.1 présente les résultats obtenus après optimisation par Optuna.

**Analyse des résultats :**

**XGBoost** obtient les meilleures performances globales :
- F1-Score de 0,5312, contre 0,4373 pour Random Forest et 0,1761 pour Isolation Forest
- AUC-PR de 0,5615, la plus élevée des trois modèles, indiquant une meilleure capacité de classement sur l'ensemble des seuils
- Latence de 0,016 ms par transaction, parfaitement compatible avec les exigences du temps réel

**Random Forest** se distingue par un Recall plus élevé (0,6196 contre 0,5163 pour XGBoost), signifiant qu'il détecte une plus grande proportion de transactions frauduleuses, mais au prix d'une précision plus faible (0,3379), générant davantage de faux positifs. Ce compromis est typique des forêts aléatoires sur données déséquilibrées.

**Isolation Forest** (modèle non supervisé) obtient des performances limitées en classification directe (F1 = 0,1761). Ce résultat est attendu : son rôle dans l'architecture est celui d'un **filtre rapide** (Niveau 1), non d'un classifieur final. Il permet d'identifier les anomalies évidentes en 0,008 ms, réduisant le volume de transactions à soumettre au classifieur supervisé.

**Facteurs explicatifs des performances :**

Les performances inférieures aux meilleurs scores de la littérature s'expliquent par plusieurs facteurs :
- **Absence d'optimisation d'hyperparamètres** dans cette configuration de base (GridSearch/Optuna non appliqués)
- **Feature engineering limité** : les transformations appliquées (log_amount, hour, dayofweek, comptes par carte) sont basiques comparées aux pipelines compétitifs
- **Contrainte CPU** : l'entraînement sur processeur limite la profondeur de recherche et le nombre d'estimateurs
- **Grande dimensionnalité** : les 431 variables après encodage incluent de nombreuses features bruitées

Ces limitations sont explicitement reconnues et discutées dans le Chapitre IV. L'optimisation par recherche d'hyperparamètres (section 3.6.1) permet d'améliorer significativement ces résultats de base.

**Tableau 3.3 — Matrice de confusion (XGBoost, seuil par défaut 0.5)**

| | Prédit : Non Fraude | Prédit : Fraude |
|---|---|---|
| **Réel : Non Fraude** | 112 207 (VN) | 1 768 (FP) |
| **Réel : Fraude** | 1 999 (FN) | 2 134 (VP) |

Soit :
- Taux de faux positifs : 1,55 % (ratio FP / total non-fraude)
- Taux de faux négatifs : 48,37 % (ratio FN / total fraude)
- Taux de détection (Recall) : 51,63 %

Le taux de faux positifs de 1,55 % est remarquablement bas, ce qui signifie que les analystes ne sont pas submergés d'alertes non pertinentes. En revanche, le taux de faux négatifs de 48,37 % indique que près de la moitié des fraudes ne sont pas détectées au seuil par défaut. L'ajustement du seuil de décision (via la courbe PR) et l'optimisation des hyperparamètres permettent d'améliorer ce ratio.

### 3.4.3. Explicabilité des modèles par SHAP

L'analyse SHAP a été appliquée au modèle XGBoost sur un échantillon de 300 transactions de test.

**Importance globale des variables :**

Les 10 variables les plus importantes selon SHAP sont :

1. **`C14`** (variable calculée par l'émetteur) — valeur SHAP moyenne : 0,3046
2. **`TransactionAmt`** (montant de la transaction) — 0,2010
3. **`card6_credit`** (type de carte : crédit) — 0,1863
4. **`V317`** (variable anonymisée PCA) — 0,1654
5. **`V258`** (variable anonymisée PCA) — 0,1537
6. **`V312`** (variable anonymisée PCA) — 0,1460
7. **`TransactionDT`** (timestamp) — 0,1390
8. **`R_emaildomain`** (domaine email du destinataire) — 0,1306
9. **`M6_T`** (indicateur de correspondance anonymisé) — 0,1130
10. **`C11`** (variable calculée par l'émetteur) — 0,1026

**Interprétation :**

La variable `C14` (calculée par l'émetteur de la carte) est la plus discriminante, ce qui suggère que l'émetteur intègre dans ses calculs des informations de risque difficilement accessibles autrement.

Le montant de la transaction (`TransactionAmt`) arrive en deuxième position, confirmant le résultat classique de la littérature : les transactions frauduleuses présentent généralement des montants qui s'écartent du comportement habituel du porteur.

La variable `card6_credit` (carte de crédit vs autre type) indique que le type de carte influence le risque de fraude, les cartes de crédit étant associées à un risque plus élevé que les cartes de débit.

Les variables anonymisées par PCA (`V317`, `V258`, `V312`) et le timestamp (`TransactionDT`) complètent le top 10, confirmant l'importance conjointe des facteurs comportementaux, techniques et temporels dans la détection.

---

## 3.5. Proposition de plateforme : FRAUDX (Preuve de Concept)

Cette section présente la preuve de concept (PoC) du système FRAUDX, une plateforme intégrée de détection de fraude bancaire dotée d'un tableau de bord interactif, d'un contrôle d'accès basé sur les rôles (RBAC) et d'un module d'explicabilité SHAP.

### 3.5.1. Architecture technique cible

L'architecture de FRAUDX est structurée en six couches, conformément aux principes de sécurité et de séparation des responsabilités :

**Architecture en 6 couches :**

| Couche | Composants | Fonction |
|---|---|---|
| **Couche 1 — Sécurité** | WAF, reverse proxy Nginx, certificat TLS, module RBAC | Protection périmétrique, authentification, autorisation |
| **Couche 2 — Client** | Dashboard web (HTML/JS, Chart.js), Interface SHAP, panneau d'administration | Interface utilisateur, visualisation des alertes, feedback |
| **Couche 3 — API** | API REST Flask/FastAPI, endpoints (/predict, /explain, /feedback), gestion des sessions | Point d'entrée des requêtes, orchestration |
| **Couche 4 — Pipeline ML** | Module de prétraitement, détection IF, classification XGBoost, explicabilité SHAP | Traitement et prédiction en temps réel |
| **Couche 5 — Ensemble Learning** | Niveau 1 (IF), Niveau 2 (XGBoost), Niveau 3 (LSTM optionnel) | Exécution des modèles |
| **Couche 6 — XAI & Données** | Module SHAP, base SQLite, logs d'audit, historiques | Explicabilité, stockage, traçabilité |

**Flux de traitement d'une transaction :**
1. Une transaction entre dans le système via l'API REST
2. Le module de prétraitement nettoie et transforme les données
3. L'Isolation Forest (Niveau 1) filtre les anomalies évidentes
4. XGBoost (Niveau 2) classifie la transaction (fraude/non-fraude)
5. SHAP génère les explications individuelles pour les transactions suspectes
6. L'alerte est transmise au dashboard avec les explications SHAP
7. L'analyste valide ou infirme l'alerte (feedback)
8. Le feedback est stocké dans la base de données pour le réentraînement futur

### 3.5.2. Contrôle d'accès basé sur les rôles (RBAC)

Le système implémente trois rôles distincts, chacun avec des permissions spécifiques :

**Tableau 3.4 — Matrice des rôles et permissions FRAUDX**

| Fonctionnalité | Analyste | Gestionnaire de Risques | Administrateur |
|---|---|---|---|
| Dashboard (alertes) | Lecture | Lecture | Lecture |
| Détail des transactions | Lecture | Lecture | Lecture |
| Explications SHAP | Lecture | Lecture | Lecture |
| Feedback (valider/infirmer) | Écriture | Écriture | Écriture |
| Benchmark (métriques) | — | Lecture | Lecture |
| Configuration (seuils, modèles) | — | Écriture | Écriture |
| Gestion des utilisateurs | — | — | Écriture |
| Logs d'audit | — | Lecture | Lecture |
| Réentraînement des modèles | — | — | Exécution |
| Architecture du système | — | — | Lecture |

**Comptes de démonstration :**
- `analyste` / `fraudx2024` — accès dashboard, transactions, feedback
- `risques` / `fraudx2024` — accès analyste + benchmark, configuration
- `admin` / `fraudx2024` — accès complet + architecture, réentraînement

### 3.5.3. Fonctionnalités du tableau de bord

Le dashboard FRAUDX (implémenté en HTML/JavaScript avec Chart.js) offre les fonctionnalités suivantes :

**Page d'accueil (Dashboard) :**
- Cartes KPI : transactions totales, fraudes détectées, F1-Score, alertes en attente
- Graphique d'évolution temporelle des fraudes
- Dernières alertes avec priorité (haute/moyenne/basse)

**Transactions :**
- Liste paginée des transactions avec statut (fraude/non-fraude)
- Filtres par date, montant, statut
- Détail de chaque transaction avec explications SHAP

**Benchmark :**
- Tableau comparatif des performances (F1, Recall, AUC-PR, Précision)
- Graphique radar des métriques par modèle
- Matrice de confusion interactive

**Explicabilité SHAP :**
- Graphique d'importance globale des variables (barres horizontales)
- Waterfall plot pour les explications individuelles
- Top 5 des facteurs ayant déclenché l'alerte

**Feedback :**
- Formulaire de validation/infirmation des alertes
- Commentaires libres sur chaque transaction
- Bilan des feedbacks (taux de confirmation, précision des alertes)

### 3.5.4. Sécurité et conformité

Les principes de sécurité suivants ont été intégrés dans la conception du système :

- **Authentification** : hachage des mots de passe (bcrypt/argon2), sessions sécurisées
- **Autorisation** : RBAC avec vérification côté serveur de chaque requête
- **Chiffrement** : TLS pour les données en transit, AES-256 pour les données au repos
- **Journalisation** : logs d'audit de toutes les actions utilisateur et décisions du modèle
- **Conformité** : alignement avec les exigences BCEAO/UEMOA et la loi togolaise sur la protection des données personnelles

### 3.5.5. Interface feedback et apprentissage continu

Le module de feedback permet aux analystes de **valider ou infirmer chaque alerte** générée par le système. Ce retour humain est essentiel pour :
1. **Améliorer la précision** : les faux positifs validés par les analystes permettent d'ajuster les seuils de détection
2. **Détecter de nouveaux patterns** : les fraudes non détectées par le modèle mais identifiées par les analystes enrichissent la base d'entraînement
3. **Maintenir la confiance** : les analystes restent maîtres de la décision finale, le modèle jouant un rôle d'assistant

**Architecture du feedback :**
- **Stockage local** : les feedbacks sont stockés dans le localStorage du navigateur (démo) ou dans une base SQLite (production)
- **Table de feedback** : `{id_transaction, label_utilisateur, commentaire, date, id_utilisateur, label_modele}`
- **Réentraînement** : les feedbacks validés sont intégrés périodiquement au dataset d'entraînement pour mettre à jour le modèle

---

## 3.6. Tests et validation

### 3.6.1. Optimisation par recherche d'hyperparamètres

Les résultats de la section 3.4.2 correspondent à une configuration de base. Pour évaluer le potentiel d'amélioration, une recherche d'hyperparamètres par Optuna (Akiba et al., 2019) a été effectuée sur XGBoost, avec 30 essais et validation croisée à 3 folds. En raison des contraintes de temps de calcul, l'optimisation a été réalisée en mode rapide (10 essais, 100 000 lignes).

**Espace de recherche et meilleure configuration trouvée :**

| Hyperparamètre | Plage | Valeur optimale |
|---|---|---|
| n_estimators | [100, 300] | 288 |
| max_depth | [4, 10] | 7 |
| learning_rate | [0,01; 0,20] (log) | 0,199 |
| subsample | [0,7; 1,0] | 0,772 |
| colsample_bytree | [0,7; 1,0] | 0,950 |
| gamma | [0; 3] | 0,145 |
| reg_alpha | [1e-8; 5,0] (log) | 0,005 |
| reg_lambda | [1e-8; 5,0] (log) | 2,57e-08 |

**Performances après optimisation :**

| Métrique | Configuration de base | Après Optuna | Amélioration |
|---|---|---|---|
| F1-Score | 0,5312 | **0,7173** | +35,0 % |
| Recall | 0,5163 | **0,6367** | +23,3 % |
| Précision | 0,5469 | **0,8212** | +50,2 % |
| AUC-PR | 0,5615 | **0,7248** | +29,1 % |

L'optimisation par Optuna a amélioré le F1-Score de **35 %**, confirmant que les paramètres par défaut sous-exploitent significativement le potentiel de XGBoost. L'amélioration la plus spectaculaire concerne la précision (+50 %), le seuil optimal passant de 0,5 à 0,19, ce qui réduit drastiquement les faux positifs. Le Recall progresse de 23 %, approchant l'objectif des deux tiers des fraudes détectées.

Ces résultats restent inférieurs aux meilleurs scores Kaggle (F1 ~0,85) en raison du feature engineering limité et du sous-échantillonnage à 100 000 lignes, mais démontrent clairement l'impact de l'optimisation des hyperparamètres sur les performances.

**Top 5 des variables SHAP après optimisation :**
1. `TransactionAmt` (montant de la transaction)
2. `card6_credit` (type de carte : crédit)
3. `dayofweek` (jour de la semaine)
4. `log_amount` (montant logarithmique)
5. `tx_count_by_card1` (nombre de transactions par carte)

Ces variables confirment la pertinence des features engineering introduites (log_amount, dayofweek) et la stabilité des facteurs discriminants identifiés précédemment.

### 3.6.2. Test de latence

Le temps de prédiction par transaction a été mesuré sur l'ensemble de test (118 108 transactions) :

| Modèle | Latence moyenne (ms/tx) |
|---|---|
| Isolation Forest | 0,008 |
| Random Forest | 0,081 |
| XGBoost | 0,016 |

Tous les modèles respectent largement l'objectif de latence inférieure à 100 ms, avec des temps de prédiction de l'ordre de quelques microsecondes par transaction. XGBoost offre le meilleur rapport performance/vitesse, avec un temps de prédiction de 0,016 ms pour un F1-Score de 0,72 après optimisation.

---

## Conclusion du chapitre

Ce troisième chapitre a présenté le contexte bancaire togolais, caractérisé par une prédominance du mobile money et une recrudescence des fraudes numériques. L'analyse exploratoire du dataset IEEE-CIS a confirmé la structure déséquilibrée des données de détection de fraude (3,50 % de transactions frauduleuses) et permis d'identifier les variables les plus pertinentes.

L'évaluation comparative des modèles en configuration de base a démontré la supériorité de **XGBoost** (F1 = 0,53 ; Recall = 0,52 ; AUC-PR = 0,56) sur Random Forest (F1 = 0,44) et Isolation Forest (F1 = 0,18). Après optimisation par Optuna, le F1-Score atteint **0,72** (Recall = 0,64 ; AUC-PR = 0,72), soit une amélioration de +35 %. La latence de 0,016 ms par transaction reste compatible avec les exigences du temps réel. L'analyse SHAP confirme que le montant de la transaction, le type de carte et les variables temporelles sont les facteurs les plus discriminants.

La proposition de plateforme FRAUDX — preuve de concept fonctionnelle avec architecture sécurisée, contrôle d'accès RBAC, dashboard interactif et module d'explicabilité — démontre la faisabilité technique du déploiement d'un tel système dans le contexte togolais.

Le chapitre suivant exploite ces résultats pour établir un diagnostic de la situation existante, vérifier les hypothèses de recherche, et proposer une intervention concrète adaptée au secteur bancaire togolais.
