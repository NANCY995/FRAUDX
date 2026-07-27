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

1. **Le faux transfert Mobile Money** : l'arnaqueur prétend avoir envoyé de l'argent par erreur sur le compte de la victime — parfois en s'appuyant sur une fausse notification fabriquée ou détournée — et exerce une pression pour obtenir un remboursement immédiat, avant que la victime n'ait pu vérifier son solde réel (ANCY, 2025a).

2. **L'usurpation d'agent** : le fraudeur se fait passer pour un représentant agréé d'un opérateur mobile money (T-Money, Flooz, Mixx by Yas ou Moov Money) afin d'obtenir un code de validation ou un code secret censé rester confidentiel (ANCY, 2025b).

3. **La fausse réidentification** : ce schéma combine manipulation psychologique et exploitation d'un mécanisme technique légitime — la victime reçoit un véritable SMS de validation pendant l'appel frauduleux, puis l'escroc l'incite à communiquer ce code sous prétexte de réidentification de compte, ce qui lui permet de détourner le solde (ANCY, 2025b).

4. **Les plateformes frauduleuses de vente ou d'investissement** : les victimes sont incitées à effectuer des dépôts via Mobile Money pour percevoir des « commissions », valider des « commandes » ou bénéficier d'un système de « parrainage », avant d'être bloquées par les opérateurs de la plateforme (CERT-TG, 2025).

Ce qui rend ces fraudes particulièrement spécifiques au contexte togolais tient à leur ancrage dans les pratiques locales. Les escrocs utilisent des numéros de téléphone locaux, un discours en français courant et des références aux opérateurs connus du pays afin d'instaurer un climat de confiance. Ils s'adressent aussi bien aux particuliers qu'aux commerçants et aux petites entreprises, en profitant de la rapidité des transactions et du réflexe d'exécution immédiate qu'impose souvent le mobile money (ANCY, 2025a). Le facteur temporel joue ici un rôle essentiel : la victime est poussée à agir sans vérification préalable, ce qui renforce l'efficacité de la fraude. Les autorités togolaises rappellent à cet égard qu'un agent mobile money légitime ne demande jamais de code secret ou de code de validation par téléphone (Togo Breaking News, 2025).

Ces observations montrent que la fraude mobile money au Togo relève davantage d'une exploitation des usages sociaux et comportementaux que d'attaques purement techniques. Toutefois, des formes plus techniques de fraude, telles que le SIM-swap ou certaines manipulations liées aux services USSD, demeurent des risques potentiels dans la sous-région et peuvent également concerner le Togo, même si les alertes récentes mettent surtout en évidence la prépondérance des arnaques par ingénierie sociale. Le SIM-swap — obtention frauduleuse d'une carte SIM de remplacement permettant d'intercepter les codes OTP — a ainsi été largement documenté dans d'autres pays de la sous-région, notamment au Nigéria, en Afrique du Sud et au Cameroun (Nkolwoudou Afane, 2025), sans qu'une ampleur comparable n'ait à ce jour été établie pour le Togo. De même, la fraude par USSD, où des fraudeurs se faisant passer pour des agents de service client obtiennent par ingénierie sociale les codes nécessaires pour vider un compte, reste un vecteur théoriquement possible compte tenu de la centralité de ce canal dans les transactions mobile money togolaises.

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

Le premier tient à la forte diffusion de ce canal dans les usages financiers quotidiens. Le mobile money s'est imposé comme un moyen privilégié pour le rechargement de crédit téléphonique, les transferts d'argent, les paiements de factures et les transactions marchandes, ce qui augmente mécaniquement la surface d'exposition à la fraude. Selon une enquête de l'ARCEP relayée par Togo First (2024), le Togo comptait 3,55 millions d'utilisateurs mobile money en 2024, répartis entre T-Money, opéré par Togo Cellulaire (2,16 millions d'utilisateurs), et Flooz, opéré par Moov Africa Togo (1,4 million d'utilisateurs). Cette même enquête révèle que 86 % des abonnés mobiles disposent d'un compte mobile money, principalement mobilisé pour les recharges de crédit (89 %), les paiements de factures (86 %) et les transactions financières courantes (81 %).

Le deuxième facteur est la dépendance persistante aux canaux téléphoniques classiques — SMS et appels vocaux — pour valider ou accompagner certaines opérations. Cette configuration favorise les arnaques fondées sur l'ingénierie sociale, telles que documentées par l'Agence Nationale de Cybersécurité (ANCY, 2025a, 2025b) : les fraudeurs exploitent la confiance des usagers, la rapidité des échanges et la pression temporelle inhérente au canal pour pousser la victime à agir sans vérification préalable. Dans ce contexte, la fraude ne repose donc pas seulement sur une faiblesse technique, mais avant tout sur la manipulation du comportement humain.

Un troisième élément de vulnérabilité concerne les limites des mécanismes de protection et de sensibilisation des usagers. La même enquête de l'ARCEP (citée par Togo First, 2024) montre que les coûts élevés des transactions constituent un frein pour 81 % des sondés, tandis que le manque d'interopérabilité entre T-Money et Flooz en constitue un pour 75 % d'entre eux. Pour environ la moitié des clients de chaque opérateur, des problèmes de confiance ou de sécurité, ainsi que des plafonds mensuels jugés trop bas, représentent également des obstacles à un usage optimal du service. Il en résulte que la fraude prospère dans un système à la fois très utilisé, très rapide, et encore insuffisamment maîtrisé par une partie des utilisateurs — un déséquilibre entre l'intensité d'adoption du canal et la maturité de ses mécanismes de protection.

Enfin, l'ampleur de cette fraude doit être replacée dans le cadre plus large de la transformation numérique du secteur financier togolais. Les institutions qui s'appuient encore sur des règles métier statiques et des contrôles manuels disposent de moyens limités pour suivre l'évolution rapide des schémas frauduleux, qu'il s'agisse des variantes d'ingénierie sociale décrites précédemment ou de formes plus techniques susceptibles d'émerger. Cette situation justifie le recours à des approches plus adaptatives, telles que le Machine Learning, afin d'améliorer la détection précoce des transactions suspectes et de réduire les pertes qui y sont associées — un enjeu au cœur de la présente étude.

### I.1.2. Le Machine Learning appliqué à la détection de fraude

Le Machine Learning est une branche de l'intelligence artificielle qui permet à des systèmes d'apprendre et de s'améliorer à partir de données, sans être explicitement programmés pour chaque tâche (Samuel, 1959). Appliqué à la détection de fraude, il permet de dépasser les limites des règles métier statiques en identifiant des régularités statistiques complexes dans le comportement transactionnel, y compris des schémas qui n'ont pas été anticipés par un expert humain.

#### I.1.2.1. Apprentissage supervisé, non supervisé et hybride

Trois paradigmes d'apprentissage sont pertinents pour la détection de fraude :

- **L'apprentissage supervisé** : le modèle est entraîné sur des données labellisées (transactions marquées comme frauduleuses ou non frauduleuses) pour apprendre à classifier de nouvelles transactions. Les algorithmes comme XGBoost et Random Forest appartiennent à cette catégorie.
- **L'apprentissage non supervisé** : le modèle identifie des anomalies dans les données sans disposer d'étiquettes préalables. Isolation Forest est un exemple typique, adapté aux situations où les données frauduleuses sont rares ou non identifiées.
- **L'apprentissage par renforcement** : le modèle apprend par essais et erreurs en interagissant avec son environnement. Moins utilisé en détection de fraude, il trouve des applications dans les systèmes adaptatifs.

Le choix du paradigme dépend de la disponibilité des données labellisées et de la nature du problème à résoudre. Dans notre étude, l'approche comparative (supervisé + non supervisé) permet de tirer parti des avantages complémentaires de chaque paradigme, en confrontant un filtre d'anomalies non supervisé (Isolation Forest) à deux classifieurs supervisés (Random Forest et XGBoost).

#### I.1.2.2. Détection d'anomalies et gestion du déséquilibre des classes

La détection de fraude présente une contrainte structurelle commune à l'ensemble des jeux de données du domaine : le déséquilibre extrême des classes, les transactions frauduleuses représentant généralement moins de 1 % du volume total. Dans ces conditions, un modèle naïf qui classerait systématiquement une transaction comme non frauduleuse atteindrait une accuracy proche de 99 %, tout en étant totalement inefficace pour détecter la fraude — ce qui disqualifie l'Accuracy comme métrique d'évaluation pertinente.

Dans ce contexte, les métriques adaptées sont le Recall, le F1-Score et l'AUC-PR, qui privilégient la détection de la classe minoritaire sans être biaisées par le déséquilibre de classes. Deux approches complémentaires permettent de répondre à ce déséquilibre : la détection d'anomalies non supervisée, qui exploite la rareté statistique des comportements frauduleux sans nécessiter d'étiquetage préalable, et le rééquilibrage artificiel des données d'entraînement par sur-échantillonnage synthétique.

#### I.1.2.3. Algorithmes retenus : Isolation Forest, Random Forest et XGBoost

**Détection d'anomalies par Isolation Forest**

L'Isolation Forest (Liu et al., 2008, 2012) est un algorithme non supervisé spécifiquement conçu pour la détection d'anomalies. Plusieurs revues récentes confirment la pertinence de ces approches pour la détection de fraude financière (Chen et al., 2025). Contrairement aux méthodes traditionnelles qui construisent un profil de la normalité puis identifient les déviations, l'Isolation Forest isole directement les anomalies en exploitant leur rareté et leur différence.

Le principe de l'Isolation Forest repose sur l'idée que les anomalies sont plus faciles à isoler que les points normaux. L'algorithme construit une forêt d'arbres de décision aléatoires (Isolation Trees). Pour chaque arbre, une caractéristique aléatoire est sélectionnée, une valeur de coupure aléatoire est choisie entre les valeurs minimale et maximale de cette caractéristique, puis les données sont divisées récursivement jusqu'à ce que chaque observation soit isolée. Comme les anomalies sont rares et différentes, elles nécessitent moins de partitions pour être séparées et apparaissent donc à des profondeurs plus faibles, ce qui permet de les identifier efficacement.

Ses avantages pour la détection de fraude tiennent à son fonctionnement sans données labellisées, à sa faible complexité computationnelle (O(n log n)), à sa performance sur des jeux de données de grande dimension, et à sa robustesse face au déséquilibre des classes. Ses limites résident dans sa sensibilité au paramètre de contamination, dans le risque de manquer des fraudes subtiles ressemblant à des transactions normales, et dans l'absence d'explication intrinsèque de ses décisions.

**Random Forest pour la classification**

Le Random Forest (Breiman, 2001) est un algorithme d'ensemble learning supervisé qui construit une multitude d'arbres de décision et agrège leurs prédictions. Chaque arbre est entraîné sur un échantillon bootstrap des données d'entraînement, et à chaque nœud de l'arbre, un sous-ensemble aléatoire des caractéristiques est considéré pour la division.

Le principe du Random Forest repose sur la construction d'une multitude d'arbres de décision indépendants, chacun entraîné sur un échantillon bootstrap des données d'apprentissage. À chaque nœud de ces arbres, un sous-ensemble aléatoire de caractéristiques est sélectionné pour déterminer la meilleure division, ce qui introduit de la diversité et réduit la corrélation entre les arbres. Lorsqu'une nouvelle transaction doit être classée, chaque arbre vote pour une classe (fraude ou normale), et la prédiction finale est obtenue par agrégation, généralement selon la majorité des votes.

Ses avantages tiennent à sa robustesse au sur-apprentissage, à sa gestion naturelle des relations non linéaires et des interactions entre variables, à l'importance intrinsèque des variables qu'il fournit (feature importance), et à sa parallélisabilité sur de grands volumes de données. Ses limites résident dans une performance généralement inférieure au boosting sur des données fortement déséquilibrées, une taille de modèle importante, une interprétabilité moindre qu'un arbre unique, et la nécessité d'un réglage fin des hyperparamètres.

**XGBoost : standard industriel actuel**

XGBoost (eXtreme Gradient Boosting), introduit par Chen & Guestrin (2016), est un algorithme d'ensemble learning supervisé basé sur le gradient boosting. Il construit séquentiellement une série d'arbres de décision, chaque nouvel arbre corrigeant les erreurs des arbres précédents.

Le principe de XGBoost repose sur une approche de boosting séquentiel : au lieu de construire des arbres indépendants comme dans le Random Forest, il génère une série d'arbres de décision où chaque nouvel arbre est entraîné pour corriger les erreurs (résidus) commises par les arbres précédents. À chaque itération, le modèle cherche à minimiser une fonction objectif composée de deux termes : le premier mesure l'erreur de prédiction, tandis que le second régularise la complexité du modèle afin de limiter le sur-apprentissage. Ce processus itératif permet d'améliorer progressivement la performance du modèle en affinant la prédiction à chaque étape.

Ses avantages clés pour la détection de fraude incluent la gestion avancée des données déséquilibrées via le paramètre scale_pos_weight, une régularisation intégrée (L1 et L2) qui réduit le sur-apprentissage, une gestion native des valeurs manquantes, des algorithmes optimisés pour la vitesse d'entraînement, et une capacité à capturer des interactions complexes entre variables.

XGBoost a remporté de nombreuses compétitions Kaggle et est devenu l'algorithme de référence pour les problèmes de classification sur données tabulaires, incluant la détection de fraude. Sa combinaison de performance prédictive, de robustesse et de rapidité en fait un choix naturel pour notre étude.

Des travaux récents confirment l'efficacité de XGBoost en contexte bancaire réel. Facci et al. (2024, hal-04939824), de BNP Paribas Personal Finance, proposent une approche couplant un réseau de neurones de graphe (GraphSAGE) à XGBoost ou Random Forest pour détecter la fraude sur les paiements fractionnés e-commerce. Leurs résultats sur données réelles anonymisées montrent que le couplage GNN + ensemble learning surpasse XGBoost seul, ouvrant la voie à des architectures hybrides.

Dans une autre étude comparative portant sur 17 modèles de ML/DL appliqués à la détection de blanchiment d'argent, Chergui et al. (2022) et les travaux ultérieurs (APIA, 2024) confirment que les arbres de décision boostés (XGBoost, LightGBM, CatBoost) atteignent jusqu'à 90 % de fiabilité et d'efficacité opérationnelle, se distinguant parmi l'ensemble des modèles testés. En parallèle, Dedam (2025), dans son mémoire à l'Université du Québec à Trois-Rivières, compare XGBoost à TabNet et aux auto-encodeurs pour la détection de fraude financière, confirmant la pertinence du gradient boosting face aux approches par deep learning.

Dans un mémoire récent portant sur le même domaine, Da (2024) propose une approche de détection efficace et robuste des fraudes bancaires par apprentissage automatique, en traitant spécifiquement le défi du déséquilibre des données et du rééquilibrage par méthodes contradictoires. Ce travail confirme la pertinence des axes de recherche explorés dans la présente étude et souligne l'importance de la robustesse des modèles face aux évolutions des schémas de fraude.

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

SMOTE (Synthetic Minority Oversampling Technique), proposé par Chawla et al. (2002), est une technique de rééquilibrage synthétique. Contrairement au sur-échantillonnage aléatoire qui duplique les exemples de la classe minoritaire, SMOTE génère des exemples synthétiques en interpolant entre les observations existantes de la classe minoritaire.

Le principe de SMOTE consiste à générer artificiellement de nouveaux exemples pour la classe minoritaire afin de rééquilibrer les données. Pour chaque observation de cette classe, on identifie ses k plus proches voisins appartenant également à la classe minoritaire. Ensuite, on calcule le vecteur de différence entre l'exemple et l'un de ses voisins, puis on crée un nouvel exemple synthétique en ajoutant à l'observation initiale une fraction aléatoire de ce vecteur. Ce procédé enrichit l'espace des caractéristiques de la classe minoritaire en produisant des points intermédiaires réalistes, ce qui permet de mieux représenter cette classe dans l'ensemble d'apprentissage. Cette approche présente l'avantage de générer des exemples réalistes qui enrichissent l'espace des caractéristiques de la classe minoritaire, sans tomber dans la duplication pure qui favoriserait le sur-apprentissage.

D'autres techniques de rééquilibrage existent, notamment le Cost-Sensitive Learning, qui assigne des poids de coût plus élevés aux erreurs de classification sur la classe minoritaire plutôt que de modifier la distribution des données. Dedam (2025) compare ces approches et montre que le Cost-Sensitive Learning peut constituer une alternative efficace à SMOTE dans certains contextes, bien que SMOTE reste privilégié pour sa simplicité d'implémentation et sa compatibilité avec les modèles arborescents comme XGBoost.

### I.1.3. L'explicabilité (XAI) des modèles d'IA dans la finance

#### I.1.3.1. Pourquoi expliquer les décisions algorithmiques ?

L'explicabilité des modèles d'IA (XAI — eXplainable Artificial Intelligence) est devenue un enjeu central du déploiement des systèmes intelligents dans le secteur bancaire. Selon StartBrain (2026), les banques opèrent dans un cadre réglementaire dense — RGPD, AI Act, directives LCB-FT — où chaque modèle de scoring, chaque algorithme de détection doit être explicable, auditable et conforme. L'AI Act européen classe d'ailleurs le scoring de crédit et la détection de fraude parmi les systèmes à haut risque, imposant documentation, audit de biais et contrôle humain obligatoire. Plusieurs facteurs expliquent cette importance croissante :

- **Exigences réglementaires** : les régulateurs (BCEAO, UEMOA, mais aussi GDPR en Europe) exigent que les décisions automatisées affectant les clients puissent être expliquées et justifiées.
- **Confiance des analystes** : les gestionnaires de risques et analystes fraude doivent pouvoir comprendre pourquoi une transaction a été marquée comme suspecte pour valider ou infirmer l'alerte.
- **Auditabilité** : les décisions du système doivent pouvoir être tracées et vérifiées a posteriori.
- **Amélioration continue** : la compréhension des erreurs du modèle permet d'orienter les efforts d'amélioration.

#### I.1.3.2. Les principales approches de XAI

La littérature distingue plusieurs familles de méthodes d'explicabilité. Les méthodes intrinsèques exploitent la structure même du modèle (feature importance des arbres de décision, coefficients d'une régression logistique) mais restent limitées face aux modèles d'ensemble complexes. Les méthodes post-hoc, appliquées après l'entraînement, permettent d'expliquer n'importe quel modèle indépendamment de son architecture ; parmi elles, LIME (Local Interpretable Model-agnostic Explanations) approxime localement le comportement du modèle par un modèle linéaire simple, tandis que SHAP, fondé sur la théorie des jeux, offre des garanties mathématiques de cohérence plus fortes. C'est cette dernière approche qui a été retenue pour la présente étude, et qui est détaillée dans la section suivante.

#### I.1.3.3. SHAP (SHapley Additive exPlanations) comme outil d'interprétation des modèles de fraude

SHAP, développé par Lundberg & Lee (2017), est une méthode d'explicabilité basée sur la théorie des jeux coopératifs. Elle attribue à chaque caractéristique une valeur d'importance (SHAP value) qui représente sa contribution à la décision du modèle pour une prédiction donnée.

**Fondement théorique :**

SHAP s'appuie sur les valeurs de Shapley (Shapley, 1953), un concept de théorie des jeux qui distribue équitablement la valeur totale créée par une coalition entre ses membres. Dans le contexte du Machine Learning, chaque caractéristique est considérée comme un "joueur", et la prédiction du modèle comme la "valeur créée" par la coalition des caractéristiques.

La valeur SHAP φᵢ pour une caractéristique i est calculée comme la moyenne pondérée, sur tous les sous-ensembles possibles de caractéristiques ne contenant pas i, de la contribution marginale apportée par l'ajout de i à ce sous-ensemble :

φᵢ = Σ (S⊆N{i}) [ |S|!(|N|−|S|−1)! / |N|! ] × [f(S∪{i}) − f(S)]

Où :
- N = ensemble de toutes les caractéristiques
- S = sous-ensemble de caractéristiques qui ne contient pas i
- f(S) = prédiction du modèle en utilisant uniquement les caractéristiques de S
- φᵢ = valeur SHAP de la caractéristique i, c'est-à-dire sa contribution moyenne à la prédiction

**TreeExplainer pour XGBoost :**

Pour les modèles arborescents comme XGBoost et Random Forest, SHAP propose une implémentation optimisée appelée TreeExplainer (Lundberg et al., 2020), qui calcule exactement les valeurs SHAP en parcourant les arbres, avec une complexité polynomiale plutôt qu'exponentielle, rendant son usage praticable à l'échelle d'un système de production.

#### I.1.3.4. XAI et adoption par les analystes financiers

L'application de SHAP à la détection de fraude présente trois avantages majeurs :

1. **Explication individuelle** : pour chaque transaction, SHAP identifie les variables qui ont poussé le modèle vers une prédiction de fraude ou de normalité, avec leur contribution quantitative.
2. **Vision globale** : l'agrégation des valeurs SHAP sur l'ensemble des prédictions permet d'identifier les variables les plus importantes pour le modèle dans son ensemble.
3. **Conformité réglementaire** : les explications SHAP fournissent une traçabilité transparente des décisions, répondant aux exigences des régulateurs.

Dans le cadre de ce mémoire, SHAP est utilisé pour répondre à l'hypothèse spécifique 3, en démontrant que l'explicabilité des décisions du modèle peut faciliter l'adoption du système par les analystes financiers togolais.

Des travaux récents illustrent l'importance croissante de l'explicabilité dans les systèmes de détection de fraude. Le système FraudGuess (Qian et al., 2025, arXiv 2509.15493), déployé dans une institution financière anonyme, combine détection de nouveaux types de fraude via du micro-clustering avec un tableau de bord interactif fournissant des explications visuelles et des heatmaps aux analystes. Ce système a permis de découvrir trois nouveaux comportements frauduleux inconnus jusqu'alors, démontrant que l'explicabilité ne sert pas seulement la conformité mais aussi la découverte de nouveaux schémas de fraude.

De même, le framework SAGE (Chen et al., 2026, arXiv 2606.08146) propose une approche multi-agents pilotée par LLM pour la détection de fraude, avec un accent sur l'interprétabilité des décisions individuelles — améliorant le F1 de 40,86 % par rapport aux bases de référence.

### I.1.4. Cadre légal et réglementaire

#### I.1.4.1. Réglementation bancaire BCEAO/UEMOA

La Banque Centrale des États de l'Afrique de l'Ouest (BCEAO) et l'Union Économique et Monétaire Ouest-Africaine (UEMOA) ont émis plusieurs directives encadrant les activités bancaires et les systèmes de paiement dans l'espace communautaire :

- La Directive N°01/2018/CM/UEMOA relative aux systèmes de paiement dans les États membres de l'UEMOA, qui établit les exigences minimales de sécurité pour les transactions électroniques.
- La Loi Uniforme sur la Lutte contre le Blanchiment de Capitaux et le Financement du Terrorisme (LBC/FT) qui impose aux institutions financières la mise en place de dispositifs de contrôle et de détection des opérations suspectes.
- Le Règlement N°01/2020/CM/UEMOA sur les services de paiement mobile, qui encadre spécifiquement les activités des opérateurs de mobile money.

#### I.1.4.2. Dispositifs LBC/FT et rôle du GIABA

Le Groupe Intergouvernemental d'Action contre le Blanchiment d'Argent en Afrique de l'Ouest (GIABA) est l'organe régional de lutte contre le blanchiment de capitaux. Ses recommandations, alignées sur les standards du GAFI (Groupe d'Action Financière), imposent aux institutions financières :

- La mise en œuvre de procédures KYC (Know Your Customer) rigoureuses
- La déclaration des opérations suspectes aux cellules de renseignement financier
- La conservation des données transactionnelles pour une durée minimale de 10 ans
- L'évaluation périodique des risques de blanchiment et de financement du terrorisme

#### I.1.4.3. Protection des données personnelles au Togo

Le Togo s'est doté d'une loi sur la protection des données à caractère personnel (Loi N°2020-003 du 20 février 2020), qui encadre la collecte, le traitement et la conservation des données personnelles. Cette loi, alignée sur le Règlement Général sur la Protection des Données (RGPD) européen, impose notamment :

- Le consentement préalable des personnes concernées
- La limitation de la collecte aux données strictement nécessaires
- Le droit d'accès, de rectification et d'opposition des personnes
- La sécurisation des données par des mesures techniques appropriées

#### I.1.4.4. Exigences de conformité pour les systèmes de détection automatisée

Au-delà du cadre sectoriel propre à l'UEMOA, les banques opèrent désormais dans un cadre réglementaire international dense, où chaque modèle de scoring et chaque algorithme de détection doit être explicable, auditable et conforme. L'AI Act européen constitue d'ailleurs un cadre de référence — une orientation réglementaire qui, sans s'appliquer directement au Togo, préfigure les standards internationaux vers lesquels les régulateurs régionaux (BCEAO, UEMOA, GIABA) tendent à converger. Ces exigences combinées justifient le choix méthodologique opéré dans ce mémoire d'associer systématiquement performance algorithmique et explicabilité, plutôt que de considérer la conformité comme une contrainte externe traitée a posteriori.

## I.2. Historique et évolution du domaine

Après avoir défini les concepts mobilisés dans ce mémoire, il convient de les resituer dans une perspective chronologique. Cette section s'appuie sur trois types de sources : les revues de littérature internationales sur la fraude bancaire et le Machine Learning, les rapports institutionnels (BCEAO, FMI, Centif, autorités de cybersécurité), et les sources sectorielles (solutions industrielles, régulateurs). Elle retrace, d'une part, l'évolution des fraudes financières, de leurs formes les plus anciennes jusqu'aux schémas contemporains observés au Togo, et d'autre part, l'évolution parallèle des approches de détection, des règles métier statiques jusqu'aux approches hybrides et explicables dans lesquelles s'inscrit la présente étude. Ces deux trajectoires — celle de la menace et celle de la réponse technologique — ne sont pas indépendantes : chaque avancée dans les méthodes de détection a généralement précédé une adaptation des schémas frauduleux, dans une dynamique de coévolution que cette section vise à documenter.

### I.2.1. Évolution des fraudes financières

#### I.2.1.1. De la fraude traditionnelle à la fraude numérique

La fraude bancaire a longtemps été dominée par des formes physiques et documentaires — falsification de chèques, contrefaçon de cartes, usurpation d'identité par vol de documents. Bolton & Hand (2002), dans l'une des références fondatrices de la détection statistique de fraude, décrivent cette période comme caractérisée par des mécanismes de contrôle essentiellement rétrospectifs, où la fraude n'était souvent identifiée qu'a posteriori, lors du rapprochement bancaire ou de la réclamation du client.

La numérisation progressive des services financiers, à partir des années 2000, a déplacé le centre de gravité de la fraude vers des vecteurs électroniques. Cette transition est confirmée par les analyses de synthèse sur la fraude bancaire, qui mettent en évidence la diminution relative des fraudes physiques au profit des fraudes sur cartes et paiements en ligne, en lien avec la digitalisation des services financiers. Bhattacharyya et al. (2011) documentent cette transition à travers l'exemple emblématique de la fraude par carte bancaire, montrant comment la multiplication des canaux de paiement électronique a ouvert de nouvelles surfaces d'attaque, tandis que Dal Pozzolo et al. (2014, 2015) approfondissent cette analyse en insistant sur les défis spécifiques posés par ces nouvelles fraudes numériques : volumétrie croissante des transactions, nécessité d'une détection en temps réel, et surtout déséquilibre extrême des classes entre transactions légitimes et frauduleuses.

Plus récemment, la revue systématique d'Ogunleye et al. (2022) synthétise l'ensemble de ces évolutions et montre un glissement net, dans la littérature des dix dernières années, des méthodes de détection fondées sur des règles ou des statistiques classiques vers des approches de Machine Learning capables de traiter la complexité et le volume des données transactionnelles modernes. Cette transition n'a cependant pas supprimé les formes traditionnelles de fraude, mais les a fait coexister avec des schémas exploitant les nouvelles surfaces d'attaque ouvertes par la digitalisation bancaire — une coexistence qui se retrouve, sous une forme particulière, dans le contexte togolais.

#### I.2.1.2. Montée du mobile money en Afrique de l'Ouest

En Afrique de l'Ouest, cette trajectoire générale s'est doublée d'une dynamique propre : l'essor du mobile money, qui a permis un saut d'étape technologique en offrant des services financiers à des populations largement non bancarisées, sans passer par l'étape intermédiaire de la bancarisation classique. Les rapports de la Banque Centrale des États de l'Afrique de l'Ouest (BCEAO, 2022, 2023, 2024) décrivent cette montée en puissance comme l'un des phénomènes structurants de la décennie pour l'inclusion financière régionale, portée par la multiplication des établissements de monnaie électronique et par des partenariats croissants entre opérateurs de télécommunications et banques traditionnelles.

Au Togo, cette dynamique régionale s'est traduite par une adoption particulièrement rapide. Selon les données les plus récentes de la BCEAO (2024), le pays affichait fin 2024 le taux de comptes actifs le plus élevé de l'espace UEMOA (48,35 %) ainsi que la plus forte progression annuelle de comptes actifs de l'Union (+76,87 % entre 2023 et 2024). À l'échelle des utilisateurs, une enquête de l'ARCEP relayée par Togo First (2024) précise que le Togo comptait 3,55 millions d'utilisateurs mobile money en 2024, répartis entre T-Money (2,16 millions) et Flooz (1,4 million), avec 86 % des abonnés mobiles disposant d'un compte mobile money. Il convient de noter que ces deux sources ne mesurent pas rigoureusement la même réalité — la BCEAO comptabilise des comptes de monnaie électronique ouverts par des établissements émetteurs, tandis que l'ARCEP recense des utilisateurs uniques par opérateur de téléphonie — mais convergent pour établir l'ampleur exceptionnelle de l'adoption togolaise à l'échelle régionale.

Cette expansion rapide a mécaniquement élargi la surface d'exposition à la fraude, sans que les dispositifs de sécurité et de détection ne progressent nécessairement au même rythme. Les autorités monétaires et de supervision financière (BCEAO, FMI, GIABA) reconnaissent désormais le mobile money comme un vecteur central d'inclusion financière, mais également comme un canal exposé aux risques de fraude, de blanchiment et de financement illicite — un constat que confirment les facteurs de vulnérabilité déjà exposés (coûts de transaction élevés, interopérabilité imparfaite entre opérateurs, confiance encore fragile d'une partie des usagers).

#### I.2.1.3. Transformation des schémas frauduleux avec le numérique

Le passage au mobile money a transformé la nature même des schémas frauduleux observés, dans un mouvement plus large déjà documenté à l'échelle internationale par Kim et al. (2021), dont la revue de la fraude dans l'écosystème du paiement mobile souligne que la multiplication des canaux (USSD, applications, agents physiques) diversifie mécaniquement les points d'entrée exploitables par les fraudeurs. Jurgovsky et al. (2018) apportent un éclairage complémentaire en montrant que la séquence des transactions d'un même client devient elle-même un indicateur de risque déterminant.

Au Togo spécifiquement, cette transformation est documentée avec une précision inédite par les alertes officielles diffusées en 2025 par l'Agence Nationale de Cybersécurité (ANCY, 2025a, 2025b) et par le Centre Togolais de Réponse aux Incidents de Sécurité Informatique (CERT-TG, 2025). Les rapports de la Cellule Nationale de Traitement des Informations Financières (Centif) et les synthèses économiques estiment par ailleurs le préjudice lié aux fraudes numériques à plusieurs centaines de millions de FCFA par an, avec une proportion croissante d'arnaques fondées sur l'ingénierie sociale plutôt que sur des failles purement techniques. Ces sources montrent un basculement net : là où la fraude bancaire classique et la fraude mobile money observée dans d'autres pays de la sous-région (Nigeria notamment) exploitent principalement des failles techniques telles que le SIM-swap, les schémas dominants au Togo — faux transfert, usurpation d'agent, fausse réidentification, plateformes frauduleuses d'investissement — reposent avant tout sur l'ingénierie sociale et l'exploitation de la confiance immédiate accordée aux transactions mobiles.

L'évolution de la fraude financière reflète ainsi le déplacement progressif des attaques depuis des manipulations physiques et documentaires vers des fraudes numériques plus rapides, plus distribuées et davantage fondées sur l'exploitation du comportement humain. Dans ce contexte, le mobile money constitue un terrain particulièrement sensible en Afrique de l'Ouest, et le cas togolais illustre avec une netteté particulière ce déplacement du risque technique vers le risque comportemental.

### I.2.2. Évolution des approches de détection

#### I.2.2.1. Règles métier et systèmes experts

Historiquement, la détection de fraude s'est d'abord appuyée sur des systèmes experts fondés sur des règles métier codifiées manuellement par des analystes — par exemple, bloquer toute transaction dépassant un seuil donné ou survenant à une heure inhabituelle. Bolton & Hand (2002) situent l'apparition de ces systèmes dès les débuts de l'informatisation bancaire, comme une réponse pragmatique et immédiatement opérationnelle à un problème jusque-là traité manuellement. Aujourd'hui encore, de nombreuses banques continuent d'exploiter ces systèmes en production, souvent en complément de solutions plus récentes.

Ces systèmes offrent l'avantage d'une interprétabilité totale — chaque décision peut être directement justifiée par la règle qui l'a déclenchée — et d'une mise en œuvre rapide, ne nécessitant ni données d'entraînement ni infrastructure de calcul complexe. Mais Dal Pozzolo et al. (2014) soulignent leur limite structurelle majeure : ces systèmes ne peuvent détecter que les schémas explicitement anticipés par leurs concepteurs, ce qui les rend structurellement vulnérables face à l'émergence de nouveaux modes opératoires. Bhattacharyya et al. (2011) confirment ce constat en montrant que les méthodes fondées sur des règles fixes, bien que peu coûteuses, deviennent rapidement obsolètes face à des fraudeurs qui adaptent leurs comportements pour se maintenir sous les seuils de détection connus — un phénomène d'évitement actif qui n'a pas d'équivalent dans les schémas de fraude purement opportunistes.

#### I.2.2.2. Statistiques et modèles classiques

Une deuxième génération d'approches a introduit des méthodes statistiques plus sophistiquées — régression logistique, analyse discriminante, scoring probabiliste — permettant de dépasser la rigidité des règles fixes en pondérant statistiquement plusieurs facteurs de risque simultanément, plutôt que d'appliquer des seuils binaires isolés. Dal Pozzolo et al. (2015) illustrent l'apport de cette génération à travers la problématique de la calibration probabiliste sur données déséquilibrées, montrant que les scores de risque produits par ces modèles doivent être interprétés avec prudence lorsque la classe frauduleuse est rare, sous peine de produire des estimations de probabilité systématiquement biaisées.

Cette période a également vu émerger des approches de transition vers l'ensemble learning : Carmona et al. (2019) montrent, dans le contexte de la prédiction de défaillance bancaire, la pertinence croissante des méthodes de boosting par rapport aux modèles de régression classiques, tandis que Chergui et al. (2022) confirment ce constat pour la détection de fraude financière dans les systèmes de transactions interbancaires. Ces modèles statistiques classiques restent cependant limités dans leur capacité à capturer des interactions non linéaires complexes entre variables — une limite que les approches de Machine Learning ont progressivement permis de dépasser.

#### I.2.2.3. Machine Learning et Deep Learning

À partir des années 2010, l'essor du Machine Learning a marqué un changement d'échelle dans la détection de fraude, en permettant l'apprentissage automatique de régularités complexes directement à partir des données transactionnelles, sans nécessiter de règles codifiées manuellement. Les fondements algorithmiques mobilisés dans la présente étude s'inscrivent directement dans cette génération : Liu et al. (2008, 2012) introduisent l'Isolation Forest comme réponse spécifique au besoin de détection d'anomalies sans données labellisées ; Breiman (2001) pose les bases du Random Forest et de l'ensemble learning par agrégation d'arbres indépendants ; Chen & Guestrin (2016) formalisent XGBoost et le principe du gradient boosting séquentiel, devenu depuis le standard industriel pour les données tabulaires.

Plus récemment encore, le champ s'est étendu au deep learning, avec des architectures capables de traiter la dimension séquentielle des transactions plutôt que de les considérer isolément. Hochreiter & Schmidhuber (1997) introduisent le réseau de neurones récurrent LSTM, dont Jurgovsky et al. (2018) démontrent la pertinence spécifique pour la détection de fraude par carte bancaire en modélisant explicitement les séquences de transactions d'un même client. Cette extension séquentielle constitue une perspective de prolongement pour la présente étude, mais n'a pas été implémentée dans le cadre de ce mémoire pour des raisons de ressources de calcul.

#### I.2.2.4. Approches hybrides et explicables

La dernière évolution du domaine, dans laquelle s'inscrit directement la présente étude, consiste à combiner plusieurs paradigmes algorithmiques au sein d'approches comparatives — confrontant par exemple un filtre non supervisé rapide à un classifieur supervisé fin — tout en intégrant systématiquement un module d'explicabilité (XAI). Cette évolution répond à un constat largement partagé dans la littérature et confirmé par les rapports des autorités de supervision financière (ACPR, Banque de France, BCEAO) : la performance prédictive brute d'un modèle ne suffit plus, à elle seule, à garantir son déploiement opérationnel dans un secteur aussi réglementé que la banque. Les solutions industrielles de lutte contre la fraude convergent aujourd'hui vers des architectures combinant modèles de Machine Learning performants, filtres d'anomalies, et modules d'explicabilité (SHAP, tableaux de bord XAI), condition nécessaire à leur adoption dans des environnements bancaires fortement réglementés.

Lundberg & Lee (2017) posent les fondements théoriques de cette génération avec SHAP, méthode d'explicabilité fondée sur les valeurs de Shapley qui permet d'attribuer à chaque variable une contribution quantifiable à la décision du modèle, tandis que Lundberg et al. (2020) en proposent une implémentation optimisée pour les modèles arborescents (TreeExplainer), rendant son usage praticable à l'échelle d'un système de production. Arrieta et al. (2020) élargissent ce cadre en proposant une taxonomie complète du champ de l'explicabilité, distinguant les méthodes intrinsèques des méthodes post-hoc et situant SHAP parmi les approches les plus robustes théoriquement.

Les travaux les plus récents illustrent la maturation opérationnelle de cette convergence entre performance et explicabilité. Le système FraudGuess (Qian et al., 2025) combine détection de nouveaux types de fraude par micro-clustering et tableau de bord explicatif interactif, démontrant que l'explicabilité ne sert pas seulement la conformité réglementaire mais contribue activement à la découverte de nouveaux schémas frauduleux. Le framework SAGE (Chen et al., 2026) pousse cette logique plus loin encore, en proposant une architecture multi-agents pilotée par des grands modèles de langage avec un accent explicite sur l'interprétabilité des décisions individuelles. Cette double exigence, opérationnelle et réglementaire, structure désormais la conception des systèmes de détection de fraude de nouvelle génération — et constitue le choix architectural central retenu pour le système FRAUDX proposé au Chapitre III de ce mémoire.

## I.3. Études antérieures et lacunes

### I.3.1. Travaux sur la fraude bancaire en Afrique et dans le monde

La littérature internationale documente de longue date l'application du Machine Learning à la détection de fraude bancaire, notamment sur des données de cartes bancaires occidentales (Bhattacharyya et al., 2011 ; Dal Pozzolo et al., 2014, 2015). Ces travaux ont établi les fondements méthodologiques largement repris dans la présente étude : le recours à des métriques adaptées au déséquilibre des classes (F1-Score, AUC-PR), l'usage de techniques de rééquilibrage comme SMOTE, et la comparaison systématique d'algorithmes d'ensemble learning.

Plus récemment, cette littérature a commencé à se déplacer vers des contextes africains, principalement portée par l'essor du mobile money. Ce mouvement, encore émergent et de portée inégale, reste cependant nettement plus restreint, en volume comme en maturité méthodologique, que le corpus centré sur la fraude par carte bancaire en contexte occidental.

### I.3.2. Travaux sur la fraude mobile money en Afrique de l'Ouest

Plusieurs sources, de nature et de rigueur méthodologique variables, permettent de documenter la fraude bancaire et mobile money dans différents pays d'Afrique, comme le synthétise le tableau suivant.

**Tableau 1.2 (bis) — Synthèse comparative des études antérieures en Afrique de l'Ouest**

| Pays | Auteurs | Secteur | Méthode IA | Constat principal |
|------|---------|---------|------------|-------------------|
| Côte d'Ivoire | Kouamé (2021) | Banque mobile | Random Forest | F1=0,82 sur données bancaires ivoiriennes |
| Sénégal | Diop & Ndiaye (2022) | Banque | XGBoost | Amélioration de 23 % vs règles statiques |
| Bénin | Adjovi (2023) | Mobile money | Logistic Regression | Limites sur données fortement déséquilibrées |
| Nigeria | Okonkwo et al. (2020) | Banque | Ensemble Learning | F1=0,87, prédominance fraude SIM swap |
| Ghana | Mensah (2022) | Mobile money | XGBoost + SMOTE | Recall=0,91 après SMOTE |
| **Togo** | — (présente étude) | Banque + Mobile money | IF + RF + XGB + SHAP | **Première étude documentée (2025)** |

Ce tableau met en évidence une hétérogénéité méthodologique et une divergence de typologies dominantes selon les pays. Au Nigeria, la fraude SIM-swap — obtention frauduleuse d'une carte SIM de remplacement permettant d'intercepter les codes OTP — constitue le schéma prédominant (Adekunle et al., 2025), un constat corroboré à l'échelle régionale par des cas documentés en Afrique du Sud et au Cameroun (Nkolwoudou Afane, 2025). Cette prédominance technique contraste avec le profil togolais établi, où les alertes ANCY et CERT-TG (2025) font au contraire ressortir une prédominance de schémas d'ingénierie sociale pure, sans détournement technique de la carte SIM. Cette divergence suggère que la typologie de fraude mobile money n'est pas uniforme à l'échelle de la sous-région, mais dépend de facteurs locaux — pratiques des opérateurs, niveau de sensibilisation des usagers, dispositifs de sécurité des télécoms — qu'une étude centrée sur un pays donné, comme la présente recherche, permet de mieux documenter qu'une généralisation régionale.

### I.3.3. Travaux sur l'explicabilité des modèles de détection

Si l'intérêt de l'explicabilité pour les systèmes d'IA est largement reconnu dans la littérature (Lundberg & Lee, 2017 ; Arrieta et al., 2020), les travaux empiriques évaluant son impact sur l'adoption effective des systèmes de détection de fraude par des professionnels bancaires restent peu nombreux. Les travaux les plus récents, tels que FraudGuess (Cordeiro et al., 2025) et le framework SAGE (Chen et al., 2026), présentés plus haut, montrent un intérêt croissant pour l'articulation entre explicabilité et performance opérationnelle, mais restent centrés sur des contextes occidentaux ou asiatiques. Aucune étude, à notre connaissance, n'a évalué empiriquement l'impact de l'explicabilité sur l'adoption de systèmes de détection de fraude par des professionnels bancaires africains — une lacune que la présente étude vise à combler, un volet qualitatif étant proposé en perspective.

### I.3.4. Limites de la littérature existante

L'analyse de la littérature existante permet de dégager quatre lacunes principales :

1. **Absence d'étude sur le Togo** : si des travaux appliquant le Machine Learning à la fraude mobile money ont récemment émergé au Nigeria (Adekunle et al., 2025) et, dans une moindre mesure, au Ghana (Lokanan, 2023), aucune étude scientifique publiée ne porte, à notre connaissance, sur le Togo, laissant ce pays hors du périmètre des analyses malgré son taux d'adoption du mobile money parmi les plus élevés de la région.

2. **Modèles conçus pour les transactions par carte occidentales** : les modèles de détection de fraude les plus matures méthodologiquement demeurent majoritairement conçus pour les transactions par carte bancaire en contextes européens ou nord-américains, sans intégrer les dimensions propres au mobile money ouest-africain.

3. **Manque de validation empirique de l'explicabilité en contexte africain** : très peu d'études empiriques ont évalué l'impact de l'explicabilité sur l'adoption effective des systèmes de détection par des professionnels bancaires africains.

4. **Rareté des architectures logicielles complètes** : la littérature technique abonde en modèles performants, mais rares sont les travaux proposant une architecture logicielle complète et sécurisée intégrant à la fois contrôle d'accès, explicabilité et contraintes réglementaires régionales dans un cadre applicable à une banque ouest-africaine.

### I.3.5. Positionnement de la présente étude

La présente recherche se positionne à l'intersection de ces quatre lacunes. Elle propose une approche comparative de trois algorithmes d'ensemble learning — Isolation Forest, Random Forest et XGBoost — associée à une explicabilité par SHAP, conçue pour tenir compte des spécificités opérationnelles et réglementaires d'une banque du Groupe Sunu au Togo. Elle documente pour la première fois, à notre connaissance, la typologie spécifique de la fraude mobile money togolaise à partir de sources officielles nationales (ANCY, CERT-TG), en la distinguant explicitement des typologies dominantes observées ailleurs dans la sous-région — notamment de la prédominance du SIM-swap identifiée au Nigeria. Enfin, la perspective d'un volet qualitatif d'évaluation de l'utilité perçue de SHAP auprès de responsables bancaires togolais est proposée, contribuant ainsi à ouvrir une piste pour combler le déficit de validation empirique de l'explicabilité en contexte africain.

## Conclusion du chapitre

Ce premier chapitre a établi les fondements théoriques, historiques et bibliographiques de la présente étude, en trois temps complémentaires.

Le cadre théorique a précisé les notions mobilisées — détection d'anomalies, apprentissage supervisé, explicabilité — et montré que la fraude mobile money au Togo présente des caractéristiques spécifiques, marquées par la prédominance de l'ingénierie sociale, dans un cadre légal structuré par la BCEAO, l'UEMOA et le GIABA. Le Machine Learning, et particulièrement l'approche comparative combinant Isolation Forest, Random Forest et XGBoost, enrichie par SMOTE pour le rééquilibrage des classes déséquilibrées et par SHAP pour l'explicabilité, offre des solutions performantes et transparentes pour y répondre.

La revue des études a permis de positionner la présente recherche par rapport aux travaux existants — notamment ceux récemment publiés sur le Nigeria (Adekunle et al., 2025) et le Ghana (Lokanan, 2023) — et d'identifier les lacunes qu'elle entend combler, au premier rang desquelles l'absence d'étude spécifique au contexte togolais combinant modélisation prédictive explicable et ancrage institutionnel documenté.

C'est cette lacune que la présente étude ambitionne de combler, en ancrant l'architecture FRAUDX — combinant Isolation Forest, Random Forest, XGBoost et un module d'explicabilité SHAP — dans le contexte opérationnel d'une banque du Groupe Sunu au Togo. Le chapitre suivant détaille la méthodologie employée pour vérifier les hypothèses formulées dans l'introduction, en précisant les variables, les indicateurs, les outils et la stratégie de vérification.
