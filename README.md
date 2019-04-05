## Smunch Customer Clustering and Meal Satisfaction Analysis
    
### Background:
Smunch is a rapidly growing B2B Food Delivery service based out of Germany, with their headquarters in Berlin. The general structure of Smunch consists of allowing employees of subscribing companies to choose an offered meal from local restaurants which Smuch packages and deliverers to the company. There are eight options per day (two restaurants with four options each). Each day the menu is changed and eight new meals are offered.

### Motivation:
As Smunch continues to expand and increase volume, it is extremely important to understand the trends and habits of their growing customer base. From a basic understanding of what meals are popular to an in-depth breakdown of what the key ingredients in meals, certain customers find most important, understanding what makes Smunch customers tick will allow Smunch to continuously improve their product and customer experience. More concretely having insights into key ingredients will allow Smunch to tailor meals to appeal to a wider customer base as well as increased order numbers. Understanding the factions or clusters of their customers and what they like will allow them to make sure each customer is presented with a good meal option every day. Other insights including identifying which customers are the most loyal and which customers churn or will allow for tailored efforts to increase customer retention and frequency of use. 

### Structure:
#### Clustering:
  - This folder attempts to clusters users based on their ingredient preferences. 
  - [cluster folder link](https://github.com/noahschumacher/smunch-user-food-analysis/tree/master/clustering "Clustering Folder")

#### Probabilty of Ordering Meal Prediction:
  - Folder contains model and information for predicting the successfulness of a meal compared to other offered meals.
  - [order prediction folder link](https://github.com/noahschumacher/smunch-user-food-analysis/tree/master/order_prediction "Probability Of Order Prediction Folder")

#### Average Meal Rating Prediction:
  - Predicting the average rating of meal by users based on the ingredients in the meal.
  - [rating prediction link](https://github.com/noahschumacher/smunch-user-food-analysis/tree/master/rating_prediction "Rating of Meal Prediction Folder")

#### Recommender (not focus of this project!!):
  - Simple recommender systems uses NMF.
  - Needs a lot of work until usable.
  - Performance is poor currently.
  - Hidden user topics show insights into meal groups.
  - [meal recommender folder link](https://github.com/noahschumacher/smunch-user-food-analysis/tree/master/recommender "Recomender Folder")


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
