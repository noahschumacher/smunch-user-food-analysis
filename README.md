## Smunch Customer Clustering and Meal Satisfaction Analysis
    
### Background:
Smunch is a rapidly growing B2B Food Delivery service based out of Germany, with their headquarters in Berlin. The general structure of Smunch consists of allowing employees of subscribing companies to choose an offered meal from local restaurants which Smuch packages and deliverers to the company. There are eight options per day (two restaurants with four options each). Each day the menu is changed and eight new meals are offered.

### Motivation:
As Smunch continues to expand and increase volume, it is extremely important to understand the trends and habits of their growing customer base. From a basic understanding of what meals are popular to an in-depth breakdown of what the key ingredients in meals, certain customers find most important, understanding what makes Smunch customers tick will allow Smunch to continuously improve their product and customer experience. More concretely having insights into key ingredients will allow Smunch to tailor meals to appeal to a wider customer base as well as increased order numbers. Understanding the factions or clusters of their customers and what they like will allow them to make sure each customer is presented with a good meal option every day. Other insights including identifying which customers are the most loyal and which customers churn or will allow for tailored efforts to increase customer retention and frequency of use. 

### Structure:
#### Clustering:
  - This folder attempts to clusters users based on their ingredient preferences.
  - Two types of clustering are used:
    1. K-Means
    2. Hierarchial
  - From inspection K-Means seems to reveal the most about the clusters.
  - The 3 significant clusters seem to be:
    1. Protien, Dairy heavy: 48.90%
    2. Vegan / Vegetarian: 39.71%
    3. Seafood / Asian ingredients: 11.39%
  - Dimensionality Reduction:
    1. PCA and tSNE dimensionality reduction were performed on the clusters.
    2. For both PCA and tSNE 2D and 3D plots were generated to help visualize the these clusters.
  - Cluster Profile Analysis:
    1. Radar plots for each cluster were created to help Smunch identify and use the important ingredients for each cluster.
    2. Thes Radar plots have been generated for 3 cluster groups (more to be made soon)
  - Other inspection is done on the hard labeled meals:
    1. From manually assigned meals in Smunch DB the meal group breakdowns are as follows
    1. Vegan: 2.2%
    2. Vegetarian / Vegan: 11% 
    3. Animal Protien: 10%

#### Probabilty of Ordering Meal Prediction:
  - Solution to bias present in the ratings.
  - Target value is now # of times ordered / # of times offered
  - Feature matrix are the ingredients the user has encountered.
  - Each user has their own model (each user has different ingredient preferences)
  - How it works:
    1. Present put x number of meals into user model.
    2. Assign meal to user with largest target value.
    3. Repeat for all users.
    4. Take # of users assigned each meal and divide by total # os users in model.
    5. Output: is the % of customer base who will order each meal.
  - Performance:
    1. When given four meal options model predicts customer % breakdown for each meal within 8%
    2. Baseline for four meal options is simply 25% for each meal.
    3. Model performs 20% better than baseline.

#### Average Meal Rating Prediction:
  - Predicting the average rating of meal by users based on the ingredients in the meal.
  - Feature and Target Description:
    - Example Table:
  - Several models attempted (listed in order of performance.)
    1. Random Forrest Regressor 1% lower MSE
    2. Gradient Boost Regressor 1% lower MSE
    3. Baseline (Avg of all meal ratings)
    4. Neural Network same as baseline.
  - Not much signal in ingredients alone to make model significant.
  - Realized ratings do not always depend on the quality or taste of the meal. In fact most bad ratings tend to come other factors besides taste. For example, delivery was late, meal was incorrect, meal was cold, etc.
  - Need a better target value.

#### Recommender (not focus of this project!!):
  - Simple recommender systems uses NMF.
  - Performance is poor currently.
  - Hidden user topics show insights into meal groups.


### Goals :
Bellow are the desired outcomes of the Smunch Customer and Meal Analysis:

- Clustering of customers based on ingredient preferences:
  - Motivation:
    - Customize menu so that each cluster of customers has a food option each day.
    - Understand what their largest customer base cares about and what features of meals are only liked by a small portion of the entire customer base.
- Identification of key ingredients in customer meal choice:
  - Motivation:
    - Allow Smunch to avoid negatively contributing ingredients to meals.
    - Work with restaurants to create other promising meals.
- Predict overall successfulness of meal compared to other offered meals based on ingredients:
   - Motivation:
    - Allow Smunch to compare different meal offering combinations to:
        1. See how well meals will performed compared to others.
        2. Make sure all user groups are given a decent meal choice.


### Potential Areas of Concern / Difficulty:
#### 1. Lack of a strong signal in individual ingredient importance. Meals are complex and the interaction of ingredients is what really makes up the taste. Individual ingredients might not encompass these complex relations.
#### 2. Comparing users who have been using Smunch for a long time vs recently started using Smunch:
  - Handling meals that have never been offered to a user.
  - Handling situations where meals have not been offered at the same time as other meals.
#### 3. Data Wrangling:
  - Large database with lots of connected tables could mean lots of time getting queries correct and performing analysis on the data.
#### 4. Unsupervised Learning:
  - Clustering users into groups might be hard to correctly identify or label the clusters
  - What to set the limit on the number of clusters to etc.
