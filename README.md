# ⚽ Comparateur de profils de joueurs (Football)

Ce projet est un outil interactif développé en **Python** avec **Streamlit** permettant de comparer les profils de joueurs de football professionnels, à partir de leurs statistiques de la saison **2022-2023**.

Il repose sur une **analyse en composantes principales (PCA)** pour projeter les joueurs dans un espace à deux dimensions et calculer leur similarité statistique.

---

## 🚀 Fonctionnalités

- Visualisation de la **variance expliquée** par les composantes principales
- Affichage des **loadings** des variables sur PC1 et PC2
- Sélection d’un joueur et affichage des **5 plus proches voisins** (tous postes / même poste)
- Nuage de points interactif (PC1 vs PC2) avec annotations pour interprétation

---

## 📊 Données

Les statistiques proviennent de ce dataset public sur Kaggle :  
📘 **"2022/2023 Football Player Stats"**  
🔗 [Accéder au dataset sur Kaggle](https://www.kaggle.com/datasets/vivovinco/20222023-football-player-stats)  
📄 Licence : [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)

Des modifications ont été apportées :
- Nettoyage et standardisation
- Regroupement de certains postes (par exemple : MF/FW → MF)
- Sélection de 6 variables clés : 
  - **Shots** (tirs hors penaltys)
  - **PasTotPrgDist** (distance des passes progressives)
  - **Assists** (passes décisives)
  - **SCA** (actions menant à un tir)
  - **Tkl+Int** (tacles + interceptions)
  - **ToAtt** (dribbles tentés)

---

## 🧪 Technologies utilisées

- Python
- pandas
- NumPy
- Streamlit
- Plotly

---

## 🖥️ Lancer le projet en local

Assurez-vous d'avoir Python installé, puis :

```bash
pip install -r requirements.txt
streamlit run ComparateurProfil.py
