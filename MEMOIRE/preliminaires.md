---

**Page de garde**

---

# CONCEPTION D'UN SYSTÈME D'INTELLIGENCE ARTIFICIELLE POUR LA DÉTECTION DE LA FRAUDE BANCAIRE : CAS DU TOGO

**Mémoire de fin d'études — Master**

Présenté et soutenu par : **[Nom de l'étudiant]**

Sous la direction de : **[Nom du directeur]**

Année académique : 2024-2025

**Collège de Paris Supérieur**
Master en [Nom du programme]

---

*Document conforme au Guide de Rédaction Scientifique du Collège de Paris Supérieur et à la Méthodologie de la Recherche Scientifique (Assou, 2024)*

---

---

**Dédicace**

---

*À mes parents, pour leur soutien indéfectible et leurs sacrifices.*

*À toutes les victimes de la fraude bancaire au Togo, dans l'espoir que ce travail contribue à un environnement financier plus sûr pour tous.*

---

---

**Remerciements**

---

Je tiens à exprimer ma profonde gratitude à **[Nom du directeur]** , Directeur de ce mémoire, pour sa disponibilité, ses conseils éclairés et son accompagnement rigoureux tout au long de ce travail de recherche.

Mes sincères remerciements vont à l'ensemble du corps enseignant du Collège de Paris Supérieur pour la qualité de la formation dispensée et pour avoir éveillé en moi l'esprit de recherche scientifique.

Je remercie également les responsables des institutions bancaires togolaises et des opérateurs de mobile money qui ont accepté de participer aux entretiens et dont les contributions ont enrichi cette étude.

Enfin, je remercie ma famille et mes proches pour leur patience, leur soutien moral et leurs encouragements durant cette année de recherche.

---

---

**Résumé**

---

La digitalisation rapide des services financiers au Togo, portée par l'essor du mobile money (TogoCom Cash, Moov Money, Flooz), s'accompagne d'une recrudescence des fraudes bancaires et numériques face auxquelles les méthodes traditionnelles de détection (règles statiques, contrôles manuels) montrent leurs limites. Cette étude vise à concevoir et proposer un système d'intelligence artificielle performant, sécurisé et explicable pour la détection de la fraude bancaire adapté au contexte togolais.

L'approche méthodologique retenue est mixte (quantitative et qualitative), non expérimentale à visée explicative. L'analyse quantitative compare trois algorithmes de Machine Learning — Isolation Forest, Random Forest et XGBoost — sur le dataset public IEEE-CIS Fraud Detection (~590 000 transactions), en utilisant SMOTE pour le rééquilibrage des classes et SHAP pour l'explicabilité. L'analyse qualitative s'appuie sur des entretiens semi-directifs auprès de responsables bancaires togolais.

Les résultats montrent la supériorité de XGBoost après optimisation par Optuna (F1 = 0,72 ; Recall = 0,64 ; AUC-PR = 0,72) — soit une amélioration de +35 % par rapport à la configuration de base (F1 = 0,53) — avec une latence de prédiction de 0,016 ms par transaction, compatible avec les exigences du temps réel. Une preuve de concept fonctionnelle (FRAUDX) a été développée, intégrant un tableau de bord interactif avec contrôle d'accès RBAC, un module SHAP d'explicabilité des décisions, et un module de feedback pour l'apprentissage continu. L'étude de faisabilité estime un retour sur investissement de 239 % sur trois ans pour une banque togolaise type.

**Mots-clés** : Détection de fraude bancaire, Machine Learning, XGBoost, Ensemble Learning, SHAP, Mobile money, Togo, RBI, Explicabilité (XAI).

---

---

**Abstract**

---

The rapid digitalization of financial services in Togo, driven by the rise of mobile money (TogoCom Cash, Moov Money, Flooz), has been accompanied by a surge in banking and digital fraud. Traditional detection methods (static rules, manual controls) are proving inadequate. This study aims to design and propose a high-performance, secure, and explainable artificial intelligence system for banking fraud detection tailored to the Togolese context.

The methodological approach is mixed (quantitative and qualitative), non-experimental, and explanatory. The quantitative analysis compares three Machine Learning algorithms — Isolation Forest, Random Forest, and XGBoost — on the public IEEE-CIS Fraud Detection dataset (~590,000 transactions), using SMOTE for class balancing and SHAP for explainability. The qualitative analysis is based on semi-structured interviews with Togolese banking officials.

Results demonstrate the superiority of XGBoost after Optuna optimization (F1 = 0.72; Recall = 0.64; AUC-PR = 0.72) — a 35% improvement over the default configuration (F1 = 0.53) — with a prediction latency of 0.016 ms per transaction, meeting real-time requirements. A functional proof of concept (FRAUDX) was developed, featuring an interactive dashboard with RBAC, a SHAP explanation module, and a feedback loop for continuous learning. The feasibility study estimates a return on investment of 239% over three years for a typical Togolese bank.

**Keywords**: Fraud detection, Machine Learning, XGBoost, Ensemble Learning, SHAP, Mobile money, Togo, RBAC, Explainable AI (XAI).

---

---

**Table des matières**

---

INTRODUCTION GÉNÉRALE ................................................. 1

CHAPITRE I — CADRE THÉORIQUE ET CONCEPTUEL ............ 15

CHAPITRE II — MÉTHODOLOGIE DE L'ÉTUDE ...................... 45

CHAPITRE III — PRÉSENTATION DU SYSTÈME ET DES DONNÉES ..... 70

CHAPITRE IV — ANALYSE-DIAGNOSTIC ET PROPOSITION D'INTERVENTION ... 100

CONCLUSION GÉNÉRALE ............................................. 130

RÉFÉRENCES BIBLIOGRAPHIQUES ................................... 140

ANNEXES .......................................................... 150

---

*(La pagination ci-dessus est indicative et sera ajustée lors de la mise en page finale)*

---

---

**Index des tableaux**

---

Tableau 1.1 — Synthèse comparative des études antérieures en Afrique de l'Ouest

Tableau 2.1 — Opérationnalisation des variables

Tableau 2.2 — Dynamique anticipée des variables et seuils de confirmation des hypothèses

Tableau 2.3 — Architecture des modèles

Tableau 2.4 — Distribution des classes avant et après SMOTE

Tableau 2.5 — Métriques d'évaluation retenues

Tableau 2.6 — Stratégie de vérification des hypothèses

Tableau 3.1 — Répartition estimée des types de fraude au Togo

Tableau 3.2 — Performances comparatives des modèles

Tableau 3.3 — Matrice de confusion (XGBoost)

Tableau 3.4 — Matrice des rôles et permissions FRAUDX

Tableau 3.5 — Validation croisée 5 folds (XGBoost)

Tableau 3.6 — Performance de XGBoost sur le dataset ULB

Tableau 4.1 — Analyse SWOT des dispositifs actuels

Tableau 4.2 — Synthèse de la vérification des hypothèses

---

---

**Index des figures**

---

Figure 3.1 — Distribution des classes (IEEE-CIS)

Figure 3.2 — Importance globale des variables (SHAP)

Figure 3.3 — Architecture technique en 6 couches (FRAUDX)

Figure 3.4 — Dashboard FRAUDX (maquette)

Figure 3.5 — Waterfall plot SHAP (exemple individuel)

---

*(Les figures seront intégrées lors de la mise en page finale du document)*

---

---

**Liste des abréviations**

---

| Abréviation | Signification |
|---|---|
| AML | Anti-Money Laundering |
| ANN | Artificial Neural Network |
| API | Application Programming Interface |
| AUC-PR | Area Under the Precision-Recall Curve |
| BCEAO | Banque Centrale des États de l'Afrique de l'Ouest |
| CDP | Collège de Paris Supérieur |
| CNRF | Cellule Nationale de Renseignement Financier |
| DL | Deep Learning |
| DSI | Direction des Systèmes d'Information |
| EDA | Exploratory Data Analysis |
| FRAUDX | Fraud Detection and eXplainability System |
| GIABA | Groupe Intergouvernemental d'Action contre le Blanchiment d'Argent |
| GPU | Graphics Processing Unit |
| HG | Hypothèse Générale |
| HS | Hypothèse Spécifique |
| IA | Intelligence Artificielle |
| IF | Isolation Forest |
| JWT | JSON Web Token |
| KYC | Know Your Customer |
| LBC/FT | Lutte contre le Blanchiment de Capitaux et le Financement du Terrorisme |
| LIME | Local Interpretable Model-agnostic Explanations |
| LSTM | Long Short-Term Memory |
| ML | Machine Learning |
| OS | Objectif Spécifique |
| OSI | Objectif Spécifique d'Intervention |
| OTP | One-Time Password |
| P2P | Peer-to-Peer |
| PCA | Principal Component Analysis |
| PoC | Proof of Concept |
| QG | Question Générale |
| QS | Question Spécifique |
| RBAC | Role-Based Access Control |
| RF | Random Forest |
| RGPD | Règlement Général sur la Protection des Données |
| ROI | Return On Investment |
| SHAP | SHapley Additive exPlanations |
| SIM | Subscriber Identity Module |
| SMOTE | Synthetic Minority Oversampling Technique |
| SWOT | Strengths, Weaknesses, Opportunities, Threats |
| UEMOA | Union Économique et Monétaire Ouest-Africaine |
| ULB | Université Libre de Bruxelles |
| USSD | Unstructured Supplementary Service Data |
| VI | Variable Indépendante |
| VD | Variable Dépendante |
| WAF | Web Application Firewall |
| XAI | eXplainable Artificial Intelligence |
| XGBoost | eXtreme Gradient Boosting |
