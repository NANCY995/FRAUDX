# CONCEPTION D'UN SYSTÈME D'INTELLIGENCE ARTIFICIELLE POUR LA DÉTECTION DE LA FRAUDE BANCAIRE : CAS DU TOGO

### Mémoire de fin d'études — Plan conforme au Guide de Rédaction Scientifique (Collège de Paris Supérieur)

---

## PAGES LIMINAIRES

- Page de garde
- Dédicace
- Remerciements
- Résumé (1 page)
- Abstract (1 page, en anglais)
- Table des matières / Sommaire
- Index des tableaux et figures
- Liste des abréviations (IA, ML, DL, ANN, XGBoost, SHAP, SMOTE, KYC, AML, BCEAO, UEMOA, GIABA…)

---

## INTRODUCTION GÉNÉRALE

### 1. Contexte général de l'étude

L'intelligence artificielle est aujourd'hui au cœur de la transformation des activités bancaires à l'échelle mondiale. En Afrique subsaharienne, et particulièrement au Togo, la digitalisation rapide des services financiers (mobile money, banque en ligne) s'accompagne d'une recrudescence des fraudes bancaires, exposant les institutions à des pertes financières croissantes.

### 2. Problématique de l'étude

**2.1. Présentation du problème**

Malgré les avancées du Machine Learning, les institutions bancaires togolaises continuent d'utiliser des méthodes traditionnelles de détection de la fraude (règles statiques, contrôles manuels), exposées à des risques accrus de pertes financières. L'intégration de systèmes d'IA soulève par ailleurs des défis majeurs : sécurité des données, interprétabilité des modèles et conformité réglementaire.

**2.2. Formulation du problème (questions de l'étude)**

> **Question générale (QG) :** Comment concevoir et implémenter un système d'IA efficace et sécurisé pour la détection de la fraude bancaire au Togo, tout en garantissant une gestion avancée des utilisateurs et une conformité aux normes réglementaires ?

**Questions spécifiques :**

- **QS1** — Quels algorithmes de Machine Learning sont les plus adaptés à la détection de la fraude dans le contexte bancaire togolais ?
- **QS2** — Comment assurer la sécurité des données et la conformité réglementaire lors de l'intégration d'un système d'IA dans une banque togolaise ?
- **QS3** — Dans quelle mesure l'interprétabilité des modèles de ML facilite-t-elle leur adoption par les analystes financiers et les gestionnaires de risques ?

### 3. Hypothèses de l'étude

**3.1. Hypothèse générale (HG)**

L'intégration d'un système de Machine Learning permet d'améliorer la précision de la détection de la fraude bancaire au Togo en exploitant de vastes ensembles de données et en identifiant des schémas complexes inaccessibles aux méthodes traditionnelles.

**3.2. Hypothèses spécifiques**

- **HS1** — L'automatisation de la détection de la fraude à l'aide de modèles d'apprentissage automatique réduit le taux de faux négatifs en fournissant des prédictions plus fiables que les méthodes statistiques classiques.
- **HS2** — Une plateforme logicielle sécurisée, intégrant une gestion avancée des utilisateurs et des mécanismes de protection des données, favorise l'adoption du ML par les banques togolaises en assurant la conformité aux réglementations en vigueur.
- **HS3** — L'interprétabilité des modèles de ML et leur adaptation aux besoins spécifiques du secteur bancaire togolais facilitent leur acceptation par les analystes financiers et les gestionnaires de risques.

### 4. Objectifs de l'étude

**4.1. Objectif général (OG)**

Concevoir et proposer un système d'IA performant et sécurisé pour la détection de la fraude bancaire, appliqué au contexte togolais.

**4.2. Objectifs spécifiques**

- **OS1** — Identifier et comparer les algorithmes de ML les plus adaptés à la détection de la fraude dans le secteur bancaire togolais. _(→ répond à QS1)_
- **OS2** — Proposer une architecture logicielle sécurisée intégrant des mécanismes avancés de gestion des utilisateurs et de protection des données conformes aux réglementations togolaises et régionales. _(→ répond à QS2)_
- **OS3** — Évaluer l'interprétabilité des modèles développés et leur adéquation aux besoins des parties prenantes du secteur bancaire. _(→ répond à QS3)_

> ✅ Cohérence méthodologique respectée : 3 QS → 3 HS → 3 OS.

### 5. Justification de l'étude

**5.1. Sur le plan scientifique** Contribution à la recherche sur l'application du Machine Learning à la détection de fraude dans les systèmes bancaires africains, contexte encore peu documenté.

**5.2. Sur le plan pratique** Réponse à un besoin concret des banques togolaises face à la montée des fraudes financières numériques, et alignement avec les exigences de transparence des régulateurs (BCEAO/UEMOA).

### 6. Délimitation de l'étude

**6.1. Délimitation géographique** — Secteur bancaire au Togo (cas d'une banque togolaise à préciser, ou approche générique applicable au secteur), avec un focus sur Lomé.

**6.2. Délimitation thématique**

- Détection de la fraude par Machine Learning ; sécurité et conformité des systèmes ; interprétabilité des modèles (XAI).
- **Périmètre Mobile Money** : au Togo, le mobile money (TogoCom Cash, Moov Money, Flooz) constitue le canal financier de facto pour une large partie de la population. L'étude **inclut donc explicitement les transactions de mobile money** dans son périmètre d'analyse, en tant que catégorie de transactions à part entière, aux côtés des transactions bancaires classiques (cartes, virements). Les patterns de fraude propres à ce canal (SIM swap, fraude par USSD, ingénierie sociale sur agents mobile money) sont intégrés dans la typologie étudiée au Chapitre I et dans la grille d'entretien (Chapitre II/III).
- Sont exclus : la fraude fiscale, la cybercriminalité générale hors secteur financier, et le blanchiment d'argent en tant que tel (traité uniquement comme cadre réglementaire connexe).

**6.3. Délimitation temporelle** — Période d'analyse 2019–2025, correspondant à la phase de digitalisation bancaire et de croissance du mobile money accélérée.

### 7. Plan du mémoire

Ce mémoire est structuré en quatre chapitres : (I) Cadre théorique et conceptuel, (II) Méthodologie de l'étude, (III) Présentation du système et des données, (IV) Analyse, diagnostic et proposition d'intervention.

---

## CHAPITRE I — CADRE THÉORIQUE ET CONCEPTUEL

**Introduction du chapitre**

### 1.1. Cadre théorique et état de l'art (revue de littérature)

- Généralités sur le Machine Learning et ses applications bancaires
- Revue empirique et théorique sur la détection de la fraude bancaire (approches classiques vs approches IA)
- Crédit bancaire et gestion du risque : définitions et enjeux
- Panorama des techniques actuelles : _Ensemble Learning_ (Random Forest, XGBoost), détection d'anomalies (Isolation Forest), Deep Learning séquentiel (LSTM)
- L'explicabilité (XAI) comme enjeu central des systèmes d'IA bancaires en 2025-2026

### 1.2. Historique

- Évolution des systèmes de détection de fraude bancaire : des règles métier aux modèles statistiques, puis au Machine Learning
- Adoption du ML dans le secteur financier africain : état des lieux et retards structurels

**Tableau 1.1 — Synthèse comparative des études antérieures en Afrique de l'Ouest**

| Pays | Auteur(s) / Année | Secteur étudié | Méthode IA utilisée | Principal constat |
|---|---|---|---|---|
| Côte d'Ivoire | _À compléter_ | Banque / Mobile money | _À compléter_ | _À compléter_ |
| Sénégal | _À compléter_ | Banque | _À compléter_ | _À compléter_ |
| Bénin | _À compléter_ | Mobile money | _À compléter_ | _À compléter_ |
| Nigeria | _À compléter_ | Banque | _À compléter_ | _À compléter_ |
| **Togo** | — | — | — | **Aucune étude identifiée à ce jour → originalité de la présente recherche** |

_Ce tableau sera complété au fil de la revue de littérature et permettra de positionner clairement la contribution originale du présent mémoire : à notre connaissance, aucune étude n'a encore porté spécifiquement sur la détection de fraude bancaire et mobile money par IA dans le contexte togolais._

### 1.3. Cadre légal et réglementaire

- Réglementations bancaires en vigueur au Togo (BCEAO, UEMOA)
- Dispositifs AML/KYC et rôle du GIABA
- Normes de sécurité des données applicables (loi togolaise sur la protection des données personnelles)
- Exigences réglementaires en matière de transparence des décisions automatisées (explicabilité)

**Conclusion du chapitre**

---

## CHAPITRE II — MÉTHODOLOGIE DE L'ÉTUDE

**Introduction du chapitre**

### 2.1. Nature de l'étude

Étude prospective, à approche mixte (qualitative et quantitative), non expérimentale à visée explicative (niveau Compréhensif — objectif : _Proposer_, selon FUNIBER, 2017).

### 2.2. Variables de l'étude

- **Définition conceptuelle des variables** : algorithmes ML (variable indépendante), sécurité et conformité des données (variable modératrice), interprétabilité des modèles (variable de résultat), taux de détection de fraude / précision (variable dépendante)
- **Limites et difficultés rencontrées** : indisponibilité de données bancaires togolaises réelles, fort déséquilibre des classes (< 1% de transactions frauduleuses)
- **Utilisation des variables et indicateurs associés** : F1-Score, Recall, AUC-PR, score d'explicabilité SHAP

### 2.3. Population et échantillon

Présentation de la banque ou du secteur bancaire togolais retenu comme cas d'étude, des données financières mobilisées (dataset public de référence) et du périmètre de l'échantillon.

### 2.4. Approche méthodologique retenue : Ensemble Learning + XAI

> 💡 Approche choisie : **"Ensemble Learning supervisé + détection d'anomalies non supervisée + explicabilité (XAI)"**, validée sur un jeu de données de référence international, puis contextualisée au Togo via une analyse qualitative (entretiens).

**2.4.1. Choix du dataset et limite assumée**

Aucune donnée bancaire togolaise réelle n'étant accessible (confidentialité), l'étude s'appuie sur un **dataset public de référence reconnu** :

- **IEEE-CIS Fraud Detection** (Kaggle) — ~590 000 transactions, dataset réaliste et largement utilisé dans la littérature récente
- _Alternative_ : Credit Card Fraud Dataset (ULB/Kaggle) — ~284 807 transactions, plus simple à manipuler

> ⚠️ **Limite assumée** : ce dataset étant constitué de transactions américaines/européennes, il ne capture pas nativement les spécificités togolaises (mobile money, fraude par USSD, SIM swap, faible bancarisation). Cette limite est explicitement reconnue et traitée selon deux axes :
>
> 1. **Validation qualitative** — les entretiens menés auprès des responsables bancaires togolais (cf. 2.4.4) serviront à **valider ou invalider la pertinence des variables et des seuils** issus du modèle entraîné sur IEEE-CIS, et à identifier les écarts avec la réalité du terrain togolais.
> 2. **Perspective de recherche** — l'utilisation d'un **jeu de données togolais réel**, obtenu via un partenariat avec une banque ou un opérateur de mobile money, est proposée comme perspective directe de prolongement de ce travail (cf. Conclusion générale).

**2.4.2. Architecture des modèles (approche à 3 niveaux)**

| Niveau | Modèle | Rôle |
|---|---|---|
| Niveau 1 — Détection rapide | **Isolation Forest** (non supervisé) | Filtre les anomalies évidentes |
| Niveau 2 — Classification fine | **XGBoost** (supervisé) | Classification précise fraude / non-fraude — standard actuel de l'industrie |
| Niveau 3 — Validation séquentielle _(optionnel)_ | **LSTM** | Capture des patterns temporels (séquences de transactions suspectes) |

**2.4.3. Explicabilité (XAI)**

Outil retenu : **SHAP (SHapley Additive exPlanations)**, permettant d'expliquer chaque décision du modèle (ex. : facteurs ayant déclenché une alerte) — répond directement à HS3 et aux exigences de transparence de la BCEAO/UEMOA.

**2.4.4. Volet qualitatif : entretiens semi-directifs**

- **Échantillon cible** : 5 à 8 responsables d'institutions bancaires et de mobile money basées à Lomé.
- **Profils visés** :
  - Responsables DSI / IT (vision technique et infrastructure)
  - Responsables Conformité / KYC-AML (vision réglementaire)
  - Gestionnaires de risques / analystes fraude (vision opérationnelle)
- **Méthode d'analyse** : codage thématique (identification de thèmes récurrents : typologies de fraude, freins à l'adoption de l'IA, attentes en matière d'explicabilité, contraintes infrastructurelles).
- **Intégration aux chapitres suivants** :
  - **Chapitre III** — les résultats des entretiens alimentent la section "Présentation des données collectées" (état des lieux de la fraude perçue par les praticiens) et permettent de discuter la transférabilité des variables du modèle IEEE-CIS au contexte togolais.
  - **Chapitre IV** — les résultats du codage thématique nourrissent directement le diagnostic (4.1) et la vérification des hypothèses HS2 et HS3 (acceptabilité, conformité, interprétabilité perçue).

**2.4.5. Métriques d'évaluation**

L'« Accuracy » seule n'étant pas pertinente sur données déséquilibrées, les métriques retenues sont :

- **F1-Score** (équilibre précision/rappel)
- **AUC-PR** (Precision-Recall, plus pertinent qu'AUC-ROC sur classes déséquilibrées)
- **Recall** (taux de fraudes détectées, lié au taux de faux négatifs — HS1)

### 2.5. Outils de l'étude

- Algorithmes : Random Forest, XGBoost, Isolation Forest, (LSTM en option)
- Outils de collecte et de traitement : Python (Scikit-learn, XGBoost, TensorFlow/Keras, Pandas, NumPy)
- Technique de rééquilibrage : SMOTE
- Outil d'explicabilité : SHAP
- Environnement de développement et de tests : Jupyter Notebook / Google Colab

**Conclusion du chapitre**

---

## CHAPITRE III — PRÉSENTATION DU SYSTÈME ET DES DONNÉES

**Introduction du chapitre**

> ⚠️ **Cadrage important** : la "plateforme logicielle" présentée dans ce chapitre correspond à une **preuve de concept (PoC)** et/ou à des **spécifications techniques détaillées accompagnées de mockups/maquettes d'interface**, et non à un logiciel complet, sécurisé et déployé en production. L'objectif est de démontrer la faisabilité technique et de proposer une architecture cible, pas de livrer un produit fini.

### 3.1. Présentation du site de l'étude (secteur/banque togolaise retenue)

- Panorama du système bancaire togolais et niveau de digitalisation
- Présentation de la banque cas d'étude (ou du secteur, si approche générique)

### 3.2. Collecte et préparation des données

- Sélection des données financières pertinentes (dataset IEEE-CIS / Credit Card Fraud)
- Analyse exploratoire (EDA) : distribution fraude/non-fraude, corrélations entre variables
- Nettoyage et prétraitement : encodage des variables catégorielles, normalisation (StandardScaler), rééquilibrage via SMOTE
- Split Train/Test (80/20, stratifié)
- _Discussion_ : correspondance/écarts entre les variables disponibles dans IEEE-CIS et les variables pertinentes pour le mobile money togolais (ex. : fréquence des recharges, montants typiques, canaux USSD)

### 3.3. Conception du modèle de Machine Learning

- Choix et architecture des algorithmes (Isolation Forest, Random Forest, XGBoost)
- Entraînement, validation croisée et tests de robustesse
- Application de SHAP sur le modèle le plus performant : identification des variables les plus influentes, exemples d'explications individuelles

### 3.4. Proposition de plateforme (PoC / Spécifications & Maquettes)

- Schéma d'architecture technique cible (sécurisée, API REST)
- Spécifications de la gestion avancée des utilisateurs (rôles : analyste, gestionnaire de risques, administrateur)
- Mockups d'interface (maquettes) du tableau de bord d'alertes et des explications SHAP
- Principes de sécurité retenus (chiffrement, conformité KYC/AML) — décrits au niveau spécifications, sans implémentation complète

### 3.5. Tests et validation

- Évaluation comparative des performances (Matrice de confusion, F1, Recall, AUC-PR pour chaque modèle)
- Simulations appliquées au cas togolais : discussion sur la disponibilité des variables et les contraintes (volume de données, infrastructure)

**Conclusion du chapitre**

---

## CHAPITRE IV — ANALYSE, DIAGNOSTIC ET PROPOSITION D'INTERVENTION

**Introduction du chapitre**

### 4.1. Présentation et analyse de la situation

- Vérification de la pertinence des prédictions du modèle retenu
- Identification des limites et ajustement du modèle
- Vérification des hypothèses (HG, HS1, HS2, HS3) à la lumière des résultats

### 4.2. Intervention proposée et justification

Lien entre les résultats du diagnostic et la solution proposée : conception d'un système d'IA de détection de fraude (Ensemble Learning + XAI), accompagné d'une plateforme sécurisée de gestion des utilisateurs.

### 4.3. Objectifs de l'intervention

- **Objectif général d'intervention** : déployer un système d'IA opérationnel, sécurisé et explicable pour la détection de la fraude bancaire au Togo
- **Objectifs spécifiques d'intervention** :
  - Développer et entraîner les modèles retenus sur des données représentatives
  - Intégrer une plateforme sécurisée avec gestion avancée des utilisateurs
  - Mettre en place un module d'explicabilité (SHAP) pour les analystes

### 4.4. Composantes de l'intervention envisagée

- Implémentation technique du système (modules de collecte, prétraitement, détection, alerte, explicabilité)
- Sécurité et gestion avancée des utilisateurs (authentification, rôles, chiffrement)
- Formation et conduite du changement auprès des agents bancaires

### 4.5. Stratégies d'action, contenu et périmètre

- Plan de déploiement progressif (phase pilote, généralisation)
- Intégration aux processus bancaires existants (API, interopérabilité avec les SI)

### 4.6. Faisabilité

- **Économique** — coûts de développement vs pertes évitées
- **Sociale** — acceptabilité par les agents bancaires, formation
- **Technique** — infrastructure requise, interopérabilité
- **Environnementale / Réglementaire** — conformité BCEAO/UEMOA, sobriété numérique

**Conclusion du chapitre**

---

## CONCLUSION GÉNÉRALE

Synthèse des résultats, vérification des hypothèses (HG, HS1, HS2, HS3), contributions scientifiques et pratiques, limites de l'étude (notamment l'utilisation d'un dataset international comme proxy, cf. 2.4.1), perspectives d'amélioration et recommandations pour une implémentation à plus grande échelle au Togo.

**Perspectives prioritaires :**

- **Partenariat avec une banque ou un opérateur de mobile money togolais** pour obtenir un jeu de données réel et ré-entraîner/valider le modèle sur des données locales authentiques.
- Extension du périmètre à l'ensemble de l'espace UEMOA.
- Exploration de l'IA fédérée pour permettre un partage inter-bancaire des modèles sans divulgation de données sensibles.
- Passage du PoC vers un prototype déployable en environnement de test (sandbox).

---

## RÉFÉRENCES BIBLIOGRAPHIQUES

_(Norme APA)_

---

## ANNEXES

- Grille d'entretien semi-directif (responsables IT / conformité)
- Questionnaire (agents bancaires)
- Code Python (prétraitement, SMOTE, entraînement des modèles, SHAP)
- Schéma d'architecture détaillée du système proposé

---

---

# CONCEPTION D'UN SYSTÈME D'INTELLIGENCE ARTIFICIELLE EN TEMPS RÉEL POUR LA DÉTECTION DE LA FRAUDE BANCAIRE : CAS DU TOGO

**Mémoire de fin d'études — Master** Conforme au Guide de Rédaction Scientifique — Collège de Paris Supérieur (Version 1.3)

---

## INTRODUCTION GÉNÉRALE

### 1. Contexte général de l'étude

L'intelligence artificielle est aujourd'hui au cœur de la transformation des activités bancaires à l'échelle mondiale. En Afrique subsaharienne, et particulièrement au Togo, la digitalisation rapide des services financiers — mobile money, banque en ligne — s'accompagne d'une recrudescence des fraudes bancaires, exposant les institutions à des pertes financières croissantes. Les méthodes traditionnelles de détection (règles statiques, contrôles manuels) montrent leurs limites face à des schémas de fraude de plus en plus complexes et évolutifs. Le Machine Learning offre une alternative plus performante, mais son intégration dans le secteur bancaire togolais soulève des défis majeurs : sécurité des données, interprétabilité des modèles et conformité réglementaire.

Points abordés :

- L'évolution du secteur bancaire au Togo et en Afrique subsaharienne
- La transformation digitale et l'émergence des services bancaires numériques (mobile money, banque en ligne)
- La recrudescence des fraudes bancaires et son impact sur les institutions togolaises
- L'importance de l'IA dans la sécurisation des transactions financières

---

### 2. Problématique de l'étude

#### 2.1. Présentation du problème

Malgré les avancées du Machine Learning, les institutions bancaires togolaises continuent d'utiliser des méthodes traditionnelles de détection de la fraude (règles statiques, contrôles manuels), exposées à des risques accrus de pertes financières. L'intégration de systèmes d'IA soulève par ailleurs des défis majeurs : sécurité des données, interprétabilité des modèles et conformité réglementaire.

Au Togo, le mobile money (TogoCom Cash, Moov Money, Flooz) constitue le canal financier de facto pour une large partie de la population. Ce canal génère des patterns de fraude spécifiques — SIM swap, fraude par USSD, ingénierie sociale sur agents mobile money — que les systèmes de détection classiques ne couvrent pas de manière adéquate.

#### 2.2. Formulation du problème (questions de l'étude)

**Question générale (QG) :**

> Comment concevoir un système d'IA efficace pour détecter en temps réel les fraudes bancaires dans le contexte spécifique du Togo, en couvrant à la fois les transactions bancaires classiques et les transactions mobile money ?

**Questions spécifiques :**

- **QS1** — Quels sont les types de fraudes bancaires les plus fréquents au Togo (y compris sur le mobile money) et quelles sont leurs caractéristiques spécifiques ?
- **QS2** — Quelles sont les limites des systèmes actuels de détection de fraude dans les banques togolaises, et comment les données contextuelles locales peuvent-elles améliorer la précision de détection ?
- **QS3** — Quels algorithmes d'IA sont les plus adaptés pour la détection en temps réel, et comment garantir leur interprétabilité afin de favoriser leur adoption par les gestionnaires bancaires togolais ?

---

### 3. Hypothèses de l'étude

#### 3.1. Hypothèse générale (HG)

Un système d'IA basé sur l'apprentissage automatique et l'analyse comportementale peut détecter efficacement les fraudes bancaires en temps réel au Togo, en s'adaptant aux spécificités locales des transactions, incluant les transactions mobile money (TogoCom Cash, Moov Money, Flooz).

#### 3.2. Hypothèses spécifiques

- **HS1** — Les modèles d'apprentissage automatique (Isolation Forest, XGBoost) peuvent identifier des patterns de fraude spécifiques au contexte togolais, notamment les fraudes liées au mobile money (SIM swap, fraude USSD, ingénierie sociale sur agents mobile money).
- **HS2** — L'intégration de données contextuelles locales (transactions mobile money, comportements utilisateurs togolais, canaux USSD) améliore significativement la précision de détection par rapport aux modèles entraînés sur des données génériques.
- **HS3** — Un système hybride combinant plusieurs algorithmes (Ensemble Learning) et intégrant des outils d'explicabilité (SHAP/XAI) réduit les faux positifs et favorise l'adoption du système par les analystes financiers et gestionnaires de risques bancaires togolais.

> ✅ **Cohérence méthodologique respectée : 3 QS → 3 HS → 3 OS**

---

### 4. Objectifs de l'étude

#### 4.1. Objectif général (OG)

Concevoir et proposer un système d'IA performant pour la détection en temps réel des fraudes bancaires, adapté au contexte togolais et couvrant les transactions bancaires classiques ainsi que les transactions mobile money.

#### 4.2. Objectifs spécifiques

- **OS1** — Analyser les types et patterns de fraudes bancaires au Togo, y compris les fraudes spécifiques au mobile money (TogoCom Cash, Moov Money, Flooz), et établir une synthèse comparative des études antérieures en Afrique de l'Ouest. _(→ répond à QS1 / HS1)_
- **OS2** — Évaluer les systèmes de détection existants dans les banques togolaises, identifier précisément leurs limites, et démontrer l'apport des données contextuelles locales dans l'amélioration de la précision de détection. _(→ répond à QS2 / HS2)_
- **OS3** — Développer un modèle d'IA hybride (Ensemble Learning à 3 niveaux) adapté aux spécificités locales, en intégrant des outils d'explicabilité (XAI/SHAP) pour faciliter son adoption par les praticiens bancaires togolais. _(→ répond à QS3 / HS3)_

---

### 5. Justification de l'étude

#### 5.1. Justification scientifique

- Contribution à la recherche sur l'application du Machine Learning à la détection de fraude dans les systèmes bancaires d'Afrique francophone — contexte encore peu documenté.
- À notre connaissance, aucune étude n'a encore porté spécifiquement sur la détection de fraude bancaire et mobile money par IA dans le contexte togolais. Ce travail constitue ainsi une contribution originale à la littérature sur l'IA appliquée aux économies émergentes d'Afrique de l'Ouest.
- Développement de modèles adaptés aux spécificités des marchés financiers africains (faible bancarisation, prédominance du mobile money, contraintes infrastructurelles).

#### 5.2. Justification pratique

- Réduction des pertes financières pour les banques et institutions de mobile money togolaises.
- Protection des clients et renforcement de la confiance dans les services financiers numériques.
- Alignement avec les exigences de transparence et de conformité des régulateurs régionaux (BCEAO/UEMOA).
- Contribution à l'inclusion financière et à la digitalisation sécurisée au Togo.

---

### 6. Délimitation de l'étude

#### 6.1. Délimitation géographique

- Focus sur le système bancaire togolais, avec un focus sur Lomé comme principal centre financier.
- Étude impliquant 3 à 5 banques principales (BTCI, Orabank Togo, UTB, Ecobank…) et les principaux opérateurs de mobile money (TogoCom Cash, Moov Money/Flooz).

#### 6.2. Délimitation thématique

- Fraudes sur les transactions électroniques bancaires et mobile money.
- **Patterns inclus dans le périmètre :** fraude par carte bancaire, virement frauduleux, SIM swap, fraude par USSD, ingénierie sociale sur agents mobile money.
- **Exclus du périmètre :** fraude fiscale, cybercriminalité générale hors secteur financier, blanchiment d'argent _(traité uniquement comme cadre réglementaire connexe)_.

#### 6.3. Délimitation temporelle

- Période d'analyse : **2020–2024**, correspondant à la phase de digitalisation bancaire accélérée et de croissance du mobile money au Togo.

---

### 7. Plan du mémoire

Ce mémoire est structuré en quatre chapitres :

1. **Chapitre I** — Cadre théorique et conceptuel
2. **Chapitre II** — Méthodologie de l'étude
3. **Chapitre III** — Présentation de la situation et collecte des données
4. **Chapitre IV** — Analyse-diagnostic et proposition d'intervention

---

## CHAPITRE I : CADRE THÉORIQUE ET CONCEPTUEL

**Introduction du chapitre**

### 1.1. Cadre théorique et état de l'art

#### 1.1.1. La fraude bancaire : concepts et typologie

- Définition et classification des fraudes bancaires
- Fraude par carte bancaire et virement frauduleux
- Fraude en ligne et mobile banking
- **Fraudes spécifiques au mobile money en Afrique de l'Ouest :** SIM swap, fraude par USSD, ingénierie sociale sur agents mobile money
- Usurpation d'identité et fraude documentaire

#### 1.1.2. L'Intelligence Artificielle et l'apprentissage automatique

- Concepts fondamentaux du Machine Learning et du Deep Learning
- Algorithmes de classification supervisée : Random Forest, XGBoost
- Détection d'anomalies non supervisée : Isolation Forest, Autoencoders
- Analyse séquentielle : Réseaux de neurones récurrents (LSTM)
- Ensemble learning : principe, avantages et état de l'art
- **L'explicabilité (XAI) — SHAP et LIME — comme enjeu central des systèmes d'IA bancaires en 2025-2026**

#### 1.1.3. Revue de littérature sur la détection de fraude par IA

- Approches traditionnelles (règles métier, statistiques classiques) et leurs limites
- Méthodes basées sur l'IA : panorama des travaux récents (2019–2024)
- Études de cas internationaux (Europe, Amérique du Nord)
- Spécificités africaines et état des travaux en Afrique de l'Ouest

**Tableau 1.1 — Synthèse comparative des études antérieures en Afrique de l'Ouest**

| Pays | Auteur(s) / Année | Secteur étudié | Méthode IA utilisée | Principal constat |
|---|---|---|---|---|
| Côte d'Ivoire | _À compléter_ | Banque / Mobile money | _À compléter_ | _À compléter_ |
| Sénégal | _À compléter_ | Banque | _À compléter_ | _À compléter_ |
| Bénin | _À compléter_ | Mobile money | _À compléter_ | _À compléter_ |
| Nigeria | _À compléter_ | Banque | _À compléter_ | _À compléter_ |
| **Togo** | — | — | — | **Aucune étude identifiée à ce jour → originalité de la présente recherche** |

> _Ce tableau sera complété au fil de la revue de littérature. Il permettra de positionner clairement la contribution originale du présent mémoire : à notre connaissance, aucune étude n'a encore porté spécifiquement sur la détection de fraude bancaire et mobile money par IA dans le contexte togolais._

---

### 1.2. Historique de la fraude bancaire au Togo

- Évolution des types de fraude au Togo : des fraudes traditionnelles aux fraudes numériques
- Statistiques et tendances (montants, fréquences, secteurs touchés — 2020-2024)
- Adoption du mobile money au Togo et émergence de nouveaux risques (TogoCom Cash, Moov Money, Flooz)
- Réponses institutionnelles des banques togolaises face à la fraude : dispositifs existants et résultats

---

### 1.3. Cadre légal et réglementaire

- Réglementation bancaire BCEAO et directives UEMOA
- Lois togolaises sur la cybercriminalité et la protection des données personnelles
- Dispositifs AML/KYC et rôle du GIABA dans la lutte contre la fraude en Afrique de l'Ouest
- Standards internationaux : PCI DSS
- **Exigences réglementaires en matière de transparence des décisions automatisées (explicabilité des modèles d'IA)**

---

**Conclusion du chapitre**

---

## CHAPITRE II : MÉTHODOLOGIE DE L'ÉTUDE

**Introduction du chapitre**

### 2.1. Nature de l'étude

- Étude **prospective**, à approche **mixte** (qualitative et quantitative)
- Recherche appliquée à visée **explicative** (niveau Compréhensif — objectif : _Proposer_, selon FUNIBER, 2017)
- Non expérimentale

---

### 2.2. Variables de l'étude

#### 2.2.1. Définition conceptuelle des variables

**Variables indépendantes :**

- Types de transactions (bancaires classiques et mobile money)
- Comportements utilisateurs (fréquence, montants, canaux utilisés)
- Données contextuelles locales (transactions USSD, canaux mobile money togolais)

**Variables dépendantes :**

- Taux de détection de fraude (F1-Score, Recall, AUC-PR)
- Taux de faux positifs
- Temps de traitement (latence de détection)

**Variable modératrice :**

- Interprétabilité des modèles (score d'importance des variables SHAP)

#### 2.2.2. Limites et difficultés rencontrées

- Indisponibilité de données bancaires togolaises réelles (confidentialité) → recours à un dataset public de référence international
- Fort déséquilibre des classes (moins de 1 % de transactions frauduleuses) → traitement par SMOTE
- Ressources techniques et infrastructure locale limitée
- Accès restreint aux statistiques sectorielles sur la fraude au Togo

#### 2.2.3. Opérationnalisation des variables et indicateurs

**Indicateurs pour "Types de transactions" :**

- Montant de la transaction
- Fréquence des transactions
- Localisation géographique
- Canal utilisé (USSD, carte, virement, application mobile)
- Heure et jour de la transaction

**Indicateurs pour "Taux de détection" :**

- **F1-Score** (équilibre précision/rappel — pertinent sur données déséquilibrées)
- **AUC-PR** (Precision-Recall Curve — plus pertinent qu'AUC-ROC sur classes déséquilibrées)
- **Recall** (taux de fraudes effectivement détectées — lié au taux de faux négatifs, répondant à HS1)
- Temps moyen de détection (cible : < 100 ms)

> ⚠️ _L'Accuracy seule n'est pas pertinente sur des données fortement déséquilibrées (< 1 % de fraudes). Les métriques retenues (F1, AUC-PR, Recall) sont les standards de l'industrie pour ce type de problème._

**Indicateurs pour "Interprétabilité" :**

- Score d'importance des variables SHAP (identification des facteurs déclenchants d'une alerte)
- Lisibilité et compréhensibilité des explications individuelles par les praticiens bancaires

---

### 2.3. Population et échantillon

#### Section 2 : Échantillonnage et collecte de données

**Population cible :**

- Toutes les transactions bancaires et mobile money au Togo (2020–2024)

**Échantillon quantitatif — Dataset public de référence :**

Aucune donnée bancaire togolaise réelle n'étant accessible (confidentialité bancaire), l'étude s'appuie sur un **dataset public de référence reconnu** :

- **Dataset principal : IEEE-CIS Fraud Detection** (Kaggle) — ~590 000 transactions, taux de fraude de 3,5 %, dataset réaliste et largement utilisé dans la littérature récente
- **Dataset alternatif :** Credit Card Fraud Dataset (ULB/Kaggle) — ~284 807 transactions, plus simple à manipuler

> ⚠️ **Limite assumée :** Ce dataset étant constitué de transactions américaines/européennes, il ne capture pas nativement les spécificités togolaises (mobile money, fraude par USSD, SIM swap, faible bancarisation). Cette limite est explicitement reconnue et traitée selon deux axes :
>
> 1. **Validation qualitative** — les entretiens menés auprès des responsables bancaires togolais (cf. 2.4) serviront à valider ou invalider la pertinence des variables et des seuils issus du modèle entraîné sur IEEE-CIS.
> 2. **Perspective de prolongement** — l'utilisation d'un jeu de données togolais réel, obtenu via un partenariat avec une banque ou un opérateur de mobile money, est proposée comme perspective directe (cf. Conclusion générale).

**Échantillon qualitatif :**

- 5 à 8 responsables d'institutions bancaires et d'opérateurs de mobile money basées à Lomé
- **Profils visés :**
  - Responsables DSI / IT (vision technique et infrastructure)
  - Responsables Conformité / KYC-AML (vision réglementaire)
  - Gestionnaires de risques / analystes fraude (vision opérationnelle)
- Technique d'échantillonnage : raisonnée (choix délibéré selon profil et disponibilité)

---

### 2.4. Outils de l'étude

#### 2.4.1. Outils de collecte

- Entretiens semi-directifs avec responsables bancaires et opérateurs mobile money _(grille d'entretien en Annexe A)_
- Analyse documentaire (rapports BCEAO, GIABA, statistiques sectorielles)
- Datasets de transactions anonymisées (IEEE-CIS / ULB)

#### 2.4.2. Approche algorithmique : Ensemble Learning à 3 niveaux + XAI

**Architecture retenue :**

| Niveau | Modèle | Type | Rôle |
|---|---|---|---|
| **Niveau 1 — Détection rapide** | Isolation Forest | Non supervisé | Filtre les anomalies évidentes parmi les transactions |
| **Niveau 2 — Classification fine** | XGBoost | Supervisé | Classification précise fraude / non-fraude — standard actuel de l'industrie |
| **Niveau 3 — Validation séquentielle** _(optionnel)_ | LSTM | Deep Learning | Capture des patterns temporels (séquences de transactions suspectes) |

**Explicabilité (XAI) :**

- Outil retenu : **SHAP (SHapley Additive exPlanations)**
- Permet d'expliquer chaque décision du modèle (facteurs ayant déclenché une alerte)
- Répond directement à HS3 et aux exigences de transparence de la BCEAO/UEMOA

#### 2.4.3. Outils d'analyse et de développement

- **Algorithmes :** Isolation Forest, Random Forest, XGBoost, LSTM
- **Langage :** Python
- **Bibliothèques :** Scikit-learn, XGBoost, TensorFlow/Keras, Pandas, NumPy
- **Technique de rééquilibrage :** SMOTE _(Synthetic Minority Oversampling Technique)_
- **Outil d'explicabilité :** SHAP
- **Environnement de développement :** Jupyter Notebook / Google Colab

#### 2.4.4. Méthode d'analyse qualitative

- Codage thématique des entretiens (identification de thèmes récurrents)
- Thèmes principaux : typologies de fraude locales, freins à l'adoption de l'IA, attentes en matière d'explicabilité, contraintes infrastructurelles
- **Intégration aux chapitres suivants :**
  - Chapitre III : validation de la transférabilité des variables du dataset IEEE-CIS au contexte togolais
  - Chapitre IV : nourrissent le diagnostic (4.1) et la vérification de HS2 et HS3

---

**Conclusion du chapitre**

---

## CHAPITRE III : PRÉSENTATION DE LA SITUATION ET COLLECTE DES DONNÉES

**Introduction du chapitre**

> ⚠️ **Cadrage important :** La "plateforme logicielle" présentée dans ce chapitre correspond à une **preuve de concept (PoC)** et/ou à des **spécifications techniques détaillées accompagnées de mockups/maquettes d'interface**, et non à un logiciel complet déployé en production. L'objectif est de démontrer la faisabilité technique et de proposer une architecture cible.

---

### 3.1. Le secteur bancaire togolais

#### 3.1.1. Structure et acteurs

- Principales banques commerciales présentes au Togo : BTCI, Orabank Togo, UTB, Ecobank, SGBT…
- Institutions de microfinance
- Opérateurs de mobile money : **TogoCom Cash, Moov Money (Flooz)**
- Niveau de bancarisation et prépondérance du mobile money comme canal financier principal

#### 3.1.2. Infrastructure technologique

- Systèmes informatiques existants dans les banques togolaises
- Niveau de digitalisation et maturité des SI bancaires
- Défis techniques : infrastructure réseau, interopérabilité entre systèmes, contraintes de connectivité

---

### 3.2. État des lieux de la fraude bancaire au Togo

#### 3.2.1. Typologie des fraudes observées

- Statistiques par type de fraude (cartes, virements, mobile money)
- Évolution temporelle 2020–2024
- Fraudes spécifiques au mobile money togolais : SIM swap, fraude USSD, ingénierie sociale sur agents
- Comparaison régionale avec les pays UEMOA voisins

#### 3.2.2. Impact économique

- Pertes financières estimées pour les banques et les clients
- Coûts des dispositifs de prévention actuels
- Impact sur la confiance dans les services financiers numériques et sur l'inclusion financière

---

### 3.3. Présentation et analyse exploratoire des données

#### 3.3.1. Description du dataset retenu (IEEE-CIS Fraud Detection)

- Volume et structure : ~590 000 transactions, ~400 variables
- Distribution fraude / non-fraude : ~3,5 % de transactions frauduleuses → déséquilibre prononcé
- Variables disponibles : montant, canal, temporalité, identifiants anonymisés…

#### 3.3.2. Prétraitement des données

- Nettoyage : traitement des valeurs manquantes, suppression des doublons
- Encodage des variables catégorielles
- Normalisation (StandardScaler)
- Rééquilibrage des classes via **SMOTE**
- Split Train/Test stratifié : 80 % entraînement / 20 % test

#### 3.3.3. Discussion sur la transférabilité au contexte togolais

- Correspondance et écarts entre les variables du dataset IEEE-CIS et les réalités togolaises (mobile money, transactions USSD, montants typiques au Togo)
- Résultats des entretiens qualitatifs : validation ou ajustement des variables et seuils pertinents pour le Togo
- Identification des variables manquantes spécifiques au contexte local (canal USSD, type d'agent mobile money, etc.)

---

### 3.4. Systèmes de détection actuels dans les banques togolaises

#### 3.4.1. Méthodes utilisées

- Règles statiques et surveillance manuelle
- Outils existants et niveau de maturité des systèmes de détection

#### 3.4.2. Performance et limites identifiées

- Taux de détection actuels
- Problèmes identifiés : rigidité des règles, délais de détection, volume d'alertes non traitées
- Lacunes spécifiques sur le canal mobile money (TogoCom Cash, Moov Money/Flooz)
- Besoins non couverts identifiés lors des entretiens avec les responsables bancaires

---

**Conclusion du chapitre**

---

## CHAPITRE IV : ANALYSE-DIAGNOSTIC ET PROPOSITION D'INTERVENTION

**Introduction du chapitre**

---

### 4.1. Analyse diagnostique

#### 4.1.1. Forces et faiblesses du système actuel

**Analyse SWOT des dispositifs de détection de fraude existants au Togo :**

|  | Forces | Faiblesses |
|---|---|---|
| **Interne** | Connaissance des clients, réseaux d'agents mobile money | Règles statiques, manque d'adaptabilité, faible couverture mobile money |
| **Externe** | Cadre réglementaire BCEAO/UEMOA, croissance du mobile money | Sophistication croissante des fraudes, SIM swap, ingénierie sociale |

- Gaps identifiés et opportunités d'amélioration
- Analyse comparative avec les systèmes déployés dans les pays UEMOA voisins

#### 4.1.2. Besoins spécifiques au contexte togolais

- Patterns de fraude locaux propres au mobile money (SIM swap, fraude USSD)
- Contraintes techniques et infrastructurelles des banques togolaises
- Facteurs comportementaux des utilisateurs togolais (fréquence, montants, canaux)

#### 4.1.3. Vérification des hypothèses

- **HG :** Confirmation ou infirmation de l'efficacité du système d'IA proposé pour le contexte togolais
- **HS1 :** Le modèle Isolation Forest + XGBoost identifie-t-il des patterns de fraude pertinents pour le contexte togolais ?
- **HS2 :** L'intégration des données contextuelles locales améliore-t-elle significativement la précision ?
- **HS3 :** Les explications SHAP favorisent-elles effectivement l'adoption par les gestionnaires bancaires ?

---

### 4.2. Intervention proposée et justification

Conception d'un système d'IA hybride (**Ensemble Learning à 3 niveaux + XAI/SHAP**) pour la détection en temps réel de la fraude bancaire et mobile money au Togo.

- Lien explicite entre les résultats du diagnostic (4.1) et les choix techniques proposés
- Justification du choix de l'Ensemble Learning vs approche mono-algorithme
- Justification de l'intégration de l'explicabilité SHAP pour répondre aux exigences réglementaires et opérationnelles

---

### 4.3. Objectifs de l'intervention

#### 4.3.1. Objectif général d'intervention

Déployer un système d'IA opérationnel, sécurisé et explicable pour la détection de la fraude bancaire et mobile money au Togo _(cible : ≥ 92 % de détection, ≤ 1 % de faux positifs, temps de réponse < 100 ms)_.

#### 4.3.2. Objectifs spécifiques d'intervention

- Développer et entraîner les modèles retenus (Isolation Forest, XGBoost, LSTM) sur des données représentatives
- Intégrer un module d'explicabilité SHAP accessible aux analystes et gestionnaires de risques
- Proposer une architecture logicielle sécurisée avec gestion avancée des utilisateurs (PoC + Spécifications + Mockups)
- Former le personnel bancaire à l'utilisation et à l'interprétation du système

---

### 4.4. Composantes de l'intervention envisagée

#### 4.4.1. Module de collecte et prétraitement

- APIs de capture de données (transactions bancaires classiques et mobile money)
- Normalisation, nettoyage, feature engineering adapté au contexte togolais
- Gestion du déséquilibre des classes en production (seuils adaptatifs)

#### 4.4.2. Module d'analyse en temps réel (Architecture 3 niveaux)

| Niveau | Modèle | Rôle | Cible de performance |
|---|---|---|---|
| **Niveau 1** | Isolation Forest _(non supervisé)_ | Filtre les anomalies évidentes | Réduction du volume à analyser |
| **Niveau 2** | XGBoost _(supervisé)_ | Classification précise fraude / non-fraude | F1-Score ≥ 0.85, Recall ≥ 0.92 |
| **Niveau 3** | LSTM _(optionnel)_ | Capture des patterns temporels séquentiels | Amélioration sur séquences suspectes |

- Moteur de scoring en temps réel (cible : < 100 ms par transaction)

#### 4.4.3. Module d'explicabilité (XAI/SHAP)

- Intégration de **SHAP** pour expliquer chaque décision du modèle aux analystes
- Tableau de bord d'alertes avec visualisation des facteurs déclenchants (top variables SHAP)
- Exemples d'explications individuelles lisibles par des non-spécialistes du ML

#### 4.4.4. Module de feedback et apprentissage continu

- Mise à jour périodique des modèles (réentraînement sur nouveaux patterns)
- Intégration du retour utilisateur (validation des alertes par les analystes bancaires)
- Adaptation continue aux nouvelles typologies de fraude

#### 4.4.5. Sécurité et gestion avancée des utilisateurs

- Authentification et gestion des rôles : analyste fraude, gestionnaire de risques, administrateur système
- Chiffrement des données au repos et en transit
- Conformité KYC/AML et réglementations BCEAO/UEMOA
- Journalisation des accès et des décisions du modèle _(auditabilité)_

---

### 4.5. Stratégies d'action, contenu et périmètre

#### 4.5.1. Phase pilote

- Sélection d'une banque test ou d'un opérateur mobile money à Lomé
- Déploiement progressif sur un périmètre limité de transactions
- Monitoring des performances et ajustements du modèle

#### 4.5.2. Déploiement complet

- Plan de rollout vers les autres institutions bancaires togolaises (3 à 5 banques)
- Formation des équipes (analystes, gestionnaires de risques, DSI)
- Support technique continu et maintenance du système
- Intégration aux systèmes d'information existants (API REST, interopérabilité)

---

### 4.6. Étude de faisabilité

#### 4.6.1. Faisabilité technique

- Infrastructure requise (serveurs, réseau, capacité de traitement temps réel)
- Compétences nécessaires et disponibilité locale au Togo
- Interopérabilité avec les systèmes bancaires togolais existants
- Contraintes spécifiques à l'environnement togolais (connectivité, disponibilité électrique)

#### 4.6.2. Faisabilité économique

- Coûts de développement et de déploiement estimés
- **ROI estimé** : pertes évitées vs coût total du système
- Modèle de financement envisageable (autofinancement bancaire, partenariat institutionnel, soutien BCEAO/UEMOA)
- Analyse coût-bénéfice à 3 ans

#### 4.6.3. Faisabilité sociale

- Acceptabilité du système par les agents bancaires, les analystes et les clients
- Impact sur l'emploi bancaire (outil d'aide à la décision, non de substitution)
- Bénéfices sociétaux : confiance dans les services financiers, protection des utilisateurs de mobile money, inclusion financière
- Formation et conduite du changement

#### 4.6.4. Faisabilité environnementale et réglementaire

- Consommation énergétique du système (sobriété numérique)
- Conformité réglementaire : BCEAO, UEMOA, loi togolaise sur les données personnelles, PCI DSS
- Durabilité et maintenance à long terme

---

### 4.7. Limites de l'étude

- Utilisation d'un dataset international (IEEE-CIS) comme proxy du contexte togolais — transférabilité à confirmer sur données réelles
- Échantillon qualitatif limité à 5–8 responsables bancaires
- Généralisation des résultats à l'ensemble de l'espace UEMOA à valider dans des travaux ultérieurs

---

**Conclusion du chapitre**

---

## CONCLUSION GÉNÉRALE

**Synthèse des résultats et vérification des hypothèses**

Rappel des principaux résultats obtenus, vérification point par point de HG, HS1, HS2 et HS3 à la lumière des résultats du modèle et des entretiens qualitatifs.

**Contributions scientifiques**

- Premier travail documenté sur la détection de fraude bancaire et mobile money par IA dans le contexte togolais
- Modèle d'Ensemble Learning à 3 niveaux adapté aux spécificités des marchés financiers d'Afrique de l'Ouest
- Démonstration de l'apport de l'explicabilité XAI/SHAP pour l'adoption des systèmes d'IA par les praticiens bancaires africains

**Contributions pratiques**

- Architecture et spécifications d'un système applicable aux banques et opérateurs mobile money togolais
- Recommandations opérationnelles pour les institutions bancaires togolaises et les régulateurs

**Limites de l'étude**

- Dataset international comme proxy (cf. 2.3 et 4.7)
- Périmètre géographique limité au Togo

**Perspectives prioritaires**

1. **Partenariat avec une banque ou un opérateur mobile money togolais** — pour obtenir un jeu de données réel et ré-entraîner/valider le modèle sur des données locales authentiques (TogoCom Cash, Moov Money/Flooz).
2. **Extension du périmètre à l'espace UEMOA** — validation du modèle dans d'autres pays francophones d'Afrique de l'Ouest (Sénégal, Côte d'Ivoire, Bénin).
3. **Exploration de l'IA fédérée** — permettre un partage inter-bancaire des modèles sans divulgation de données sensibles, conforme aux réglementations sur la protection des données.
4. **Passage du PoC vers un prototype en sandbox** — déploiement en environnement de test réel auprès d'une institution bancaire togolaise partenaire.

---

## RÉFÉRENCES BIBLIOGRAPHIQUES

_(Norme APA — à compléter au fil de la rédaction)_

---

## ANNEXES

_(Non numérotées)_

- **Annexe A** — Grille d'entretien semi-directif _(responsables IT / Conformité / Risques)_
- **Annexe B** — Questionnaire agents bancaires
- **Annexe C** — Code Python _(prétraitement, SMOTE, entraînement des modèles, SHAP)_
- **Annexe D** — Schéma d'architecture détaillée du système proposé
- **Annexe E** — Résultats complets des métriques d'évaluation _(matrices de confusion, courbes AUC-PR par modèle)_

---

_Format de présentation (norme CDP) :_

- _Police : Times New Roman ou Arial, taille 12_
- _Interligne : 1,5_
- _Marges : 3 cm (gauche), 2,5 cm (droite, supérieure, inférieure)_
- _Longueur cible : 80 à 120 pages (Master), hors couverture, table des matières et annexes_
- _Numérotation des pages : bas de page, à droite_
- _Titres de chapitres : MAJUSCULES, gras, taille 13_
- _Titres de sous-chapitres : gras, minuscule, taille 13_
- _Titres de section (niveau 3) : italique, gras, minuscule, taille 12_
- _Titres de sous-section (niveau 4) : italique, minuscule, taille 12_
