## RÉSUMÉ

Dans un monde où la digitalisation financière transforme en profondeur les relations bancaires, la détection de la fraude représente à la fois un enjeu de sécurité et un défi majeur pour les institutions financières. Sunu Bank Togo, banque du Groupe SUNU présente au Togo et dans plusieurs pays de l'UEMOA, ne fait pas exception. Confrontée à une recrudescence des fraudes bancaires et numériques face auxquelles les méthodes traditionnelles de détection — règles statiques, contrôles manuels — montrent leurs limites, cette banque peine à exploiter pleinement le potentiel des technologies d'intelligence artificielle pour sécuriser ses transactions et protéger sa clientèle. Ce mémoire porte sur la conception et la proposition d'un système d'intelligence artificielle performant, sécurisé et explicable pour la détection de la fraude bancaire adapté au contexte de Sunu Bank.

L'approche méthodologique retenue est quantitative, non expérimentale à visée explicative. L'analyse compare trois algorithmes de Machine Learning — Isolation Forest, Random Forest et XGBoost — sur le dataset public IEEE-CIS Fraud Detection, en utilisant SMOTE pour le rééquilibrage des classes et SHAP pour l'explicabilité.

Les résultats montrent la supériorité de XGBoost après optimisation du seuil de décision (Recall = 85,02 % ; Précision = 13,54 % ; F1-Score = 0,23 ; AUC-PR = 0,57), avec une latence de prédiction compatible avec les exigences du temps réel. Une preuve de concept fonctionnelle (FRAUDX) a été développée, intégrant un tableau de bord interactif avec contrôle d'accès RBAC, un module SHAP d'explicabilité des décisions et un module de feedback pour l'apprentissage continu.

Si le périmètre conceptuel de l'étude inclut les transactions bancaires classiques et le mobile money, le modèle est entraîné sur un dataset international de transactions par carte (IEEE-CIS) faute de données réelles togolaises accessibles — une limite explicitement reconnue dont l'intégration des spécificités du mobile money constitue la perspective prioritaire.

Cette recherche contribue au domaine émergent de l'IA appliquée à la détection de fraude bancaire en contexte africain, en démontrant la faisabilité technique et le potentiel économique d'une solution adaptée aux contraintes des banques ouest-africaines.

**Mots-clés :** Détection de fraude bancaire, Machine Learning, XGBoost, Ensemble Learning, SHAP, Sunu Bank, Togo, RBAC, Explicabilité (XAI).

---

## ABSTRACT

In a world where financial digitalization is profoundly reshaping banking relationships, fraud detection represents both a security challenge and a major strategic issue for financial institutions. Sunu Bank Togo, a member of the Sunu Group operating in Togo and several WAEMU countries, is no exception. Faced with a resurgence of banking and digital fraud against which traditional detection methods — static rules, manual controls — are proving inadequate, this bank struggles to fully harness the potential of artificial intelligence technologies to secure its transactions and protect its customers. This thesis focuses on the design and proposal of a high-performance, secure, and explainable artificial intelligence system for banking fraud detection tailored to the context of Sunu Bank.

The methodological approach is quantitative, non-experimental, and explanatory in nature. The analysis compares three Machine Learning algorithms — Isolation Forest, Random Forest, and XGBoost — on the public IEEE-CIS Fraud Detection dataset, using SMOTE for class balancing and SHAP for explainability.

Results demonstrate the superiority of XGBoost after threshold optimization (Recall = 85.02%; Precision = 13.54%; F1-Score = 0.23; AUC-PR = 0.57), with a prediction latency meeting real-time requirements. A functional proof of concept (FRAUDX) was developed, featuring an interactive dashboard with RBAC access control, a SHAP explainability module, and a feedback loop for continuous learning.

While the conceptual scope of the study includes both banking and mobile money transactions, the model is trained on an international credit card transaction dataset (IEEE-CIS) due to the unavailability of real Togolese data — a limitation explicitly acknowledged, with the integration of mobile money specifics identified as the primary future direction.

This research contributes to the emerging field of AI applied to banking fraud detection in the African context, by demonstrating the technical feasibility and economic potential of a solution adapted to the constraints of West African banks.

**Keywords:** Banking fraud detection, Machine Learning, XGBoost, Ensemble Learning, SHAP, Sunu Bank, Togo, RBAC, Explainable AI (XAI).
