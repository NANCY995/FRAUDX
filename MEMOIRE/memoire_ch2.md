# CHAPITRE II : MÉTHODOLOGIE DE L'ÉTUDE

**Introduction**

Au cœur de toute démarche scientifique rigoureuse se trouve une méthodologie claire et structurée, garante de la cohérence et de la fiabilité des résultats obtenus. Ce chapitre détaille l'approche méthodologique qui a guidé cette étude. Il présente la nature de la recherche, les variables retenues, les indicateurs de mesure, ainsi que les outils mobilisés pour la collecte et l'analyse des données. Cette approche vise à garantir la transparence et la rigueur scientifique de la démarche. Elle montre comment chaque choix méthodologique a contribué au test des hypothèses et à l'atteinte des objectifs de l'étude.

---

## II.1. Nature de l'étude

Cette recherche adopte une approche **quasi-expérimentale, exploratoire et descriptive**, intégrant des dimensions qualitatives et quantitatives pour appréhender de manière complète le phénomène étudié.

**Dimension quasi-expérimentale :**

L'étude est qualifiée de quasi-expérimentale car elle repose sur l'évaluation comparative de trois algorithmes de Machine Learning (Isolation Forest, Random Forest, XGBoost) dans un environnement contrôlé reproduisant les conditions d'utilisation réelles d'un système de détection de fraude bancaire. Cette approche diffère d'une expérimentation directe au sein d'une institution bancaire togolaise : les tests sont conduits par le chercheur sur un jeu de données international de référence (IEEE-CIS), permettant d'observer les effets potentiels de l'ensemble learning sur la performance de détection sans interférer avec le fonctionnement opérationnel d'un établissement financier (Hernández Sampieri et al., 2014).

**Dimension exploratoire :**

Le caractère exploratoire de la recherche découle de la documentation encore limitée sur l'application de l'IA explicable (XAI) à la détection de fraude dans le contexte des pays africains, et plus particulièrement au Togo. L'utilisation de SHAP (SHapley Additive exPlanations) pour rendre les décisions des modèles interprétables par des analystes financiers non spécialistes constitue un domaine émergent où les retours d'expérience pratiques demeurent rares. L'objectif consiste à identifier, par une démarche inductive, les premières observations et contraintes rencontrées, sans prétendre à une généralisation immédiate des résultats (Creswell & Poth, 2017).

**Dimension descriptive :**

L'étude revêt également un caractère descriptif en se concentrant sur l'observation et la mesure systématique d'indicateurs opérationnels : F1-Score, Recall, AUC-PR, taux de faux positifs, latence de détection et valeurs SHAP d'importance des variables. L'approche ne vise pas à valider une théorie préexistante, mais à établir un diagnostic structuré et détaillé des performances du système proposé.

**Approche méthodologique mixte :**

La méthodologie articule des dimensions qualitatives et quantitatives à travers trois phases complémentaires de collecte de données :

- **Phase quantitative** :
  - Entraînement et évaluation de trois modèles de Machine Learning (Isolation Forest, Random Forest, XGBoost) sur le dataset IEEE-CIS Fraud Detection (~590 000 transactions)
  - Optimisation des hyperparamètres par validation croisée (5 folds) avec recherche automatisée (Optuna)
  - Mesures de performance : F1-Score, Recall, AUC-PR, précision, temps de latence
  - Analyse d'explicabilité : calcul des valeurs SHAP (importance globale et individuelle)

- **Phase qualitative** :
  - Entretiens semi-directifs avec 5 à 8 responsables d'institutions bancaires et d'opérateurs de mobile money au Togo
  - Objectif : comprendre les typologies de fraude locales, les limites des systèmes actuels, et les attentes en matière d'IA et d'explicabilité
  - Analyse par codage thématique des transcriptions

Cette articulation en phases complémentaires permet d'obtenir une vision complète et triangulée : validation technique des modèles (quantitatif), compréhension du contexte local (qualitatif), et adéquation entre les variables du modèle et les réalités du terrain. Le choix d'une approche mixte se justifie par la nature multidimensionnelle de la problématique : la détection de fraude par IA comporte à la fois une dimension technique (sélection et optimisation des algorithmes) et une dimension humaine et organisationnelle (acceptabilité, conformité, interprétabilité). Aucune de ces deux dimensions ne peut être appréhendée de manière isolée.

---

## II.2. Variables de l'étude

### II.2.1. Définition conceptuelle des variables

Dans le cadre de cette étude, nous avons identifié et défini un ensemble de variables directement issues de notre hypothèse générale, formulée pour répondre à la problématique posée. Ces variables sont essentielles car elles permettent de traduire en éléments observables et mesurables l'effet attendu de l'introduction d'un système d'ensemble learning et d'explicabilité SHAP dans la détection de fraude bancaire.

Comme le rappellent Hernández Sampieri et al. (2014) et Creswell & Poth (2017), toute recherche empirique nécessite de passer d'une hypothèse théorique à un cadre opérationnel, où chaque dimension du phénomène est représentée par une variable associée à des indicateurs spécifiques. La définition claire et structurée des variables, ainsi que le choix d'indicateurs pertinents, visent à garantir la validité, la transparence et la reproductibilité de notre démarche scientifique.

**Variable explicative (indépendante) :**

- **Architecture d'ensemble learning à trois niveaux** : Cette variable désigne l'introduction dans le processus de détection de fraude d'un système combinant Isolation Forest (Niveau 1 — filtrage non supervisé), XGBoost (Niveau 2 — classification supervisée) et LSTM optionnel (Niveau 3 — analyse séquentielle), enrichi par un module d'explicabilité SHAP.
  - *Indicateurs* :
    - Existence d'une architecture opérationnelle à trois niveaux
    - Nombre de modèles entraînés et déployés
    - Taux de couverture des transactions par le pipeline de détection
    - Qualité des explications SHAP générées (couverture, cohérence)

**Variables expliquées (dépendantes) :**

- **Performance de détection de fraude** : Capacité du système à identifier correctement les transactions frauduleuses tout en minimisant les fausses alertes.
  - *Indicateurs* :
    - F1-Score (moyenne harmonique précision/rappel)
    - Recall (taux de fraude détectée)
    - AUC-PR (aire sous la courbe Precision-Recall)
    - Taux de faux positifs

- **Efficacité opérationnelle** : Capacité du système à traiter les transactions en temps réel avec une latence compatible avec les exigences du secteur bancaire.
  - *Indicateurs* :
    - Temps de latence moyen par transaction (ms)
    - Temps d'entraînement des modèles

- **Interprétabilité des décisions** : Capacité du système à fournir des explications compréhensibles des décisions de détection, mesurée via les valeurs SHAP.
  - *Indicateurs* :
    - Score SHAP moyen par variable
    - Top-K variables les plus importantes
    - Cohérence des explications avec la littérature

### II.2.2. Limites et difficultés

Comme toute recherche appliquée conduite dans un cadre limité, cette étude présente plusieurs contraintes et difficultés méthodologiques qu'il est important de reconnaître pour interpréter correctement ses résultats.

- **Indisponibilité des données bancaires togolaises réelles** : la confidentialité bancaire et l'absence de dataset public togolais imposent le recours à un dataset international de référence (IEEE-CIS Fraud Detection). Cette limite est explicitement assumée et traitée par un volet qualitatif de validation contextuelle.

- **Fort déséquilibre des classes** : dans les jeux de données de détection de fraude, la proportion de transactions frauduleuses est généralement inférieure à 1 %. Ce déséquilibre rend l'Accuracy non pertinente comme métrique d'évaluation et nécessite des techniques de rééquilibrage (SMOTE).

- **Ressources techniques limitées** : l'étude a été menée sans accès à une infrastructure de calcul spécialisée (GPU). Les modèles ont été entraînés sur Google Colab et sur une machine locale, ce qui a limité la complexité des architectures explorées et justifie le caractère optionnel du niveau LSTM.

- **Accès restreint aux statistiques sectorielles** : les données agrégées sur la fraude bancaire au Togo ne sont pas publiquement disponibles. Le volet qualitatif (entretiens) n'a pu être réalisé dans le cadre de cette étude.

- **Biais méthodologique potentiel** : dans le volet qualitatif, les entretiens reposent sur des déclarations subjectives des répondants, qui peuvent être influencées par des biais de désirabilité sociale ou des contraintes institutionnelles.

Ces limites n'invalident pas la démarche, mais soulignent que les conclusions devront être comprises comme des résultats préliminaires, issus d'un test exploratoire et technique, et non comme une validation définitive d'un déploiement en conditions réelles.

### II.2.3. Utilisation des variables

Les variables définies précédemment et leurs indicateurs associés servent de base à l'ensemble du protocole expérimental. Elles orientent la collecte, l'observation et l'analyse des données, permettant de vérifier de manière concrète les hypothèses formulées.

L'opérationnalisation de ces variables s'articule autour d'une stratégie de mesure à plusieurs dimensions. La variable explicative, correspondant à l'architecture d'ensemble learning, constitue la condition introduite volontairement dans le processus, dont nous cherchons à observer les effets. Parallèlement, les variables dépendantes — performance de détection, efficacité opérationnelle et interprétabilité — servent à mesurer les effets concrets de cette intervention.

**Tableau II.1 — Opérationnalisation des variables**

| Variable | Indicateur | Source de données | Unité de mesure |
|---|---|---|---|
| Architecture ensemble learning | Modèles entraînés (IF, XGBoost, LSTM) | Logs d'entraînement | Nombre, configuration |
| Performance de détection | F1-Score, Recall, AUC-PR | Résultats des modèles | Score [0-1] |
| Efficacité opérationnelle | Latence par transaction | Benchmark Python | Millisecondes |
| Interprétabilité | Score SHAP moyen, top-K variables | Analyse SHAP | Valeur Shapley |
| Contexte local | Typologies de fraude, besoins | Entretiens qualitatifs | Thèmes codés |

Les modalités d'exploitation de ces variables combinent différentes approches complémentaires. D'une part, des **mesures quantitatives objectives** sont collectées : F1-Score, Recall, AUC-PR, temps de latence, valeurs SHAP. D'autre part, des **évaluations qualitatives subjectives** sont réalisées à travers les entretiens semi-directifs, dont les transcriptions sont analysées par codage thématique. Enfin, des **observations techniques** sont effectuées à travers l'analyse des logs système et la mesure continue des performances du prototype.

La combinaison de ces différents types de données permet d'identifier si l'introduction de l'architecture d'ensemble learning produit effectivement un effet positif sur la détection de fraude, et si l'explicabilité SHAP facilite l'adoption par les utilisateurs finaux. Cette approche multidimensionnelle vise également à préciser la nature et l'ampleur de cet effet, même dans un contexte de données proxy et sur une durée limitée.

**Tableau II.2 — Dynamique anticipée des variables et seuils de confirmation des hypothèses**

| Hypothèse | Variable indépendante | Variable dépendante | Dynamique anticipée | Seuil de confirmation | Seuil d'infirmation |
|---|---|---|---|---|---|
| HG | Architecture ensemble learning (3 niveaux) | F1-Score, Recall, AUC-PR | XGBoost surpasse RF et IF sur les 3 métriques | XGBoost F1 ≥ 0,60 et Recall ≥ 0,60 | XGBoost F1 < 0,40 ou IF > XGBoost |
| HS1 | Modèles ML (IF, XGBoost) | Recall, correspondance SHAP/littérature | Recall ≥ 60%, top-10 SHAP aligné sur littérature | Recall ≥ 0,60 et ≥ 6/10 variables SHAP concordantes | Recall < 0,40 ou < 3/10 variables concordantes |
| HS2* | Données contextuelles locales | Pertinence perçue par répondants | ≥ 70% des répondants valident la transférabilité | ≥ 70% de validation qualitative | < 50% de validation qualitative |
| HS3 | Module SHAP (explicabilité) | Taux de FP, utilité perçue | Baisse du FP, ≥ 70% jugent SHAP utile | FP ≤ 2% et ≥ 70% satisfaction utilisateur | FP > 5% ou < 50% satisfaction |

> *HS2 est marquée comme partiellement vérifiable dans le cadre de cette étude (cf. Ch.IV). La dynamique anticipée est néanmoins précisée pour orienter les travaux futurs.

**Règles de décision pour la confirmation des hypothèses :**

- **HG confirmée** si XGBoost atteint un F1-Score ≥ 0,60 **et** un Recall ≥ 0,60 **et** surpasse significativement Random Forest et Isolation Forest
- **HS1 confirmée** si le Recall ≥ 0,60 **et** qu'au moins 6 des 10 variables les plus importantes selon SHAP correspondent aux facteurs de fraude documentés dans la littérature et les entretiens
- **HS2** : la confirmation de cette hypothèse nécessite un jeu de données local qui n'est pas disponible dans le cadre de cette étude — elle est proposée comme perspective principale
- **HS3 confirmée** si le taux de faux positifs ≤ 2 % **et** qu'au moins 70 % des répondants aux entretiens jugent les explications SHAP utiles et compréhensibles

---

## II.3. Outils de recherche

Pour la réalisation de ce mémoire, trois catégories d'outils de recherche ont été mobilisées afin de recueillir des données fiables et pertinentes : un dispositif quantitatif de modélisation, un dispositif qualitatif d'entretiens, et un environnement technique de développement et d'expérimentation.

### II.3.1. Dispositif quantitatif : datasets et modélisation

**Datasets retenus :**

Aucune donnée bancaire togolaise réelle n'étant accessible pour des raisons de confidentialité, l'étude s'appuie sur deux datasets publics de référence internationale :

- **Dataset principal** : **IEEE-CIS Fraud Detection** (Kaggle, 2020) — Environ 590 000 transactions, dont 3,5 % frauduleuses. Ce dataset, issu d'une compétition Kaggle organisée par IEEE Computational Intelligence Society, est largement utilisé dans la littérature récente (Dhieb et al., 2020 ; Kim et al., 2021 ; Ogunleye et al., 2022). Il présente l'avantage d'être réaliste, avec une structure proche des données bancaires réelles, et d'inclure des variables temporelles et catégorielles riches (~400 variables).

- **Dataset secondaire** : **Credit Card Fraud Dataset** (ULB Machine Learning Group, Dal Pozzolo et al., 2015) — Environ 284 807 transactions, dont 0,17 % frauduleuses. Utilisé comme référence complémentaire pour valider la robustesse des modèles sur un déséquilibre plus marqué.

**Tableau II.3 — Caractéristiques des datasets retenus**

| Caractéristique | IEEE-CIS Fraud Detection | Credit Card Fraud (ULB) |
|---|---|---|
| Nombre de transactions | ~590 000 | ~284 807 |
| Taux de fraude | 3,5 % | 0,17 % |
| Nombre de variables | ~400 (dont ~250 anonymisées) | 30 (PCA) |
| Période | 2019-2020 | 2013 |
| Origine géographique | États-Unis/Europe | Europe |
| Type de transactions | Cartes, virements | Cartes de crédit |

> **Limite assumée** : Ces datasets étant constitués de transactions européennes et nord-américaines, ils ne capturent pas nativement les spécificités du contexte togolais (mobile money, fraude par USSD, SIM swap, faible bancarisation). Cette limite est traitée par validation qualitative (entretiens) et proposée comme perspective de recherche.

**Architecture de modélisation retenue :**

L'approche combine trois niveaux algorithmiques complémentaires selon le principe de l'ensemble learning supervisé renforcé par une détection d'anomalies non supervisée.

**Tableau II.4 — Architecture des modèles**

| Niveau | Modèle | Type | Rôle | Entrée | Sortie |
|---|---|---|---|---|---|
| Niveau 1 | Isolation Forest | Non supervisé | Filtrage rapide des anomalies évidentes | Transactions brutes | Score d'anomalie |
| Niveau 2 | XGBoost | Supervisé (gradient boosting) | Classification fine fraude / non-fraude | Caractéristiques enrichies | Probabilité de fraude |
| Niveau 3 | LSTM (optionnel) | Deep Learning séquentiel | Analyse des patterns temporels | Séquences de transactions | Détection de séquences suspectes |

**Niveau 1 — Isolation Forest** (Liu et al., 2008) : algorithme non supervisé de détection d'anomalies qui isole les points anormaux par partitionnement aléatoire. Paramètres : 100 estimateurs, contamination 0,05, échantillonnage de 256 transactions par arbre.

**Niveau 2 — XGBoost** (Chen & Guestrin, 2016) : algorithme de gradient boosting considéré comme l'état de l'art pour les problèmes de classification tabulaire. Hyperparamètres optimisés par Optuna (30 essais, validation croisée 5 folds) : learning rate 0,05, max depth 6, scale pos weight adapté au ratio de classes.

**Niveau 3 — LSTM** (Hochreiter & Schmidhuber, 1997) : réseau de neurones récurrents pour l'analyse des patterns temporels complexes. Qualifié d'optionnel car son entraînement nécessite des ressources GPU non disponibles dans le cadre de cette étude.

**Stratégie de gestion du déséquilibre des classes :**

Le déséquilibre est traité par **SMOTE (Synthetic Minority Oversampling Technique)** , proposé par Chawla et al. (2002). Protocole : split Train/Test stratifié (80/20), application de SMOTE uniquement sur l'ensemble d'entraînement avec un rapport de sur-échantillonnage de 0,5 (k=5 pour les voisins synthétiques).

**Tableau II.5 — Distribution des classes avant et après SMOTE**

| Étape | Non-fraude | Fraude | Ratio |
|---|---|---|---|
| Données brutes | 96,5 % | 3,5 % | 27:1 |
| Train (80%) | 96,5 % | 3,5 % | 27:1 |
| Test (20%) | 96,5 % | 3,5 % | 27:1 |
| Après SMOTE (train) | 66,7 % | 33,3 % | 2:1 |

**Métriques d'évaluation :**

Le choix des métriques est guidé par la nature déséquilibrée des données :

**Tableau II.6 — Métriques d'évaluation retenues**

| Métrique | Formule | Justification | Cible |
|---|---|---|---|
| **F1-Score** | 2 × (P × R) / (P + R) | Équilibre précision/rappel, penalise FP et FN | ≥ 0,50 |
| **Recall** | TP / (TP + FN) | Priorité : détecter un maximum de fraudes (minimiser FN) | ≥ 0,60 |
| **AUC-PR** | Aire sous courbe PR | Pertinent pour classes déséquilibrées | ≥ 0,50 |
| **Précision** | TP / (TP + FP) | Limiter les faux positifs (économie d'effort analyste) | ≥ 0,50 |
| **Temps de latence** | — | Contrainte temps réel | < 100 ms |

> **Rappel** : L'Accuracy n'est pas retenue comme métrique principale en raison du fort déséquilibre des classes. Avec 0,5 % de transactions frauduleuses, un modèle prédisant systématiquement "non fraude" obtiendrait 99,5 % d'Accuracy sans rien détecter.

**Procédure d'entraînement et de validation :**

Pour chaque modèle : recherche d'hyperparamètres (Optuna, 30 essais, validation croisée 5 folds), entraînement sur l'ensemble rééquilibré, prédiction sur l'ensemble de test (non rééquilibré), calcul des métriques, puis interprétation par SHAP sur un sous-ensemble de 500 transactions.

### II.3.2. Dispositif qualitatif proposé : entretiens semi-directifs (perspective)

Les entretiens semi-directifs constituent le volet qualitatif proposé pour une recherche ultérieure. Ce protocole n'a pas pu être exécuté dans le cadre de ce mémoire — il est décrit ci-dessous pour servir de base à des travaux futurs.

**Population et échantillon ciblés :**

La population cible est constituée de l'ensemble des responsables d'institutions bancaires et d'opérateurs de mobile money au Togo. L'échantillon ciblé est de **5 à 8 répondants**, sélectionnés selon une technique d'échantillonnage **raisonnée** (choix délibéré en fonction du profil et de l'expertise).

| Profil | Rôle | Objectif de l'entretien |
|---|---|---|
| Responsable DSI / IT | Vision technique et infrastructure | Contraintes techniques, maturité des SI, besoins en infrastructure |
| Responsable Conformité / KYC-AML | Vision réglementaire | Exigences de conformité, processus AML/KYC, attentes régulateurs |
| Gestionnaire de risques / Analyste fraude | Vision opérationnelle | Typologies de fraude, limites des outils actuels, besoins en explicabilité |

Institutions ciblées : BTCI, Orabank Togo, UTB, Ecobank Togo, SGBT (banques) ; TogoCom Cash, Moov Money/Flooz (mobile money) ; BCEAO, CNRF (régulateur).

**Guide d'entretien (proposé) :**

| Thème | Questions clés | Durée estimée |
|---|---|---|
| Profil et contexte | Fonction, ancienneté, missions liées à la détection de fraude | 5 min |
| Typologies de fraude | Quels types de fraude observez-vous ? Quels canaux sont les plus touchés ? | 10 min |
| Systèmes actuels | Quels outils utilisez-vous ? Quelles sont leurs limites ? | 10 min |
| Attentes vis-à-vis de l'IA | Qu'attendez-vous d'un système IA ? Quels sont vos freins ? | 10 min |
| Explicabilité | Comment interprétez-vous les alertes ? L'explicabilité est-elle importante ? | 10 min |
| Conformité | Quelles sont les exigences réglementaires auxquelles vous devez répondre ? | 5 min |

**Méthode d'analyse (proposée) :** codage thématique. Les entretiens seraient retranscrits, puis analysés par identification de thèmes récurrents (typologies de fraude, limites techniques, besoins en explicabilité, contraintes réglementaires).

### II.3.3. Outil d'explicabilité : SHAP

L'outil d'explicabilité retenu est **SHAP (SHapley Additive exPlanations)** , fondé sur la théorie des jeux de Shapley (Lundberg & Lee, 2017). SHAP attribue à chaque variable une valeur d'importance (valeur Shapley) qui représente sa contribution à l'écart entre la prédiction du modèle et la prédiction moyenne.

SHAP a été préféré à LIME pour les raisons suivantes : fondement théorique solide (théorie des jeux), consistance mathématique des explications, capacité à fournir une interprétabilité globale (feature importance) en plus des explications locales, et adoption académique très élevée dans le domaine de la détection de fraude.

**Protocole d'application :**
1. Calcul des valeurs Shapley sur un échantillon de 500 transactions
2. Génération du graphique d'importance globale des variables (top 20)
3. Génération d'explications individuelles (force plot, waterfall plot) pour les transactions jugées frauduleuses
4. Intégration des explications dans l'interface du dashboard (Chapitre III)

SHAP répond directement à **HS3** : l'hypothèse selon laquelle l'interprétabilité des modèles facilite leur adoption par les analystes financiers et les gestionnaires de risques bancaires togolais.

### II.3.4. Environnement technique de développement

| Outil | Version | Utilisation |
|---|---|---|
| Python | 3.10 | Langage principal |
| Scikit-learn | 1.2 | Isolation Forest, Random Forest, métriques |
| XGBoost | 1.7 | Implémentation XGBoost |
| TensorFlow/Keras | 2.12 | LSTM (optionnel) |
| Optuna | 3.6 | Optimisation d'hyperparamètres |
| Pandas | 1.5 | Manipulation et prétraitement des données |
| NumPy | 1.23 | Calculs numériques |
| SHAP | 0.41 | Explicabilité des modèles |
| Imbalanced-learn | 0.10 | SMOTE |
| Google Colab | — | Calcul cloud (GPU disponible) |
| Jupyter Notebook | — | Développement et documentation interactive |

**Pipeline de prétraitement :** nettoyage et imputation des valeurs manquantes (médiane/mode), encodage des variables catégorielles (One-Hot/Label Encoding), normalisation (StandardScaler), feature engineering (montant moyen, fréquence, intervalle inter-transactions), split stratifié (80/20), et application de SMOTE sur l'ensemble d'entraînement.

---

**Conclusion**

La démarche méthodologique adoptée a permis de passer d'un cadre théorique à une approche empirique concrète et opérationnelle. L'articulation établie entre rigueur scientifique et outils d'investigation adaptés a posé les prérequis indispensables à une exploration méthodique et pertinente de notre problématique. La définition précise des variables et de leurs indicateurs constitue l'architecture conceptuelle permettant d'appréhender les phénomènes étudiés, tandis que les instruments de recherche sélectionnés — datasets internationaux, architecture d'ensemble learning à trois niveaux, explicabilité SHAP, entretiens qualitatifs et environnement technique — forment les supports opérationnels qui matérialisent nos questionnements en données exploitables.

Fort de ces assises méthodologiques solidement établies, nous sommes désormais en mesure d'aborder le terrain d'étude concret. Le chapitre suivant présente les résultats de l'application de cette méthodologie : état des lieux du secteur bancaire togolais, analyse exploratoire des données issues du dataset IEEE-CIS, performances comparatives des modèles, interprétation SHAP, et proposition de la plateforme logicielle FRAUDX.
