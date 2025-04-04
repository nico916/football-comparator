import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

@st.cache_data
def load_and_prepare_data(csv_path='player_stats_processed.csv'):
    df = pd.read_csv(csv_path, sep=';', encoding='utf-8')
    pos_map = {
        "MFFW": "MF",
        "FWMF": "FW",
        "DFMF": "DF",
        "MFDF": "MF",
        "FWDF": "FW",
        "DFFW": "DF"
    }
    df['Pos'] = df['Pos'].replace(pos_map)
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    data_numeric = df[numeric_cols].values
    data_mean = np.mean(data_numeric, axis=0)
    data_std = np.std(data_numeric, axis=0, ddof=1)
    data_standardized = (data_numeric - data_mean) / data_std
    cov_matrix = np.cov(data_standardized, rowvar=False)
    eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)
    sorted_idx = np.argsort(eigenvalues)[::-1]
    eigenvalues_sorted = eigenvalues[sorted_idx]
    eigenvectors_sorted = eigenvectors[:, sorted_idx]
    pca_scores = data_standardized @ eigenvectors_sorted
    pca_scores[:, 0] = -pca_scores[:, 0]
    pca_scores[:, 1] = -pca_scores[:, 1]
    df['PC1'] = pca_scores[:, 0]
    df['PC2'] = pca_scores[:, 1]
    return df, eigenvalues_sorted, eigenvectors_sorted, numeric_cols

df, eigenvalues_sorted, eigenvectors_sorted, numeric_cols = load_and_prepare_data()

sum_eig = np.sum(eigenvalues_sorted)
variance_explained = [(val / sum_eig)*100 for val in eigenvalues_sorted]
df_variance = pd.DataFrame({
    'Composante': [f"PC{i+1}" for i in range(len(variance_explained))],
    'Variance (%)': variance_explained
})

st.title("Dashboard PCA Joueurs de Football")
st.subheader("Variance expliquée par chaque composante PCA")

fig_var = px.bar(
    df_variance,
    x='Composante',
    y='Variance (%)',
    title="Pourcentage de variance expliquée par chaque PC",
    text='Variance (%)',
    width=700,
    height=400
)
fig_var.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
fig_var.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
st.plotly_chart(fig_var, use_container_width=True)

st.subheader("Contributions des variables à PC1 et PC2 (Loadings)")

loadings_pc1_pc2 = eigenvectors_sorted[:, :2]
df_loadings = pd.DataFrame(
    loadings_pc1_pc2,
    columns=["PC1", "PC2"],
    index=numeric_cols
)
st.dataframe(df_loadings.style.background_gradient(cmap='RdBu', axis=0))

st.markdown("""
<small>**Interprétation :**  
- Une valeur **positive** élevée (rouge) signifie que la variable contribue fortement et positivement à la composante.  
- Une valeur **négative** (bleu) signifie qu’elle contribue dans l’autre sens.  
- Par exemple, si “Shots” est fort en PC1 (valeur +0.8), les joueurs qui tirent beaucoup seront plutôt côté PC1 positif.</small>
""", unsafe_allow_html=True)

st.subheader("Recherche de joueurs similaires")

all_players = df['Player'].unique()
all_players_sorted = sorted(all_players)

selected_player = st.selectbox(
    "Choisissez un joueur",
    options=all_players_sorted
)

def get_nearest_neighbors(df, player_name, n=5):
    row_player = df[df['Player'] == player_name]
    if row_player.empty:
        return pd.DataFrame()
    pc1_player = row_player['PC1'].values[0]
    pc2_player = row_player['PC2'].values[0]
    distances = np.sqrt(
        (df['PC1'] - pc1_player)**2 +
        (df['PC2'] - pc2_player)**2
    )
    df_dist = pd.DataFrame({
        'Player': df['Player'],
        'Pos': df['Pos'],
        'Distance': distances
    })
    df_dist = df_dist[df_dist['Player'] != player_name]
    df_dist_sorted = df_dist.sort_values(by='Distance', ascending=True)
    return df_dist_sorted.head(n)

if selected_player:
    st.write(f"**Joueur sélectionné** : {selected_player}")
    neighbors_global = get_nearest_neighbors(df, selected_player, n=5)
    st.write("**5 plus proches voisins (tous postes)**")
    st.dataframe(neighbors_global.reset_index(drop=True))
    player_pos = df.loc[df['Player'] == selected_player, 'Pos'].values[0]
    df_same_pos = df[df['Pos'] == player_pos]
    neighbors_same_pos = get_nearest_neighbors(df_same_pos, selected_player, n=5)
    st.write(f"**5 plus proches voisins (même poste = {player_pos})**")
    st.dataframe(neighbors_same_pos.reset_index(drop=True))

st.subheader("Projection PCA (PC1 vs PC2)")

color_map = {'FW': 'red', 'MF': 'blue', 'DF': 'green'}

fig = px.scatter(
    df,
    x="PC1", y="PC2",
    color='Pos',
    color_discrete_map=color_map,
    hover_data=['Player', 'Pos'],
    title="Projection PCA (PC1 vs PC2)",
    width=800, height=600
)

xmin, xmax = df['PC1'].min(), df['PC1'].max()
ymin, ymax = df['PC2'].min(), df['PC2'].max()

fig.add_shape(type="line", x0=0, x1=0, y0=ymin, y1=ymax, line=dict(color="gray", width=1, dash="dash"))
fig.add_shape(type="line", x0=xmin, x1=xmax, y0=0, y1=0, line=dict(color="gray", width=1, dash="dash"))

fig.add_annotation(x=xmax*1.05, y=0, text="Offensif", showarrow=False, font=dict(color="red", size=12))
fig.add_annotation(x=xmin*1.05, y=0, text="Défensif", showarrow=False, font=dict(color="blue", size=12))
fig.add_annotation(x=0, y=ymax*1.05, text="Créatif", showarrow=False, font=dict(color="black", size=12))
fig.add_annotation(x=0, y=ymin*1.05, text="Stéréotypé", showarrow=False, font=dict(color="black", size=12))
fig.add_annotation(x=xmax*0.75, y=ymax*0.75, text="Créateurs offensifs", showarrow=False, font=dict(color="red", size=10))
fig.add_annotation(x=xmin*0.75, y=ymax*0.75, text="Créateurs Défensifs", showarrow=False, font=dict(color="blue", size=10))
fig.add_annotation(x=xmin*0.75, y=ymin*0.75, text="Rugueux défensifs", showarrow=False, font=dict(color="green", size=10))
fig.add_annotation(x=xmax*0.75, y=ymin*0.75, text="Finisseurs", showarrow=False, font=dict(color="purple", size=10))

st.plotly_chart(fig, use_container_width=True)
