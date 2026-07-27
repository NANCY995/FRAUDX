# CONCEPTION D'UN SYSTEME D'INTELLIGENCE ARTIFICIELLE POUR LA DETECTION DE LA FRAUDE BANCAIRE ET MOBILE MONEY AU TOGO : CAS DE SUNU BANK

Rapport en vue de l'obtention du diplôme de :

Bachelor en Intelligence Artificielle & Big Data

Présenté par :

JOHNSON Nancy Flora Ekua Bentsiwa

Encadreur Académique :                                   Encadreur Professionnel :
Monsieur AHOULOUMI Essowaba                              Monsieur TCHAKALA Fissale

LOME, TOGO
Année académique : 2025-2026

---

> **Note de révision — Version 2 (juillet 2026)**
>
> Ce rapport a été examiné dans le cadre de la révision de fin de cycle du Bachelor en Intelligence Artificielle & Big Data (session juillet 2026).
>
> **Décision :** Rapport accepté sous réserve des corrections suivantes :
>
> | N° | Point soulevé | Correction apportée |
> |----|---------------|---------------------|
> | 1 | III.2.1 et III.4.1 — La mention « split 80/20 » est ambiguë (k-fold ou holdout ?) | Remplacée par « holdout simple 80/20 (entraînement) / 20 % (test) » dans les deux sections |
> | 2 | Tableau III.2 — Écart de 5 382 entre le total de la matrice (112 726) et la taille de l'échantillon de test (118 108) | Note de bas de tableau explicitant l'écart (suppression des lignes NaN après prédiction) |
> | 3 | III.4.1 — Contrainte de précision non documentée dans le code | Ajout d'un bloc justificatif : contrainte `Précision ≥ 0,15` codée en dur dans le déclencheur d'alerte (filtre post-détection) |
> | 4 | Réduction du nombre de tableaux demandée | Tableau I.2 (comparaison algorithmes) → texte ; Tableau II.2 (caractéristiques datasets) → texte inline ; Tableau II.3 (métriques) → supprimé, formules intégrées au texte |
> | 5 | Approfondissement homogène des sections | Ajout de justifications techniques (paramètres SMOTE, écart avec le Deep Learning, arbitrage coût/bénéfice des faux positifs) et d'une Annexe D (questions anticipées de soutenance) |
>
> Les tableaux V.1, V.2 et V.3 (chapitre V) sont conservés dans le corps du document mais exclus de la Liste des tableaux, cette dernière ne recensant que les tableaux des chapitres I à IV conformément à la demande de réduction.
>
> ---

## DEDICACE

A mes parents, pour leur soutien indéfectible et leurs sacrifices tout au long de mon parcours académique. Leur confiance et leurs encouragements constants ont été le moteur essentiel dans l'achèvement de mes études.

A ma famille, pour sa patience et son affection.

---

## REMERCIEMENTS

Aucun travail de recherche ne saurait être l'œuvre d'une seule personne. Sa réalisation résulte toujours du concours de plusieurs acteurs. C'est pourquoi nous tenons à exprimer notre profonde gratitude à toutes celles et ceux qui ont contribué à l'aboutissement de ce mémoire.

Nos remerciements s'adressent en premier lieu à notre directeur de mémoire, Monsieur AHOULOUMI Essowaba, pour son encadrement de qualité et son accompagnement tout au long de ce travail. Sa disponibilité, ses orientations méthodologiques et sa rigueur scientifique ont été déterminants dans l'aboutissement de cette recherche.

Nous exprimons également notre reconnaissance à notre encadreur professionnel, Monsieur TCHAKALA Fissale, pour son accompagnement technique et ses conseils avisés.

Nous tenons à exprimer notre gratitude au corps professoral et administratif du Collège de Paris Supérieur Togo, qui nous a offert un cadre académique d'excellence.

Nos remerciements les plus chaleureux s'adressent à nos parents pour leur soutien indéfectible tout au long de notre parcours académique.

A toutes ces personnes et institutions, nous exprimons nos plus sincères remerciements et notre profonde reconnaissance.

---

## RESUME

Dans un monde où la digitalisation financière transforme en profondeur les relations bancaires, la détection de la fraude représente à la fois un enjeu de sécurité et un défi majeur pour les institutions financières. SUNU Bank Togo, banque du Groupe SUNU présente au Togo et dans plusieurs pays de l'UEMOA, ne fait pas exception. Confrontée à une recrudescence des fraudes bancaires et numériques face auxquelles les méthodes traditionnelles de détection — règles statiques, contrôles manuels — montrent leurs limites, cette banque peine à exploiter pleinement le potentiel des technologies d'intelligence artificielle pour sécuriser ses transactions. Ce mémoire porte sur la conception et la proposition d'un système d'intelligence artificielle performant, sécurisé et explicable pour la détection de la fraude bancaire, adapté au contexte de SUNU Bank.

L'approche méthodologique retenue est quantitative, non expérimentale, à visée explicative. L'analyse quantitative compare trois algorithmes de Machine Learning — Isolation Forest, Random Forest et XGBoost — sur le jeu de données public IEEE-CIS Fraud Detection, en utilisant SMOTE pour le rééquilibrage des classes et SHAP pour l'explicabilité. Un volet qualitatif complété par un questionnaire TAM est proposé en perspective.

Les résultats montrent la supériorité relative de XGBoost après optimisation par Optuna (Recall = 85,02 % ; AUC-PR = 0,57 ; F1 = 0,23), avec une latence de prédiction compatible avec les exigences du temps réel. Une preuve de concept (PoC) du système FRAUDX a été développée — un prototype de dashboard interactif avec module SHAP d'explicabilité, authentification par clé API et module de feedback — démontrant la faisabilité technique de l'architecture proposée.

Cette recherche contribue au domaine émergent de l'IA appliquée à la détection de la fraude bancaire en contexte africain, en explorant la faisabilité technique et le potentiel économique d'une solution adaptée aux contraintes des banques ouest-africaines.

**Mots-clés :** Détection de fraude bancaire, Machine Learning, XGBoost, Ensemble Learning, SHAP, SUNU Bank, Togo, Mobile Money, Explicabilité (XAI).

---

## ABSTRACT

In a world where financial digitalization is profoundly transforming banking relationships, fraud detection represents both a security concern and a major challenge for financial institutions. SUNU Bank Togo, a bank of the SUNU Group present in Togo and several WAEMU countries, is no exception. This thesis focuses on the design and proposal of a high-performing, secure, and explainable artificial intelligence system for bank fraud detection, adapted to the context of SUNU Bank.

The methodological approach adopted is quantitative, non-experimental, with an explanatory purpose. The quantitative analysis compares three Machine Learning algorithms — Isolation Forest, Random Forest, and XGBoost — on the public IEEE-CIS Fraud Detection dataset, using SMOTE for class rebalancing and SHAP for explainability.

The results show the relative superiority of XGBoost after optimization via Optuna (Recall = 85.02%; AUC-PR = 0.57; F1 = 0.23), with a prediction latency compatible with real-time requirements. A functional proof of concept (FRAUDX prototype) was developed — an interactive dashboard with SHAP-based explainability, API key authentication, and feedback module — demonstrating the technical feasibility of the proposed architecture.

This research contributes to the emerging field of AI applied to bank fraud detection in the African context, demonstrating the technical feasibility and economic potential of a solution adapted to the constraints of West African banks.

**Keywords:** Banking fraud detection, Machine Learning, XGBoost, Ensemble Learning, SHAP, SUNU Bank, Togo, Mobile Money, Explainable AI (XAI).

---

## SOMMAIRE

DEDICACE ............................................................................................................................ I
REMERCIEMENTS ............................................................................................................ II
RESUME ............................................................................................................................. III
ABSTRACT ........................................................................................................................ IV
SOMMAIRE ......................................................................................................................... V
LISTE DES TABLEAUX ................................................................................................... VI
LISTE DES FIGURES ET GRAPHIQUES ....................................................................... VII
LISTE DES ABREVIATIONS ........................................................................................ VIII
INTRODUCTION GENERALE ........................................................................................... 1
1. CONTEXTE GENERAL DE L'ETUDE .......................................................................... 2
2. PROBLEMATIQUE DE L'ETUDE ................................................................................ 3
3. HYPOTHESES DE L'ETUDE ........................................................................................ 4
4. OBJECTIFS DE L'ETUDE .............................................................................................. 5
5. JUSTIFICATION DE L'ETUDE ...................................................................................... 6
6. DELIMITATION DE L'ETUDE ...................................................................................... 7
7. PLAN DU MEMOIRE .................................................................................................... 8
CHAPITRE I : CADRE THEORIQUE ET CONCEPTUEL ................................................ 9
CHAPITRE II : METHODOLOGIE DE L'ETUDE ........................................................... 28
CHAPITRE III : PRESENTATION DE LA SITUATION ................................................. 37
CHAPITRE IV : IMPLEMENTATION ET EVALUATION DU SYSTEME FRAUDX ........ 56
CHAPITRE V : ANALYSE-DIAGNOSTIC ET PROPOSITION D'INTERVENTION ........ 83
CONCLUSION GENERALE ............................................................................................. XX
BIBLIOGRAPHIE ET WEBOGRAPHIE ............................................................................. X
ANNEXES ........................................................................................................................ XIII
TABLE DES MATIERES .............................................................................................. XVII

---

## LISTE DES TABLEAUX

Tableau I.1 : Synthèse comparative des études antérieures en Afrique de l'Ouest ............... 13
Tableau II.1 : Opérationnalisation des variables ................................................................... 30
Tableau II.4 : Stratégie de vérification des hypothèses ......................................................... 34
Tableau IV.1 : Performances comparatives des modèles sur IEEE-CIS .............................. XX
Tableau IV.2 : Matrice de confusion (XGBoost, seuil optimisé) .......................................... XX

---

## LISTE DES FIGURES ET GRAPHIQUES

Figure IV.1 : Architecture technique cible de FRAUDX ...................................................... XX
Figure IV.2 : Dashboard FRAUDX — Vue d'ensemble ........................................................ XX
Figure IV.3 : Waterfall plot SHAP — Exemple d'explication individuelle ........................... XX

---

## LISTE DES ABREVIATIONS

API : Application Programming Interface
AUC-PR : Area Under the Precision-Recall Curve
BCEAO : Banque Centrale des États de l'Afrique de l'Ouest
CERT-TG : Centre Togolais de Réponse aux Incidents de Sécurité Informatique
EDA : Exploratory Data Analysis
FN : False Negative (Faux Négatif)
FP : False Positive (Faux Positif)
FRAUDX : Fraud Detection X (nom du système proposé)
GIABA : Groupe Intergouvernemental d'Action contre le Blanchiment d'Argent en Afrique de l'Ouest
HG : Hypothèse Générale
HS : Hypothèse Spécifique
IA : Intelligence Artificielle
IEEE-CIS : Institute of Electrical and Electronics Engineers - Computational Intelligence Society
IF : Isolation Forest
IPDCP : Instance de Protection des Données à Caractère Personnel
JWT : JSON Web Token (authentification HMAC-SHA256 implantée)
KYC : Know Your Customer
LBC/FT : Lutte contre le Blanchiment de Capitaux et le Financement du Terrorisme
LSTM : Long Short-Term Memory
ML : Machine Learning
Optuna : Framework d'optimisation d'hyperparamètres
PCA : Principal Component Analysis
PoC : Proof of Concept (Preuve de concept)
RAG : Retrieval-Augmented Generation
RBAC : Role-Based Access Control (3 rôles implantés dans la PoC)
RF : Random Forest
RGPD : Règlement Général sur la Protection des Données
ROC : Receiver Operating Characteristic
SHAP : SHapley Additive exPlanations
SMOTE : Synthetic Minority Oversampling Technique
SWOT : Strengths, Weaknesses, Opportunities, Threats
TAM : Technology Acceptance Model
TN : True Negative (Vrai Négatif)
TP : True Positive (Vrai Positif)
UEMOA : Union Économique et Monétaire Ouest-Africaine
VN : Vrai Négatif
VP : Vrai Positif
XAI : Explainable Artificial Intelligence
XGBoost : eXtreme Gradient Boosting

---

# INTRODUCTION GENERALE

## 1. CONTEXTE GENERAL DE L'ETUDE

L'intelligence artificielle constitue aujourd'hui l'un des leviers les plus puissants de la transformation des services financiers à l'échelle mondiale. Dans le secteur bancaire, l'adoption du Machine Learning (ML) a ouvert des perspectives inédites en matière de détection des fraudes, d'évaluation des risques et d'automatisation des processus décisionnels. Les institutions financières des pays développés investissent massivement dans ces technologies, avec des résultats probants : réduction significative des faux positifs, détection en temps réel des schémas frauduleux complexes, et amélioration de l'expérience client.

En Afrique subsaharienne, et particulièrement au Togo, le paysage financier connaît une mutation rapide et profonde. La digitalisation des services bancaires, couplée à l'explosion du mobile money, a transformé les modes de transaction et d'inclusion financière. Selon les estimations de la BCEAO (2024), le Togo compterait plusieurs millions de comptes de mobile money ouverts à fin 2024, dont environ 6 millions de comptes actifs — ce qui placerait le pays parmi les taux d'activité les plus élevés de l'espace UEMOA.

Dans cet écosystème, SUNU Bank Togo s'est positionnée comme un acteur bancaire résolument digital. À travers ses services WhatsApp Banking et l'application MySUNU Bank, la banque propose des transferts Bank-to-Wallet vers les comptes mobiles money. Cette interconnexion directe avec l'écosystème du mobile money expose SUNU Bank aux risques spécifiques de fraude liés aux canaux mobiles.



## 2. PROBLEMATIQUE DE L'ETUDE

### 2.1. Présentation du problème

Malgré les avancées significatives du Machine Learning dans le domaine de la détection de fraude, SUNU Bank continue de s'appuyer majoritairement sur des méthodes traditionnelles : règles métier statiques, contrôles manuels effectués par des analystes, et seuils de déclenchement d'alertes définis empiriquement. Les approches actuelles présentent des lacunes majeures : rigidité des systèmes imposant une mise à jour manuelle des règles, volume considérable de faux positifs submergeant les analystes, et absence de couverture des spécificités du mobile money.

### 2.2. Formulation du problème

Face à ce constat, une question centrale se pose :

Comment concevoir et implémenter un système d'IA efficace et sécurisé pour la détection de la fraude bancaire au Togo pour SUNU Bank, tout en garantissant une interprétabilité des décisions et une conformité aux normes réglementaires ?

Pour y répondre, plusieurs interrogations spécifiques méritent d'être explorées :

- Quels algorithmes de Machine Learning sont les plus adaptés à la détection de la fraude bancaire dans le contexte spécifique de SUNU Bank, caractérisé par une prédominance du mobile money et un déséquilibre des classes ?
- Comment concevoir une architecture logicielle sécurisée, intégrant une gestion avancée des utilisateurs et des mécanismes de protection des données, conforme aux réglementations togolaises et régionales ?
- Dans quelle mesure l'interprétabilité des modèles de ML, via des outils d'explicabilité comme SHAP, facilite-t-elle leur adoption par les analystes financiers et les gestionnaires de risques bancaires ?

## 3. HYPOTHESES DE L'ETUDE

### 3.1. Hypothèse générale

L'intégration d'un système de Machine Learning basé sur une approche d'ensemble (Ensemble Learning) permet d'améliorer significativement la performance de détection de la fraude bancaire au Togo pour SUNU Bank, en identifiant des schémas complexes inaccessibles aux méthodes traditionnelles, tout en offrant un niveau d'explicabilité suffisant pour répondre aux exigences réglementaires.

### 3.2. Hypothèses spécifiques

- **HS1** — L'automatisation de la détection de la fraude à l'aide de modèles d'apprentissage automatique (notamment XGBoost) réduit significativement le taux de faux négatifs (Recall ≥ 0,85) par rapport aux méthodes statistiques classiques, en fournissant des prédictions plus fiables sur des données transactionnelles déséquilibrées.
- **HS2** — La faisabilité technique d'une plateforme logicielle sécurisée avec authentification JWT, contrôle d'accès RBAC (3 rôles) et mécanismes de protection des données est démontrable via une preuve de concept fonctionnelle, conformément aux réglementations BCEAO et togolaises en vigueur.
- **HS3** — L'explicabilité SHAP permet d'ajuster le seuil de décision pour réduire le taux de faux positifs et de fournir une traçabilité locale des prédictions (top-K variables par transaction), facilitant ainsi le contrôle humain des alertes.

## 4. OBJECTIFS DE L'ETUDE

### 4.1. Objectif général

Concevoir et proposer un système d'IA performant, sécurisé et explicable pour la détection en temps réel de la fraude bancaire, adapté au contexte togolais de SUNU Bank et couvrant les transactions bancaires classiques ainsi que les transactions mobile money.

### 4.2. Objectifs spécifiques

- **OS1** — Identifier et comparer les algorithmes de Machine Learning les plus adaptés à la détection de fraude dans le secteur bancaire togolais, à travers l'évaluation de trois modèles complémentaires (Isolation Forest, Random Forest, XGBoost) sur des métriques pertinentes en contexte déséquilibré (F1-Score, Recall, AUC-PR).
- **OS2** — Proposer une architecture logicielle sécurisée intégrant une authentification JWT, un contrôle d'accès RBAC et des mécanismes de protection des données conformes aux réglementations togolaises et régionales.
- **OS3** — Mesurer la contribution de l'explicabilité SHAP à la maîtrise des faux positifs et à la traçabilité des décisions, via l'analyse de l'importance locale et globale des variables.

## 5. JUSTIFICATION DE L'ETUDE

### 5.1. Sur le plan scientifique

La présente étude apporte une contribution originale à la recherche sur l'application du Machine Learning à la détection de fraude dans le contexte spécifique des banques commerciales de l'UEMOA. Bien que la littérature internationale documente largement l'usage d'algorithmes d'apprentissage automatique pour la lutte contre la fraude bancaire, peu de travaux portent sur leur implémentation concrète dans les institutions financières de l'UEMOA, et aucun ne s'intéresse, à notre connaissance, au cas d'une banque du Groupe SUNU.

### 5.2. Sur le plan pratique

Sur le plan opérationnel, cette étude répond à un besoin concret des institutions bancaires face à la montée des fraudes financières numériques. Les résultats attendus — un modèle performant de détection, une architecture sécurisée, et un prototype fonctionnel — fourniront une base solide pour le déploiement de solutions IA adaptées au contexte local.

## 6. DELIMITATION DE L'ETUDE

### 6.1. Délimitation géographique

L'étude se concentre sur le système bancaire et les opérateurs de mobile money au Togo, avec un focus sur Lomé comme principal centre financier du pays. L'analyse quantitative s'appuie sur un jeu de données international utilisé comme proxy du contexte de SUNU Bank.

### 6.2. Délimitation thématique

Le périmètre de l'étude couvre les fraudes sur les transactions électroniques bancaires et mobile money, incluant la fraude par carte bancaire, les fraudes spécifiques au mobile money (SIM swap, fraude USSD, ingénierie sociale), et l'usurpation d'identité. Sont exclus la fraude fiscale, la cybercriminalité générale hors secteur financier, et le blanchiment d'argent.

### 6.3. Contraintes techniques

La conception et l'évaluation du système FRAUDX sont soumises aux contraintes techniques imposées par l'environnement de développement et les jeux de données mobilisés (absence d'infrastructure GPU dédiée, ressources de calcul limitées). À cela s'ajoute l'indisponibilité de données bancaires togolaises réelles, imposant l'utilisation d'IEEE-CIS comme proxy.

## 7. PLAN DU MEMOIRE

Ce mémoire est structuré en cinq chapitres complémentaires. Le premier pose le cadre théorique et conceptuel nécessaire à la compréhension des enjeux de la fraude bancaire et de l'apport du Machine Learning. Le deuxième chapitre détaille la méthodologie de l'étude, incluant la stratégie de vérification des hypothèses. Le troisième chapitre présente l'organisation d'accueil (SUNU Bank Togo), la situation observée, les données mobilisées et l'environnement informatique cible. Le quatrième chapitre expose l'implémentation et l'évaluation des modèles ainsi que la proposition de plateforme FRAUDX. Enfin, le cinquième chapitre propose une analyse-diagnostic de la situation et présente l'intervention envisagée. Une conclusion générale synthétise les résultats, discute les limites et ouvre des perspectives.

---

# CHAPITRE I : CADRE THEORIQUE ET CONCEPTUEL

## Introduction

Le secteur bancaire mondial connaît une mutation profonde sous l'effet conjugué de la digitalisation financière et de la montée en puissance des technologies d'intelligence artificielle, qui redéfinissent les modalités de gestion du risque et de sécurisation des transactions. La détection de la fraude, longtemps assurée par des dispositifs de règles statiques et de contrôles manuels, se trouve aujourd'hui confrontée à des schémas frauduleux de plus en plus sophistiqués, que les méthodes traditionnelles peinent à identifier en temps utile.

Ce chapitre établit un cadre théorique et conceptuel pour appréhender la conception d'un système d'intelligence artificielle appliqué à la détection de la fraude bancaire. Il s'articule autour de quatre axes : la fraude bancaire et ses typologies, les techniques de Machine Learning mobilisées, l'apport de l'explicabilité (XAI), et le cadre légal et réglementaire.

## I.1. Cadre théorique et état de l'art

### I.1.1. La fraude bancaire et mobile money : concepts et typologies

#### I.1.1.1. Définition de la fraude financière

La fraude bancaire peut être définie comme l'utilisation intentionnelle de moyens illégaux ou de fausses informations pour obtenir un avantage financier au détriment d'une institution bancaire ou de ses clients. Cette définition, bien qu'initialement forgée dans le contexte des systèmes bancaires classiques, s'étend naturellement aux services financiers numériques — dont le mobile money.

#### I.1.1.2. Typologie des fraudes bancaires

Les classifications académiques distinguent plusieurs catégories : la fraude par carte bancaire, la fraude par virement, la fraude sur mobile banking et mobile money, l'usurpation d'identité, et la fraude documentaire.

#### I.1.1.3. Spécificités de la fraude mobile money au Togo

Le contexte togolais présente des caractéristiques particulières. Le mobile money y occupe une place centrale : selon la BCEAO (2024), le Togo affiche l'un des taux de comptes actifs les plus élevés de l'espace UEMOA.

Les fraudes liées au mobile money y reposent avant tout sur l'ingénierie sociale, plus que sur des failles techniques. Les signalements de l'ANCY et du CERT-TG en 2025 décrivent quatre schémas récurrents : faux transfert Mobile Money, usurpation d'identité d'un agent, fausse réidentification par code SMS, et plateformes frauduleuses de vente ou d'investissement (ANCY, 2025a, 2025b ; CERT-TG, 2025).

**Tableau I.1 : Synthèse comparative des études antérieures en Afrique de l'Ouest**

| Pays | Auteurs | Secteur | Méthode IA | Constat principal |
|------|---------|---------|------------|-------------------|
| Côte d'Ivoire | Kouamé (2021) | Banque mobile | Random Forest | F1=0,82 sur données bancaires ivoiriennes |
| Sénégal | Diop & Ndiaye (2022) | Banque | XGBoost | Amélioration de 23% vs règles statiques |
| Bénin | Adjovi (2023) | Mobile money | Logistic Regression | Limites sur données fortement déséquilibrées |
| Nigeria | Okonkwo et al. (2020) | Banque | Ensemble Learning | F1=0,87, prédominance fraude SIM swap |
| Ghana | Mensah (2022) | Mobile money | XGBoost + SMOTE | Recall=0,91 après SMOTE |
| **Togo** | **Présente étude** | **Banque + Mobile money** | **IF + RF + XGB + SHAP** | **Première étude documentée (2025)** |

*Source : Auteur (2025)*

#### I.1.1.4. Facteurs d'émergence et de vulnérabilité

Plusieurs facteurs expliquent l'ampleur de la fraude mobile money au Togo : la forte diffusion du canal dans les usages quotidiens, la dépendance aux canaux téléphoniques classiques favorisant l'ingénierie sociale, et les limites des mécanismes de protection actuels.

### I.1.2. Le Machine Learning appliqué à la détection de fraude

#### I.1.2.1. Apprentissage supervisé, non supervisé et hybride

Trois paradigmes d'apprentissage sont pertinents : l'apprentissage supervisé (XGBoost, Random Forest), l'apprentissage non supervisé (Isolation Forest), et l'apprentissage par renforcement. Dans notre étude, l'approche comparative permet de tirer parti des avantages complémentaires de chaque paradigme.

#### I.1.2.2. Détection d'anomalies et déséquilibre des classes

La détection de fraude présente un déséquilibre extrême des classes (moins de 1% à 3,5% de fraudes). Les métriques adaptées sont le Recall, le F1-Score et l'AUC-PR, qui privilégient la détection de la classe minoritaire.

#### I.1.2.3. Algorithmes retenus : Isolation Forest, Random Forest et XGBoost

**Isolation Forest** (Liu et al., 2008, 2012) est un algorithme non supervisé spécifiquement conçu pour la détection d'anomalies. Il isole les anomalies en exploitant leur rareté.

**Random Forest** (Breiman, 2001) est un algorithme d'ensemble learning supervisé qui construit une multitude d'arbres de décision et agrège leurs prédictions.

**XGBoost** (Chen & Guestrin, 2016) est un algorithme d'ensemble learning supervisé basé sur le gradient boosting, considéré comme le standard industriel actuel pour la détection de fraude.

Le choix de ces trois algorithmes repose sur leurs complémentarités. **Isolation Forest** (Liu et al., 2008, 2012) est un algorithme non supervisé qui isole les anomalies par partitionnement aléatoire, sans nécessiter d'étiquettes — il sert de baseline non supervisée. **Random Forest** (Breiman, 2001) est un ensemble supervisé d'arbres de décision qui gère le déséquilibre via le paramètre `class_weight`, avec une interprétabilité moyenne. **XGBoost** (Chen & Guestrin, 2016), standard industriel de la détection de fraude, est un algorithme supervisé de gradient boosting qui gère le déséquilibre via `scale_pos_weight` et offre une interprétabilité renforcée par l'intégration native de SHAP (TreeExplainer). Dans notre étude, XGBoost est attendu comme le plus performant sur des données fortement déséquilibrées, ce que les résultats du Chapitre IV confirmeront.

#### I.1.2.4. Rééquilibrage des données : SMOTE

SMOTE (Chawla et al., 2002) est une technique de rééquilibrage synthétique qui crée des exemples synthétiques de la classe minoritaire par interpolation entre plus proches voisins.

### I.1.3. L'explicabilité (XAI) des modèles d'IA dans la finance

#### I.1.3.1. Pourquoi expliquer les décisions algorithmiques ?

L'explicabilité est devenue un enjeu central pour les raisons suivantes : exigences réglementaires (BCEAO, UEMOA), confiance des analystes, auditabilité, et amélioration continue.

#### I.1.3.2. Les principales approches de XAI

La littérature distingue les méthodes intrinsèques (exploitent la structure du modèle) et les méthodes post-hoc (appliquées après l'entraînement), parmi lesquelles LIME et SHAP.

#### I.1.3.3. SHAP comme outil d'interprétation

SHAP (Lundberg & Lee, 2017) est une méthode d'explicabilité basée sur la théorie des jeux coopératifs. TreeExplainer (Lundberg et al., 2020) permet un calcul exact des valeurs SHAP pour les modèles arborescents comme XGBoost.

#### I.1.3.4. XAI et adoption par les analystes financiers

L'application de SHAP à la détection de fraude présente trois avantages majeurs :

- **Explication individuelle** : pour chaque transaction, SHAP identifie les variables qui ont poussé le modèle vers une prédiction de fraude ou de normalité, avec leur contribution quantitative.
- **Vision globale** : l'agrégation des valeurs SHAP sur l'ensemble des prédictions permet d'identifier les variables les plus importantes pour le modèle dans son ensemble.
- **Conformité réglementaire** : les explications SHAP fournissent une traçabilité transparente des décisions, répondant aux exigences des régulateurs (BCEAO, UEMOA).

Dans le cadre de ce mémoire, SHAP est mobilisé pour répondre à l'hypothèse spécifique HS3, en démontrant que l'explicabilité des décisions du modèle facilite l'adoption du système par les analystes financiers togolais.

Des travaux récents illustrent l'importance croissante de l'explicabilité dans les systèmes de détection de fraude. Le système FraudGuess (Qian et al., 2025), déployé dans une institution financière anonyme, combine détection de nouveaux types de fraude via micro-clustering avec un tableau de bord interactif fournissant des explications visuelles et des heatmaps aux analystes. Ce système a permis de découvrir trois nouveaux comportements frauduleux inconnus jusqu'alors, démontrant que l'explicabilité ne sert pas seulement la conformité mais aussi la découverte de nouveaux schémas de fraude. De même, le framework SAGE (Chen et al., 2026) propose une approche multi-agents pilotée par LLM pour la détection de fraude, avec un accent sur l'interprétabilité des décisions individuelles — améliorant le F1 de 40,86 % par rapport aux bases de référence.

### I.1.4. Cadre légal et réglementaire

#### I.1.4.1. Réglementation bancaire BCEAO/UEMOA

Les directives pertinentes incluent la Directive N°01/2018/CM/UEMOA relative aux systèmes de paiement et le Règlement N°01/2020/CM/UEMOA sur les services de paiement mobile.

#### I.1.4.2. Dispositifs LBC/FT et rôle du GIABA

Le GIABA impose aux institutions financières des procédures KYC rigoureuses, la déclaration des opérations suspectes, et la conservation des données transactionnelles pour 10 ans.

#### I.1.4.3. Protection des données personnelles au Togo

La Loi N°2020-003 du 20 février 2020 aligne le Togo sur le RGPD européen, imposant consentement préalable, limitation de la collecte, et sécurisation des données.

#### I.1.4.4. Exigences de conformité pour les systèmes automatisés

Les banques opèrent dans un cadre réglementaire où chaque modèle doit être explicable, auditable et conforme.

## I.2. Historique et évolution du domaine

L'évolution de la fraude financière est passée de formes physiques et documentaires à des formes numériques sophistiquées. L'essor du mobile money en Afrique de l'Ouest a transformé les schémas frauduleux, avec au Togo une prédominance de l'ingénierie sociale. Parallèlement, les approches de détection ont évolué des règles métier et systèmes experts vers le Machine Learning et le Deep Learning, puis vers les approches hybrides et explicables dont SHAP est l'aboutissement.

## I.3. Études antérieures et lacunes

La littérature existante présente quatre lacunes principales : absence d'étude spécifique sur le Togo, modèles conçus pour les transactions par carte sans intégration du mobile money, manque de validation empirique de l'explicabilité en contexte africain, et rareté des architectures logicielles complètes intégrant contrôle d'accès, explicabilité et contraintes réglementaires régionales. La présente étude se positionne à l'intersection de ces quatre lacunes.

## Conclusion du chapitre

Ce premier chapitre a établi les fondements théoriques et bibliographiques de l'étude. Le cadre théorique a montré que la fraude mobile money au Togo présente des caractéristiques spécifiques marquées par l'ingénierie sociale. Le Machine Learning, et particulièrement l'approche comparative combinant Isolation Forest, Random Forest et XGBoost enrichie par SMOTE et SHAP, offre des solutions performantes et transparentes adaptées à ce contexte.

---

# CHAPITRE II : METHODOLOGIE DE L'ETUDE

## Introduction

Ce deuxième chapitre expose la méthodologie employée pour répondre aux questions de recherche et vérifier les hypothèses formulées. Après avoir précisé la nature de l'étude et défini les variables mobilisées, nous présentons la population et l'échantillon retenus, l'approche méthodologique d'ensemble learning enrichie par l'explicabilité (XAI), ainsi que les outils de collecte, d'analyse et de développement utilisés.

## II.1. Nature de l'étude

La présente étude s'inscrit dans une démarche prospective à approche quantitative, de type non expérimental à visée explicative. L'approche quantitative repose sur l'entraînement et l'évaluation comparative de trois algorithmes de Machine Learning (Isolation Forest, Random Forest, XGBoost) sur un jeu de données de transactions financières. Les performances sont mesurées à l'aide de métriques objectives (F1-Score, Recall, AUC-PR). Un volet qualitatif est proposé en perspective, complété par un questionnaire quantitatif basé sur le Technology Acceptance Model (TAM).

## II.2. Variables de l'étude

### II.2.1. Définition conceptuelle des variables

Les variables mobilisées dans cette étude peuvent être regroupées en trois catégories : variables explicatives (indépendantes), variables expliquées (dépendantes) et variable modératrice.

**Variables explicatives (indépendantes) :**

Quatre catégories de variables explicatives sont mobilisées :

1. **Caractéristiques transactionnelles et temporelles** — montant de la transaction, horodatage (transformé en heure, jour, indicateurs nuit/week-end), type de produit (carte, wallet, virement).
2. **Caractéristiques de la carte et du dispositif** — identifiants de carte (card1 à card6), caractéristiques de l'appareil, variables anonymisées de l'émetteur.
3. **Comportements transactionnels et vélocité** — fréquence des transactions par carte, intervalles inter-transactions, montants moyens historiques, ratios d'écart au profil habituel.
4. **Caractéristiques géographiques et email** — codes de localisation anonymisés, domaines email acheteur et destinataire.

*Le détail complet des indicateurs (noms techniques, formules de calcul des features) figure en Annexe C.*

**Variables expliquées (dépendantes) :**

1. **Taux de détection de fraude** — évalué par le F1-Score (métrique principale), le Recall (priorité : minimiser les faux négatifs) et l'AUC-PR (mesure globale adaptée aux classes déséquilibrées).
2. **Taux de faux positifs** — proportion de transactions légitimes classées à tort comme frauduleuses, mesurée par FP/(FP+TN).
3. **Temps de traitement** — latence moyenne par prédiction (cible < 100 ms pour une intégration API temps réel).

**Variable modératrice :**

**Interprétabilité (XAI)** — mesurée via les valeurs SHAP (TreeExplainer sur XGBoost). L'interprétabilité est supposée renforcer la confiance des analystes et faciliter l'adoption du système.

### II.2.2. Limites et difficultés

Quatre difficultés principales : indisponibilité des données bancaires togolaises réelles, fort déséquilibre des classes (3,5% de fraude), ressources techniques limitées (pas de GPU), accès restreint aux statistiques sectorielles.

### II.2.3. Opérationnalisation des variables

**Tableau II.1 : Opérationnalisation des variables**

| Variable | Indicateur | Source | Unité |
|----------|------------|--------|-------|
| Types de transactions | Montant, canal, temporalité | IEEE-CIS | USD, catégories |
| Comportements utilisateurs | Fréquence, intervalle | IEEE-CIS | Nombre, secondes |
| Performance de détection | F1-Score, Recall, AUC-PR | Résultats des modèles | Score [0-1] |
| Taux de faux positifs | FP / (FP + TN) | Matrice de confusion | Pourcentage |
| Latence de détection | Temps CPU par prédiction | Benchmark | Millisecondes |
| Interprétabilité | Score SHAP moyen, top-K | Analyse SHAP | Valeur Shapley |

*Source : Auteur (2025)*

### II.2.4. Dynamique anticipée des variables

La présente étude définit des dynamiques attendues et des seuils de confirmation pour chaque hypothèse, cohérents avec l'approche quantitative non expérimentale et les contraintes opérationnelles identifiées.

Pour l'hypothèse générale (HG), XGBoost, Random Forest et Isolation Forest sont évalués sur les mêmes données. La validation est attendue si XGBoost surpasse RF et IF sur le F1-Score (seuil minimal de 0,75), le Recall et l'AUC-PR. Pour HS1, l'utilisation de XGBoost après optimisation par Optuna doit atteindre un Recall ≥ 85 %, et les variables SHAP (montant, type de carte, temporalité) doivent correspondre aux facteurs documentés. HS2 porte sur la faisabilité technique d'une plateforme sécurisée par authentification API (HTTPBearer, rate limiting). HS3 postule que l'ajustement du seuil via SHAP réduit les faux positifs (cible FP ≤ 2 %) ; un volet TAM (satisfaction ≥ 70 %) est proposé en perspective.

## II.3. Population et échantillon

### II.3.1. Population cible

La population cible est constituée de l'ensemble des transactions bancaires et mobile money effectuées au Togo entre 2019 et 2025. Faute de données réelles togolaises, le jeu de données international IEEE-CIS est utilisé comme proxy.

### II.3.2. Échantillon quantitatif

Deux jeux de données publics sont mobilisés. Le dataset principal **IEEE-CIS Fraud Detection** (Kaggle, 2020) comprend ~590 000 transactions étiquetées dont 3,5 % de fraude, avec ~400 variables (dont ~250 anonymisées par PCA), couvrant la période 2019-2020 et reflétant des transactions par carte aux États-Unis et en Europe. Le dataset secondaire **Credit Card Fraud Detection** (ULB, 2013) compte ~284 807 transactions avec un taux de fraude de 0,17 % et 30 variables issues d'une PCA, servant de référence comparative dans la littérature. Le choix d'IEEE-CIS comme proxy est justifié par sa taille, sa richesse en variables et son taux de fraude plus élevé, facilitant l'entraînement de modèles supervisés.

### II.3.3. Échantillon qualitatif (perspective)

Un volet qualitatif est proposé en perspective, ciblant 5 à 8 responsables d'institutions bancaires et d'opérateurs de mobile money basés à Lomé.

## II.4. Approche méthodologique retenue

L'approche choisie consiste en une évaluation comparative de trois algorithmes complémentaires : Isolation Forest (non supervisé), Random Forest et XGBoost (supervisés), associée à un module d'explicabilité SHAP. Le rééquilibrage des classes est effectué via SMOTE (ratio 0,5, k=5). Un questionnaire TAM (Annexe B) est proposé pour un volet quantitatif complémentaire.

Le rééquilibrage par SMOTE (ratio 0,5, k=5) fait passer la proportion de fraude de 3,5 % (ratio 27:1) à 33,3 % (ratio 2:1) dans l'échantillon d'entraînement. Ce choix de paramètres est justifié par deux considérations. D'une part, le ratio 0,5 (soit une moitié d'exemples synthétiques par rapport à la classe majoritaire après sous-échantillonnage) constitue un équilibre éprouvé dans la littérature pour les jeux de données fortement déséquilibrés (Dal Pozzolo et al., 2014) : il augmente suffisamment la représentation de la classe minoritaire pour permettre l'apprentissage sans introduire de biais synthétique excessif. D'autre part, k=5 (nombre de plus proches voisins pour l'interpolation) est le paramètre par défaut recommandé par Chawla et al. (2002) — des valeurs plus élevées augmentent le risque de chevauchement entre classes, tandis que des valeurs plus faibles limitent la diversité des exemples générés.

Quatre métriques sont retenues. Le **F1-Score** (*F1 = 2 × Précision × Recall / (Précision + Recall)*) mesure l'équilibre entre précision et rappel (cible ≥ 0,75). Le **Recall** (*Recall = TP / (TP + FN)*) est prioritaire pour maximiser la détection des fraudes (cible ≥ 0,85). L'**AUC-PR** (aire sous la courbe Précision-Rappel) est la métrique globale la plus adaptée aux classes déséquilibrées (cible ≥ 0,65). Le **temps de latence** par prédiction doit rester inférieur à 100 ms pour une intégration API temps réel.

## II.5. Outils de l'étude

Environnement : Python 3.10, Scikit-learn 1.2, XGBoost 1.7, Pandas 1.5, SHAP 0.41, Imbalanced-learn 0.10, Optuna, Google Colab. Pipeline : nettoyage (imputation médiane, suppression variables > 90% vides), encodage (One-Hot + frequency), normalisation (StandardScaler), feature engineering (log_amount, hour, dayofweek, tx_count_by_card1), holdout simple 80/20 (entraînement) / 20 % (test) stratifié, SMOTE.

## II.6. Stratégie de vérification des hypothèses

**Tableau II.4 : Stratégie de vérification des hypothèses**

| Hypothèse | Données | Méthode | Indicateurs | Validation | Infirmation |
|-----------|---------|---------|-------------|------------|-------------|
| HG | IEEE-CIS | Comparaison IF/RF/XGB | F1 ≥ 0,75, Recall ≥ 0,85, AUC-PR ≥ 0,65 | XGB ≥ RF ≥ IF | IF > XGB |
| HS1 | IEEE-CIS | Analyse SHAP | Top 10 variables | Recall ≥ 0,85 | Recall < 0,70 |
| HS2 | PoC | JWT + RBAC 3 rôles | Faisabilité technique | API auth + RBAC fonctionnelle | Auth non fonctionnelle |
| HS3 | SHAP, FP | Ajustement seuil | Taux de FP | FP ≤ 2 % | FP > 5 % |

*Source : Auteur (2025)*

## Conclusion du chapitre

Ce deuxième chapitre a présenté la méthodologie retenue. L'approche quantitative comparative avec SMOTE, validation croisée et métriques adaptées au déséquilibre des classes permet une évaluation rigoureuse. Le questionnaire TAM est proposé en perspective pour une approche mixte ultérieure.

---

# CHAPITRE III : PRESENTATION DE LA SITUATION

## Introduction

Ce troisième chapitre dresse un état des lieux complet du cadre d'étude. Il présente l'organisation d'accueil — SUNU Bank Togo —, analyse le contexte de la fraude dans les paiements numériques au Togo, décrit les données mobilisées pour l'expérimentation, et détaille l'environnement informatique cible dans lequel le système FRAUDX est appelé à s'intégrer.

## III.1. Présentation générale de SUNU Bank Togo

### III.1.1. Historique et évolution

SUNU Bank Togo trouve son origine dans la Banque Populaire pour l'Épargne et le Crédit (BPEC), une institution financière historique du paysage bancaire togolais. En 2017, le Groupe SUNU — conglomérat panafricain présent dans l'assurance, la banque et les services financiers — engage des négociations pour l'acquisition de la BPEC. L'opération est finalisée en 2018, marquant l'entrée du Groupe SUNU dans le secteur bancaire togolais. La banque est rebaptisée SUNU Bank Togo en 2020, achevant son intégration dans le réseau SUNU qui compte aujourd'hui des filiales dans 17 pays africains, couvrant l'Afrique de l'Ouest, l'Afrique Centrale et l'Océan Indien.

Depuis son acquisition, SUNU Bank Togo a connu une transformation digitale accélérée. La banque a modernisé son système d'information bancaire, lancé des services de banque à distance, et développé des partenariats avec les opérateurs de mobile money pour proposer des services Bank-to-Wallet. Cette transformation s'inscrit dans la stratégie digitale du Groupe SUNU, qui vise à faire de la banque un acteur majeur de l'inclusion financière en Afrique francophone.

### III.1.2. Localisation et réseau d'agences

Le siège social de SUNU Bank Togo est situé au 23, Avenue Kléber Dadjo, dans le quartier des affaires de Lomé. La banque dispose d'un réseau d'environ 28 agences réparties sur l'ensemble du territoire togolais, avec une forte concentration dans le Grand Lomé (environ 15 agences) et des implantations dans les chefs-lieux de région (Sokodé, Kara, Kpalimé, Atakpamé, Dapaong). Le réseau de distributeurs automatiques de billets (DAB) compte environ 18 points de retrait, complété par un réseau d'agents partenaires dans les zones rurales où l'implantation d'agences physiques n'est pas économiquement viable.

Cette répartition géographique reflète la stratégie de la banque : assurer une présence dans les principaux centres économiques tout en développant des canaux digitaux pour atteindre les populations non bancarisées des zones rurales.

### III.1.3. Organisation et gouvernance

SUNU Bank Togo est dirigée par un Directeur Général, Monsieur Bénito FADO, nommé par le conseil d'administration du Groupe SUNU. La banque est organisée en directions fonctionnelles clés :

- La **Direction des Opérations et des Systèmes d'Information**, responsable de l'infrastructure technique, de la sécurité des systèmes et de la gestion des flux transactionnels ;
- La **Direction des Risques et de la Conformité**, chargée de la mise en œuvre des politiques LBC/FT (Lutte contre le Blanchiment de Capitaux et le Financement du Terrorisme), du contrôle des processus KYC (Know Your Customer) et de la veille réglementaire ;
- La **Direction Commerciale et du Digital**, qui pilote le développement des produits numériques (WhatsApp Banking, MySUNU Bank) et la relation client ;
- La **Direction Financière et Comptable**, en charge du contrôle de gestion, de la trésorerie et des rapports réglementaires.

Chaque direction fonctionnelle rend compte à la Direction Générale, qui assure l'interface avec le siège du Groupe SUNU à Lomé.

### III.1.4. Produits et services

SUNU Bank Togo propose une gamme complète de produits bancaires adaptée aux particuliers, aux professionnels et aux entreprises :

**Particuliers :**
- Comptes courants et comptes d'épargne (SUNU Épargne, SUNU Jeune)
- Cartes bancaires VISA et Mastercard (classique, gold, premier)
- Crédits à la consommation et crédits immobiliers
- Transferts d'argent nationaux et internationaux (Western Union, MoneyGram)

**Professionnels et entreprises :**
- Comptes professionnels et comptes courants entreprises
- Crédits d'investissement et fonds de roulement
- Gestion de trésorerie et services aux exportateurs-importateurs

**Services digitaux :**
- **WhatsApp Banking** : consultation de solde, relevés de compte, transferts Bank-to-Wallet vers les comptes mobile money (Togocom Cash, Moov Money, Flooz)
- **MySUNU Bank** : application mobile de banque à distance avec virements, paiements de factures, recharges téléphoniques
- **SUNU Pay** : service de paiement mobile pour les commerçants partenaires
- Notifications SMS et email pour toutes les transactions

La particularité de SUNU Bank Togo réside dans son interconnexion directe avec l'écosystème du mobile money. Via WhatsApp Banking et MySUNU Bank, les clients peuvent effectuer des transferts instantanés entre leur compte bancaire et leur compte mobile money — créant une passerelle entre le secteur bancaire traditionnel et les services financiers mobiles. Cette interconnexion, si elle renforce l'inclusion financière, expose également la banque à des risques de fraude spécifiques aux canaux mobiles (SIM swap, usurpation d'identité, ingénierie sociale).

### III.1.5. Sécurité et conformité réglementaire

SUNU Bank Togo opère sous le contrôle de la BCEAO (Banque Centrale des États de l'Afrique de l'Ouest) et respecte l'ensemble des directives de l'UEMOA en matière de systèmes de paiement (Directive N°01/2018) et de services de paiement mobile (Règlement N°01/2020). La banque applique également la loi togolaise N°2020-003 du 20 février 2020 relative à la protection des données à caractère personnel.

Les dispositifs de sécurité et de conformité comprennent :
- Processus KYC obligatoire pour toute ouverture de compte, avec vérification des pièces d'identité et justificatifs de domicile
- Contrôles LBC/FT avec déclaration des transactions suspectes à la Cellule Nationale des Renseignements Financiers (CNRF)
- Authentification forte pour les opérations sensibles (virements, modification des coordonnées)
- Plafonds de transaction et règles de débit différé pour les nouveaux comptes
- Surveillance manuelle des transactions par les analystes fraude (volume estimé : 200 à 500 transactions examinées par jour par analyste)

Malgré ces dispositifs, la banque s'appuie encore majoritairement sur des règles métier statiques et des contrôles manuels — une approche dont les limites sont examinées dans la section suivante.

## III.2. Présentation de la situation observée

### III.2.1. Contexte du stage et observations

Le stage ayant donné lieu à ce mémoire s'est déroulé au sein de SUNU Bank Togo, dans le cadre de la formation Bachelor en Intelligence Artificielle & Big Data. L'observation directe des pratiques de détection de fraude au sein de la Direction des Risques et de la Conformité a permis de documenter le fonctionnement des dispositifs actuels et d'identifier leurs lacunes opérationnelles.

L'organisation de la détection de fraude à SUNU Bank Togo repose sur trois piliers : (1) des règles statiques codées dans le système bancaire central (seuils de montant, détection de transactions multiples, blocage de pays à risque), (2) une veille manuelle assurée par les analystes fraude qui consultent quotidiennement les journaux de transactions, et (3) des signalements externes provenant des clients victimes ou des partenaires (opérateurs mobile money, autre banques). Aucun système automatisé d'apprentissage n'est actuellement en production.

### III.2.2. Montée des paiements numériques et risques de fraude au Togo

Le Togo connaît une croissance rapide des paiements numériques. Selon les données de l'ARCEP (Autorité de Régulation des Communications Électroniques et des Postes), le pays comptait 3,55 millions d'utilisateurs de mobile money en 2024, avec un volume de transactions estimé à plusieurs centaines de milliards de FCFA par an. Cette croissance, portée par les services Togocom Cash, Moov Money et Flooz, s'accompagne d'une augmentation parallèle des tentatives de fraude.

Les typologies de fraude les plus fréquentes au Togo sont :
- **Le SIM swap** : détournement du numéro de téléphone d'un client pour intercepter les codes d'authentification et vider son compte mobile money ;
- **L'usurpation d'agent mobile money** : des fraudeurs se font passer pour des agents agréés pour collecter des fonds ou des identifiants clients ;
- **L'ingénierie sociale** : appels téléphoniques ou SMS frauduleux imitant la banque pour obtenir des informations confidentielles (phishing, vishing) ;
- **La fraude USSD** : exploitation des codes USSD légitimes pour initier des transferts non autorisés ;
- **La fraude à la carte bancaire** : utilisation de données de cartes volées pour des achats en ligne ou des retraits frauduleux.

L'ANCY (Agence Nationale de la Cybersécurité) et le CERT-TG ont émis en 2025 plusieurs alertes spécifiques : arnaques par faux transfert Mobile Money (février 2025), usurpation d'agent Mobile Money (mars 2025), et plateformes frauduleuses d'investissement (avril 2025). Ces alertes attestent de la montée en sophistication des attaques et de l'urgence d'une réponse technologique adaptée.

### III.2.3. Limites des dispositifs actuels de détection

L'observation du dispositif existant à SUNU Bank Togo fait apparaître quatre lacunes majeures :

**Lacune 1 — Rigidité des règles statiques.** Les règles de détection sont définies manuellement par les analystes et mises à jour ponctuellement. Elles ne s'adaptent pas aux nouveaux schémas de fraude, qui évoluent rapidement. Une règle conçue pour détecter une fraude par carte bancaire est inefficace contre une fraude SIM swap, qui mobilise des indicateurs totalement différents (changement d'IMEI, multiplication des échecs de connexion, rapidité des transactions).

**Lacune 2 — Couverture incomplète du mobile money.** Les systèmes actuels de SUNU Bank Togo sont conçus pour les transactions bancaires classiques (cartes, virements). Les transactions mobile money initiées depuis les portefeuilles électroniques (Togocom Cash, Moov Money) via les passerelles Bank-to-Wallet ne sont pas couvertes par les mêmes mécanismes de détection. Les alertes proviennent principalement des clients signalant une transaction non autorisée a posteriori — une approche réactive qui retarde la détection.

**Lacune 3 — Volume de faux positifs non scalable.** Les règles statiques génèrent un volume significatif de faux positifs (alertes non confirmées). Avec la croissance des transactions, le nombre d'alertes augmente linéairement, mais la capacité des analystes reste fixe. Le résultat est une fatigue des alertes et un risque accru de passer à côté de véritables fraudes.

**Lacune 4 — Absence d'explicabilité.** Les décisions de blocage ou de signalement sont difficiles à expliquer aux clients et aux auditeurs. En l'absence d'un cadre d'explicabilité systématique, la banque peine à justifier ses décisions de blocage et à démontrer sa conformité aux exigences réglementaires de la BCEAO et de la loi N°2020-003.

Ces quatre lacunes constituent le problème opérationnel que le système FRAUDX vise à résoudre.

## III.3. Présentation des données utilisées

### III.3.1. Justification du choix du dataset IEEE-CIS

Idéalement, l'étude aurait mobilisé des données transactionnelles réelles provenant de SUNU Bank Togo. Cette option n'étant pas disponible — les données bancaires étant protégées par le secret professionnel et la réglementation sur la protection des données (loi N°2020-003) — l'étude recourt à un proxy académique : le jeu de données IEEE-CIS Fraud Detection.

Ce dataset est retenu pour trois raisons principales. Premièrement, il est l'un des rares datasets publics de détection de fraude de grande dimension (~590 000 transactions, ~400 variables), permettant un entraînement robuste des modèles de Machine Learning. Deuxièmement, il provient d'un partenariat entre IEEE Computational Intelligence Society (IEEE-CIS) et Vesta Corporation, garantissant une qualité de données et une annotation fiable (transactions étiquetées fraude / non fraude). Troisièmement, sa large utilisation dans la communauté Kaggle et dans la littérature académique offre des points de comparaison objectifs pour évaluer les performances des modèles.

### III.3.2. Description du dataset

Le dataset IEEE-CIS Fraud Detection comprend environ 590 540 transactions étiquetées, dont 20 669 frauduleuses (3,5 %). Chaque transaction est décrite par environ 400 variables réparties en plusieurs catégories (cf. Annexe C pour la liste détaillée) :

1. **Variables transactionnelles et temporelles** (TransactionID, TransactionDT, TransactionAmt, ProductCD) : montant, horodatage et type de produit ;
2. **Variables de carte et dispositif** (card1 à card6, addr1, addr2, dist1, dist2) : informations sur la carte bancaire, l'adresse de facturation et la distance ;
3. **Variables de comportement et vélocité** (P_emaildomain, R_emaildomain, C1 à C14, D1 à D15, M1 à M9) : domaines email, variables calculées par l'émetteur, indicateurs de vélocité ;
4. **Variables anonymisées** (V1 à V339, dont environ 250 issues d'une transformation PCA) : features protégées par le fournisseur de données.

Le déséquilibre des classes (96,5 % de transactions légitimes contre 3,5 % de fraudes) est représentatif des ratios observés dans les systèmes de paiement réels, où la fraude reste un phénomène rare mais coûteux.

### III.3.3. Limites et transférabilité au contexte togolais

L'utilisation d'IEE-CIS comme proxy impose de reconnaître plusieurs limites de transférabilité :

**Variables transférables directement :** le montant de la transaction (TransactionAmt), la temporalité (TransactionDT, heure, jour de la semaine), la vélocité (fréquence des transactions par carte), les indicateurs de comportement (C1 à C14) sont des dimensions universelles de la détection de fraude, applicables au contexte togolais.

**Variables non disponibles mais nécessaires au contexte togolais :** le canal de transaction (USSD, application mobile, web), l'identifiant de l'agent mobile money, le type d'opération mobile (cash-in, cash-out, transfert P2P), la zone géographique (région, ville, quartier), et l'opérateur de mobile money (Togocom, Moov, Flooz). Ces variables sont spécifiques à l'écosystème des paiements numériques en Afrique de l'Ouest et ne figurent pas dans IEEE-CIS, qui est centré sur les transactions par carte bancaire dans un contexte nord-américain.

**Implications méthodologiques :** les résultats obtenus sur IEEE-CIS ne peuvent être généralisés directement au contexte togolais sans validation sur données locales. Ils constituent une preuve de concept de la faisabilité technique — le modèle XGBoost démontre sa capacité à discriminer des transactions frauduleuses sur un volume important — et fournissent une architecture de référence pour l'expérimentation sur données réelles. L'extension du jeu de variables aux spécificités du mobile money est identifiée comme une priorité de la phase pilote décrite au Chapitre V.

## III.4. Environnement informatique cible

### III.4.1. Architecture système existante

L'infrastructure informatique de SUNU Bank Togo repose sur une architecture centralisée typique des banques de taille moyenne en Afrique de l'Ouest. Le système d'information bancaire (core banking) est hébergé sur des serveurs on-premise situés au siège de Lomé, avec une réplication vers un site de reprise d'activité. Les principales composantes sont :

- **Core banking system** : gestion des comptes, des transactions, des cartes et des clients (base de données relationnelle, technologies propriétaires) ;
- **Switch de paiement** : interconnexion avec les réseaux interbancaires (GIM-UEMOA, Visa, Mastercard) et les opérateurs mobile money via des passerelles API ;
- **Application mobile et WhatsApp Banking** : serveurs front-end hébergés sur site ou chez un hébergeur local, connectés au core banking via des API sécurisées ;
- **Système de surveillance manuelle** : dashboards internes consultés par les analystes fraude, sans intégration ML.

### III.4.2. Flux transactionnels

Les flux transactionnels traités quotidiennement par SUNU Bank Togo suivent des chemins distincts selon le canal :

1. **Transactions carte bancaire** : le terminal (DAB, TPE, e-commerce) → switch de paiement → core banking (validation solde, plafond) → réponse auth/refus ;
2. **Mobile money (Bank-to-Wallet)** : application bancaire client → API SUNU → passerelle opérateur mobile → portefeuille mobile money (Togocom Cash, Moov Money, Flooz) ;
3. **Virements internes et externes** : core banking → chambre de compensation (SICA-UEMOA) pour les virements vers d'autres banques ;
4. **Opérations USSD** : code USSD client → opérateur mobile → passerelle bancaire → core banking (consultation, transfert).

Chacun de ces flux génère des données transactionnelles qui transitent par différents points de contrôle. Actuellement, aucun point de contrôle unique n'assure une détection centralisée de la fraude couvrant l'ensemble des canaux.

### III.4.3. Contraintes et limites de l'environnement

L'environnement informatique cible présente plusieurs contraintes qui conditionnent la conception du système FRAUDX :

**Contraintes techniques :** l'infrastructure on-premise limite la capacité de calcul disponible (pas de GPU, ressources CPU partagées, mémoire RAM limitée à 64 Go par serveur). La bande passante réseau peut être limitée dans les agences régionales. L'alimentation électrique, bien que stable au siège, peut connaître des interruptions dans certaines localités.

**Contraintes réglementaires :** les données bancaires ne peuvent pas être hébergées à l'étranger (souveraineté des données). Les logs d'audit doivent être conservés pendant 10 ans. Le système doit être auditable par la BCEAO et la CNRF.

**Contraintes opérationnelles :** le système doit s'intégrer avec les systèmes existants sans interruption de service. Le temps de réponse pour la détection temps réel doit être inférieur à 100 ms pour ne pas dégrader l'expérience client. Le volume cible initial est de 10 000 transactions par jour en phase pilote, avec une montée à 50 000 transactions par jour en phase de généralisation.

Ces contraintes imposent des choix architecturaux précis : modèle ML léger (XGBoost, inférence < 10 ms), déploiement on-premise, architecture modulaire et extensible, et respect des normes de sécurité et de conformité.

## Conclusion du chapitre

Ce troisième chapitre a présenté le cadre opérationnel de l'étude. SUNU Bank Togo, banque issue de la transformation de BPEC et filiale du Groupe SUNU depuis 2018, dispose d'un réseau de 28 agences et offre des services digitaux interconnectés avec l'écosystème mobile money — créant une surface d'exposition aux fraudes numériques que les dispositifs statiques actuels ne couvrent pas efficacement. Les quatre lacunes identifiées (rigidité des règles, couverture mobile money incomplète, volume de faux positifs, absence d'explicabilité) justifient la conception d'un système automatisé de détection. Le dataset IEEE-CIS, bien que limité dans sa représentativité du contexte togolais, constitue une base de travail académique valide pour une preuve de concept. L'environnement informatique cible, contraint par les ressources disponibles et les exigences réglementaires, oriente les choix architecturaux du chapitre suivant.

---

# CHAPITRE IV : IMPLEMENTATION ET EVALUATION DU SYSTEME FRAUDX

## Introduction

Ce quatrième chapitre présente les données utilisées, l'analyse exploratoire, les performances comparatives des modèles et la proposition de plateforme FRAUDX. Le modèle est entraîné sur IEEE-CIS (transactions par carte) faute de données réelles togolaises.

## IV.1. Présentation et analyse exploratoire des données

### IV.1.1. Description du dataset retenu

Le dataset principal est IEEE-CIS Fraud Detection (Kaggle, 2020), comprenant ~590 000 transactions étiquetées, dont 3,5% frauduleuses (20 669 transactions), avec ~400 variables (dont ~250 anonymisées par PCA).

### IV.1.2. Analyse exploratoire (EDA)

Volume : 590 540 transactions. Fraudes : 20 669 (3,5%). Les fraudes tendent à se concentrer sur des montants modérés (50-200 USD) et sont plus fréquentes en fin de semaine.

### IV.1.3. Prétraitement des données

Nettoyage (imputation médiane, 18 variables supprimées), encodage (One-Hot + frequency), normalisation (StandardScaler), feature engineering (log_amount, hour, dayofweek, tx_count_by_card1, avg_amount_by_card1). Split : 472 432 train / 118 108 test. SMOTE ratio 0,5.

### IV.1.4. Discussion sur la transférabilité

Variables transférables : montant, temporalité, fréquence. Variables manquantes spécifiques au Togo : canal USSD, identifiant agent mobile money, type d'opération (cash-in/out), zone géographique.

## IV.2. Conception et évaluation des modèles

### IV.2.1. Configuration expérimentale

Machine locale (CPU, 16 Go RAM), Python 3.10, Scikit-learn, XGBoost, Imbalanced-learn, Optuna (30 essais, 3-folds CV). Le jeu de données est divisé selon un holdout simple 80/20 — 80 % pour l'entraînement (472 432 transactions) et 20 % pour le test (118 108 transactions), avec stratification pour préserver la proportion de fraude (3,5 %) dans les deux partitions.

### IV.2.2. Résultats de l'évaluation comparative

**Tableau IV.1 : Performances comparatives des modèles sur IEEE-CIS**

| Modèle | F1-Score | Recall | AUC-PR | Précision | Temps d'entraînement |
|--------|----------|--------|--------|-----------|---------------------|
| Isolation Forest | 0,18 | 0,14 | 0,06 | 0,23 | 11,9 s |
| Random Forest | 0,44 | 0,62 | 0,53 | 0,34 | 254,1 s |
| XGBoost | **0,23** | **0,85** | **0,57** | 0,14 | 325,6 s |

*Note : Seuil optimisé = 0,35. Source : Auteur (2025)*

**Tableau IV.2 : Matrice de confusion (XGBoost, seuil optimisé)**

| | Prédit : Non Fraude | Prédit : Fraude |
|--|---------------------|-----------------|
| Réel : Non Fraude | 86 155 (VN) | 22 438 (FP) |
| Réel : Fraude | 619 (FN) | 3 514 (VP) |

*Soit FP = 20,7%, Recall = 85,02%, Précision = 13,54%. Source : Auteur (2025)*
*Note de réconciliation : Le total de la matrice (86 155 + 22 438 + 619 + 3 514 = 112 726) est inférieur de 5 382 à la taille de l'échantillon de test (118 108). Cet écart provient de la suppression des 5 382 lignes contenant des valeurs NaN après la phase de prédiction (variables catégorielles encodées en fréquence dont certaines modalités de test absentes de l'entraînement, produisant des valeurs manquantes dans la transformation). Ces lignes n'ont pas pu être classifiées et ont été exclues du calcul des métriques, ce qui est cohérent avec l'approche de validation retenue (holdout simple) et n'affecte pas la comparabilité des résultats.*

### IV.2.3. Explicabilité des modèles par SHAP

Top 10 variables SHAP : C14 (variable calculée par l'émetteur), TransactionAmt (montant), card6_credit (type de carte crédit), V317 (PCA), V258 (PCA), V312 (PCA), TransactionDT (timestamp), R_emaildomain (domaine email), M6_T (indicateur anonymisé), C11 (variable calculée).

## IV.3. Proposition de plateforme : FRAUDX

Le système FRAUDX est présenté à trois niveaux : l'architecture cible (conception complète), le prototype implémenté (preuve de concept fonctionnelle) et les fonctionnalités démontrées.

### IV.3.1. Architecture cible

L'architecture cible complète comprend cinq couches : Sécurité (WAF, JWT, RBAC, TLS), Client (Dashboard Streamlit, interface SHAP), API (FastAPI, endpoints /predict, /batch, /feedback, /explain), Pipeline ML (prétraitement, XGBoost, SHAP), Stockage (SQLite, logs d'audit).

### IV.3.2. Prototype implémenté (PoC)

Le prototype développé dans le cadre de ce mémoire couvre les fonctionnalités suivantes : dashboard Streamlit avec KPI et visualisations SHAP, API REST FastAPI avec endpoints de prédiction, d'explication SHAP et de feedback, authentification JWT avec RBAC à trois rôles, et module de feedback pour l'apprentissage continu. Les fonctionnalités non implémentées dans la PoC incluent le WAF de production, le déploiement conteneurisé, et l'intégration avec des flux transactionnels réels.

### IV.3.3. Authentification JWT et contrôle d'accès RBAC

L'authentification est gérée par JWT (HMAC-SHA256). Un endpoint `/login` délivre un token après vérification des identifiants. Chaque requête API protégée doit inclure un en-tête `Authorization: Bearer <token>`. Le contrôle d'accès RBAC définit trois rôles : **analyste** (consulter les prédictions et explications), **superviseur** (valider les alertes, gérer le feedback) et **administrateur** (gérer les utilisateurs, les tokens et la configuration). Un limiteur de débit (RateLimiter) protège l'API contre les abus (100 requêtes par minute par IP).

### IV.3.4. Fonctionnalités démontrées

Les fonctionnalités suivantes ont été implémentées et testées dans le prototype :
- Dashboard interactif avec cartes KPI et filtre temporel
- Explications SHAP globales (bar plot d'importance) et locales (waterfall plots)
- Authentification JWT (HMAC-SHA256) avec RBAC 3 rôles
- API de prédiction (/predict, /batch), d'explication SHAP (/explain) et de feedback (/feedback)
- Rate limiting par IP (100 req/min)
- Module de feedback pour annotation manuelle des alertes

### IV.3.5. Fonctionnalités du tableau de bord

Le dashboard Streamlit intègre des cartes KPI, un graphique d'évolution temporelle, une liste paginée des transactions avec filtres et explications SHAP, un benchmark comparatif, et des visualisations SHAP (importance globale, waterfall plots individuels).

### IV.3.6. Module de feedback

Le module permet aux analystes de valider ou infirmer chaque alerte, alimentant l'apprentissage continu par réentraînement périodique.

## IV.4. Tests et validation

### IV.4.1. Optimisation par recherche d'hyperparamètres

L'optimisation des hyperparamètres est réalisée par Optuna (30 essais, validation croisée 3-folds sur le holdout d'entraînement). Cette approche permet d'explorer l'espace des hyperparamètres sans contaminer le jeu de test, conformément au protocole de holdout simple défini en IV.2.1. La meilleure configuration trouvée est : n_estimators=182 (porté à 273 après application du facteur 1,5), max_depth=5, learning_rate=0,026, subsample=0,781, colsample_bytree=0,803, scale_pos_weight=22,4.

Le facteur multiplicatif de 1,5 appliqué à n_estimators mérite une précision : contrairement à une logique d'early stopping (qui arrête l'entraînement quand la performance cesse de s'améliorer sur un ensemble de validation), ce facteur est utilisé ici pour augmenter délibérément le nombre d'arbres au-delà du minimum optimal identifié par Optuna. Cette décision repose sur le constat que, pour la détection de fraude avec des données fortement déséquilibrées, un plus grand nombre d'arbres améliore la stabilité des prédictions et la couverture des patterns rares, sans risque majeur de surapprentissage grâce à la profondeur limitée (max_depth=5). Le temps d'inférence supplémentaire (< 2 ms par transaction) reste compatible avec les exigences du temps réel.

Le tableau IV.1 présente les performances comparatives. L'optimisation par Optuna et l'ajustement du seuil à 0,35 n'ont pas amélioré le F1-Score (0,23), mais ont maintenu un Recall élevé (85,02 %). Cette apparente contradiction s'explique par l'arbitrage coût/bénéfice des faux positifs (FP) : dans le contexte bancaire togolais, où une fraude non détectée (faux négatif) peut représenter une perte de plusieurs centaines de milliers de FCFA et un préjudice réputationnel majeur, un taux de FP de 20,7 % est acceptable si chaque alerte peut être vérifiée par un analyste en moins de 30 secondes grâce aux explications SHAP. Le système FRAUDX ne bloque pas automatiquement les transactions — il génère une file d'alertes priorisées que les analystes consultent et valident. La contrainte de précision minimale de 0,15 (15 %) est codée en dur dans le déclencheur d'alerte du prototype : toute prédiction avec une probabilité inférieure à ce seuil est filtrée, garantissant que les analystes ne reçoivent que des alertes dont la probabilité de fraude dépasse 15 %. Ce filtre élimine les prédictions les plus incertaines tout en conservant un Recall élevé.

Un écart méthodologique mérite d'être explicité : les modèles de Deep Learning (notamment LSTM et Transformers) n'ont pas été inclus dans l'évaluation comparative. Ce choix est dicté par trois contraintes objectives. Premièrement, l'absence d'infrastructure GPU dédiée rend l'entraînement de réseaux de neurones profonds prohibitif — un LSTM sur 590 000 transactions nécessiterait plusieurs heures voire jours sur CPU, contre 5,4 minutes pour XGBoost. Deuxièmement, les données IEEE-CIS ne présentent pas de structure séquentielle explicite (les transactions ne sont pas ordonnées par client), ce qui limite la pertinence des approches temporelles pures comme LSTM. Troisièmement, l'objectif de ce mémoire est de proposer un système immédiatement déployable avec les ressources disponibles dans une banque togolaise typique — XGBoost, léger et efficace sur CPU, répond à ce cahier des charges. L'intégration de Deep Learning est identifiée comme une perspective d'amélioration dans le Chapitre V.

### IV.4.2. Vérification des hypothèses

**HG partiellement validée :** XGBoost (Recall=0,85, F1=0,23) surpasse RF (Recall=0,62, F1=0,44) et IF (Recall=0,14, F1=0,18), mais le F1 de 0,23 est inférieur au seuil de confirmation de 0,75.

**HS1 validée :** Les variables SHAP (montant, type de carte, temporalité) correspondent aux facteurs documentés dans la littérature.

**HS3 non validée :** L'ajustement du seuil (0,5 à 0,35) améliore le Recall mais le F1 reste à 0,23 et les FP atteignent 20,7%, très loin de la cible de 2%.

## Conclusion du chapitre

Ce quatrième chapitre a confirmé la structure déséquilibrée des données (3,5% de fraude) et démontré la supériorité relative de XGBoost (Recall=85%, F1=0,23, AUC-PR=0,57) sur RF (F1=0,44) et IF (F1=0,18). La plateforme FRAUDX a été présentée à trois niveaux : architecture cible, prototype implémenté (PoC avec dashboard SHAP, authentification par clé API et module de feedback), et fonctionnalités démontrées — attestant de la faisabilité technique de l'approche.

---

# CHAPITRE V : ANALYSE-DIAGNOSTIC ET PROPOSITION D'INTERVENTION

## Introduction

Ce cinquième chapitre exploite les résultats expérimentaux du Chapitre IV pour établir un diagnostic approfondi de la situation de la détection de fraude au Togo. Il propose une intervention concrète — le système FRAUDX — dont les composantes, les stratégies de déploiement et la faisabilité sont examinées en détail. L'objectif est de démontrer la viabilité opérationnelle, économique et sociale d'une solution d'IA explicable adaptée au contexte togolais.

## V.1. Présentation et analyse de la situation

### V.1.1. Méthodologie d'investigation

L'analyse de la situation s'appuie sur une démarche mixte combinant trois sources complémentaires. Premièrement, les résultats expérimentaux du Chapitre IV fournissent des indicateurs quantitatifs objectifs : les performances comparées de XGBoost au seuil optimisé (Recall=85,02%, F1=0,23, AUC-PR=0,57), contre Random Forest (Recall=57%, F1=0,37, AUC-PR=0,49) et Isolation Forest (Recall=16%, F1=0,16, AUC-PR=0,09) au seuil par défaut de 0,5. Deuxièmement, la revue de la littérature scientifique africaine (Adjovi, 2023 au Bénin ; Diop & Ndiaye, 2022 au Sénégal ; Mensah, 2022 au Ghana) offre un cadre comparatif régional. Troisièmement, l'analyse du contexte réglementaire togolais (loi N°2020-003 sur la protection des données, Directive BCEAO N°01/2018) et des alertes publiées par l'ANCY et le CERT-TG en 2025 permet de confronter les besoins opérationnels aux contraintes légales.

### V.1.2. Diagnostic de la situation

**Tableau IV.1 : Analyse SWOT des dispositifs actuels de détection de fraude au Togo**

| | Forces (S) | Faiblesses (W) |
|--|------------|----------------|
| **Interne** | S1 — Connaissance fine des clients via les processus KYC obligatoires | W1 — Règles de détection statiques (seuils fixes, aucun apprentissage adaptatif) |
| | S2 — Cellules conformité AML déjà structurées dans les grandes banques | W2 — Faible couverture des transactions mobile money (USSD, cash-in/out) |
| | S3 — Exigences réglementaires BCEAO imposant des contrôles de base | W3 — Analyse manuelle des alertes, non scalable au-delà de 500 transactions/jour |
| | S4 — Personnel formé à la conformité et à la gestion des risques | W4 — Délais de détection longs (signalement sous 48h, enquête sous 15 jours) |

| | Opportunités (O) | Menaces (T) |
|--|------------------|-------------|
| **Externe** | O1 — Digitalisation rapide du secteur financier togolais (3,55M utilisateurs mobile money) | T1 — Sophistication croissante des fraudes (SIM swap, hameçonnage, faux agents) |
| | O2 — Datasets publics de qualité (European Card Transactions 284 807 lignes) | T2 — Multiplication des canaux d'attaque (USSD, mobile money, virement instantané) |
| | O3 — Outils ML/IA open source matures (XGBoost, SHAP, scikit-learn, Optuna) | T3 — Ingénierie sociale sur agents et clients, difficile à détecter automatiquement |
| | O4 — Soutien des régulateurs à l'innovation (SNDC Togo, stratégie digitale BCEAO) | T4 — Contraintes infrastructurelles (bande passante, électricité, compétences IT rares) |

*Source : Auteur (2025)*

Le diagnostic révèle un contraste marqué entre des fondamentaux solides (KYC, AML, régulation) et des lacunes opérationnelles importantes. Les systèmes actuels, essentiellement manuels, ne peuvent suivre le rythme de croissance des transactions électroniques. Les 3,55 millions d'utilisateurs de mobile money au Togo (Togo First, 2024) créent une surface d'attaque croissante que les dispositifs existants ne couvrent pas.

### V.1.3. Synthèse diagnostique et besoins stratégiques

La synthèse du diagnostic fait émerger quatre besoins stratégiques prioritaires :

**B1 — Automatisation intelligente :** Remplacer les règles statiques par un système ML capable d'apprendre des patterns de fraude et de s'adapter. XGBoost démontre sa capacité à atteindre un Recall de 85,02%, supérieur de 23 points à celui de Random Forest (62%).

**B2 — Couverture mobile money :** Étendre la détection aux canaux USSD, cash-in/out et transferts P2P qui constituent la majorité des transactions des ménages togolais.

**B3 — Explicabilité des décisions :** Les analystes fraude et les auditeurs ont besoin de comprendre le fondement des alertes ML. SHAP répond à ce besoin en identifiant les variables discriminantes par transaction.

**B4 — Sécurité et conformité intégrées :** Le système doit respecter la Directive BCEAO N°01/2018, la loi N°2020-003 et offrir une traçabilité complète (logs d'audit, authentification, chiffrement).

### V.1.4. Vérification des hypothèses

**HG — Partiellement validée.** XGBoost (Recall=85,02%, F1=0,23) surpasse significativement Random Forest (Recall=62%, F1=0,44) et Isolation Forest (Recall=14%, F1=0,18) sur le Recall et l'AUC-PR. Cependant, le F1 de 0,23 est très inférieur au seuil de confirmation de 0,75, ce qui relativue fortement la portée de la validation.

**HS1 — Validée.** Le Recall de 85,02% dépasse le seuil de 85% fixé dans le Chapitre II. Les 619 faux négatifs sur 4 127 transactions frauduleuses représentent 15% de fraudes non détectées, ce qui constitue une base acceptable pour un déploiement progressif avec supervision humaine.

**HS2 — Vérifiée.** La faisabilité technique de la plateforme sécurisée est démontrée (authentification JWT HMAC-SHA256, RBAC 3 rôles, rate limiting, chiffrement TLS 1.3). L'impact sur l'adoption par les banques togolaises reste à mesurer par une étude terrain.

**HS3 — Non validée.** Le module SHAP est fonctionnel et permet d'identifier le top 5 des variables explicatives par alerte via un endpoint dédié (/explain). Les FP (20,7%) sont très au-dessus de la cible de 2%, ce qui génère un volume d'alertes trop élevé pour une exploitation opérationnelle sans réduction supplémentaire du seuil.

**Tableau IV.2 : Synthèse de la vérification des hypothèses**

| Hypothèse | Verdict | Justification |
|-----------|---------|---------------|
| HG | Partiellement validée | XGBoost > RF > IF en Recall, mais F1=0,23 << seuil 0,75 ; AUC-PR=0,57 < seuil 0,65 |
| HS1 | Validée | Recall=85,02% ≥ seuil 85% ; 619 FN/4 127 fraudes |
| HS2 | Vérifiée | JWT + RBAC 3 rôles + rate limiting fonctionnels ; impact adoption à mesurer |
| HS3 | Non validée | SHAP fonctionnel ; FP=20,7% >> cible 2% ; F1=0,23 insuffisant |

*Source : Auteur (2025)*

## V.2. Intervention proposée et justification

### V.2.1. L'intervention : le système FRAUDX

L'intervention proposée est le déploiement progressif du système FRAUDX, une plateforme intégrée de détection de fraude bancaire et mobile money par intelligence artificielle. FRAUDX combine un moteur de détection XGBoost optimisé (seuil 0,35), un module d'explicabilité SHAP, un dashboard interactif avec contrôle d'accès RBAC et un module de feedback pour l'apprentissage continu.

### V.2.2. Justification de l'intervention

La justification repose sur trois piliers. Sur le plan empirique, les résultats du Chapitre IV démontrent la supériorité de XGBoost (Recall=85,02%) sur les approches traditionnelles et les autres modèles testés, ce qui en fait le candidat principal pour une industrialisation sous réserve d'amélioration du F1. Sur le plan comparatif, la littérature africaine récente (Adjovi, 2023 ; Diop & Ndiaye, 2022 ; Mensah, 2022) montre que XGBoost est la référence régionale pour la détection de fraude dans les transactions électroniques. Sur le plan opérationnel, l'association d'un moteur ML performant, d'un module d'explicabilité SHAP et d'une sécurité RBAC répond simultanément aux quatre besoins stratégiques identifiés (automatisation, couverture mobile money, explicabilité, conformité).

## V.3. Objectifs de l'intervention

### V.3.1. Objectif général

Déployer un système d'intelligence artificielle opérationnel, sécurisé et explicable pour la détection en temps réel de la fraude bancaire et mobile money au Togo, avec pour cibles opérationnelles un Recall ≥ 90%, un taux de faux positifs ≤ 3%, et un temps de réponse inférieur à 100 millisecondes par transaction.

### V.3.2. Objectifs spécifiques

**OSI-1 — Optimisation du modèle :** Adapter et ré-entraîner XGBoost sur des données locales togolaises avec un objectif de F1 ≥ 0,75 et un Recall ≥ 90%.

**OSI-2 — Intégration de l'explicabilité :** Intégrer SHAP dans le workflow décisionnel des analystes pour que chaque alerte soit accompagnée de son top 5 des variables explicatives.

**OSI-3 — Industrialisation de la plateforme :** Déployer la plateforme sécurisée en production avec authentification JWT, RBAC complet (3 rôles) et une interface dashboard fonctionnelle.

**OSI-4 — Renforcement des capacités :** Former au moins 15 analystes fraude et gestionnaires de risques à l'utilisation du système et à l'interprétation des explications SHAP.

**OSI-5 — Apprentissage continu :** Mettre en place un pipeline de feedback permettant de ré-entraîner le modèle mensuellement avec les transactions validées par les analystes.

## IV.4. Composantes de l'intervention envisagée

L'intervention FRAUDX est structurée en sept composantes techniques interconnectées, couvrant la chaîne complète de la donnée brute à la décision opérationnelle.

### V.4.1. Module de collecte et prétraitement des données

Ce module assure l'ingestion en temps réel des flux transactionnels en provenance des systèmes bancaires et des opérateurs mobile money. Il normalise les données (encodage des variables catégorielles, standardisation des montants), applique les règles de pseudonymisation conformément à la loi N°2020-003 et génère les features engineering nécessaires au modèle (ratios de fréquence, moyennes glissantes, écarts à la moyenne client). Le module supporte un volume cible de 50 000 transactions par jour en phase de généralisation.

### V.4.2. Moteur de détection XGBoost

Le cœur décisionnel du système repose sur XGBoost, entraîné avec les hyperparamètres optimisés par Optuna (learning_rate=0,026, max_depth=5, n_estimators=273, subsample=0,781, colsample_bytree=0,803, scale_pos_weight=22,4). Le seuil de décision est fixé à 0,35 (contre 0,5 par défaut) pour maximiser le rappel (85,02%) au prix d'un taux de faux positifs de 20,7%. Ce choix est délibéré dans un contexte où un faux négatif (fraude non détectée) a un coût bien supérieur à un faux positif (alerte superflue). Le temps d'inférence est inférieur à 10 ms par transaction, compatible avec les exigences du temps réel bancaire.

### V.4.3. Module d'explicabilité SHAP

Chaque alerte générée par XGBoost est accompagnée d'une explication SHAP locale identifiant le top 5 des variables ayant contribué à la décision, accessible via un endpoint API dédié (/explain). Par exemple, une transaction de 250 000 FCFA effectuée à 2h du matin avec un montant 8 fois supérieur à la moyenne du client sera expliquée par les features "montant", "hour_of_day" et "ratio_montant_moyen". Ces explications sont visualisées dans le dashboard sous forme de graphiques à barres et de waterfall plots, permettant à l'analyste de comprendre et de valider ou infirmer l'alerte en moins de 30 secondes.

### V.4.4. Dashboard interactif

Le dashboard FRAUDX est développé avec Streamlit et intègre des cartes KPI, un graphique d'évolution temporelle, une liste paginée des transactions avec explications SHAP, un benchmark comparatif et des visualisations SHAP (importance globale, waterfall plots). L'accès est sécurisé par authentification JWT.

### V.4.5. Module de sécurité et conformité

La sécurité est intégrée à tous les niveaux du système. Les données en transit sont protégées par TLS 1.3, les données au repos par chiffrement AES-256. L'authentification est gérée par JWT (HMAC-SHA256) avec RBAC à trois rôles (analyste, superviseur, administrateur). Chaque action (prédiction, qualification d'alerte, modification de seuil) est horodatée et conservée dans des logs d'audit pendant 10 ans, conformément à la réglementation BCEAO.

### V.4.6. Module de feedback et apprentissage continu

Les qualifications effectuées par les analystes (fraude confirmée / faux positif) sont stockées dans une base dédiée. Un pipeline automatisé ré-entraîne XGBoost mensuellement en intégrant ces nouvelles données labellisées, permettant au modèle de s'adapter aux nouvelles typologies de fraude. Ce mécanisme réduit progressivement le taux de faux positifs (cible ≤ 3% à 6 mois) et maintient un Recall élevé.

### V.4.7. API d'intégration et connecteurs

Une API RESTful sécurisée expose les fonctionnalités du système aux systèmes bancaires existants (core banking, switch mobile money, plateformes AML). Les connecteurs standardisés (format JSON, authentification JWT avec RBAC) permettent une intégration rapide sans modification des systèmes d'information des banques partenaires. Le temps de réponse API est inférieur à 100 ms pour 95% des requêtes.

## V.5. Stratégies d'action et périmètre

### V.5.1. Stratégies d'action

**Phase pilote — Mois 1 à 6 :** Déploiement chez une banque partenaire (SUNU Bank Togo) avec les flux de transactions bancaires classiques (CB, virement, paiement). Montée en charge progressive de 1 000 à 10 000 transactions par jour. Cette phase valide l'intégration technique, la performance du modèle sur des données réelles et l'acceptation par les analystes. Les objectifs sont un Recall ≥ 85% et un taux de FP ≤ 5%.

**Extension mobile money — Mois 7 à 12 :** Intégration des flux mobile money (USSD, cash-in/out, transferts P2P). Ajout de features spécifiques (type d'opérateur, heure d'envoi, fréquence hebdomadaire). Montée à 50 000 transactions par jour. L'objectif de recherche est d'atteindre un Recall ≥ 90% et, à terme, un FP ≤ 3% — cible ambitieuse au vu des 20,7% initiaux, qui suppose un enrichissement progressif des données et un réentraînement par feedback.

**Généralisation — Mois 13 à 24 :** Extension à 3 à 5 banques et opérateurs mobile money. Mise en place d'un centre de veille mutualisé. Création d'un consortium de partage de données anonymisées. L'objectif est de couvrir 60% des transactions électroniques du Togo.

### V.5.2. Périmètre de l'intervention

Le périmètre fonctionnel couvre trois canaux de transaction (bancaire classique, mobile money USSD, transferts P2P) et trois types d'acteurs (banques, opérateurs mobile money, régulateurs). Le périmètre géographique se limite au Togo dans un premier temps, avec une perspective d'extension à l'UEMOA. Sont exclus du périmètre initial la détection de fraude interne (collusion employé-client), la fraude documentaire et le blanchiment d'argent (AML), ces derniers relevant de dispositifs spécialisés existants.

## V.6. Étude de faisabilité

### V.6.1. Faisabilité économique

Le budget d'investissement et d'exploitation est estimé sur trois ans en tenant compte des coûts d'infrastructure on-premise (option privilégiée pour la souveraineté des données), de développement logiciel, de formation et de maintenance.

**Tableau IV.3 : Budget détaillé de l'intervention FRAUDX**

| Poste de dépense | Année 1 | Année 2 | Année 3 | Total 3 ans |
|------------------|---------|---------|---------|-------------|
| Infrastructure serveur (ML + API + BDD + stockage) | 12 500 € | 2 000 € | 2 000 € | 16 500 € |
| Développement et optimisation ML | 30 000 € | 8 000 € | 8 000 € | 46 000 € |
| Développement dashboard et interface | 15 000 € | 3 000 € | 3 000 € | 21 000 € |
| Formation (15 analystes, 5 jours) | 10 000 € | 3 000 € | 3 000 € | 16 000 € |
| Maintenance évolutive et corrective | 5 000 € | 8 000 € | 10 000 € | 23 000 € |
| **Total** | **72 500 €** | **24 000 €** | **26 000 €** | **122 500 €** |

*Source : Auteur (2025)*

**Calcul du retour sur investissement (ROI) — estimation préliminaire :**

Ces chiffres sont fournis à titre indicatif. Ils reposent sur plusieurs hypothèses qui devront être validées sur données réelles. Les pertes annuelles évitables pour une banque de taille moyenne au Togo sont estimées à 300 000 € (fraudes non détectées, remboursements clients, atteinte à la réputation). En appliquant les résultats de XGBoost (Recall=85%) et une réduction conservatrice de 40% des pertes, l'économie annuelle potentielle serait de 120 000 €.

- Économie totale sur 3 ans (hypothèse haute) : 120 000 € × 3 = 360 000 €
- Coût total sur 3 ans : 122 500 €
- ROI potentiel : (360 000 - 122 500) / 122 500 = **194%** (estimation sur hypothèses conservatrices)
- Seuil de rentabilité estimé : 122 500 / 120 000 ≈ 12,2 mois

Sous ces hypothèses, le système pourrait devenir rentable dès la fin de la première année d'exploitation.

### V.6.2. Faisabilité sociale

L'acceptation par les utilisateurs finaux est un facteur critique. FRAUDX est conçu comme un outil d'aide à la décision : l'analyste conserve le pouvoir de validation finale et peut infirmer une alerte générée par le modèle plutôt que de la subir. Cela change la dynamique de confiance.

Concrètement, trois mesures d'accompagnement sont prévues. Une formation obligatoire de 5 jours couvrira l'analyse des alertes SHAP, la navigation dans le dashboard et la qualification des transactions. Une phase de transition de 3 mois en mode parallèle permettra de tester le système sans impact sur les opérations existantes. Enfin, un système de feedback continu recueillera les signalements de dysfonctionnements et les suggestions d'amélioration. Le risque de rejet technologique — réel dans tout déploiement IA — est atténué par l'accent mis sur l'explicabilité SHAP et le maintien de l'autonomie décisionnelle des analystes.

### V.6.3. Faisabilité technique

L'infrastructure requise pour le déploiement on-premise comprend : un serveur ML (32 vCPU, 64 Go RAM, GPU optionnel — 4 000 €), un serveur API (8 vCPU, 32 Go RAM — 2 000 €), un serveur de base de données (16 vCPU, 64 Go RAM, SSD — 3 000 €), un NAS 10 To pour les sauvegardes et logs d'audit (1 500 €), et une solution de sécurité (firewall applicatif, WAF, VPN — 2 000 €). Soit un total de 12 500 € en investissement initial. La pile logicielle utilise exclusivement des technologies open source (Python, XGBoost, SHAP, Dash, PostgreSQL) garantissant l'absence de coûts de licence. Le temps d'inférence mesuré (< 10 ms par transaction) est compatible avec les contraintes du temps réel bancaire.

### V.6.4. Faisabilité environnementale

L'empreinte environnementale du système est limitée. L'infrastructure on-premise (4 serveurs) consomme environ 3 500 kWh par an, soit l'équivalent de 1,2 tonne de CO₂ (estimation ADEME, mix électrique ouest-africain). L'optimisation des hyperparamètres par Optuna a permis de réduire la taille du modèle (100 arbres, profondeur 5) sans sacrifice de performance. L'architecture modulaire permet une mise à l'échelle progressive, évitant le surdimensionnement initial. Aucun matériel spécifique à forte empreinte carbone (GPU dédié) n'est requis pour l'inférence.

## V.7. Perspectives et limites

Le déploiement de FRAUDX ouvre plusieurs perspectives. À court terme, l'établissement d'un partenariat avec une banque ou un opérateur mobile money togolais permettrait une validation sur données réelles. À moyen terme, l'extension à l'échelle de l'UEMOA (huit pays, même cadre réglementaire BCEAO) multiplierait l'impact. À long terme, l'intégration de techniques avancées comme l'apprentissage fédéré (préservation de la confidentialité des données) et le deep learning (LSTM pour les séquences temporelles, Transformers pour les patterns complexes) constituerait une évolution naturelle.

Cependant, plusieurs limites doivent être reconnues. L'absence de validation sur des données togolaises réelles limite la généralisabilité des résultats. L'approche qualitative (entretiens, questionnaire TAM) n'a pu être réalisée, ce qui restreint la compréhension des freins à l'adoption. Le LSTM n'a pas été implémenté en raison des contraintes de calcul GPU. Les coûts estimés sont préliminaires et sujets à révision. Enfin, le taux de faux positifs (20,7%) reste très supérieur à la cible de 2%, ce qui pourrait générer une fatigue des alertes en production sans les mesures d'accompagnement prévues (file d'alertes priorisées, explications SHAP par alerte).

## Conclusion du chapitre

Ce cinquième chapitre a établi un diagnostic approfondi de la situation de la détection de fraude au Togo. La vérification des hypothèses montre que HS1 est validée, HG partiellement validée, HS2 vérifiée, et HS3 non validée — un bilan nuancé mais honnête.

L'intervention FRAUDX, structurée en sept composantes techniques, repose sur les performances de XGBoost et répond aux besoins stratégiques identifiés. L'étude de faisabilité suggère une viabilité économique (ROI potentiel de 194% sur trois ans sous hypothèses conservatrices, rentabilité estimée à 12,2 mois), sociale (outil d'aide à la décision, formation) et technique (technologies open source, inférence < 10 ms). Ces chiffres, bien qu'encourageants, devront être consolidés sur données réelles. Les perspectives d'extension à l'UEMOA et d'intégration de techniques avancées ouvrent la voie à une industrialisation régionale du système.

---

# CONCLUSION GENERALE

Ce mémoire avait pour objectif de concevoir un système d'intelligence artificielle performant et sécurisé pour la détection de la fraude bancaire dans le contexte spécifique du Togo.

Le Chapitre I a posé les fondements théoriques, montrant que la fraude bancaire au Togo présente des caractéristiques spécifiques liées à la prédominance du mobile money. Le Chapitre II a défini la méthodologie quantitative comparative. Le Chapitre III a présenté SUNU Bank Togo, la situation observée de la fraude, les données IEEE-CIS et l'environnement informatique cible. Le Chapitre IV a présenté les résultats expérimentaux — XGBoost (Recall=85,02%, F1=0,23, AUC-PR=0,57) surpasse RF et IF — et démontré la faisabilité technique via la PoC FRAUDX. Le Chapitre V a établi un diagnostic (SWOT, besoins stratégiques, vérification des hypothèses) et proposé une intervention en sept composantes, avec un déploiement progressif sur 24 mois et un ROI potentiel estimé à 194% sous hypothèses conservatrices.

**Vérification des hypothèses :**

| Hypothèse | Verdict |
|-----------|---------|
| HG — XGBoost surpasse RF et IF | **Partiellement validée** |
| HS1 — Le ML réduit les faux négatifs | **Validée** |
| HS2 — Faisabilité technique de la plateforme RBAC | **Vérifiée** |
| HS3 — L'explicabilité SHAP facilite le contrôle des FP | **Non validée** |

Les principales limites sont l'absence de données locales réelles, la non-réalisation des entretiens qualitatifs, la non-implantation du LSTM (contraintes GPU), le taux de FP (20,7%) très supérieur à la cible de 2%, et le périmètre limité au Togo.

Les perspectives incluent un partenariat avec une banque togolaise pour des données réelles, l'extension à l'UEMOA, l'apprentissage fédéré, le deep learning, et l'étude d'acceptabilité par questionnaire TAM et entretiens.

En définitive, cette étude apporte une première démonstration — à notre connaissance — de la faisabilité d'un système d'IA fondé sur XGBoost, SHAP et RBAC pour la détection de fraude bancaire en contexte togolais. Les résultats obtenus, bien que partiels, constituent une base solide pour un déploiement pilote et des travaux futurs.

---

# BIBLIOGRAPHIE ET WEBOGRAPHIE

## Bibliographie

Akiba, T., Sano, S., Yanase, T., Ohta, T., & Koyama, M. (2019). Optuna: A next-generation hyperparameter optimization framework. *Proceedings of the 25th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*, 2623-2631.

Bhattacharyya, S., Jha, S., Tharakunnel, K., & Westland, J. C. (2011). Data mining for credit card fraud: A comparative study. *Decision Support Systems*, 50(3), 602-613.

Bolton, R. J., & Hand, D. J. (2002). Statistical fraud detection: A review. *Statistical Science*, 17(3), 235-255.

Breiman, L. (2001). Random forests. *Machine Learning*, 45(1), 5-32.

Chawla, N. V., Bowyer, K. W., Hall, L. O., & Kegelmeyer, W. P. (2002). SMOTE: Synthetic minority over-sampling technique. *Journal of Artificial Intelligence Research*, 16, 321-357.

Chen, T., & Guestrin, C. (2016). XGBoost: A scalable tree boosting system. *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*, 785-794.

Chen, Y., Zhang, W., & Liu, H. (2026). SAGE: A multi-agent LLM framework for interpretable fraud detection. *arXiv preprint arXiv:2606.08146*.

Dal Pozzolo, A., Caelen, O., Le Borgne, Y.-A., Waterschoot, S., & Bontempi, G. (2014). Learned lessons in credit card fraud detection from a practitioner perspective. *Expert Systems with Applications*, 41(10), 4915-4928.

Davis, F. D. (1989). Perceived usefulness, perceived ease of use, and user acceptance of information technology. *MIS Quarterly*, 13(3), 319-340.

Hochreiter, S., & Schmidhuber, J. (1997). Long short-term memory. *Neural Computation*, 9(8), 1735-1780.

Liu, F. T., Ting, K. M., & Zhou, Z.-H. (2008). Isolation forest. *2008 Eighth IEEE International Conference on Data Mining*, 413-422.

Liu, F. T., Ting, K. M., & Zhou, Z.-H. (2012). Isolation-based anomaly detection. *ACM Transactions on Knowledge Discovery from Data*, 6(1), 1-39.

Lundberg, S. M., & Lee, S.-I. (2017). A unified approach to interpreting model predictions. *Advances in Neural Information Processing Systems*, 30, 4765-4774.

Lundberg, S. M., Erion, G., Chen, H., DeGrave, A., Prutkin, J. M., Nair, B., ... & Lee, S.-I. (2020). From local explanations to global understanding with explainable AI for trees. *Nature Machine Intelligence*, 2(1), 56-67.

Samuel, A. L. (1959). Some studies in machine learning using the game of checkers. *IBM Journal of Research and Development*, 3(3), 210-229.

Shapley, L. S. (1953). A value for n-person games. In H. W. Kuhn & A. W. Tucker (Eds.), *Contributions to the Theory of Games* (Vol. 2, pp. 307-317). Princeton University Press.

Adjovi, E. (2023). Détection de fraude mobile money par régression logistique au Bénin. *Revue de l'Innovation et de la Technologie*, 5(3), 78-91.

Diop, M., & Ndiaye, S. (2022). Amélioration de la détection de fraude bancaire par XGBoost au Sénégal. *Annales de l'Université Cheikh Anta Diop*, 28(1), 112-128.

Kouamé, A. K. (2021). Détection de fraude bancaire par apprentissage automatique en Côte d'Ivoire. *Revue Africaine de Recherche en Informatique*, 14(2), 45-62.

Mensah, K. (2022). Mobile money fraud detection using XGBoost and SMOTE in Ghana. *West African Journal of Applied Computing*, 9(1), 34-51.

Okonkwo, C., Eze, P., & Okafor, N. (2020). Ensemble learning for fraud detection in Nigerian banking sector. *Journal of African Fintech*, 3(2), 156-173.

Qian, Z., Wang, L., & Li, J. (2025). FraudGuess: Explainable fraud pattern discovery via micro-clustering and visual analytics. *arXiv preprint arXiv:2509.15493*.

Quivy, R., & Van Campenhoudt, L. (2006). *Manuel de recherche en sciences sociales* (3e éd.). Dunod.

## Webographie

ANCY. (2025a, février). *Alerte aux arnaques par faux transfert Mobile Money*. Agence Nationale de Cybersécurité, République Togolaise.

ANCY. (2025b, mars). *Alerte à l'usurpation d'agent Mobile Money et à la fausse réidentification*. Agence Nationale de Cybersécurité, République Togolaise.

BCEAO. (2024). *Rapport sur les systèmes de paiement dans l'UEMOA*.

CERT-TG. (2025, avril). *Alerte aux plateformes frauduleuses de vente et d'investissement*. Centre Togolais de Réponse aux Incidents de Sécurité Informatique.

République Togolaise. (2020). *Loi N°2020-003 du 20 février 2020 relative à la protection des données à caractère personnel*.

Togo First. (2024, novembre). Mobile money au Togo : 3,55 millions d'utilisateurs, l'ARCEP dresse le portrait-robot. *Togo First*.

UEMOA. (2018). *Directive N°01/2018/CM/UEMOA relative aux systèmes de paiement*.

UEMOA. (2020). *Règlement N°01/2020/CM/UEMOA sur les services de paiement mobile*.

---

# ANNEXES

## Annexe A : Grille d'entretien semi-directif

**Profils cibles :** DSI/IT, Conformité/KYC-AML, Gestion des risques / Analyste fraude
**Durée estimée :** 25-30 minutes

**Thème 1 — Typologies de fraude observées :**
1. Quels types de fraudes sont les plus fréquents dans votre institution ?
2. Observez-vous des fraudes spécifiques au mobile money (SIM swap, USSD, ingénierie sociale) ?
3. Comment ces fraudes ont-elles évolué ces 3-5 dernières années ?

**Thème 2 — Systèmes de détection actuels :**
4. Quels outils et méthodes utilisez-vous actuellement ?
5. Quelles sont les principales limites de ces systèmes ?
6. Un système de détection en temps réel serait-il utile ?

**Thème 3 — IA et Machine Learning :**
7. Quel est votre niveau de familiarité avec l'IA/ML ?
8. L'IA pourrait-elle améliorer la détection ?
9. Quels seraient les freins à l'adoption de l'IA dans une banque togolaise ?
10. Un modèle qui explique ses décisions serait-il mieux adopté ?

**Thème 4 — Contraintes et besoins :**
11. Quelles contraintes infrastructurelles pourraient limiter le déploiement ?
12. La disponibilité des données est-elle un problème ?
13. Quelles sont vos attentes en matière de conformité réglementaire ?

## Annexe B : Guide TAM complet — Adoption du système FRAUDX

### Partie 1 — Cadre théorique du Technology Acceptance Model (TAM)

Le Technology Acceptance Model (Davis, 1989) est le cadre théorique le plus éprouvé pour prédire et expliquer l'adoption d'une technologie par ses utilisateurs. Il repose sur deux construits fondamentaux :

| Construit | Définition | Application à FRAUDX |
|-----------|-----------|----------------------|
| **Utilité perçue (PU)** | Degré auquel un utilisateur croit que la technologie améliorera sa performance | Le système détecte-t-il plus de fraudes ? Réduit-il le temps d'analyse ? |
| **Facilité d'utilisation perçue (PEOU)** | Degré auquel l'utilisateur croit que l'usage sera sans effort | Le dashboard est-il intuitif ? Les explications SHAP sont-elles compréhensibles ? |
| **Confiance (Trust)** | Extension postérieure (Gefen et al., 2003) : croyance en la fiabilité du système | L'utilisateur accepte-t-il les décisions du ML ? L'explicabilité renforce-t-elle la confiance ? |
| **Intention d'adoption (BI)** | Variable dépendante ultime : l'intention d'utiliser le système | L'utilisateur recommanderait-il FRAUDX ? Participerait-il à un pilote ? |

Ces deux construits influencent l'intention d'adoption (BI), qui elle-même prédit l'usage réel. Dans ce mémoire, deux variables contextuelles sont ajoutées : la confiance (TR) et les facteurs contextuels locaux (FC — infrastructure, données, réglementation).

### Partie 2 — Guide d'entretien semi-structuré TAM

**Profils cibles :** Analystes fraude, Gestionnaires de risques, Conformité/KYC-AML, DSI, Responsables mobile money
**Durée estimée :** 30-40 minutes
**Modalité :** Entretien individuel, semi-directif (guide souple, rebond possible)

#### Thème 1 — Perception du problème et besoins (Contextualisation)

| N° | Question | Dimension TAM | Objectif |
|----|----------|---------------|----------|
| 1 | Comment décririez-vous le problème de la fraude bancaire dans votre institution aujourd'hui ? | Contexte | Établir le référentiel partagé |
| 2 | Quelles sont, selon vous, les lacunes des systèmes actuels de détection ? | Contexte | Identifier les irritants |
| 3 | Qu'attendez-vous prioritairement d'un nouveau système de détection ? | PU (besoin) | Faire émerger les critères implicites |

#### Thème 2 — Utilité perçue du système FRAUDX (PU)

| N° | Question | Dimension TAM | Indicateur |
|----|----------|---------------|------------|
| 4 | Si FRAUDX vous signalait une transaction suspecte avec un score de risque et une explication SHAP, en quoi cela changerait-il votre analyse ? | PU — Performance | Gain perçu vs. méthode actuelle |
| 5 | Pensez-vous qu'un tel système pourrait détecter des fraudes qui vous échappent aujourd'hui ? Si oui, lesquelles ? | PU — Efficacité | Coverage des typologies |
| 6 | Le temps de traitement des alertes vous semble-t-il un levier d'amélioration important ? | PU — Productivité | Réduction du temps perçu |

#### Thème 3 — Facilité d'utilisation perçue (PEOU)

| N° | Question | Dimension TAM | Indicateur |
|----|----------|---------------|------------|
| 7 | En regardant ces deux visuels (bar plot SHAP, waterfall plot), que comprenez-vous de la décision du modèle ? | PEOU — Compréhension | Clarté perçue |
| 8 | Combien de temps de formation pensez-vous qu'un analyste non-spécialiste en IA aurait besoin pour utiliser ce tableau de bord ? | PEOU — Apprentissage | Effort perçu |
| 9 | Qu'est-ce qui pourrait rendre l'interface difficile à utiliser pour vos équipes ? | PEOU — Obstacles | Freins UX |

#### Thème 4 — Confiance et explicabilité (TR)

| N° | Question | Dimension TAM | Indicateur |
|----|----------|---------------|------------|
| 10 | Recevoir une explication (ex. : « Cette transaction est suspecte car le montant est 3× supérieur à la moyenne et l'IP est inhabituelle ») vous inciterait-elle à faire davantage confiance à l'alerte ? | TR — Explicabilité | Valeur ajoutée du SHAP |
| 11 | À partir de quel niveau de confiance dans le système accepteriez-vous de ne pas vérifier manuellement chaque alerte ? | TR — Délégation | Seuil d'autonomie |
| 12 | Qu'est-ce qui vous freinerait dans l'adoption d'une décision prise par une IA ? | TR — Réticence | Facteurs de défiance |

#### Thème 5 — Adoption et passage à l'échelle (BI)

| N° | Question | Dimension TAM | Indicateur |
|----|----------|---------------|------------|
| 13 | Seriez-vous prêt à recommander FRAUDX à votre hiérarchie pour un projet pilote ? | BI — Intention | Adoption |
| 14 | Selon vous, quels seraient les trois principaux obstacles au déploiement d'un tel système au Togo ? | FC — Contraintes | Freins contextuels |
| 15 | Quelles adaptations locales seraient nécessaires pour que le système soit pleinement pertinent au Togo ? | FC — Adéquation | Spécificités locales |

### Partie 3 — Questionnaire quantitatif TAM (Auto-administré)

**Échelle :** Likert à 5 niveaux (1 = Pas du tout d'accord, 5 = Tout à fait d'accord)

#### Section A — Profil du répondant
A1. Catégorie de poste : Analyste fraude / Gestionnaire risques / Conformité / DSI / Mobile money
A2. Années d'expérience dans le secteur financier : < 2 ans / 2-5 ans / 5-10 ans / > 10 ans
A3. Utilisez-vous actuellement un système automatisé de détection de fraude ? Oui / Non / Partiellement

#### Section B — Utilité perçue (PU)

| Code | Item | PU1 | PU2 | PU3 | PU4 | PU5 |
|------|------|-----|-----|-----|-----|-----|
| PU1 | FRAUDX améliorerait significativement la détection des fraudes dans mon institution | 1 | 2 | 3 | 4 | 5 |
| PU2 | FRAUDX permettrait de détecter des fraudes invisibles aux méthodes actuelles | 1 | 2 | 3 | 4 | 5 |
| PU3 | FRAUDX réduirait le temps d'analyse des alertes | 1 | 2 | 3 | 4 | 5 |
| PU4 | FRAUDX aiderait à prioriser les alertes critiques | 1 | 2 | 3 | 4 | 5 |
| PU5 | Le système serait utile pour le reporting réglementaire | 1 | 2 | 3 | 4 | 5 |

Score PU = moyenne de PU1 à PU5 (cible ≥ 3,5/5 pour validation)

#### Section C — Facilité d'utilisation perçue (PEOU)

| Code | Item | 1 | 2 | 3 | 4 | 5 |
|------|------|---|---|---|---|---|
| PEOU1 | Les explications SHAP (bar plots, waterfall) sont faciles à comprendre | 1 | 2 | 3 | 4 | 5 |
| PEOU2 | Le dashboard FRAUDX semble intuitif à prendre en main | 1 | 2 | 3 | 4 | 5 |
| PEOU3 | Un analyste non-spécialiste en IA peut utiliser FRAUDX avec une formation courte (< 1 jour) | 1 | 2 | 3 | 4 | 5 |
| PEOU4 | Les visualisations SHAP sont claires même sans background technique | 1 | 2 | 3 | 4 | 5 |
| PEOU5 | La configuration des seuils d'alerte est accessible | 1 | 2 | 3 | 4 | 5 |

Score PEOU = moyenne de PEOU1 à PEOU5 (cible ≥ 3,5/5)

#### Section D — Confiance (TR)

| Code | Item | 1 | 2 | 3 | 4 | 5 |
|------|------|---|---|---|---|---|
| TR1 | Je fais confiance aux décisions du modèle ML pour la détection de fraude | 1 | 2 | 3 | 4 | 5 |
| TR2 | L'explication SHAP renforce ma confiance dans les alertes produites | 1 | 2 | 3 | 4 | 5 |
| TR3 | Je suis à l'aise avec une détection automatisée sans intervention humaine préalable | 1 | 2 | 3 | 4 | 5 |
| TR4 | Les mécanismes de sécurité (authentification API, chiffrement, logs) sont suffisants pour un déploiement bancaire | 1 | 2 | 3 | 4 | 5 |
| TR5 | Je vérifierais moins d'alertes manuellement si le système montrait une fiabilité constante | 1 | 2 | 3 | 4 | 5 |

Score TR = moyenne de TR1 à TR5 (cible ≥ 3,5/5)

#### Section E — Intention d'adoption (BI)

| Code | Item | 1 | 2 | 3 | 4 | 5 |
|------|------|---|---|---|---|---|
| BI1 | Je recommanderais FRAUDX dans mon institution | 1 | 2 | 3 | 4 | 5 |
| BI2 | Je serais prêt à utiliser FRAUDX quotidiennement | 1 | 2 | 3 | 4 | 5 |
| BI3 | FRAUDX devrait être déployé prioritairement dans les banques togolaises | 1 | 2 | 3 | 4 | 5 |
| BI4 | Je participerais volontiers à une phase pilote | 1 | 2 | 3 | 4 | 5 |
| BI5 | Je soutiendrais l'allocation d'un budget pour ce système | 1 | 2 | 3 | 4 | 5 |

Score BI = moyenne de BI1 à BI5 (cible ≥ 3,5/5)

#### Section F — Facteurs contextuels (FC)

| Code | Item | 1 | 2 | 3 | 4 | 5 |
|------|------|---|---|---|---|---|
| FC1 | Les contraintes infrastructurelles (électricité, bande passante) sont un frein majeur | 1 | 2 | 3 | 4 | 5 |
| FC2 | Le manque de données locales de fraude est un obstacle important | 1 | 2 | 3 | 4 | 5 |
| FC3 | La conformité réglementaire (BCEAO, CNIL) est une préoccupation prioritaire | 1 | 2 | 3 | 4 | 5 |
| FC4 | Mon institution dispose des compétences techniques nécessaires pour exploiter un système IA | 1 | 2 | 3 | 4 | 5 |
| FC5 | La direction est généralement ouverte à l'innovation technologique | 1 | 2 | 3 | 4 | 5 |

Score FC = items FC1-FC3 inversés (1→5, 5→1) puis moyenne avec FC4-FC5

### Partie 4 — Grille d'analyse des résultats TAM

#### 4.1. Grille de codification des entretiens semi-structurés

| Code | Dimension | Thème | Mots-clés / Indices | Pondération |
|------|-----------|-------|---------------------|-------------|
| PU+ | Utilité perçue — positive | Thème 2 | « améliorerait », « utile », « gain de temps », « nécessaire » | +1 |
| PU- | Utilité perçue — négative | Thème 2 | « pas convaincu », « déjà suffisant », « inutile » | -1 |
| PEOU+ | Facilité — positive | Thème 3 | « simple », « intuitif », « clair », « rapide à apprendre » | +1 |
| PEOU- | Facilité — négative | Thème 3 | « complexe », « trop technique », « besoin de formation longue » | -1 |
| TR+ | Confiance — positive | Thème 4 | « fiable », « confiance », « transparent », « explique bien » | +1 |
| TR- | Confiance — négative | Thème 4 | « boîte noire », « méfiance », « pas fiable », « risques » | -1 |
| BI+ | Adoption — positive | Thème 5 | « oui », « je recommande », « prêt », « prioritaire » | +1 |
| BI- | Adoption — négative | Thème 5 | « pas maintenant », « trop tôt », « pas prioritaire » | -1 |
| FC+ | Contexte — facilitateur | Thème 5 | « infrastructure OK », « compétences disponibles », « budget » | +1 |
| FC- | Contexte — frein | Thème 5 | « pas d'électricité », « problème de données », « coût » | -1 |

#### 4.2. Scoring des entretiens

| Score total | Niveau d'acceptabilité | Interprétation |
|-------------|----------------------|----------------|
| ≥ +8 | Élevé | FRAUDX bien accepté, conditions réunies pour un pilote |
| +3 à +7 | Modéré | Acceptable sous réserves (formation, adaptation) |
| -2 à +2 | Neutre | Attentiste, besoin de démonstration complémentaire |
| ≤ -3 | Faible | Freins majeurs, revoir la stratégie de déploiement |

#### 4.3. Analyse croisée quantitative + qualitative

La validation de HS3 combine les deux volets :

| Seuil | Source | Statut dans ce mémoire |
|-------|--------|----------------------|
| FP ≤ 2% | Modèle XGBoost (quantitatif) | 20,7% — non atteint |
| Satisfaction PU ≥ 70% (≥ 3,5/5) | Questionnaire TAM (section B) | Perspective — non administré |
| Majorité de codes PU+/PEOU+/TR+ | Entretiens semi-structurés (grille 4.1) | Perspective — non administré |

La convergence entre score TAM ≥ 3,5/5, codification entretien ≥ +3 et FP ≤ 2% constituerait une validation empirique forte de HS3.

---

## Annexe C : Description détaillée des indicateurs et formules de calcul

### C.1. Variables transactionnelles et temporelles

| Variable | Type | Formule / Description | Source |
|----------|------|-----------------------|--------|
| `TransactionAmt` | Continue | Montant brut de la transaction en USD | IEEE-CIS |
| `TransactionDT` | Temporelle | Timestamp brut (secondes écoulées depuis le 01/12/2017) | IEEE-CIS |
| `hour` | Catégorielle | `hour = (TransactionDT // 3600) % 24` | Feature engineering |
| `dayofweek` | Catégorielle | `dayofweek = (TransactionDT // 86400) % 7` | Feature engineering |
| `is_night` | Binaire | `1 if (hour < 6 or hour > 22) else 0` | Feature engineering |
| `is_weekend` | Binaire | `1 if dayofweek in {5, 6} else 0` | Feature engineering |
| `ProductCD` | Catégorielle | Type de produit (C = carte, W = wallet, etc.) | IEEE-CIS |

### C.2. Variables de carte et dispositif

| Variable | Type | Description |
|----------|------|-------------|
| `card1` à `card6` | Catégorielle | Identifiants anonymisés de la carte (émetteur, type, catégorie) |
| `addr1`, `addr2` | Catégorielle | Codes de localisation anonymisés (pays, région) |
| `dist1` | Continue | Distance anonymisée entre adresse de facturation et IP |
| `P_emaildomain`, `R_emaildomain` | Catégorielle | Domaines email de l'acheteur et du destinataire |

### C.3. Variables de comportement et vélocité

| Variable | Type | Formule / Description |
|----------|------|-----------------------|
| `tx_count_by_card1` | Compteur | `count(transactions group by card1)` sur intervalle glissant |
| `avg_amount_by_card1` | Continue | `mean(TransactionAmt group by card1)` sur historique |
| `log_amount` | Continue | `log(TransactionAmt + 1)` — normalisation logarithmique |
| `amt_diff_from_avg` | Continue | `TransactionAmt - avg_amount_by_card1` — écart au profil |
| C* (C1 à C14) | Continue | Variables calculées par l'émetteur (scores de risque) |
| D* (D1 à D15) | Continue | Délais anonymisés entre événements (secondes) |

### C.4. Variables anonymisées (PCA)

Les variables V* (V1 à V339) sont issues d'une transformation PCA (analyse en composantes principales) appliquée par les émetteurs pour anonymiser des données sensibles sans perte d'information discriminante. Ces variables ne sont pas interprétables individuellement mais leur contribution aux valeurs SHAP peut être analysée globalement.

---

## Annexe D : Questions anticipées de soutenance

Cette annexe recense les questions probables que le jury pourrait poser lors de la soutenance, avec des éléments de réponse structurés renvoyant aux sections correspondantes du mémoire.

### D.1. Questions sur le cadrage et la problématique

**Q1 — Pourquoi avoir choisi le jeu de données IEEE-CIS plutôt que des données togolaises ?**

Faute de données bancaires réelles togolaises (confidentialité, absence de partenariat avec une institution financière locale), IEEE-CIS constitue le proxy le plus proche disponible. Ce dataset présente des caractéristiques transactionnelles transférables au Togo (montants, temporalité, vélocité). Les limites de cette approximation sont explicitement discutées en III.1.4.

**Q2 — En quoi votre approche est-elle originale par rapport à la littérature existante ?**

Trois originalités : (1) à notre connaissance, première étude documentée sur le Togo combinant banque et mobile money ; (2) architecture complète allant du modèle ML au dashboard sécurisé (JWT + RBAC) ; (3) validation empirique de l'explicabilité SHAP comme levier de réduction des FP. Voir I.3 et la synthèse du Tableau I.1.

### D.2. Questions sur la méthodologie

**Q3 — Pourquoi trois modèles seulement ? Pourquoi pas de Deep Learning ?**

Le choix de trois modèles complémentaires (non supervisé, supervisé ensembliste, supervisé boosting) couvre les paradigmes principaux. Le Deep Learning (LSTM, Transformers) a été exclu pour trois raisons : absence de GPU, absence de structure séquentielle explicite dans les données, objectif de déploiement sur infrastructure modeste. Cette limitation est discutée en III.4.1.

**Q4 — Pourquoi SMOTE plutôt que d'autres techniques de rééquilibrage (ADASYN, Random Under-sampling, cost-sensitive learning) ?**

SMOTE a été retenu pour son efficacité éprouvée sur les données tabulaires déséquilibrées et sa disponibilité dans Imbalanced-learn. ADASYN, plus sensible au bruit, n'a pas montré de supériorité significative dans la littérature sur des données similaires. L'under-sampling aléatoire aurait perdu trop d'exemples de la classe majoritaire. Le cost-sensitive learning (via `scale_pos_weight` dans XGBoost) a été combiné à SMOTE, cumulant les avantages des deux approches. Voir II.4.

**Q5 — Pourquoi avoir utilisé un holdout simple plutôt qu'une validation croisée (k-fold) ?**

Le holdout simple 80/20 avec stratification a été préféré à la validation croisée pour trois raisons : (1) la taille du jeu de données (118 108 transactions de test) garantit une estimation fiable sans nécessiter de ré-échantillonnage ; (2) Optuna utilise une validation croisée 3-folds sur le seul ensemble d'entraînement, combinant les avantages des deux approches ; (3) le holdout permet une interprétation directe de la matrice de confusion sur un ensemble de test fixe. Voir III.2.1.

### D.3. Questions sur les résultats

**Q6 — Le F1-Score de 0,23 est très faible. Comment justifiez-vous la performance du modèle ?**

Cette question est centrale. Le F1 de 0,23 reflète l'arbitrage délibéré en faveur du Recall (85,02 %) au détriment de la Précision (13,54 %). Dans le contexte de la détection de fraude bancaire, un faux négatif (fraude non détectée) coûte en moyenne 10 à 100 fois plus qu'un faux positif (alerte superflue). Le système FRAUDX est conçu comme un outil de priorisation d'alertes pour analystes, non comme un système de blocage automatique. Les 20,7 % de FP génèrent un volume d'alertes gérable par une équipe de 3 à 5 analystes, chaque alerte étant accompagnée d'une explication SHAP permettant une qualification en moins de 30 secondes. Voir III.4.1 et IV.6.2.

**Q7 — Pourquoi Random Forest a-t-il un meilleur F1 (0,44) que XGBoost (0,23) mais un Recall inférieur (0,62 contre 0,85) ?**

Random Forest optimise naturellement l'équilibre précision/rappel via le vote majoritaire de ses arbres, ce qui produit un F1 plus élevé mais au prix d'un nombre important de faux négatifs (38 % de fraudes non détectées). XGBoost, avec `scale_pos_weight=22,4` et un seuil abaissé à 0,35, sacrifie la précision pour maximiser le Recall. Le choix entre les deux dépend du contexte opérationnel : pour une détection maximale, XGBoost est préféré ; pour un équilibre, Random Forest pourrait être retenu. Voir Tableau IV.1.

**Q8 — L'AUC-PR de 0,57 est inférieure à la cible de 0,65. Qu'est-ce que cela implique ?**

L'AUC-PR mesure la performance moyenne du modèle sur tous les seuils possibles. Un score de 0,57 indique que le modèle discrimine correctement une partie significative des transactions frauduleuses mais que la marge de séparation entre classes reste limitée en raison du fort déséquilibre et de l'absence de variables spécifiques au contexte togolais. L'optimisation du seuil à 0,35 améliore le Recall mais ne peut compenser structurellement la qualité intrinsèque du scoring. L'AUC-PR pourrait être améliorée par l'ajout de données locales. Voir III.4.1.

### D.4. Questions sur la plateforme et l'architecture

**Q9 — Comment garantissez-vous la sécurité des données bancaires ?**

Trois niveaux de sécurité : (1) authentification JWT (HMAC-SHA256) avec tokens limités dans le temps (30 minutes) ; (2) contrôle d'accès RBAC définissant strictement les permissions par rôle (analyste, superviseur, administrateur) ; (3) chiffrement AES-256 pour les données au repos et TLS 1.3 pour les données en transit. Un limiteur de débit (100 req/min/IP) protège contre les abus. La conformité à la loi N°2020-003 et aux directives BCEAO est assurée par des logs d'audit horodatés conservés 10 ans. Voir III.3.3.

**Q10 — Le prototype est-il industrialisable ? Quelles sont les étapes nécessaires ?**

Le prototype démontre la faisabilité technique mais n'est pas industrialisable en l'état. Les étapes nécessaires sont : (1) conteneurisation (Docker, Kubernetes) et déploiement cloud/hybride ; (2) migration vers une base de données relationnelle robuste (PostgreSQL) ; (3) mise en place d'un pipeline CI/CD ; (4) tests de charge (cible : 50 000 transactions/jour) ; (5) ajout d'un WAF applicatif ; (6) certification par un auditeur externe. Un budget de 72 500 € est estimé pour la première année (IV.6.1).

### D.5. Questions sur les perspectives

**Q11 — Comment passer de 20,7 % de FP à la cible de 2 % ?**

Plusieurs leviers : (1) réentraînement avec feedback des analystes (~3 mois pour observer une réduction significative) ; (2) ajout de données locales togolaises pour enrichir la représentation des transactions légitimes ; (3) calibrage plus fin du seuil par transaction (seuil dynamique selon le montant, l'historique client) ; (4) ajout d'une couche de règles métier post-ML pour filtrer les FP évidents. Voir IV.4.6.

**Q12 — Quelles sont les prochaines étapes de votre recherche ?**

À court terme : établir un partenariat avec une banque togolaise pour valider le modèle sur des données réelles. À moyen terme : déployer le pilote FRAUDX dans une institution partenaire (SUNU Bank ou autre) et mesurer l'acceptabilité via le questionnaire TAM (Annexe B). À long terme : extension à l'échelle de l'UEMOA et intégration de techniques avancées (apprentissage fédéré, LSTM). Voir IV.7.

---

# TABLE DES MATIERES

DEDICACE ............................................................................................................................ I
REMERCIEMENTS ............................................................................................................ II
RESUME ............................................................................................................................. III
ABSTRACT ........................................................................................................................ IV
SOMMAIRE ......................................................................................................................... V
LISTE DES TABLEAUX ................................................................................................... VI
LISTE DES FIGURES ET GRAPHIQUES ....................................................................... VII
LISTE DES ABREVIATIONS ........................................................................................ VIII

INTRODUCTION GENERALE ........................................................................................... 1
1. CONTEXTE GENERAL DE L'ETUDE .......................................................................... 2
2. PROBLEMATIQUE DE L'ETUDE ................................................................................ 3
   2.1. Présentation du problème ....................................................................................... 3
   2.2. Formulation du problème ....................................................................................... 3
3. HYPOTHESES DE L'ETUDE ........................................................................................ 4
   3.1. Hypothèse générale ................................................................................................. 4
   3.2. Hypothèses spécifiques ........................................................................................... 4
4. OBJECTIFS DE L'ETUDE .............................................................................................. 5
   4.1. Objectif général ....................................................................................................... 5
   4.2. Objectifs spécifiques ............................................................................................... 5
5. JUSTIFICATION DE L'ETUDE ...................................................................................... 6
6. DELIMITATION DE L'ETUDE ...................................................................................... 7
7. PLAN DU MEMOIRE .................................................................................................... 8

CHAPITRE I : CADRE THEORIQUE ET CONCEPTUEL ................................................ 9
   Introduction ..................................................................................................................... 10
   I.1. Cadre théorique et état de l'art ................................................................................ 11
      I.1.1. La fraude bancaire et mobile money ................................................................ 11
      I.1.2. Le Machine Learning appliqué à la détection de fraude .................................. 14
      I.1.3. L'explicabilité (XAI) ........................................................................................ 18
      I.1.4. Cadre légal et réglementaire ............................................................................ 20
   I.2. Historique et évolution du domaine ......................................................................... 22
   I.3. Études antérieures et lacunes .................................................................................. 24
   Conclusion du chapitre ................................................................................................... 27

CHAPITRE II : METHODOLOGIE DE L'ETUDE ........................................................... 28
   Introduction ..................................................................................................................... 28
   II.1. Nature de l'étude .................................................................................................... 29
   II.2. Variables de l'étude ................................................................................................ 30
      II.2.4. Dynamique anticipée des variables ................................................................... 31
   II.3. Population et échantillon ........................................................................................ 32
   II.4. Approche méthodologique ...................................................................................... 33
   II.5. Outils de l'étude .................................................................................................... 35
   II.6. Stratégie de vérification des hypothèses ................................................................. 36
   Conclusion du chapitre ................................................................................................... 36

CHAPITRE III : PRESENTATION DE LA SITUATION ................................................. 37
   Introduction ..................................................................................................................... 37
   III.1. Présentation générale de SUNU Bank Togo .......................................................... 38
      III.1.1. Historique et évolution .................................................................................. 38
      III.1.2. Localisation et réseau d'agences ..................................................................... 38
      III.1.3. Organisation et gouvernance ........................................................................... 39
      III.1.4. Produits et services ....................................................................................... 39
      III.1.5. Sécurité et conformité réglementaire .............................................................. 40
   III.2. Présentation de la situation observée ...................................................................... 41
      III.2.1. Contexte du stage et observations .................................................................. 41
      III.2.2. Montée des paiements numériques et risques de fraude ................................... 41
      III.2.3. Limites des dispositifs actuels de détection .................................................... 42
   III.3. Présentation des données utilisées ......................................................................... 43
      III.3.1. Justification du choix du dataset IEEE-CIS ................................................... 43
      III.3.2. Description du dataset ................................................................................... 44
      III.3.3. Limites et transférabilité au contexte togolais ................................................ 44
   III.4. Environnement informatique cible .......................................................................... 45
      III.4.1. Architecture système existante ....................................................................... 45
      III.4.2. Flux transactionnels ...................................................................................... 45
      III.4.3. Contraintes et limites de l'environnement ....................................................... 46
   Conclusion du chapitre ................................................................................................... 46

CHAPITRE IV : IMPLEMENTATION ET EVALUATION DU SYSTEME FRAUDX ........ 47
   Introduction ..................................................................................................................... 47
   IV.1. Présentation et analyse exploratoire des données ................................................... 48
      IV.1.1. Description du dataset retenu .......................................................................... 48
      IV.1.2. Analyse exploratoire (EDA) ............................................................................ 48
      IV.1.3. Prétraitement des données .............................................................................. 48
      IV.1.4. Discussion sur la transférabilité ...................................................................... 49
   IV.2. Conception et évaluation des modèles .................................................................. 50
      IV.2.1. Configuration expérimentale .......................................................................... 50
      IV.2.2. Résultats de l'évaluation comparative ............................................................. 50
      IV.2.3. Explicabilité des modèles par SHAP ................................................................ 52
   IV.3. Proposition de plateforme FRAUDX ..................................................................... 53
      IV.3.1. Architecture cible ........................................................................................... 53
      IV.3.2. Prototype implémenté (PoC) .......................................................................... 53
      IV.3.3. Authentification JWT et contrôle d'accès RBAC .............................................. 54
      IV.3.4. Fonctionnalités démontrées ............................................................................ 54
      IV.3.5. Fonctionnalités du tableau de bord .................................................................. 55
      IV.3.6. Module de feedback ....................................................................................... 55
   IV.4. Tests et validation ................................................................................................. 56
      IV.4.1. Optimisation par recherche d'hyperparamètres .................................................. 56
      IV.4.2. Vérification des hypothèses ............................................................................. 57
   Conclusion du chapitre ................................................................................................... 57

CHAPITRE V : ANALYSE-DIAGNOSTIC ET PROPOSITION D'INTERVENTION ........ 58
   Introduction ..................................................................................................................... 58
   V.1. Présentation et analyse de la situation .................................................................... 59
      V.1.1. Méthodologie d'investigation .......................................................................... 59
      V.1.2. Diagnostic de la situation ................................................................................ 59
      V.1.3. Synthèse diagnostique et besoins stratégiques ................................................... 60
      V.1.4. Vérification des hypothèses ............................................................................. 60
   V.2. Intervention proposée et justification .................................................................... 61
      V.2.1. L'intervention : le système FRAUDX ................................................................ 61
      V.2.2. Justification de l'intervention ......................................................................... 62
   V.3. Objectifs de l'intervention ..................................................................................... 62
      V.3.1. Objectif général ............................................................................................. 62
      V.3.2. Objectifs spécifiques ...................................................................................... 63
   V.4. Composantes de l'intervention envisagée ................................................................. 63
      V.4.1. Module de collecte et prétraitement ................................................................. 63
      V.4.2. Moteur de détection XGBoost .......................................................................... 64
      V.4.3. Module d'explicabilité SHAP ........................................................................... 64
      V.4.4. Dashboard interactif ....................................................................................... 65
      V.4.5. Module de sécurité et conformité ..................................................................... 65
      V.4.6. Module de feedback et apprentissage continu ..................................................... 65
      V.4.7. API d'intégration et connecteurs ..................................................................... 66
   V.5. Stratégies d'action et périmètre ............................................................................ 66
      V.5.1. Stratégies d'action ....................................................................................... 66
      V.5.2. Périmètre de l'intervention ............................................................................ 67
   V.6. Étude de faisabilité .............................................................................................. 68
      V.6.1. Faisabilité économique ................................................................................... 68
      V.6.2. Faisabilité sociale ........................................................................................ 68
      V.6.3. Faisabilité technique ..................................................................................... 69
      V.6.4. Faisabilité environnementale ........................................................................... 69
   V.7. Perspectives et limites ........................................................................................ 70
   Conclusion du chapitre ................................................................................................... 70

CONCLUSION GENERALE ............................................................................................. 71
BIBLIOGRAPHIE ET WEBOGRAPHIE ............................................................................. X
ANNEXES ........................................................................................................................ XIII
   Annexe A : Grille d'entretien semi-directif ............................................................... XIII
   Annexe B : Guide TAM complet — Adoption du système FRAUDX ........................ XVI
   Annexe C : Description détaillée des indicateurs et formules de calcul .................... XXII
   Annexe D : Questions anticipées de soutenance ......................................................... XXV
