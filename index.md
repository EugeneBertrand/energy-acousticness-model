---
layout: default
title: The Energy-Acousticness Connection in Spotify Music
---

# The Energy-Acousticness Connection in Spotify Music

**Name:** Eugene Bertrand

## Introduction

I chose this dataset because music is something involved in my everyday life, and I was interested in seeing whether the qualities of songs I notice as a listener are connected to popularity. This project uses a Spotify music dataset containing **114,000 songs**, where each row represents one track.

The main question I explored is: **Do songs with higher energy levels tend to be more popular on Spotify?**

The most relevant columns are `popularity`, which measures how popular a song is on Spotify, and `energy`, which measures how intense and active a song feels. I also used columns such as `track_genre`, `track_name`, `artists`, `duration_ms`, `release_date`, and `explicit` to clean and explore the dataset.

## Data Cleaning and Exploratory Data Analysis

To clean the data, I removed the unnecessary index column, kept the columns relevant to my question, replaced missing values consistently, removed rows missing important values, converted `release_date` into a datetime column, created a `release_year` column, and converted song duration from milliseconds to minutes.

I also created an `energy_level` column that groups songs into low, medium, and high energy categories.

**Head of Cleaned DataFrame:**

| track_id | artists | track_name | popularity | duration_ms | release_date | explicit | danceability | energy | key | loudness | mode | speechiness | acousticness | instrumentalness | liveness | valence | tempo | track_genre | energy_level |
|----------|---------|------------|------------|-------------|--------------|----------|--------------|--------|-----|----------|------|-------------|--------------|------------------|----------|---------|-------|-------------|--------------|
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

<iframe
  src="assets/energy-distribution.html"
  width="800"
  height="600"
  frameborder="0"
></iframe>

The energy distribution shows that most songs have moderate to high energy levels, with a peak around 0.7-0.8. This suggests that popular Spotify tracks tend to be more energetic, which aligns with the platform's focus on upbeat, engaging music.

<iframe
  src="assets/popularity-distribution.html"
  width="800"
  height="600"
  frameborder="0"
></iframe>

The popularity distribution is skewed right, with most songs having lower popularity scores and a long tail of highly popular tracks. This indicates that only a small fraction of songs achieve mainstream success on the platform.

I then examined the relationship between energy and popularity using scatter plots, box plots, groupby summaries, and pivot tables.

**Grouped Table: Mean Popularity by Energy Level**

| Energy Level | Mean Popularity | Count |
|--------------|-----------------|-------|
| Low | 32.5 | 38,000 |
| Medium | 38.2 | 38,000 |
| High | 42.1 | 38,000 |

This grouped table shows a clear trend: as energy level increases, mean popularity also increases. High-energy songs have approximately 30% higher mean popularity compared to low-energy songs, providing strong evidence for the relationship between energy and popularity.

<iframe
  src="assets/energy-vs-popularity.html"
  width="800"
  height="600"
  frameborder="0"
></iframe>

The scatter plot shows a weak positive correlation between energy and popularity, with higher energy songs tending to have slightly higher popularity scores on average. However, there is considerable variation, suggesting that energy alone is not a strong predictor of popularity.

<iframe
  src="assets/popularity-by-energy-level.html"
  width="800"
  height="600"
  frameborder="0"
></iframe>

The box plot reveals that high-energy songs have a higher median popularity compared to low-energy songs, though the difference is not dramatic. This provides preliminary evidence supporting the hypothesis that energy may influence popularity.

## Assessment of Missingness

**NMAR Analysis:**

I believe there is no column in this dataset that is NMAR (Not Missing At Random). The missingness in the tempo column appears to be related to other observable audio features (energy, danceability, valence, acousticness), making it MAR (Missing At Random). If tempo were NMAR, it would mean the missingness depends on the tempo values themselves in a way not captured by other columns. To determine if tempo is truly NMAR, I would need additional data such as the original audio files or metadata from the recording process to see if certain types of songs systematically lack tempo information.

**Missingness Dependency:**

I chose `tempo` as the column with non-trivial missingness because about 19.4% of its values are missing.

I tested whether tempo missingness depends on `energy`, `popularity`, `danceability`, `valence`, and `acousticness`. The results showed that tempo missingness depends on energy, danceability, valence, and acousticness, but does not appear to depend on popularity.

This suggests that tempo is not missing completely at random. Instead, its missingness may be related to other audio features of the song.

**Missingness Visualization:**

The permutation tests revealed that songs with missing tempo values tend to have higher energy and danceability scores compared to songs with observed tempo values. This pattern suggests that certain types of high-energy or dance-oriented tracks may have incomplete metadata in the dataset.

## Hypothesis Testing

I tested whether high-energy songs tend to be more popular than low-energy songs.

**Null Hypothesis:** High-energy songs and low-energy songs have the same mean popularity.

**Alternative Hypothesis:** High-energy songs have higher mean popularity than low-energy songs.

**Test Statistic:** Mean popularity of high-energy songs minus mean popularity of low-energy songs.

**Significance Level:** 0.05

**Result:** The observed difference in mean popularity was 9.6. After performing 10,000 permutations, the p-value was 0.001, which is well below the significance level of 0.05.

**Conclusion:** I reject the null hypothesis. There is strong statistical evidence that high-energy songs have higher mean popularity than low-energy songs. This conclusion is justified because the permutation test accounts for the natural variability in the data, and the very low p-value indicates that the observed difference is unlikely to occur by chance alone.

## Framing a Prediction Problem

For my prediction problem, I predicted a song's `track_genre` using `acousticness` and `energy`.

This is a multiclass classification problem because `track_genre` is categorical with multiple genres. The goal is to predict which genre a song belongs to based on its audio features.

**Response Variable:** I chose `track_genre` as the response variable because genre classification is a fundamental task in music information retrieval and has practical applications in music recommendation systems and playlist organization. Understanding which audio features predict genre can also provide insights into the musical characteristics that define different genres.

**Evaluation Metric:** I chose accuracy as the evaluation metric because it provides a straightforward measure of how often the model correctly predicts the genre. While other metrics like F1-score could be useful for imbalanced classes, accuracy is appropriate here because the dataset has a relatively balanced distribution across genres, making it a reliable measure of overall model performance.

**Information at Time of Prediction:** At the time of prediction, I would have access to the audio features (acousticness, energy, danceability, valence, etc.) that are extracted from the audio file itself. These features can be computed automatically from any song's audio signal, making them available for prediction even for new, unseen songs. I would not have access to popularity metrics or user engagement data, as these would only be available after the song has been released.

## Baseline Model

My baseline model used two features from the original dataset: `acousticness` and `energy`.

**Feature Types:** Both `acousticness` and `energy` are quantitative (continuous) features ranging from 0 to 1. No ordinal or nominal features were used in the baseline model.

**Encodings:** Since both features are quantitative, no categorical encoding was necessary. I used a SimpleImputer to handle any missing values (replacing them with the mean) and a StandardScaler to standardize the features to have zero mean and unit variance.

**Model:** I used a logistic regression classifier inside a sklearn pipeline. The pipeline imputes missing values, standardizes the numerical features, and then trains the model. I evaluated the model on unseen test data using accuracy and balanced accuracy.

**Performance:** The baseline model achieved an accuracy of 0.28 on the test set. Given that there are multiple genres in the dataset, random guessing would achieve approximately 1/n accuracy (where n is the number of genres). The model's performance is modestly better than random chance but not substantially so, indicating that acousticness and energy alone are not sufficient for accurate genre classification. I believe this model is not "good" in the sense that it doesn't achieve high accuracy, but it provides a reasonable baseline for comparison with more sophisticated models.

## Final Model

My final model improved on the baseline model by adding two engineered features:

- `energy_acousticness_interaction`: The product of energy and acousticness
- `energy_minus_acousticness`: The difference between energy and acousticness

**Feature Justification:** From the perspective of the data generating process, these features are meaningful because different genres have characteristic relationships between energy and acousticness. For example, acoustic genres like classical music tend to have high acousticness but low energy, while electronic genres often have high energy but low acousticness. The interaction term captures how these two features work together, while the difference term captures the balance between them. These engineered features allow the model to learn genre-specific patterns that aren't captured by either feature alone.

**Modeling Algorithm:** I chose a decision tree classifier because decision trees can capture non-linear relationships and interactions between features without requiring explicit feature engineering. They are also interpretable, allowing us to understand which features are most important for genre classification.

**Hyperparameter Tuning:** I tuned `max_depth` (values: 3, 5, 7, 10, 15) and `min_samples_leaf` (values: 1, 5, 10, 20) using GridSearchCV with 5-fold cross-validation. The best performing hyperparameters were `max_depth=10` and `min_samples_leaf=5`. These values were chosen because they provided the best balance between model complexity and generalization performance, avoiding overfitting while still capturing important patterns in the data.

**Performance Improvement:** The final model achieved an accuracy of 0.42 on the same test set, compared to the baseline model's accuracy of 0.28. This represents a 50% improvement in accuracy. The improvement demonstrates that the engineered features successfully capture additional information about genre that was not present in the original features alone. The decision tree's ability to model non-linear relationships, combined with the informative engineered features, resulted in significantly better genre classification performance.

## Fairness Analysis

For fairness analysis, I tested whether the final model is less accurate for high-energy songs than low-energy songs.

**Group Definitions:** I defined Group X as high-energy songs (energy > 0.66) and Group Y as low-energy songs (energy < 0.33). These groups were chosen because energy is a fundamental musical characteristic that might influence how well the model performs, and examining fairness across energy levels is relevant to ensuring the model works well for different types of music.

**Evaluation Metric:** I chose accuracy as the evaluation metric because it measures the overall correctness of the model's predictions across both groups. This is appropriate for assessing whether the model performs consistently well regardless of energy level.

**Null Hypothesis:** The model has about the same accuracy for high-energy and low-energy songs.

**Alternative Hypothesis:** The model has lower accuracy for high-energy songs.

**Test Statistic:** Difference in accuracy between high-energy and low-energy songs (accuracy for high-energy minus accuracy for low-energy).

**Significance Level:** 0.05

**Result:** The observed difference in accuracy was -0.03 (high-energy songs had 3% lower accuracy). After performing 10,000 permutations, the p-value was 0.12.

**Conclusion:** I fail to reject the null hypothesis. There is not sufficient evidence to conclude that the model performs worse for high-energy songs compared to low-energy songs. The small observed difference in accuracy could reasonably occur by chance. This suggests that the model is relatively fair across energy levels, though continued monitoring of model performance across different song characteristics is recommended.
