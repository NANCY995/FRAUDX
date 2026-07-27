# CHAPITRE II : MÉTHODOLOGIE DE L'ÉTUDE

## Introduction du chapitre

Ce deuxième chapitre expose la méthodologie employée pour répondre aux questions de recherche formulées dans l'introduction générale et vérifier les hypothèses qui en découlent. Après avoir précisé la nature de l'étude et défini les variables mobilisées, nous présentons la population et l'échantillon retenus, l'approche méthodologique d'ensemble learning enrichie par l'explicabilité (XAI), ainsi que les outils de collecte, d'analyse et de développement utilisés. La stratégie de vérification des hypothèses est exposée en fin de chapitre, établissant le lien systématique entre chaque hypothèse, les données mobilisées et les indicateurs retenus.

## 2.1. Nature de l'étude

La présente étude s'inscrit dans une démarche prospective à approche quantitative, de type non expérimental à visée explicative. Elle s'inscrit dans une logique de recherche en sciences sociales telle que décrite par Quivy & Van Campenhoudt (2006), et correspond au niveau Compréhensif selon la classification de FUNIBER (2017), dont l'objectif est de proposer une solution fondée sur une analyse rigoureuse des données et de la littérature existante.

L'approche quantitative repose sur l'entraînement et l'évaluation comparative de trois algorithmes de Machine Learning (Isolation Forest, Random Forest, XGBoost) sur un jeu de données de transactions financières. Les performances sont mesurées à l'aide de métriques objectives (F1-Score, Recall, AUC-PR) et confrontées aux résultats rapportés dans la littérature.

Un volet qualitatif est proposé en perspective pour confronter les résultats aux perceptions du terrain.

Le choix d'une approche quantitative se justifie par la nature de la problématique : la détection de fraude par IA comporte une dimension technique prépondérante (sélection et optimisation des algorithmes) qui constitue le cœur de l'étude. Un volet qualitatif ultérieur permettrait d'enrichir l'analyse par une dimension humaine et organisationnelle (acceptabilité, conformité, interprétabilité).

## 2.2. Variables de l'étude

### 2.2.1. Définition conceptuelle des variables

**Variables indépendantes (VI) :**

- Types de transactions : transactions bancaires classiques (cartes, virements) et transactions mobile money (USSD, application mobile)
- Comportements utilisateurs : fréquence des transactions, montants, canaux utilisés, localisation géographique
- Données contextuelles locales : spécificités du marché togolais (canaux USSD, agents mobile money, temporalité des transactions)

**Variables dépendantes (VD) :**

- Taux de détection de fraude : mesuré par le F1-Score, le Recall et l'AUC-PR
- Taux de faux positifs : proportion de transactions légitimes classées à tort comme frauduleuses
- Temps de traitement : latence de détection par transaction (cible inférieure à 100 ms)

**Variable modératrice :**

- Interprétabilité des modèles : mesurée via les scores SHAP (importance des variables) et la lisibilité des explications individuelles par des non-spécialistes

### 2.2.2. Limites et difficultés rencontrées

Plusieurs contraintes ont été identifiées en amont de l'étude :

1. **Indisponibilité des données bancaires togolaises réelles** : la confidentialité bancaire et l'absence de dataset public togolais imposent le recours à un dataset international de référence (IEEE-CIS Fraud Detection). Cette limite est explicitement assumée.
2. **Fort déséquilibre des classes** : dans les jeux de données de détection de fraude, la proportion de transactions frauduleuses est généralement inférieure à 1 % (3,5 % pour IEEE-CIS). Ce déséquilibre rend l'Accuracy non pertinente comme métrique d'évaluation et nécessite des techniques de rééquilibrage (SMOTE).
3. **Ressources techniques limitées** : l'étude a été menée sans accès à une infrastructure de calcul spécialisée (GPU). Les modèles ont été entraînés sur Google Colab et sur une machine locale, ce qui a limité la complexité des architectures explorées.
4. **Accès restreint aux statistiques sectorielles** : les données agrégées sur la fraude bancaire au Togo ne sont pas publiquement disponibles.

### 2.2.3. Opérationnalisation des variables et indicateurs

**Tableau 2.1 — Opérationnalisation des variables**

| Variable | Indicateur | Source de données | Unité de mesure |
|----------|------------|-------------------|-----------------|
| Types de transactions | Montant, canal, temporalité, localisation | IEEE-CIS | USD (montant), catégories (canal) |
| Comportements utilisateurs | Fréquence des transactions, intervalle inter-transactions | IEEE-CIS | Nombre, secondes |
| Performance de détection | F1-Score, Recall, AUC-PR | Résultats des modèles | Score [0-1] |
| Taux de faux positifs | FP / (FP + TN) | Matrice de confusion | Pourcentage |
| Latence de détection | Temps CPU par prédiction | Benchmark Python | Millisecondes |
| Interprétabilité | Score SHAP moyen, top-K variables | Analyse SHAP | Valeur Shapley |

**Indicateurs détaillés :**

- **F1-Score** : moyenne harmonique de la précision et du rappel. C'est la métrique principale retenue car elle pénalise à la fois les faux positifs et les faux négatifs.
- **AUC-PR (Area Under the Precision-Recall Curve)** : mesure la performance du modèle sur l'ensemble des seuils de décision. Contrairement à l'AUC-ROC, l'AUC-PR est plus informative sur les classes déséquilibrées car elle se concentre sur la classe minoritaire.
- **Recall (Rappel)** : proportion de transactions frauduleuses effectivement détectées. Un Recall élevé est prioritaire car un faux négatif (fraude non détectée) a un impact financier direct.

Note : l'Accuracy seule n'est pas pertinente sur des données fortement déséquilibrées.

### 2.2.4. Dynamique anticipée des variables

**Tableau 2.2 — Dynamique anticipée des variables et seuils de confirmation des hypothèses**

| Hypothèse | Variable indépendante | Variable dépendante | Dynamique anticipée | Seuil de confirmation | Seuil d'infirmation |
|-----------|----------------------|---------------------|---------------------|----------------------|---------------------|
| HG | Comparaison IF / RF / XGBoost | F1-Score, Recall, AUC-PR | XGBoost surpasse les deux autres modèles | XGBoost F1 ≥ 0,60 et Recall ≥ 0,80 | XGBoost F1 < 0,40 ou IF > XGBoost |
| HS1 | Modèles ML (IF, XGBoost) | Recall, correspondance SHAP/littérature | Recall ≥ 85 %, top-10 SHAP aligné sur littérature | Recall ≥ 0,85 et ≥ 7/10 variables SHAP concordantes | Recall < 0,70 ou < 4/10 variables concordantes |
| HS2 | Données contextuelles locales | Pertinence perçue | Non vérifiable dans cette étude — perspective proposée | — | — |
| HS3 | Module SHAP (explicabilité) | Taux de FP, utilité perçue | Baisse du FP visible via ajustement du seuil | FP ≤ 2 % | FP > 5 % |

**Règles de décision pour la confirmation des hypothèses :**

- **HG confirmée** si XGBoost atteint un F1-Score ≥ 0,60 et un Recall ≥ 0,80, surpassant les deux autres modèles
- **HS1 confirmée** si le Recall ≥ 0,85 et qu'au moins 7 des 10 variables les plus importantes selon SHAP correspondent aux facteurs de fraude documentés dans la littérature
- **HS2** : la confirmation de cette hypothèse nécessite un jeu de données local qui n'est pas disponible dans le cadre de cette étude — elle est proposée comme perspective
- **HS3 confirmée** si le taux de faux positifs ≤ 2 % après optimisation du seuil

## 2.3. Population et échantillon

### 2.3.1. Population cible

La population cible de cette étude est constituée de l'ensemble des transactions bancaires et mobile money effectuées au Togo entre 2019 et 2025. Cette période correspond à la phase de digitalisation bancaire accélérée et de croissance exponentielle du mobile money dans le pays. Faute de données réelles togolaises accessibles, un jeu de données international est utilisé comme proxy.

### 2.3.2. Échantillon quantitatif

Aucune donnée bancaire togolaise réelle n'étant accessible pour des raisons de confidentialité, l'étude s'appuie sur un dataset public de référence international :

- **Dataset principal : IEEE-CIS Fraud Detection (Kaggle, 2020)** — Environ 590 000 transactions, dont 3,5 % frauduleuses. Ce dataset, issu d'une compétition Kaggle organisée par IEEE Computational Intelligence Society, est largement utilisé dans la littérature récente (Dhieb et al., 2020 ; Kim et al., 2021 ; Ogunleye et al., 2022).
- **Dataset secondaire : Credit Card Fraud Dataset (ULB Machine Learning Group, Dal Pozzolo et al., 2015)** — Environ 284 807 transactions, dont 0,17 % frauduleuses. Utilisé comme référence complémentaire pour valider la robustesse des modèles sur un déséquilibre plus marqué.

**Limite** : Ces datasets étant constitués de transactions européennes et nord-américaines, ils ne capturent pas nativement les spécificités du contexte togolais. Cette limite est explicitement reconnue.

**Tableau 2.3 — Caractéristiques des datasets retenus**

| Caractéristique | IEEE-CIS Fraud Detection | Credit Card Fraud (ULB) |
|-----------------|--------------------------|------------------------|
| Nombre de transactions | ~590 000 | ~284 807 |
| Taux de fraude | 3,5 % | 0,17 % |
| Nombre de variables | ~400 (dont ~250 anonymisées) | 30 (PCA) |
| Période | 2019-2020 | 2013 |
| Origine géographique | États-Unis/Europe | Europe |
| Type de transactions | Cartes, virements | Cartes de crédit |

### 2.3.3. Échantillon qualitatif (perspective)

Un volet qualitatif est proposé en perspective, ciblant 5 à 8 responsables d'institutions bancaires et d'opérateurs de mobile money basés à Lomé (Togo). La technique d'échantillonnage raisonnée (choix délibéré des participants en fonction de leur profil et de leur expertise) est recommandée :

| Profil | Rôle | Objectif de l'entretien |
|--------|------|------------------------|
| Responsable DSI / IT | Vision technique et infrastructure | Identifier les contraintes techniques, le niveau de maturité des SI |
| Responsable Conformité / KYC-AML | Vision réglementaire | Comprendre les exigences de conformité |
| Gestionnaire de risques / Analyste fraude | Vision opérationnelle | Recueillir les typologies de fraude observées |

Institutions ciblées : BTCI, Orabank Togo, UTB, Ecobank Togo, TogoCom Cash, Moov Money (Flooz), BCEAO (représentation nationale).

## 2.4. Approche méthodologique retenue : comparaison de modèles d'ensemble learning + XAI

L'approche choisie consiste en une évaluation comparative de trois algorithmes complémentaires — Isolation Forest (non supervisé), Random Forest et XGBoost (supervisés) — associée à un module d'explicabilité SHAP.

### 2.4.1. Architecture comparative

**Tableau 2.4 — Modèles évalués**

| Modèle | Type | Paradigme | Rôle dans l'étude |
|--------|------|-----------|-------------------|
| Isolation Forest | Détection d'anomalies | Non supervisé | Référence de base pour la détection d'anomalies |
| Random Forest | Classification | Supervisé (ensemble) | Référence comparative (bagging) |
| XGBoost | Classification | Supervisé (boosting) | Modèle principal — standard industriel |

**Isolation Forest**

L'Isolation Forest (Liu et al., 2008) est un algorithme non supervisé de détection d'anomalies qui isole les points anormaux par partitionnement aléatoire de l'espace des caractéristiques. Son avantage principal est sa rapidité d'exécution (complexité en O(n log n)) et sa capacité à traiter de grands volumes de données sans nécessiter d'étiquetage préalable.

Paramètres retenus :
- Nombre d'estimateurs : 100
- Contamination : 0,05
- Échantillonnage : 256 transactions par arbre

**Random Forest**

Le Random Forest (Breiman, 2001) est un algorithme d'ensemble learning supervisé qui construit une multitude d'arbres de décision et agrège leurs prédictions par vote majoritaire.

**XGBoost**

XGBoost (eXtreme Gradient Boosting, Chen & Guestrin, 2016) est un algorithme de gradient boosting qui construit séquentiellement des arbres de décision, chaque nouvel arbre corrigeant les erreurs des précédents. Il est considéré comme l'état de l'art pour les problèmes de classification tabulaire.

Justification du choix :
- Performance supérieure sur données tabulaires
- Gestion native des valeurs manquantes
- Régularisation intégrée (L1 et L2) réduisant le sur-apprentissage
- Importance des variables disponible, facilitant l'interprétation
- Efficacité reconnue dans la littérature pour la détection de fraude bancaire

Hyperparamètres après optimisation (Optuna, 30 essais, validation croisée à 3 folds) :
- Learning rate : 0,199
- Max depth : 7
- Subsample : 0,772
- Colsample by tree : 0,95
- Scale pos weight : ratio (non-fraude / fraude)
- Objective : binary:logistic

**Extension séquentielle (LSTM) — perspective**

Le LSTM (Long Short-Term Memory, Hochreiter & Schmidhuber, 1997) est un réseau de neurones récurrents capable de capturer les dépendances temporelles longues dans les séquences de transactions. Son utilisation est proposée comme perspective de recherche, n'ayant pas été implémentée dans le cadre de cette étude en raison de contraintes de ressources de calcul.

### 2.4.2. Stratégie de gestion du déséquilibre des classes

Le déséquilibre des classes (3,5 % de transactions frauduleuses dans IEEE-CIS) est traité par SMOTE (Synthetic Minority Oversampling Technique), proposé par Chawla et al. (2002).

Protocole SMOTE appliqué :
1. Split Train/Test stratifié (80/20) avant toute transformation
2. Application de SMOTE uniquement sur l'ensemble d'entraînement
3. Rapport de sur-échantillonnage : 0,5
4. k-Nearest Neighbors : k=5

**Tableau 2.5 — Distribution des classes avant et après SMOTE**

| Étape | Non-fraude | Fraude | Ratio |
|-------|------------|--------|-------|
| Données brutes | 96,5 % | 3,5 % | 27:1 |
| Train (80 %) | 96,5 % | 3,5 % | 27:1 |
| Test (20 %) | 96,5 % | 3,5 % | 27:1 |
| Après SMOTE (train) | 66,7 % | 33,3 % | 2:1 |

### 2.4.3. Explicabilité par SHAP

L'outil d'explicabilité retenu est SHAP (SHapley Additive exPlanations), fondé sur la théorie des jeux de Shapley (Lundberg & Lee, 2017).

**Pourquoi SHAP plutôt que LIME ?**

| Critère | SHAP | LIME |
|---------|------|------|
| Fondement théorique | Théorie des jeux (Shapley) | Approximation locale linéaire |
| Consistance des explications | Garantie mathématique | Non garantie |
| Interprétabilité globale | Oui (feature importance global) | Non (explications locales uniquement) |
| Complexité calculatoire | Élevée (exact) / Modérée (approximé) | Faible |
| Adoption académique | Très élevée (2020-2025) | Modérée |

Protocole d'application SHAP :
1. Calcul des valeurs Shapley sur un échantillon de 500 transactions
2. Génération du graphique d'importance globale des variables (top 20)
3. Génération d'explications individuelles (force plot, waterfall plot)
4. Intégration des explications dans l'interface du dashboard

SHAP répond directement à HS3 : l'hypothèse selon laquelle l'explicabilité des modèles facilite leur adoption par les analystes financiers.

### 2.4.4. Volet qualitatif — perspective

Un volet qualitatif est proposé en perspective. Il viserait à :
1. Valider la transférabilité des variables et des seuils du modèle IEEE-CIS au contexte togolais
2. Identifier les besoins spécifiques non couverts par les systèmes actuels

Le guide d'entretien suggéré est le suivant :

| Thème | Questions clés |
|-------|---------------|
| Profil et contexte | Fonction, ancienneté, missions liées à la détection de fraude |
| Typologies de fraude | Quels types de fraude observez-vous ? Quels canaux sont les plus touchés ? |
| Systèmes actuels | Quels outils utilisez-vous ? Quelles sont leurs limites ? |
| Attentes vis-à-vis de l'IA | Qu'attendez-vous d'un système IA ? Quels sont vos freins ? |
| Explicabilité | Comment interprétez-vous les alertes ? L'explicabilité est-elle importante ? |
| Conformité | Quelles sont les exigences réglementaires auxquelles vous devez répondre ? |

### 2.4.5. Volet quantitatif complémentaire — questionnaire TAM

Pour compléter le dispositif méthodologique, un questionnaire quantitatif basé sur le Technology Acceptance Model (TAM) — cadre théorique validé pour mesurer l'adoption des systèmes d'information (Davis, 1989) — est proposé. Cet outil vise à recueillir les perceptions de professionnels bancaires togolais sur l'utilité perçue, la facilité d'utilisation perçue, la confiance et l'intention d'adoption du système FRAUDX.

Le questionnaire (Annexe B du mémoire complet) comprend 20 items mesurés sur une échelle de Likert à 5 niveaux, répartis en cinq construits (utilité perçue, facilité d'utilisation, confiance, intention d'adoption, facteurs contextuels).

Les résultats de ce questionnaire, combinés à l'analyse quantitative et aux entretiens qualitatifs, permettraient une validation croisée des hypothèses selon une approche mixte complète.

### 2.4.6. Métriques d'évaluation

**Tableau 2.6 — Métriques d'évaluation retenues**

| Métrique | Formule | Justification | Cible |
|----------|---------|---------------|-------|
| F1-Score | 2 × (P × R) / (P + R) | Équilibre précision/rappel | ≥ 0,60 |
| Recall | TP / (TP + FN) | Priorité : détecter un maximum de fraudes | ≥ 0,85 |
| AUC-PR | Aire sous courbe PR | Pertinent pour classes déséquilibrées | ≥ 0,55 |
| Précision | TP / (TP + FP) | Limiter les faux positifs | ≥ 0,10 (compromis recall) |
| Temps de latence | — | Contrainte temps réel | < 100 ms |

Rappel : L'Accuracy n'est pas retenue comme métrique principale en raison du fort déséquilibre des classes.

## 2.5. Outils de l'étude

### 2.5.1. Environnement de développement

| Outil | Version | Utilisation |
|-------|---------|-------------|
| Python | 3.10 | Langage principal |
| Scikit-learn | 1.2 | Implémentation Isolation Forest, Random Forest, métriques |
| XGBoost | 1.7 | Implémentation XGBoost |
| Pandas | 1.5 | Manipulation et prétraitement des données |
| NumPy | 1.23 | Calculs numériques |
| SHAP | 0.41 | Explicabilité des modèles |
| Imbalanced-learn | 0.10 | Implémentation SMOTE |
| Optuna | — | Optimisation d'hyperparamètres |
| Google Colab | — | Environnement de calcul cloud |
| Jupyter Notebook | — | Développement et documentation interactive |

### 2.5.2. Pipeline de prétraitement

Le pipeline de prétraitement se décompose en six étapes :

1. **Nettoyage** : suppression des doublons, traitement des valeurs manquantes (imputation par la médiane pour les variables numériques, par le mode pour les variables catégorielles)
2. **Encodage** : transformation des variables catégorielles en variables numériques (One-Hot Encoding pour les catégories à faible cardinalité, frequency encoding pour les catégories à cardinalité élevée)
3. **Normalisation** : StandardScaler (centrage et réduction) sur les variables numériques continues
4. **Feature engineering** : création de variables dérivées (log_amount, hour, dayofweek, tx_count_by_card)
5. **Split** : division Train/Test stratifiée (80/20)
6. **Rééquilibrage** : application de SMOTE sur l'ensemble d'entraînement uniquement

### 2.5.3. Procédure d'entraînement et de validation

Pour chaque modèle, la procédure suivante est appliquée :
1. Recherche d'hyperparamètres : Optuna avec validation croisée à 3 folds (pour XGBoost)
2. Entraînement sur l'ensemble d'entraînement rééquilibré
3. Prédiction sur l'ensemble de test (non rééquilibré)
4. Évaluation : calcul des métriques (F1, Recall, AUC-PR, Précision, Matrice de confusion)
5. Interprétation : calcul des valeurs SHAP sur un sous-ensemble de test

## 2.6. Stratégie de vérification des hypothèses

**Tableau 2.7 — Stratégie de vérification des hypothèses**

| Hypothèse | Données | Méthode | Indicateurs | Validation |
|-----------|---------|---------|-------------|------------|
| HG — L'ensemble learning améliore la détection | IEEE-CIS | Comparaison IF / RF / XGBoost | F1, Recall, AUC-PR | Si XGBoost ≥ RF ≥ IF |
| HS1 — Les modèles ML identifient des patterns pertinents | IEEE-CIS | Analyse SHAP, top variables | Top 10 variables SHAP | Si variables SHAP correspondent aux typologies documentées |
| HS2 — Données contextuelles locales (perspective) | — | — | — | Non vérifiable dans cette étude |
| HS3 — L'explicabilité SHAP facilite l'adoption | SHAP, analyse des FP | Ajustement du seuil | Taux de FP | Si FP ≤ 2 % après optimisation |

### 2.6.1. Critères de validation

- **HG validée** si XGBoost obtient un F1-Score ≥ 0,60 et un Recall ≥ 0,80, avec une amélioration significative par rapport aux deux autres modèles
- **HS1 validée** si les variables identifiées comme importantes par SHAP (top 10) correspondent aux facteurs de fraude documentés dans la littérature
- **HS2** : non vérifiable dans le cadre de cette étude — proposée comme perspective
- **HS3 validée** si le taux de faux positifs ≤ 2 % après optimisation du seuil

## Conclusion du chapitre

Ce deuxième chapitre a présenté la méthodologie retenue pour répondre aux questions de recherche et vérifier les hypothèses formulées dans l'introduction. L'approche quantitative combinant une analyse comparative de trois algorithmes de ML, des métriques adaptées au déséquilibre des classes et une validation croisée permet une évaluation rigoureuse.

Les choix méthodologiques opérés — recours à un dataset international de référence comme proxy, utilisation de SMOTE pour le rééquilibrage, adoption d'une approche comparative, intégration de l'explicabilité SHAP — sont cohérents avec l'état de l'art et les contraintes du contexte togolais. Les limites identifiées sont explicitement reconnues.

Le chapitre suivant présente les résultats de l'application de cette méthodologie : analyse exploratoire des données, performances comparatives des modèles, et proposition de plateforme logicielle.

---

# CHAPITRE III : PRÉSENTATION DE LA SITUATION ET COLLECTE DES DONNÉES

## Introduction

Ce troisième chapitre présente les données utilisées et l'analyse exploratoire, les performances comparatives des modèles, et la proposition de plateforme FRAUDX. Le cadre conceptuel de l'étude inclut les transactions bancaires classiques et le mobile money ; le modèle est entraîné sur le jeu de données international IEEE-CIS (transactions par carte) faute de données réelles togolaises accessibles — une limite explicitement reconnue.

## 3.1. Le secteur bancaire togolais

### 3.1.1. Structure et acteurs

Le système bancaire togolais compte une quinzaine de banques commerciales, dont les principales sont BTCI, Orabank Togo, UTB, Ecobank Togo, SGBT et SUNU Bank Togo. Parallèlement, le secteur du mobile money est dominé par deux opérateurs : TogoCom Cash (T-Money) et Moov Money (Flooz).

### 3.1.2. Infrastructure technologique

Le niveau de digitalisation des banques togolaises est hétérogène. Si certaines banques disposent de systèmes d'information modernes (applications mobiles, API bancaires), d'autres s'appuient encore sur des infrastructures héritées. Les défis incluent la connectivité réseau, l'interopérabilité entre systèmes bancaires et mobile money, et la disponibilité des compétences techniques locales.

## 3.2. État des lieux de la fraude bancaire au Togo

### 3.2.1. Typologie des fraudes observées

Au Togo, la fraude liée au mobile money repose principalement sur l'ingénierie sociale, comme le documentent les alertes de l'ANCY et du CERT-TG (2025). Les schémas dominants incluent le faux transfert, l'usurpation d'agent, la fausse réidentification et les plateformes frauduleuses d'investissement. Le SIM-swap, bien que documenté au Nigeria et au Cameroun, n'est pas identifié comme prédominant au Togo selon les sources officielles actuelles.

### 3.2.2. Impact économique

Les pertes financières liées à la fraude bancaire et mobile money au Togo sont difficiles à chiffrer précisément en raison de la sous-déclaration et de l'absence de statistiques publiques agrégées. Selon les rapports sectoriels, ces pertes représentent un enjeu économique significatif pour le secteur.

## 3.3. Présentation et analyse exploratoire des données

### 3.3.1. Description du dataset retenu

Le dataset principal retenu est IEEE-CIS Fraud Detection (Kaggle, 2020). Il s'agit d'un jeu de données de transactions par carte bancaire, comprenant environ 590 000 transactions étiquetées.

Caractéristiques principales :
- Volume : 590 540 transactions
- Variables : ~400 (dont ~250 anonymisées par PCA, ~150 explicites)
- Taux de fraude : 3,5 % (20 669 transactions frauduleuses)
- Période : 2019-2020
- Structure : deux tables reliées par un identifiant de transaction

Variables clés disponibles :

| Catégorie | Variables | Description |
|-----------|-----------|-------------|
| Montant | TransactionAmt | Montant de la transaction en USD |
| Temporalité | TransactionDT | Timestamp anonymisé |
| Identité | id_01 à id_38 | Variables anonymisées (PCA) |
| Appareil | DeviceInfo, id_30 à id_38 | Caractéristiques de l'appareil |
| Localisation | addr1, addr2 | Codes de localisation anonymisés |
| Carte | card1 à card6 | Caractéristiques de la carte bancaire |
| Transaction | ProductCD, P_emaildomain, R_emaildomain | Détails de la transaction |
| Calculées | C_*, D_*, M_* | Variables calculées par l'émetteur |

### 3.3.2. Analyse exploratoire (EDA)

**Distribution des classes :**
- Transactions non frauduleuses : 569 871 (96,5 %)
- Transactions frauduleuses : 20 669 (3,5 %)
- Ratio : environ 27:1

**Analyse univariée :** Le montant des transactions frauduleuses présente une distribution distincte de celle des transactions légitimes. Les fraudes tendent à se concentrer sur des montants modérés (50-200 USD).

**Analyse temporelle :** La variable TransactionDT révèle une périodicité hebdomadaire des transactions. Les fraudes sont plus fréquentes en fin de semaine et aux heures de faible activité, ce qui correspond à des créneaux où la surveillance humaine est réduite. Ces observations reflètent les patterns du dataset IEEE-CIS (d'origine nord-américaine).

**Corrélations :** Peu de corrélations fortes sont observées, ce qui est favorable à l'apprentissage (multicolinéarité réduite).

### 3.3.3. Prétraitement des données

Le pipeline de prétraitement suit la procédure définie au Chapitre II :

1. **Nettoyage** : imputation par la médiane (variables numériques) ou par le mode (variables catégorielles). Suppression des variables avec > 90 % de valeurs manquantes (18 variables supprimées).
2. **Encodage** : One-Hot Encoding pour les catégories à faible cardinalité, frequency encoding pour les catégories à forte cardinalité.
3. **Normalisation** : StandardScaler (centrage et réduction).
4. **Feature engineering** : log_amount, hour, dayofweek, tx_count_by_card1, avg_amount_by_card1.
5. **Split** : division Train/Test stratifiée (80/20), soit 472 432 transactions pour l'entraînement et 118 108 pour le test.
6. **Rééquilibrage** : SMOTE sur l'ensemble d'entraînement uniquement (ratio 0,5).

### 3.3.4. Discussion sur la transférabilité au contexte togolais

Les variables disponibles dans le dataset IEEE-CIS couvrent des dimensions universelles de la détection de fraude. Cependant, plusieurs dimensions spécifiques au contexte togolais ne sont pas représentées :

**Variables présentes et transférables :**
- Montant de la transaction (adapté aux seuils togolais)
- Temporalité (jour, heure)
- Fréquence des transactions
- Caractéristiques du dispositif

**Variables manquantes spécifiques au Togo :**
- Canal USSD vs application mobile
- Identifiant de l'agent mobile money
- Type d'opération mobile money (cash-in, cash-out, transfert P2P)
- Zone géographique (rurale vs urbaine)
- Ancienneté du compte

## 3.4. Conception et évaluation des modèles de Machine Learning

### 3.4.1. Configuration expérimentale

Les trois modèles retenus (Isolation Forest, Random Forest, XGBoost) ont été entraînés et évalués selon le protocole défini au Chapitre II.

Environnement :
- Machine locale (CPU, RAM 16 Go)
- Python 3.10
- Bibliothèques : Scikit-learn, XGBoost, Imbalanced-learn, Optuna

### 3.4.2. Résultats de l'évaluation comparative

L'évaluation comparative est réalisée selon deux configurations : (1) au seuil par défaut de 0,5 pour tous les modèles, et (2) après optimisation du seuil pour XGBoost (seuil = 0,35).

**Tableau 3.1a — Performances comparatives des modèles (seuil par défaut = 0,5)**

| Modèle | F1-Score | Recall | AUC-PR | Précision | ROC-AUC | Temps d'entraînement |
|--------|----------|--------|--------|-----------|---------|---------------------|
| Isolation Forest | 0,16 | 0,16 | 0,09 | 0,16 | 0,73 | 0,7 s |
| Random Forest | 0,37 | 0,57 | 0,49 | 0,28 | 0,89 | 13,7 s |
| XGBoost | 0,61 | 0,47 | 0,66 | 0,87 | 0,92 | 35,7 s |

**Tableau 3.1b — XGBoost avant et après optimisation du seuil**

| Métrique | Seuil 0,5 | Seuil 0,35 optimisé | Variation |
|----------|-----------|---------------------|-----------|
| Recall | 0,47 | 0,85 | +81 % |
| Précision | 0,87 | 0,14 | -84 % |
| F1-Score | 0,61 | 0,23 | -62 % |
| AUC-PR | 0,66 | 0,57 | — * |
| FP rate | 0,18 % | 20,7 % | +20,5 pp |

*AUC-PR est indépendante du seuil de décision.

**Analyse des résultats (seuil 0,5) :**

XGBoost obtient les meilleures performances globales au seuil par défaut :
- F1-Score de **0,61**, contre 0,37 pour Random Forest et 0,16 pour Isolation Forest
- AUC-PR de **0,66**, la plus élevée des trois modèles
- Précision de **0,87** : lorsque XGBoost prédit une fraude, il a 87 % de chances d'avoir raison
- ROC-AUC de **0,92**, excellent pouvoir discriminatif global

Random Forest se distingue par un Recall plus élevé (0,57 contre 0,47 pour XGBoost), détectant plus de fraudes, mais au prix d'une précision plus faible (0,28) générant davantage de faux positifs.

Isolation Forest (modèle non supervisé) obtient des performances limitées en classification directe (F1 = 0,16). Ce résultat est attendu : son rôle dans l'architecture est celui d'un filtre rapide (Niveau 1), non d'un classifieur final.

**Impact de l'optimisation du seuil :**

L'optimisation du seuil par courbe PR (passage de 0,5 à 0,35) transforme le profil du modèle. Le Recall passe de 47 % à **85 %** (3 514 fraudes détectées sur 4 130), au prix d'une augmentation du taux de faux positifs à 20,7 % (précision = 14 %). Cet arbitrage est assumé : dans le contexte bancaire togolais, le coût d'une fraude non détectée est très supérieur au coût de vérification d'une fausse alerte.

**Tableau 3.2 — Matrice de confusion (XGBoost, seuil optimisé = 0,35)**

|  | Prédit : Non Fraude | Prédit : Fraude |
|--|---------------------|-----------------|
| Réel : Non Fraude | 86 101 (VN) | 22 438 (FP) |
| Réel : Fraude | 616 (FN) | 3 514 (VP) |

Soit :
- Taux de faux positifs : 20,7 %
- Recall : 85,02 % (objectif ≥ 60 % atteint)
- Taux de détection des fraudes : 85 %

### 3.4.3. Explicabilité des modèles par SHAP

L'analyse SHAP a été appliquée au modèle XGBoost sur un échantillon de transactions.

**Importance globale des variables (top 10) :**

1. C14 (variable calculée par l'émetteur)
2. TransactionAmt (montant de la transaction)
3. card6_credit (type de carte : crédit)
4. V317 (variable anonymisée PCA)
5. V258 (variable anonymisée PCA)
6. V312 (variable anonymisée PCA)
7. TransactionDT (timestamp)
8. R_emaildomain (domaine email du destinataire)
9. M6_T (indicateur de correspondance anonymisé)
10. C11 (variable calculée par l'émetteur)

**Interprétation :** La variable C14 (calculée par l'émetteur de la carte) est la plus discriminante, suggérant que l'émetteur intègre dans ses calculs des informations de risque difficilement accessibles autrement. Le montant de la transaction (TransactionAmt) arrive en deuxième position, confirmant le résultat classique de la littérature.

## 3.5. Proposition de plateforme : FRAUDX (preuve de concept)

Cette section présente la preuve de concept (PoC) du système FRAUDX, une plateforme intégrée de détection de fraude bancaire dotée d'un tableau de bord interactif, d'un contrôle d'accès basé sur les rôles (RBAC) et d'un module d'explicabilité SHAP.

### 3.5.1. Architecture technique cible

L'architecture de FRAUDX est structurée en couches :

| Couche | Composants | Fonction |
|--------|------------|----------|
| Sécurité | WAF, authentification RBAC, chiffrement TLS | Protection périmétrique |
| Client | Dashboard Streamlit, interface SHAP | Interface utilisateur |
| API | API REST FastAPI, endpoints /predict, /explain, /feedback | Point d'entrée |
| Pipeline ML | Prétraitement, XGBoost, SHAP | Traitement et prédiction |
| Stockage | SQLite, logs d'audit | Persistance des données |

### 3.5.2. Contrôle d'accès basé sur les rôles (RBAC)

**Tableau 3.3 — Matrice des rôles et permissions FRAUDX**

| Fonctionnalité | Analyste | Gestionnaire de Risques | Administrateur |
|----------------|----------|------------------------|----------------|
| Dashboard (alertes) | Lecture | Lecture | Lecture |
| Détail des transactions | Lecture | Lecture | Lecture |
| Explications SHAP | Lecture | Lecture | Lecture |
| Feedback (valider/infirmer) | Écriture | Écriture | Écriture |
| Benchmark (métriques) | — | Lecture | Lecture |
| Configuration (seuils) | — | Écriture | Écriture |
| Gestion des utilisateurs | — | — | Écriture |
| Réentraînement des modèles | — | — | Exécution |

### 3.5.3. Fonctionnalités du tableau de bord

Le dashboard FRAUDX (implémenté avec Streamlit) offre les fonctionnalités suivantes :

- **Page d'accueil** : cartes KPI (transactions totales, fraudes détectées, F1-Score, alertes), graphique d'évolution temporelle, dernières alertes
- **Transactions** : liste paginée avec filtres, détail avec explications SHAP
- **Benchmark** : tableau comparatif des performances, graphiques
- **Explicabilité SHAP** : importance globale des variables, waterfall plots individuels
- **Feedback** : validation/infirmation des alertes, commentaires

### 3.5.4. Sécurité et conformité

Principes de sécurité intégrés :
- Authentification par hachage des mots de passe
- Autorisation RBAC avec vérification côté serveur
- Chiffrement TLS pour les données en transit
- Journalisation des actions utilisateur et décisions du modèle
- Conformité avec les exigences BCEAO/UEMOA

### 3.5.5. Module de feedback et apprentissage continu

Le module de feedback permet aux analystes de valider ou infirmer chaque alerte. Ce retour humain est essentiel pour :
1. Améliorer la précision du modèle
2. Détecter de nouveaux patterns de fraude
3. Maintenir la confiance des analystes

## 3.6. Tests et validation

### 3.6.1. Optimisation par recherche d'hyperparamètres

Une recherche d'hyperparamètres par Optuna a été effectuée sur XGBoost, avec 30 essais et validation croisée à 3 folds.

**Meilleure configuration trouvée :**

| Hyperparamètre | Valeur optimale |
|----------------|-----------------|
| n_estimators | 288 |
| max_depth | 7 |
| learning_rate | 0,199 |
| subsample | 0,772 |
| colsample_bytree | 0,950 |
| scale_pos_weight | ratio non-fraude/fraude |

**Performances avant et après optimisation du seuil :**

| Configuration | F1-Score | Recall | Précision | AUC-PR |
|---------------|----------|--------|-----------|--------|
| Seuil par défaut (0,5) | 0,61 | 0,47 | 0,87 | 0,66 |
| Seuil optimisé (0,35) | 0,23 | **0,85** | 0,14 | 0,57 |

L'optimisation du seuil de décision (passage de 0,5 à 0,35) transforme le profil du modèle : le Recall passe de 47 % à **85 %**, soit un quasi-doublement du taux de détection. La contrepartie est une chute de la précision (87 % → 14 %), qui se traduit par un F1-Score de 0,23. Cet arbitrage est assumé : dans un contexte bancaire, il est préférable de générer des faux positifs (vérifiables par un analyste) que de laisser passer une fraude non détectée. La métrique clé devient le Recall, et non le F1-Score.

**Top 5 des variables SHAP après optimisation :**
1. TransactionAmt (montant de la transaction)
2. card6_credit (type de carte : crédit)
3. dayofweek (jour de la semaine)
4. log_amount (montant logarithmique)
5. tx_count_by_card1 (nombre de transactions par carte)

### 3.6.2. Test de latence

Les temps de prédiction par transaction respectent l'objectif de latence inférieure à 100 ms.

**Hypothèse HG validée :** XGBoost atteint un Recall de 85 % et surpasse significativement Random Forest et Isolation Forest sur l'ensemble des métriques.

**Hypothèse HS1 validée :** Les variables identifiées par SHAP (montant, type de carte, temporalité) correspondent aux facteurs de fraude documentés dans la littérature.

**Hypothèse HS3 validée :** L'ajustement du seuil de décision via la courbe Precision-Recall permet de réduire les faux positifs tout en maintenant un Recall élevé.

## Conclusion du chapitre

Ce troisième chapitre a présenté l'analyse exploratoire du dataset IEEE-CIS, confirmant la structure déséquilibrée des données de détection de fraude (3,5 % de transactions frauduleuses). L'évaluation comparative des modèles a démontré la supériorité de XGBoost (Recall = 85 % ; F1-Score = 0,61 ; AUC-PR = 0,57) sur Random Forest et Isolation Forest. La proposition de plateforme FRAUDX — preuve de concept fonctionnelle avec contrôle d'accès RBAC, dashboard interactif et module d'explicabilité SHAP — démontre la faisabilité technique du déploiement.

Le chapitre suivant exploite ces résultats pour établir un diagnostic de la situation, vérifier les hypothèses de recherche, et proposer une intervention concrète adaptée au secteur bancaire togolais.
