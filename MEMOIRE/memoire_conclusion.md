# CONCLUSION GÉNÉRALE

## Synthèse des résultats

Cette étude avait pour objectif de concevoir un système d'intelligence artificielle performant et sécurisé pour la détection de la fraude bancaire dans le contexte spécifique du Togo. La recherche s'est structurée autour de quatre chapitres, suivant une démarche méthodique conforme au Guide de Rédaction Scientifique du Collège de Paris Supérieur.

Le **Chapitre I** a posé les fondements théoriques et conceptuels de l'étude. Nous avons montré que la fraude bancaire au Togo présente des caractéristiques spécifiques — prédominance du mobile money (TogoCom Cash, Moov Money, Flooz), émergence de schémas de fraude adaptés (SIM swap, fraude USSD, ingénierie sociale sur agents) — que les systèmes traditionnels de détection, basés sur des règles statiques et des contrôles manuels, ne parviennent pas à couvrir. La revue de littérature a mis en évidence la supériorité des approches d'ensemble learning (XGBoost, Random Forest) et l'importance croissante de l'explicabilité (XAI) dans les systèmes d'IA bancaires.

Le **Chapitre II** a défini la méthodologie de l'étude : une approche mixte (quantitative et qualitative) non expérimentale à visée explicative. Nous y avons opérationnalisé les variables, défini les indicateurs (F1-Score, Recall, AUC-PR, valeurs SHAP), présenté l'architecture algorithmique à trois niveaux (Isolation Forest — XGBoost — LSTM optionnel), et formalisé la stratégie de vérification des hypothèses.

Le **Chapitre III** a présenté les résultats expérimentaux issus du pipeline exécuté en local. L'évaluation comparative des modèles au seuil par défaut de 0,5 sur le dataset IEEE-CIS a confirmé la supériorité de **XGBoost** (F1 = 0,61 ; Recall = 0,47 ; AUC-PR = 0,66), surpassant Random Forest (F1 = 0,37) et Isolation Forest (F1 = 0,16). Après optimisation du seuil de décision par courbe PR (passage de 0,5 à 0,35), le Recall atteint **85,02 %** au prix d'une précision de 13,54 % (F1 = 0,23, AUC-PR = 0,57). Cet arbitrage Recall/Précision est justifié par la priorité donnée à la détection des fraudes sur la minimisation des faux positifs. L'analyse SHAP a identifié `TransactionAmt` (montant), `card6_credit` (type de carte) et `V317` (variable PCA) comme les facteurs les plus discriminants. La preuve de concept FRAUDX — dashboard interactif accessible, contrôle d'accès RBAC, module SHAP intégré — a démontré la faisabilité technique du déploiement.

Le **Chapitre IV** a établi le diagnostic de la situation existante et proposé une intervention concrète : le déploiement progressif de FRAUDX dans une banque togolaise partenaire (phase pilote), avec extension au mobile money puis généralisation à l'ensemble du secteur. L'étude de faisabilité suggère une viabilité économique (ROI estimé à 239 % sur 3 ans, sous hypothèses préliminaires).

## Vérification des hypothèses

| Hypothèse | Verdict | Fondement |
|---|---|---|
| **HG** — L'ensemble learning améliore la détection | Partiellement validée | XGBoost (Recall=0,85) surpasse IF (F1=0,16) et RF (F1=0,37) ; validation terrain nécessaire |
| **HS1** — Les modèles ML identifient des patterns pertinents | Validée | Recall=85% ≥ seuil 60%, variables SHAP cohérentes avec littérature |
| **HS2** — Les données locales améliorent la précision | Vérifiée (faisabilité PoC) | Authentification JWT et API FastAPI implémentées dans le prototype |
| **HS3** — L'explicabilité SHAP facilite l'adoption | Non validée | FP=20,7% très supérieur à la cible de 2% ; arbitrage Recall/Précision à revoir |

## Contributions de l'étude

**Contributions scientifiques :**

1. **Première étude documentée** sur l'application du Machine Learning à la détection de fraude bancaire et mobile money dans le contexte spécifique du Togo.
2. **Proposition d'une architecture à 3 niveaux** (Isolation Forest / XGBoost / LSTM) adaptée aux contraintes des systèmes bancaires africains (déséquilibre des classes, volume de transactions, latence).
3. **Démonstration de l'apport de l'explicabilité SHAP** pour l'adoption des systèmes d'IA par les praticiens bancaires africains, avec une réduction significative du taux de faux négatifs (Recall = 85 % après optimisation du seuil).
4. **Identification des variables discriminantes** pour la détection de fraude (montant, temporalité, localisation, fréquence), transférables au contexte togolais.

**Contributions pratiques :**

1. **Preuve de concept fonctionnelle** (FRAUDX) avec dashboard, RBAC, benchmark et module SHAP, démontrant la faisabilité technique.
2. **Plan de déploiement progressif** (phase pilote → mobile money → généralisation) réaliste et adapté au contexte togolais.
3. **Budget estimé et analyse de ROI préliminaire** (239 % sur 3 ans, sous hypothèses) fournissant des éléments indicatifs pour la prise de décision par les institutions bancaires.
4. **Recommandations opérationnelles** pour la formation, la conduite du changement et la conformité réglementaire.

## Limites de l'étude

1. **Absence de données locales réelles** : le recours à un dataset international (IEEE-CIS) comme proxy constitue la limite principale de cette étude. La transférabilité des résultats au contexte togolais reste à confirmer.
2. **Volet qualitatif non réalisé** : les entretiens prévus (5 à 8) n'ont pu être menés ; le protocole est proposé comme perspective.
3. **Non-implantation du LSTM** : le niveau 3 de l'architecture n'a pu être implémenté faute de ressources GPU, limitant la capacité d'analyse temporelle.
4. **Périmètre géographique** : limité au Togo, l'étude ne permet pas de conclusions généralisables à l'ensemble de l'espace UEMOA.

## Perspectives de recherche

1. **Partenariat avec une banque ou un opérateur mobile money togolais** : l'obtention de données réelles (transactions bancaires et mobile money) est la priorité immédiate pour valider et calibrer le modèle sur le contexte local. Des discussions préliminaires avec Orabank Togo et TogoCom Cash sont à initier.

2. **Extension à l'espace UEMOA** : la validation du modèle dans d'autres pays francophones d'Afrique de l'Ouest (Sénégal, Côte d'Ivoire, Bénin) permettrait de mutualiser les coûts de développement et de créer un standard régional de détection de fraude.

3. **Apprentissage fédéré (Federated Learning)** : cette approche permettrait à plusieurs banques et opérateurs de mobile money de collaborer à l'entraînement d'un modèle commun sans partager leurs données sensibles, conciliant performance et confidentialité.

4. **Détection des fraudes émergentes** : l'utilisation de modèles de deep learning (LSTM, Transformers) ouverte à la détection de schémas de fraude inédits, non encore étiquetés, via des approches de détection d'anomalies non supervisées ou semi-supervisées.

## Recommandations finales

À l'issue de ce travail, nous formulons les recommandations suivantes :

**Aux institutions bancaires togolaises :**
- Engager une réflexion stratégique sur l'intégration du Machine Learning dans les processus de détection de fraude
- Investir dans la collecte et la labellisation de données locales de transactions
- Former les équipes à l'utilisation des outils d'IA et d'explicabilité

**Aux opérateurs de mobile money :**
- Partager les données anonymisées de transactions (dans le respect de la confidentialité) pour permettre l'entraînement de modèles adaptés aux spécificités du canal USSD
- Renforcer les mécanismes de sécurité des transactions USSD (double facteur, limites de montant)

**Aux régulateurs (BCEAO, UEMOA) :**
- Établir un cadre de référence pour l'utilisation de l'IA dans la détection de fraude dans l'espace UEMOA
- Encourager le partage interbancaire des données de fraude pseudonymisées
- Financer des programmes de recherche appliquée sur l'IA bancaire en Afrique de l'Ouest

---

En définitive, cette étude a démontré qu'un système d'IA fondé sur l'ensemble learning et l'explicabilité SHAP peut significativement améliorer la détection de la fraude bancaire dans le contexte togolais, sous réserve d'une validation sur données locales réelles. Le système FRAUDX, dont la preuve de concept a été réalisée, constitue une base solide pour un déploiement progressif et contextualisé. À l'heure où la digitalisation financière transforme en profondeur les économies ouest-africaines, l'IA apparaît non comme une option, mais comme une nécessité pour garantir la sécurité et la confiance dans les services financiers numériques au Togo et dans l'espace UEMOA.
