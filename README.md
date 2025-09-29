# Football Player Profile Comparator

![Language](https://img.shields.io/badge/language-Python-3776AB?style=flat-square)
![Framework](https://img.shields.io/badge/framework-Streamlit-FF4B4B?style=flat-square)
![Concept](https://img.shields.io/badge/concept-PCA%20%7C%20Data--Viz-blueviolet?style=flat-square)

An interactive web app built with Python & Streamlit to compare football player profiles based on a Principal Component Analysis (PCA) of their 2022-2023 season stats. Data sourced from Kaggle.

## Table of Contents

- [About The Project](#about-the-project)
- [Live Demo](#live-demo)
- [Key Features](#key-features)
- [Built With](#built-with)
- [Getting Started](#getting-started)
- [Technical Deep Dive](#technical-deep-dive)
- [Future Improvements](#future-improvements)
- [Data Source](#data-source)
- [License](#license)

## About The Project

This personal project is a direct continuation of a previous academic PCA study. The goal was to transform a static analysis into an interactive and usable tool with **Streamlit**. The application allows users to visually compare professional football players based on their statistics from the 2022-2023 season.

The core idea emerged from observing the player data projected onto a 2D plane: since each point represents a player's statistical profile, the Euclidean distance between points can be used as a measure of similarity.

## Live Demo

The application is deployed on Render and can be accessed directly.

**👉 [Open the Live Application](https://comparateur-de-profils.onrender.com)**

*Note: The app is hosted on a free service and may take a few seconds to wake up if it has been idle.*

## Key Features

-   **Explained Variance**: Visualizes the variance explained by each principal component.
-   **Feature Contributions**: Displays the loadings of the selected variables on PC1 and PC2.
-   **Nearest Neighbors**: Select a player to find and display the 5 most statistically similar players.
-   **Interactive Scatter Plot**: An interactive plot of PC1 vs. PC2 with conceptual zone annotations.

## Built With

-   **Python**
-   **Streamlit**
-   **Pandas**
-   **NumPy**
-   **Scikit-learn**
-   **Plotly**

## Getting Started

To get a local copy up and running, follow these steps.

1.  **Prerequisites**: Ensure you have Python installed.
2.  **Clone the repository:**
    ```sh
    git clone https://github.com/nico916/football-comparator.git
    ```
3.  **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```
4.  **Run the Streamlit app:**
    ```sh
    streamlit run ComparateurProfil.py
    ```

## Technical Deep Dive

The application relies on a pre-processed dataset where 6 key statistical variables were selected to define player profiles:
-   **Shots**: Total shots (excluding penalties)
-   **PasTotPrgDist**: Total progressive passing distance
-   **Assists**: Goal assists
-   **SCA**: Shot-Creating Actions
-   **Tkl+Int**: Tackles + Interceptions
-   **ToAtt**: Dribbles attempted

These multi-dimensional stats are then reduced to two principal components (PC1 and PC2) using PCA, which form the basis for the 2D visualization and similarity calculations.

## Future Improvements

-   Offer a comparison method that does not rely on PCA.
-   Add filters for age, league, etc.
-   Implement a comparison history feature.

## Data Source

The player statistics used in this analysis are from the **"2022/2023 Football Player Stats"** dataset on Kaggle, available under the [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) license. The data was cleaned, standardized, and transformed for this specific analysis.

## License

Distributed under the MIT License. See `LICENSE` file for more information.
