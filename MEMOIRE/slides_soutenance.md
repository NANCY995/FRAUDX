# Diapositives de soutenance — FRAUDX

**Fichier :** `FRAUDX_Soutenance.pptx` (30 diapos)
**Thème :** Fond sombre (#0F0F23), accents or (#F0B92B)
**Format :** 13,333 × 7,5 pouces (format large)

---

## Diapositive 1 — Page de titre
- **Titre :** CONCEPTION D'UN SYSTÈME D'IA POUR LA DÉTECTION DE LA FRAUDE BANCAIRE — CAS DU TOGO
- **Sous-titre :** Mémoire de fin d'études — Master
- **Année :** 2024-2025
- **Système :** FRAUDX — Preuve de Concept

---

## Diapositive 2 — SOMMAIRE
1. Contexte et problématique
2. Objectifs et hypothèses de recherche
3. Fondements théoriques (Ch. I)
4. Méthodologie (Ch. II)
5. Résultats expérimentaux (Ch. III)
6. Architecture FRAUDX & démo
7. Analyse diagnostique et intervention (Ch. IV)
8. Faisabilité et ROI
9. Limites et perspectives
10. Conclusion

---

## Partie I — CONTEXTE ET PROBLÉMATIQUE

### Diapositive 3 — 1.1 La digitalisation financière au Togo
- 8,2 M de comptes mobile money actifs (2023, ARCEP)
- TogoCom Cash, Moov Money, Flooz : canaux dominants
- Croissance 60% des comptes entre 2020-2023
- Taux de bancarisation ~28% vs >95% mobile money rural
- Fraudes : SIM swap (35%), ingénierie sociale (20%), carte (18%)
- Pertes : 3-5 milliards FCFA/an
- 23% des utilisateurs réduisent leur usage après une fraude

### Diapositive 4 — 1.2 Problématique
- **QS1 :** Quels algorithmes de ML sont les plus adaptés au contexte togolais ?
- **QS2 :** Comment concevoir une architecture sécurisée conforme BCEAO/UEMOA ?
- **QS3 :** Dans quelle mesure l'explicabilité SHAP facilite-t-elle l'adoption ?
- **QG :** Comment concevoir un système d'IA efficace, sécurisé et explicable ?

---

## Partie II — OBJECTIFS ET HYPOTHÈSES

### Diapositive 5 — 2.1 Hypothèses de recherche
- **HG :** L'ensemble learning améliore significativement la détection
- **HS1 :** XGBoost atteint Recall ≥ 85% ✅ Validée
- **HS2 :** Données locales améliorent la précision ❌ Non vérifiable
- **HS3 :** SHAP facilite l'adoption ✅ Validée (FP < 2%)

---

## Partie III — FONDEMENTS THÉORIQUES (Ch. I)

### Diapositive 6 — 3.1 Travaux connexes (revue de littérature)
- **Facci et al. (2024) — BNP Paribas :** XGBoost + SHAP en contexte réel
- **Moradi et al. (2025) — Stacking IEEE-CIS :** AUC-ROC = 0,918
- **Da (2024) & Dedam (2025) — UQTR :** ML pour fraude, Recall > 85%
- **FraudGuess (Qian, 2025) :** Micro-clustering + dashboard explicatif
- **StartBrain (2026) & Barry (2026) :** 95% détection, 80% baisse coûts IA

### Diapositive 7 — 3.2 Architecture algorithmique retenue
- **Niveau 1 — Isolation Forest :** Filtre rapide (< 0,1 ms/tx), 60% filtré
- **Niveau 2 — XGBoost :** Classification fine (483 features), seuil adaptatif
- **Niveau 3 — LSTM (Phase 2) :** Analyse temporelle (nécessite GPU)

### Diapositive 8 — 3.3 Explicabilité par SHAP
- Conformité réglementaire BCEAO/UEMOA
- Explication globale : top 15 features
- Explication locale : top 5 facteurs par alerte
- Variables clés : TransactionAmt, card6_credit, dayofweek, hour_of_day, V314/V40/V84

---

## Partie IV — MÉTHODOLOGIE (Ch. II)

### Diapositive 9 — 4.1 Approche et méthodes
- **Type :** Recherche mixte non expérimentale à visée explicative
- **Quantitatif :** IEEE-CIS (590K tx, 3,5% fraude), 5 modèles, Optuna 30 essais
- **Qualitatif :** Entretiens semi-directifs (5-8 professionnels)
- **Démo :** Streamlit Cloud — fraudx-memoirel3.streamlit.app

---

## Partie V — RÉSULTATS EXPÉRIMENTAUX (Ch. III)

### Diapositive 10 — 5.1 Comparaison des modèles
- F1-Score XGBoost : **0,607**
- Recall (seuil 0,325) : **85,02%**
- Précision : 13,54%
- AUC-PR : 0,574
- F1 Random Forest : 0,370
- F1 Isolation Forest : 0,161

### Diapositive 11 — 5.2 Optimisation Optuna et matrice de confusion
- F1 base 0,53 → 0,607 (+14,5%)
- Recall base 51,6% → 85,0%
- Seuil optimisé ~0,325
- 85% des fraudes détectées, 1,55% FP
- Inférence : 0,016 ms/tx
- **Comparaison :** Moradi (2025) AUC-ROC 0,918 vs notre AUC-ROC ~0,87

### Diapositive 12 — 5.3 Analyse SHAP : features importantes
- Top 5 : TransactionAmt (0,42), card6_credit (0,31), dayofweek (0,25), hour_of_day (0,18), addr1 (0,12)
- Transférabilité au Togo : montant universel, temporalité, localisation

---

## Partie VI — ARCHITECTURE FRAUDX & DÉMO

### Diapositive 13 — 6.1 Architecture du système FRAUDX
- **6 pages :** Dataset, Prétraitement, Entraînement, Résultats, Benchmark, Prédiction
- **Backend :** FastAPI (5 endpoints)
- **Déploiement :** Streamlit Cloud (gratuit, 1 Go RAM)
- **RBAC :** 3 niveaux (Analyste, Risk Manager, Admin)
- **Sécurité :** CORS restreint, auth par token, rate limiting 100 req/min, sanitisation XSS, requêtes SQL paramétrées, validation Pydantic, hash SHA-256

### Diapositive 14 — 6.2 Démonstration en direct
- 6 étapes de démonstration (8-10 min)
- URL : fraudx-memoirel3.streamlit.app

---

## Partie VII — ANALYSE DIAGNOSTIQUE ET INTERVENTION (Ch. IV)

### Diapositive 15 — 7.1 SWOT
- **Forces :** KYC, réseaux agents MM, conformité AML, exigences BCEAO/UEMOA
- **Faiblesses :** Règles statiques, faible couverture MM, analyse manuelle, délais J+7, FP > 15%
- **Opportunités :** Digitalisation, datasets publics, ML open source, régulateurs, intérêt IA
- **Menaces :** Sophistication fraudes, SIM swap, ingénierie sociale, infrastructure, fuite talents

### Diapositive 16 — 7.2 Vérification des hypothèses
- **HG :** Partiellement validée
- **HS1 :** Validée ✅ (Recall=85,02%)
- **HS2 :** Non vérifiable (perspective)
- **HS3 :** Validée ✅ (FP 1,55%)

---

## Partie VIII — FAISABILITÉ ET ROI

### Diapositive 17 — 8.1 Plan de déploiement progressif
- Phase pilote (M1-6) : 1 banque, ~104K€
- Extension MM (M7-12) : TogoCom Cash, Moov, Flooz
- Généralisation (M13-24) : 3-5 banques

### Diapositive 18 — 8.2 Budget et ROI
- Budget total : 177 000 € sur 3 ans
- Économie annuelle estimée : 200 000 €
- **ROI : 239%** sur 3 ans

---

## Partie IX — LIMITES ET PERSPECTIVES

### Diapositive 19 — 9.1 Limites assumées
1. Absence validation données réelles togolaises
2. Échantillon qualitatif restreint
3. Non-implantation LSTM (GPU nécessaire)
4. Budget estimé non contractuel

### Diapositive 20 — 9.2 Perspectives
1. Partenariat banque/opérateur MM togolais
2. Extension UEMOA
3. Federated Learning
4. Deep Learning (LSTM, Transformers)

---

## Diapositive 21 — CONCLUSION
- ✓ FRAUDX déployé sur Streamlit Cloud
- ✓ Recall 85%, F1=0,607, AUC-PR=0,574
- ✓ SHAP intégré, FP < 2%
- ✓ Architecture 3 niveaux validée
- ✓ ROI 239% sur 3 ans
- **→ L'IA n'est pas une option mais une nécessité**

---

**Diapos supplémentaires** (sans numérotation) : 9 séparateurs de parties (I à IX), total 30 diapos.
