## RÉSUMÉ

Dans un monde où la digitalisation financière transforme en profondeur les relations bancaires, la détection de la fraude représente à la fois un enjeu de sécurité et un défi majeur pour les institutions financières. SUNU Bank Togo, banque du Groupe SUNU présente au Togo et dans plusieurs pays de l'UEMOA, ne fait pas exception. Confrontée à une recrudescence des fraudes bancaires et numériques face auxquelles les méthodes traditionnelles de détection — règles statiques, contrôles manuels — montrent leurs limites, cette banque peine à exploiter pleinement le potentiel des technologies d'intelligence artificielle pour sécuriser ses transactions et protéger sa clientèle. Ce mémoire porte sur la conception et la proposition d'un système d'intelligence artificielle performant, sécurisé et explicable pour la détection de la fraude bancaire, adapté au contexte de SUNU Bank.

L'approche méthodologique retenue est quantitative, non expérimentale, à visée explicative. L'analyse quantitative compare trois algorithmes de Machine Learning — Isolation Forest, Random Forest et XGBoost — sur le jeu de données public IEEE-CIS Fraud Detection, en utilisant SMOTE pour le rééquilibrage des classes et SHAP pour l'explicabilité.

Un volet qualitatif est proposé en perspective pour confronter les résultats aux perceptions du terrain. Les résultats montrent la supériorité de XGBoost après optimisation du seuil de décision (Recall = 85,02 % ; Précision = 13,54 % ; AUC-PR = 0,57), avec une latence de prédiction compatible avec les exigences du temps réel. Une preuve de concept fonctionnelle (FRAUDX) a été développée, intégrant un tableau de bord interactif avec contrôle d'accès RBAC, un module SHAP d'explicabilité des décisions et un module de feedback pour l'apprentissage continu.

Si le périmètre conceptuel de l'étude inclut les transactions bancaires classiques et le mobile money (via TogoCom Cash et Moov Money/Flooz), le modèle a été entraîné sur le jeu de données international de transactions par carte (IEEE-CIS), faute de données réelles togolaises accessibles — une limite explicitement reconnue, dont l'intégration des spécificités du mobile money constitue la perspective prioritaire.

Cette recherche contribue au domaine émergent de l'IA appliquée à la détection de la fraude bancaire en contexte africain, en démontrant la faisabilité technique et le potentiel économique d'une solution adaptée aux contraintes des banques ouest-africaines.

**Mots-clés :** Détection de fraude bancaire, Machine Learning, XGBoost, Ensemble Learning, SHAP, SUNU Bank, Togo, Mobile Money, RBAC, Explicabilité (XAI).

---

## ABSTRACT

In a world where financial digitalization is profoundly transforming banking relationships, fraud detection represents both a security concern and a major challenge for financial institutions. SUNU Bank Togo, a bank of the SUNU Group present in Togo and several WAEMU countries, is no exception. Faced with a rise in banking and digital fraud against which traditional detection methods — static rules, manual controls — are showing their limits, the bank struggles to fully exploit the potential of artificial intelligence technologies to secure its transactions and protect its customers. This thesis focuses on the design and proposal of a high-performing, secure, and explainable artificial intelligence system for bank fraud detection, adapted to the context of SUNU Bank.

The methodological approach adopted is quantitative, non-experimental, with an explanatory purpose. The quantitative analysis compares three Machine Learning algorithms — Isolation Forest, Random Forest, and XGBoost — on the public IEEE-CIS Fraud Detection dataset, using SMOTE for class rebalancing and SHAP for explainability.

A qualitative component is proposed as a future direction to compare the results with field perceptions. The results show the superiority of XGBoost after threshold optimization (Recall = 85.02%; Precision = 13.54%; AUC-PR = 0.57), with a prediction latency compatible with real-time requirements. A functional proof of concept (FRAUDX) was developed, featuring an interactive dashboard with RBAC access control, a SHAP-based decision-explainability module, and a feedback module for continuous learning.

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

- **HS1** — L'automatisation de la détection de la fraude à l'aide de modèles d'apprentissage automatique (notamment XGBoost) réduit significativement le taux de faux négatifs (Recall ≥ 0,85) par rapport aux méthodes statistiques classiques, en fournissant des prédictions plus fiables sur des données transactionnelles déséquilibrées.
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
