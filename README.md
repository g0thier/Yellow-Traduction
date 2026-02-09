# Yellow Traduction

## Description

Yellow Traduction est une application web permettant de traduire grâce au deep learning des documents PDF volumineux. Il est conçu pour les fichiers trop lourds ou trop longs pour être traduits par les solutions en ligne classique.

## 🎯 Objectif du projet

L'objectif est de rendre la traduction de documents aussi simple et rapide que possible, tout en maintenant une haute qualité de traduction.

## 🚀 Cas d’usage

- Conversion rapide de documentation technique pour des projets internationaux

## 👥 Public cible

- **Professionnels et entreprises** ayant besoin de traduire rapidement des documents
- **Étudiants** ayant besoin de traduire rapidement des documents
- **Développeurs** intéressés par des solutions d'automatisation de traduction

## ⚙️ Fonctionnalités actuelles

- Interface Streamlit intuitive
  - Upload de documents PDF
  - Sélection de la langue de destination
- Traduction automatique de documents
  - Préservation du formatage
  - [ToDo]() : ~~Support de multiples langues~~
- Scripts de traitement par lot
  - Traduction multithread pour optimiser les performances
  - [ToDo]() : ~~Support des gros volumes de documents~~

## 🖥️ Interface graphique

Le fichier `streamlit_app.py` implémente l’interface Streamlit décrite ci-dessus.

![image](docs/images/Capture.png)

## 🧠 Fonctionnement général

1. L'utilisateur charge un document PDF par l'interface Streamlit ou via script
2. Le document est analysé et préparé pour la traduction
3. Le moteur de traduction traite le contenu
   - Extraction du texte du PDF
   - Traduction des éléments textuels
   - Reconstruction du document avec les éléments traduits
4. Le document traduit est retourné à l'utilisateur

## 🗂️ Structure du repository

```text
Yellow Traduction/
├── .github/
├── dashboard/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── streamlit_app.py
├── docs/
│   └── images/Capture.png
├── scripts/
│   ├── Traduction_PDF_multicore.ipynb
│   └── Traduction_PDF.ipynb
├── CHANGELOG.md
├── LICENSE.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── SECURITY.md
└── ACKNOWLEDGEMENTS.md
```

## 🐳 Installation & déploiement

Le projet est prévu pour être déployé :

- Via Docker pour une containerisation simple et reproductible
- Directement sur serveur en exécutant l'application Streamlit

### Environnement

- **Python ≥ 3.13.5**
- Dépendances listées dans `requirements.txt`

## 🧪 État du projet

- 🔬 **Statut** : expérimental
- 🧭 **Roadmap** : à définir

## 🔒 Licence

- Voir [LICENSE.md](/LICENSE.md)

## 🤝 Contributions

- Voir [CONTRIBUTING.md](/CONTRIBUTING.md)
- Code de conduite disponible dans [CODE_OF_CONDUCT.md](/CODE_OF_CONDUCT.md)

## 👤 Auteur

**Gauthier RAMMAULT**