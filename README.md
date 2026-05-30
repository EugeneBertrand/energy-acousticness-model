---
layout: home
title: The Energy-Popularity Connection in Spotify Music
---

**Name:** Eugene Bertrand

## Introduction

I chose this dataset because music is something involved in my everyday life, and I was interested in seeing whether the qualities of songs I notice as a listener are connected to popularity. This project uses a Spotify music dataset containing **114,000 songs**, where each row represents one track.

The main question I explored is: **Do songs with higher energy levels tend to be more popular on Spotify?**

The most relevant columns are `popularity`, which measures how popular a song is on Spotify, and `energy`, which measures how intense and active a song feels. I also used columns such as `track_genre`, `track_name`, `artists`, `duration_ms`, `release_date`, and `explicit` to clean and explore the dataset.

## Data Cleaning and Exploratory Data Analysis

To clean the data, I removed the unnecessary index column, kept the columns relevant to my question, replaced missing values consistently, removed rows missing important values, converted `release_date` into a datetime column, created a `release_year` column, and converted song duration from milliseconds to minutes.

I also created an `energy_level` column that groups songs into low, medium, and high energy categories.

<iframe
  src="assets/energy-distribution.html"
  width="800"
  height="600"
  frameborder="0"
></iframe>

<iframe
  src="assets/popularity-distribution.html"
  width="800"
  height="600"
  frameborder="0"
></iframe>

I then examined the relationship between energy and popularity using scatter plots, box plots, groupby summaries, and pivot tables.

<iframe
  src="assets/energy-vs-popularity.html"
  width="800"
  height="600"
  frameborder="0"
></iframe>

<iframe
  src="assets/popularity-by-energy-level.html"
  width="800"
  height="600"
  frameborder="0"
></iframe>

## Assessment of Missingness

I chose `tempo` as the column with non-trivial missingness because about 19.4% of its values are missing.

I tested whether tempo missingness depends on `energy`, `popularity`, `danceability`, `valence`, and `acousticness`. The results showed that tempo missingness depends on energy, danceability, valence, and acousticness, but does not appear to depend on popularity.

This suggests that tempo is not missing completely at random. Instead, its missingness may be related to other audio features of the song.

## Hypothesis Testing

I tested whether high-energy songs tend to be more popular than low-energy songs.

**Null Hypothesis:** High-energy songs and low-energy songs have the same mean popularity.

**Alternative Hypothesis:** High-energy songs have higher mean popularity than low-energy songs.

**Test Statistic:** Mean popularity of high-energy songs minus mean popularity of low-energy songs.

Using a permutation test, I compared the observed difference in mean popularity to a distribution of shuffled differences. If the p-value is below 0.05, I reject the null hypothesis and conclude that there is evidence that high-energy songs have higher mean popularity.

## Framing a Prediction Problem

For my prediction problem, I predicted a song's `track_genre` using `acousticness` and `energy`.

This is a classification problem because `track_genre` is categorical. The goal is to predict which genre a song belongs to based on its audio features.

## Baseline Model

My baseline model used two features from the original dataset: `acousticness` and `energy`.

I used a logistic regression classifier inside a sklearn pipeline. The pipeline imputes missing values, standardizes the numerical features, and then trains the model. I evaluated the model on unseen test data using accuracy and balanced accuracy.

## Final Model

My final model improved on the baseline model by adding two engineered features:

- `energy_acousticness_interaction`
- `energy_minus_acousticness`

These features help capture how the relationship between energy and acousticness differs across genres.

I used a decision tree classifier and tuned the hyperparameters `max_depth` and `min_samples_leaf` using `GridSearchCV`. I evaluated the final model on the same unseen test set used for the baseline model.

## Fairness Analysis

For fairness analysis, I tested whether the final model is less accurate for high-energy songs than low-energy songs.

**Null Hypothesis:** The model has about the same accuracy for high-energy and low-energy songs.

**Alternative Hypothesis:** The model has lower accuracy for high-energy songs.

**Metric:** Accuracy.

I used a permutation test to compare the model's accuracy across the two groups. This allowed me to test whether any observed difference in accuracy was likely due to chance.
