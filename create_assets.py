import pandas as pd
import plotly.express as px
from pathlib import Path

# Load your data
tracks = pd.read_csv('Data/music_tracks.csv')

# Create energy_level column
tracks['energy_level'] = pd.cut(tracks['energy'], bins=[0, 0.33, 0.66, 1], labels=['low', 'medium', 'high'])

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

print("Interactive plots saved to:", assets_folder)
