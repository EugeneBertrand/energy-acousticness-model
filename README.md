---
layout: default
title: The Energy-Popularity Connection in Spotify Music
---

# The Energy-Popularity Connection in Spotify Music

**Name:** Eugene Bertrand

## Introduction

Music listeners often describe songs as calm, intense, danceable, emotional, or energetic. I wanted to see whether one of those qualities, **energy**, is connected to how popular a song is on Spotify. This matters because popularity is often treated like a measure of listener preference, but it may also reflect measurable audio features, genre conventions, and platform behavior.

This project uses a Spotify tracks dataset with **114,000 rows**, where each row represents one song. The central question is:

**Do songs with higher energy levels tend to be more popular on Spotify?**

The most relevant columns are:

| Column | Description |
| --- | --- |
| `popularity` | A Spotify popularity score from 0 to 100. This is the main outcome for the EDA and hypothesis test. |
| `energy` | A numerical audio feature from 0 to 1 describing how intense and active a track sounds. |
| `acousticness` | A numerical audio feature from 0 to 1 describing whether a track sounds acoustic. |
| `danceability` | A numerical audio feature from 0 to 1 describing how suitable a track is for dancing. |
| `tempo` | The estimated speed of the song in beats per minute. This column has non-trivial missingness. |
| `track_genre` | The genre label for each track. I use this as the response variable in the prediction task. |
| `duration_ms` and `release_date` | Track metadata used to create `duration_min` and `release_year`. |

## Data Cleaning and Exploratory Data Analysis

I cleaned the data by removing the unnecessary `Unnamed: 0` index column, converting `duration_ms` into `duration_min`, extracting the first four digits of `release_date` into `release_year`, and creating an `energy_level` column that groups tracks into low, medium, and high energy. Since the dataset appears to be generated from Spotify track metadata and audio analysis outputs, these cleaning steps keep the original track-level unit of observation while making the variables easier to interpret. I also removed the one row that was missing identifying track information, leaving **113,999 cleaned rows**.

Here is the head of the cleaned DataFrame:

| track_name | artists | track_genre | popularity | energy | acousticness | duration_min | release_year | energy_level |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Comedy | Gen Hoshino | acoustic | 73 | 0.461 | 0.032 | 3.84 | 1974 | medium |
| Ghost - Acoustic | Ben Woodward | acoustic | 55 | 0.166 | 0.924 | 2.49 | 1995 | low |
| To Begin Again | Ingrid Michaelson;ZAYN | acoustic | 57 | 0.359 | 0.210 | 3.51 | 1973 | medium |
| Can't Help Falling In Love | Kina Grannis | acoustic | 71 | 0.060 | 0.905 | 3.37 | 2018 | low |
| Hold On | Chord Overstreet | acoustic | 82 | 0.443 | 0.469 | 3.31 | 2017 | medium |

### Univariate Analysis

<iframe
  src="assets/energy-distribution.html"
  width="800"
  height="600"
  frameborder="0"
></iframe>

The energy distribution is concentrated more heavily in the medium-to-high range than the very low range. This suggests that many songs in the dataset are fairly active or intense, which makes energy a useful feature to compare against popularity.

<iframe
  src="assets/popularity-distribution.html"
  width="800"
  height="600"
  frameborder="0"
></iframe>

Popularity is spread across the 0 to 100 scale, but many songs have low or moderate popularity rather than extremely high popularity. This makes sense for a large catalog-style dataset, since only a small share of songs become very popular.

### Bivariate Analysis

<iframe
  src="assets/energy-vs-popularity.html"
  width="800"
  height="600"
  frameborder="0"
></iframe>

The scatter plot does not show a strong linear relationship between energy and popularity, but it does show that popular songs can appear across a wide range of energy values. This suggests that energy alone cannot explain popularity, even if there may be some group-level differences.

<iframe
  src="assets/popularity-by-energy-level.html"
  width="800"
  height="600"
  frameborder="0"
></iframe>

The box plot compares popularity across low, medium, and high energy songs. Medium-energy songs have the highest mean popularity in the cleaned data, while high-energy songs are more popular on average than low-energy songs.

### Interesting Aggregates

| energy_level | song_count | mean_popularity | median_popularity | mean_energy |
| --- | --- | --- | --- | --- |
| low | 15,836 | 30.07 | 28.00 | 0.19 |
| medium | 37,278 | 35.29 | 38.00 | 0.51 |
| high | 60,885 | 32.80 | 33.00 | 0.84 |

This grouped table shows that popularity is not simply increasing with energy. Medium-energy songs have the highest mean and median popularity, while high-energy songs still have a higher mean popularity than low-energy songs.

| track_genre | low | medium | high |
| --- | --- | --- | --- |
| anime | 49.59 | 46.69 | 49.26 |
| chill | 54.03 | 54.09 | 50.47 |
| emo | 58.94 | 50.65 | 44.84 |
| grunge | 57.60 | 49.66 | 49.48 |
| indian | 48.34 | 50.10 | 49.33 |
| k-pop | 52.91 | 51.21 | 61.10 |
| pop-film | 53.96 | 60.82 | 58.26 |
| sad | 52.74 | 52.21 | 52.45 |

This pivot table shows that the energy-popularity relationship differs by genre. For example, high-energy K-pop songs are much more popular on average than low-energy K-pop songs, while the opposite pattern appears for emo.

## Assessment of Missingness

The `tempo` column has non-trivial missingness: **19.4%** of its values are missing. I believe `tempo` could be **NMAR** if the missingness happens because Spotify's audio-analysis system has difficulty estimating tempo for songs with unclear beats, unusual rhythms, or noisy recordings. In that case, the missingness would depend on an unobserved property of the tempo value or rhythm itself. Additional data about beat-confidence scores, audio-analysis failures, or whether a song has a steady beat would help explain the missingness and could make it MAR.

To test missingness dependency, I created a boolean column indicating whether `tempo` is missing and ran permutation tests comparing the difference in means between songs with missing and non-missing tempo.

<iframe
  src="assets/tempo-missingness-energy.html"
  width="800"
  height="600"
  frameborder="0"
></iframe>

For `energy`, songs with missing tempo had mean energy **0.513**, while songs with non-missing tempo had mean energy **0.672**. The observed absolute difference was **0.159**, and the permutation test produced **p = 0.001**, so tempo missingness appears to depend on energy.

For `popularity`, songs with missing tempo had mean popularity **33.29**, while songs with non-missing tempo had mean popularity **33.23**. The observed absolute difference was only **0.059**, and the permutation test produced **p = 0.731**, so I do not have evidence that tempo missingness depends on popularity.

## Hypothesis Testing

I tested whether high-energy songs tend to be more popular than low-energy songs.

**Null Hypothesis:** High-energy songs and low-energy songs have the same mean popularity, and any observed difference is due to random chance.

**Alternative Hypothesis:** High-energy songs have higher mean popularity than low-energy songs.

**Test Statistic:** Mean popularity of high-energy songs minus mean popularity of low-energy songs.

I used a significance level of **0.05**. This test statistic is appropriate because my question compares average popularity between two energy-based groups, and a permutation test is appropriate because it simulates the null hypothesis by shuffling energy-group labels.

<iframe
  src="assets/energy-hypothesis-permutation.html"
  width="800"
  height="600"
  frameborder="0"
></iframe>

The observed mean popularity for high-energy songs was **32.80**, while the observed mean popularity for low-energy songs was **30.07**. The observed difference was **2.73 popularity points**, and the permutation test gave **p = 0.001**. Since this p-value is below 0.05, I reject the null hypothesis. This provides evidence that high-energy songs are more popular on average than low-energy songs in this dataset, though this does not prove that energy causes popularity.

## Framing a Prediction Problem

For the prediction task, I predicted a song's `track_genre` using audio features and track metadata. This is a **multiclass classification** problem because `track_genre` has many possible genre labels.

The response variable is `track_genre`. I chose it because genre is closely connected to audio characteristics, so features like energy, acousticness, danceability, loudness, and duration should contain useful information about it. I used **accuracy** and **balanced accuracy** as evaluation metrics. Accuracy is easy to interpret as the proportion of correctly classified songs, while balanced accuracy is especially useful because the task has many genre classes and I want each genre to matter equally.

The time of prediction is after a track already exists in the Spotify-style catalog and its audio features and popularity score have been measured. At that point, the model can use audio-analysis features such as `energy`, `acousticness`, `danceability`, `valence`, and `loudness`, along with metadata such as `duration_min` and `popularity`.

For modeling, I used a stratified sample of up to 500 songs per genre, for **57,000 songs** total. This kept the 114-class task computationally manageable while making the genre classes more balanced for comparison.

## Baseline Model

My baseline model used two original quantitative features: `energy` and `acousticness`. It used **0 ordinal features** and **0 nominal features**, so no categorical encoding was needed. I built the model as a single sklearn `Pipeline` that imputes missing numerical values with the median, standardizes the two features, and fits a logistic regression classifier.

The baseline model was evaluated on an unseen test set using the same train-test split later used for the final model. It achieved:

| Model | Accuracy | Balanced Accuracy |
| --- | --- | --- |
| Baseline logistic regression | 0.0416 | 0.0416 |

I do not believe this baseline model is very strong. Since it predicts among **114 genres**, two numerical audio features are not enough to distinguish many genres that can share similar energy and acousticness levels.

## Final Model

My final model used a decision tree classifier. I added the original quantitative features `danceability`, `valence`, `loudness`, `duration_min`, and `popularity`, plus three engineered quantitative features:

- `energy_acousticness_interaction`, which captures songs that are both energetic and acoustic or non-acoustic.
- `energy_minus_acousticness`, which captures the contrast between intensity and acoustic sound.
- `energy_danceability_interaction`, which captures songs that are both energetic and danceable.

These features make sense for genre prediction because genres are often defined by combinations of sound qualities rather than by one audio feature alone. For example, energetic acoustic tracks and energetic electronic tracks can have similar energy values but very different genre labels.

I selected hyperparameters using `GridSearchCV` with 3-fold cross-validation on the training data. I tuned `max_depth` because deeper trees can learn more complex genre boundaries, and `min_samples_leaf` because larger leaf sizes reduce overfitting. The best hyperparameters were:

| Hyperparameter | Best Value |
| --- | --- |
| `max_depth` | 18 |
| `min_samples_leaf` | 30 |

<iframe
  src="assets/model-performance.html"
  width="800"
  height="600"
  frameborder="0"
></iframe>

| Model | Accuracy | Balanced Accuracy |
| --- | --- | --- |
| Baseline logistic regression | 0.0416 | 0.0416 |
| Final decision tree | 0.2057 | 0.2057 |

The final model improves substantially over the baseline model, increasing balanced accuracy from **0.0416** to **0.2057** on the unseen test set. The model is still far from perfect because genre prediction across 114 classes is difficult, but it performs much better than the two-feature baseline.

## Fairness Analysis

For the fairness analysis, I asked whether the final model performs worse for high-energy songs than for low-or-medium-energy songs.

**Group X:** High-energy songs, where `energy > 0.66`.

**Group Y:** Low-or-medium-energy songs, where `energy <= 0.66`.

**Evaluation Metric:** Accuracy.

**Null Hypothesis:** The model is fair. Its accuracy for high-energy songs and low-or-medium-energy songs is roughly the same, and any observed difference is due to random chance.

**Alternative Hypothesis:** The model is less accurate for high-energy songs than for low-or-medium-energy songs.

**Test Statistic:** Accuracy for low-or-medium-energy songs minus accuracy for high-energy songs.

On the test set, the final model had accuracy **0.1992** for high-energy songs and **0.2130** for low-or-medium-energy songs. The observed test statistic was **0.0138**, and the permutation test gave **p = 0.026**. At the 0.05 significance level, I reject the null hypothesis. This provides evidence that the model performs slightly worse for high-energy songs, although the size of the accuracy gap is fairly small.
