# CHAPITRE II : MÉTHODOLOGIE DE L'ÉTUDE

**Introduction du chapitre**

Ce deuxième chapitre expose la méthodologie employée pour répondre aux questions de recherche formulées dans l'introduction générale et vérifier les hypothèses qui en découlent. Après avoir précisé la nature de l'étude et défini les variables mobilisées, nous présentons la population et l'échantillon retenus, l'approche méthodologique d'ensemble learning enrichie par l'explicabilité (XAI), ainsi que les outils de collecte, d'analyse et de développement utilisés. La stratégie de vérification des hypothèses est exposée en fin de chapitre, établissant le lien systématique entre chaque hypothèse, les données mobilisées et les indicateurs retenus.

---

## 2.1. Nature de l'étude

La présente étude s'inscrit dans une démarche **prospective** à **approche mixte** (qualitative et quantitative), de type **non expérimental à visée explicative**. Elle correspond au niveau **Compréhensif** selon la classification de FUNIBER (2017), dont l'objectif est de *Proposer* une solution fondée sur une analyse rigoureuse des données et de la littérature existante.

**Approche quantitative :** elle repose sur l'entraînement et l'évaluation comparative de trois algorithmes de Machine Learning (Isolation Forest, Random Forest, XGBoost) sur un jeu de données de transactions financières. Les performances sont mesurées à l'aide de métriques objectives (F1-Score, Recall, AUC-PR) et confrontées aux résultats rapportés dans la littérature.

**Approche qualitative :** elle consiste en une série d'entretiens semi-directifs auprès de responsables d'institutions bancaires et d'opérateurs de mobile money au Togo. Ces entretiens visent à comprendre les typologies de fraude locales, les limites des systèmes actuels, et les attentes en matière d'IA et d'explicabilité.

Le choix d'une approche mixte se justifie par la nature multidimensionnelle de la problématique : la détection de fraude par IA comporte à la fois une dimension technique (sélection et optimisation des algorithmes) et une dimension humaine et organisationnelle (acceptabilité, conformité, interprétabilité). Aucune de ces deux dimensions ne peut être appréhendée de manière isolée.

---

## 2.2. Variables de l'étude

### 2.2.1. Définition conceptuelle des variables

**Variables indépendantes (VI) :**
- **Types de transactions** : transactions bancaires classiques (cartes, virements) et transactions mobile money (USSD, application mobile)
- **Comportements utilisateurs** : fréquence des transactions, montants, canaux utilisés, localisation géographique
- **Données contextuelles locales** : spécificités du marché togolais (canaux USSD, agents mobile money, temporalité des transactions)

**Variables dépendantes (VD) :**
- **Taux de détection de fraude** : mesuré par le F1-Score, le Recall et l'AUC-PR
- **Taux de faux positifs** : proportion de transactions légitimes classées à tort comme frauduleuses
- **Temps de traitement** : latence de détection par transaction (cible inférieure à 100 ms)

**Variable modératrice :**
- **Interprétabilité des modèles** : mesurée via les scores SHAP (importance des variables) et la lisibilité des explications individuelles par des non-spécialistes

### 2.2.2. Limites et difficultés rencontrées

Plusieurs contraintes ont été identifiées en amont de l'étude :

1. **Indisponibilité des données bancaires togolaises réelles** : la confidentialité bancaire et l'absence de dataset public togolais imposent le recours à un dataset international de référence (IEEE-CIS Fraud Detection). Cette limite est explicitement assumée et traitée par un volet qualitatif de validation contextuelle.

2. **Fort déséquilibre des classes** : dans les jeux de données de détection de fraude, la proportion de transactions frauduleuses est généralement inférieure à 1 %. Ce déséquilibre rend l'Accuracy non pertinente comme métrique d'évaluation et nécessite des techniques de rééquilibrage (SMOTE).

3. **Ressources techniques limitées** : l'étude a été menée sans accès à une infrastructure de calcul spécialisée (GPU). Les modèles ont été entraînés sur Google Colab et sur une machine locale, ce qui a limité la complexité des architectures explorées.

4. **Accès restreint aux statistiques sectorielles** : les données agrégées sur la fraude bancaire au Togo ne sont pas publiquement disponibles. Les entretiens qualitatifs ont partiellement comblé cette lacune.

### 2.2.3. Opérationnalisation des variables et indicateurs

**Tableau 2.1 — Opérationnalisation des variables**

| Variable | Indicateur | Source de données | Unité de mesure |
|---|---|---|---|
| Types de transactions | Montant, canal, temporalité, localisation | IEEE-CIS, entretiens | Euros (montant), catégories (canal) |
| Comportements utilisateurs | Fréquence des transactions, intervalle inter-transactions | IEEE-CIS | Nombre, secondes |
| Performance de détection | F1-Score, Recall, AUC-PR | Résultats des modèles | Score [0-1] |
| Taux de faux positifs | FP / (FP + TN) | Matrice de confusion | Pourcentage |
| Latence de détection | Temps CPU par prédiction | Benchmark Python | Millisecondes |
| Interprétabilité | Score SHAP moyen, top-K variables | Analyse SHAP | Valeur Shapley |

**Indicateurs détaillés :**

- **F1-Score** : moyenne harmonique de la précision et du rappel. C'est la métrique principale retenue car elle penalise à la fois les faux positifs et les faux négatifs, ce qui est crucial en détection de fraude où les deux types d'erreur ont un coût.

- **AUC-PR (Area Under the Precision-Recall Curve)** : mesure la performance du modèle sur l'ensemble des seuils de décision. Contrairement à l'AUC-ROC, l'AUC-PR est plus informative sur les classes déséquilibrées car elle se concentre sur la classe minoritaire (fraude).

- **Recall (Rappel)** : proportion de transactions frauduleuses effectivement détectées. Un Recall élevé est prioritaire car un faux négatif (fraude non détectée) a un impact financier direct.

> ⚠️ **Note méthodologique** : l'Accuracy seule n'est pas pertinente sur des données fortement déséquilibrées. Avec 0,5 % de transactions frauduleuses, un modèle qui prédit "non fraude" pour toutes les transactions obtiendrait 99,5 % d'Accuracy sans rien détecter. Toutes les métriques utilisées dans cette étude sont donc adaptées au contexte du déséquilibre de classes.

### 2.2.4. Dynamique anticipée des variables

Conformément aux exigences du cadre opératoire (Assou, 2024), nous précisons ci-dessous la dynamique anticipée des variables et indicateurs, c'est-à-dire la direction et l'ampleur des changements attendus pour confirmer ou infirmer chaque hypothèse.

**Tableau 2.2 — Dynamique anticipée des variables et seuils de confirmation des hypothèses**

| Hypothèse | Variable indépendante | Variable dépendante | Dynamique anticipée | Seuil de confirmation | Seuil d'infirmation |
|---|---|---|---|---|---|
| HG | Architecture ensemble learning (3 niveaux) | F1-Score, Recall, AUC-PR | Hausse des métriques vs modèle unique (RF seul) | XGBoost F1 ≥ 0,85 | XGBoost F1 < 0,75 ou IF > XGBoost |
| HS1 | Modèles ML (IF, XGBoost) | Recall, correspondance SHAP/littérature | Recall ≥ 90%, top-10 SHAP aligné sur littérature | Recall ≥ 0,90 et ≥ 7/10 variables SHAP concordantes | Recall < 0,80 ou < 4/10 variables concordantes |
| HS2* | Données contextuelles locales | Pertinence perçue par répondants | ≥ 70% des répondants valident la transférabilité | ≥ 70% de validation qualitative | < 50% de validation qualitative |
| HS3 | Module SHAP (explicabilité) | Taux de FP, utilité perçue | Baisse du FP, ≥ 70% jugent SHAP utile | FP ≤ 2% et ≥ 70% satisfaction utilisateur | FP > 5% ou < 50% satisfaction |

> *HS2 est marquée comme non vérifiable dans le cadre de cette étude (cf. Ch.IV). La dynamique anticipée est néanmoins précisée pour orienter les travaux futurs.

**Règles de décision pour la confirmation des hypothèses :**

- **HG confirmée** si XGBoost atteint un F1-Score ≥ 0,85 **et** un Recall ≥ 0,90 **et** surpasse significativement Random Forest (test de McNemar, p < 0,05)
- **HS1 confirmée** si le Recall ≥ 0,90 **et** qu'au moins 7 des 10 variables les plus importantes selon SHAP correspondent aux facteurs de fraude documentés dans la littérature et les entretiens
- **HS2** : la confirmation de cette hypothèse nécessite un jeu de données local qui n'est pas disponible dans le cadre de cette étude — elle est proposée comme perspective
- **HS3 confirmée** si le taux de faux positifs ≤ 2 % **et** qu'au moins 70 % des répondants aux entretiens jugent les explications SHAP utiles et compréhensibles

---

## 2.3. Population et échantillon

### 2.3.1. Population cible

La population cible de cette étude est constituée de **l'ensemble des transactions bancaires et mobile money effectuées au Togo entre 2020 et 2024**. Cette période correspond à la phase de digitalisation bancaire accélérée et de croissance exponentielle du mobile money dans le pays.

### 2.3.2. Échantillon quantitatif

Aucune donnée bancaire togolaise réelle n'étant accessible pour des raisons de confidentialité, l'étude s'appuie sur un **dataset public de référence international** :

- **Dataset principal** : **IEEE-CIS Fraud Detection** (Kaggle, 2020) — Environ 590 000 transactions, dont 3,5 % frauduleuses. Ce dataset, issu d'une compétition Kaggle organisée par IEEE Computational Intelligence Society, est largement utilisé dans la littérature récente (Dhieb et al., 2020 ; Kim et al., 2021 ; Ogunleye et al., 2022). Il présente l'avantage d'être réaliste, avec une structure proche des données bancaires réelles, et d'inclure des variables temporelles et catégorielles riches.

- **Dataset secondaire** : **Credit Card Fraud Dataset** (ULB Machine Learning Group, Dal Pozzolo et al., 2015) — Environ 284 807 transactions, dont 0,17 % frauduleuses. Utilisé comme référence complémentaire pour valider la robustesse des modèles sur un déséquilibre plus marqué.

> ⚠️ **Limite assumée** : Ces datasets étant constitués de transactions européennes et nord-américaines, ils ne capturent pas nativement les spécificités du contexte togolais (mobile money, fraude par USSD, SIM swap, faible bancarisation). Cette limite est traitée selon deux axes :
>
> 1. **Validation qualitative** : les entretiens menés auprès des responsables bancaires togolais (cf. 2.3.3) permettent de valider ou d'invalider la pertinence des variables et des seuils issus des modèles entraînés sur IEEE-CIS.
> 2. **Perspective de prolongement** : l'utilisation d'un jeu de données togolais réel, obtenu via un partenariat avec une banque ou un opérateur de mobile money, est proposée comme perspective directe (cf. Conclusion générale).

**Tableau 2.2 — Caractéristiques des datasets retenus**

| Caractéristique | IEEE-CIS Fraud Detection | Credit Card Fraud (ULB) |
|---|---|---|
| Nombre de transactions | ~590 000 | ~284 807 |
| Taux de fraude | 3,5 % | 0,17 % |
| Nombre de variables | ~400 (dont ~250 anonymisées) | 30 (PCA) |
| Période | 2019-2020 | 2013 |
| Origine géographique | États-Unis/Europe | Europe |
| Type de transactions | Cartes, virements | Cartes de crédit |

### 2.3.3. Échantillon qualitatif

L'échantillon qualitatif est constitué de **5 à 8 responsables d'institutions bancaires et d'opérateurs de mobile money** basés à Lomé (Togo). La technique d'échantillonnage retenue est **raisonnée** (choix délibéré des participants en fonction de leur profil et de leur expertise).

**Profils visés :**

| Profil | Rôle | Objectif de l'entretien |
|---|---|---|
| Responsable DSI / IT | Vision technique et infrastructure | Identifier les contraintes techniques, le niveau de maturité des SI, les besoins en infrastructure |
| Responsable Conformité / KYC-AML | Vision réglementaire | Comprendre les exigences de conformité, les processus AML/KYC, les attentes des régulateurs |
| Gestionnaire de risques / Analyste fraude | Vision opérationnelle | Recueillir les typologies de fraude observées, les limites des outils actuels, les besoins en explicabilité |

**Institutions ciblées :**
- Banques commerciales : BTCI, Orabank Togo, UTB, Ecobank Togo, SGBT
- Opérateurs de mobile money : TogoCom Cash, Moov Money (Flooz)
- Régulateur : BCEAO (représentation nationale), Cellule Nationale de Renseignement Financier (CNRF)

---

## 2.4. Approche méthodologique retenue : Ensemble Learning + XAI

L'approche choisie combine **trois niveaux algorithmiques complémentaires** avec un **module d'explicabilité (XAI)** , selon le principe de l'ensemble learning supervisé renforcé par une détection d'anomalies non supervisée.

### 2.4.1. Architecture à trois niveaux

**Tableau 2.3 — Architecture des modèles**

| Niveau | Modèle | Type | Rôle | Entrée | Sortie |
|---|---|---|---|---|---|
| Niveau 1 | Isolation Forest | Non supervisé | Filtrage rapide des anomalies évidentes | Transactions brutes | Score d'anomalie |
| Niveau 2 | XGBoost | Supervisé (gradient boosting) | Classification fine fraude / non-fraude | Caractéristiques enrichies | Probabilité de fraude |
| Niveau 3 | LSTM (optionnel) | Deep Learning séquentiel | Analyse des patterns temporels | Séquences de transactions | Détection de séquences suspectes |

**Niveau 1 — Isolation Forest**

L'Isolation Forest (Liu et al., 2008) est un algorithme non supervisé de détection d'anomalies qui isole les points anormaux par partitionnement aléatoire de l'espace des caractéristiques. Son avantage principal est sa rapidité d'exécution (complexité en O(n log n)) et sa capacité à traiter de grands volumes de données sans nécessiter d'étiquetage préalable.

Dans notre architecture, l'Isolation Forest joue le rôle de **filtre rapide** : les transactions identifiées comme anomalies évidentes sont immédiatement transmises au module d'alerte, tandis que les cas ambigus (scores d'anomalie intermédiaires) sont transmis au Niveau 2 pour analyse approfondie.

**Paramètres retenus :**
- Nombre d'estimateurs : 100
- Contamination : 0,05 (proportion attendue d'anomalies)
- Échantillonnage : 256 transactions par arbre
- Seuil de transfert vers Niveau 2 : score d'anomalie ∈ [0,5 ; 0,75]

**Niveau 2 — XGBoost**

XGBoost (eXtreme Gradient Boosting, Chen & Guestrin, 2016) est un algorithme de gradient boosting qui construit séquentiellement des arbres de décision, chaque nouvel arbre corrigeant les erreurs des précédents. Il est considéré comme l'état de l'art pour les problèmes de classification tabulaire et a été largement adopté dans l'industrie financière pour la détection de fraude (Carmona et al., 2019 ; Jurgovsky et al., 2018).

**Justification du choix :**
- Performance supérieure sur données tabulaires par rapport à Random Forest (vitesse d'entraînement, précision)
- Gestion native des valeurs manquantes
- Régularisation intégrée (L1 et L2) réduisant le sur-apprentissage
- Importance des variables disponible, facilitant l'interprétation
- Efficacité reconnue dans la littérature pour la détection de fraude bancaire

**Hyperparamètres optimisés** (validation croisée à 5 folds) :
- Learning rate : 0,05
- Max depth : 6
- Subsample : 0,8
- Colsample by tree : 0,8
- Scale pos weight : ratio (non-fraude / fraude) pour gérer le déséquilibre
- Objective : binary:logistic
- Evaluation metric : AUC-PR

**Niveau 3 — LSTM (optionnel)**

Le LSTM (Long Short-Term Memory, Hochreiter & Schmidhuber, 1997) est un réseau de neurones récurrents capable de capturer les dépendances temporelles longues dans les séquences de transactions. Il est proposé comme niveau optionnel pour l'analyse des patterns temporels complexes, tels que :
- Les séquences de petites transactions suivies d'un retrait important (cramming)
- Les intervalles anormalement courts entre transactions successives
- Les changements brusques de comportement sur une fenêtre temporelle glissante

> **Note** : Le niveau LSTM est qualifié d'optionnel car son entraînement nécessite des ressources de calcul conséquentes (GPU) qui n'étaient pas disponibles dans le cadre de cette étude. Son inclusion est recommandée pour une implémentation en production.

### 2.4.2. Stratégie de gestion du déséquilibre des classes

Le déséquilibre des classes (moins de 1 % de transactions frauduleuses) est traité par **SMOTE (Synthetic Minority Oversampling Technique)** , proposé par Chawla et al. (2002). SMOTE génère des exemples synthétiques de la classe minoritaire par interpolation entre les échantillons existants, plutôt que par simple duplication, ce qui réduit le risque de sur-apprentissage.

**Protocole SMOTE appliqué :**
1. Split Train/Test stratifié (80/20) avant toute transformation pour éviter la contamination des données de test
2. Application de SMOTE uniquement sur l'ensemble d'entraînement
3. Rapport de sur-échantillonnage : 0,5 (la classe minoritaire passe à 50 % de la classe majoritaire)
4. k-Nearest Neighbors : k=5 pour la génération des voisins synthétiques

**Tableau 2.4 — Distribution des classes avant et après SMOTE**

| Étape | Non-fraude | Fraude | Ratio |
|---|---|---|---|
| Données brutes | 96,5 % | 3,5 % | 27:1 |
| Train (80%) | 96,5 % | 3,5 % | 27:1 |
| Test (20%) | 96,5 % | 3,5 % | 27:1 |
| Après SMOTE (train) | 66,7 % | 33,3 % | 2:1 |

### 2.4.3. Explicabilité par SHAP

L'outil d'explicabilité retenu est **SHAP (SHapley Additive exPlanations)** , fondé sur la théorie des jeux de Shapley (Lundberg & Lee, 2017). SHAP attribue à chaque variable une valeur d'importance (valeur Shapley) qui représente sa contribution à l'écart entre la prédiction du modèle et la prédiction moyenne.

**Pourquoi SHAP plutôt que LIME ?**

| Critère | SHAP | LIME |
|---|---|---|
| Fondement théorique | Théorie des jeux (Shapley) | Approximation locale linéaire |
| Consistance des explications | Garantie mathématique | Non garantie |
| Interprétabilité globale | Oui (feature importance global) | Non (explications locales uniquement) |
| Complexité calculatoire | Élevée (exact) / Modérée (approximé) | Faible |
| Adoption académique (détection fraude) | Très élevée (2020-2025) | Modérée |

**Protocole d'application SHAP :**
1. Calcul des valeurs Shapley sur un échantillon de 500 transactions (compromis précision/temps de calcul)
2. Génération du graphique d'importance globale des variables (top 20)
3. Génération d'explications individuelles (force plot, waterfall plot) pour les transactions jugées frauduleuses
4. Intégration des explications dans l'interface du dashboard (Chapitre III)

SHAP répond directement à **HS3** : l'hypothèse selon laquelle l'interprétabilité des modèles facilite leur adoption par les analystes financiers et les gestionnaires de risques bancaires togolais.

### 2.4.4. Volet qualitatif : entretiens semi-directifs

Les entretiens semi-directifs constituent le volet qualitatif de l'étude. Leur objectif est double :
1. **Valider la transférabilité** des variables et des seuils du modèle IEEE-CIS au contexte togolais
2. **Identifier les besoins spécifiques** non couverts par les systèmes actuels

**Guide d'entretien (structure) :**

| Thème | Questions clés | Durée estimée |
|---|---|---|
| Profil et contexte | Fonction, ancienneté, missions liées à la détection de fraude | 5 min |
| Typologies de fraude | Quels types de fraude observez-vous ? Quels canaux sont les plus touchés ? | 10 min |
| Systèmes actuels | Quels outils utilisez-vous ? Quelles sont leurs limites ? | 10 min |
| Attentes vis-à-vis de l'IA | Qu'attendez-vous d'un système IA ? Quels sont vos freins ? | 10 min |
| Explicabilité | Comment interprétez-vous les alertes ? L'explicabilité est-elle importante ? | 10 min |
| Conformité | Quelles sont les exigences réglementaires auxquelles vous devez répondre ? | 5 min |

**Méthode d'analyse :** codage thématique. Les entretiens sont retranscrits, puis analysés par identification de thèmes récurrents (typologies de fraude, limites techniques, besoins en explicabilité, contraintes réglementaires). Les résultats du codage alimentent directement :
- Le Chapitre III (section 3.2 — État des lieux de la fraude au Togo)
- Le Chapitre IV (section 4.1 — Vérification des hypothèses HS2 et HS3)

### 2.4.5. Métriques d'évaluation

Le choix des métriques d'évaluation est guidé par la nature déséquilibrée des données et les objectifs opérationnels de la détection de fraude.

**Tableau 2.5 — Métriques d'évaluation retenues**

| Métrique | Formule | Justification | Cible |
|---|---|---|---|
| **F1-Score** | 2 × (P × R) / (P + R) | Équilibre précision/rappel, penalise FP et FN | ≥ 0,85 |
| **Recall** | TP / (TP + FN) | Priorité : détecter un maximum de fraudes (minimiser FN) | ≥ 0,90 |
| **AUC-PR** | Aire sous courbe PR | Pertinent pour classes déséquilibrées | ≥ 0,70 |
| **Précision** | TP / (TP + FP) | Limiter les faux positifs (économie d'effort analyste) | ≥ 0,80 |
| **Temps de latence** | — | Contrainte temps réel | < 100 ms |

> **Rappel** : L'Accuracy n'est pas retenue comme métrique principale en raison du fort déséquilibre des classes. Avec 0,5 % de transactions frauduleuses, un modèle prédisant systématiquement "non fraude" obtiendrait 99,5 % d'Accuracy sans rien détecter.

---

## 2.5. Outils de l'étude

### 2.5.1. Environnement de développement

| Outil | Version | Utilisation |
|---|---|---|
| Python | 3.10 | Langage principal |
| Scikit-learn | 1.2 | Implémentation Isolation Forest, Random Forest, métriques |
| XGBoost | 1.7 | Implémentation XGBoost |
| TensorFlow/Keras | 2.12 | Implémentation LSTM (optionnel) |
| Pandas | 1.5 | Manipulation et prétraitement des données |
| NumPy | 1.23 | Calculs numériques |
| SHAP | 0.41 | Explicabilité des modèles |
| Imbalanced-learn | 0.10 | Implémentation SMOTE |
| Google Colab | — | Environnement de calcul cloud (GPU disponible) |
| Jupyter Notebook | — | Développement et documentation interactive |

### 2.5.2. Pipeline de prétraitement

Le pipeline de prétraitement se décompose en six étapes :

1. **Nettoyage** : suppression des doublons, traitement des valeurs manquantes (imputation par la médiane pour les variables numériques, par le mode pour les variables catégorielles)
2. **Encodage** : transformation des variables catégorielles en variables numériques (One-Hot Encoding pour les catégories à faible cardinalité, Label Encoding pour les catégories à cardinalité élevée)
3. **Normalisation** : StandardScaler (centrage et réduction) sur les variables numériques continues
4. **Feature engineering** : création de variables dérivées (montant moyen par utilisateur, fréquence des transactions par période, intervalle depuis la dernière transaction, etc.)
5. **Split** : division Train/Test stratifiée (80/20)
6. **Rééquilibrage** : application de SMOTE sur l'ensemble d'entraînement uniquement

### 2.5.3. Procédure d'entraînement et de validation

Pour chaque modèle, la procédure suivante est appliquée :

1. **Recherche d'hyperparamètres** : GridSearchCV ou RandomizedSearchCV avec validation croisée à 5 folds
2. **Entraînement** : sur l'ensemble d'entraînement rééquilibré
3. **Prédiction** : sur l'ensemble de test (non rééquilibré, représentatif de la distribution réelle)
4. **Évaluation** : calcul des métriques (F1, Recall, AUC-PR, Précision, Matrice de confusion)
5. **Interprétation** : calcul des valeurs SHAP sur un sous-ensemble de test (500 transactions)

---

## 2.6. Stratégie de vérification des hypothèses

Le tableau ci-dessous établit le lien systématique entre chaque hypothèse, les données mobilisées, la méthode d'analyse et les indicateurs retenus.

**Tableau 2.6 — Stratégie de vérification des hypothèses**

| Hypothèse | Données | Méthode | Indicateurs | Validation |
|---|---|---|---|---|
| **HG** — L'ensemble learning améliore la détection | IEEE-CIS, ULB | Comparaison IF / RF / XGBoost | F1, Recall, AUC-PR | Si XGBoost ≥ RF ≥ IF |
| **HS1** — Les modèles ML identifient des patterns de fraude pertinents | IEEE-CIS | Analyse SHAP, top variables | Top 10 variables SHAP | Si variables SHAP correspondent aux typologies de fraude documentées |
| **HS2** — L'intégration de données contextuelles améliore la précision (qualitatif) | Entretiens | Codage thématique | Thèmes : adéquation dataset/variables vs réalité togolaise | Si ≥ 70% des répondants valident la pertinence des variables |
| **HS3** — L'explicabilité SHAP facilite l'adoption | Entretiens | Codage thématique | Thèmes : utilité perçue, compréhension, confiance | Si ≥ 70% des répondants jugent SHAP utile |

### 2.6.1. Critères de validation

- **HG validée** si XGBoost obtient un F1-Score ≥ 0,85 et un Recall ≥ 0,90, avec une amélioration significative par rapport aux deux autres modèles (test statistique de McNemar, α = 0,05)
- **HS1 validée** si les variables identifiées comme importantes par SHAP (top 10) correspondent aux facteurs de fraude documentés dans la littérature et dans les entretiens
- **HS2 validée** si l'analyse qualitative confirme que les variables du dataset IEEE-CIS couvrent significativement les dimensions pertinentes du contexte togolais, et identifie clairement les lacunes résiduelles
- **HS3 validée** si au moins 70 % des répondants aux entretiens considèrent les explications SHAP comme utiles et compréhensibles

---

## Conclusion du chapitre

Ce deuxième chapitre a présenté la méthodologie retenue pour répondre aux questions de recherche et vérifier les hypothèses formulées dans l'introduction. L'approche mixte combinant une analyse quantitative rigoureuse (trois algorithmes de ML, métriques adaptées au déséquilibre des classes, validation croisée) et une analyse qualitative (entretiens semi-directifs, codage thématique) permet une appréhension complète de la problématique.

Les choix méthodologiques opérés — recours à un dataset international de référence comme proxy, utilisation de SMOTE pour le rééquilibrage, adoption de l'ensemble learning à trois niveaux, intégration de l'explicabilité SHAP — sont cohérents avec l'état de l'art et les contraintes du contexte togolais. Les limites identifiées (indisponibilité des données réelles, ressources de calcul limitées) sont explicitement reconnues et traitées dans le dispositif de recherche.

Le chapitre suivant présente les résultats de l'application de cette méthodologie : état des lieux du secteur bancaire togolais, analyse exploratoire des données, performances comparatives des modèles, et proposition de plateforme logicielle.
