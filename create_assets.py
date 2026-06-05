import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# Load your data
tracks = pd.read_csv('Data/music_tracks.csv')

# Create energy_level column
tracks['energy_level'] = pd.cut(tracks['energy'], bins=[-0.001, 0.33, 0.66, 1], labels=['low', 'medium', 'high'])
tracks['tempo_missing'] = tracks['tempo'].isna()

assets_folder = Path("assets")
assets_folder.mkdir(parents=True, exist_ok=True)

fig = px.histogram(
    tracks,
    x="energy",
    nbins=40,
    title="Distribution of Song Energy",
    labels={"energy": "Energy"}
)
fig.write_html(assets_folder / "energy-distribution.html", include_plotlyjs="cdn")

fig = px.histogram(
    tracks,
    x="popularity",
    nbins=40,
    title="Distribution of Song Popularity",
    labels={"popularity": "Popularity"}
)
fig.write_html(assets_folder / "popularity-distribution.html", include_plotlyjs="cdn")

fig = px.scatter(
    tracks.sample(5000, random_state=1),
    x="energy",
    y="popularity",
    opacity=0.4,
    title="Energy vs. Popularity",
    labels={
        "energy": "Energy",
        "popularity": "Popularity"
    }
)
fig.write_html(assets_folder / "energy-vs-popularity.html", include_plotlyjs="cdn")

fig = px.box(
    tracks,
    x="energy_level",
    y="popularity",
    title="Popularity Distribution by Energy Level",
    labels={
        "energy_level": "Energy Level",
        "popularity": "Popularity"
    }
)
fig.write_html(assets_folder / "popularity-by-energy-level.html", include_plotlyjs="cdn")

fig = px.box(
    tracks,
    x="tempo_missing",
    y="energy",
    title="Energy Distribution by Tempo Missingness",
    labels={
        "tempo_missing": "Tempo Missing?",
        "energy": "Energy"
    }
)
fig.write_html(assets_folder / "tempo-missingness-energy.html", include_plotlyjs="cdn")

rng = np.random.default_rng(42)
hypothesis_data = tracks[tracks["energy_level"].isin(["low", "high"])].copy()
hypothesis_popularity = hypothesis_data["popularity"].to_numpy()
hypothesis_labels = (hypothesis_data["energy_level"] == "high").to_numpy()
observed_difference = (
    hypothesis_data.loc[hypothesis_data["energy_level"] == "high", "popularity"].mean()
    - hypothesis_data.loc[hypothesis_data["energy_level"] == "low", "popularity"].mean()
)
permuted_differences = []
for _ in range(1000):
    shuffled_labels = rng.permutation(hypothesis_labels)
    permuted_differences.append(
        hypothesis_popularity[shuffled_labels].mean()
        - hypothesis_popularity[~shuffled_labels].mean()
    )

fig = px.histogram(
    x=permuted_differences,
    nbins=40,
    title="Permutation Distribution for Energy-Level Hypothesis Test",
    labels={"x": "Mean popularity difference under the null"}
)
fig.add_vline(
    x=observed_difference,
    line_color="red",
    line_dash="dash",
    annotation_text="Observed difference",
    annotation_position="top right"
)
fig.write_html(assets_folder / "energy-hypothesis-permutation.html", include_plotlyjs="cdn")

fig = go.Figure(
    data=[
        go.Bar(name="Baseline", x=["Accuracy", "Balanced Accuracy"], y=[0.0416, 0.0416]),
        go.Bar(name="Final Model", x=["Accuracy", "Balanced Accuracy"], y=[0.2057, 0.2057]),
    ]
)
fig.update_layout(
    title="Baseline vs. Final Model Performance",
    yaxis_title="Score",
    barmode="group"
)
fig.write_html(assets_folder / "model-performance.html", include_plotlyjs="cdn")

print("Interactive plots saved to:", assets_folder)
