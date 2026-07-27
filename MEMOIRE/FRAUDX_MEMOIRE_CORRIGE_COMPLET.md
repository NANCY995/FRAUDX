## RÉSUMÉ

Dans un monde où la digitalisation financière transforme en profondeur les relations bancaires, la détection de la fraude représente à la fois un enjeu de sécurité et un défi majeur pour les institutions financières. SUNU Bank Togo, banque du Groupe SUNU présente au Togo et dans plusieurs pays de l'UEMOA, ne fait pas exception. Confrontée à une recrudescence des fraudes bancaires et numériques face auxquelles les méthodes traditionnelles de détection — règles statiques, contrôles manuels — montrent leurs limites, cette banque peine à exploiter pleinement le potentiel des technologies d'intelligence artificielle pour sécuriser ses transactions et protéger sa clientèle. Ce mémoire porte sur la conception et la proposition d'un système d'intelligence artificielle performant, sécurisé et explicable pour la détection de la fraude bancaire, adapté au contexte de SUNU Bank.

L'approche méthodologique retenue est quantitative, non expérimentale, à visée explicative. L'analyse quantitative compare trois algorithmes de Machine Learning — Isolation Forest, Random Forest et XGBoost — sur le jeu de données public IEEE-CIS Fraud Detection, en utilisant SMOTE pour le rééquilibrage des classes et SHAP pour l'explicabilité.

Un volet qualitatif est proposé en perspective pour confronter les résultats aux perceptions du terrain. Les résultats montrent la supériorité de XGBoost après optimisation par Optuna (Recall = 85,02 % ; Précision = 13,54 % ; AUC-PR = 0,57), avec une latence de prédiction compatible avec les exigences du temps réel. Une preuve de concept fonctionnelle (FRAUDX) a été développée, intégrant un tableau de bord interactif avec contrôle d'accès RBAC, un module SHAP d'explicabilité des décisions et un module de feedback pour l'apprentissage continu.

Si le périmètre conceptuel de l'étude inclut les transactions bancaires classiques et le mobile money (via TogoCom Cash et Moov Money/Flooz), le modèle a été entraîné sur le jeu de données international de transactions par carte (IEEE-CIS), faute de données réelles togolaises accessibles — une limite explicitement reconnue, dont l'intégration des spécificités du mobile money constitue la perspective prioritaire.

Cette recherche contribue au domaine émergent de l'IA appliquée à la détection de la fraude bancaire en contexte africain, en démontrant la faisabilité technique et le potentiel économique d'une solution adaptée aux contraintes des banques ouest-africaines.

**Mots-clés :** Détection de fraude bancaire, Machine Learning, XGBoost, Ensemble Learning, SHAP, SUNU Bank, Togo, Mobile Money, RBAC, Explicabilité (XAI).

---

## ABSTRACT

In a world where financial digitalization is profoundly transforming banking relationships, fraud detection represents both a security concern and a major challenge for financial institutions. SUNU Bank Togo, a bank of the SUNU Group present in Togo and several WAEMU countries, is no exception. Faced with a rise in banking and digital fraud against which traditional detection methods — static rules, manual controls — are showing their limits, the bank struggles to fully exploit the potential of artificial intelligence technologies to secure its transactions and protect its customers. This thesis focuses on the design and proposal of a high-performing, secure, and explainable artificial intelligence system for bank fraud detection, adapted to the context of SUNU Bank.

The methodological approach adopted is quantitative, non-experimental, with an explanatory purpose. The quantitative analysis compares three Machine Learning algorithms — Isolation Forest, Random Forest, and XGBoost — on the public IEEE-CIS Fraud Detection dataset, using SMOTE for class rebalancing and SHAP for explainability.

A qualitative component is proposed as a future direction to compare the results with field perceptions. The results show the superiority of XGBoost after optimization via Optuna (Recall = 85.02%; Precision = 13.54%; AUC-PR = 0.57), with a prediction latency compatible with real-time requirements. A functional proof of concept (FRAUDX) was developed, featuring an interactive dashboard with RBAC access control, a SHAP-based decision-explainability module, and a feedback module for continuous learning.

While the conceptual scope of the study includes both traditional banking transactions and mobile money (via TogoCom Cash and Moov Money/Flooz), the model was trained on the international card transaction dataset (IEEE-CIS) due to the lack of accessible real Togolese data — an explicitly acknowledged limitation, with the integration of mobile money-specific characteristics identified as a priority direction for future work.

This research contributes to the emerging field of AI applied to bank fraud detection in the African context, demonstrating the technical feasibility and economic potential of a solution adapted to the constraints of West African banks.

**Keywords:** Banking fraud detection, Machine Learning, XGBoost, Ensemble Learning, SHAP, SUNU Bank, Togo, Mobile Money, RBAC, Explainable AI (XAI).

---

# INTRODUCTION GÉNÉRALE

## 1. CONTEXTE GÉNÉRAL DE L'ÉTUDE

L'intelligence artificielle constitue aujourd'hui l'un des leviers les plus puissants de la transformation des services financiers à l'échelle mondiale. Dans le secteur bancaire, l'adoption du Machine Learning (ML) a ouvert des perspectives inédites en matière de détection des fraudes, d'évaluation des risques et d'automatisation des processus décisionnels. Les institutions financières des pays développés investissent massivement dans ces technologies, avec des résultats probants : réduction significative des faux positifs, détection en temps réel des schémas frauduleux complexes, et amélioration de l'expérience client (Bhattacharyya et al., 2011 ; Dal Pozzolo et al., 2014).

En Afrique subsaharienne, et particulièrement au Togo, le paysage financier connaît une mutation rapide et profonde. La digitalisation des services bancaires, couplée à l'explosion du mobile money, a transformé les modes de transaction et d'inclusion financière. Selon le rapport de la Banque Centrale des États de l'Afrique de l'Ouest (BCEAO, 2024), le Togo comptait plus de 12,5 millions de comptes de mobile money ouverts à fin 2024, dont environ 6,1 millions de comptes actifs — soit un taux d'activité de 48,35 %, le plus élevé de l'espace UEMOA. Ce dynamisme s'est confirmé par une progression du nombre de comptes actifs togolais de 76,87 % entre 2023 et 2024, la plus forte croissance enregistrée dans l'Union sur la période. Des opérateurs comme TogoCom Cash, Moov Money et Flooz sont devenus les canaux financiers de facto pour une large majorité de la population, notamment dans les zones rurales où l'accès aux agences bancaires reste limité.

Dans cet écosystème, Sunu Bank Togo s'est positionnée comme un acteur bancaire résolument digital. À travers ses services WhatsApp Banking et l'application MySUNU Bank, la banque propose des transferts Bank-to-Wallet vers les comptes mobiles money (T-money, Flooz, Mixx by Yas), avec des plafonds quotidiens pouvant atteindre 400 000 FCFA. Cette interconnexion directe avec l'écosystème du mobile money expose Sunu Bank aux risques spécifiques de fraude liés aux canaux mobiles et aux portefeuilles électroniques.

Cette digitalisation rapide s'accompagne malheureusement d'une recrudescence des fraudes financières numériques. Les méthodes traditionnelles de détection — règles statiques, contrôles manuels, seuils fixes — montrent leurs limites face à des schémas de fraude de plus en plus sophistiqués : SIM swap, fraude par USSD, ingénierie sociale sur les agents mobile money, usurpation d'identité, et transactions frauduleuses par carte bancaire. Les pertes financières qui en résultent pèsent lourdement sur les institutions bancaires togolaises et érodent la confiance des utilisateurs dans les services financiers numériques.

C'est dans ce contexte que s'inscrit la présente étude, qui vise à concevoir et proposer un système d'intelligence artificielle performant et sécurisé pour la détection de la fraude bancaire, adapté au contexte spécifique de Sunu Bank Togo.

## 2. PROBLÉMATIQUE DE L'ÉTUDE

### 2.1. Présentation du problème

Malgré les avancées significatives du Machine Learning dans le domaine de la détection de fraude, Sunu Bank continue de s'appuyer majoritairement sur des méthodes traditionnelles : règles métier statiques, contrôles manuels effectués par des analystes, et seuils de déclenchement d'alertes définis empiriquement. Cette approche historique, bien qu'elle ait fourni une base opérationnelle, révèle ses limitations face à un contexte où les risques évoluent rapidement et où les attaquants développent des stratégies toujours plus sophistiquées.

Les approches actuelles présentent des lacunes majeures qui impactent directement l'efficacité opérationnelle. La rigidité des systèmes impose une mise à jour manuelle des règles face à l'émergence de nouveaux schémas de fraude, générant des délais de réaction critiques. Parallèlement, les seuils fixes produisent un volume considérable de faux positifs, submergeant les analystes et dégradant leur capacité de traitement, tandis que les fraudes sophistiquées, qui ne correspondent pas aux patterns codifiés, passent inaperçues comme faux négatifs. Un enjeu supplémentaire réside dans l'absence de couverture du mobile money : les spécificités des canaux USSD, des agents mobile money et des recharges ne sont pas prises en compte par des systèmes conçus exclusivement pour les transactions bancaires classiques.

L'intégration d'un système d'IA soulève cependant des défis majeurs qu'il est indispensable de résoudre pour garantir le succès du projet. La sécurité des données, la conformité réglementaire et l'interprétabilité des modèles deviennent des enjeux critiques : les décisions prises par l'IA doivent pouvoir être expliquées et validées par les analystes financiers. Seule une approche qui associe la puissance prédictive du Machine Learning à une transparence opérationnelle et une acceptabilité des utilisateurs permettra une véritable modernisation du système de détection de fraude.

### 2.2. Formulation du problème

Face à ce constat, une question centrale se pose :

**Comment concevoir et implémenter un système d'IA efficace et sécurisé pour la détection de la fraude bancaire au Togo pour Sunu Bank, tout en garantissant une interprétabilité des décisions et une conformité aux normes réglementaires ?**

Pour y répondre, plusieurs interrogations spécifiques méritent d'être explorées :

- Quels algorithmes de Machine Learning sont les plus adaptés à la détection de la fraude bancaire dans le contexte spécifique de Sunu Bank, caractérisé par une prédominance du mobile money et un déséquilibre des classes ?
- Comment concevoir une architecture logicielle sécurisée, intégrant une gestion avancée des utilisateurs et des mécanismes de protection des données, conforme aux réglementations togolaises et régionales (BCEAO/UEMOA) ?
- Dans quelle mesure l'interprétabilité des modèles de ML, via des outils d'explicabilité comme SHAP, facilite-t-elle leur adoption par les analystes financiers et les gestionnaires de risques bancaires de Sunu Bank ?

## 3. HYPOTHÈSES DE L'ÉTUDE

### 3.1. Hypothèse générale

L'intégration d'un système de Machine Learning basé sur une approche d'ensemble (Ensemble Learning) permet d'améliorer significativement la précision de la détection de la fraude bancaire au Togo pour Sunu Bank, en identifiant des schémas complexes inaccessibles aux méthodes traditionnelles, tout en offrant un niveau d'explicabilité suffisant pour répondre aux exigences réglementaires.

### 3.2. Hypothèses spécifiques

Pour approfondir cette hypothèse générale, plusieurs hypothèses spécifiques sont avancées :

- **HS1** — L'automatisation de la détection de la fraude à l'aide de modèles d'apprentissage automatique (notamment XGBoost) réduit significativement le taux de faux négatifs (Recall ≥ 0,60) par rapport aux méthodes statistiques classiques, en fournissant des prédictions plus fiables sur des données transactionnelles déséquilibrées.
- **HS2** — Une plateforme logicielle sécurisée, intégrant une gestion avancée des utilisateurs basée sur le contrôle d'accès par rôles (RBAC) et des mécanismes de protection des données, favorise l'adoption du Machine Learning par les banques togolaises en assurant la conformité aux réglementations en vigueur.
- **HS3** — L'interprétabilité des décisions du modèle via des explications SHAP facilite l'acceptation du système par les analystes financiers et les gestionnaires de risques, en rendant les décisions du modèle compréhensibles et vérifiables.

## 4. OBJECTIFS DE L'ÉTUDE

### 4.1. Objectif général

Concevoir et proposer un système d'IA performant, sécurisé et explicable pour la détection en temps réel de la fraude bancaire, adapté au contexte togolais de Sunu Bank et couvrant les transactions bancaires classiques ainsi que les transactions mobile money.

### 4.2. Objectifs spécifiques

Afin de répondre à cet objectif principal, l'étude poursuit plusieurs objectifs complémentaires :

- **OS1** — Identifier et comparer les algorithmes de Machine Learning les plus adaptés à la détection de fraude dans le secteur bancaire togolais, à travers l'évaluation de trois modèles complémentaires (Isolation Forest, Random Forest, XGBoost) sur des métriques pertinentes en contexte déséquilibré (F1-Score, Recall, AUC-PR).
- **OS2** — Proposer une architecture logicielle sécurisée intégrant une gestion avancée des utilisateurs (RBAC à trois niveaux : analyste, gestionnaire de risques, administrateur) et des mécanismes de protection des données conformes aux réglementations togolaises et régionales.
- **OS3** — Évaluer l'apport de l'explicabilité (XAI) via SHAP dans l'adoption du système par les parties prenantes bancaires, à travers l'analyse de la concentration des variables influentes.

## 5. JUSTIFICATION DE L'ÉTUDE

### 5.1. Justification scientifique

La présente étude apporte une contribution originale à la recherche sur l'application du Machine Learning à la détection de fraude dans le contexte spécifique des banques commerciales de l'UEMOA. Bien que la littérature internationale documente largement l'usage d'algorithmes d'apprentissage automatique et de méthodes ensemblistes pour la lutte contre la fraude bancaire, peu de travaux portent sur leur implémentation concrète dans les institutions financières de l'UEMOA, et aucun ne s'intéresse, à notre connaissance, au cas d'une banque du Groupe SUNU. Ce travail s'inscrit ainsi dans la littérature émergente sur l'IA appliquée aux banques africaines en proposant une approche comparative de trois algorithmes d'ensemble learning (Isolation Forest, Random Forest, XGBoost) associée à une explicabilité par SHAP — conçue pour tenir compte des spécificités opérationnelles et réglementaires des institutions financières régionales.

### 5.2. Justification pratique

Sur le plan opérationnel, cette étude répond à un besoin concret des institutions bancaires face à la montée des fraudes financières numériques. Les résultats attendus — un modèle performant de détection, une architecture sécurisée, et un prototype fonctionnel — fourniront une base solide pour le déploiement de solutions IA adaptées au contexte local. L'étude s'aligne par ailleurs avec les exigences de transparence des décisions automatisées formulées par les régulateurs régionaux (BCEAO, UEMOA, GIABA), contribuant ainsi à un environnement financier numérique plus sûr et plus inclusif au Togo.

## 6. DÉLIMITATION DE L'ÉTUDE

### 6.1. Délimitation géographique

L'étude se concentre sur le système bancaire et les opérateurs de mobile money au Togo, avec un focus sur Lomé comme principal centre financier du pays. L'analyse quantitative s'appuie sur un jeu de données international utilisé comme proxy du contexte de Sunu Bank. Un volet qualitatif est proposé en perspective pour confronter les résultats aux perceptions des professionnels du secteur basés à Lomé.

### 6.2. Délimitation thématique

Le périmètre de l'étude couvre les fraudes sur les transactions électroniques bancaires et mobile money, incluant :

- La fraude par carte bancaire et virement frauduleux
- Les fraudes spécifiques au mobile money : SIM swap, fraude par USSD, ingénierie sociale sur agents
- L'usurpation d'identité et les transactions non autorisées

Sont exclus du périmètre : la fraude fiscale, la cybercriminalité générale hors secteur financier, et le blanchiment d'argent (traité uniquement comme cadre réglementaire connexe).

### 6.3. Délimitation technique

La période d'analyse couvre 2019-2025, correspondant à la phase de digitalisation bancaire accélérée et de croissance exponentielle du mobile money au Togo et la période de fin du stage dans l'entreprise (2025). Il convient également de souligner que la conception et l'évaluation du système FRAUDX sont soumises aux contraintes techniques imposées par l'environnement de développement et les jeux de données mobilisés (absence d'infrastructure GPU dédiée, ressources de calcul limitées à une machine locale et à Google Colab, quotas et limites de traitement inhérents à ces environnements).

Ces contraintes ont notamment restreint la profondeur de la recherche d'hyperparamètres et imposé le recours à un sous-échantillonnage des données lors de la phase d'optimisation. À cela s'ajoute l'indisponibilité de données bancaires et mobile money togolaises réelles, imposant l'utilisation d'un jeu de données international (IEEE-CIS) comme proxy, ce qui peut affecter certaines fonctionnalités, comme la calibration fine des seuils de détection, l'intégration des spécificités du canal USSD ou la prise en compte des comportements propres aux agents mobile money.

Le système est par ailleurs contraint par des exigences opérationnelles strictes (latence inférieure à 100 ms par transaction, taux de faux positifs maîtrisé, conservation des logs d'audit sur une durée de dix ans) ainsi que par des exigences de sécurité imposées par la nature sensible des données traitées (chiffrement des données en transit et au repos, authentification renforcée, contrôle d'accès par rôles), qui doivent être conciliées avec les contraintes de performance et de rapidité de traitement en temps réel.

Les canaux mobile money autres que ceux explicitement mentionnés (TogoCom Cash, Moov Money, Flooz), ainsi que les canaux bancaires internationaux ou les moyens de paiement non couverts par Sunu Bank, ne sont pas inclus dans le périmètre de cette étude. De même, les aspects financiers, juridiques et organisationnels liés au déploiement à grande échelle du système ne sont abordés que de façon indirecte, uniquement dans la mesure où ils influencent la faisabilité technique de la solution proposée.

## 7. PLAN DU MÉMOIRE

Ce mémoire est structuré en quatre chapitres complémentaires. Le premier pose le cadre théorique et conceptuel nécessaire à la compréhension des enjeux de la fraude bancaire et de l'apport du Machine Learning. Le deuxième chapitre détaille la méthodologie de l'étude, incluant la stratégie de vérification des hypothèses et l'opérationnalisation des variables. Le troisième chapitre présente le système développé et les données utilisées, décrivant l'analyse exploratoire, la conception des modèles et la proposition de plateforme. Enfin, le quatrième chapitre propose une analyse-diagnostic de la situation et présente l'intervention envisagée, avant de vérifier les hypothèses et d'évaluer la faisabilité du système proposé. Une conclusion générale synthétise les résultats, discute les limites et ouvre des perspectives pour des recherches futures.

---

# CHAPITRE I : CADRE THÉORIQUE ET CONCEPTUEL

## Introduction

Le secteur bancaire mondial connaît une mutation profonde sous l'effet conjugué de la digitalisation financière et de la montée en puissance des technologies d'intelligence artificielle, qui redéfinissent les modalités de gestion du risque et de sécurisation des transactions (Bhattacharyya et al., 2011). La détection de la fraude, longtemps assurée par des dispositifs de règles statiques et de contrôles manuels, se trouve aujourd'hui confrontée à des schémas frauduleux de plus en plus sophistiqués, que les méthodes traditionnelles peinent à identifier en temps utile (Dal Pozzolo et al., 2014). Pour les institutions financières, cette évolution représente à la fois une opportunité de renforcer leur résilience et un défi majeur, tant sur le plan technique que réglementaire. Néanmoins, de nombreuses banques ouest-africaines peinent à exploiter pleinement ce potentiel, confrontées à un déficit de données locales labellisées, à des contraintes d'infrastructure et à l'absence de cadres méthodologiques adaptés à la spécificité du mobile money (BCEAO, 2023).

Face à ces défis, l'intégration de systèmes d'apprentissage automatique combinant plusieurs algorithmes complémentaires — Isolation Forest, Random Forest et XGBoost — couplés à des outils d'explicabilité comme SHAP, émerge comme une voie prometteuse pour concilier performance de détection et conformité réglementaire (Lundberg & Lee, 2017). Ces technologies permettent l'identification de patterns de fraude complexes, inaccessibles aux règles codifiées manuellement (Chen & Guestrin, 2016), tout en offrant aux analystes financiers la transparence nécessaire à la validation de leurs décisions. Sunu Bank Togo constitue un cas d'étude pertinent pour analyser ces technologies dans un contexte bancaire ouest-africain marqué par la prédominance du mobile money.

Ce chapitre établit un cadre théorique et conceptuel solide pour appréhender la conception d'un système d'intelligence artificielle appliqué à la détection de la fraude bancaire. Il s'articule autour de quatre axes : la fraude bancaire et ses typologies, notamment ses spécificités liées au mobile money togolais ; les techniques de Machine Learning mobilisées pour sa détection ; l'apport de l'explicabilité (XAI) dans les systèmes financiers ; et le cadre légal et réglementaire encadrant le déploiement de l'IA au Togo et dans l'espace UEMOA.

## I.1. Cadre théorique et état de l'art

Dans cette section du premier chapitre, nous établissons les fondements théoriques et conceptuels nécessaires à la compréhension des enjeux de la fraude bancaire et mobile money, ainsi que de l'apport du Machine Learning et de l'explicabilité (XAI) pour y répondre. Il s'organise en trois temps : le cadre théorique qui définit les concepts mobilisés ; l'historique et l'évolution du domaine qui situe ces concepts dans une trajectoire chronologique ; et l'état de l'art qui positionne la présente étude par rapport aux travaux antérieurs et identifie les lacunes qu'elle entend combler.

### I.1.1. La fraude bancaire et mobile money : concepts et typologies

#### I.1.1.1. Définition de la fraude financière

La fraude bancaire peut être définie comme l'utilisation intentionnelle de moyens illégaux ou de fausses informations pour obtenir un avantage financier au détriment d'une institution bancaire ou de ses clients (Bolton & Hand, 2002). Elle se distingue de la simple défaillance technique ou de l'erreur humaine par son caractère intentionnel et frauduleux. Cette définition, bien qu'initialement forgée dans le contexte des systèmes bancaires classiques, s'étend naturellement aux services financiers numériques — dont le mobile money — dès lors que l'intention frauduleuse et le préjudice financier sont établis, indépendamment du canal technique utilisé.

#### I.1.1.2. Typologie des fraudes bancaires

Les classifications académiques distinguent généralement plusieurs catégories de fraude bancaire :

- **La fraude par carte bancaire** : utilisation non autorisée d'une carte (physique ou virtuelle) pour effectuer des transactions, incluant la contrefaçon, le skimming, et les achats en ligne frauduleux.
- **La fraude par virement** : détournement de fonds via des transferts électroniques, souvent par social engineering ou compromission de comptes.
- **La fraude sur mobile banking et mobile money** : exploitation des vulnérabilités des plateformes de banque mobile et de transfert d'argent par téléphone.
- **L'usurpation d'identité** : utilisation de données personnelles volées pour ouvrir des comptes ou effectuer des transactions.
- **La fraude documentaire** : falsification de documents bancaires (chèques, lettres de crédit, garanties).

Cette typologie générale sert de socle commun à la littérature internationale ; la section suivante en précise les manifestations propres au contexte togolais.

#### I.1.1.3. Spécificités de la fraude mobile money au Togo

Le contexte togolais présente des caractéristiques particulières qui influencent directement la typologie des fraudes observées. Le mobile money y occupe une place centrale dans les usages financiers quotidiens, grâce à sa rapidité, sa simplicité d'utilisation et sa large adoption par la population : selon la BCEAO (2024), le Togo affiche le taux de comptes actifs le plus élevé de l'espace UEMOA (48,35 %), traduisant une intensité d'usage particulièrement forte de ce canal. Cette forte dépendance au canal numérique en fait une cible privilégiée pour les fraudeurs, qui exploitent moins des failles techniques complexes que la confiance des usagers et la pression psychologique exercée dans l'urgence.

Au Togo, les fraudes liées au mobile money reposent principalement sur l'ingénierie sociale, ainsi que le montrent les alertes officielles diffusées en 2025 par l'Agence Nationale de Cybersécurité (ANCY) et le Centre Togolais de Réponse aux Incidents de Sécurité Informatique (CERT-TG). Les escrocs cherchent à manipuler la victime par téléphone ou par message afin de l'amener à divulguer un code de validation, à confirmer une opération qu'elle n'a pas initiée, ou à effectuer un remboursement frauduleux. Quatre schémas dominent :

1. **Le faux transfert Mobile Money** : l'arnaqueur prétend avoir envoyé de l'argent par erreur sur le compte de la victime et exerce une pression pour obtenir un remboursement immédiat, avant que la victime n'ait pu vérifier son solde réel (ANCY, 2025a).

2. **L'usurpation d'agent** : le fraudeur se fait passer pour un représentant agréé d'un opérateur mobile money (T-Money, Flooz, Mixx by Yas ou Moov Money) afin d'obtenir un code de validation ou un code secret censé rester confidentiel (ANCY, 2025b).

3. **La fausse réidentification** : ce schéma combine manipulation psychologique et exploitation d'un mécanisme technique légitime — la victime reçoit un véritable SMS de validation pendant l'appel frauduleux, puis l'escroc l'incite à communiquer ce code sous prétexte de réidentification de compte (ANCY, 2025b).

4. **Les plateformes frauduleuses de vente ou d'investissement** : les victimes sont incitées à effectuer des dépôts via Mobile Money pour percevoir des « commissions », valider des « commandes » ou bénéficier d'un système de « parrainage », avant d'être bloquées par les opérateurs de la plateforme (CERT-TG, 2025).

Ce qui rend ces fraudes particulièrement spécifiques au contexte togolais tient à leur ancrage dans les pratiques locales. Les escrocs utilisent des numéros de téléphone locaux, un discours en français courant et des références aux opérateurs connus du pays afin d'instaurer un climat de confiance. Le facteur temporel joue ici un rôle essentiel : la victime est poussée à agir sans vérification préalable, ce qui renforce l'efficacité de la fraude.

Ces observations montrent que la fraude mobile money au Togo relève davantage d'une exploitation des usages sociaux et comportementaux que d'attaques purement techniques. Toutefois, des formes plus techniques de fraude, telles que le SIM-swap ou certaines manipulations liées aux services USSD, demeurent des risques potentiels dans la sous-région et peuvent également concerner le Togo, même si les alertes récentes mettent surtout en évidence la prépondérance des arnaques par ingénierie sociale.

**Tableau 1.1 — Synthèse comparative des études antérieures en Afrique de l'Ouest**

| Pays | Auteurs | Secteur | Méthode IA | Constat principal |
|------|---------|---------|------------|-------------------|
| Côte d'Ivoire | Kouamé (2021) | Banque mobile | Random Forest | F1=0,82 sur données bancaires ivoiriennes |
| Sénégal | Diop & Ndiaye (2022) | Banque | XGBoost | Amélioration de 23% vs règles statiques |
| Bénin | Adjovi (2023) | Mobile money | Logistic Regression | Limites sur données fortement déséquilibrées |
| Nigeria | Okonkwo et al. (2020) | Banque | Ensemble Learning | F1=0,87, prédominance fraude SIM swap |
| Ghana | Mensah (2022) | Mobile money | XGBoost + SMOTE | Recall=0,91 après SMOTE |
| **Togo** | — (présente étude) | Banque + Mobile money | IF + RF + XGB + SHAP | **Première étude documentée (2025)** |

Ce tableau montre qu'aucune étude n'a à ce jour porté spécifiquement sur la détection de fraude bancaire et mobile money par IA dans le contexte togolais, confirmant l'originalité et la pertinence de la présente recherche.

#### I.1.1.4. Facteurs d'émergence et de vulnérabilité

Plusieurs facteurs structurels expliquent l'ampleur que prend la fraude liée au mobile money au Togo.

Le premier tient à la forte diffusion de ce canal dans les usages financiers quotidiens. Le mobile money s'est imposé comme un moyen privilégié pour le rechargement de crédit téléphonique, les transferts d'argent, les paiements de factures et les transactions marchandes, ce qui augmente mécaniquement la surface d'exposition à la fraude. Selon une enquête de l'ARCEP relayée par Togo First (2024), le Togo comptait 3,55 millions d'utilisateurs mobile money en 2024, et 86 % des abonnés mobiles disposent d'un compte mobile money.

Le deuxième facteur est la dépendance persistante aux canaux téléphoniques classiques — SMS et appels vocaux — pour valider ou accompagner certaines opérations. Cette configuration favorise les arnaques fondées sur l'ingénierie sociale, telles que documentées par l'ANCY (2025a, 2025b).

Un troisième élément de vulnérabilité concerne les limites des mécanismes de protection et de sensibilisation des usagers. La même enquête de l'ARCEP montre que les coûts élevés des transactions constituent un frein pour 81 % des sondés, tandis que le manque d'interopérabilité entre T-Money et Flooz en constitue un pour 75 % d'entre eux.

Enfin, l'ampleur de cette fraude doit être replacée dans le cadre plus large de la transformation numérique du secteur financier togolais. Les institutions qui s'appuient encore sur des règles métier statiques et des contrôles manuels disposent de moyens limités pour suivre l'évolution rapide des schémas frauduleux.

### I.1.2. Le Machine Learning appliqué à la détection de fraude

Le Machine Learning est une branche de l'intelligence artificielle qui permet à des systèmes d'apprendre et de s'améliorer à partir de données, sans être explicitement programmés pour chaque tâche (Samuel, 1959). Appliqué à la détection de fraude, il permet de dépasser les limites des règles métier statiques en identifiant des régularités statistiques complexes dans le comportement transactionnel, y compris des schémas qui n'ont pas été anticipés par un expert humain.

#### I.1.2.1. Apprentissage supervisé, non supervisé et hybride

Trois paradigmes d'apprentissage sont pertinents pour la détection de fraude :

- **L'apprentissage supervisé** : le modèle est entraîné sur des données labellisées pour apprendre à classifier de nouvelles transactions. Les algorithmes comme XGBoost et Random Forest appartiennent à cette catégorie.
- **L'apprentissage non supervisé** : le modèle identifie des anomalies dans les données sans disposer d'étiquettes préalables. Isolation Forest est un exemple typique.
- **L'apprentissage par renforcement** : le modèle apprend par essais et erreurs. Moins utilisé en détection de fraude.

Dans notre étude, l'approche comparative (supervisé + non supervisé) permet de tirer parti des avantages complémentaires de chaque paradigme.

#### I.1.2.2. Détection d'anomalies et gestion du déséquilibre des classes

La détection de fraude présente une contrainte structurelle : le déséquilibre extrême des classes, les transactions frauduleuses représentant généralement moins de 1 % du volume total. Dans ces conditions, un modèle naïf qui classerait systématiquement une transaction comme non frauduleuse atteindrait une accuracy proche de 99 %, tout en étant totalement inefficace — ce qui disqualifie l'Accuracy comme métrique pertinente.

Dans ce contexte, les métriques adaptées sont le Recall, le F1-Score et l'AUC-PR, qui privilégient la détection de la classe minoritaire.

#### I.1.2.3. Algorithmes retenus : Isolation Forest, Random Forest et XGBoost

**Détection d'anomalies par Isolation Forest**

L'Isolation Forest (Liu et al., 2008, 2012) est un algorithme non supervisé spécifiquement conçu pour la détection d'anomalies. Contrairement aux méthodes traditionnelles qui construisent un profil de la normalité puis identifient les déviations, l'Isolation Forest isole directement les anomalies en exploitant leur rareté et leur différence.

Le principe repose sur l'idée que les anomalies sont plus faciles à isoler que les points normaux. L'algorithme construit une forêt d'arbres de décision aléatoires (Isolation Trees) et partitionne récursivement les données jusqu'à ce que chaque observation soit isolée. Les anomalies, étant rares et différentes, nécessitent moins de partitions et apparaissent à des profondeurs plus faibles.

**Random Forest pour la classification**

Le Random Forest (Breiman, 2001) est un algorithme d'ensemble learning supervisé qui construit une multitude d'arbres de décision et agrège leurs prédictions. Chaque arbre est entraîné sur un échantillon bootstrap, et à chaque nœud, un sous-ensemble aléatoire de caractéristiques est considéré pour la division.

**XGBoost : standard industriel actuel**

XGBoost (eXtreme Gradient Boosting), introduit par Chen & Guestrin (2016), est un algorithme d'ensemble learning supervisé basé sur le gradient boosting. Il construit séquentiellement une série d'arbres de décision, chaque nouvel arbre corrigeant les erreurs des arbres précédents.

Ses avantages clés pour la détection de fraude incluent la gestion avancée des données déséquilibrées via le paramètre scale_pos_weight, une régularisation intégrée (L1 et L2), une gestion native des valeurs manquantes, et une capacité à capturer des interactions complexes entre variables.

Des travaux récents confirment l'efficacité de XGBoost en contexte bancaire réel. Facci et al. (2024) proposent une approche couplant un réseau de neurones de graphe (GraphSAGE) à XGBoost ou Random Forest. Chergui et al. (2022) confirment que les arbres de décision boostés atteignent jusqu'à 90 % de fiabilité.

**Tableau 1.2 — Comparaison des algorithmes de Machine Learning retenus**

| Caractéristique | Isolation Forest | Random Forest | XGBoost |
|-----------------|------------------|---------------|---------|
| Type | Non supervisé | Supervisé (ensemble) | Supervisé (boosting) |
| Paradigme | Détection d'anomalies | Classification | Classification |
| Données labellisées | Non requis | Requis | Requis |
| Gestion déséquilibre | Naturelle | Via class_weight | Via scale_pos_weight |
| Interprétabilité | Faible | Moyenne (feature importance) | Moyenne (+ SHAP) |
| Temps d'entraînement | Rapide | Modéré | Modéré |
| Performance sur données déséquilibrées | Bonne (anomalies évidentes) | Bonne | Excellente |

#### I.1.2.4. Rééquilibrage des données : SMOTE et alternatives

SMOTE (Synthetic Minority Oversampling Technique), proposé par Chawla et al. (2002), est une technique de rééquilibrage synthétique. Pour chaque observation de la classe minoritaire, on identifie ses k plus proches voisins, puis on crée un nouvel exemple synthétique en interpolant entre l'observation et l'un de ses voisins. Cette approche génère des exemples réalistes qui enrichissent l'espace des caractéristiques sans tomber dans la duplication pure.

### I.1.3. L'explicabilité (XAI) des modèles d'IA dans la finance

#### I.1.3.1. Pourquoi expliquer les décisions algorithmiques ?

L'explicabilité des modèles d'IA (XAI) est devenue un enjeu central du déploiement des systèmes intelligents dans le secteur bancaire. Plusieurs facteurs expliquent cette importance croissante :

- **Exigences réglementaires** : les régulateurs (BCEAO, UEMOA, GDPR) exigent que les décisions automatisées puissent être expliquées et justifiées.
- **Confiance des analystes** : les gestionnaires de risques doivent comprendre pourquoi une transaction a été marquée comme suspecte.
- **Auditabilité** : les décisions doivent pouvoir être tracées et vérifiées a posteriori.
- **Amélioration continue** : la compréhension des erreurs du modèle permet d'orienter les efforts d'amélioration.

#### I.1.3.2. Les principales approches de XAI

La littérature distingue plusieurs familles de méthodes d'explicabilité. Les méthodes intrinsèques exploitent la structure même du modèle mais restent limitées face aux modèles d'ensemble complexes. Les méthodes post-hoc, appliquées après l'entraînement, permettent d'expliquer n'importe quel modèle ; parmi elles, LIME approxime localement le comportement du modèle, tandis que SHAP, fondé sur la théorie des jeux, offre des garanties mathématiques de cohérence plus fortes.

#### I.1.3.3. SHAP (SHapley Additive exPlanations) comme outil d'interprétation des modèles de fraude

SHAP, développé par Lundberg & Lee (2017), est une méthode d'explicabilité basée sur la théorie des jeux coopératifs. Elle attribue à chaque caractéristique une valeur d'importance (SHAP value) qui représente sa contribution à la décision du modèle pour une prédiction donnée.

**TreeExplainer pour XGBoost :** Pour les modèles arborescents comme XGBoost, SHAP propose une implémentation optimisée appelée TreeExplainer (Lundberg et al., 2020), qui calcule exactement les valeurs SHAP en parcourant les arbres, rendant son usage praticable à l'échelle d'un système de production.

#### I.1.3.4. XAI et adoption par les analystes financiers

L'application de SHAP à la détection de fraude présente trois avantages majeurs :
1. **Explication individuelle** : pour chaque transaction, SHAP identifie les variables qui ont poussé le modèle vers une prédiction de fraude ou de normalité.
2. **Vision globale** : l'agrégation des valeurs SHAP permet d'identifier les variables les plus importantes pour le modèle.
3. **Conformité réglementaire** : les explications SHAP fournissent une traçabilité transparente des décisions.

### I.1.4. Cadre légal et réglementaire

#### I.1.4.1. Réglementation bancaire BCEAO/UEMOA

La BCEAO et l'UEMOA ont émis plusieurs directives encadrant les activités bancaires et les systèmes de paiement :
- La Directive N°01/2018/CM/UEMOA relative aux systèmes de paiement
- La Loi Uniforme sur la Lutte contre le Blanchiment de Capitaux et le Financement du Terrorisme (LBC/FT)
- Le Règlement N°01/2020/CM/UEMOA sur les services de paiement mobile

#### I.1.4.2. Dispositifs LBC/FT et rôle du GIABA

Le GIABA est l'organe régional de lutte contre le blanchiment de capitaux. Ses recommandations imposent aux institutions financières :
- La mise en œuvre de procédures KYC rigoureuses
- La déclaration des opérations suspectes
- La conservation des données transactionnelles pour 10 ans
- L'évaluation périodique des risques

#### I.1.4.3. Protection des données personnelles au Togo

Le Togo s'est doté d'une loi sur la protection des données à caractère personnel (Loi N°2020-003 du 20 février 2020), alignée sur le RGPD européen, qui impose notamment le consentement préalable, la limitation de la collecte, et la sécurisation des données.

#### I.1.4.4. Exigences de conformité pour les systèmes de détection automatisée

Au-delà du cadre sectoriel propre à l'UEMOA, les banques opèrent désormais dans un cadre réglementaire international dense où chaque modèle doit être explicable, auditable et conforme. L'AI Act européen constitue un cadre de référence préfigurant les standards internationaux vers lesquels les régulateurs régionaux tendent à converger.

## I.2. Historique et évolution du domaine

### I.2.1. Évolution des fraudes financières

#### I.2.1.1. De la fraude traditionnelle à la fraude numérique

La fraude bancaire a longtemps été dominée par des formes physiques et documentaires — falsification de chèques, contrefaçon de cartes, usurpation d'identité. Bolton & Hand (2002) décrivent cette période comme caractérisée par des mécanismes de contrôle essentiellement rétrospectifs. La numérisation des services financiers à partir des années 2000 a déplacé le centre de gravité vers des vecteurs électroniques, comme le documentent Bhattacharyya et al. (2011) et Dal Pozzolo et al. (2014, 2015).

#### I.2.1.2. Montée du mobile money en Afrique de l'Ouest

En Afrique de l'Ouest, l'essor du mobile money a permis un saut d'étape technologique en offrant des services financiers à des populations largement non bancarisées. Selon la BCEAO (2024), le Togo affichait fin 2024 le taux de comptes actifs le plus élevé de l'espace UEMOA (48,35 %) ainsi que la plus forte progression annuelle (+76,87 %).

#### I.2.1.3. Transformation des schémas frauduleux avec le numérique

Le passage au mobile money a transformé la nature des schémas frauduleux. Au Togo, les alertes de l'ANCY et du CERT-TG (2025) montrent un basculement vers des schémas d'ingénierie sociale, contrastant avec la prédominance du SIM-swap au Nigeria.

### I.2.2. Évolution des approches de détection

#### I.2.2.1. Règles métier et systèmes experts

Historiquement, la détection de fraude s'est appuyée sur des systèmes experts fondés sur des règles métier codifiées manuellement. Bolton & Hand (2002) situent l'apparition de ces systèmes dès les débuts de l'informatisation bancaire.

#### I.2.2.2. Statistiques et modèles classiques

Une deuxième génération a introduit des méthodes statistiques plus sophistiquées — régression logistique, analyse discriminante — permettant de pondérer statistiquement plusieurs facteurs de risque simultanément.

#### I.2.2.3. Machine Learning et Deep Learning

À partir des années 2010, l'essor du Machine Learning a marqué un changement d'échelle. Liu et al. (2008, 2012) introduisent l'Isolation Forest ; Breiman (2001) pose les bases du Random Forest ; Chen & Guestrin (2016) formalisent XGBoost. Le deep learning, avec le LSTM (Hochreiter & Schmidhuber, 1997), constitue une perspective de prolongement pour cette étude mais n'a pas été implémenté.

#### I.2.2.4. Approches hybrides et explicables

La dernière évolution du domaine, dans laquelle s'inscrit cette étude, consiste à combiner plusieurs paradigmes algorithmiques au sein d'approches comparatives tout en intégrant un module d'explicabilité (XAI). Lundberg & Lee (2017) posent les fondements théoriques de cette génération avec SHAP.

## I.3. Études antérieures et lacunes

### I.3.1. Travaux sur la fraude bancaire en Afrique et dans le monde

La littérature internationale documente l'application du ML à la détection de fraude bancaire sur des données de cartes bancaires occidentales (Bhattacharyya et al., 2011 ; Dal Pozzolo et al., 2014, 2015). Plus récemment, des travaux ont commencé à émerger dans des contextes africains.

### I.3.2. Travaux sur la fraude mobile money en Afrique de l'Ouest

Les études existantes montrent une hétérogénéité méthodologique et une divergence de typologies selon les pays. Au Nigeria, le SIM-swap prédomine (Adekunle et al., 2025), tandis qu'au Togo, l'ingénierie sociale est dominante.

### I.3.3. Travaux sur l'explicabilité des modèles de détection

Les travaux empiriques évaluant l'impact de l'explicabilité sur l'adoption des systèmes de détection par des professionnels bancaires africains restent peu nombreux. Aucune étude n'a évalué cet impact dans un contexte africain — une lacune que cette étude vise à combler.

### I.3.4. Limites de la littérature existante

1. **Absence d'étude sur le Togo** : aucune étude scientifique publiée ne porte sur le Togo.
2. **Modèles conçus pour les transactions par carte occidentales** : sans intégration du mobile money ouest-africain.
3. **Manque de validation empirique de l'explicabilité en contexte africain**.
4. **Rareté des architectures logicielles complètes** intégrant contrôle d'accès, explicabilité et contraintes réglementaires régionales.

### I.3.5. Positionnement de la présente étude

Cette recherche se positionne à l'intersection de ces quatre lacunes. Elle propose une approche comparative de trois algorithmes — Isolation Forest, Random Forest et XGBoost — associée à une explicabilité par SHAP, conçue pour le contexte d'une banque du Groupe Sunu au Togo.

## Conclusion du chapitre

Ce premier chapitre a établi les fondements théoriques, historiques et bibliographiques de la présente étude. Le cadre théorique a montré que la fraude mobile money au Togo présente des caractéristiques spécifiques marquées par la prédominance de l'ingénierie sociale. Le Machine Learning, et particulièrement l'approche comparative combinant Isolation Forest, Random Forest et XGBoost enrichie par SMOTE et SHAP, offre des solutions performantes et transparentes. La revue des études a permis d'identifier les lacunes que cette étude entend combler, au premier rang desquelles l'absence d'étude spécifique au contexte togolais.

---

# CHAPITRE II : MÉTHODOLOGIE DE L'ÉTUDE

## Introduction du chapitre

Ce deuxième chapitre expose la méthodologie employée pour répondre aux questions de recherche formulées dans l'introduction générale et vérifier les hypothèses qui en découlent. Après avoir précisé la nature de l'étude et défini les variables mobilisées, nous présentons la population et l'échantillon retenus, l'approche méthodologique d'ensemble learning enrichie par l'explicabilité (XAI), ainsi que les outils de collecte, d'analyse et de développement utilisés.

## 2.1. Nature de l'étude

La présente étude s'inscrit dans une démarche prospective à approche quantitative, de type non expérimental à visée explicative. Elle s'inscrit dans une logique de recherche en sciences sociales telle que décrite par Quivy & Van Campenhoudt (2006).

L'approche quantitative repose sur l'entraînement et l'évaluation comparative de trois algorithmes de Machine Learning (Isolation Forest, Random Forest, XGBoost) sur un jeu de données de transactions financières. Les performances sont mesurées à l'aide de métriques objectives (F1-Score, Recall, AUC-PR).

Un volet qualitatif est proposé en perspective pour confronter les résultats aux perceptions du terrain.

## 2.2. Variables de l'étude

### 2.2.1. Définition conceptuelle des variables

**Variables indépendantes (VI) :**
- Types de transactions : transactions bancaires classiques et transactions mobile money
- Comportements utilisateurs : fréquence des transactions, montants, canaux utilisés
- Données contextuelles locales : spécificités du marché togolais

**Variables dépendantes (VD) :**
- Taux de détection de fraude : mesuré par le F1-Score, le Recall et l'AUC-PR
- Taux de faux positifs : proportion de transactions légitimes classées à tort comme frauduleuses
- Temps de traitement : latence de détection par transaction

**Variable modératrice :**
- Interprétabilité des modèles : mesurée via les scores SHAP

### 2.2.2. Limites et difficultés rencontrées

1. **Indisponibilité des données bancaires togolaises réelles**
2. **Fort déséquilibre des classes** (3,5 % de fraude dans IEEE-CIS)
3. **Ressources techniques limitées** (pas de GPU dédié)
4. **Accès restreint aux statistiques sectorielles**

### 2.2.3. Opérationnalisation des variables et indicateurs

**Tableau 2.1 — Opérationnalisation des variables**

| Variable | Indicateur | Source de données | Unité de mesure |
|----------|------------|-------------------|-----------------|
| Types de transactions | Montant, canal, temporalité | IEEE-CIS | USD, catégories |
| Comportements utilisateurs | Fréquence, intervalle | IEEE-CIS | Nombre, secondes |
| Performance de détection | F1-Score, Recall, AUC-PR | Résultats des modèles | Score [0-1] |
| Taux de faux positifs | FP / (FP + TN) | Matrice de confusion | Pourcentage |
| Latence de détection | Temps CPU par prédiction | Benchmark Python | Millisecondes |
| Interprétabilité | Score SHAP moyen, top-K variables | Analyse SHAP | Valeur Shapley |

### 2.2.4. Dynamique anticipée des variables

**Tableau 2.2 — Dynamique anticipée des variables et seuils de confirmation des hypothèses**

| Hypothèse | Variable indépendante | Variable dépendante | Dynamique anticipée | Seuil de confirmation | Seuil d'infirmation |
|-----------|----------------------|---------------------|---------------------|----------------------|---------------------|
| HG | Comparaison IF / RF / XGBoost | F1-Score, Recall, AUC-PR | XGBoost surpasse les deux autres | XGBoost F1 ≥ 0,60 et Recall ≥ 0,60 | XGBoost F1 < 0,40 ou IF > XGBoost |
| HS1 | Modèles ML | Recall, correspondance SHAP/littérature | Recall ≥ 85 %, top-10 SHAP aligné | Recall ≥ 0,60 et ≥ 7/10 variables concordantes | Recall < 0,70 ou < 4/10 variables concordantes |
| HS2 | Plateforme RBAC sécurisée | Conformité, adoption perçue | Faisabilité technique démontrée (RBAC implémenté) ; impact sur l'adoption non mesurable sans déploiement réel | Architecture RBAC fonctionnelle dans la PoC | Architecture RBAC non fonctionnelle dans la PoC |
| HS3 | Module SHAP | Taux de FP, utilité perçue | Baisse du FP visible via ajustement du seuil | FP ≤ 2 % | FP > 5 % |

## 2.3. Population et échantillon

### 2.3.1. Population cible

La population cible est constituée de l'ensemble des transactions bancaires et mobile money effectuées au Togo entre 2019 et 2025. Faute de données réelles togolaises accessibles, un jeu de données international est utilisé comme proxy.

### 2.3.2. Échantillon quantitatif

- **Dataset principal : IEEE-CIS Fraud Detection (Kaggle, 2020)** — ~590 000 transactions, 3,5 % frauduleuses
- **Dataset secondaire : Credit Card Fraud Dataset (ULB)** — ~284 807 transactions, 0,17 % frauduleuses

**Tableau 2.3 — Caractéristiques des datasets retenus**

| Caractéristique | IEEE-CIS | Credit Card Fraud (ULB) |
|-----------------|----------|------------------------|
| Nombre de transactions | ~590 000 | ~284 807 |
| Taux de fraude | 3,5 % | 0,17 % |
| Nombre de variables | ~400 | 30 (PCA) |
| Période | 2019-2020 | 2013 |
| Origine | États-Unis/Europe | Europe |
| Type | Cartes, virements | Cartes de crédit |

### 2.3.3. Échantillon qualitatif (perspective)

Un volet qualitatif est proposé en perspective, ciblant 5 à 8 responsables d'institutions bancaires et d'opérateurs de mobile money basés à Lomé.

## 2.4. Approche méthodologique retenue : comparaison de modèles d'ensemble learning + XAI

L'approche choisie consiste en une évaluation comparative de trois algorithmes complémentaires — Isolation Forest (non supervisé), Random Forest et XGBoost (supervisés) — associée à un module d'explicabilité SHAP.

### 2.4.1. Architecture comparative

**Tableau 2.4 — Modèles évalués**

| Modèle | Type | Paradigme | Rôle dans l'étude |
|--------|------|-----------|-------------------|
| Isolation Forest | Détection d'anomalies | Non supervisé | Référence de base |
| Random Forest | Classification | Supervisé (ensemble) | Référence comparative (bagging) |
| XGBoost | Classification | Supervisé (boosting) | Modèle principal — standard industriel |

**Isolation Forest :** Paramètres : n_estimators=100, contamination=0,05, max_samples=256.

**Random Forest :** Algorithme d'ensemble learning supervisé par agrégation d'arbres indépendants.

**XGBoost :** Hyperparamètres après optimisation (Optuna, 30 essais, 3-folds CV) :
- Learning rate : 0,199
- Max depth : 7
- Subsample : 0,772
- Colsample by tree : 0,95
- Scale pos weight : ratio non-fraude/fraude

**Extension séquentielle (LSTM) — perspective :** Le LSTM (Hochreiter & Schmidhuber, 1997) est proposé comme perspective de recherche, n'ayant pas été implémenté dans cette étude en raison de contraintes de ressources de calcul.

### 2.4.2. Stratégie de gestion du déséquilibre des classes

Protocole SMOTE : Split Train/Test stratifié (80/20), SMOTE uniquement sur l'entraînement, ratio de sur-échantillonnage 0,5, k=5.

**Tableau 2.5 — Distribution des classes avant et après SMOTE**

| Étape | Non-fraude | Fraude | Ratio |
|-------|------------|--------|-------|
| Données brutes | 96,5 % | 3,5 % | 27:1 |
| Après SMOTE (train) | 66,7 % | 33,3 % | 2:1 |

### 2.4.3. Explicabilité par SHAP

Protocole : calcul des valeurs Shapley sur 500 transactions, génération du graphique d'importance globale (top 20), génération d'explications individuelles (force plot), intégration dans le dashboard.

### 2.4.4. Volet qualitatif — perspective

Un volet qualitatif est proposé en perspective pour valider la transférabilité des variables et des seuils du modèle IEEE-CIS au contexte togolais, et identifier les besoins spécifiques non couverts.

### 2.4.5. Volet quantitatif complémentaire — questionnaire TAM

Pour compléter le dispositif méthodologique et enrichir la validation des hypothèses HS2 et HS3, un questionnaire quantitatif basé sur le Technology Acceptance Model (TAM) — cadre théorique validé pour mesurer l'adoption des systèmes d'information (Davis, 1989) — est proposé. Cet outil vise à recueillir les perceptions de professionnels bancaires togolais sur l'utilité perçue, la facilité d'utilisation perçue, la confiance et l'intention d'adoption du système FRAUDX.

Le questionnaire (Annexe B) comprend 20 items mesurés sur une échelle de Likert à 5 niveaux, répartis en cinq construits :

- **Utilité perçue** (4 items) : capacité du système à améliorer la détection de fraude
- **Facilité d'utilisation perçue** (4 items) : compréhensibilité et accessibilité du système
- **Confiance** (4 items) : fiabilité et transparence des décisions algorithmiques
- **Intention d'adoption** (4 items) : volonté d'utiliser et de recommander le système
- **Facteurs contextuels** (4 items) : contraintes infrastructurelles et organisationnelles

Les résultats de ce questionnaire, combinés à l'analyse quantitative des performances du modèle et aux entretiens qualitatifs (perspective), permettraient une validation croisée des hypothèses selon une approche mixte complète.

### 2.4.6. Métriques d'évaluation

**Tableau 2.6 — Métriques d'évaluation retenues**

| Métrique | Formule | Justification | Cible |
|----------|---------|---------------|-------|
| F1-Score | 2 × (P × R) / (P + R) | Équilibre précision/rappel | ≥ 0,60 |
| Recall | TP / (TP + FN) | Priorité : détecter un maximum de fraudes | ≥ 0,60 |
| AUC-PR | Aire sous courbe PR | Pertinent pour classes déséquilibrées | ≥ 0,55 |
| Précision | TP / (TP + FP) | Limiter les faux positifs | ≥ 0,10 |
| Temps de latence | — | Contrainte temps réel | < 100 ms |

## 2.5. Outils de l'étude

### 2.5.1. Environnement de développement

Python 3.10, Scikit-learn 1.2, XGBoost 1.7, Pandas 1.5, NumPy 1.23, SHAP 0.41, Imbalanced-learn 0.10, Optuna, Google Colab, Jupyter Notebook.

### 2.5.2. Pipeline de prétraitement

1. Nettoyage (imputation médiane/mode, suppression des variables avec > 90 % de valeurs manquantes)
2. Encodage (One-Hot Encoding, frequency encoding)
3. Normalisation (StandardScaler)
4. Feature engineering (log_amount, hour, dayofweek, tx_count_by_card1)
5. Split Train/Test stratifié (80/20)
6. Rééquilibrage (SMOTE)

### 2.5.3. Procédure d'entraînement et de validation

1. Recherche d'hyperparamètres (Optuna, 3-folds CV)
2. Entraînement sur l'ensemble rééquilibré
3. Prédiction sur l'ensemble de test (non rééquilibré)
4. Évaluation (F1, Recall, AUC-PR, Précision, Matrice de confusion)
5. Interprétation (SHAP)

## 2.6. Stratégie de vérification des hypothèses

**Tableau 2.7 — Stratégie de vérification des hypothèses**

| Hypothèse | Données | Méthode | Indicateurs | Validation |
|-----------|---------|---------|-------------|------------|
| HG — L'ensemble learning améliore la détection | IEEE-CIS | Comparaison IF / RF / XGBoost | F1, Recall, AUC-PR | Si XGBoost ≥ RF ≥ IF |
| HS1 — Les modèles ML identifient des patterns pertinents | IEEE-CIS | Analyse SHAP, top variables | Top 10 variables SHAP | Si variables SHAP correspondent aux typologies documentées |
| HS2 — Plateforme RBAC sécurisée | Architecture PoC | RBAC implémenté | Faisabilité technique | Si RBAC fonctionnel dans la PoC | Si RBAC non fonctionnel dans la PoC |
| HS3 — L'explicabilité SHAP facilite l'adoption | SHAP, analyse des FP | Ajustement du seuil | Taux de FP | Si FP ≤ 2 % après optimisation |

## Conclusion du chapitre

Ce deuxième chapitre a présenté la méthodologie retenue pour répondre aux questions de recherche et vérifier les hypothèses. L'approche quantitative combinant une analyse comparative de trois algorithmes, des métriques adaptées au déséquilibre des classes et une validation croisée permet une évaluation rigoureuse. Les choix méthodologiques — recours à un dataset international comme proxy, SMOTE, approche comparative, SHAP — sont cohérents avec l'état de l'art et les contraintes du contexte togolais.

---

# CHAPITRE III : PRÉSENTATION DE LA SITUATION ET COLLECTE DES DONNÉES

## Introduction

Ce troisième chapitre présente les données utilisées et l'analyse exploratoire, les performances comparatives des modèles, et la proposition de plateforme FRAUDX. Le cadre conceptuel de l'étude inclut les transactions bancaires classiques et le mobile money ; le modèle est entraîné sur le jeu de données international IEEE-CIS (transactions par carte) faute de données réelles togolaises accessibles — une limite explicitement reconnue.

## 3.1. Présentation et analyse exploratoire des données

### 3.1.1. Description du dataset retenu

Le dataset principal retenu est IEEE-CIS Fraud Detection (Kaggle, 2020), comprenant environ 590 000 transactions étiquetées.

Caractéristiques principales :
- Volume : 590 540 transactions
- Variables : ~400 (dont ~250 anonymisées par PCA, ~150 explicites)
- Taux de fraude : 3,5 % (20 669 transactions frauduleuses)
- Période : 2019-2020

### 3.1.2. Analyse exploratoire (EDA)

**Distribution des classes :**
- Non frauduleuses : 569 871 (96,5 %)
- Frauduleuses : 20 669 (3,5 %)
- Ratio : ~27:1

**Analyse univariée :** Les fraudes tendent à se concentrer sur des montants modérés (50-200 USD).

**Analyse temporelle :** Les fraudes sont plus fréquentes en fin de semaine et aux heures de faible activité.

### 3.1.3. Prétraitement des données

1. Nettoyage : imputation médiane/mode, suppression des variables avec > 90 % de valeurs manquantes (18 variables supprimées)
2. Encodage : One-Hot Encoding + frequency encoding
3. Normalisation : StandardScaler
4. Feature engineering : log_amount, hour, dayofweek, tx_count_by_card1, avg_amount_by_card1
5. Split : 472 432 train / 118 108 test
6. Rééquilibrage : SMOTE (ratio 0,5)

### 3.1.4. Discussion sur la transférabilité au contexte togolais

**Variables présentes et transférables :** montant, temporalité, fréquence, caractéristiques du dispositif.

**Variables manquantes spécifiques au Togo :** canal USSD vs application, identifiant agent mobile money, type d'opération (cash-in/out), zone géographique rurale/urbaine, ancienneté du compte.

## 3.2. Conception et évaluation des modèles de Machine Learning

### 3.2.1. Configuration expérimentale

Environnement : Machine locale (CPU, RAM 16 Go), Python 3.10, Scikit-learn, XGBoost, Imbalanced-learn, Optuna.

### 3.2.2. Résultats de l'évaluation comparative

**Tableau 3.1 — Performances comparatives des modèles sur le dataset IEEE-CIS**

| Modèle | F1-Score | Recall | AUC-PR | Précision | Temps d'entraînement |
|--------|----------|--------|--------|-----------|---------------------|
| Isolation Forest | 0,16 | 0,16 | 0,09 | 0,16 | 11,9 s |
| Random Forest | 0,37 | 0,57 | 0,49 | 0,28 | 254,1 s |
| XGBoost (seuil 0.5) | 0,61 | 0,47 | 0,66 | 0,87 | 325,6 s |
| XGBoost (seuil 0.35) | 0,23 | 0,85 | 0,57 | 0,14 | 325,6 s |

Note : Les résultats de XGBoost sont présentés pour les deux configurations de seuil afin de montrer le compromis Recall/Précision.

**Analyse des résultats :**
- XGBoost (seuil 0.5) : F1-Score de 0,61, AUC-PR de 0,66 ; XGBoost (seuil 0.35) : Recall de 85 %, AUC-PR de 0,57
- Random Forest : F1-Score de 0,37 avec un Recall de 0,57, ne permettant pas d'atteindre la cible
- Isolation Forest : Performances limitées (F1 = 0,16), sert de référence de base

**Tableau 3.2 — Matrice de confusion (XGBoost, seuil optimisé)**

| | Prédit : Non Fraude | Prédit : Fraude |
|--|---------------------|-----------------|
| Réel : Non Fraude | 86 101 (VN) | 22 438 (FP) |
| Réel : Fraude | 619 (FN) | 3 514 (VP) |

Soit :
- Taux de faux positifs : 20,7 %
- Recall : 85,02 %

### 3.2.3. Explicabilité des modèles par SHAP

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

## 3.3. Proposition de plateforme : FRAUDX (preuve de concept)

### 3.3.1. Architecture technique cible

| Couche | Composants | Fonction |
|--------|------------|----------|
| Sécurité | WAF, authentification RBAC, chiffrement TLS | Protection périmétrique |
| Client | Dashboard Streamlit, interface SHAP | Interface utilisateur |
| API | API REST FastAPI, endpoints /predict, /explain, /feedback | Point d'entrée |
| Pipeline ML | Prétraitement, XGBoost, SHAP | Traitement et prédiction |
| Stockage | SQLite, logs d'audit | Persistance des données |

### 3.3.2. Contrôle d'accès basé sur les rôles (RBAC)

**Tableau 3.3 — Matrice des rôles et permissions FRAUDX**

| Fonctionnalité | Analyste | Gestionnaire de Risques | Administrateur |
|----------------|----------|------------------------|----------------|
| Dashboard (alertes) | Lecture | Lecture | Lecture |
| Détail des transactions | Lecture | Lecture | Lecture |
| Explications SHAP | Lecture | Lecture | Lecture |
| Feedback | Écriture | Écriture | Écriture |
| Benchmark (métriques) | — | Lecture | Lecture |
| Configuration (seuils) | — | Écriture | Écriture |
| Gestion des utilisateurs | — | — | Écriture |
| Réentraînement des modèles | — | — | Exécution |

### 3.3.3. Fonctionnalités du tableau de bord

- Page d'accueil : cartes KPI, graphique d'évolution temporelle, dernières alertes
- Transactions : liste paginée avec filtres, détail avec explications SHAP
- Benchmark : tableau comparatif des performances
- Explicabilité SHAP : importance globale, waterfall plots individuels
- Feedback : validation/infirmation des alertes

### 3.3.4. Module de feedback et apprentissage continu

Le module de feedback permet aux analystes de valider ou infirmer chaque alerte, permettant l'amélioration du modèle par réentraînement périodique.

## 3.4. Tests et validation

### 3.4.1. Optimisation par recherche d'hyperparamètres

Optuna, 30 essais, 3-folds CV.

**Meilleure configuration :**

| Hyperparamètre | Valeur optimale |
|----------------|-----------------|
| n_estimators | 288 |
| max_depth | 7 |
| learning_rate | 0,199 |
| subsample | 0,772 |
| colsample_bytree | 0,950 |
| scale_pos_weight | ratio non-fraude/fraude |

**Performances avant et après optimisation :**

| Configuration | F1-Score | Recall | AUC-PR |
|---------------|----------|--------|--------|
| Seuil 0.5 | 0,61 | 0,47 | 0,66 |
| Seuil 0.35 | 0,23 | 0,85 | 0,57 |

Note : Le seuil 0.5 maximise le F1-Score (0,61) mais limite le Recall (47 %). Le seuil 0,35 privilégie le Recall (85 %) au détriment du F1-Score. Ce compromis est assumé : il est préférable de générer des faux positifs vérifiables par un analyste que de laisser passer une fraude non détectée.

**Top 5 des variables SHAP après optimisation :**
1. TransactionAmt (montant)
2. card6_credit (type de carte : crédit)
3. dayofweek (jour de la semaine)
4. log_amount (montant logarithmique)
5. tx_count_by_card1 (nombre de transactions par carte)

### 3.4.2. Vérification des hypothèses (résultats)

**Hypothèse HG partiellement validée :** XGBoost atteint un Recall de 85 %, surpassant significativement Random Forest (F1=0,37) et Isolation Forest (F1=0,16). Le seuil de confirmation (F1 ≥ 0,60 et Recall ≥ 0,60) est partiellement atteint (Recall satisfait, F1 de 0,23 au seuil 0,35).

**Hypothèse HS1 validée :** Les variables identifiées par SHAP (montant, type de carte, temporalité) correspondent aux facteurs de fraude documentés dans la littérature (Bhattacharyya et al., 2011 ; Dal Pozzolo et al., 2014).

**Hypothèse HS3 non validée :** L'ajustement du seuil de décision (de 0,5 à 0,35) via la courbe Precision-Recall permet d'atteindre un Recall de 85 %, mais le F1-Score chute à 0,23. Le taux de faux positifs (20,7 %) reste très au-dessus de la cible de 2 %, indiquant que l'explicabilité SHAP seule ne suffit pas à réduire les FP au niveau souhaité sans sacrifier le Recall.

## Conclusion du chapitre

Ce troisième chapitre a présenté l'analyse exploratoire du dataset IEEE-CIS, confirmant la structure déséquilibrée des données (3,5 % de fraude). L'évaluation comparative des modèles a démontré la supériorité de XGBoost (Recall = 85,02 % ; AUC-PR = 0,57) sur Random Forest et Isolation Forest. La proposition de plateforme FRAUDX — preuve de concept fonctionnelle avec contrôle d'accès RBAC, dashboard interactif et module d'explicabilité SHAP — démontre la faisabilité technique du déploiement.

---

# CHAPITRE IV : ANALYSE-DIAGNOSTIC ET PROPOSITION D'INTERVENTION

## Introduction du chapitre

Ce quatrième et dernier chapitre exploite les résultats expérimentaux du Chapitre III pour établir un diagnostic de la situation existante, vérifier les hypothèses de recherche formulées dans l'introduction, et proposer une intervention concrète et contextualisée. L'intervention proposée — le système FRAUDX, dont la preuve de concept a été présentée au Chapitre III — est ici justifiée, détaillée et évaluée sous ses dimensions techniques, économiques, sociales et réglementaires.

## 4.1. Analyse diagnostique

### 4.1.1. Forces et faiblesses du système actuel

L'analyse des dispositifs de détection de fraude existants dans les banques togolaises, enrichie par l'étude documentaire et les entretiens exploratoires (perspective), peut être synthétisée sous forme d'analyse SWOT :

**Tableau 4.1 — Analyse SWOT des dispositifs actuels de détection de fraude au Togo**

| | Forces (S) | Faiblesses (W) |
|--|------------|----------------|
| Interne | S1 — Connaissance fine des clients (KYC) | W1 — Règles de détection statiques et obsolètes |
| | S2 — Existence de cellules conformité AML | W2 — Faible couverture des fraudes mobile money |
| | S3 — Exigences réglementaires BCEAO/UEMOA | W3 — Analyse manuelle non scalable |
| | | W4 — Délais de détection trop longs |
| | | W5 — Taux de faux positifs élevé |

| | Opportunités (O) | Menaces (T) |
|--|------------------|-------------|
| Externe | O1 — Digitalisation rapide du secteur financier | T1 — Sophistication croissante des schémas de fraude |
| | O2 — Disponibilité de datasets publics de référence | T2 — SIM swap et fraude USSD en hausse |
| | O3 — Outils open source de ML matures | T3 — Ingénierie sociale sur agents mobile money |
| | O4 — Soutien des régulateurs à l'innovation | T4 — Contraintes infrastructurelles |

### 4.1.2. Gaps identifiés

1. **Gap technologique** : les systèmes actuels (règles statiques, Excel, requêtes SQL) sont dépassés. Aucune banque togolaise n'a déployé, à notre connaissance, un système de détection basé sur du ML supervisé en production.

2. **Gap mobile money** : les fraudes SIM swap et USSD ne sont pas couvertes par les systèmes de détection conçus pour les transactions bancaires classiques.

3. **Gap explicabilité** : les systèmes de ML sont perçus comme des "boîtes noires", freinant leur adoption.

4. **Gap données** : l'absence de données locales labellisées empêche l'entraînement de modèles spécifiques au contexte togolais.

### 4.1.3. Vérification des hypothèses

#### HG — Hypothèse générale

*L'intégration d'un système de Machine Learning basé sur une approche d'ensemble (Ensemble Learning) améliore significativement la détection de la fraude bancaire au Togo, en offrant un niveau d'explicabilité suffisant pour répondre aux exigences réglementaires.*

**Verdict : Partiellement validée**

Les résultats du Chapitre III démontrent la supériorité de l'approche comparative : XGBoost (F1=0,61 au seuil 0.5 ; Recall=85 % au seuil 0.35 ; AUC-PR=0,57) surpasse significativement Random Forest (F1=0,37) et Isolation Forest (F1=0,16). Le seuil de confirmation (F1 ≥ 0,60 et Recall ≥ 0,60) est atteint pour la configuration seuil 0.5 (F1=0,61) mais pas simultanément pour les deux métriques au seuil 0.35 (F1=0,23). L'explicabilité SHAP est intégrée et fonctionnelle.

**Nuance** : la validation sur données togolaises réelles n'a pu être effectuée faute de dataset local accessible. La transférabilité des performances au contexte togolais reste à confirmer par une étude sur données réelles.

#### HS1 — L'automatisation par ML (notamment XGBoost) réduit significativement le taux de faux négatifs (Recall ≥ 0,60)

**Verdict : Validée**

Le Recall de 85,02 % atteint par XGBoost après optimisation dépasse le seuil de confirmation (0,60). Les 619 faux négatifs (FN) sur 4 133 transactions frauduleuses représentent 15 % de fraudes non détectées — une amélioration considérable par rapport aux méthodes traditionnelles.

#### HS2 — Une plateforme sécurisée avec RBAC favorise l'adoption du ML par les banques togolaises

**Verdict : Partiellement vérifiée**

La **faisabilité technique** de la plateforme sécurisée est démontrée : l'architecture RBAC (trois rôles : analyste, gestionnaire de risques, administrateur) est implémentée et fonctionnelle dans la preuve de concept FRAUDX, avec permissions granulaires, chiffrement TLS, hachage des mots de passe, logs d'audit et conformité aux exigences BCEAO/UEMOA.

Ce qui reste **non vérifiable** dans le cadre de ce mémoire est la **deuxième partie** de l'hypothèse : mesurer si cette plateforme "favorise l'adoption du ML par les banques togolaises". Cela nécessiterait un déploiement en environnement bancaire réel et une évaluation par des utilisateurs réels — ce qui constitue la perspective prioritaire de recherche appliquée.

#### HS3 — L'explicabilité SHAP facilite l'acceptation du système par les analystes

**Verdict : Non validée**

L'analyse SHAP permet d'identifier les variables discriminantes (montant, type de carte, temporalité) et de générer des explications individuelles pour chaque alerte. Le taux de faux positifs (20,7 %) reste toutefois très au-dessus de la cible de 2 % fixée dans la méthodologie, ce qui relativise fortement la portée de l'explicabilité seule pour réduire les FP. L'acceptation par les analystes n'a pas pu être mesurée empiriquement (absence d'entretiens réalisés).

**Tableau 4.2 — Synthèse de la vérification des hypothèses**

| Hypothèse | Verdict | Justification |
|-----------|---------|---------------|
| HG | Partiellement validée | XGBoost F1=0,61 (seuil 0.5) / Recall=0,85 (seuil 0.35) — seuil de confirmation partiellement atteint |
| HS1 | Validée | Recall=85,02 % ≥ seuil 0,60 |
| HS2 | Partiellement vérifiée | RBAC implémenté dans la PoC (faisabilité technique) ; impact sur l'adoption non mesurable sans déploiement réel |
| HS3 | Non validée | SHAP fonctionnel, FP=20,7 % >> cible 2 % |

## 4.2. Intervention proposée et justification

### 4.2.1. Présentation de l'intervention

Sur la base du diagnostic établi, nous proposons le déploiement progressif du système FRAUDX au sein d'une banque togolaise partenaire. FRAUDX est un système intégré de détection de fraude bancaire par Intelligence Artificielle, fondé sur :

1. **Une approche comparative de trois modèles** (Isolation Forest, Random Forest, XGBoost) avec sélection du meilleur modèle pour la production
2. **Un module d'explicabilité SHAP** pour la transparence des décisions
3. **Un dashboard sécurisé** avec contrôle d'accès RBAC (3 rôles)
4. **Un module de feedback humain** pour l'apprentissage continu

### 4.2.2. Justification des choix techniques

**Pourquoi une approche comparative plutôt qu'un modèle unique ?**

L'évaluation comparative de trois algorithmes permet de :
- Disposer d'une référence de base non supervisée (Isolation Forest)
- Comparer deux paradigmes supervisés complémentaires (bagging vs boosting)
- Sélectionner objectivement le modèle le plus performant (XGBoost)
- Justifier le choix auprès des parties prenantes par des métriques objectives

**Pourquoi l'explicabilité SHAP ?**

Les régulateurs BCEAO/UEMOA exigent la transparence des décisions automatisées. SHAP répond à cette exigence en fournissant :
- Une explication globale (variables les plus importantes)
- Des explications locales (facteurs ayant déclenché chaque alerte)
- Des visualisations accessibles aux non-spécialistes

**Pourquoi un déploiement progressif ?**

Le phasage en trois étapes (pilote → extension mobile money → généralisation) permet une montée en charge maîtrisée, une adaptation aux retours terrain, et une maîtrise des risques.

## 4.3. Objectifs de l'intervention

### 4.3.1. Objectif général

Déployer un système d'IA opérationnel, sécurisé et explicable pour la détection de la fraude bancaire et mobile money au Togo, avec les cibles de performance suivantes :
- Recall ≥ 90 %
- Taux de faux positifs ≤ 3 %
- Temps de réponse < 100 ms par transaction
- Top 5 variables SHAP affichées pour chaque alerte

### 4.3.2. Objectifs spécifiques

1. **OSI-1** : Adapter et réentraîner XGBoost sur des données locales (objectif : F1 ≥ 0,75)
2. **OSI-2** : Intégrer le module SHAP dans le workflow décisionnel des analystes
3. **OSI-3** : Déployer la plateforme sécurisée avec RBAC dans un environnement de production
4. **OSI-4** : Former le personnel bancaire à l'utilisation et à l'interprétation du système
5. **OSI-5** : Mettre en place un processus d'apprentissage continu par le feedback

## 4.4. Composantes de l'intervention envisagée

### 4.4.1. Module de collecte et prétraitement

**Sources de données cibles :**
- Flux de transactions bancaires (API core banking)
- Flux de transactions mobile money (API TogoCom Cash, Moov Money)
- Données de référence clients (KYC)

**Pipeline de prétraitement temps réel :**
Transaction entrante → Validation format → Nettoyage → Feature engineering (features issues de l'analyse SHAP) → Normalisation → Transmission au module de scoring

**Défis spécifiques au contexte togolais :**
- Hétérogénéité des formats entre banques et opérateurs mobile money
- Faible qualité de certaines données (champs manquants)
- Nécessité d'un mapping entre variables IEEE-CIS et variables locales

### 4.4.2. Module de détection

Le module de détection repose sur XGBoost, sélectionné comme meilleur modèle à l'issue de l'évaluation comparative :

- **Prétraitement** : application du pipeline défini (StandardScaler, feature engineering)
- **Scoring** : calcul du score de probabilité de fraude par XGBoost
- **Seuillage** : application du seuil optimal (0,35) calibré sur les données locales
- **Explication** : génération des valeurs SHAP pour chaque transaction signalée

**Intégration du feedback pour réentraînement :**
1. Le modèle génère une alerte avec explication SHAP
2. L'analyste valide ou infirme l'alerte via le dashboard
3. Le feedback est stocké dans la base de données
4. Périodiquement, le modèle est réentraîné incluant les feedbacks validés

### 4.4.3. Module d'explicabilité (XAI/SHAP)

Pour chaque alerte, le module SHAP calcule et affiche les top 5 variables ayant contribué à la décision, avec leur valeur SHAP et une explication en langage naturel.

**Exemple d'explication générée pour un analyste :**

> **Alerte FRAUDX — Transaction #TX-2025-06-4219**
> Date : 15/06/2025 à 03:14
> Montant : 250 000 FCFA
> Statut : FRAUDE PRÉSUMÉE (score : 0,89)
>
> Facteurs ayant contribué à la décision :
> 1. Montant anormalement élevé (+0,42 SHAP) — 250 000 FCFA vs moyenne client 45 000 FCFA
> 2. Heure inhabituelle (+0,31 SHAP) — transaction à 3h14, activité habituelle 8h-20h
> 3. Nouveau bénéficiaire (+0,25 SHAP) — premier transfert vers ce compte
> 4. Localisation différente (+0,18 SHAP) — transaction depuis une zone non habituelle
> 5. Intervalle court (+0,12 SHAP) — 2e transaction en moins de 5 minutes

### 4.4.4. Sécurité et gestion avancée des utilisateurs

**Authentification :**
- Connexion sécurisée par mot de passe (hachage SHA-256 côté client, bcrypt en base)
- Sessions avec token JWT (expiration 30 minutes)

**Contrôle d'accès (RBAC) :**
- Trois rôles : Analyste, Gestionnaire de Risques, Administrateur
- Permissions granulaires par fonctionnalité
- Journalisation de toutes les actions

**Protection des données :**
- Chiffrement TLS 1.3 pour les données en transit
- Pseudonymisation des données personnelles dans les logs
- Conformité avec la loi togolaise 2020-003

**Auditabilité :**
- Logs complets : qui a consulté quoi, quand, et quelle décision a été prise
- Traçabilité des décisions (version du modèle, features, score SHAP)
- Conservation des logs : 10 ans (exigence BCEAO)

## 4.5. Stratégies d'action et périmètre

### 4.5.1. Phase pilote (Mois 1-6)

**Périmètre :**
- Une banque togolaise partenaire (recommandation : SUNU Bank Togo)
- Transactions bancaires classiques uniquement
- Volume : montée en charge progressive (1 000 → 10 000 transactions/jour)

**Étapes :**

| Étape | Livrable |
|-------|----------|
| 1. Installation infrastructure | Serveurs, réseau, sécurité déployés |
| 2. Intégration API | Connexion aux flux de transactions |
| 3. Entraînement modèle local | XGBoost calibré sur données locales |
| 4. Déploiement dashboard | Dashboard accessible aux analystes |
| 5. Formation utilisateurs | Analystes formés |
| 6. Mise en production | Système opérationnel |

**Critères de succès :**
- F1-Score ≥ 0,70 sur les données locales
- Taux de faux positifs ≤ 5 %
- Taux d'utilisation du dashboard par les analystes > 80 %

### 4.5.2. Extension mobile money (Mois 7-12)

**Périmètre :**
- Intégration des flux mobile money
- Transactions USSD, cash-in/cash-out, transferts P2P
- Volume : 50 000 transactions/jour

**Adaptations :**
- Ajout des features spécifiques mobile money (canal USSD, identifiant agent, type d'opération)
- Réentraînement du modèle sur données mobile money
- Adaptation des seuils aux montants typiques du mobile money

### 4.5.3. Généralisation (Mois 13-24)

- Extension à 3-5 banques togolaises
- Extension aux opérateurs mobile money
- Mise en place d'un centre de veille fraude mutualisé
- Gouvernance du système (comité banques + régulateur)

## 4.6. Étude de faisabilité

### 4.6.1. Faisabilité technique

**Infrastructure requise (phase pilote) :**

| Composant | Spécification | Coût estimé |
|-----------|---------------|-------------|
| Serveur de calcul (ML) | 32 vCPU, 64 Go RAM | 4 000 € |
| Serveur API | 8 vCPU, 32 Go RAM | 2 000 € |
| Serveur base de données | 16 vCPU, 64 Go RAM, SSD 1 To | 3 000 € |
| Stockage (logs, données) | NAS 10 To | 1 500 € |
| Sécurité (WAF, VPN) | Licence + matériel | 2 000 € |
| **Total infrastructure** | | **12 500 €** |

**Compétences requises :**
- 1 ingénieur ML (CDI ou consultant)
- 1 développeur full-stack
- 1 administrateur système

### 4.6.2. Faisabilité économique

**Budget estimé (déploiement + 3 ans) :**

| Poste | Année 1 | Année 2 | Année 3 | Total 3 ans |
|-------|---------|---------|---------|-------------|
| Infrastructure | 12 500 € | 2 000 € | 2 000 € | 16 500 € |
| Développement ML | 30 000 € | 8 000 € | 8 000 € | 46 000 € |
| Développement dashboard | 15 000 € | 3 000 € | 3 000 € | 21 000 € |
| Formation | 10 000 € | 3 000 € | 3 000 € | 16 000 € |
| Maintenance | 5 000 € | 8 000 € | 10 000 € | 23 000 € |
| **Total** | **72 500 €** | **24 000 €** | **26 000 €** | **122 500 €** |

**ROI estimé :**
- Pertes annuelles estimées par fraude pour une banque togolaise moyenne : 300 000 € (estimation BCEAO)
- Réduction attendue : 40 % (hypothèse prudente basée sur Recall=85 % avant feedback)
- Économie annuelle : 300 000 € × 40 % = 120 000 €
- ROI sur 3 ans : (120 000 × 3 - 122 500) / 122 500 = **194 %**

### 4.6.3. Faisabilité sociale

**Acceptabilité par les agents bancaires :**
Le système FRAUDX est conçu comme un outil d'aide à la décision, non comme un système autonome. Les analystes conservent le pouvoir de validation finale.

**Mesures d'atténuation des risques :**
- Formation obligatoire (5 jours) avant le déploiement
- Phase de transition de 3 mois (affichage des alertes sans action)
- Feedback continu des utilisateurs
- Maintien d'une équipe de veille humaine parallèle

**Impact sur l'inclusion financière :**
- Renforcement de la confiance dans les services financiers numériques
- Protection des populations rurales, principales utilisatrices du mobile money
- Libération de temps pour les analystes (valeur ajoutée)

### 4.6.4. Faisabilité réglementaire

**Conformité BCEAO/UEMOA :**
- Respect de la Directive N°01/2018/CM/UEMOA sur les systèmes de paiement
- Explications SHAP répondant aux obligations de transparence
- Journalisation complète assurant l'auditabilité

**Conformité protection des données :**
- Pseudonymisation des données personnelles
- Chiffrement AES-256 au repos
- Principe de minimisation des données

**Conformité AML/KYC :**
- Intégration aux dispositifs AML/KYC existants
- Alertes formatées selon les standards de déclaration de la CNRF

## 4.7. Limites de l'étude et perspectives

### 4.7.1. Limites identifiées

1. **Absence de validation sur données togolaises réelles** : l'utilisation d'un dataset international (IEEE-CIS) comme proxy constitue la limite principale. La transférabilité des résultats reste à confirmer.

2. **Validation qualitative non réalisée** : les entretiens semi-directifs auprès de responsables de SUNU Bank n'ont pu être menés dans le cadre de ce mémoire. Le guide d'entretien et la grille d'analyse sont proposés comme outils pour une recherche ultérieure.

3. **Non-implantation du LSTM** : l'analyse temporelle par réseau de neurones récurrents n'a pu être implémentée faute de ressources GPU, limitant la capacité à capturer les dépendances séquentielles entre transactions.

4. **Coûts estimés** : le budget présenté est une estimation préliminaire. Les coûts réels dépendront des spécificités de l'environnement de déploiement.

5. **Seuil de confirmation HS3 non atteint** : le taux de faux positifs (20,7 %) dépasse très largement la cible de 2 %, indiquant que l'explicabilité SHAP seule ne résout pas entièrement le problème des faux positifs.

### 4.7.2. Perspectives de recherche

1. **Partenariat avec une banque ou un opérateur mobile money togolais** : l'obtention d'un jeu de données réel est la priorité absolue pour valider et calibrer le modèle sur le contexte local.

2. **Extension à l'espace UEMOA** : adapter et déployer le système dans d'autres pays de l'Union.

3. **Apprentissage fédéré (Federated Learning)** : permettre à plusieurs banques de partager un modèle commun sans divulguer leurs données sensibles.

4. **Détection des fraudes émergentes** : utilisation du deep learning (LSTM, Transformers) pour détecter des schémas de fraude inédits.

5. **Étude d'acceptabilité** : mener les entretiens qualitatifs et le questionnaire TAM (Annexe B) auprès des analystes et gestionnaires de risques pour valider empiriquement l'apport de l'explicabilité SHAP en contexte africain (HS2 et volet qualitatif de HS3).

### 4.7.3. Recommandations

**Aux institutions bancaires togolaises :**
- Engager une réflexion stratégique sur l'intégration du ML dans la détection de fraude
- Investir dans la collecte et la labellisation de données locales
- Former les équipes à l'utilisation des outils d'IA et d'explicabilité

**Aux opérateurs de mobile money :**
- Partager des données anonymisées pour permettre l'entraînement de modèles adaptés au canal USSD
- Renforcer les mécanismes de sécurité des transactions

**Aux régulateurs (BCEAO, UEMOA) :**
- Établir un cadre de référence pour l'utilisation de l'IA dans la détection de fraude
- Encourager le partage interbancaire des données de fraude pseudonymisées
- Financer des programmes de recherche sur l'IA bancaire en Afrique de l'Ouest

## Conclusion du chapitre

Ce quatrième chapitre a établi un diagnostic de la situation de la détection de fraude dans le secteur bancaire togolais, confirmant la pertinence d'une intervention basée sur l'IA et l'ensemble learning. Les hypothèses de recherche ont été vérifiées : HG est partiellement validée, HS1 est validée, HS3 n'est pas validée (SHAP fonctionnel mais FP=20,7 % >> cible), HS2 est partiellement vérifiée (faisabilité technique de la plateforme RBAC démontrée, impact sur l'adoption en perspective).

L'intervention proposée — le système FRAUDX — est justifiée par le diagnostic et détaillée dans ses composantes techniques (modèle XGBoost, explicabilité SHAP, RBAC), organisationnelles (formation, feedback, apprentissage continu) et stratégiques (phasage pilote → extension mobile money → généralisation). L'étude de faisabilité confirme la viabilité technique, économique (ROI estimé à 194 % sur 3 ans), sociale et réglementaire du projet.

Les limites de l'étude, notamment l'absence de validation sur données togolaises réelles et la non-réalisation des entretiens qualitatifs, sont explicitement reconnues et constituent autant de perspectives pour des travaux futurs.

---

# CONCLUSION GÉNÉRALE

## Synthèse des résultats

Cette étude avait pour objectif de concevoir un système d'intelligence artificielle performant et sécurisé pour la détection de la fraude bancaire dans le contexte spécifique du Togo. La recherche s'est structurée autour de quatre chapitres.

Le **Chapitre I** a posé les fondements théoriques et conceptuels. Nous avons montré que la fraude bancaire au Togo présente des caractéristiques spécifiques — prédominance du mobile money, émergence de schémas d'ingénierie sociale — que les systèmes traditionnels de détection ne parviennent pas à couvrir.

Le **Chapitre II** a défini la méthodologie : approche quantitative comparative de trois algorithmes (Isolation Forest, Random Forest, XGBoost) avec métriques adaptées au déséquilibre des classes (F1-Score, Recall, AUC-PR) et explicabilité SHAP.

Le **Chapitre III** a présenté les résultats expérimentaux. L'évaluation comparative a confirmé la supériorité de XGBoost après optimisation par Optuna (Recall = 85,02 % ; AUC-PR = 0,57). L'analyse SHAP a identifié TransactionAmt (montant), card6_credit (type de carte) et dayofweek comme facteurs les plus discriminants. La preuve de concept FRAUDX — dashboard Streamlit, contrôle d'accès RBAC, module SHAP — démontre la faisabilité technique.

Le **Chapitre IV** a établi le diagnostic et proposé une intervention : le déploiement progressif de FRAUDX dans une banque togolaise partenaire. L'étude de faisabilité a estimé un ROI de 194 % sur 3 ans.

## Vérification des hypothèses

| Hypothèse | Verdict | Fondement |
|-----------|---------|-----------|
| HG — L'ensemble learning améliore la détection | **Partiellement validée** | XGBoost F1=0,61 (seuil 0.5) / Recall=0,85 (seuil 0.35), surpasse RF (0,37) et IF (0,16) |
| HS1 — Le ML réduit les faux négatifs | **Validée** | Recall=85,02 % ≥ seuil 0,60 |
| HS2 — Plateforme RBAC sécurisée favorise l'adoption du ML | **Partiellement vérifiée** | RBAC implémenté (PoC fonctionnelle) ; impact adoption nécessite déploiement réel |
| HS3 — L'explicabilité SHAP facilite l'adoption | **Non validée** | SHAP fonctionnel, FP=20,7 % >> cible 2 % |

## Contributions de l'étude

**Contributions scientifiques :**
1. Première étude documentée sur l'application du ML à la détection de fraude bancaire et mobile money dans le contexte spécifique du Togo
2. Proposition d'une méthodologie comparative (Isolation Forest / Random Forest / XGBoost) adaptée aux contraintes des systèmes bancaires africains
3. Démonstration de l'apport de l'explicabilité SHAP pour la transparence des décisions
4. Identification des variables discriminantes (montant, temporalité, type de carte)

**Contributions pratiques :**
1. Preuve de concept fonctionnelle (FRAUDX) avec dashboard, RBAC, benchmark et module SHAP
2. Plan de déploiement progressif réaliste et adapté au contexte togolais
3. Budget estimé et analyse de ROI (194 % sur 3 ans)
4. Recommandations opérationnelles pour la formation, la conduite du changement et la conformité

## Limites de l'étude

1. Absence de données locales réelles (utilisation d'IEEE-CIS comme proxy)
2. Validation qualitative non réalisée (entretiens en perspective)
3. Non-implantation du LSTM (contraintes GPU)
4. Taux de faux positifs (20,7 %) supérieur à la cible de 2 %
5. Périmètre limité au Togo

## Perspectives

1. **Partenariat avec une banque ou un opérateur mobile money togolais** pour obtenir des données réelles
2. **Extension à l'espace UEMOA** (Sénégal, Côte d'Ivoire, Bénin)
3. **Apprentissage fédéré** pour un modèle interbancaire préservant la confidentialité
4. **Détection des fraudes émergentes** via deep learning (LSTM, Transformers)
5. **Étude d'acceptabilité** auprès des analystes bancaires togolais (questionnaire TAM et entretiens qualitatifs — validation empirique de HS3)

En définitive, cette étude a démontré qu'un système d'IA fondé sur l'ensemble learning et l'explicabilité SHAP peut améliorer significativement la détection de la fraude bancaire dans le contexte togolais. Le système FRAUDX, dont la preuve de concept a été réalisée, constitue une base solide pour un déploiement progressif et contextualisé. À l'heure où la digitalisation financière transforme les économies ouest-africaines, l'IA apparaît non comme une option, mais comme une nécessité pour garantir la sécurité et la confiance dans les services financiers numériques au Togo et dans l'espace UEMOA.

---

# RÉFÉRENCES BIBLIOGRAPHIQUES

## Norme APA 7e édition

Akiba, T., Sano, S., Yanase, T., Ohta, T., & Koyama, M. (2019). Optuna: A next-generation hyperparameter optimization framework. *Proceedings of the 25th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*, 2623-2631.

Arrieta, A. B., Díaz-Rodríguez, N., Del Ser, J., Bennetot, A., Tabik, S., Barbado, A., ... & Herrera, F. (2020). Explainable artificial intelligence (XAI): Concepts, taxonomies, opportunities and challenges toward responsible AI. *Information Fusion*, 58, 82-115.

Bhattacharyya, S., Jha, S., Tharakunnel, K., & Westland, J. C. (2011). Data mining for credit card fraud: A comparative study. *Decision Support Systems*, 50(3), 602-613.

Bolton, R. J., & Hand, D. J. (2002). Statistical fraud detection: A review. *Statistical Science*, 17(3), 235-255.

Breiman, L. (2001). Random forests. *Machine Learning*, 45(1), 5-32.

Chawla, N. V., Bowyer, K. W., Hall, L. O., & Kegelmeyer, W. P. (2002). SMOTE: Synthetic minority over-sampling technique. *Journal of Artificial Intelligence Research*, 16, 321-357.

Chen, T., & Guestrin, C. (2016). XGBoost: A scalable tree boosting system. *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*, 785-794.

Dal Pozzolo, A., Caelen, O., Le Borgne, Y.-A., Waterschoot, S., & Bontempi, G. (2014). Learned lessons in credit card fraud detection from a practitioner perspective. *Expert Systems with Applications*, 41(10), 4915-4928.

Dal Pozzolo, A., Caelen, O., Johnson, R. A., & Bontempi, G. (2015). Calibrating probability with undersampling for unbalanced classification. *2015 IEEE Symposium Series on Computational Intelligence*, 159-166.

Hochreiter, S., & Schmidhuber, J. (1997). Long short-term memory. *Neural Computation*, 9(8), 1735-1780.

Liu, F. T., Ting, K. M., & Zhou, Z.-H. (2008). Isolation forest. *2008 Eighth IEEE International Conference on Data Mining*, 413-422.

Liu, F. T., Ting, K. M., & Zhou, Z.-H. (2012). Isolation-based anomaly detection. *ACM Transactions on Knowledge Discovery from Data*, 6(1), 1-39.

Lundberg, S. M., & Lee, S.-I. (2017). A unified approach to interpreting model predictions. *Advances in Neural Information Processing Systems*, 30, 4765-4774.

Lundberg, S. M., Erion, G., Chen, H., DeGrave, A., Prutkin, J. M., Nair, B., ... & Lee, S.-I. (2020). From local explanations to global understanding with explainable AI for trees. *Nature Machine Intelligence*, 2(1), 56-67.

Samuel, A. L. (1959). Some studies in machine learning using the game of checkers. *IBM Journal of Research and Development*, 3(3), 210-229.

Shapley, L. S. (1953). A value for n-person games. In H. W. Kuhn & A. W. Tucker (Eds.), *Contributions to the Theory of Games* (Vol. 2, pp. 307-317). Princeton University Press.

## Mémoires et thèses

Da, C. A. C. (2024). *Vers une détection efficace et robuste des fraudes bancaires grâce à l'apprentissage automatique* [Mémoire de maîtrise]. Université du Québec à Trois-Rivières.

Dedam, K. G. (2025). *L'application du Machine Learning pour la détection de fraude en finance* [Mémoire de maîtrise]. Université du Québec à Trois-Rivières.

## Études par pays d'Afrique de l'Ouest

Adjovi, E. (2023). Détection de fraude mobile money par régression logistique au Bénin. *Revue de l'Innovation et de la Technologie*, 5(3), 78-91.

Diop, M., & Ndiaye, S. (2022). Amélioration de la détection de fraude bancaire par XGBoost au Sénégal. *Annales de l'Université Cheikh Anta Diop*, 28(1), 112-128.

Kouamé, A. K. (2021). Détection de fraude bancaire par apprentissage automatique en Côte d'Ivoire. *Revue Africaine de Recherche en Informatique*, 14(2), 45-62.

Mensah, K. (2022). Mobile money fraud detection using XGBoost and SMOTE in Ghana. *West African Journal of Applied Computing*, 9(1), 34-51.

Okonkwo, C., Eze, P., & Okafor, N. (2020). Ensemble learning for fraud detection in Nigerian banking sector. *Journal of African Fintech*, 3(2), 156-173.

## Ouvrages et méthodologie

Davis, F. D. (1989). Perceived usefulness, perceived ease of use, and user acceptance of information technology. *MIS Quarterly*, 13(3), 319-340.

FUNIBER. (2017). *Guide pour l'élaboration de projets de recherche*. Fondation Universitaire Ibero-Américaine.

Quivy, R., & Van Campenhoudt, L. (2006). *Manuel de recherche en sciences sociales* (3e éd.). Dunod.

## Rapports institutionnels et réglementations

BCEAO. (2022). *Enquête sur l'utilisation des services financiers numériques dans l'UEMOA*.

BCEAO. (2023). *Rapport annuel sur les systèmes de paiement dans l'UEMOA*.

BCEAO. (2024). *Rapport sur les systèmes de paiement dans l'UEMOA*.

République Togolaise. (2020). *Loi N°2020-003 du 20 février 2020 relative à la protection des données à caractère personnel*.

UEMOA. (2018). *Directive N°01/2018/CM/UEMOA relative aux systèmes de paiement*.

UEMOA. (2020). *Règlement N°01/2020/CM/UEMOA sur les services de paiement mobile*.

## Webographie

ANCY. (2025a, février). *Alerte aux arnaques par faux transfert Mobile Money*. Agence Nationale de Cybersécurité, République Togolaise.

ANCY. (2025b, mars). *Alerte à l'usurpation d'agent Mobile Money et à la fausse réidentification*. Agence Nationale de Cybersécurité, République Togolaise.

CERT-TG. (2025, avril). *Alerte aux plateformes frauduleuses de vente et d'investissement*. Centre Togolais de Réponse aux Incidents de Sécurité Informatique.

RepublicOfTogo. (2025). *Lutte contre la cybercriminalité : le Togo intensifie ses actions*. Site officiel de la République Togolaise.

Togo First. (2024, novembre). Mobile money au Togo : 3,55 millions d'utilisateurs, l'ARCEP dresse le portrait-robot. *Togo First*.

---

# ANNEXE B : QUESTIONNAIRE TAM — ADOPTION DU SYSTÈME FRAUDX

> **Cadre théorique :** Technology Acceptance Model (TAM) — Davis (1989)
> **Profils cibles :** Analystes fraude, Gestionnaires de risques, Conformité, DSI — institutions bancaires et opérateurs mobile money au Togo
> **Durée estimée :** 8-10 minutes
> **Mode :** Auto-administré (Google Forms / KoboToolbox)
> **Échelle :** Likert à 5 niveaux (1 = Pas du tout d'accord, 5 = Tout à fait d'accord)
> **Confidentialité :** Anonyme — données agrégées à des fins de recherche uniquement

---

## Section A : Profil du répondant

**A1.** Dans quelle catégorie votre poste se situe-t-il ?
- Analyste fraude / Conformité
- Gestionnaire de risques
- DSI / Informatique
- Direction générale
- Autre (précisez) : _______

**A2.** Depuis combien d'années travaillez-vous dans le secteur financier ?
- Moins de 2 ans
- 2-5 ans
- 6-10 ans
- Plus de 10 ans

**A3.** Votre institution utilise-t-elle actuellement un système automatisé de détection de fraude ?
- Oui, basé sur des règles métier
- Oui, basé sur du Machine Learning
- Non
- Je ne sais pas

---

## Section B : Utilité perçue (PU)

*Pour chaque affirmation, indiquez votre niveau d'accord de 1 (Pas du tout d'accord) à 5 (Tout à fait d'accord).*

**PU1.** Un système comme FRAUDX améliorerait significativement la détection des fraudes dans mon institution.

**PU2.** FRAUDX permettrait de détecter des fraudes qui passent inaperçues avec les méthodes actuelles.

**PU3.** L'utilisation de FRAUDX réduirait le temps nécessaire à l'analyse des alertes.

**PU4.** FRAUDX serait utile pour prioriser les alertes les plus critiques.

---

## Section C : Facilité d'utilisation perçue (PEOU)

**PEOU1.** Les explications SHAP ("cette alerte a été déclenchée parce que...") sont faciles à comprendre.

**PEOU2.** Le tableau de bord FRAUDX semble intuitif et facile à prendre en main.

**PEOU3.** Je pense pouvoir utiliser FRAUDX avec une formation courte (moins d'une semaine).

**PEOU4.** Les visualisations SHAP (graphiques d'importance des variables) sont claires pour un non-spécialiste.

---

## Section D : Confiance (TR)

**TR1.** Je fais confiance aux décisions prises par un modèle de Machine Learning pour la détection de fraude.

**TR2.** Le fait que FRAUDX explique ses décisions (SHAP) renforce ma confiance dans le système.

**TR3.** Je suis à l'aise avec l'idée qu'un système d'IA analyse des transactions sans intervention humaine préalable.

**TR4.** Les mécanismes de sécurité proposés (RBAC, chiffrement, logs d'audit) me semblent suffisants pour un déploiement en production.

---

## Section E : Intention d'adoption (BI)

**BI1.** Je recommanderais l'adoption de FRAUDX dans mon institution.

**BI2.** Je serais prêt à utiliser FRAUDX dans mon travail quotidien.

**BI3.** Un système comme FRAUDX devrait être déployé prioritairement dans les banques togolaises.

**BI4.** Je participerais volontiers à une phase pilote de FRAUDX.

---

## Section F : Facteurs contextuels (FC)

**FC1.** Les contraintes infrastructurelles (connectivité, électricité, serveurs) sont un frein majeur au déploiement de l'IA bancaire au Togo.

**FC2.** Le manque de données locales labellisées est un obstacle important à l'adoption de l'IA.

**FC3.** La conformité réglementaire (BCEAO, UEMOA, protection des données) est une préoccupation prioritaire pour mon institution.

**FC4.** Mon institution dispose des compétences techniques nécessaires pour exploiter un système comme FRAUDX.

---

## Section G : Commentaires libres

**G1.** Quels seraient, selon vous, les principaux freins à l'adoption de FRAUDX dans une banque togolaise ?

**G2.** Avez-vous des suggestions ou des attentes particulières concernant un système de détection de fraude par IA ?

---

*Merci de votre participation. Vos réponses contribueront à une meilleure compréhension des facteurs d'adoption de l'IA dans le secteur bancaire togolais.*

---

## Structure d'analyse proposée

| Construit | Items | Échelle | Analyse |
|-----------|-------|---------|---------|
| Utilité perçue (PU) | PU1-PU4 | Likert 1-5 | Moyenne, écart-type, α de Cronbach |
| Facilité d'utilisation (PEOU) | PEOU1-PEOU4 | Likert 1-5 | Moyenne, écart-type, α de Cronbach |
| Confiance (TR) | TR1-TR4 | Likert 1-5 | Moyenne, écart-type, α de Cronbach |
| Intention d'adoption (BI) | BI1-BI4 | Likert 1-5 | Moyenne, écart-type, α de Cronbach |
| Facteurs contextuels (FC) | FC1-FC4 | Likert 1-5 | Analyse descriptive, corrélations |

**Tests statistiques envisagés :** corrélations de Pearson entre construits, régression linéaire multiple (BI = variable dépendante), test t de Student (comparaison profils), α de Cronbach ≥ 0,70 pour la fiabilité interne.
