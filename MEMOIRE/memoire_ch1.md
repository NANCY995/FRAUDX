# CONCEPTION D'UN SYSTÈME D'INTELLIGENCE ARTIFICIELLE POUR LA DÉTECTION DE LA FRAUDE BANCAIRE : CAS DU TOGO

**Mémoire de fin d'études — Master**
Conforme au Guide de Rédaction Scientifique — Collège de Paris Supérieur

---

## INTRODUCTION GÉNÉRALE

### 1. Contexte général de l'étude

L'intelligence artificielle constitue aujourd'hui l'un des leviers les plus puissants de la transformation des services financiers à l'échelle mondiale. Dans le secteur bancaire, l'adoption du Machine Learning (ML) a ouvert des perspectives inédites en matière de détection des fraudes, d'évaluation des risques et d'automatisation des processus décisionnels. Les institutions financières des pays développés investissent massivement dans ces technologies, avec des résultats probants : réduction significative des faux positifs, détection en temps réel des schémas frauduleux complexes, et amélioration de l'expérience client (Bhattacharyya et al., 2011 ; Dal Pozzolo et al., 2014).

En Afrique subsaharienne, et particulièrement au Togo, le paysage financier connaît une mutation rapide et profonde. La digitalisation des services bancaires, couplée à l'explosion du mobile money, a transformé les modes de transaction et d'inclusion financière. Selon le rapport de la Banque Centrale des États de l'Afrique de l'Ouest (BCEAO, 2023), le Togo compte désormais plus de 8 millions de comptes de mobile money actifs, dépassant largement le nombre de comptes bancaires traditionnels. Des opérateurs comme TogoCom Cash, Moov Money et Flooz sont devenus les canaux financiers de facto pour une large majorité de la population, notamment dans les zones rurales où l'accès aux agences bancaires reste limité.

Cette digitalisation rapide s'accompagne malheureusement d'une recrudescence des fraudes financières numériques. Les méthodes traditionnelles de détection — règles statiques, contrôles manuels, seuils fixes — montrent leurs limites face à des schémas de fraude de plus en plus sophistiqués : SIM swap, fraude par USSD, ingénierie sociale sur les agents mobile money, usurpation d'identité, et transactions frauduleuses par carte bancaire. Les pertes financières qui en résultent pèsent lourdement sur les institutions bancaires togolaises et érodent la confiance des utilisateurs dans les services financiers numériques.

C'est dans ce contexte que s'inscrit la présente étude, qui vise à concevoir et proposer un système d'intelligence artificielle performant et sécurisé pour la détection de la fraude bancaire, adapté au contexte spécifique du Togo.

### 2. Problématique de l'étude

#### 2.1. Présentation du problème

Malgré les avancées significatives du Machine Learning dans le domaine de la détection de fraude, les institutions bancaires togolaises continuent de s'appuyer majoritairement sur des méthodes traditionnelles : règles métier statiques, contrôles manuels effectués par des analystes, et seuils de déclenchement d'alertes définis empiriquement. Ces approches présentent plusieurs limitations majeures :

- **Rigidité** : les règles doivent être mises à jour manuellement face à l'émergence de nouveaux schémas de fraude, ce qui génère des délais de réaction importants.
- **Taux de faux positifs élevé** : les systèmes basés sur des seuils fixes génèrent un volume considérable d'alertes non pertinentes, submergeant les analystes et réduisant l'efficacité du traitement.
- **Taux de faux négatifs préoccupant** : les fraudes sophistiquées, qui ne correspondent pas aux patterns codifiés dans les règles, passent inaperçues.
- **Absence de couverture du mobile money** : les spécificités des canaux USSD, des agents mobile money et des recharges ne sont pas prises en compte par les systèmes conçus pour les transactions bancaires classiques.

L'intégration d'un système d'IA dans ce contexte soulève par ailleurs des défis majeurs : sécurité des données, interprétabilité des modèles (indispensable pour la conformité réglementaire), et acceptabilité par les analystes financiers qui doivent pouvoir comprendre et valider les décisions du système.

#### 2.2. Formulation du problème

**Question générale (QG) :**
Comment concevoir et implémenter un système d'IA efficace et sécurisé pour la détection de la fraude bancaire au Togo, tout en garantissant une interprétabilité des décisions et une conformité aux normes réglementaires ?

**Questions spécifiques :**

- **QS1** — Quels algorithmes de Machine Learning sont les plus adaptés à la détection de la fraude bancaire dans le contexte spécifique du Togo, caractérisé par une prédominance du mobile money et un fort déséquilibre des classes ?
- **QS2** — Comment concevoir une architecture logicielle sécurisée, intégrant une gestion avancée des utilisateurs et des mécanismes de protection des données, conforme aux réglementations togolaises et régionales (BCEAO/UEMOA) ?
- **QS3** — Dans quelle mesure l'interprétabilité des modèles de ML, via des outils d'explicabilité comme SHAP, facilite-t-elle leur adoption par les analystes financiers et les gestionnaires de risques bancaires togolais ?

### 3. Hypothèses de l'étude

#### 3.1. Hypothèse générale (HG)

L'intégration d'un système de Machine Learning basé sur une approche d'ensemble (Ensemble Learning) permet d'améliorer significativement la précision de la détection de la fraude bancaire au Togo, en identifiant des schémas complexes inaccessibles aux méthodes traditionnelles, tout en offrant un niveau d'explicabilité suffisant pour répondre aux exigences réglementaires.

#### 3.2. Hypothèses spécifiques

- **HS1** — L'automatisation de la détection de la fraude à l'aide de modèles d'apprentissage automatique (notamment XGBoost) réduit significativement le taux de faux négatifs (Recall ≥ 0,85) par rapport aux méthodes statistiques classiques, en fournissant des prédictions plus fiables sur des données transactionnelles déséquilibrées.
- **HS2** — Une plateforme logicielle sécurisée, intégrant une gestion avancée des utilisateurs basée sur le contrôle d'accès par rôles (RBAC) et des mécanismes de protection des données, favorise l'adoption du Machine Learning par les banques togolaises en assurant la conformité aux réglementations en vigueur.
- **HS3** — L'interprétabilité des décisions du modèle via des explications SHAP (concentration des variables influentes, visualisations individuelles) facilite l'acceptation du système par les analystes financiers et les gestionnaires de risques, en rendant les décisions du modèle compréhensibles et vérifiables.

**Cohérence méthodologique :**

| Question | Hypothèse | Objectif |
|---|---|---|
| QS1 — Algorithmes adaptés | HS1 — Réduction des faux négatifs | OS1 — Comparer IF, RF, XGB |
| QS2 — Sécurité et conformité | HS2 — Plateforme RBAC sécurisée | OS2 — Proposer architecture cible |
| QS3 — Interprétabilité | HS3 — SHAP facilite l'adoption | OS3 — Évaluer l'explicabilité |

### 4. Objectifs de l'étude

#### 4.1. Objectif général (OG)

Concevoir et proposer un système d'IA performant, sécurisé et explicable pour la détection en temps réel de la fraude bancaire, adapté au contexte togolais et couvrant les transactions bancaires classiques ainsi que les transactions mobile money.

#### 4.2. Objectifs spécifiques

- **OS1** — Identifier et comparer les algorithmes de Machine Learning les plus adaptés à la détection de fraude dans le secteur bancaire togolais, à travers l'évaluation de trois modèles complémentaires (Isolation Forest, Random Forest, XGBoost) sur des métriques pertinentes en contexte déséquilibré (F1-Score, Recall, AUC-PR).
- **OS2** — Proposer une architecture logicielle sécurisée intégrant une gestion avancée des utilisateurs (RBAC à trois niveaux : analyste, gestionnaire de risques, administrateur) et des mécanismes de protection des données conformes aux réglementations togolaises et régionales.
- **OS3** — Évaluer l'apport de l'explicabilité (XAI) via SHAP dans l'adoption du système par les parties prenantes bancaires, à travers l'analyse de la concentration des variables influentes et la validation qualitative auprès de professionnels du secteur.

### 5. Justification de l'étude

#### 5.1. Justification scientifique

La présente étude apporte une contribution originale à la recherche sur l'application du Machine Learning à la détection de fraude dans le contexte spécifique de l'Afrique de l'Ouest francophone. À notre connaissance, aucune étude n'a encore porté spécifiquement sur la détection de fraude bancaire et mobile money par intelligence artificielle dans le contexte togolais. Ce travail constitue ainsi une contribution à la littérature sur l'IA appliquée aux économies émergentes, en proposant un modèle hybride (Ensemble Learning à trois niveaux + explicabilité SHAP) adapté aux spécificités des marchés financiers africains (faible bancarisation, prédominance du mobile money, contraintes infrastructurelles).

#### 5.2. Justification pratique

Sur le plan opérationnel, cette étude répond à un besoin concret et urgent des institutions bancaires et des opérateurs de mobile money togolais face à la montée des fraudes financières numériques. Les résultats attendus — un modèle performant de détection, une architecture sécurisée, et un prototype fonctionnel — fourniront une base solide pour le déploiement de solutions IA adaptées au contexte local. L'étude s'aligne par ailleurs avec les exigences de transparence des décisions automatisées formulées par les régulateurs régionaux (BCEAO, UEMOA, GIABA), contribuant ainsi à un environnement financier numérique plus sûr et plus inclusif au Togo.

### 5.3. Lacunes identifiées dans la littérature

Conformément à la démarche méthodologique préconisée par Assou (2024), la formulation du problème spécifique de recherche repose sur l'identification d'une ou plusieurs lacunes dans les travaux antérieurs. L'analyse approfondie de la littérature existante — dont la revue détaillée est présentée au Chapitre I (section 1.1.3) — permet de dégager quatre lacunes principales que le présent mémoire vise à combler :

**Lacune 1 — Absence d'étude spécifique au contexte togolais**
À notre connaissance, aucune étude scientifique publiée ne porte spécifiquement sur l'application du Machine Learning à la détection de fraude bancaire et mobile money dans le contexte du Togo. Les travaux existants en Afrique de l'Ouest concernent principalement le Nigeria, le Ghana et la Côte d'Ivoire (cf. Tableau 1.1), laissant le Togo — pourtant caractérisé par l'un des taux d'adoption du mobile money les plus élevés de la région — en dehors du périmètre des analyses. Cette absence constitue une lacune scientifique que le présent travail entreprend de combler.

**Lacune 2 — Non-prise en compte des spécificités du mobile money dans les modèles existants**
Les modèles de détection de fraude proposés dans la littérature récente (Dal Pozzolo et al., 2015 ; Bhattacharyya et al., 2011 ; Carmona et al., 2019) sont majoritairement conçus pour les transactions par carte bancaire dans des contextes européens ou nord-américains. Aucun de ces modèles n'intègre les dimensions propres au mobile money ouest-africain (canal USSD, agents de distribution, cash-in/cash-out, SIM swap) ni ne traite de l'adaptation des variables discriminantes à ce canal spécifique.

**Lacune 3 — Absence de validation empirique de l'apport de l'explicabilité (XAI) dans l'adoption des systèmes de détection de fraude par les praticiens bancaires africains**
Si l'intérêt de l'explicabilité pour les systèmes d'IA est largement reconnu dans la littérature (Lundberg & Lee, 2017 ; Arrieta et al., 2020), très peu d'études empiriques ont évalué son impact sur l'adoption effective des systèmes de détection de fraude par des professionnels bancaires, et aucune à notre connaissance dans un contexte africain. La présente étude propose de combler cette lacune en intégrant un volet qualitatif d'évaluation de l'utilité perçue de SHAP auprès de responsables bancaires togolais.

**Lacune 4 — Insuffisance des architectures sécurisées documentées pour le déploiement de l'IA bancaire en Afrique de l'Ouest**
La littérature technique abonde en modèles performants de détection de fraude, mais rares sont les travaux qui proposent une architecture logicielle complète et sécurisée intégrant à la fois le contrôle d'accès (RBAC), l'explicabilité et les contraintes réglementaires (BCEAO/UEMOA) dans un cadre applicable à une banque ouest-africaine. Ce mémoire contribue à combler cette lacune en proposant une architecture en six couches, une preuve de concept fonctionnelle, et un plan de déploiement progressif.

> **Synthèse** : Ces quatre lacunes justifient la pertinence et l'originalité de la présente recherche. Elles établissent la raison d'être du travail entrepris et orientent directement la formulation des questions spécifiques de recherche (QS1, QS2, QS3) présentées en section 2.2.

### 6. Délimitation de l'étude

#### 6.1. Délimitation géographique

L'étude se concentre sur le système bancaire et les opérateurs de mobile money au Togo, avec un focus sur Lomé comme principal centre financier du pays. Les entretiens qualitatifs sont menés auprès de responsables basés à Lomé, tandis que l'analyse quantitative s'appuie sur un dataset international utilisé comme proxy du contexte togolais.

#### 6.2. Délimitation thématique

Le périmètre de l'étude couvre les fraudes sur les transactions électroniques bancaires et mobile money, incluant :
- La fraude par carte bancaire et virement frauduleux
- Les fraudes spécifiques au mobile money : SIM swap, fraude par USSD, ingénierie sociale sur agents
- L'usurpation d'identité et les transactions non autorisées

Sont exclus du périmètre : la fraude fiscale, la cybercriminalité générale hors secteur financier, et le blanchiment d'argent (traité uniquement comme cadre réglementaire connexe).

#### 6.3. Délimitation temporelle

La période d'analyse couvre 2019-2025, correspondant à la phase de digitalisation bancaire accélérée et de croissance exponentielle du mobile money au Togo.

### 7. Plan du mémoire

Ce mémoire est structuré en quatre chapitres complémentaires. Le **Chapitre I** pose le cadre théorique et conceptuel nécessaire à la compréhension des enjeux de la fraude bancaire et de l'apport du Machine Learning. Le **Chapitre II** détaille la méthodologie de l'étude, incluant la stratégie de vérification des hypothèses et l'opérationnalisation des variables. Le **Chapitre III** présente le système développé et les données utilisées, décrivant l'analyse exploratoire, la conception des modèles et la proposition de plateforme. Enfin, le **Chapitre IV** propose une analyse-diagnostic de la situation et présente l'intervention envisagée, avant de vérifier les hypothèses et d'évaluer la faisabilité du système proposé. Une conclusion générale synthétise les résultats, discute les limites et ouvre des perspectives pour des recherches futures.


## CHAPITRE I — CADRE THÉORIQUE ET CONCEPTUEL

**Introduction du chapitre**

Ce premier chapitre établit les fondements théoriques et conceptuels nécessaires à la compréhension de l'étude. Il aborde successivement la fraude bancaire et ses typologies, les techniques de Machine Learning appliquées à sa détection, l'apport de l'explicabilité (XAI) dans les systèmes financiers, et le cadre légal et réglementaire qui encadre ces technologies au Togo et dans l'espace UEMOA.

### 1.1. La fraude bancaire : concepts et typologie

#### 1.1.1. Définition et classification

La fraude bancaire peut être définie comme l'utilisation intentionnelle de moyens illégaux ou de fausses informations pour obtenir un avantage financier au détriment d'une institution bancaire ou de ses clients (Bolton & Hand, 2002). Elle se distingue de la simple défaillance technique ou de l'erreur humaine par son caractère intentionnel et frauduleux.

Les classifications académiques distinguent généralement plusieurs catégories de fraude bancaire :
- **La fraude par carte bancaire** : utilisation non autorisée d'une carte (physique ou virtuelle) pour effectuer des transactions, incluant la contrefaçon, le skimming, et les achats en ligne frauduleux.
- **La fraude par virement** : détournement de fonds via des transferts électroniques, souvent par social engineering ou compromission de comptes.
- **La fraude sur mobile banking et mobile money** : exploitation des vulnérabilités des plateformes de banque mobile et de transfert d'argent par téléphone.
- **L'usurpation d'identité** : utilisation de données personnelles volées pour ouvrir des comptes ou effectuer des transactions.
- **La fraude documentaire** : falsification de documents bancaires (chèques, lettres de crédit, garanties).

#### 1.1.2. Spécificités de la fraude mobile money au Togo

Le contexte togolais présente des caractéristiques uniques qui influencent directement la typologie des fraudes observées. Le mobile money, avec des opérateurs comme TogoCom Cash, Moov Money et Flooz, constitue le premier canal financier du pays, bien devant les comptes bancaires traditionnels. Cette prédominance s'accompagne de schémas de fraude spécifiques :

**Le SIM swap fraud** : Cette technique consiste à obtenir frauduleusement une carte SIM de remplacement auprès d'un opérateur de téléphonie mobile, permettant au fraudeur d'intercepter les codes de validation (OTP) envoyés par SMS et de prendre le contrôle du compte mobile money de la victime. Cette fraude est particulièrement répandue au Togo en raison de la dépendance au SMS comme facteur d'authentification (BCEAO, 2023).

**La fraude par USSD** : Les codes USSD (* Unstructured Supplementary Service Data), largement utilisés pour les transactions mobile money, peuvent être détournés via des techniques de social engineering. Les fraudeurs contactent les victimes en se faisant passer pour des agents de service client et obtiennent les codes nécessaires pour vider le compte.

**L'ingénierie sociale sur agents mobile money** : Cette fraude cible les agents agréés qui constituent le point d'entrée principal du système mobile money. Les fraudeurs manipulent les agents, exploitent leur méconnaissance des procédures de sécurité, ou soudoyent certains d'entre eux pour effectuer des transactions frauduleuses.

**Tableau 1.1 — Synthèse comparative des études antérieures en Afrique de l'Ouest**

| Pays | Auteurs | Secteur | Méthode IA | Constat principal |
|---|---|---|---|---|
| Côte d'Ivoire | Kouamé (2021) | Banque mobile | Random Forest | F1=0,82 sur données bancaires ivoiriennes |
| Sénégal | Diop & Ndiaye (2022) | Banque | XGBoost | Amélioration de 23% vs règles statiques |
| Bénin | Adjovi (2023) | Mobile money | Logistic Regression | Limites sur données fortement déséquilibrées |
| Nigeria | Okonkwo et al. (2020) | Banque | Ensemble Learning | F1=0,87, prédominance fraude SIM swap |
| Ghana | Mensah (2022) | Mobile money | XGBoost + SMOTE | Recall=0,91 après SMOTE |
| **Togo** | **— (présente étude)** | **Banque + Mobile money** | **IF + RF + XGB + SHAP** | **Première étude documentée (2025)** |

Ce tableau montre qu'aucune étude n'a à ce jour porté spécifiquement sur la détection de fraude bancaire et mobile money par IA dans le contexte togolais, confirmant l'originalité et la pertinence de la présente recherche.

#### 1.1.3. Impact économique

Selon les données disponibles auprès de la BCEAO et du GIABA, les pertes liées à la fraude bancaire et mobile money dans l'espace UEMOA ont augmenté de 45% entre 2020 et 2023. Au Togo, les estimations (basées sur les déclarations des institutions financières) font état de pertes annuelles de l'ordre de 3 à 5 milliards de FCFA, un chiffre probablement sous-évalué en raison de la sous-déclaration et de la difficulté à détecter certaines formes de fraude sophistiquée.

### 1.2. Machine Learning pour la détection de fraude

#### 1.2.1. Concepts fondamentaux

Le Machine Learning est une branche de l'intelligence artificielle qui permet à des systèmes d'apprendre et de s'améliorer à partir de données, sans être explicitement programmés pour chaque tâche (Samuel, 1959). Dans le contexte de la détection de fraude, trois paradigmes d'apprentissage sont pertinents :

- **L'apprentissage supervisé** : le modèle est entraîné sur des données labellisées (transactions marquées comme frauduleuses ou non frauduleuses) pour apprendre à classifier de nouvelles transactions. Les algorithmes comme XGBoost et Random Forest appartiennent à cette catégorie.
- **L'apprentissage non supervisé** : le modèle identifie des anomalies dans les données sans disposer d'étiquettes préalables. Isolation Forest est un exemple typique, adapté aux situations où les données frauduleuses sont rares ou non identifiées.
- **L'apprentissage par renforcement** : le modèle apprend par essais et erreurs en interagissant avec son environnement. Moins utilisé en détection de fraude, il trouve des applications dans les systèmes adaptatifs.

Le choix du paradigme dépend de la disponibilité des données labellisées et de la nature du problème à résoudre. Dans notre étude, l'approche hybride (supervisé + non supervisé) permet de tirer parti des avantages complémentaires de chaque paradigme.

#### 1.2.2. Détection d'anomalies par Isolation Forest

L'Isolation Forest (Liu et al., 2008, 2012) est un algorithme non supervisé spécifiquement conçu pour la détection d'anomalies. Contrairement aux méthodes traditionnelles qui construisent un profil de la normalité puis identifient les déviations, l'Isolation Forest isole directement les anomalies en exploitant leur rareté et leur différence.

**Principe de fonctionnement :**

L'algorithme construit une forêt d'arbres de décision aléatoires (Isolation Trees). Pour chaque arbre :
1. Une caractéristique aléatoire est sélectionnée
2. Une valeur de séparation aléatoire est choisie entre les valeurs minimale et maximale de cette caractéristique
3. Les données sont divisées récursivement jusqu'à l'isolement de chaque point

Les anomalies, étant rares et différentes, nécessitent moins de partitions pour être isolées. Le score d'anomalie est calculé à partir de la profondeur moyenne d'isolement : plus la profondeur est faible, plus le point est considéré comme anormal.

**Avantages pour la détection de fraude :**
- Fonctionne sans données labellisées (adapté aux fraudes émergentes)
- Faible complexité computationnelle (O(n log n))
- Performant sur les jeux de données de grande dimension
- Robuste face au déséquilibre des classes

**Limites :**
- Sensible au choix du paramètre de contamination (proportion attendue d'anomalies)
- Peut manquer des fraudes subtiles qui ressemblent à des transactions normales
- Ne fournit pas d'explication intrinsèque de ses décisions

#### 1.2.3. Random Forest pour la classification

Le Random Forest (Breiman, 2001) est un algorithme d'ensemble learning supervisé qui construit une multitude d'arbres de décision et agrège leurs prédictions. Chaque arbre est entraîné sur un échantillon bootstrap des données d'entraînement, et à chaque nœud de l'arbre, un sous-ensemble aléatoire des caractéristiques est considéré pour la division.

**Principe :**

Le Random Forest combine deux techniques clés :
- **Le bagging (Bootstrap Aggregating)** : chaque arbre est entraîné sur un échantillon différent, réduisant la variance du modèle final
- **La randomisation des caractéristiques** : à chaque nœud, seules m caractéristiques (parmi p) sont considérées, décorrélant les arbres entre eux

Pour une nouvelle transaction, chaque arbre de la forêt vote pour la classe (fraude ou normale), et la prédiction finale est déterminée par la majorité des votes.

**Avantages :**
- Robuste au sur-apprentissage grâce à l'agrégation d'arbres
- Gère naturellement les relations non linéaires et les interactions entre variables
- Fournit une importance intrinsèque des variables (feature importance)
- Parallélisable et efficace sur de grands volumes de données

**Limites :**
- Peut être moins performant que le boosting sur des données fortement déséquilibrées
- Taille du modèle importante (nombreux arbres)
- Moins interprétable qu'un arbre de décision unique
- Nécessite un réglage des hyperparamètres (nombre d'arbres, profondeur maximale)

#### 1.2.4. XGBoost : standard industriel actuel

XGBoost (eXtreme Gradient Boosting), introduit par Chen & Guestrin (2016), est un algorithme d'ensemble learning supervisé basé sur le gradient boosting. Il construit séquentiellement une série d'arbres de décision, chaque nouvel arbre corrigeant les erreurs des arbres précédents.

**Principe :**

Contrairement au Random Forest qui construit des arbres indépendants et parallèles, XGBoost construit des arbres séquentiellement. Chaque nouvel arbre est entraîné sur les résidus (erreurs) de l'ensemble des arbres précédents, en minimisant une fonction objectif qui combine :

$$ \mathcal{L}(\theta) = \sum_{i=1}^{n} l(y_i, \hat{y}_i) + \sum_{k=1}^{K} \Omega(f_k) $$

Où le premier terme mesure l'erreur de prédiction et le second régularise la complexité du modèle pour éviter le sur-apprentissage.

**Avantages clés pour la détection de fraude :**
- Gestion avancée des données déséquilibrées via le paramètre scale_pos_weight
- Régularisation intégrée (L1 et L2) qui réduit le sur-apprentissage
- Gestion native des valeurs manquantes
- Algorithmes optimisés pour la vitesse d'entraînement et l'efficacité mémoire
- Capacité à capturer des interactions complexes entre variables

**Pourquoi XGBoost est le standard industriel :**

XGBoost a remporté de nombreuses compétitions Kaggle et est devenu l'algorithme de référence pour les problèmes de classification sur données tabulaires, incluant la détection de fraude. Sa combinaison de performance prédictive, de robustesse et de rapidité en fait un choix naturel pour notre étude.

**Tableau 1.2 — Comparaison des algorithmes de Machine Learning retenus**

| Caractéristique | Isolation Forest | Random Forest | XGBoost |
|---|---|---|---|
| Type | Non supervisé | Supervisé (ensemble) | Supervisé (boosting) |
| Paradigme | Détection d'anomalies | Classification | Classification |
| Données labellisées | Non requis | Requis | Requis |
| Gestion déséquilibre | Naturelle | Via class_weight | Via scale_pos_weight |
| Interprétabilité | Faible | Moyenne (feature importance) | Moyenne (+ SHAP) |
| Temps d'entraînement | Rapide | Modéré | Modéré |
| Performance sur données déséquilibrées | Bonne (anomalies évidentes) | Bonne | Excellente |
| Rôle dans l'architecture | Niveau 1 : filtrage | Alternative Niveau 2 | Niveau 2 principal |

#### 1.2.5. SMOTE pour le rééquilibrage des classes

Le déséquilibre des classes est un défi majeur en détection de fraude, où les transactions frauduleuses représentent généralement moins de 1% du volume total. Dans ces conditions, un modèle naïf qui classerait toutes les transactions comme normales atteindrait une accuracy de 99%, tout en étant totalement inefficace pour détecter les fraudes.

SMOTE (Synthetic Minority Oversampling Technique), proposé par Chawla et al. (2002), est une technique de rééquilibrage synthétique. Contrairement au sur-échantillonnage aléatoire qui duplique les exemples de la classe minoritaire, SMOTE génère des exemples synthétiques en interpolant entre les observations existantes de la classe minoritaire.

**Principe :**
1. Pour chaque exemple de la classe minoritaire, ses k plus proches voisins (parmi la classe minoritaire) sont identifiés
2. Un vecteur de différence est calculé entre l'exemple et l'un de ses voisins
3. Un nouvel exemple synthétique est créé en ajoutant à l'exemple original une fraction aléatoire de ce vecteur de différence

Cette approche présente l'avantage de générer des exemples réalistes qui enrichissent l'espace des caractéristiques de la classe minoritaire, sans tomber dans la duplication pure qui favoriserait le sur-apprentissage.

### 1.3. Explicabilité (XAI) dans les systèmes bancaires

#### 1.3.1. Le besoin d'explicabilité en finance

L'explicabilité des modèles d'IA (XAI — eXplainable Artificial Intelligence) est devenue un enjeu central du déploiement des systèmes intelligents dans le secteur bancaire. Plusieurs facteurs expliquent cette importance croissante :

- **Exigences réglementaires** : les régulateurs (BCEAO, UEMOA, mais aussi GDPR en Europe) exigent que les décisions automatisées affectant les clients puissent être expliquées et justifiées.
- **Confiance des analystes** : les gestionnaires de risques et analystes fraude doivent pouvoir comprendre pourquoi une transaction a été marquée comme suspecte pour valider ou infirmer l'alerte.
- **Auditabilité** : les décisions du système doivent pouvoir être tracées et vérifiées a posteriori.
- **Amélioration continue** : la compréhension des erreurs du modèle permet d'orienter les efforts d'amélioration.

#### 1.3.2. SHAP (SHapley Additive exPlanations)

SHAP, développé par Lundberg & Lee (2017), est une méthode d'explicabilité basée sur la théorie des jeux coopératifs. Elle attribue à chaque caractéristique une valeur d'importance (SHAP value) qui représente sa contribution à la décision du modèle pour une prédiction donnée.

**Fondement théorique :**

SHAP s'appuie sur les valeurs de Shapley (Shapley, 1953), un concept de théorie des jeux qui distribue équitablement la valeur totale créée par une coalition entre ses membres. Dans le contexte du Machine Learning, chaque caractéristique est considérée comme un "joueur", et la prédiction du modèle comme la "valeur créée" par la coalition des caractéristiques.

La valeur SHAP $ \phi_i $ pour une caractéristique $ i $ est calculée comme :

$$ \phi_i = \sum_{S \subseteq N \setminus \{i\}} \frac{|S|!(|N|-|S|-1)!}{|N|!} [f(S \cup \{i\}) - f(S)] $$

Où $ N $ est l'ensemble de toutes les caractéristiques, $ S $ un sous-ensemble de caractéristiques, et $ f(S) $ la prédiction du modèle utilisant uniquement les caractéristiques de $ S $.

**TreeExplainer pour XGBoost :**

Pour les modèles arborescents comme XGBoost et Random Forest, SHAP propose une implémentation optimisée appelée TreeExplainer (Lundberg et al., 2020), qui calcule exactement les valeurs SHAP en parcourant les arbres, avec une complexité polynomiale plutôt qu'exponentielle.

#### 1.3.3. Applications à la détection de fraude

L'application de SHAP à la détection de fraude présente trois avantages majeurs :

1. **Explication individuelle** : pour chaque transaction, SHAP identifie les variables qui ont poussé le modèle vers une prédiction de fraude ou de normalité, avec leur contribution quantitative.
2. **Vision globale** : l'agrégation des valeurs SHAP sur l'ensemble des prédictions permet d'identifier les variables les plus importantes pour le modèle dans son ensemble.
3. **Conformité réglementaire** : les explications SHAP fournissent une traçabilité transparente des décisions, répondant aux exigences des régulateurs.

Dans le cadre de ce mémoire, SHAP est utilisé pour répondre à HS3, en démontrant que l'explicabilité des décisions du modèle facilite l'adoption du système par les analystes financiers togolais.

### 1.4. Cadre légal et réglementaire

#### 1.4.1. Réglementations bancaires BCEAO/UEMOA

La Banque Centrale des États de l'Afrique de l'Ouest (BCEAO) et l'Union Économique et Monétaire Ouest-Africaine (UEMOA) ont émis plusieurs directives encadrant les activités bancaires et les systèmes de paiement dans l'espace communautaire :

- **La Directive N°01/2018/CM/UEMOA** relative aux systèmes de paiement dans les États membres de l'UEMOA, qui établit les exigences minimales de sécurité pour les transactions électroniques.
- **La Loi Uniforme sur la Lutte contre le Blanchiment de Capitaux et le Financement du Terrorisme (LBC/FT)** qui impose aux institutions financières la mise en place de dispositifs de contrôle et de détection des opérations suspectes.
- **Le Règlement N°01/2020/CM/UEMOA** sur les services de paiement mobile, qui encadre spécifiquement les activités des opérateurs de mobile money.

#### 1.4.2. Dispositifs AML/KYC et GIABA

Le Groupe Intergouvernemental d'Action contre le Blanchiment d'Argent en Afrique de l'Ouest (GIABA) est l'organe régional de lutte contre le blanchiment de capitaux. Ses recommandations, alignées sur les standards du GAFI (Groupe d'Action Financière), imposent aux institutions financières :

- La mise en œuvre de procédures KYC (Know Your Customer) rigoureuses
- La déclaration des opérations suspectes aux cellules de renseignement financier
- La conservation des données transactionnelles pour une durée minimale de 10 ans
- L'évaluation périodique des risques de blanchiment et de financement du terrorisme

#### 1.4.3. Protection des données personnelles

Le Togo s'est doté d'une loi sur la protection des données à caractère personnel (Loi N°2020-003 du 20 février 2020), qui encadre la collecte, le traitement et la conservation des données personnelles. Cette loi, alignée sur le Règlement Général sur la Protection des Données (RGPD) européen, impose notamment :

- Le consentement préalable des personnes concernées
- La limitation de la collecte aux données strictement nécessaires
- Le droit d'accès, de rectification et d'opposition des personnes
- La sécurisation des données par des mesures techniques appropriées

Ces exigences ont été intégrées dans la conception de l'architecture proposée au Chapitre III.

**Conclusion du chapitre**

Ce premier chapitre a établi les fondements théoriques et conceptuels de notre étude. Nous avons montré que la fraude bancaire au Togo présente des caractéristiques spécifiques, notamment liées à la prédominance du mobile money et à l'émergence de schémas de fraude adaptés à ce canal. Le Machine Learning, et particulièrement l'approche d'ensemble learning combinant Isolation Forest, Random Forest et XGBoost, offre des solutions performantes pour la détection de ces fraudes, à condition de traiter correctement le déséquilibre des classes via SMOTE.

L'explicabilité des modèles, via SHAP, apparaît comme un facteur clé de l'adoption des systèmes d'IA par les professionnels bancaires, répondant à la fois aux exigences réglementaires et aux besoins opérationnels. Le cadre légal et réglementaire, incarné par la BCEAO, l'UEMOA et le GIABA, fournit un socle normatif solide pour le déploiement de ces technologies au Togo.

Le chapitre suivant détaille la méthodologie employée pour vérifier les hypothèses formulées dans l'introduction, en précisant les variables, les indicateurs, les outils et la stratégie de vérification.
