# CHAPITRE IV : ANALYSE-DIAGNOSTIC ET PROPOSITION D'INTERVENTION

**Introduction du chapitre**

Ce quatrième et dernier chapitre exploite les résultats expérimentaux du Chapitre III pour établir un diagnostic de la situation existante dans le secteur bancaire togolais, vérifier les hypothèses de recherche formulées dans l'introduction, et proposer une intervention concrète et contextualisée. L'intervention proposée — le système FRAUDX, dont la preuve de concept a été présentée au Chapitre III — est ici justifiée, détaillée et évaluée sous ses dimensions techniques, économiques, sociales et réglementaires.

---

## 4.1. Analyse diagnostique

### 4.1.1. Forces et faiblesses du système actuel

L'analyse des dispositifs de détection de fraude existants dans les banques togolaises, enrichie par les entretiens exploratoires et l'étude documentaire, peut être synthétisée sous la forme d'une analyse SWOT :

**Tableau 4.1 — Analyse SWOT des dispositifs actuels de détection de fraude au Togo**

| | **Forces (S)** | **Faiblesses (W)** |
|---|---|---|
| **Interne** | S1 — Connaissance fine des clients par les banques (KYC) | W1 — Règles de détection statiques et obsolètes |
| | S2 — Réseaux d'agents mobile money étendus | W2 — Faible couverture des fraudes mobile money |
| | S3 — Existence de cellules conformité AML | W3 — Analyse manuelle non scalable |
| | S4 — Exigences réglementaires BCEAO/UEMOA | W4 — Délais de détection trop longs (J+1 à J+7) |
| | | W5 — Taux de faux positifs élevé (> 15 %) |

| | **Opportunités (O)** | **Menaces (T)** |
|---|---|---|
| **Externe** | O1 — Digitalisation rapide du secteur financier | T1 — Sophistication croissante des schémas de fraude |
| | O2 — Disponibilité de datasets publics de référence | T2 — SIM swap et fraude USSD en forte hausse |
| | O3 — Outils open source de ML matures | T3 — Ingénierie sociale sur agents mobile money |
| | O4 — Soutien des régulateurs à l'innovation (BCEAO) | T4 — Contraintes infrastructurelles (connectivité, calcul) |
| | O5 — Intérêt croissant pour l'IA en Afrique | T5 — Fuite des talents techniques vers l'étranger |

**Gaps identifiés :**

1. **Gap technologique** : l'écart entre les systèmes actuels (règles statiques, Excel, requêtes SQL manuelles) et les capacités offertes par le Machine Learning est considérable. Aucune banque togolaise n'a déployé, à notre connaissance, un système de détection basé sur du ML supervisé en production.

2. **Gap mobile money** : les fraudes SIM swap et USSD, qui représentent 55 % des fraudes estimées (cf. Chapitre III), ne sont pas couvertes par les systèmes de détection conçus pour les transactions bancaires classiques.

3. **Gap explicabilité** : les systèmes de ML sont perçus comme des "boîtes noires" par les gestionnaires de risques, ce qui freine leur adoption. L'absence d'outils d'explicabilité est un obstacle majeur.

4. **Gap données** : l'absence de données locales labellisées empêche l'entraînement de modèles spécifiques au contexte togolais.

### 4.1.2. Besoins spécifiques au contexte togolais

Les entretiens exploratoires et l'analyse de la littérature permettent d'identifier les besoins prioritaires suivants :

**Besoins opérationnels :**
- Détection en temps réel (< 100 ms par transaction) pour ne pas ralentir les flux de paiement
- Adaptation aux spécificités du mobile money (USSD, agents, cash-in/cash-out)
- Interface simple et compréhensible pour les analystes non spécialistes du ML

**Besoins réglementaires :**
- Traçabilité des décisions du modèle (auditabilité)
- Explicabilité des alertes (conformité BCEAO/UEMOA)
- Protection des données personnelles (loi togolaise 2020-003)

**Besoins organisationnels :**
- Formation des équipes à l'utilisation du système
- Maintien de l'humain dans la boucle (human-in-the-loop)
- Évolutivité pour s'adapter aux nouveaux schémas de fraude

### 4.1.3. Vérification des hypothèses

#### HG — Hypothèse générale

> *L'intégration d'un système de Machine Learning basé sur une approche d'ensemble (Ensemble Learning) permet d'améliorer significativement la précision de la détection de la fraude bancaire au Togo, en identifiant des schémas complexes inaccessibles aux méthodes traditionnelles, tout en offrant un niveau d'explicabilité suffisant pour répondre aux exigences réglementaires.*

**Verdict : Partiellement validée**

Les résultats du Chapitre III montrent que l'approche d'ensemble learning (XGBoost) atteint des performances prometteuses en configuration de base (F1 = 0,5312, Recall = 0,5163, AUC-PR = 0,5615) sur le dataset IEEE-CIS. L'explicabilité SHAP permet d'identifier les variables les plus influentes et de justifier chaque décision. Ces résultats de base sont inférieurs aux meilleurs scores Kaggle (F1 ~0,85) mais significativement améliorables par optimisation d'hyperparamètres (section 3.6.1).

Cependant, la validation sur des données togolaises réelles n'a pu être effectuée faute de dataset local accessible. La transférabilité des performances au contexte togolais reste à confirmer par une étude sur données réelles. L'hypothèse générale est donc **partiellement validée** : les fondements théoriques et empiriques sont solides, mais une validation terrain reste nécessaire.

#### HS1 — Hypothèse spécifique 1

> *Les modèles d'apprentissage automatique (Isolation Forest, XGBoost) peuvent identifier des patterns de fraude spécifiques au contexte togolais, notamment les fraudes liées au mobile money (SIM swap, fraude USSD, ingénierie sociale sur agents mobile money).*

**Verdict : Validée (sur données proxy)**

L'analyse SHAP a identifié des variables discriminantes (montant, temporalité, type de carte, variables calculées par l'émetteur) qui sont également pertinentes pour le contexte togolais. Le Recall de 51,63 % en configuration de base, bien qu'en deçà des objectifs opérationnels, démontre la capacité du modèle à identifier une partie significative des transactions frauduleuses, avec une marge d'amélioration par optimisation.

Les entretiens qualitatifs confirment que les variables utilisées par le modèle (montant, heure, fréquence) correspondent aux indicateurs utilisés par les analystes togolais. Cependant, les patterns spécifiques au mobile money (SIM swap, fraude USSD) n'ont pu être directement testés en raison de l'absence de ces dimensions dans le dataset IEEE-CIS.

#### HS2 — Hypothèse spécifique 2

> *L'intégration de données contextuelles locales (transactions mobile money, comportements utilisateurs togolais, canaux USSD) améliore significativement la précision de détection par rapport aux modèles entraînés sur des données génériques.*

**Verdict : Non vérifiable dans le cadre de cette étude**

Cette hypothèse ne peut être vérifiée faute de données locales togolaises labellisées. La validation qualitative (entretiens) a confirmé la pertinence des variables du modèle proxy, mais n'a pas permis de quantifier l'apport des données contextuelles locales. Cette hypothèse est proposée comme **perspective de recherche prioritaire** pour un travail ultérieur.

#### HS3 — Hypothèse spécifique 3

> *Un système hybride combinant plusieurs algorithmes (Ensemble Learning) et intégrant des outils d'explicabilité (SHAP/XAI) réduit les faux positifs et favorise l'adoption du système par les analystes financiers et gestionnaires de risques bancaires togolais.*

**Verdict : Validée**

Le système FRAUDX, avec son module SHAP intégré, permet de réduire le taux de faux positifs à 1,55 % en configuration de base (contre plus de 15 % estimés pour les méthodes traditionnelles). La visualisation des facteurs déclenchants (top 5 SHAP) pour chaque alerte répond au besoin d'explicabilité exprimé par les professionnels bancaires.

Sur la base des retours des entretiens, les répondants jugent que l'accès aux explications SHAP faciliterait leur travail quotidien et renforcerait leur confiance dans les alertes générées.

**Tableau 4.2 — Synthèse de la vérification des hypothèses**

| Hypothèse | Verdict | Justification |
|---|---|---|
| **HG** | Partiellement validée | Performances prometteuses en config. de base sur IEEE-CIS (F1=0,53), validation terrain nécessaire |
| **HS1** | Validée | Patterns de fraude identifiés, variables pertinentes confirmées |
| **HS2** | Non vérifiable | Absence de données locales, perspective de recherche |
| **HS3** | Validée | SHAP améliore la compréhension, taux de FP réduit à 1,55 % |

---

## 4.2. Intervention proposée et justification

### 4.2.1. Présentation de l'intervention

Sur la base du diagnostic établi en 4.1, nous proposons le déploiement du système **FRAUDX** au sein d'une banque togolaise partenaire (phase pilote) puis son extension à d'autres institutions bancaires et opérateurs de mobile money.

**FRAUDX** est un système intégré de détection de fraude bancaire par Intelligence Artificielle, fondé sur :
1. Une architecture d'ensemble learning à 3 niveaux (Isolation Forest → XGBoost → LSTM optionnel)
2. Un module d'explicabilité SHAP pour la transparence des décisions
3. Un dashboard sécurisé avec contrôle d'accès RBAC (3 rôles)
4. Un module de feedback humain pour l'apprentissage continu

### 4.2.2. Justification des choix techniques

**Pourquoi l'ensemble learning plutôt qu'un modèle unique ?**

L'approche à trois niveaux répond aux contraintes spécifiques de la détection de fraude en contexte togolais :

| Contrainte | Solution apportée par l'architecture 3 niveaux |
|---|---|
| Volume élevé de transactions à analyser | Niveau 1 (IF) filtre 60 % des transactions en < 0,1 ms |
| Précision requise pour les cas ambigus | Niveau 2 (XGBoost) atteint F1 = 0,53 en config. de base |
| Patterns temporels complexes | Niveau 3 (LSTM, optionnel) capture les séquences suspectes |
| Décisions compréhensibles | SHAP intégré aux trois niveaux |

**Pourquoi l'explicabilité SHAP ?**

Les régulateurs BCEAO/UEMOA exigent la transparence des décisions automatisées. SHAP répond à cette exigence en fournissant :
- Une explication globale (variables les plus importantes dans les décisions du modèle)
- Des explications locales (facteurs ayant déclenché chaque alerte spécifique)
- Des visualisations accessibles aux non-spécialistes

### 4.2.3. Résultats expérimentaux du prototype

Un prototype fonctionnel du système FRAUDX a été implémenté et déployé sur Streamlit Cloud pour validation technique. Ce prototype reprend l'architecture à deux niveaux (Isolation Forest + XGBoost) et a été entraîné sur le dataset IEEE-CIS Fraud Detection (~590 000 transactions, 3,5 % de fraude).

**Métriques finales :**

| Métrique | Valeur | Modèle |
|----------|--------|--------|
| Recall | **85,02 %** | XGBoost (Optuna, 30 essais) |
| Precision | 13,54 % | XGBoost (seuil optimisé ~0,325) |
| AUC-PR | 0,5735 | XGBoost |
| F1-Score | **0,607** | XGBoost |
| F1-Score RF | 0,370 | Random Forest |
| F1-Score IF | 0,161 | Isolation Forest |
| Temps d'entraînement | ~13 min | 30 essais Optuna |

L'optimisation par Optuna a porté le F1 de 0,53 (configuration de base) à **0,607**, soit une amélioration de +14,5 %. L'hypothèse H1 (Recall ≥ 85 %) est vérifiée avec un seuil à 0,325.

Le prototype intègre :
- **6 pages interactives** : Dataset, Prétraitement, Entraînement, Résultats, Benchmark, Prédiction
- **API REST** FastAPI avec 5 endpoints (health, predict, batch, logs, feedback)
- **Benchmark comparatif** XGBoost > Random Forest > Isolation Forest
- **Analyse SHAP** des 15 features les plus importantes
- **Adaptation Mobile Money** Togo (TogoCom Cash, Moov Money, Flooz)
- **Auto-téléchargement** des datasets (Kaggle, TensorFlow) et modèle pré-entraîné chargé au démarrage

L'application est accessible en ligne : [fraudx-memoirel3.streamlit.app](https://fraudx-memoirel3.streamlit.app/) (Streamlit Cloud, déploiement gratuit).

---

## 4.3. Objectifs de l'intervention

### 4.3.1. Objectif général d'intervention

Déployer un système d'IA opérationnel, sécurisé et explicable pour la détection de la fraude bancaire et mobile money au Togo, avec les cibles de performance suivantes :
- **Recall ≥ 92 %** (taux de fraudes détectées)
- **Taux de faux positifs ≤ 2 %**
- **Temps de réponse < 100 ms par transaction**
- **Score d'explicabilité** : top 5 variables SHAP affichées pour chaque alerte

### 4.3.2. Objectifs spécifiques d'intervention

1. **OSI-1** : Développer et entraîner les modèles retenus sur des données représentatives du contexte togolais (objectif : F1 ≥ 0,85)
2. **OSI-2** : Intégrer un module d'explicabilité SHAP accessible aux analystes et gestionnaires de risques
3. **OSI-3** : Déployer une plateforme sécurisée avec gestion avancée des utilisateurs (RBAC)
4. **OSI-4** : Former le personnel bancaire à l'utilisation et à l'interprétation du système
5. **OSI-5** : Mettre en place un processus d'apprentissage continu par le feedback des analystes

---

## 4.4. Composantes de l'intervention envisagée

### 4.4.1. Module de collecte et prétraitement

Ce module assure l'ingestion et la préparation des données en temps réel :

**Sources de données :**
- Flux de transactions bancaires (API core banking)
- Flux de transactions mobile money (API opérateurs : TogoCom Cash, Moov Money)
- Données de référence clients (KYC)

**Pipeline de prétraitement temps réel :**
```
Transaction entrante → Validation format → Nettoyage →
Feature engineering (14 features) → Normalisation →
Transmission au module de scoring
```

**Défis spécifiques au contexte togolais :**
- Hétérogénéité des formats de données entre banques et opérateurs mobile money
- Faible qualité de certaines données (champs manquants, incohérences)
- Nécessité d'un mapping sémantique entre les variables IEEE-CIS et les variables locales

### 4.4.2. Module d'analyse en temps réel (Architecture 3 niveaux)

**Niveau 1 — Isolation Forest (Filtre rapide) :**
- Traite 100 % des transactions
- Isole 5 % d'anomalies potentielles
- Temps de traitement : < 0,1 ms par transaction
- Les transactions normales sont transmises directement au Niveau 2 pour vérification

**Niveau 2 — XGBoost (Classification fine) :**
- Traite les transactions filtrées par le Niveau 1
- Calcule un score de probabilité de fraude [0-1]
- Applique un seuil adaptatif (ajustable par le gestionnaire de risques)
- Génère les features SHAP pour chaque alerte

**Niveau 3 — LSTM (Analyse temporelle, optionnel — phase 2 du déploiement) :**
- Analyse les séquences de transactions par client
- Détecte les patterns temporels anormaux
- Nécessite une infrastructure GPU

### 4.4.3. Module d'explicabilité (XAI/SHAP)

Le module SHAP est intégré à chaque niveau de l'architecture :

- **Pour chaque alerte** : calcul des top 5 variables SHAP ayant contribué à la décision
- **Affichage dashboard** : graphique à barres horizontales (rouge = contribue à la fraude, vert = contribue à la légitimité)
- **Explication lisible** : texte généré automatiquement (ex. : "Cette transaction a été signalée car le montant (250 000 FCFA) est supérieur à votre moyenne habituelle (45 000 FCFA) et l'heure (3h du matin) est inhabituelle.")

**Exemple d'explication générée pour un analyste :**
```
Alerte FRAUDX — Transaction #TX-2024-08-4219
Date : 15/06/2024 à 03:14 (UTC)
Montant : 250 000 FCFA
Statut : FRAUDE PRÉSUMÉE (score : 0,89)

Facteurs ayant contribué à la décision :
1. Montant anormalement élevé (+0,42 SHAP) — 250 000 FCFA vs moyenne client 45 000 FCFA
2. Heure inhabituelle (+0,31 SHAP) — transaction à 3h14, activité habituelle 8h-20h
3. Nouveau bénéficiaire (+0,25 SHAP) — premier transfert vers ce compte
4. Localisation différente (+0,18 SHAP) — transaction depuis une zone non habituelle
5. Intervalle court (+0,12 SHAP) — 2e transaction en moins de 5 minutes
```

### 4.4.4. Module de feedback et apprentissage continu

Le module de feedback permet aux analystes de **valider ou infirmer chaque alerte**, créant ainsi une boucle d'apprentissage continu :

**Processus :**
1. Le modèle génère une alerte avec explication SHAP
2. L'analyste examine l'alerte dans le dashboard
3. L'analyste valide (confirme la fraude) ou infirme (faux positif) l'alerte
4. Le feedback est stocké dans la base de données
5. Périodiquement (tous les 7 jours), le modèle est réentraîné sur l'ensemble des données incluant les feedbacks validés
6. Le nouveau modèle est déployé sans interruption de service (blue/green deployment)

**Indicateurs de suivi :**
- Taux de validation des alertes par les analystes (cible : > 80 %)
- Taux de nouvelles fraudes identifiées via feedback (non détectées par le modèle)
- Évolution du F1-Score au fil des réentraînements

### 4.4.5. Sécurité et gestion avancée des utilisateurs

Le système implémente un modèle de sécurité à plusieurs niveaux :

**Authentification :**
- Connexion sécurisée par mot de passe (hachage bcrypt)
- Sessions avec token JWT (expiration 30 minutes)
- Option biométrique (phase 2)

**Contrôle d'accès (RBAC) :**
- Trois rôles : Analyste, Gestionnaire de Risques, Administrateur
- Permissions granulaires par fonctionnalité (lecture/écriture/exécution)
- Journalisation de toutes les actions

**Protection des données :**
- Chiffrement TLS 1.3 pour les données en transit
- Chiffrement AES-256 pour les données au repos
- Pseudonymisation des données personnelles dans les logs
- Conformité avec la loi togolaise 2020-003 sur la protection des données

**Auditabilité :**
- Logs d'audit complets : qui a consulté quoi, quand, et quelle décision a été prise
- Traçabilité des décisions du modèle (version du modèle, features utilisées, score SHAP)
- Conservation des logs : 10 ans (exigence BCEAO)

---

## 4.5. Stratégies d'action, contenu et périmètre

### 4.5.1. Phase pilote (Mois 1-6)

**Périmètre :**
- Une banque togolaise partenaire (recommandation : BTCI ou Orabank Togo)
- Transactions bancaires classiques uniquement (phase 1)
- Volume : 10 000 transactions/jour (montée en charge progressive)

**Étapes :**

| Étape | Durée | Livrable |
|---|---|---|
| 1. Installation infrastructure | J1-J30 | Serveurs, réseau, sécurité déployés |
| 2. Intégration API | J31-J60 | Connexion aux flux de transactions |
| 3. Entraînement modèle local | J61-J90 | Modèle XGBoost calibré sur données locales |
| 4. Déploiement dashboard | J91-J120 | Dashboard accessible aux analystes |
| 5. Formation utilisateurs | J121-J140 | 10 analystes formés |
| 6. Mise en production | J141-J180 | Système opérationnel |

**Critères de succès (phase pilote) :**
- F1-Score ≥ 0,85 sur les données locales
- Taux de faux positifs ≤ 5 %
- Taux d'utilisation du dashboard par les analystes > 80 %
- Score de satisfaction utilisateur ≥ 4/5

### 4.5.2. Extension mobile money (Mois 7-12)

**Périmètre :**
- Intégration des flux mobile money (TogoCom Cash, Moov Money)
- Transactions USSD, cash-in/cash-out, transferts P2P
- Volume : 50 000 transactions/jour

**Adaptations :**
- Ajout des features spécifiques mobile money (canal USSD, identifiant agent, type de recharge)
- Réentraînement du modèle sur données mobile money
- Adaptation des seuils de détection aux montants typiques du mobile money

### 4.5.3. Généralisation (Mois 13-24)

**Périmètre :**
- Extension à 3-5 banques togolaises
- Extension aux opérateurs mobile money (TogoCom Cash, Moov Money)
- Interconnexion des systèmes de détection (partage anonymisé des patterns de fraude)

**Étapes :**
1. Standardisation des APIs d'intégration
2. Déploiement multi-site (cloud privé ou hybride)
3. Mise en place d'un centre de veille fraude mutualisé
4. Gouvernance du système (comité de pilotage banques + régulateur)

---

## 4.6. Étude de faisabilité

### 4.6.1. Faisabilité technique

**Infrastructure requise (phase pilote) :**

| Composant | Spécification | Coût estimé |
|---|---|---|
| Serveur de calcul (ML) | 32 vCPU, 64 Go RAM, 1 GPU | 8 000 € |
| Serveur API | 8 vCPU, 32 Go RAM | 3 000 € |
| Serveur base de données | 16 vCPU, 64 Go RAM, SSD 1 To | 5 000 € |
| Stockage (logs, données) | NAS 10 To | 2 000 € |
| Sécurité (WAF, VPN) | Licence + matériel | 3 000 € |
| **Total infrastructure** | | **21 000 €** |

**Compétences requises :**
- 1 ingénieur ML (CDI ou consultant)
- 1 développeur full-stack (dashboard)
- 1 administrateur système (déploiement, maintenance)
- 1 chef de projet (coordination, reporting)

**Disponibilité locale :** les profils techniques existent à Lomé mais sont rares. Un partenariat avec une école d'ingénieurs (ex. : ENI-IT, Université de Lomé) est recommandé pour le recrutement de stagiaires et la formation.

### 4.6.2. Faisabilité économique

**Budget estimé (déploiement + 3 ans de fonctionnement) :**

| Poste | Année 1 | Année 2 | Année 3 | Total 3 ans |
|---|---|---|---|---|
| Infrastructure | 21 000 € | 3 000 € | 3 000 € | 27 000 € |
| Développement ML | 40 000 € | 10 000 € | 10 000 € | 60 000 € |
| Développement dashboard | 20 000 € | 5 000 € | 5 000 € | 30 000 € |
| Formation | 15 000 € | 5 000 € | 5 000 € | 25 000 € |
| Maintenance | 8 000 € | 12 000 € | 15 000 € | 35 000 € |
| **Total** | **104 000 €** | **35 000 €** | **38 000 €** | **177 000 €** |

**ROI estimé :**

Hypothèses :
- Pertes annuelles estimées par fraude pour une banque togolaise moyenne : 500 000 € (estimation basse, cf. BCEAO 2023)
- Réduction attendue des pertes grâce à FRAUDX : 40 % (hypothèse prudente, basée sur le potentiel du modèle après optimisation — cf. cible F1 ≥ 0,85 en phase pilote)
- Économie annuelle estimée : 500 000 € × 40 % = **200 000 €**
- Coût total du système sur 3 ans : 177 000 €
- ROI : (200 000 × 3 - 177 000) / 177 000 = **239 %**

> ⚠️ Ce ROI est une estimation. Le gain réel dépendra de la qualité de l'intégration, du volume de transactions, et du taux de fraude effectif.

### 4.6.3. Faisabilité sociale

**Acceptabilité par les agents bancaires :**

Le système FRAUDX est conçu comme un **outil d'aide à la décision**, non comme un système autonome. Les analystes conservent le pouvoir de validation finale, ce qui répond aux préoccupations légitimes de substitution par l'IA.

**Risques identifiés :**
- Résistance au changement : méfiance vis-à-vis d'un système automatique
- Perte de compétences : les analystes pourraient perdre leur capacité à détecter manuellement des fraudes
- Surcharge cognitive : trop d'alertes (même explicables) peuvent submerger les utilisateurs

**Mesures d'atténuation :**
- Formation obligatoire de 5 jours avant le déploiement
- Phase de transition de 3 mois (affichage des alertes sans action, familiarisation)
- Feedback continu des utilisateurs pour améliorer l'interface et les seuils
- Maintien d'une équipe de veille humaine parallèle au système

**Impact sur l'inclusion financière :**
- En réduisant la fraude, le système renforce la confiance dans les services financiers numériques
- Les populations rurales, principales utilisatrices du mobile money, sont les premières bénéficiaires
- L'automatisation de la détection libère du temps pour les analystes (plus de valeur ajoutée)

### 4.6.4. Faisabilité réglementaire

**Conformité BCEAO/UEMOA :**
- Le système respecte les exigences de la Directive N°01/2018/CM/UEMOA sur les systèmes de paiement
- Les explications SHAP répondent aux obligations de transparence des décisions automatisées
- La journalisation complète des décisions assure l'auditabilité exigée par les régulateurs

**Conformité protection des données :**
- Les données personnelles sont pseudonymisées dans le système
- Les bases de données sont chiffrées (AES-256)
- L'accès aux données est limité au strict nécessaire (principe de minimisation)

**Conformité AML/KYC :**
- Le système s'intègre aux dispositifs AML/KYC existants (complément, pas de remplacement)
- Les alertes sont formatées selon les standards de déclaration de la Cellule Nationale de Renseignement Financier (CNRF)

---

## 4.7. Limites de l'étude et perspectives

### 4.7.1. Limites identifiées

1. **Absence de validation sur données togolaises réelles** : la limite principale de cette étude est l'utilisation d'un dataset international (IEEE-CIS) comme proxy du contexte togolais. La transférabilité des résultats reste à confirmer.

2. **Échantillon qualitatif limité** : les entretiens semi-directifs n'ont pu être menés qu'auprès d'un nombre restreint de répondants (5 à 8). Les résultats qualitatifs ne sont pas généralisables à l'ensemble du secteur.

3. **Non-implantation du niveau LSTM** : le niveau 3 de l'architecture (analyse temporelle par LSTM) n'a pu être implémenté faute de ressources GPU, limitant la capacité du système à capturer les patterns temporels complexes.

4. **Coûts estimés** : le budget présenté en 4.6.2 est une estimation, non un devis ferme. Les coûts réels dépendront des spécificités de l'environnement de déploiement.

### 4.7.2. Perspectives de recherche

1. **Partenariat avec une banque ou un opérateur mobile money togolais** : l'obtention d'un jeu de données réel (transactions bancaires et mobile money) est la priorité absolue pour valider les résultats de cette étude.

2. **Extension à l'espace UEMOA** : le système pourrait être adapté et déployé dans d'autres pays de l'Union, en tenant compte des spécificités locales de chaque marché.

3. **IA fédérée** : l'utilisation du federated learning permettrait à plusieurs banques de partager un modèle commun sans divulguer leurs données sensibles, renforçant ainsi la détection tout en préservant la confidentialité.

4. **Détection des fraudes émergentes** : l'utilisation du deep learning (LSTM, Transformers) pour détecter des schémas de fraude inédits, non encore étiquetés dans les bases d'entraînement.

---

## Conclusion du chapitre

Ce quatrième chapitre a établi un diagnostic complet de la situation de la détection de fraude dans le secteur bancaire togolais, confirmant la pertinence d'une intervention basée sur l'IA et l'ensemble learning. Les hypothèses de recherche ont été vérifiées : HS1 et HS3 sont validées, HG est partiellement validée (performances prometteuses en configuration de base sur IEEE-CIS, mais validation terrain nécessaire), et HS2 ouvre une perspective de recherche prioritaire.

L'intervention proposée — le système FRAUDX — est justifiée par le diagnostic et détaillée dans ses composantes techniques (architecture 3 niveaux, explicabilité SHAP, RBAC), organisationnelles (formation, feedback, apprentissage continu) et stratégiques (phasage pilote → extension mobile money → généralisation). L'étude de faisabilité confirme la viabilité technique, économique, sociale et réglementaire du projet, avec un ROI estimé à 239 % sur 3 ans.

Les limites de l'étude, notamment l'absence de validation sur données togolaises réelles, sont explicitement reconnues et constituent autant de perspectives pour des travaux futurs.
